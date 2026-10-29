#!/usr/bin/env python3
"""Percentile latency report and goodput against an SLO, from a CSV of request timings.

Input: a CSV file with a header row. Recognized columns (others ignored):
    ttft_ms        time to first token (required)
    tpot_ms        time per output token (optional)
    output_tokens  output token count (optional; enables total latency)
    total_ms       total latency (optional; overrides ttft + tpot x tokens)
    start_s        request start time in seconds (optional; sets the window)

Output: count, mean, p50/p90/p95/p99 and max for each available metric
(nearest-rank percentiles), the share of requests meeting the SLO, throughput
and goodput in requests per minute when a time window is known (--window-s, or
the span of start_s values), and a warning when the mean exceeds 1.5x the median.

Example:
    python3 latency_report.py timings.csv --slo-ttft-ms 500 --slo-tpot-ms 50 --window-s 60
"""
import argparse
import csv
import math
import sys


def pct(sorted_vals, q):
    """Nearest-rank percentile (q in 0..100) of an ascending list."""
    if not sorted_vals:
        return float("nan")
    k = max(1, math.ceil(q / 100 * len(sorted_vals)))
    return sorted_vals[k - 1]


def summarize(name, vals):
    v = sorted(vals)
    mean = sum(v) / len(v)
    p50 = pct(v, 50)
    print(f"{name:<10} n={len(v):<5} mean={mean:9.1f} p50={p50:9.1f} p90={pct(v, 90):9.1f} "
          f"p95={pct(v, 95):9.1f} p99={pct(v, 99):9.1f} max={v[-1]:9.1f}")
    if p50 > 0 and mean > 1.5 * p50:
        print(f"  warning: {name} mean is {mean / p50:.1f}x the median; inspect outliers")


def main(argv=None):
    p = argparse.ArgumentParser(description="Latency percentiles and goodput from request timings.")
    p.add_argument("csv_path", help="CSV with ttft_ms and optional tpot_ms, output_tokens, "
                                    "total_ms, start_s columns")
    p.add_argument("--slo-ttft-ms", type=float, help="max acceptable TTFT")
    p.add_argument("--slo-tpot-ms", type=float, help="max acceptable TPOT")
    p.add_argument("--slo-total-ms", type=float, help="max acceptable total latency")
    p.add_argument("--window-s", type=float, help="measurement window in seconds for RPM/goodput")
    a = p.parse_args(argv)

    rows = []
    with open(a.csv_path, newline="") as f:
        for r in csv.DictReader(f):
            def num(k):
                x = (r.get(k) or "").strip()
                return float(x) if x else None
            row = {k: num(k) for k in ("ttft_ms", "tpot_ms", "output_tokens", "total_ms", "start_s")}
            if row["ttft_ms"] is None:
                continue
            if row["total_ms"] is None and row["tpot_ms"] is not None and row["output_tokens"] is not None:
                row["total_ms"] = row["ttft_ms"] + row["tpot_ms"] * row["output_tokens"]
            rows.append(row)
    if not rows:
        print("No rows with ttft_ms found.")
        return 1

    for key, label in (("ttft_ms", "TTFT ms"), ("tpot_ms", "TPOT ms"), ("total_ms", "Total ms")):
        vals = [r[key] for r in rows if r[key] is not None]
        if vals:
            summarize(label, vals)

    def ok(r):
        checks = (("ttft_ms", a.slo_ttft_ms), ("tpot_ms", a.slo_tpot_ms), ("total_ms", a.slo_total_ms))
        for key, limit in checks:
            if limit is not None and (r[key] is None or r[key] > limit):
                return False
        return True

    good = sum(1 for r in rows if ok(r))
    has_slo = any(x is not None for x in (a.slo_ttft_ms, a.slo_tpot_ms, a.slo_total_ms))
    if has_slo:
        print(f"SLO met: {good}/{len(rows)} requests ({100 * good / len(rows):.1f}%)")

    window = a.window_s
    starts = [r["start_s"] for r in rows if r["start_s"] is not None]
    if window is None and len(starts) >= 2 and max(starts) > min(starts):
        window = max(starts) - min(starts)
        print(f"Window inferred from start_s span: {window:.1f} s")
    if window:
        print(f"Throughput: {len(rows) * 60 / window:.1f} requests/min")
        if has_slo:
            print(f"Goodput:    {good * 60 / window:.1f} requests/min meeting the SLO")
    return 0


if __name__ == "__main__":
    sys.exit(main())
