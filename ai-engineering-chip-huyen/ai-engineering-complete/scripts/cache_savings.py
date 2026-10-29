#!/usr/bin/env python3
"""Estimate whether a system cache (exact or semantic) pays off.

Model: every query pays the cache lookup. A hit returns the cached answer;
a miss runs the full pipeline. For semantic caches, a fraction of hits are
wrong matches, each charged an optional penalty cost.

Inputs (flags): per-query generation latency and cost, lookup latency and
cost, hit rate, wrong-hit share of hits, wrong-hit penalty, daily volume.

Output: a plain-text report with mean latency and cost per query with and
without the cache, daily cost, expected wrong answers per day, and the
break-even hit rates for latency and for cost. Deterministic, stdlib only.

Example:
  python3 cache_savings.py --gen-latency 1.2 --gen-cost 0.004 \
      --lookup-latency 0.04 --lookup-cost 0.0001 --hit-rate 0.30 \
      --wrong-hit-share 0.02 --wrong-hit-penalty 0.05 --queries-per-day 100000
"""
import argparse


def breakeven(lookup, gen, wrong_share=0.0, penalty=0.0):
    """Hit rate h at which lookup + (1-h)*gen + h*wrong*penalty == gen."""
    denom = gen - wrong_share * penalty
    if denom <= 0:
        return None  # wrong hits cost more than they save: never breaks even
    return lookup / denom


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--gen-latency", type=float, required=True, help="seconds per uncached query")
    p.add_argument("--gen-cost", type=float, required=True, help="dollars per uncached query")
    p.add_argument("--lookup-latency", type=float, default=0.0, help="seconds per cache lookup (paid on every query)")
    p.add_argument("--lookup-cost", type=float, default=0.0, help="dollars per cache lookup (paid on every query)")
    p.add_argument("--hit-rate", type=float, required=True, help="fraction of queries served from cache, 0..1")
    p.add_argument("--wrong-hit-share", type=float, default=0.0,
                   help="fraction of hits that return a wrong answer (semantic cache), 0..1")
    p.add_argument("--wrong-hit-penalty", type=float, default=0.0,
                   help="dollar cost assigned to each wrong answer (support ticket, churn risk)")
    p.add_argument("--queries-per-day", type=float, default=0.0, help="daily volume for totals")
    a = p.parse_args()

    for name in ("hit_rate", "wrong_hit_share"):
        v = getattr(a, name)
        if not 0.0 <= v <= 1.0:
            p.error(f"--{name.replace('_', '-')} must be between 0 and 1")

    h, w = a.hit_rate, a.wrong_hit_share
    lat_cached = a.lookup_latency + (1 - h) * a.gen_latency
    cost_cached = a.lookup_cost + (1 - h) * a.gen_cost
    penalty = h * w * a.wrong_hit_penalty
    total_cached = cost_cached + penalty

    print("Per query            no cache      with cache")
    print(f"  mean latency (s)   {a.gen_latency:10.4f}    {lat_cached:10.4f}")
    print(f"  compute cost ($)   {a.gen_cost:10.6f}    {cost_cached:10.6f}")
    print(f"  wrong-hit penalty  {0:10.6f}    {penalty:10.6f}")
    print(f"  total cost ($)     {a.gen_cost:10.6f}    {total_cached:10.6f}")
    print(f"Latency change: {100 * (lat_cached / a.gen_latency - 1):+.1f}%   "
          f"Total cost change: {100 * (total_cached / a.gen_cost - 1):+.1f}%")
    if a.queries_per_day:
        q = a.queries_per_day
        print(f"Per day: cost ${q * a.gen_cost:,.2f} -> ${q * total_cached:,.2f}; "
              f"expected wrong answers served: {q * h * w:,.0f}")
    be_lat = breakeven(a.lookup_latency, a.gen_latency)
    be_cost = breakeven(a.lookup_cost, a.gen_cost, w, a.wrong_hit_penalty)
    print(f"Break-even hit rate for latency: {be_lat:.2%}" if be_lat is not None else
          "Break-even hit rate for latency: n/a")
    print(f"Break-even hit rate for total cost: {be_cost:.2%}" if be_cost is not None else
          "Break-even hit rate for total cost: never (wrong hits cost more than generation)")
    verdict = lat_cached < a.gen_latency and total_cached < a.gen_cost
    print("Verdict:", "cache pays off on both latency and cost" if verdict else
          "cache does not pay off on both axes; check hit rate, lookup cost, wrong-hit risk")


if __name__ == "__main__":
    main()
