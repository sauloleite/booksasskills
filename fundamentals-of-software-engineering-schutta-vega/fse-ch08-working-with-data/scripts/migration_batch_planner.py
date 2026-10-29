#!/usr/bin/env python3
"""Plan batches and timing for a big bang or phased data migration.

Turns proof-of-concept (PoC) measurements into a batch plan, so the
batch size and phase order are chosen from evidence rather than guesswork.

Inputs (command-line flags):
  --segment NAME=COUNT   one per migration phase, in execution order
                         (repeat the flag); a single segment = big bang
  --poc-records/--poc-seconds   records processed and wall time in the PoC
  --batch-size           records per batch (default 5000; 1,000 to 10,000
                         is a common starting range, confirm with the PoC)
  --per-batch-overhead   extra seconds per batch (commit, validation, pauses)
  --safety-factor        multiplier for surprises the PoC did not show
                         (dirty data, contention); default 1.5
  --record-bytes/--memory-mb    optional memory check for one batch in RAM
  --memory-multiplier    in-memory size vs raw bytes (objects, copies); default 3
  --window-hours         optional downtime window length per run

Outputs: a per-segment table (batches, estimated hours, cumulative hours),
totals, warnings (batch size outside the usual range, batch memory over
budget, a segment longer than one window), and the number of windows needed.
--json prints the same data as JSON. Deterministic, stdlib only, no network.
"""
import argparse
import json
import math
import sys


def parse_segment(text):
    if "=" not in text:
        raise argparse.ArgumentTypeError(f"segment must be NAME=COUNT, got {text!r}")
    name, count = text.split("=", 1)
    try:
        n = int(count.replace("_", "").replace(",", ""))
    except ValueError:
        raise argparse.ArgumentTypeError(f"bad record count in {text!r}")
    if n <= 0 or not name.strip():
        raise argparse.ArgumentTypeError(f"segment needs a name and a positive count: {text!r}")
    return name.strip(), n


def plan(args):
    throughput = args.poc_records / args.poc_seconds  # records per second
    warnings = []
    if not 1000 <= args.batch_size <= 10000:
        warnings.append(f"batch size {args.batch_size} is outside the usual 1,000 to 10,000 "
                        "starting range; make sure a PoC supports it")
    batch_mb = None
    if args.record_bytes:
        batch_mb = args.batch_size * args.record_bytes * args.memory_multiplier / 1_048_576
        if args.memory_mb and batch_mb > args.memory_mb:
            max_batch = int(args.memory_mb * 1_048_576 / (args.record_bytes * args.memory_multiplier))
            warnings.append(f"one batch needs about {batch_mb:.1f} MB, over the {args.memory_mb} MB "
                            f"budget; largest batch that fits is about {max_batch}")
    rows, cumulative = [], 0.0
    window_s = args.window_hours * 3600 if args.window_hours else None
    for name, n in args.segment:
        batches = math.ceil(n / args.batch_size)
        secs = (n / throughput + batches * args.per_batch_overhead) * args.safety_factor
        cumulative += secs
        rows.append({"segment": name, "records": n, "batches": batches,
                     "est_hours": round(secs / 3600, 3),
                     "cumulative_hours": round(cumulative / 3600, 3)})
        if window_s and secs > window_s:
            warnings.append(f"segment {name!r} needs {secs/3600:.2f} h, longer than one "
                            f"{args.window_hours} h window; split it further")
    total_records = sum(n for _, n in args.segment)
    result = {
        "strategy": "big bang" if len(args.segment) == 1 else "phased",
        "throughput_records_per_s": round(throughput, 2),
        "batch_size": args.batch_size,
        "batch_memory_mb": round(batch_mb, 2) if batch_mb is not None else None,
        "segments": rows,
        "total_records": total_records,
        "total_batches": sum(r["batches"] for r in rows),
        "total_est_hours": round(cumulative / 3600, 3),
        "windows_needed": math.ceil(cumulative / window_s) if window_s else None,
        "warnings": warnings,
    }
    return result


def print_text(r):
    print(f"Strategy: {r['strategy']}   throughput: {r['throughput_records_per_s']} rec/s   "
          f"batch size: {r['batch_size']}")
    if r["batch_memory_mb"] is not None:
        print(f"Estimated memory per batch: {r['batch_memory_mb']} MB")
    print(f"{'segment':<20}{'records':>12}{'batches':>10}{'est h':>10}{'cum h':>10}")
    for s in r["segments"]:
        print(f"{s['segment']:<20}{s['records']:>12}{s['batches']:>10}"
              f"{s['est_hours']:>10.2f}{s['cumulative_hours']:>10.2f}")
    print(f"Total: {r['total_records']} records, {r['total_batches']} batches, "
          f"{r['total_est_hours']:.2f} h")
    if r["windows_needed"] is not None:
        print(f"Downtime windows needed: {r['windows_needed']}")
    for w in r["warnings"]:
        print(f"WARNING: {w}")


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0],
                                formatter_class=argparse.RawDescriptionHelpFormatter,
                                epilog="Example: %(prog)s --segment tools=12000 --segment "
                                       "sales=480000 --poc-records 20000 --poc-seconds 50 "
                                       "--window-hours 4")
    p.add_argument("--segment", type=parse_segment, action="append", required=True,
                   help="NAME=COUNT, repeat in execution order (least critical first)")
    p.add_argument("--poc-records", type=int, required=True, help="records processed in the PoC")
    p.add_argument("--poc-seconds", type=float, required=True, help="PoC wall-clock seconds")
    p.add_argument("--batch-size", type=int, default=5000)
    p.add_argument("--per-batch-overhead", type=float, default=0.0, help="seconds per batch")
    p.add_argument("--safety-factor", type=float, default=1.5)
    p.add_argument("--record-bytes", type=int, help="average raw bytes per record")
    p.add_argument("--memory-mb", type=float, help="memory budget for one batch")
    p.add_argument("--memory-multiplier", type=float, default=3.0)
    p.add_argument("--window-hours", type=float, help="downtime window length")
    p.add_argument("--json", action="store_true", help="print JSON instead of a table")
    args = p.parse_args(argv)
    for name, val in (("--poc-records", args.poc_records), ("--poc-seconds", args.poc_seconds),
                      ("--batch-size", args.batch_size), ("--safety-factor", args.safety_factor)):
        if val <= 0:
            p.error(f"{name} must be positive")
    result = plan(args)
    if args.json:
        json.dump(result, sys.stdout, indent=2)
        print()
    else:
        print_text(result)


if __name__ == "__main__":
    main()
