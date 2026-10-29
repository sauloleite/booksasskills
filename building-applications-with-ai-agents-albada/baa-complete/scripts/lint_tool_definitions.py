#!/usr/bin/env python3
"""Lint a set of agent tool definitions for selection and safety problems.

Input
  A JSON file containing either a list of tool definitions or an object with a
  "tools" list. Each definition may be in any of these shapes:
    OpenAI style    {"type": "function", "function": {"name", "description", "parameters"}}
    Flat / OpenAI   {"name", "description", "parameters"}
    Anthropic style {"name", "description", "input_schema"}
    MCP style       {"name", "description", "inputSchema"}

Checks (severity in brackets)
  names        missing [E], not snake_case or camelCase [W], too generic or
               single-word catch-all [W], duplicates [E]
  descriptions missing [E], shorter than --min-desc-words [W], near-duplicate
               of another tool (Jaccard over content words >= --overlap-threshold) [W]
  schema       missing or not type "object" [E], parameter without type [E],
               parameter without description [W], no "required" list while
               parameters exist [W], required name not defined [E],
               additionalProperties not false [I], short closed-set hint
               ("one of", "either") without enum [I]
  power        free-form high-power parameter (sql, query, code, command,
               script, shell, url, path) [W]; destructive verb in name
               (delete, drop, remove, update, write...) [I], or [E] with --read-only

Output
  Human-readable report on stdout (or JSON with --json). Exit code 1 if any
  error-level finding exists, else 0.

Deterministic, standard library only, no network.
"""
import argparse
import json
import re
import sys
from itertools import combinations

GENERIC_NAMES = {
    "tool", "run", "execute", "exec", "do", "call", "query", "search", "get",
    "fetch", "data", "helper", "util", "utils", "process", "handle", "action",
    "api", "request", "function", "task", "lookup", "misc", "general",
}
HIGH_POWER_PARAMS = {
    "sql", "query", "code", "command", "cmd", "script", "shell", "expression",
    "statement", "url", "path", "filepath", "file_path",
}
DESTRUCTIVE_VERBS = {
    "delete", "drop", "remove", "truncate", "update", "write", "modify",
    "alter", "insert", "create", "set", "put", "patch", "send", "pay",
    "transfer", "cancel", "purge", "overwrite", "execute", "exec", "run",
}
STOPWORDS = {
    "a", "an", "the", "and", "or", "of", "to", "for", "in", "on", "by", "with",
    "is", "it", "this", "that", "from", "as", "at", "be", "use", "returns",
    "return", "given", "tool", "function", "will", "can", "if", "its", "into",
}
NAME_OK = re.compile(r"^[a-z][a-z0-9]*(_[a-z0-9]+)*$|^[a-z][a-zA-Z0-9]*$")
CLOSED_SET_HINT = re.compile(r"\b(one of|either|must be|allowed values)\b", re.I)


def normalize(raw):
    """Return (name, description, schema) for any supported shape."""
    if isinstance(raw.get("function"), dict):
        raw = raw["function"]
    schema = raw.get("parameters") or raw.get("input_schema") or raw.get("inputSchema")
    return raw.get("name"), raw.get("description"), schema


def content_words(text):
    return {w for w in re.findall(r"[a-z0-9]+", (text or "").lower())
            if w not in STOPWORDS and len(w) > 2}


def name_tokens(name):
    spaced = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name or "")
    return [t for t in re.split(r"[^a-z0-9]+", spaced.lower()) if t]


def lint(tools, min_desc_words, overlap_threshold, read_only):
    findings = []

    def add(sev, tool, msg):
        findings.append({"severity": sev, "tool": tool, "message": msg})

    seen = {}
    descs = {}
    for idx, raw in enumerate(tools):
        if not isinstance(raw, dict):
            add("E", f"#{idx}", "definition is not an object")
            continue
        name, desc, schema = normalize(raw)
        label = name or f"#{idx}"
        if not name:
            add("E", label, "missing name")
        else:
            if name in seen:
                add("E", label, f"duplicate name (also tool #{seen[name]})")
            seen[name] = idx
            if not NAME_OK.match(name):
                add("W", label, "name is not snake_case or camelCase")
            toks = name_tokens(name)
            if name.lower() in GENERIC_NAMES or (len(toks) == 1 and toks[0] in GENERIC_NAMES):
                add("W", label, "name is generic; models may call it when it does not apply")
            elif len(toks) == 1:
                add("I", label, "single-word name; consider verb_object form")
            verbs = DESTRUCTIVE_VERBS.intersection(toks)
            if verbs:
                sev = "E" if read_only else "I"
                add(sev, label, f"state-changing verb in name ({', '.join(sorted(verbs))})"
                    + ("; not allowed for a read-only agent" if read_only else
                       "; confirm least privilege, logging and approval"))
        if not desc or not str(desc).strip():
            add("E", label, "missing description")
        else:
            n = len(str(desc).split())
            if n < min_desc_words:
                add("W", label, f"description has {n} words (< {min_desc_words}); say what is distinct and when to use it")
            descs[label] = content_words(desc)
        check_schema(label, schema, desc, add)

    for (a, wa), (b, wb) in combinations(descs.items(), 2):
        if not wa or not wb:
            continue
        j = len(wa & wb) / len(wa | wb)
        if j >= overlap_threshold:
            add("W", a, f"description overlaps with '{b}' (Jaccard {j:.2f}); differentiate them")
    return findings


def check_schema(label, schema, desc, add):
    if schema is None:
        add("E", label, "missing input schema")
        return
    if not isinstance(schema, dict) or schema.get("type") != "object":
        add("E", label, 'input schema must be an object with "type": "object"')
        return
    props = schema.get("properties") or {}
    required = schema.get("required")
    if props and not required:
        add("W", label, 'no "required" list; mark mandatory parameters')
    for r in required or []:
        if r not in props:
            add("E", label, f"required parameter '{r}' is not defined in properties")
    if props and schema.get("additionalProperties") is not False:
        add("I", label, "additionalProperties is not false; strict schemas reduce misfires")
    for pname, p in props.items():
        if not isinstance(p, dict):
            add("E", label, f"parameter '{pname}' definition is not an object")
            continue
        if "type" not in p and not any(k in p for k in ("enum", "anyOf", "oneOf", "$ref", "const")):
            add("E", label, f"parameter '{pname}' has no type")
        if not p.get("description"):
            add("W", label, f"parameter '{pname}' has no description")
        if p.get("type") == "string" and "enum" not in p and CLOSED_SET_HINT.search(p.get("description", "")):
            add("I", label, f"parameter '{pname}' describes a closed set; use an enum")
        if pname.lower() in HIGH_POWER_PARAMS and p.get("type", "string") == "string" \
                and "enum" not in p and "pattern" not in p:
            add("W", label, f"free-form high-power parameter '{pname}'; prefer narrow operations or validate and sanitize")


def main():
    ap = argparse.ArgumentParser(description="Lint agent tool definitions (names, descriptions, schemas, power).")
    ap.add_argument("file", help="JSON file with a list of tools or {\"tools\": [...]}")
    ap.add_argument("--min-desc-words", type=int, default=8, help="minimum words per description (default 8)")
    ap.add_argument("--overlap-threshold", type=float, default=0.5,
                    help="Jaccard threshold for near-duplicate descriptions (default 0.5)")
    ap.add_argument("--read-only", action="store_true", help="treat state-changing tools as errors")
    ap.add_argument("--json", action="store_true", help="emit findings as JSON")
    args = ap.parse_args()

    with open(args.file, encoding="utf-8") as fh:
        data = json.load(fh)
    tools = data.get("tools", []) if isinstance(data, dict) else data
    if not isinstance(tools, list):
        sys.exit("input must be a list of tools or an object with a 'tools' list")

    findings = lint(tools, args.min_desc_words, args.overlap_threshold, args.read_only)
    counts = {s: sum(f["severity"] == s for f in findings) for s in "EWI"}
    if args.json:
        print(json.dumps({"tools": len(tools), "counts": counts, "findings": findings}, indent=2))
    else:
        order = {"E": 0, "W": 1, "I": 2}
        for f in sorted(findings, key=lambda f: (order[f["severity"]], f["tool"])):
            print(f"[{f['severity']}] {f['tool']}: {f['message']}")
        print(f"\n{len(tools)} tools checked: {counts['E']} errors, {counts['W']} warnings, {counts['I']} info")
    return 1 if counts["E"] else 0


if __name__ == "__main__":
    sys.exit(main())
