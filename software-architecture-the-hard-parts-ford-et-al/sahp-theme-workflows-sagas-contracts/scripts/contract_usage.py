#!/usr/bin/env python3
"""Contract field-usage analyzer: detects stamp coupling and bandwidth waste.

INPUT: a JSON spec file (path argument, or "-" for stdin):

{
  "provider": "CustomerProfile",
  "fields": {"id": 36, "name": 40, "addr1": 120},   # field -> bytes per message
  "consumers": {
    "Wishlist": {
      "uses": ["id", "name"],              # fields the consumer actually reads/writes
      "receives": ["id", "name", "addr1"], # optional; default = all provider fields
      "rps": 2000                          # optional; requests (messages) per second
    }
  }
}

"fields" may also be a plain list of names (sizes unknown, bandwidth skipped).
Sizes are bytes; a field missing a size counts as 0 bytes.

OUTPUT (text or --format json):
  * provider fields no consumer uses (candidates to drop from contracts)
  * fields used by exactly one consumer (candidates for a consumer-specific view)
  * fields used by every consumer (core shared contract)
  * fields a consumer uses but the provider does not supply (contract gaps)
  * per consumer: received vs used counts, over-coupled fields (received but
    unused, i.e. breaking-change exposure), unused ratio, payload bytes received
    vs needed, and bandwidth waste in bytes/s when rps and sizes are given
  * totals of bandwidth sent, needed and wasted

EXIT CODE: 0 normally; 1 if --max-unused-ratio is set and any consumer's
unused ratio exceeds it (usable as a CI fitness function); 2 on input errors.
Deterministic, standard library only, no network.
"""
import argparse
import json
import sys


def load_spec(path):
    text = sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()
    spec = json.loads(text)
    fields = spec.get("fields")
    if isinstance(fields, list):
        sizes, have_sizes = {f: 0 for f in fields}, False
    elif isinstance(fields, dict):
        sizes, have_sizes = {k: int(v or 0) for k, v in fields.items()}, True
    else:
        raise ValueError("'fields' must be a list or an object of field -> bytes")
    consumers = spec.get("consumers")
    if not isinstance(consumers, dict) or not consumers:
        raise ValueError("'consumers' must be a non-empty object")
    return spec.get("provider", "provider"), sizes, have_sizes, consumers


def human(n):
    for unit in ("B", "KB", "MB", "GB"):
        if abs(n) < 1000 or unit == "GB":
            return f"{n:,.0f} {unit}" if unit == "B" else f"{n:,.1f} {unit}"
        n /= 1000.0


def analyze(provider, sizes, have_sizes, consumers):
    all_fields = list(sizes)
    usage = {f: [] for f in all_fields}
    report = {"provider": provider, "consumers": {}, "gaps": {}}
    tot_sent = tot_needed = 0.0
    for name in sorted(consumers):
        c = consumers[name] or {}
        uses = list(dict.fromkeys(c.get("uses", [])))
        receives = list(dict.fromkeys(c.get("receives", all_fields)))
        gaps = sorted(f for f in uses if f not in sizes)
        if gaps:
            report["gaps"][name] = gaps
        not_received = sorted(f for f in uses if f in sizes and f not in receives)
        for f in uses:
            if f in usage:
                usage[f].append(name)
        recv_known = [f for f in receives if f in sizes]
        unused = sorted(f for f in recv_known if f not in uses)
        sent_b = sum(sizes[f] for f in recv_known)
        need_b = sum(sizes[f] for f in recv_known if f in uses)
        ratio = len(unused) / len(recv_known) if recv_known else 0.0
        entry = {
            "received": len(recv_known), "used": len(set(uses) & set(recv_known)),
            "unused_fields": unused, "unused_ratio": round(ratio, 3),
            "used_but_not_received": not_received,
        }
        if have_sizes:
            entry.update(bytes_per_msg=sent_b, needed_bytes_per_msg=need_b)
            rps = c.get("rps")
            if rps is not None:
                entry.update(rps=rps, bandwidth_Bps=sent_b * rps,
                             needed_Bps=need_b * rps, waste_Bps=(sent_b - need_b) * rps)
                tot_sent += sent_b * rps
                tot_needed += need_b * rps
        report["consumers"][name] = entry
    n = len(consumers)
    report["unused_by_all"] = [f for f in all_fields if not usage[f]]
    report["single_consumer"] = {f: usage[f][0] for f in all_fields if len(usage[f]) == 1}
    report["used_by_all"] = [f for f in all_fields if len(usage[f]) == n]
    if have_sizes:
        report["totals"] = {"bandwidth_Bps": tot_sent, "needed_Bps": tot_needed,
                            "waste_Bps": tot_sent - tot_needed}
    return report


def print_text(r):
    print(f"Provider: {r['provider']}")
    print(f"Fields used by no consumer (stamp coupling): {', '.join(r['unused_by_all']) or '-'}")
    single = ", ".join(f"{f} ({c})" for f, c in r["single_consumer"].items())
    print(f"Fields used by exactly one consumer: {single or '-'}")
    print(f"Fields used by every consumer: {', '.join(r['used_by_all']) or '-'}")
    for c, g in r["gaps"].items():
        print(f"CONTRACT GAP: {c} uses fields the provider lacks: {', '.join(g)}")
    for name, e in r["consumers"].items():
        print(f"\nConsumer {name}: receives {e['received']}, uses {e['used']}, "
              f"unused ratio {e['unused_ratio']:.0%}")
        print(f"  over-coupled (received, unused): {', '.join(e['unused_fields']) or '-'}")
        if e["used_but_not_received"]:
            print(f"  WARNING used but not received: {', '.join(e['used_but_not_received'])}")
        if "bytes_per_msg" in e:
            print(f"  payload {human(e['bytes_per_msg'])}/msg, needed {human(e['needed_bytes_per_msg'])}/msg")
        if "waste_Bps" in e:
            print(f"  at {e['rps']:,} rps: sent {human(e['bandwidth_Bps'])}/s, "
                  f"needed {human(e['needed_Bps'])}/s, waste {human(e['waste_Bps'])}/s")
    if "totals" in r and r["totals"]["bandwidth_Bps"]:
        t = r["totals"]
        print(f"\nTotal: sent {human(t['bandwidth_Bps'])}/s, needed {human(t['needed_Bps'])}/s, "
              f"waste {human(t['waste_Bps'])}/s")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec", help="JSON spec file, or - for stdin")
    ap.add_argument("--format", choices=["text", "json"], default="text")
    ap.add_argument("--max-unused-ratio", type=float, default=None,
                    help="exit 1 if any consumer's unused-field ratio exceeds this (0..1)")
    a = ap.parse_args()
    try:
        r = analyze(*load_spec(a.spec))
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if a.format == "json":
        print(json.dumps(r, indent=2, sort_keys=True))
    else:
        print_text(r)
    if a.max_unused_ratio is not None:
        bad = [n for n, e in r["consumers"].items() if e["unused_ratio"] > a.max_unused_ratio]
        if bad:
            print(f"FITNESS FAIL: unused ratio above {a.max_unused_ratio} for {', '.join(bad)}",
                  file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
