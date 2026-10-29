#!/usr/bin/env python3
"""Validate a fine-tuning JSONL file for agent SFT (chat + tool calls) or DPO.

Inputs
  path            JSONL file, one JSON object per line.
  --format        sft | dpo | auto (default auto: decided per line by keys).
  --schemas FILE  optional JSON file: list of tool definitions, each either
                  {"name", "parameters"} or {"type": "function", "function": {...}}.
                  Per-record "tools" lists are also honored.
  --min-no-call-share X  warn if the share of SFT examples with no tool call
                  is below X (default 0.0 = only warn when there are none).
  --json          print the report as JSON instead of text.

SFT record: {"messages": [...], "tools": [...]?}  ("conversations" accepted).
  Roles: system (first only), user, assistant, tool. First non-system turn is
  user, last turn is assistant. Assistant tool calls are either OpenAI-style
  "tool_calls" [{"id","type":"function","function":{"name","arguments"}}] or
  inline <tool_call>{"name":..,"arguments":{..}}</tool_call> in content. Every
  call must be answered by a following "tool" message (matched by
  tool_call_id when ids exist) before the next user/assistant turn.
DPO record: {"prompt", "chosen", "rejected"} (strings or message lists).

Output
  Per-line errors and warnings plus summary stats (examples with and without
  tool calls, tools used, DPO length comparison). Exit code 1 if any error.
Deterministic, stdlib only, no network.
"""
import argparse
import json
import re
import sys
from collections import Counter

ROLES = {"system", "user", "assistant", "tool"}
INLINE_CALL = re.compile(r"<tool_call>(.*?)</tool_call>", re.S)
TYPE_CHECK = {
    "string": lambda v: isinstance(v, str),
    "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
    "boolean": lambda v: isinstance(v, bool),
    "array": lambda v: isinstance(v, list),
    "object": lambda v: isinstance(v, dict),
}


def load_schemas(tools):
    out = {}
    for t in tools or []:
        if not isinstance(t, dict):
            continue
        fn = t.get("function", t)
        if isinstance(fn, dict) and "name" in fn:
            out[fn["name"]] = fn.get("parameters") or {}
    return out


def check_args(name, args, schemas, err, warn):
    if name not in schemas:
        if schemas:
            err(f"call to unknown tool '{name}'")
        return
    params = schemas[name]
    props = params.get("properties", {})
    for req in params.get("required", []):
        if req not in args:
            err(f"tool '{name}' missing required argument '{req}'")
    for key, val in args.items():
        if key not in props:
            msg = f"tool '{name}' got unexpected argument '{key}'"
            (err if params.get("additionalProperties") is False else warn)(msg)
            continue
        typ = props[key].get("type")
        if isinstance(typ, str) and typ in TYPE_CHECK and not TYPE_CHECK[typ](val):
            err(f"tool '{name}' argument '{key}' should be {typ}")


def extract_calls(msg, err):
    """Return list of (id_or_None, name, args_dict) for an assistant message."""
    calls = []
    for tc in msg.get("tool_calls") or []:
        fn = tc.get("function", {}) if isinstance(tc, dict) else {}
        name, raw = fn.get("name"), fn.get("arguments", {})
        if not name:
            err("tool_call without function name")
            continue
        if isinstance(raw, str):
            try:
                raw = json.loads(raw)
            except json.JSONDecodeError:
                err(f"arguments for '{name}' are not valid JSON")
                continue
        if not isinstance(raw, dict):
            err(f"arguments for '{name}' must be a JSON object")
            continue
        calls.append((tc.get("id"), name, raw))
    content = msg.get("content") or ""
    if isinstance(content, str):
        for blob in INLINE_CALL.findall(content):
            try:
                obj = json.loads(blob)
            except json.JSONDecodeError:
                err("inline <tool_call> body is not valid JSON")
                continue
            if not isinstance(obj, dict) or "name" not in obj:
                err("inline <tool_call> needs a 'name' field")
                continue
            args = obj.get("arguments", {})
            if not isinstance(args, dict):
                err(f"inline arguments for '{obj['name']}' must be an object")
                continue
            calls.append((None, obj["name"], args))
        for tag in ("think", "tool_call"):
            if content.count(f"<{tag}>") != content.count(f"</{tag}>"):
                err(f"unbalanced <{tag}> tags in assistant content")
    return calls


def validate_sft(rec, global_schemas, err, warn, stats):
    msgs = rec.get("messages", rec.get("conversations"))
    if not isinstance(msgs, list) or not msgs:
        err("SFT record needs a non-empty 'messages' list")
        return
    schemas = dict(global_schemas)
    schemas.update(load_schemas(rec.get("tools")))
    pending, n_calls, prev_role = [], 0, None
    for i, m in enumerate(msgs):
        role = m.get("role") if isinstance(m, dict) else None
        if role not in ROLES:
            err(f"message {i}: invalid role {role!r}")
            return
        if role == "system" and i != 0:
            err(f"message {i}: system message must be first")
        if role != "tool" and pending:
            err(f"message {i}: {len(pending)} tool call(s) not answered before this {role} turn")
            pending = []
        if role == "tool":
            if not pending:
                err(f"message {i}: tool result without a preceding tool call")
            else:
                tid = m.get("tool_call_id")
                ids = [p for p in pending if p is not None]
                if ids and tid not in ids:
                    err(f"message {i}: tool_call_id {tid!r} matches no open call")
                pending.remove(tid if tid in pending else pending[0])
        elif role == "assistant":
            calls = extract_calls(m, lambda s, i=i: err(f"message {i}: {s}"))
            for cid, name, args in calls:
                check_args(name, args, schemas, lambda s, i=i: err(f"message {i}: {s}"),
                           lambda s, i=i: warn(f"message {i}: {s}"))
                stats["tools"][name] += 1
            if not calls and not (m.get("content") or "").strip():
                err(f"message {i}: empty assistant message")
            pending = [cid for cid, _, _ in calls]
            n_calls += len(calls)
        elif role == "user" and prev_role == "user":
            warn(f"message {i}: two consecutive user turns")
        prev_role = role
    first = next((m["role"] for m in msgs if m.get("role") != "system"), None)
    if first != "user":
        err("first non-system message must be from the user")
    if pending:
        err("conversation ends with unanswered tool call(s)")
    elif msgs[-1].get("role") != "assistant":
        err("conversation must end with an assistant turn")
    stats["sft"] += 1
    stats["with_call" if n_calls else "no_call"] += 1


def as_text(x):
    if isinstance(x, str):
        return x
    if isinstance(x, list):
        return " ".join(str(m.get("content", "")) for m in x if isinstance(m, dict))
    return None


def validate_dpo(rec, err, warn, stats):
    vals = {}
    for key in ("prompt", "chosen", "rejected"):
        t = as_text(rec.get(key))
        if t is None or not t.strip():
            err(f"DPO field '{key}' missing or empty")
            return
        vals[key] = t
    if " ".join(vals["chosen"].split()) == " ".join(vals["rejected"].split()):
        err("chosen and rejected are identical")
        return
    stats["dpo"] += 1
    stats["chosen_len"] += len(vals["chosen"])
    stats["rejected_len"] += len(vals["rejected"])
    stats["chosen_longer"] += len(vals["chosen"]) > len(vals["rejected"])


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("path")
    ap.add_argument("--format", choices=["sft", "dpo", "auto"], default="auto")
    ap.add_argument("--schemas")
    ap.add_argument("--min-no-call-share", type=float, default=0.0)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    global_schemas = {}
    if a.schemas:
        with open(a.schemas) as f:
            global_schemas = load_schemas(json.load(f))
    stats = Counter()
    stats["tools"] = Counter()
    errors, warnings, seen = [], [], {}
    with open(a.path) as f:
        for ln, line in enumerate(f, 1):
            if not line.strip():
                continue
            err = lambda s, ln=ln: errors.append(f"line {ln}: {s}")
            warn = lambda s, ln=ln: warnings.append(f"line {ln}: {s}")
            stats["lines"] += 1
            if line.strip() in seen:
                warn(f"exact duplicate of line {seen[line.strip()]}")
            seen.setdefault(line.strip(), ln)
            try:
                rec = json.loads(line)
            except json.JSONDecodeError as e:
                err(f"invalid JSON ({e.msg})")
                continue
            if not isinstance(rec, dict):
                err("record is not a JSON object")
                continue
            fmt = a.format
            if fmt == "auto":
                fmt = "dpo" if "chosen" in rec or "rejected" in rec else "sft"
            (validate_dpo(rec, err, warn, stats) if fmt == "dpo"
             else validate_sft(rec, global_schemas, err, warn, stats))

    summary = {"lines": stats["lines"], "errors": len(errors), "warnings": len(warnings)}
    if stats["sft"]:
        share = stats["no_call"] / stats["sft"]
        summary.update(sft_records=stats["sft"], with_tool_call=stats["with_call"],
                       no_tool_call=stats["no_call"], no_call_share=round(share, 3),
                       tool_usage=dict(sorted(stats["tools"].items())))
        if stats["no_call"] == 0 or share < a.min_no_call_share:
            warnings.append(f"dataset: no-call share {share:.1%} is low; add examples "
                            "where the right move is to answer without a tool")
    if stats["dpo"]:
        n = stats["dpo"]
        summary.update(dpo_valid_pairs=n, mean_chosen_chars=round(stats["chosen_len"] / n, 1),
                       mean_rejected_chars=round(stats["rejected_len"] / n, 1),
                       chosen_longer_share=round(stats["chosen_longer"] / n, 3))
    summary["warnings"] = len(warnings)
    if a.json:
        print(json.dumps({"summary": summary, "errors": errors, "warnings": warnings}, indent=2))
    else:
        for e in errors:
            print("ERROR  ", e)
        for w in warnings:
            print("WARN   ", w)
        print("SUMMARY", json.dumps(summary))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
