#!/usr/bin/env python3
"""Evaluate agent tool selection against labeled expectations.

Input: a JSONL file, one case per line, e.g.
  {"id": "q1", "strategy": "semantic", "expected": ["get_weather"],
   "selected": ["get_weather"], "retrieved": ["get_weather", "get_time"],
   "latency_ms": 420}

Fields:
  expected    (required) list of tool names that should be called (may be empty)
  selected    (required) list of tool names the system actually chose
  strategy    (optional) label used to group results, default "default"
  retrieved   (optional) candidate tools surfaced before the final choice
              (semantic or hierarchical pipelines); enables candidate recall
  latency_ms  (optional) number; enables mean and p95 latency
  id          (optional) case identifier, used in the failure listing

Output (per strategy, text or --json):
  cases, exact-match accuracy (selected set == expected set),
  micro precision / recall / F1 over tool names,
  candidate recall (share of expected tools present in "retrieved"),
  mean and p95 latency, and the most frequent (expected -> wrongly chosen)
  pairs, which usually point at colliding tool descriptions.

Deterministic, standard library only, no network access.
"""
import argparse
import json
import math
import sys
from collections import Counter, defaultdict


def load_cases(path):
    cases = []
    with open(path, encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                c = json.loads(line)
            except json.JSONDecodeError as e:
                sys.exit(f"line {n}: invalid JSON ({e})")
            for key in ("expected", "selected"):
                if not isinstance(c.get(key), list):
                    sys.exit(f"line {n}: '{key}' must be a list")
            c.setdefault("id", f"line{n}")
            cases.append(c)
    return cases


def p95(values):
    if not values:
        return None
    s = sorted(values)
    idx = max(0, math.ceil(0.95 * len(s)) - 1)  # nearest-rank method
    return s[idx]


def evaluate(cases, top_confusions):
    groups = defaultdict(list)
    for c in cases:
        groups[c.get("strategy", "default")].append(c)
    report = {}
    for strat in sorted(groups):
        tp = fp = fn = exact = 0
        cand_hit = cand_total = 0
        lat = []
        confusions = Counter()
        failures = []
        for c in groups[strat]:
            exp, sel = set(c["expected"]), set(c["selected"])
            tp += len(exp & sel)
            fp += len(sel - exp)
            fn += len(exp - sel)
            if exp == sel:
                exact += 1
            else:
                failures.append(c["id"])
                missed, extra = sorted(exp - sel), sorted(sel - exp)
                for m in missed or ["<none>"]:
                    for x in extra or ["<none>"]:
                        confusions[(m, x)] += 1
            if isinstance(c.get("retrieved"), list):
                ret = set(c["retrieved"])
                cand_total += len(exp)
                cand_hit += len(exp & ret)
            if isinstance(c.get("latency_ms"), (int, float)):
                lat.append(float(c["latency_ms"]))
        n = len(groups[strat])
        prec = tp / (tp + fp) if tp + fp else None
        rec = tp / (tp + fn) if tp + fn else None
        f1 = (2 * prec * rec / (prec + rec)) if prec and rec else (0.0 if prec is not None and rec is not None else None)
        report[strat] = {
            "cases": n,
            "exact_match_accuracy": exact / n,
            "precision": prec,
            "recall": rec,
            "f1": f1,
            "candidate_recall": cand_hit / cand_total if cand_total else None,
            "mean_latency_ms": sum(lat) / len(lat) if lat else None,
            "p95_latency_ms": p95(lat),
            "top_confusions": [
                {"expected": e, "chosen": x, "count": k}
                for (e, x), k in sorted(confusions.items(), key=lambda kv: (-kv[1], kv[0]))[:top_confusions]
            ],
            "failed_case_ids": failures,
        }
    return report


def fmt(v, pct=False):
    if v is None:
        return "n/a"
    return f"{100 * v:.1f}%" if pct else f"{v:.1f}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cases", help="path to JSONL file of labeled tool-selection cases")
    ap.add_argument("--top", type=int, default=5, help="number of confusion pairs to show (default 5)")
    ap.add_argument("--json", action="store_true", help="print machine-readable JSON")
    args = ap.parse_args()

    report = evaluate(load_cases(args.cases), args.top)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
        return
    for strat, r in report.items():
        print(f"== strategy: {strat} ({r['cases']} cases)")
        print(f"  exact-match accuracy : {fmt(r['exact_match_accuracy'], True)}")
        print(f"  precision            : {fmt(r['precision'], True)}")
        print(f"  recall               : {fmt(r['recall'], True)}")
        print(f"  F1                   : {fmt(r['f1'], True)}")
        print(f"  candidate recall     : {fmt(r['candidate_recall'], True)}")
        print(f"  mean / p95 latency ms: {fmt(r['mean_latency_ms'])} / {fmt(r['p95_latency_ms'])}")
        if r["top_confusions"]:
            print("  most frequent errors (expected -> chosen):")
            for c in r["top_confusions"]:
                print(f"    {c['expected']} -> {c['chosen']}  x{c['count']}")
        if r["failed_case_ids"]:
            print(f"  failed cases: {', '.join(r['failed_case_ids'])}")


if __name__ == "__main__":
    main()
