#!/usr/bin/env python3
"""Two-proportion A/B test analyzer and sample-size planner for agent experiments.

Subcommands
  analyze     Compare a binary metric (task success, resolved ticket, thumbs-up)
              between control A and treatment B.
              Inputs:  --a-success, --a-total, --b-success, --b-total,
                       optional --alpha (default 0.05).
              Outputs: rates, absolute and relative lift, pooled two-sided
                       z-test p-value, unpooled (Wald) confidence interval for
                       B minus A, and a plain-language verdict.
  samplesize  Users (or sessions) needed per arm to detect a minimum effect.
              Inputs:  --baseline (rate of A, 0..1), --mde (absolute lift,
                       e.g. 0.03), optional --alpha, --power (default 0.8),
                       --ratio (B size / A size, default 1).
              Outputs: required n for A and B and the total.

Standard library only, deterministic, no network.
Example:
  python3 ab_test_analyzer.py analyze --a-success 412 --a-total 1000 \
      --b-success 455 --b-total 1000
  python3 ab_test_analyzer.py samplesize --baseline 0.41 --mde 0.03
"""
import argparse
import math
from statistics import NormalDist

Z = NormalDist()


def analyze(a_s, a_n, b_s, b_n, alpha):
    if not (0 <= a_s <= a_n and 0 <= b_s <= b_n and a_n > 0 and b_n > 0):
        raise SystemExit("error: need 0 <= successes <= totals and totals > 0")
    pa, pb = a_s / a_n, b_s / b_n
    diff = pb - pa
    pooled = (a_s + b_s) / (a_n + b_n)
    se_pool = math.sqrt(pooled * (1 - pooled) * (1 / a_n + 1 / b_n))
    z = diff / se_pool if se_pool > 0 else 0.0
    p = 2 * (1 - Z.cdf(abs(z)))
    se = math.sqrt(pa * (1 - pa) / a_n + pb * (1 - pb) / b_n)
    zc = Z.inv_cdf(1 - alpha / 2)
    lo, hi = diff - zc * se, diff + zc * se
    rel = diff / pa if pa > 0 else float("nan")
    return dict(pa=pa, pb=pb, diff=diff, rel=rel, z=z, p=p, lo=lo, hi=hi)


def sample_size(base, mde, alpha, power, ratio):
    p1, p2 = base, base + mde
    if not (0 < p1 < 1 and 0 < p2 < 1) or mde == 0:
        raise SystemExit("error: baseline and baseline+mde must lie in (0,1), mde != 0")
    za, zb = Z.inv_cdf(1 - alpha / 2), Z.inv_cdf(power)
    pbar = (p1 + ratio * p2) / (1 + ratio)
    num = (za * math.sqrt(pbar * (1 - pbar) * (1 + 1 / ratio))
           + zb * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2) / ratio)) ** 2
    n_a = math.ceil(num / mde ** 2)
    n_b = math.ceil(n_a * ratio)
    return n_a, n_b


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("analyze", help="test a finished A/B experiment")
    for k in ("a-success", "a-total", "b-success", "b-total"):
        a.add_argument("--" + k, type=int, required=True)
    a.add_argument("--alpha", type=float, default=0.05)
    s = sub.add_parser("samplesize", help="plan users per arm")
    s.add_argument("--baseline", type=float, required=True)
    s.add_argument("--mde", type=float, required=True)
    s.add_argument("--alpha", type=float, default=0.05)
    s.add_argument("--power", type=float, default=0.8)
    s.add_argument("--ratio", type=float, default=1.0)
    args = ap.parse_args()

    if args.cmd == "analyze":
        r = analyze(args.a_success, args.a_total, args.b_success, args.b_total, args.alpha)
        conf = int(round((1 - args.alpha) * 100))
        print(f"rate A = {r['pa']:.4f}   rate B = {r['pb']:.4f}")
        print(f"lift B-A = {r['diff']:+.4f} absolute ({r['rel']:+.1%} relative)")
        print(f"z = {r['z']:.3f}   two-sided p = {r['p']:.4f}")
        print(f"{conf}% CI for B-A = [{r['lo']:+.4f}, {r['hi']:+.4f}]")
        if r["p"] < args.alpha:
            side = "B beats A" if r["diff"] > 0 else "B is worse than A"
            print(f"verdict: significant at alpha={args.alpha}: {side}")
        else:
            print(f"verdict: not significant at alpha={args.alpha}; "
                  "do not ship on this metric alone (check sample size)")
    else:
        n_a, n_b = sample_size(args.baseline, args.mde, args.alpha, args.power, args.ratio)
        print(f"baseline={args.baseline} target={args.baseline + args.mde:.4f} "
              f"alpha={args.alpha} power={args.power}")
        print(f"n per arm: A = {n_a}, B = {n_b}, total = {n_a + n_b}")


if __name__ == "__main__":
    main()
