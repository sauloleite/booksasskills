#!/usr/bin/env python3
"""Component inventory and sizing analyzer (component-based decomposition).

Reads a CSV inventory of a monolith's namespaces and reports, per namespace:
statement count, percent of the codebase, z-score (distance from the mean in
sample standard deviations) and flags. It also checks namespace hygiene.

INPUT
  CSV with a header row. Required columns:
    namespace   dotted namespace or directory path (slashes are converted to dots)
    statements  number of source statements located directly in that namespace
  Optional columns:
    name        human readable component name
    files       number of source files directly in that namespace
  Rows with 0 statements are treated as pure container namespaces.

OUTPUT (stdout, plain text by default or JSON with --json)
  * one line per component: statements, percent, z-score, files, flags
  * summary: total statements, component count, mean, sample std dev
  * ORPHAN: namespaces holding code that are also extended by child
    namespaces (they should be flattened so code lives only in leaf nodes)
  * TOO_LARGE / TOO_SMALL: z-score beyond +/- --sd-threshold
  * OVER_PCT: percent above --max-percent (if given)
  * DENSE: statements per file above --max-stmts-per-file (if given)
  * shared-code metrics for leaf names matching --shared-leaf
  * repeated leaf names (possible duplicated domain logic), minus --exclude-leaf

Exit code is 0 unless --fail-on-flags is set and at least one flag fired,
which lets the script act as a CI fitness function.

Deterministic, standard library only, no network access.
"""
import argparse
import csv
import json
import math
import sys
from collections import defaultdict


def load(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        missing = {"namespace", "statements"} - set(reader.fieldnames or [])
        if missing:
            sys.exit(f"error: missing column(s): {', '.join(sorted(missing))}")
        for r in reader:
            ns = r["namespace"].strip().strip("/").replace("/", ".").replace("\\", ".")
            if not ns:
                continue
            files = r.get("files")
            rows.append({
                "namespace": ns,
                "name": (r.get("name") or "").strip() or ns,
                "statements": int(float(r["statements"])),
                "files": int(float(files)) if files not in (None, "") else None,
            })
    seen = set()
    for r in rows:
        if r["namespace"] in seen:
            sys.exit(f"error: duplicate namespace {r['namespace']}")
        seen.add(r["namespace"])
    return rows


def analyze(rows, args):
    names = {r["namespace"] for r in rows}
    # A namespace is a root (sub-domain) if any other namespace extends it.
    roots = {n for n in names for m in names if m != n and m.startswith(n + ".")}
    comps = [r for r in rows if r["statements"] > 0]
    total = sum(r["statements"] for r in comps)
    n = len(comps)
    mean = total / n if n else 0.0
    sd = math.sqrt(sum((r["statements"] - mean) ** 2 for r in comps) / (n - 1)) if n > 1 else 0.0

    results = []
    for r in sorted(comps, key=lambda x: -x["statements"]):
        pct = 100.0 * r["statements"] / total if total else 0.0
        z = (r["statements"] - mean) / sd if sd else 0.0
        flags = []
        if r["namespace"] in roots:
            flags.append("ORPHAN")
        if z > args.sd_threshold:
            flags.append("TOO_LARGE")
        if z < -args.sd_threshold:
            flags.append("TOO_SMALL")
        if args.max_percent is not None and pct > args.max_percent:
            flags.append("OVER_PCT")
        if (args.max_stmts_per_file is not None and r["files"]
                and r["statements"] / r["files"] > args.max_stmts_per_file):
            flags.append("DENSE")
        results.append({**r, "percent": round(pct, 2), "z": round(z, 2), "flags": flags})

    shared = [r for r in comps if r["namespace"].split(".")[-1] in args.shared_leaf]
    shared_stmts = sum(r["statements"] for r in shared)

    leaf_groups = defaultdict(list)
    for r in comps:
        if r["namespace"] not in roots:
            leaf_groups[r["namespace"].split(".")[-1]].append(r["namespace"])
    excluded = set(args.exclude_leaf) | set(args.shared_leaf)
    repeated = {k: sorted(v) for k, v in sorted(leaf_groups.items())
                if len(v) > 1 and k not in excluded}

    return {
        "summary": {
            "total_statements": total,
            "components": n,
            "mean": round(mean, 2),
            "std_dev": round(sd, 2),
            "sd_threshold": args.sd_threshold,
            "max_percent": args.max_percent,
        },
        "components": results,
        "orphan_namespaces": sorted(r["namespace"] for r in comps if r["namespace"] in roots),
        "shared_code": {
            "leaf_names": args.shared_leaf,
            "count": len(shared),
            "statements": shared_stmts,
            "percent": round(100.0 * shared_stmts / total, 2) if total else 0.0,
        },
        "repeated_leaf_names": repeated,
    }


def print_text(rep):
    s = rep["summary"]
    print(f"{'namespace':40} {'stmts':>8} {'pct':>6} {'z':>6} {'files':>6}  flags")
    for r in rep["components"]:
        files = "" if r["files"] is None else str(r["files"])
        print(f"{r['namespace']:40} {r['statements']:>8} {r['percent']:>6.2f} "
              f"{r['z']:>6.2f} {files:>6}  {','.join(r['flags'])}")
    print()
    print(f"total statements: {s['total_statements']}  components: {s['components']}  "
          f"mean: {s['mean']}  sample std dev: {s['std_dev']}")
    print(f"z threshold: +/-{s['sd_threshold']}  max percent: {s['max_percent']}")
    if rep["orphan_namespaces"]:
        print("orphaned code in root namespaces (flatten): " + ", ".join(rep["orphan_namespaces"]))
    sc = rep["shared_code"]
    print(f"shared components ({'/'.join(sc['leaf_names'])}): {sc['count']}, "
          f"{sc['statements']} statements, {sc['percent']}% of codebase")
    for leaf, nss in rep["repeated_leaf_names"].items():
        print(f"repeated leaf name '{leaf}': {', '.join(nss)}")


def main():
    p = argparse.ArgumentParser(description="Size components of a monolith from a CSV inventory "
                                "and flag outliers, orphaned code and shared-code share.")
    p.add_argument("csv", help="inventory CSV (columns: namespace, statements[, name, files])")
    p.add_argument("--sd-threshold", type=float, default=2.0,
                   help="flag components whose z-score exceeds +/- this value (default 2)")
    p.add_argument("--max-percent", type=float, default=None,
                   help="flag components above this percent of total statements")
    p.add_argument("--max-stmts-per-file", type=float, default=None,
                   help="flag components whose statements per file exceed this value")
    p.add_argument("--shared-leaf", nargs="*", default=["shared", "sharedcode", "commoncode"],
                   help="leaf names that denote shared code (default: shared sharedcode commoncode)")
    p.add_argument("--exclude-leaf", nargs="*", default=[],
                   help="leaf names to ignore when reporting repeated leaf names")
    p.add_argument("--json", action="store_true", help="emit JSON instead of text")
    p.add_argument("--fail-on-flags", action="store_true",
                   help="exit with status 1 if any component is flagged")
    args = p.parse_args()

    rep = analyze(load(args.csv), args)
    if args.json:
        print(json.dumps(rep, indent=2, sort_keys=True))
    else:
        print_text(rep)
    if args.fail_on_flags and any(r["flags"] for r in rep["components"]):
        sys.exit(1)


if __name__ == "__main__":
    main()
