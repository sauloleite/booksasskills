#!/usr/bin/env python3
"""Estimate the cost of a chain of synchronous remote calls (fallacies 1-3).

Inputs (command-line flags):
  --hops N            number of sequential remote calls in one business request
  --avg-ms X          average round-trip latency per hop, in milliseconds
  --p95-ms Y          optional 95th percentile latency per hop, in milliseconds
  --availability A    optional per-hop availability as a fraction (e.g. 0.999)
  --budget-ms B       optional end-to-end latency budget to check against
  --payload-bytes P   optional bytes returned per interservice call
  --needed-bytes Q    optional bytes the caller actually uses per call
  --rps R             optional calls per second (required for bandwidth output)
  --json              emit JSON instead of text

Outputs:
  Average chain latency (N * X); worst-case tail if every hop is slow (N * Y);
  share of requests that touch at least one tail-latency hop (1 - 0.95^N);
  chain availability (A^N) and expected failed requests per million;
  bandwidth sent versus needed (bytes/s and bits/s) and the waste ratio
  caused by stamp coupling. Assumes independent hops; deterministic, stdlib only.
"""
import argparse
import json
import sys


def human_rate(bytes_per_s):
    units = ["B", "KB", "MB", "GB", "TB"]
    value, i = float(bytes_per_s), 0
    while value >= 1000 and i < len(units) - 1:
        value /= 1000
        i += 1
    bits = bytes_per_s * 8
    bunits = ["bps", "Kbps", "Mbps", "Gbps", "Tbps"]
    bval, j = float(bits), 0
    while bval >= 1000 and j < len(bunits) - 1:
        bval /= 1000
        j += 1
    return f"{value:,.2f} {units[i]}/s ({bval:,.2f} {bunits[j]})"


def compute(a):
    out = {"hops": a.hops, "avg_chain_ms": a.hops * a.avg_ms}
    if a.p95_ms is not None:
        out["all_hops_p95_chain_ms"] = a.hops * a.p95_ms
        out["share_requests_hitting_a_tail_hop"] = 1 - 0.95 ** a.hops
    if a.availability is not None:
        chain = a.availability ** a.hops
        out["chain_availability"] = chain
        out["failed_per_million"] = (1 - chain) * 1_000_000
    if a.budget_ms is not None:
        out["budget_ms"] = a.budget_ms
        out["avg_within_budget"] = out["avg_chain_ms"] <= a.budget_ms
        if a.p95_ms is not None:
            out["tail_within_budget"] = out["all_hops_p95_chain_ms"] <= a.budget_ms
    if a.payload_bytes is not None and a.rps is not None:
        sent = a.payload_bytes * a.rps
        out["bandwidth_sent_bytes_per_s"] = sent
        if a.needed_bytes is not None:
            need = a.needed_bytes * a.rps
            out["bandwidth_needed_bytes_per_s"] = need
            out["waste_ratio"] = sent / need if need else None
    return out


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--hops", type=int, required=True)
    p.add_argument("--avg-ms", type=float, required=True)
    p.add_argument("--p95-ms", type=float)
    p.add_argument("--availability", type=float)
    p.add_argument("--budget-ms", type=float)
    p.add_argument("--payload-bytes", type=float)
    p.add_argument("--needed-bytes", type=float)
    p.add_argument("--rps", type=float)
    p.add_argument("--json", action="store_true")
    a = p.parse_args(argv)
    if a.hops < 1 or a.avg_ms < 0:
        p.error("--hops must be >= 1 and --avg-ms >= 0")
    if a.availability is not None and not 0 < a.availability <= 1:
        p.error("--availability must be in (0, 1]")
    r = compute(a)
    if a.json:
        print(json.dumps(r, indent=2))
        return 0
    print(f"Hops in chain:            {r['hops']}")
    print(f"Average chain latency:    {r['avg_chain_ms']:,.1f} ms")
    if "all_hops_p95_chain_ms" in r:
        print(f"Chain if every hop slow:  {r['all_hops_p95_chain_ms']:,.1f} ms (pessimistic bound)")
        print(f"Requests touching a p95+ hop: {100 * r['share_requests_hitting_a_tail_hop']:.1f}%")
    if "chain_availability" in r:
        print(f"Chain availability:       {100 * r['chain_availability']:.4f}%"
              f" (~{r['failed_per_million']:,.0f} failures per million requests)")
    if "budget_ms" in r:
        print(f"Budget {r['budget_ms']:,.0f} ms: average {'OK' if r['avg_within_budget'] else 'EXCEEDED'}", end="")
        if "tail_within_budget" in r:
            print(f", tail {'OK' if r['tail_within_budget'] else 'EXCEEDED'}")
        else:
            print()
    if "bandwidth_sent_bytes_per_s" in r:
        print(f"Bandwidth sent:           {human_rate(r['bandwidth_sent_bytes_per_s'])}")
        if "bandwidth_needed_bytes_per_s" in r:
            print(f"Bandwidth needed:         {human_rate(r['bandwidth_needed_bytes_per_s'])}")
            if r["waste_ratio"]:
                print(f"Stamp-coupling waste:     {r['waste_ratio']:,.0f}x more data than used")
    return 0


if __name__ == "__main__":
    sys.exit(main())
