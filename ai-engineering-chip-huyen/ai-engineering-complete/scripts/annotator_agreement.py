#!/usr/bin/env python3
"""Inter-annotator agreement (Cohen's kappa) between two label files.

Inputs: two files with labels from annotator A and annotator B. Accepted formats,
        detected by extension:
          .jsonl  objects with an id field and a label field (--id-field, --label-field)
          .csv    header row with the same two columns
          other   plain text, one label per line, aligned by line number
        With ids, items are aligned by id and unmatched ids are reported.
Output: on stdout: item count, observed agreement, chance agreement, Cohen's kappa
        (unweighted, or linear/quadratic weighted for ordinal scores with --weights),
        per-annotator label distributions (to spot an annotator skewing high or low),
        a confusion matrix, and the ids/lines of disagreements to review.
Formula: kappa = (p_o - p_e) / (1 - p_e), with p_e from each annotator's marginals.
         Weighted: kappa_w = 1 - sum(w*O) / sum(w*E), w = |i-j|/(k-1) or ((i-j)/(k-1))**2.
Standard library only; deterministic; no network.
Example:
  python3 annotator_agreement.py a.jsonl b.jsonl --weights quadratic
"""
import argparse
import csv
import json
import os
from collections import Counter


def load(path, id_field, label_field):
    ext = os.path.splitext(path)[1].lower()
    out = {}
    with open(path, encoding="utf-8", newline="") as fh:
        if ext == ".jsonl":
            for line in fh:
                if line.strip():
                    o = json.loads(line)
                    out[str(o[id_field])] = str(o[label_field]).strip()
        elif ext == ".csv":
            for r in csv.DictReader(fh):
                out[str(r[id_field])] = str(r[label_field]).strip()
        else:
            n = 0
            for line in fh:
                if line.strip():
                    n += 1
                    out[f"line{n}"] = line.strip()
    return out


def sort_labels(labels):
    try:
        return sorted(labels, key=float)
    except ValueError:
        return sorted(labels)


def kappa(pairs, cats, weights):
    n, k = len(pairs), len(cats)
    idx = {c: i for i, c in enumerate(cats)}
    obs = [[0] * k for _ in range(k)]
    for x, y in pairs:
        obs[idx[x]][idx[y]] += 1
    row = [sum(obs[i]) for i in range(k)]
    col = [sum(obs[i][j] for i in range(k)) for j in range(k)]
    p_o = sum(obs[i][i] for i in range(k)) / n
    p_e = sum(row[i] * col[i] for i in range(k)) / (n * n)
    if weights == "none":
        kap = 1.0 if p_e == 1 else (p_o - p_e) / (1 - p_e)
    else:
        def w(i, j):
            d = abs(i - j) / (k - 1) if k > 1 else 0
            return d if weights == "linear" else d * d
        num = sum(w(i, j) * obs[i][j] for i in range(k) for j in range(k))
        den = sum(w(i, j) * row[i] * col[j] / n for i in range(k) for j in range(k))
        kap = 1.0 if den == 0 else 1 - num / den
    return p_o, p_e, kap, obs


def interpret(k):
    # Landis and Koch (1977) bands, a common convention, not a hard rule.
    for lim, name in [(0, "poor"), (0.2, "slight"), (0.4, "fair"), (0.6, "moderate"),
                      (0.8, "substantial")]:
        if k <= lim:
            return name
    return "almost perfect"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file_a")
    ap.add_argument("file_b")
    ap.add_argument("--id-field", default="id")
    ap.add_argument("--label-field", default="label")
    ap.add_argument("--weights", choices=["none", "linear", "quadratic"], default="none",
                    help="use linear/quadratic for ordinal scores such as 1-5 ratings")
    ap.add_argument("--max-list", type=int, default=20, help="disagreements to print")
    a = ap.parse_args()

    A = load(a.file_a, a.id_field, a.label_field)
    B = load(a.file_b, a.id_field, a.label_field)
    common = sorted(set(A) & set(B), key=lambda s: (len(s), s))
    only_a, only_b = sorted(set(A) - set(B)), sorted(set(B) - set(A))
    if not common:
        raise SystemExit("no overlapping items")
    pairs = [(A[i], B[i]) for i in common]
    cats = sort_labels({l for p in pairs for l in p})
    p_o, p_e, kap, obs = kappa(pairs, cats, a.weights)

    print(f"Items compared: {len(pairs)}  (only in A: {len(only_a)}, only in B: {len(only_b)})")
    print(f"Observed agreement p_o: {p_o:.4f}")
    print(f"Chance agreement  p_e: {p_e:.4f}")
    label = "Cohen's kappa" if a.weights == "none" else f"{a.weights}-weighted kappa"
    print(f"{label}: {kap:.4f}  ({interpret(kap)})")
    ca, cb = Counter(x for x, _ in pairs), Counter(y for _, y in pairs)
    print("Label distribution  A: " + ", ".join(f"{c}={ca[c]}" for c in cats))
    print("Label distribution  B: " + ", ".join(f"{c}={cb[c]}" for c in cats))
    w = max(5, max(len(c) for c in cats) + 1)
    print("Confusion (rows A, cols B):")
    print(" " * w + "".join(c.rjust(w) for c in cats))
    for c, r in zip(cats, obs):
        print(c.rjust(w) + "".join(str(v).rjust(w) for v in r))
    dis = [(i, A[i], B[i]) for i in common if A[i] != B[i]]
    print(f"Disagreements: {len(dis)}")
    for i, x, y in dis[:a.max_list]:
        print(f"  {i}: A={x} B={y}")


if __name__ == "__main__":
    main()
