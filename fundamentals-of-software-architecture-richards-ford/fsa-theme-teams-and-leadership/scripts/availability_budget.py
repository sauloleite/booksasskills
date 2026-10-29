#!/usr/bin/env python3
"""Translate availability targets ("nines") into concrete downtime budgets, and back.

Supports the negotiation tactic of replacing abstract "nines" with hours, minutes
and seconds of unplanned downtime so stakeholders can judge what they are asking for.

Inputs (subcommands):
  downtime  TARGET [TARGET ...]   Each TARGET is a percentage (99.95, 99.9%) or a
                                  nines shorthand (3n, 5n). Prints allowed downtime
                                  per year, month (year/12), week and day.
  percent   --per {year,month,week,day} --seconds S | --minutes M | --hours H
                                  Converts a tolerated downtime budget into the
                                  availability percentage it implies.

Options:
  --year-days D   Days per year used for budgets (default 365.25).
  --json          Machine-readable output.

Outputs: a plain-text table (or JSON) on stdout. Deterministic; stdlib only.
Note: some published tables differ by a few seconds or minutes depending on the
year length and rounding used; this script states its assumption explicitly.
"""
import argparse
import json
import sys

PERIOD_DAYS = {"day": 1.0, "week": 7.0}


def parse_target(text):
    t = text.strip().lower().rstrip("%")
    if t.endswith("n") and t[:-1].isdigit():
        n = int(t[:-1])
        if n < 1:
            raise ValueError("nines count must be >= 1")
        return 100.0 * (1 - 10 ** (-n))
    value = float(t)
    if not 0 < value < 100:
        raise ValueError("percentage must be between 0 and 100 (exclusive)")
    return value


def period_seconds(period, year_days):
    if period == "year":
        return year_days * 86400
    if period == "month":
        return year_days * 86400 / 12
    return PERIOD_DAYS[period] * 86400


def fmt(seconds):
    if seconds < 1:
        return f"{seconds * 1000:.0f} ms"
    s = round(seconds)
    d, rem = divmod(s, 86400)
    h, rem = divmod(rem, 3600)
    m, sec = divmod(rem, 60)
    parts = [f"{d}d"] if d else []
    if h or d:
        parts.append(f"{h}h")
    if m or h or d:
        parts.append(f"{m}m")
    parts.append(f"{sec}s")
    return " ".join(parts)


def cmd_downtime(args):
    rows = []
    for raw in args.targets:
        pct = parse_target(raw)
        frac = 1 - pct / 100.0
        row = {"target": raw, "percent": round(pct, 6)}
        for p in ("year", "month", "week", "day"):
            row[f"{p}_seconds"] = round(frac * period_seconds(p, args.year_days), 3)
        rows.append(row)
    if args.json:
        print(json.dumps({"year_days": args.year_days, "rows": rows}, indent=2))
        return
    print(f"Allowed unplanned downtime (year = {args.year_days} days, month = year/12)")
    print(f"{'target':>10} {'percent':>10} {'per year':>14} {'per month':>12} {'per week':>12} {'per day':>10}")
    for r in rows:
        print(f"{r['target']:>10} {r['percent']:>10} {fmt(r['year_seconds']):>14} "
              f"{fmt(r['month_seconds']):>12} {fmt(r['week_seconds']):>12} {fmt(r['day_seconds']):>10}")


def cmd_percent(args):
    budget = args.seconds or 0.0
    budget += (args.minutes or 0.0) * 60 + (args.hours or 0.0) * 3600
    total = period_seconds(args.per, args.year_days)
    if budget <= 0 or budget >= total:
        sys.exit("error: downtime budget must be > 0 and smaller than the period")
    pct = 100.0 * (1 - budget / total)
    out = {"per": args.per, "budget_seconds": budget, "percent": round(pct, 6)}
    if args.json:
        print(json.dumps(out, indent=2))
    else:
        print(f"{fmt(budget)} of downtime per {args.per} -> {pct:.6f}% availability")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--year-days", type=float, default=365.25)
    ap.add_argument("--json", action="store_true")
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("downtime", help="targets -> downtime budgets")
    d.add_argument("targets", nargs="+", help="e.g. 99.9 99.95%% 5n")
    p = sub.add_parser("percent", help="downtime budget -> availability percent")
    p.add_argument("--per", choices=["year", "month", "week", "day"], required=True)
    p.add_argument("--seconds", type=float)
    p.add_argument("--minutes", type=float)
    p.add_argument("--hours", type=float)
    args = ap.parse_args()
    try:
        cmd_downtime(args) if args.cmd == "downtime" else cmd_percent(args)
    except ValueError as exc:
        sys.exit(f"error: {exc}")


if __name__ == "__main__":
    main()
