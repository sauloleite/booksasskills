#!/usr/bin/env python3
"""Size an evaluation set and check how stable its score is.

Two subcommands:

  size       Estimate how many evaluation examples are needed to be ~95%
             confident that one system beats another by a given score gap.
             Inputs: --gap (absolute difference, e.g. 0.05 for 5 points) and
             optionally --baseline (expected score of the weaker system, 0..1),
             --confidence and --power.
             Outputs: (a) the rule-of-thumb estimate (30% gap ~ 10 examples,
             and every 3x smaller gap needs ~10x more data, i.e. n ~ 10*(0.3/gap)^2),
             and (b) a normal-approximation two-proportion estimate per system
             for binary (pass/fail) scores.

  bootstrap  Resample a file of per-example scores with replacement and report
             the mean, the bootstrap standard error and a percentile confidence
             interval. With --compare, the second file must hold scores for the
             SAME examples in the SAME order; the script then bootstraps the
             paired difference (B - A) and reports how often B beats A.
             Input files: one numeric score per line (blank lines and lines
             starting with # are ignored). Scores can be 0/1 or continuous.

Deterministic: a fixed --seed (default 0) gives identical output every run.
Standard library only; no network access.

Examples:
  python3 eval_sample_size.py size --gap 0.03
  python3 eval_sample_size.py size --gap 0.05 --baseline 0.80
  python3 eval_sample_size.py bootstrap scores_a.txt
  python3 eval_sample_size.py bootstrap scores_a.txt --compare scores_b.txt
"""
import argparse
import math
import random
import statistics
import sys


def z_quantile(p):
    """Inverse standard normal CDF via bisection (no scipy needed)."""
    lo, hi = -10.0, 10.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if 0.5 * (1 + math.erf(mid / math.sqrt(2))) < p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def rule_of_thumb(gap):
    # Anchored at 30% gap -> ~10 examples; n scales with 1/gap^2,
    # so a 3x smaller gap needs ~10x more examples (sqrt(10) ~ 3.16).
    return 10 * (0.30 / gap) ** 2


def two_proportion_n(p1, p2, confidence, power):
    z_a = z_quantile(1 - (1 - confidence) / 2)
    z_b = z_quantile(power)
    var = p1 * (1 - p1) + p2 * (1 - p2)
    return (z_a + z_b) ** 2 * var / (p2 - p1) ** 2


def cmd_size(args):
    gap = args.gap
    if not 0 < gap < 1:
        sys.exit("--gap must be between 0 and 1 (e.g. 0.05 for 5 points)")
    print(f"Score gap to detect: {gap:.4f} ({gap * 100:.1f} points)")
    print(f"Rule of thumb (95% confidence): ~{math.ceil(rule_of_thumb(gap)):,} examples")
    p1 = args.baseline
    p2 = p1 + gap
    if p2 >= 1:
        print("Two-proportion estimate skipped: baseline + gap must be < 1")
        return
    n = two_proportion_n(p1, p2, args.confidence, args.power)
    print(
        f"Two-proportion test (binary scores, baseline {p1:.2f} vs {p2:.2f}, "
        f"confidence {args.confidence:.2f}, power {args.power:.2f}): "
        f"~{math.ceil(n):,} examples per system"
    )
    print("The rule of thumb is a rough guide; the two-proportion figure is the stricter plan.")
    print("If both systems are scored on the same examples (paired),")
    print("the real requirement is usually lower; use 'bootstrap --compare' to check.")


def read_scores(path):
    vals = []
    with open(path, encoding="utf-8") as fh:
        for ln, line in enumerate(fh, 1):
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            try:
                vals.append(float(s))
            except ValueError:
                sys.exit(f"{path}:{ln}: not a number: {s!r}")
    if not vals:
        sys.exit(f"{path}: no scores found")
    return vals


def percentile(sorted_vals, q):
    # Linear interpolation between closest ranks.
    k = (len(sorted_vals) - 1) * q
    f, c = math.floor(k), math.ceil(k)
    if f == c:
        return sorted_vals[f]
    return sorted_vals[f] + (sorted_vals[c] - sorted_vals[f]) * (k - f)


def cmd_bootstrap(args):
    rng = random.Random(args.seed)
    a = read_scores(args.scores)
    alpha = (1 - args.confidence) / 2
    if args.compare:
        b = read_scores(args.compare)
        if len(a) != len(b):
            sys.exit("--compare file must have the same number of scores (paired examples)")
        diffs = [y - x for x, y in zip(a, b)]
        data, label = diffs, "difference (B - A)"
        print(f"Mean A = {statistics.fmean(a):.4f}, mean B = {statistics.fmean(b):.4f}")
    else:
        data, label = a, "score"
    n = len(data)
    means = []
    for _ in range(args.resamples):
        means.append(statistics.fmean(data[rng.randrange(n)] for _ in range(n)))
    means.sort()
    lo, hi = percentile(means, alpha), percentile(means, 1 - alpha)
    print(f"Examples: {n}, resamples: {args.resamples}, seed: {args.seed}")
    print(f"Observed mean {label}: {statistics.fmean(data):.4f}")
    print(f"Bootstrap standard error: {statistics.stdev(means):.4f}")
    print(f"{args.confidence * 100:.0f}% percentile interval: [{lo:.4f}, {hi:.4f}] (width {hi - lo:.4f})")
    print(f"Range of resampled means: [{means[0]:.4f}, {means[-1]:.4f}]")
    if args.compare:
        wins = sum(1 for m in means if m > 0) / len(means)
        print(f"Share of resamples where B beats A: {wins:.3f}")
        verdict = "B is better" if lo > 0 else ("A is better" if hi < 0 else "not distinguishable")
        print(f"Verdict at {args.confidence * 100:.0f}%: {verdict}")
    elif hi - lo > args.max_width:
        print(f"Interval wider than --max-width {args.max_width}: grow the evaluation set.")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("size", help="estimate examples needed to detect a score gap")
    s.add_argument("--gap", type=float, required=True, help="absolute score gap, e.g. 0.05")
    s.add_argument("--baseline", type=float, default=0.5,
                   help="expected score of the weaker system, 0..1 (default 0.5, the worst case)")
    s.add_argument("--confidence", type=float, default=0.95, help="two-sided confidence (default 0.95)")
    s.add_argument("--power", type=float, default=0.8,
                   help="chance of detecting a gap that really exists (default 0.8)")
    s.set_defaults(func=cmd_size)
    b = sub.add_parser("bootstrap", help="bootstrap a confidence interval from per-example scores")
    b.add_argument("scores", help="file with one score per line (system A)")
    b.add_argument("--compare", help="paired score file for system B, same example order")
    b.add_argument("--resamples", type=int, default=2000, help="number of bootstrap resamples (default 2000)")
    b.add_argument("--confidence", type=float, default=0.95, help="interval level (default 0.95)")
    b.add_argument("--max-width", type=float, default=0.10,
                   help="warn if the single-system interval is wider than this (default 0.10)")
    b.add_argument("--seed", type=int, default=0, help="random seed (default 0)")
    b.set_defaults(func=cmd_bootstrap)
    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
