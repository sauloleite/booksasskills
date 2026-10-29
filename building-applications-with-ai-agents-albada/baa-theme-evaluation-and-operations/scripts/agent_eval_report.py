#!/usr/bin/env python3
"""Score agent runs against expected final states and apply release gates.

INPUT: a JSONL file, one agent run per line. Repeated runs of the same case
share a case_id (used for the consistency metric). Fields:
  case_id   str   required
  tags      list  optional, e.g. ["refund", "multi_item"] for per-slice metrics
  expected  obj   {"tool_calls": [{"tool": str, "params": {...}}],
                   "msg_contains": [str, ...],          # required phrases
                   "forbidden_tools": [str, ...]}       # must never be called
  actual    obj   {"tool_calls": [...], "final_message": str,
                   "latency_ms": num, "cost_usd": num, "steps": int,
                   "error": str|null}                   # crash => scored as failure

METRICS per run: tool_recall, tool_precision (multiset, so duplicate calls
count against precision), param_accuracy (expected calls matched with exact
params, numbers within --num-tol), phrase_recall (case-insensitive), forbidden
violation, task_success (all of: recall 1, precision 1, params 1, phrases 1,
no forbidden call, no error). Aggregates: means, Wilson 95% interval for
task_success, latency p50/p95, cost, steps, per-tag slices, and consistency
(share of repeated runs whose tool-call signature equals the case's modal one).

OUTPUT: human-readable report on stdout; optional JSON summary (--save).
Exit code 1 if any --gate threshold or --baseline regression check fails.

Example:
  python3 agent_eval_report.py runs.jsonl --gate tool_recall=0.95 \
      --gate task_success=0.9 --baseline last_release.json --max-drop 0.02
"""
import argparse
import json
import math
import sys
from collections import Counter, defaultdict

METRICS = ["tool_recall", "tool_precision", "param_accuracy",
           "phrase_recall", "task_success"]


def params_equal(a, b, tol):
    if isinstance(a, bool) or isinstance(b, bool):
        return a == b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return abs(a - b) <= tol
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(params_equal(a[k], b[k], tol) for k in a)
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(params_equal(x, y, tol) for x, y in zip(a, b))
    return a == b


def score_run(rec, tol):
    exp = rec.get("expected", {})
    act = rec.get("actual", {}) or {}
    exp_calls = exp.get("tool_calls", [])
    act_calls = act.get("tool_calls", []) or []
    exp_names = Counter(c["tool"] for c in exp_calls)
    act_names = Counter(c.get("tool") for c in act_calls)
    overlap = sum((exp_names & act_names).values())
    recall = overlap / sum(exp_names.values()) if exp_names else 1.0
    if act_names:
        precision = overlap / sum(act_names.values())
    else:
        precision = 1.0 if not exp_names else 0.0
    used, matched = set(), 0
    for e in exp_calls:
        for i, a in enumerate(act_calls):
            if i not in used and a.get("tool") == e["tool"] and \
                    params_equal(a.get("params", {}), e.get("params", {}), tol):
                used.add(i)
                matched += 1
                break
    param_acc = matched / len(exp_calls) if exp_calls else 1.0
    msg = (act.get("final_message") or "").lower()
    phrases = exp.get("msg_contains", [])
    phrase_rec = (sum(p.lower() in msg for p in phrases) / len(phrases)) if phrases else 1.0
    forbidden = sorted(set(exp.get("forbidden_tools", [])) & set(act_names))
    error = act.get("error")
    success = (not error and not forbidden and recall == 1.0 and precision == 1.0
               and param_acc == 1.0 and phrase_rec == 1.0)
    if error:
        recall = precision = param_acc = phrase_rec = 0.0
    sig = tuple(sorted(json.dumps(c, sort_keys=True) for c in act_calls))
    return {"tool_recall": recall, "tool_precision": precision,
            "param_accuracy": param_acc, "phrase_recall": phrase_rec,
            "task_success": 1.0 if success else 0.0, "forbidden": forbidden,
            "error": error, "sig": sig, "latency_ms": act.get("latency_ms"),
            "cost_usd": act.get("cost_usd"), "steps": act.get("steps")}


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    den = 1 + z * z / n
    mid = (p + z * z / (2 * n)) / den
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (max(0.0, mid - half), min(1.0, mid + half))


def pct(vals, q):
    vals = sorted(vals)
    if not vals:
        return None
    idx = max(0, math.ceil(q * len(vals)) - 1)  # nearest-rank
    return vals[idx]


def mean(vals):
    return sum(vals) / len(vals) if vals else None


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("runs", help="JSONL file of agent runs")
    ap.add_argument("--num-tol", type=float, default=0.005,
                    help="absolute tolerance for numeric params (default 0.005)")
    ap.add_argument("--gate", action="append", default=[],
                    help="metric=min_value, e.g. tool_recall=0.95 (repeatable)")
    ap.add_argument("--baseline", help="JSON summary from a previous --save")
    ap.add_argument("--max-drop", type=float, default=0.0,
                    help="allowed drop vs baseline per metric (default 0)")
    ap.add_argument("--save", help="write JSON summary here")
    args = ap.parse_args()

    scored, bad_lines = [], 0
    with open(args.runs) as fh:
        for ln, line in enumerate(fh, 1):
            if not line.strip():
                continue
            try:
                rec = json.loads(line)
                r = score_run(rec, args.num_tol)
            except (ValueError, KeyError, TypeError) as exc:
                bad_lines += 1
                print(f"[unparseable line {ln}] {exc!r} (counted as failure)", file=sys.stderr)
                rec, r = {"case_id": f"__line{ln}", "tags": []}, None
            if r is None:
                r = {m: 0.0 for m in METRICS}
                r.update(forbidden=[], error="unparseable", sig=(), latency_ms=None,
                         cost_usd=None, steps=None)
            r["case_id"], r["tags"] = rec.get("case_id"), rec.get("tags", [])
            scored.append(r)
    if not scored:
        sys.exit("no runs found")

    n = len(scored)
    summary = {"runs": n, "cases": len({r["case_id"] for r in scored}),
               "errors": sum(1 for r in scored if r["error"]),
               "forbidden_violations": sum(1 for r in scored if r["forbidden"])}
    for m in METRICS:
        summary[m] = round(mean([r[m] for r in scored]), 4)
    k = int(sum(r["task_success"] for r in scored))
    summary["task_success_ci95"] = [round(x, 4) for x in wilson(k, n)]
    lat = [r["latency_ms"] for r in scored if r["latency_ms"] is not None]
    cost = [r["cost_usd"] for r in scored if r["cost_usd"] is not None]
    steps = [r["steps"] for r in scored if r["steps"] is not None]
    summary["latency_ms_p50"], summary["latency_ms_p95"] = pct(lat, 0.5), pct(lat, 0.95)
    summary["cost_usd_total"] = round(sum(cost), 6) if cost else None
    summary["cost_usd_per_success"] = round(sum(cost) / k, 6) if cost and k else None
    summary["steps_mean"] = round(mean(steps), 2) if steps else None
    summary["steps_max"] = max(steps) if steps else None

    by_case = defaultdict(list)
    for r in scored:
        by_case[r["case_id"]].append(r["sig"])
    rep = {c: s for c, s in by_case.items() if len(s) > 1}
    if rep:
        agree = sum(Counter(s).most_common(1)[0][1] for s in rep.values())
        summary["consistency"] = round(agree / sum(len(s) for s in rep.values()), 4)
        summary["inconsistent_cases"] = sorted(c for c, s in rep.items() if len(set(s)) > 1)

    slices = defaultdict(list)
    for r in scored:
        for t in r["tags"]:
            slices[t].append(r)
    summary["slices"] = {t: {"runs": len(rs), **{m: round(mean([x[m] for x in rs]), 4)
                                                 for m in METRICS}}
                         for t, rs in sorted(slices.items())}
    summary["failed_cases"] = sorted({r["case_id"] for r in scored if not r["task_success"]})

    print(f"Runs: {n}  Cases: {summary['cases']}  Errors: {summary['errors']}  "
          f"Unparseable: {bad_lines}  Forbidden-tool violations: {summary['forbidden_violations']}")
    for m in METRICS:
        print(f"  {m:15s} {summary[m]:.3f}")
    lo, hi = summary["task_success_ci95"]
    print(f"  task_success 95% CI [{lo:.3f}, {hi:.3f}]")
    print(f"  latency_ms p50={summary['latency_ms_p50']} p95={summary['latency_ms_p95']}  "
          f"cost_total={summary['cost_usd_total']} cost/success={summary['cost_usd_per_success']}  "
          f"steps mean={summary['steps_mean']} max={summary['steps_max']}")
    if "consistency" in summary:
        print(f"  consistency (repeated runs) {summary['consistency']:.3f}  "
              f"unstable cases: {summary['inconsistent_cases']}")
    for t, s in summary["slices"].items():
        print(f"  [slice {t}] runs={s['runs']} " +
              " ".join(f"{m}={s[m]:.2f}" for m in METRICS))
    print(f"  failed cases: {summary['failed_cases']}")

    failures = []
    for g in args.gate:
        name, _, thr = g.partition("=")
        val = summary.get(name)
        if not isinstance(val, (int, float)):
            failures.append(f"gate {name}: metric unavailable")
        elif val < float(thr):
            failures.append(f"gate {name}: {val:.3f} < {float(thr):.3f}")
    if summary["forbidden_violations"]:
        failures.append(f"forbidden tool called in {summary['forbidden_violations']} run(s)")
    if args.baseline:
        with open(args.baseline) as fh:
            base = json.load(fh)
        for m in METRICS:
            if m in base and summary[m] < base[m] - args.max_drop:
                failures.append(f"regression {m}: {summary[m]:.3f} vs baseline {base[m]:.3f}")
        for t, s in summary["slices"].items():
            b = base.get("slices", {}).get(t)
            if b and s["task_success"] < b["task_success"] - args.max_drop:
                failures.append(f"regression slice {t}: task_success "
                                f"{s['task_success']:.3f} vs {b['task_success']:.3f}")
    if args.save:
        with open(args.save, "w") as fh:
            json.dump(summary, fh, indent=2)
    if failures:
        print("GATE: FAIL")
        for f in failures:
            print("  - " + f)
        sys.exit(1)
    print("GATE: PASS")


if __name__ == "__main__":
    main()
