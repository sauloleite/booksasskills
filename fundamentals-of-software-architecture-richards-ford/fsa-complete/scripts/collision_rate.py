#!/usr/bin/env python3
"""Estimate replicated-cache data collisions in a space-based architecture.

Model (Richards and Ford, FSA 2nd ed., ch. 16):
    collisions_per_second = N * UR**2 / S * RL
where
    N  = processing-unit instances sharing the same named replicated cache
    UR = update rate of that cache, in updates per second
    S  = cache size, in rows (entries)
    RL = replication latency, in SECONDS (input is given in ms and converted)

Units note: the book labels UR and RL as milliseconds, but its own worked
numbers only reproduce when UR is per second and RL is converted to seconds
(20 upd/s, N=5, S=50,000, RL=100 ms -> 14.4 collisions/hour, 0.02%).
This script uses that consistent interpretation.

Inputs (CLI):
    --instances N --rows S [--rl-ms 100] and either
    --rate UR             a single update rate (updates/second), or
    --scenario NAME=UR    repeatable, e.g. min, normal and peak rates.
    --threshold-pct P     optional: flag scenarios whose collision % exceeds P.
Output: a plain-text table per scenario with updates/hour, collisions/hour
and collisions as a percentage of updates. Deterministic, stdlib only.
"""
import argparse
import sys


def collisions_per_hour(n, rate, rows, rl_ms):
    per_second = n * (rate ** 2) / rows * (rl_ms / 1000.0)
    return per_second * 3600.0


def parse_scenario(text):
    if "=" not in text:
        raise argparse.ArgumentTypeError("scenario must look like NAME=RATE")
    name, value = text.split("=", 1)
    try:
        rate = float(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"rate in {text!r} is not a number")
    if rate < 0:
        raise argparse.ArgumentTypeError("rate must be >= 0")
    return name.strip() or "scenario", rate


def main(argv=None):
    p = argparse.ArgumentParser(
        description="Estimate hourly data collisions for a replicated cache "
        "(space-based architecture, FSA ch. 16).")
    p.add_argument("--instances", "-n", type=int, required=True,
                   help="processing-unit instances sharing the named cache")
    p.add_argument("--rows", "-s", type=int, required=True,
                   help="cache size in rows/entries")
    p.add_argument("--rl-ms", type=float, default=100.0,
                   help="replication latency in ms (default 100, the "
                   "planning value when no production measurement exists)")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--rate", type=float, help="updates per second")
    g.add_argument("--scenario", type=parse_scenario, action="append",
                   help="NAME=updates_per_second; repeat for min/normal/peak")
    p.add_argument("--threshold-pct", type=float, default=None,
                   help="flag scenarios whose collision percentage exceeds this")
    a = p.parse_args(argv)

    if a.instances < 1 or a.rows < 1 or a.rl_ms < 0:
        p.error("instances and rows must be >= 1; rl-ms must be >= 0")

    scenarios = a.scenario if a.scenario else [("single", a.rate)]
    print(f"N={a.instances} instances, S={a.rows} rows, RL={a.rl_ms:g} ms")
    print(f"{'scenario':<12}{'upd/s':>10}{'upd/hour':>14}"
          f"{'coll/hour':>12}{'coll %':>11}  flag")
    worst = 0.0
    for name, rate in scenarios:
        updates = rate * 3600.0
        coll = collisions_per_hour(a.instances, rate, a.rows, a.rl_ms)
        pct = 100.0 * coll / updates if updates else 0.0
        worst = max(worst, pct)
        flag = ""
        if a.threshold_pct is not None and pct > a.threshold_pct:
            flag = "OVER"
        print(f"{name:<12}{rate:>10g}{updates:>14,.0f}"
              f"{coll:>12.1f}{pct:>10.4f}%  {flag}")
    if a.threshold_pct is not None:
        verdict = "exceeds" if worst > a.threshold_pct else "within"
        print(f"worst case {worst:.4f}% {verdict} threshold "
              f"{a.threshold_pct:g}%")
    return 0


if __name__ == "__main__":
    sys.exit(main())
