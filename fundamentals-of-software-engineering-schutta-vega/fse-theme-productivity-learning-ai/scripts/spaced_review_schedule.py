#!/usr/bin/env python3
"""Spaced-repetition review scheduler for things you are learning.

Computes review dates at expanding intervals after the day a topic was
first studied, so you revisit it before it is forgotten.

Inputs (one of):
  --topic NAME --learned YYYY-MM-DD   a single topic
  --csv FILE                          CSV with header columns topic,learned_on

Options:
  --intervals 1,3,7,14,30,60          gaps in days after the learn date
  --on YYYY-MM-DD                     instead of full schedules, list reviews
                                      due on that date
  --window N                          with --on, include reviews due up to N
                                      days after that date (default 0)

Output: plain-text table on stdout. Columns for full schedules:
  topic, review number, date, days since learned.
With --on: date, topic, review number (sorted by date then topic).

Deterministic, standard library only, no network.
"""
import argparse
import csv
import sys
from datetime import date, timedelta

DEFAULT_INTERVALS = "1,3,7,14,30,60"


def parse_date(text):
    try:
        return date.fromisoformat(text.strip())
    except ValueError:
        raise argparse.ArgumentTypeError(f"invalid date '{text}', use YYYY-MM-DD")


def parse_intervals(text):
    try:
        values = [int(v) for v in text.split(",") if v.strip()]
    except ValueError:
        raise argparse.ArgumentTypeError("intervals must be comma-separated integers")
    if not values or any(v <= 0 for v in values):
        raise argparse.ArgumentTypeError("intervals must be positive")
    if values != sorted(values) or len(set(values)) != len(values):
        raise argparse.ArgumentTypeError("intervals must be strictly increasing")
    return values


def load_topics(args):
    if args.csv:
        topics = []
        with open(args.csv, newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            if not reader.fieldnames or not {"topic", "learned_on"} <= set(reader.fieldnames):
                sys.exit("CSV must have header columns: topic,learned_on")
            for row in reader:
                if not row["topic"].strip():
                    continue
                topics.append((row["topic"].strip(), parse_date(row["learned_on"])))
        return topics
    if args.topic and args.learned:
        return [(args.topic, args.learned)]
    sys.exit("give either --csv FILE or both --topic and --learned")


def schedule(learned, intervals):
    return [(i + 1, learned + timedelta(days=gap), gap) for i, gap in enumerate(intervals)]


def main():
    p = argparse.ArgumentParser(description="Compute expanding-interval review dates for study topics.")
    p.add_argument("--topic", help="topic name (with --learned)")
    p.add_argument("--learned", type=parse_date, help="date first studied, YYYY-MM-DD")
    p.add_argument("--csv", help="CSV file with columns topic,learned_on")
    p.add_argument("--intervals", type=parse_intervals, default=parse_intervals(DEFAULT_INTERVALS),
                   help=f"comma-separated day gaps (default {DEFAULT_INTERVALS})")
    p.add_argument("--on", type=parse_date, help="list reviews due on this date")
    p.add_argument("--window", type=int, default=0, help="with --on, extra days to include (default 0)")
    args = p.parse_args()
    if args.window < 0:
        p.error("--window must be >= 0")

    topics = load_topics(args)

    if args.on:
        end = args.on + timedelta(days=args.window)
        due = [(d, t, n) for t, learned in topics for n, d, _ in schedule(learned, args.intervals)
               if args.on <= d <= end]
        due.sort()
        if not due:
            print(f"No reviews due between {args.on} and {end}.")
            return
        print(f"{'date':<12}{'review':<8}topic")
        for d, t, n in due:
            print(f"{d.isoformat():<12}{n:<8}{t}")
        return

    width = max([len("topic")] + [len(t) for t, _ in topics]) + 2
    print(f"{'topic':<{width}}{'review':<8}{'date':<12}days_after")
    for t, learned in topics:
        for n, d, gap in schedule(learned, args.intervals):
            print(f"{t:<{width}}{n:<8}{d.isoformat():<12}{gap}")


if __name__ == "__main__":
    main()
