#!/usr/bin/env python3
"""Daily completeness fitness function for a data product feed.

Flags each calendar day of a feed as complete or exempt by looking for gaps
between consecutive message arrival timestamps. A gap longer than the
threshold means the day is treated as incomplete (exempt), so a downstream
trend or ML consumer can drop it instead of training on partial data.

Inputs
  timestamps file: one ISO 8601 timestamp per line (e.g. 2026-03-01T00:00:12
    or 2026-03-01T00:00:12+00:00). Blank lines and lines starting with '#'
    are ignored. Order does not matter. Use '-' to read stdin.
  --max-gap-seconds: largest allowed gap between consecutive arrivals.
  --check-day-edges: also count the gap from midnight to the first message
    and from the last message to the next midnight (only sensible for feeds
    that are busy around the clock).
  --start/--end: optional inclusive date range (YYYY-MM-DD); days in range
    with no messages are reported as empty (also exempt).
  --max-exempt-ratio: if given, exit with status 1 when exempt days / days
    evaluated exceeds this ratio.

Outputs
  One line per day: date, message count, largest gap in seconds, status
  (COMPLETE, EXEMPT or EMPTY), then a summary with the exempt ratio.
  Timezone-aware timestamps are converted to UTC; naive ones are used as is.
"""
import argparse
import sys
from datetime import date, datetime, timedelta, timezone


def parse_ts(text):
    ts = datetime.fromisoformat(text.strip().replace("Z", "+00:00"))
    if ts.tzinfo is not None:
        ts = ts.astimezone(timezone.utc).replace(tzinfo=None)
    return ts


def evaluate_day(day, stamps, max_gap, check_edges):
    stamps = sorted(stamps)
    points = list(stamps)
    if check_edges:
        start = datetime.combine(day, datetime.min.time())
        points = [start] + points + [start + timedelta(days=1)]
    largest = 0.0
    for a, b in zip(points, points[1:]):
        largest = max(largest, (b - a).total_seconds())
    status = "EXEMPT" if largest > max_gap else "COMPLETE"
    return largest, status


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("timestamps", help="file with one ISO 8601 timestamp per line, or '-'")
    p.add_argument("--max-gap-seconds", type=float, default=60.0,
                   help="largest allowed gap between arrivals (default 60)")
    p.add_argument("--check-day-edges", action="store_true",
                   help="include midnight-to-first and last-to-midnight gaps")
    p.add_argument("--start", type=date.fromisoformat, help="first day to evaluate")
    p.add_argument("--end", type=date.fromisoformat, help="last day to evaluate")
    p.add_argument("--max-exempt-ratio", type=float,
                   help="fail (exit 1) if exempt ratio exceeds this value")
    args = p.parse_args()

    fh = sys.stdin if args.timestamps == "-" else open(args.timestamps)
    by_day = {}
    with fh:
        for n, line in enumerate(fh, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            try:
                ts = parse_ts(line)
            except ValueError:
                sys.exit(f"line {n}: cannot parse timestamp {line!r}")
            by_day.setdefault(ts.date(), []).append(ts)

    if not by_day and not (args.start and args.end):
        sys.exit("no timestamps found")
    first = args.start or min(by_day)
    last = args.end or max(by_day)
    if first > last:
        sys.exit("--start is after --end")

    print(f"{'date':<12}{'count':>8}{'max_gap_s':>12}  status")
    exempt = total = 0
    d = first
    while d <= last:
        stamps = by_day.get(d, [])
        total += 1
        if not stamps:
            exempt += 1
            print(f"{d.isoformat():<12}{0:>8}{'-':>12}  EMPTY")
        else:
            gap, status = evaluate_day(d, stamps, args.max_gap_seconds, args.check_day_edges)
            exempt += status == "EXEMPT"
            print(f"{d.isoformat():<12}{len(stamps):>8}{gap:>12.1f}  {status}")
        d += timedelta(days=1)

    ratio = exempt / total
    print(f"\ndays evaluated: {total}, exempt or empty: {exempt}, exempt ratio: {ratio:.3f}")
    if args.max_exempt_ratio is not None and ratio > args.max_exempt_ratio:
        print(f"FAIL: exempt ratio {ratio:.3f} exceeds {args.max_exempt_ratio}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
