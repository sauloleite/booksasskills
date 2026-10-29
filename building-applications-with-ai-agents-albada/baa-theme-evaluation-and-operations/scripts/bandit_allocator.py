#!/usr/bin/env python3
"""Beta-Bernoulli Thompson-sampling allocator for adaptive agent experiments.

Each arm is a variant (prompt, reasoning chain, orchestration strategy) with a
binary reward (task resolved, user approved). The script updates a Beta prior
with observed rewards, estimates by Monte Carlo the probability that each arm
is best, and proposes the next traffic split with a minimum exploration share
per arm so weak arms keep being probed.

Inputs:
  --arm NAME:SUCCESSES:TRIALS   repeat once per arm (at least two arms)
  --prior-a, --prior-b          Beta prior (default 1 1 = neutral/uniform)
  --min-share                   exploration floor per arm (default 0.05)
  --draws                       Monte Carlo draws (default 20000)
  --seed                        RNG seed (default 7) for deterministic output
Outputs: table with posterior mean, 95% credible interval, P(best) and the
proposed allocation; a stop hint when one arm has P(best) >= --stop (0.95).

Standard library only, deterministic for a given seed, no network.
Example:
  python3 bandit_allocator.py --arm chainA:120:400 --arm chainB:150:400 \
      --arm chainC:118:400
"""
import argparse
import random


def parse_arm(text):
    try:
        name, s, n = text.split(":")
        s, n = int(s), int(n)
    except ValueError:
        raise argparse.ArgumentTypeError("arm must be NAME:SUCCESSES:TRIALS")
    if not 0 <= s <= n:
        raise argparse.ArgumentTypeError("need 0 <= SUCCESSES <= TRIALS")
    return name, s, n


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--arm", type=parse_arm, action="append", required=True)
    ap.add_argument("--prior-a", type=float, default=1.0)
    ap.add_argument("--prior-b", type=float, default=1.0)
    ap.add_argument("--min-share", type=float, default=0.05)
    ap.add_argument("--draws", type=int, default=20000)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--stop", type=float, default=0.95)
    args = ap.parse_args()
    arms = args.arm
    k = len(arms)
    if k < 2:
        ap.error("give at least two --arm values")
    if args.min_share * k > 1:
        ap.error("--min-share times number of arms must be <= 1")

    rng = random.Random(args.seed)
    post = [(args.prior_a + s, args.prior_b + n - s) for _, s, n in arms]
    samples = [[] for _ in range(k)]
    wins = [0] * k
    for _ in range(args.draws):
        draw = [rng.betavariate(a, b) for a, b in post]
        for i, v in enumerate(draw):
            samples[i].append(v)
        wins[max(range(k), key=lambda i: draw[i])] += 1
    p_best = [w / args.draws for w in wins]
    free = 1 - args.min_share * k
    alloc = [args.min_share + free * p for p in p_best]

    print(f"{'arm':<14}{'succ/trials':>13}{'mean':>8}{'95% CrI':>18}{'P(best)':>9}{'next share':>12}")
    for i, (name, s, n) in enumerate(arms):
        a, b = post[i]
        xs = sorted(samples[i])
        lo, hi = xs[int(0.025 * len(xs))], xs[int(0.975 * len(xs)) - 1]
        print(f"{name:<14}{f'{s}/{n}':>13}{a / (a + b):>8.3f}"
              f"{f'[{lo:.3f}, {hi:.3f}]':>18}{p_best[i]:>9.3f}{alloc[i]:>12.1%}")
    best = max(range(k), key=lambda i: p_best[i])
    if p_best[best] >= args.stop:
        print(f"hint: {arms[best][0]} has P(best) >= {args.stop}; consider promoting it "
              "after checking guardrail metrics and long-term effects")
    else:
        print("hint: no clear winner yet; keep collecting rewards with the shares above")


if __name__ == "__main__":
    main()
