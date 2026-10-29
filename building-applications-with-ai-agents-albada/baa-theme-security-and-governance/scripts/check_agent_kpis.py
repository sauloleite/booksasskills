#!/usr/bin/env python3
"""Check an agent metrics snapshot against default alert thresholds.

Default thresholds follow the monitoring KPIs suggested in Chapter 12 of
Albada's "Building Applications with AI Agents":
  error_rate         > 0.05 over the rolling window (fraction, 0..1)
  p99_latency_s      > 2.0 seconds on critical operations
  cpu/gpu/memory     >= 0.80 sustained utilization (fraction, 0..1)
  anomaly_score      < 0.85 (e.g. semantic similarity to expected output)
  state_conflicts    > 0 race/sync failures (multiagent setups)

INPUT: JSON file with one snapshot object or a list of snapshots, e.g.
  {"agent": "planner", "window_minutes": 60, "tasks": 400, "failed_tasks": 26,
   "p99_latency_s": 1.4, "cpu_util": 0.62, "gpu_util": 0.85,
   "memory_util": 0.55, "anomaly_score": 0.91, "state_conflicts": 0}
error_rate may be given directly, or derived from failed_tasks / tasks.
Missing metrics are reported as SKIP. A window under 60 minutes produces a
note because the error-rate default assumes a one-hour rolling window.

OUTPUT: one line per metric (OK / ALERT / SKIP) per snapshot, or JSON with
--json. Exit code 1 if any ALERT, else 0.
"""
import argparse
import json
import sys


def evaluate(snap, th):
    rows = []

    def row(metric, value, status, rule):
        rows.append({"metric": metric, "value": value, "status": status, "rule": rule})

    er = snap.get("error_rate")
    if er is None and snap.get("tasks"):
        er = snap.get("failed_tasks", 0) / snap["tasks"]
    rule = f"> {th.error_rate_max}"
    if er is None:
        row("error_rate", None, "SKIP", rule)
    else:
        row("error_rate", round(er, 4), "ALERT" if er > th.error_rate_max else "OK", rule)

    checks = [
        ("p99_latency_s", lambda v: v > th.p99_max, f"> {th.p99_max}"),
        ("cpu_util", lambda v: v >= th.util_max, f">= {th.util_max}"),
        ("gpu_util", lambda v: v >= th.util_max, f">= {th.util_max}"),
        ("memory_util", lambda v: v >= th.util_max, f">= {th.util_max}"),
        ("anomaly_score", lambda v: v < th.anomaly_min, f"< {th.anomaly_min}"),
        ("state_conflicts", lambda v: v > th.conflicts_max, f"> {th.conflicts_max}"),
    ]
    for metric, bad, rule in checks:
        v = snap.get(metric)
        if v is None:
            row(metric, None, "SKIP", rule)
        else:
            row(metric, v, "ALERT" if bad(v) else "OK", rule)

    notes = []
    win = snap.get("window_minutes")
    if win is not None and win < 60:
        notes.append("window under 60 min; error-rate default assumes a rolling hour")
    return rows, notes


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("metrics", help="path to metrics JSON (object or list)")
    ap.add_argument("--error-rate-max", type=float, default=0.05)
    ap.add_argument("--p99-max", type=float, default=2.0, help="seconds")
    ap.add_argument("--util-max", type=float, default=0.80)
    ap.add_argument("--anomaly-min", type=float, default=0.85)
    ap.add_argument("--conflicts-max", type=int, default=0)
    ap.add_argument("--json", action="store_true", help="emit JSON")
    th = ap.parse_args()

    with open(th.metrics, encoding="utf-8") as fh:
        data = json.load(fh)
    snaps = data if isinstance(data, list) else [data]

    report, any_alert = [], False
    for i, snap in enumerate(snaps):
        rows, notes = evaluate(snap, th)
        any_alert |= any(r["status"] == "ALERT" for r in rows)
        report.append({"agent": snap.get("agent", f"snapshot-{i}"),
                       "results": rows, "notes": notes})

    if th.json:
        print(json.dumps(report, indent=2))
    else:
        for rep in report:
            alerts = sum(r["status"] == "ALERT" for r in rep["results"])
            print(f"== {rep['agent']}: {alerts} alert(s)")
            for r in rep["results"]:
                print(f"  {r['status']:5} {r['metric']:15} value={r['value']} rule={r['rule']}")
            for n in rep["notes"]:
                print(f"  NOTE  {n}")
    sys.exit(1 if any_alert else 0)


if __name__ == "__main__":
    main()
