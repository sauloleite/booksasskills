#!/usr/bin/env python3
"""Compare candidate models by cost per successful task, and estimate VRAM fit.

Subcommand `cost`
  Input: a JSON file with a list of candidate models, each
    {"name": str, "in_price": float, "out_price": float, "score": float}
  where prices are per million tokens (any currency or relative unit) and
  score is the task success rate (0..1) measured on YOUR eval set.
  Workload flags: --in-tokens, --out-tokens (average per request),
  --requests (per month). Optional --route "small=0.8,large=0.2" blends
  models by traffic share (shares must sum to 1) to model hybrid routing.
  Optional --failure-cost F: cost of handling one failed task (human
  rework, refund, escalation). Adds "total/req" = cost/req + (1-score)*F
  and ranks by it instead, since a cheap but weak model can cost more.
  Output: table ranked by cost per successful task (or total/req when
  --failure-cost is given), plus the routed blend.
  Note: the blended score assumes each model's score holds on the slice
  of traffic routed to it; measure per-slice scores when you can.

Subcommand `vram`
  Input: --params (billions), --bytes-per-param (2 for 16-bit, 1 for
  8-bit, 0.5 for 4-bit), --overhead multiplier (default 1.2 for
  activations and KV cache at modest context).
  Output: estimated GB and whether it fits common GPU sizes.

Deterministic, standard library only, no network.
"""
import argparse
import json
import sys

GPU_SIZES = [("24 GB consumer (RTX 3090/4090)", 24), ("40 GB A100", 40),
             ("80 GB A100/H100", 80)]


def per_request(m, tin, tout):
    return (tin * m["in_price"] + tout * m["out_price"]) / 1e6


def parse_route(text):
    shares = {}
    for part in text.split(","):
        name, _, val = part.partition("=")
        shares[name.strip()] = float(val)
    if abs(sum(shares.values()) - 1.0) > 1e-6:
        sys.exit("error: --route shares must sum to 1")
    return shares


def cmd_cost(a):
    with open(a.models) as fh:
        models = json.load(fh)
    rows = []
    for m in models:
        if not 0 < m["score"] <= 1:
            sys.exit(f"error: score for {m['name']} must be in (0, 1]")
        c = per_request(m, a.in_tokens, a.out_tokens)
        total = c + (1 - m["score"]) * a.failure_cost
        rows.append((m["name"], m["score"], c, c * a.requests, c / m["score"], total))
    key = 5 if a.failure_cost else 4
    rows.sort(key=lambda r: r[key])
    print(f"{'model':<22}{'score':>7}{'cost/req':>12}{'monthly':>14}"
          f"{'cost/success':>14}{'total/req':>12}")
    for name, s, c, mon, cps, tot in rows:
        print(f"{name:<22}{s:>7.3f}{c:>12.6f}{mon:>14.2f}{cps:>14.6f}{tot:>12.4f}")
    label = "total cost incl. failures" if a.failure_cost else "price per success"
    print(f"\nbest {label}: {rows[0][0]}")
    if a.route:
        by_name = {r[0]: r for r in rows}
        shares = parse_route(a.route)
        missing = [n for n in shares if n not in by_name]
        if missing:
            sys.exit(f"error: unknown model(s) in --route: {missing}")
        bc = sum(sh * by_name[n][2] for n, sh in shares.items())
        bs = sum(sh * by_name[n][1] for n, sh in shares.items())
        bt = bc + (1 - bs) * a.failure_cost
        print(f"routed blend {a.route}: score={bs:.3f} cost/req={bc:.6f} "
              f"monthly={bc * a.requests:.2f} cost/success={bc / bs:.6f} "
              f"total/req={bt:.4f}")


def cmd_vram(a):
    gb = a.params * a.bytes_per_param * a.overhead
    print(f"estimated VRAM: {gb:.1f} GB "
          f"({a.params}B params x {a.bytes_per_param} B x {a.overhead} overhead)")
    for label, size in GPU_SIZES:
        n = -(-gb // size)  # ceiling division
        print(f"  {label:<32} {'fits on 1' if n <= 1 else f'needs ~{int(n)} GPUs'}")


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("cost", help="rank models by cost per successful task")
    c.add_argument("models", help="JSON file with candidate models")
    c.add_argument("--in-tokens", type=float, required=True, help="avg input tokens/request")
    c.add_argument("--out-tokens", type=float, required=True, help="avg output tokens/request")
    c.add_argument("--requests", type=float, default=100000, help="requests per month")
    c.add_argument("--route", help='traffic shares, e.g. "small=0.8,large=0.2"')
    c.add_argument("--failure-cost", type=float, default=0.0,
                   help="cost of handling one failed task, same unit as prices")
    c.set_defaults(func=cmd_cost)
    v = sub.add_parser("vram", help="estimate VRAM for an open-weight model")
    v.add_argument("--params", type=float, required=True, help="parameters in billions")
    v.add_argument("--bytes-per-param", type=float, default=2.0)
    v.add_argument("--overhead", type=float, default=1.2)
    v.set_defaults(func=cmd_vram)
    a = p.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
