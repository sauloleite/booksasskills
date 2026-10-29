#!/usr/bin/env python3
"""Show how temperature, top-k, top-p and min-p reshape a next-token distribution.

Inputs:
  --logits      comma-separated raw logits, e.g. "1,2" or "5,3.5,3,2,-1"
  --tokens      optional comma-separated labels (default t0, t1, ...)
  --temperature T (default 1.0; 0 means greedy argmax)
  --top-k K     keep the K highest logits (0 = off)
  --top-p P     keep the smallest prefix of sorted tokens whose cumulative probability reaches P (1 = off)
  --min-p M     drop tokens with probability below M x max probability (0 = off);
                add --min-p-absolute to use M as a fixed probability floor instead
  --samples S   draw S tokens with --seed to show empirical frequencies (0 = off)

Output: a table with the softmax distribution at temperature 1, after temperature, and the
final renormalized distribution after the filters, plus optional sample counts.
Filters run in this order: temperature, top-k, top-p, min-p. Standard library only, deterministic.
"""
import argparse
import math
import random


def softmax(xs):
    m = max(xs)
    exps = [math.exp(x - m) for x in xs]
    s = sum(exps)
    return [e / s for e in exps]


def main():
    p = argparse.ArgumentParser(description="Apply temperature, top-k, top-p and min-p to logits and print the result.")
    p.add_argument("--logits", required=True, help="comma-separated logits")
    p.add_argument("--tokens", help="comma-separated token labels")
    p.add_argument("--temperature", type=float, default=1.0)
    p.add_argument("--top-k", type=int, default=0)
    p.add_argument("--top-p", type=float, default=1.0)
    p.add_argument("--min-p", type=float, default=0.0)
    p.add_argument("--min-p-absolute", action="store_true", help="treat --min-p as an absolute floor")
    p.add_argument("--samples", type=int, default=0)
    p.add_argument("--seed", type=int, default=0)
    a = p.parse_args()

    logits = [float(x) for x in a.logits.split(",")]
    names = a.tokens.split(",") if a.tokens else [f"t{i}" for i in range(len(logits))]
    if len(names) != len(logits):
        p.error("--tokens and --logits must have the same length")
    if a.temperature < 0 or not 0 < a.top_p <= 1 or a.top_k < 0 or a.min_p < 0:
        p.error("invalid sampling parameter")

    base = softmax(logits)
    if a.temperature == 0:
        best = max(range(len(logits)), key=lambda i: logits[i])
        temp = [1.0 if i == best else 0.0 for i in range(len(logits))]
    else:
        temp = softmax([x / a.temperature for x in logits])

    order = sorted(range(len(logits)), key=lambda i: (-temp[i], -logits[i]))
    keep = {order[0]} if a.temperature == 0 else set(order)
    if a.top_k:
        keep &= set(order[:a.top_k])
    if a.top_p < 1:
        cum, nucleus = 0.0, set()
        for i in order:
            if i not in keep:
                continue
            nucleus.add(i)
            cum += temp[i]
            if cum >= a.top_p - 1e-12:
                break
        keep &= nucleus
    if a.min_p:
        floor = a.min_p if a.min_p_absolute else a.min_p * max(temp[i] for i in keep)
        keep = {i for i in keep if temp[i] >= floor} or {order[0]}

    total = sum(temp[i] for i in keep)
    final = [temp[i] / total if i in keep else 0.0 for i in range(len(logits))]

    print(f"temperature={a.temperature:g} top_k={a.top_k or 'off'} top_p={a.top_p:g} "
          f"min_p={a.min_p:g}{' (absolute)' if a.min_p_absolute else ' (relative)' if a.min_p else ''}")
    print(f"{'token':<12}{'logit':>8}{'p(T=1)':>10}{'p(T)':>10}{'final':>10}")
    for i in order:
        print(f"{names[i]:<12}{logits[i]:>8.2f}{base[i]:>10.4f}{temp[i]:>10.4f}{final[i]:>10.4f}")
    print(f"candidates kept: {len(keep)} of {len(logits)}")

    if a.samples:
        rng = random.Random(a.seed)
        draws = rng.choices(range(len(logits)), weights=final, k=a.samples)
        counts = {names[i]: draws.count(i) for i in order if final[i] > 0}
        print(f"{a.samples} samples (seed {a.seed}): " + ", ".join(f"{k}={v}" for k, v in counts.items()))


if __name__ == "__main__":
    main()
