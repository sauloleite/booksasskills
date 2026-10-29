#!/usr/bin/env python3
"""Summarize a Cobertura coverage.xml into actionable hotspots.

Coverage is treated as a feedback signal, not a target: the report points at
code that matters and is under-tested, and at trivial code that is being
tested anyway.

Inputs:
  coverage_xml        Path to a Cobertura-format XML report (produced by
                      coverage.py `coverage xml`, JaCoCo-to-Cobertura converters,
                      Istanbul/nyc `cobertura` reporter, gcovr --xml, etc.).
  --critical GLOB     Glob (repeatable) matching files that hold important
                      business logic. These are flagged when line coverage is
                      below --critical-min.
  --trivial GLOB      Glob (repeatable) matching data carriers, DTOs, config or
                      generated code. These are flagged when line coverage is
                      at or above --trivial-max (effort possibly misplaced).
  --top N             How many least-covered files and functions to list.
  --min-lines N       Ignore files/functions with fewer executable lines.
  --json              Emit JSON instead of text.

Outputs (stdout): overall line and branch rate, the N least-covered files and
functions (by line rate, ties broken by missed lines), and the flagged
critical/trivial files. Exit code is always 0 unless the XML cannot be read;
this tool informs, it does not gate.
"""
import argparse
import fnmatch
import json
import sys
import xml.etree.ElementTree as ET


def _rate(covered, total):
    return covered / total if total else 1.0


def _line_stats(lines_el):
    total = covered = b_total = b_covered = 0
    if lines_el is None:
        return total, covered, b_total, b_covered
    for ln in lines_el.findall("line"):
        total += 1
        if int(ln.get("hits", "0")) > 0:
            covered += 1
        if ln.get("branch") == "true":
            cc = ln.get("condition-coverage", "")
            # format: "50% (1/2)"
            if "(" in cc and "/" in cc:
                frac = cc[cc.index("(") + 1:cc.index(")")]
                c, t = frac.split("/")
                b_covered += int(c)
                b_total += int(t)
    return total, covered, b_total, b_covered


def analyze(path, min_lines):
    root = ET.parse(path).getroot()
    files = {}
    funcs = []
    for cls in root.iter("class"):
        fname = cls.get("filename") or cls.get("name")
        t, c, bt, bc = _line_stats(cls.find("lines"))
        agg = files.setdefault(fname, [0, 0, 0, 0])
        agg[0] += t
        agg[1] += c
        agg[2] += bt
        agg[3] += bc
        methods = cls.find("methods")
        if methods is not None:
            for m in methods.findall("method"):
                mt, mc, _, _ = _line_stats(m.find("lines"))
                if mt >= min_lines:
                    funcs.append({
                        "file": fname,
                        "function": m.get("name"),
                        "lines": mt,
                        "missed": mt - mc,
                        "line_rate": round(_rate(mc, mt), 4),
                    })
    file_rows = []
    tot = [0, 0, 0, 0]
    for fname, (t, c, bt, bc) in files.items():
        for i, v in enumerate((t, c, bt, bc)):
            tot[i] += v
        if t >= min_lines:
            file_rows.append({
                "file": fname,
                "lines": t,
                "missed": t - c,
                "line_rate": round(_rate(c, t), 4),
                "branch_rate": round(_rate(bc, bt), 4) if bt else None,
            })
    overall = {
        "line_rate": round(_rate(tot[1], tot[0]), 4),
        "branch_rate": round(_rate(tot[3], tot[2]), 4) if tot[2] else None,
        "lines": tot[0],
        "branches": tot[2],
    }
    key = lambda r: (r["line_rate"], -r["missed"], r.get("file", ""), r.get("function", ""))
    file_rows.sort(key=key)
    funcs.sort(key=key)
    return overall, file_rows, funcs


def _match(fname, globs):
    return any(fnmatch.fnmatch(fname, g) for g in globs)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("coverage_xml")
    ap.add_argument("--critical", action="append", default=[], metavar="GLOB")
    ap.add_argument("--trivial", action="append", default=[], metavar="GLOB")
    ap.add_argument("--critical-min", type=float, default=0.80,
                    help="flag critical files below this line rate (default 0.80)")
    ap.add_argument("--trivial-max", type=float, default=0.90,
                    help="flag trivial files at/above this line rate (default 0.90)")
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--min-lines", type=int, default=1)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    try:
        overall, files, funcs = analyze(a.coverage_xml, a.min_lines)
    except (OSError, ET.ParseError) as e:
        print(f"error: cannot read {a.coverage_xml}: {e}", file=sys.stderr)
        return 2

    crit = [f for f in files if _match(f["file"], a.critical) and f["line_rate"] < a.critical_min]
    triv = [f for f in files if _match(f["file"], a.trivial) and f["line_rate"] >= a.trivial_max]
    out = {
        "overall": overall,
        "least_covered_files": files[:a.top],
        "least_covered_functions": funcs[:a.top],
        "critical_under_tested": crit,
        "trivial_over_tested": triv,
    }
    if a.json:
        print(json.dumps(out, indent=2))
        return 0

    pct = lambda r: "n/a" if r is None else f"{100 * r:.1f}%"
    print(f"Overall: line {pct(overall['line_rate'])} of {overall['lines']} lines, "
          f"branch {pct(overall['branch_rate'])} of {overall['branches']} branches")
    print(f"\nLeast-covered files (top {a.top}):")
    for f in out["least_covered_files"]:
        print(f"  {pct(f['line_rate']):>7} line  {pct(f['branch_rate']):>7} branch  "
              f"missed {f['missed']:>4}  {f['file']}")
    print(f"\nLeast-covered functions (top {a.top}):")
    if not funcs:
        print("  (report has no method-level data)")
    for m in out["least_covered_functions"]:
        print(f"  {pct(m['line_rate']):>7}  missed {m['missed']:>4}  {m['file']}::{m['function']}")
    if a.critical:
        print(f"\nCritical code below {pct(a.critical_min)} (add behavior-checking tests here first):")
        for f in crit or []:
            print(f"  {pct(f['line_rate']):>7}  {f['file']}")
        if not crit:
            print("  none")
    if a.trivial:
        print(f"\nTrivial code at/above {pct(a.trivial_max)} (tests may be spent on code that needs none):")
        for f in triv:
            print(f"  {pct(f['line_rate']):>7}  {f['file']}")
        if not triv:
            print("  none")
    print("\nReminder: coverage shows what ran, not what was asserted. Review flagged tests for real assertions.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
