#!/usr/bin/env python3
"""Lint a JSON prompt catalog for the metadata a production prompt needs.

Input: a JSON file that is either a list of prompt records or an object
{"prompts": [...], "pins": {...}}. Each prompt record should contain:
  id, version (int), model, application, creator, date_created (YYYY-MM-DD),
  template (text with {{placeholder}} variables),
  sampling {temperature, top_p}, input_schema {name: type, ...},
  and output_schema when output_format is "json".
Optional: endpoint (http/https URL), output_format.
"pins" maps application -> {prompt_id: pinned_version}.

Checks: missing or empty required fields, duplicate (id, version), bad dates,
sampling values out of range (temperature 0..2, top_p in (0, 1]),
template placeholders missing from input_schema (error) or schema keys the
template never uses (warning), missing output_schema for JSON output,
pins that reference unknown prompts or versions (error), and pins behind the
latest version (info, so owners can re-evaluate and upgrade).

Output: one line per finding, then a summary. Exit code 1 if any error.
"""
import argparse
import datetime
import json
import re
import sys

REQUIRED = ["id", "version", "model", "application", "creator",
            "date_created", "template", "sampling", "input_schema"]
PLACEHOLDER = re.compile(r"\{\{\s*([A-Za-z_][A-Za-z0-9_]*)\s*\}\}")


def lint(data):
    findings = []  # (level, where, message)
    if isinstance(data, list):
        prompts, pins = data, {}
    else:
        prompts, pins = data.get("prompts", []), data.get("pins", {})

    seen = set()
    versions = {}  # id -> set of versions
    for i, p in enumerate(prompts):
        where = f"{p.get('id', '?')}@v{p.get('version', '?')} (#{i})"
        for field in REQUIRED:
            if field not in p or p[field] in ("", None, {}, []):
                findings.append(("ERROR", where, f"missing or empty '{field}'"))
        if not isinstance(p.get("version"), int):
            findings.append(("ERROR", where, "version must be an integer"))
        key = (p.get("id"), p.get("version"))
        if key in seen:
            findings.append(("ERROR", where, "duplicate id and version"))
        seen.add(key)
        versions.setdefault(p.get("id"), set()).add(p.get("version"))

        date = p.get("date_created")
        if date:
            try:
                datetime.date.fromisoformat(str(date))
            except ValueError:
                findings.append(("ERROR", where, f"date_created '{date}' is not YYYY-MM-DD"))

        s = p.get("sampling") or {}
        t, tp = s.get("temperature"), s.get("top_p")
        if s and t is None:
            findings.append(("ERROR", where, "sampling.temperature missing"))
        elif t is not None and not (isinstance(t, (int, float)) and 0 <= t <= 2):
            findings.append(("ERROR", where, f"temperature {t} outside 0..2"))
        if s and tp is None:
            findings.append(("ERROR", where, "sampling.top_p missing"))
        elif tp is not None and not (isinstance(tp, (int, float)) and 0 < tp <= 1):
            findings.append(("ERROR", where, f"top_p {tp} outside (0, 1]"))

        used = set(PLACEHOLDER.findall(p.get("template") or ""))
        schema = set((p.get("input_schema") or {}).keys())
        for name in sorted(used - schema):
            findings.append(("ERROR", where, f"placeholder '{name}' not in input_schema"))
        for name in sorted(schema - used):
            findings.append(("WARN", where, f"input_schema key '{name}' unused in template"))

        if p.get("output_format") == "json" and not p.get("output_schema"):
            findings.append(("ERROR", where, "output_format is json but output_schema missing"))
        ep = p.get("endpoint")
        if ep is None:
            findings.append(("WARN", where, "no endpoint recorded"))
        elif not re.match(r"^https?://", str(ep)):
            findings.append(("ERROR", where, f"endpoint '{ep}' is not an http(s) URL"))

    for app, mapping in sorted(pins.items()):
        for pid, ver in sorted(mapping.items()):
            where = f"pin {app} -> {pid}@v{ver}"
            if pid not in versions:
                findings.append(("ERROR", where, "unknown prompt id"))
            elif ver not in versions[pid]:
                findings.append(("ERROR", where, "pinned version does not exist"))
            else:
                latest = max(v for v in versions[pid] if isinstance(v, int))
                if ver < latest:
                    findings.append(("INFO", where, f"newer version v{latest} available"))
    return findings, len(prompts)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("catalog", help="path to the JSON prompt catalog")
    ap.add_argument("--strict", action="store_true", help="treat warnings as errors")
    args = ap.parse_args()
    with open(args.catalog, encoding="utf-8") as fh:
        findings, n = lint(json.load(fh))
    for level, where, msg in findings:
        print(f"{level:5} {where}: {msg}")
    errors = sum(1 for f in findings if f[0] == "ERROR")
    warns = sum(1 for f in findings if f[0] == "WARN")
    infos = sum(1 for f in findings if f[0] == "INFO")
    print(f"checked {n} prompts: {errors} errors, {warns} warnings, {infos} info")
    sys.exit(1 if errors or (args.strict and warns) else 0)


if __name__ == "__main__":
    main()
