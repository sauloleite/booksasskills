#!/usr/bin/env python3
"""Rank models from pairwise matches with Elo and Bradley-Terry, and score each
ranking by how well it predicts held-out matches.

Input: CSV with header model_a,model_b,winner where winner is the name of
model_a, model_b, or "tie". Ties count as half a win for each side.

Procedure:
  1. Deterministically split matches into train/test (every Nth match is
     held out, N from --holdout-every; default 5, i.e. 20%).
  2. Fit Elo (sequential updates, K from --k, start 1000) and Bradley-Terry
     (minorization-maximization, strengths normalized to geometric mean 1)
     on the training matches.
  3. Report each model's rating and rank, and held-out accuracy: share of
     decisive test matches where the higher-rated model won. Also log loss.
  4. Refit both on all matches for the final leaderboard.

Bradley-Terry is order-invariant; Elo depends on match order. Use --shuffle-seed
to replay Elo in a different (seeded) order and see that sensitivity.
Output: plain-text tables to stdout. Deterministic for fixed inputs and seed.
"""
import argparse
import csv
import math
import random
import sys
from collections import defaultdict


def load(path):
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    out = []
    for r in rows:
        a, b, w = r["model_a"].strip(), r["model_b"].strip(), r["winner"].strip()
        if w not in (a, b, "tie"):
            raise ValueError(f"winner {w!r} is neither {a!r}, {b!r} nor 'tie'")
        score_a = 1.0 if w == a else 0.0 if w == b else 0.5
        out.append((a, b, score_a))
    return out


def fit_elo(matches, k=16.0, start=1000.0):
    r = defaultdict(lambda: start)
    for a, b, s in matches:
        ea = 1.0 / (1.0 + 10 ** ((r[b] - r[a]) / 400.0))
        r[a] += k * (s - ea)
        r[b] -= k * (s - ea)
    return dict(r)


def elo_prob(ra, rb):
    return 1.0 / (1.0 + 10 ** ((rb - ra) / 400.0))


def fit_bt(matches, iters=1000, tol=1e-10, prior=0.5):
    """MM algorithm (Hunter 2004). A small prior (virtual tie vs every other
    model) keeps strengths finite when a model never loses or never wins."""
    models = sorted({m for a, b, _ in matches for m in (a, b)})
    wins = defaultdict(float)
    games = defaultdict(float)
    for a, b, s in matches:
        wins[a] += s
        wins[b] += 1 - s
        games[frozenset((a, b))] += 1
    for i, x in enumerate(models):
        for y in models[i + 1:]:
            wins[x] += prior / 2
            wins[y] += prior / 2
            games[frozenset((x, y))] += prior
    p = {m: 1.0 for m in models}
    for _ in range(iters):
        new = {}
        for i in models:
            denom = sum(games[frozenset((i, j))] / (p[i] + p[j]) for j in models if j != i)
            new[i] = wins[i] / denom
        g = math.exp(sum(math.log(v) for v in new.values()) / len(new))
        new = {m: v / g for m, v in new.items()}
        done = max(abs(new[m] - p[m]) for m in models) < tol
        p = new
        if done:
            break
    return p


def bt_prob(pa, pb):
    return pa / (pa + pb)


def evaluate(test, prob):
    decisive = [(a, b, s) for a, b, s in test if s != 0.5]
    correct = sum(1 for a, b, s in decisive if (prob(a, b) > 0.5) == (s == 1.0))
    eps = 1e-12
    ll = -sum(s * math.log(max(prob(a, b), eps)) + (1 - s) * math.log(max(1 - prob(a, b), eps))
              for a, b, s in test) / max(1, len(test))
    acc = correct / len(decisive) if decisive else float("nan")
    return acc, len(decisive), ll


def table(title, ratings, fmt):
    print(title)
    for rank, (m, v) in enumerate(sorted(ratings.items(), key=lambda kv: -kv[1]), 1):
        print(f"  {rank:>2}. {m:<20} {fmt.format(v)}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv", help="matches CSV: model_a,model_b,winner")
    ap.add_argument("--k", type=float, default=16.0, help="Elo K factor (default 16)")
    ap.add_argument("--holdout-every", type=int, default=5, help="hold out every Nth match (default 5)")
    ap.add_argument("--shuffle-seed", type=int, help="replay matches in a seeded random order")
    args = ap.parse_args()

    matches = load(args.csv)
    if args.shuffle_seed is not None:
        random.Random(args.shuffle_seed).shuffle(matches)
    n = args.holdout_every
    test = [m for i, m in enumerate(matches) if n > 0 and i % n == n - 1]
    train = [m for i, m in enumerate(matches) if not (n > 0 and i % n == n - 1)]
    print(f"matches: {len(matches)}  train: {len(train)}  held out: {len(test)}")

    if test:
        elo = fit_elo(train, args.k)
        bt = fit_bt(train)
        unseen = {m for a, b, _ in test for m in (a, b)} - set(bt)
        if unseen:
            print(f"warning: models only in held-out set: {sorted(unseen)}")
        e_acc, nd, e_ll = evaluate(test, lambda a, b: elo_prob(elo.get(a, 1000), elo.get(b, 1000)))
        b_acc, _, b_ll = evaluate(test, lambda a, b: bt_prob(bt.get(a, 1.0), bt.get(b, 1.0)))
        print(f"held-out accuracy on {nd} decisive matches: Elo {e_acc:.3f} (log loss {e_ll:.3f}), "
              f"Bradley-Terry {b_acc:.3f} (log loss {b_ll:.3f})")

    print()
    table("Elo (all matches):", fit_elo(matches, args.k), "{:8.1f}")
    bt_all = fit_bt(matches)
    # Elo-like display scale: 400*log10(strength) + 1000
    table("Bradley-Terry (all matches, Elo-like scale):",
          {m: 400 * math.log10(v) + 1000 for m, v in bt_all.items()}, "{:8.1f}")


if __name__ == "__main__":
    sys.exit(main())
