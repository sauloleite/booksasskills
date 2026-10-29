#!/usr/bin/env python3
"""Inspection report for a JSONL training dataset (first step of data processing).

Input:  a JSONL file, one JSON object per line (e.g. {"instruction": ..., "response": ...}).
Output: a plain-text report on stdout (or JSON with --json) containing:
  - row count, blank lines, unparseable lines, non-object rows
  - per field: presence, missing, empty (""/[]/{}/null), value types
  - per string field: length stats in characters and whitespace-separated words
    (min, mean, p50, p90, p99, max) plus a coarse word-length histogram
  - exact duplicate rows (all fields identical after JSON canonicalization)
  - duplicates on --key fields, and "conflicts": same key with different --target values
    (same instruction, different response), the pattern the chapter says to look for
  - --reverse: same --target value reached from different --key values

Standard library only; deterministic; no network.
Example:
  python3 inspect_jsonl.py data.jsonl --key instruction --target response
"""
import argparse
import json
import math
import sys
from collections import Counter, defaultdict


def pct(sorted_vals, q):
    """Nearest-rank percentile (q in 0..100) of an already sorted list."""
    if not sorted_vals:
        return None
    rank = max(1, math.ceil(q / 100 * len(sorted_vals)))
    return sorted_vals[rank - 1]


def stats(vals):
    s = sorted(vals)
    if not s:
        return {}
    return {"n": len(s), "min": s[0], "mean": round(sum(s) / len(s), 2),
            "p50": pct(s, 50), "p90": pct(s, 90), "p99": pct(s, 99), "max": s[-1]}


def histogram(vals, edges=(0, 1, 5, 20, 50, 100, 250, 500, 1000, 2000)):
    """Counts per bucket [edge_i, edge_{i+1}); last bucket is open-ended."""
    out = Counter()
    for v in vals:
        label = f">={edges[-1]}"
        for lo, hi in zip(edges, edges[1:]):
            if lo <= v < hi:
                label = f"{lo}-{hi - 1}"
                break
        out[label] += 1
    order = [f"{lo}-{hi - 1}" for lo, hi in zip(edges, edges[1:])] + [f">={edges[-1]}"]
    return [(b, out[b]) for b in order if out[b]]


def is_empty(v):
    return v is None or (isinstance(v, (str, list, dict)) and len(v if not isinstance(v, str) else v.strip()) == 0)


def keyof(row, fields):
    return json.dumps([row.get(f) for f in fields], sort_keys=True, ensure_ascii=False)


def inspect(path, key_fields, target_fields, max_examples):
    rows, bad_lines, blank, non_obj = [], [], 0, 0
    with open(path, encoding="utf-8") as fh:
        for ln, line in enumerate(fh, 1):
            if not line.strip():
                blank += 1
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as e:
                bad_lines.append((ln, str(e)))
                continue
            if not isinstance(obj, dict):
                non_obj += 1
                continue
            rows.append((ln, obj))

    fields = sorted({k for _, r in rows for k in r})
    per_field = {}
    for f in fields:
        present = [r[f] for _, r in rows if f in r]
        types = Counter(type(v).__name__ for v in present)
        strs = [v for v in present if isinstance(v, str)]
        info = {"present": len(present), "missing": len(rows) - len(present),
                "empty": sum(is_empty(v) for v in present), "types": dict(types)}
        if strs:
            words = [len(v.split()) for v in strs]
            info["chars"] = stats([len(v) for v in strs])
            info["words"] = stats(words)
            info["word_hist"] = histogram(words)
            info["distinct_values"] = len(set(strs))
        per_field[f] = info

    canon = Counter(json.dumps(r, sort_keys=True, ensure_ascii=False) for _, r in rows)
    exact_dup_rows = sum(c - 1 for c in canon.values() if c > 1)

    report = {"file": path, "rows": len(rows), "blank_lines": blank,
              "unparseable_lines": len(bad_lines), "non_object_rows": non_obj,
              "bad_line_examples": bad_lines[:max_examples], "fields": per_field,
              "exact_duplicate_rows": exact_dup_rows,
              "exact_duplicate_groups": sum(1 for c in canon.values() if c > 1)}

    if key_fields:
        groups = defaultdict(list)
        for ln, r in rows:
            groups[keyof(r, key_fields)].append((ln, r))
        dup_groups = {k: g for k, g in groups.items() if len(g) > 1}
        report["key_fields"] = key_fields
        report["key_duplicate_groups"] = len(dup_groups)
        report["key_duplicate_rows"] = sum(len(g) - 1 for g in dup_groups.values())
        if target_fields:
            conflicts = []
            for k, g in dup_groups.items():
                distinct = {keyof(r, target_fields) for _, r in g}
                if len(distinct) > 1:
                    conflicts.append({"key": k, "lines": [ln for ln, _ in g],
                                      "distinct_targets": len(distinct)})
            report["target_fields"] = target_fields
            report["conflicting_groups"] = len(conflicts)
            report["conflict_examples"] = conflicts[:max_examples]
    return report, rows


def reverse_check(rows, key_fields, target_fields, max_examples):
    groups = defaultdict(set)
    lines = defaultdict(list)
    for ln, r in rows:
        t = keyof(r, target_fields)
        groups[t].add(keyof(r, key_fields))
        lines[t].append(ln)
    hits = [{"target": t, "lines": lines[t], "distinct_keys": len(ks)}
            for t, ks in groups.items() if len(ks) > 1]
    return len(hits), hits[:max_examples]


def print_text(rep):
    p = print
    p(f"File: {rep['file']}")
    p(f"Rows: {rep['rows']}  blank lines: {rep['blank_lines']}  unparseable: "
      f"{rep['unparseable_lines']}  non-object: {rep['non_object_rows']}")
    for ln, err in rep["bad_line_examples"]:
        p(f"  bad line {ln}: {err}")
    p("")
    for f, info in rep["fields"].items():
        p(f"Field '{f}': present {info['present']}, missing {info['missing']}, "
          f"empty {info['empty']}, types {info['types']}")
        if "chars" in info:
            c, w = info["chars"], info["words"]
            p(f"  chars: min {c['min']} mean {c['mean']} p50 {c['p50']} p90 {c['p90']} "
              f"p99 {c['p99']} max {c['max']}")
            p(f"  words: min {w['min']} mean {w['mean']} p50 {w['p50']} p90 {w['p90']} "
              f"p99 {w['p99']} max {w['max']}")
            p("  word-length histogram: " + ", ".join(f"{b}: {n}" for b, n in info["word_hist"]))
            p(f"  distinct string values: {info['distinct_values']}")
    p("")
    p(f"Exact duplicate rows (extra copies): {rep['exact_duplicate_rows']} "
      f"in {rep['exact_duplicate_groups']} groups")
    if "key_fields" in rep:
        p(f"Duplicates on key {rep['key_fields']}: {rep['key_duplicate_rows']} extra rows "
          f"in {rep['key_duplicate_groups']} groups")
    if "target_fields" in rep:
        p(f"Conflicts (same key, different {rep['target_fields']}): {rep['conflicting_groups']} groups")
        for c in rep["conflict_examples"]:
            p(f"  lines {c['lines']}: {c['distinct_targets']} distinct targets for key {c['key'][:80]}")
    if "reverse_groups" in rep:
        p(f"Same {rep['target_fields']} from different keys: {rep['reverse_groups']} groups")
        for c in rep["reverse_examples"]:
            p(f"  lines {c['lines']}: {c['distinct_keys']} distinct keys for target {c['target'][:80]}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", help="JSONL file to inspect")
    ap.add_argument("--key", nargs="+", default=[], help="field(s) identifying the query, e.g. instruction")
    ap.add_argument("--target", nargs="+", default=[], help="field(s) holding the answer, e.g. response")
    ap.add_argument("--reverse", action="store_true",
                    help="also report identical targets produced from different keys")
    ap.add_argument("--max-examples", type=int, default=5, help="examples to list per finding")
    ap.add_argument("--json", action="store_true", help="emit the report as JSON")
    a = ap.parse_args()
    if a.reverse and not (a.key and a.target):
        ap.error("--reverse needs both --key and --target")
    rep, rows = inspect(a.path, a.key, a.target, a.max_examples)
    if a.reverse:
        rep["reverse_groups"], rep["reverse_examples"] = reverse_check(rows, a.key, a.target, a.max_examples)
    if a.json:
        json.dump(rep, sys.stdout, indent=2, ensure_ascii=False)
        print()
    else:
        print_text(rep)


if __name__ == "__main__":
    main()
