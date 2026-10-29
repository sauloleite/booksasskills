#!/usr/bin/env python3
"""Unbiased pass@k estimator for functional-correctness evaluation.

For each problem you generated n samples and c of them passed all tests.
The per-problem estimate is 1 - C(n-c, k) / C(n, k) (Chen et al., 2021);
the benchmark score is the mean over problems.

Inputs (choose one):
  --n N --c C           a single problem
  --csv FILE            CSV with columns n,c (header row required), one row per problem
  -k K [K ...]          one or more k values (default: 1 5 10)

Output: a table with pass@k per k. With --csv, also the number of problems.
k values larger than n for some problem are reported as undefined (n/a).
"""
import argparse
import csv
import sys
from math import comb


def pass_at_k(n: int, c: int, k: int) -> float:
    """Unbiased probability that at least one of k samples (drawn from n) is correct."""
    if not 0 <= c <= n:
        raise ValueError(f"need 0 <= c <= n, got n={n}, c={c}")
    if k > n:
        raise ValueError(f"k={k} exceeds n={n}")
    if n - c < k:
        return 1.0
    return 1.0 - comb(n - c, k) / comb(n, k)


def read_problems(path):
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    return [(int(r["n"]), int(r["c"])) for r in rows]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--n", type=int, help="samples generated (single problem)")
    ap.add_argument("--c", type=int, help="samples that passed (single problem)")
    ap.add_argument("--csv", help="CSV file with columns n,c")
    ap.add_argument("-k", type=int, nargs="+", default=[1, 5, 10], help="k values")
    args = ap.parse_args()

    if args.csv:
        problems = read_problems(args.csv)
    elif args.n is not None and args.c is not None:
        problems = [(args.n, args.c)]
    else:
        ap.error("give --n and --c, or --csv")

    print(f"problems: {len(problems)}")
    for k in args.k:
        if any(k > n for n, _ in problems):
            print(f"pass@{k}: n/a (k exceeds n for at least one problem)")
            continue
        score = sum(pass_at_k(n, c, k) for n, c in problems) / len(problems)
        print(f"pass@{k}: {score:.4f}")


if __name__ == "__main__":
    sys.exit(main())
