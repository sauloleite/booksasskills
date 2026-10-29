#!/usr/bin/env python3
"""Compare a baseline and a current sample for distribution shift (PSI, KS, KL).

Modes:
  numeric      two files of numbers (one per line, or comma/space separated), e.g.
               query lengths or latencies. Computes two-sample KS (exact statistic;
               asymptotic p-value, approximate for small n) and PSI over baseline-quantile bins (--bins).
  categorical  two files of labels (one per line), e.g. tool or intent per request;
               or two CSV count files "label,count". Computes PSI and KL(baseline||current).

Verdicts use the chapter's default thresholds, overridable by flags:
  PSI < 0.1 stable, 0.1-0.25 minor (monitor), > 0.25 major (intervene)
  KS statistic > 0.1 AND p < 0.05 -> drift;  KL > 0.5 -> concept drift
Zero bins are floored with --eps. Output: text, or JSON with --json.
Deterministic, stdlib only, no network.
"""
import argparse
import json
import math
import re
import sys
from collections import Counter


def read_numbers(path):
    with open(path, encoding="utf-8") as fh:
        vals = [float(x) for x in re.split(r"[,\s]+", fh.read().strip()) if x]
    if not vals:
        sys.exit(f"{path}: no numbers")
    return vals


def read_counts(path):
    c = Counter()
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            parts = line.rsplit(",", 1)
            if len(parts) == 2 and re.fullmatch(r"\s*\d+(\.\d+)?\s*", parts[1]):
                c[parts[0].strip()] += float(parts[1])
            else:
                c[line] += 1
    if not c:
        sys.exit(f"{path}: no labels")
    return c


def normalize(counts, eps):
    floored = [max(x, 0.0) + eps for x in counts]
    s = sum(floored)
    return [x / s for x in floored]


def psi(base_counts, cur_counts, eps):
    e, a = normalize(base_counts, eps), normalize(cur_counts, eps)
    return sum((ai - ei) * math.log(ai / ei) for ai, ei in zip(a, e))


def kl(base_counts, cur_counts, eps):
    p, q = normalize(base_counts, eps), normalize(cur_counts, eps)
    return sum(pi * math.log(pi / qi) for pi, qi in zip(p, q))


def ks_2samp(x, y):
    x, y = sorted(x), sorted(y)
    n, m = len(x), len(y)
    i = j = 0
    d = 0.0
    while i < n and j < m:
        v = min(x[i], y[j])
        while i < n and x[i] == v:
            i += 1
        while j < m and y[j] == v:
            j += 1
        d = max(d, abs(i / n - j / m))
    # Asymptotic Kolmogorov distribution with Stephens' small-sample correction.
    en = math.sqrt(n * m / (n + m))
    lam = (en + 0.12 + 0.11 / en) * d
    if lam < 1e-3:
        return d, 1.0
    p = 2 * sum((-1) ** (k - 1) * math.exp(-2 * k * k * lam * lam) for k in range(1, 101))
    return d, min(1.0, max(0.0, p))


def quantile_edges(base, bins):
    s = sorted(base)
    edges = []
    for k in range(1, bins):
        e = s[min(len(s) - 1, int(k * len(s) / bins))]
        if not edges or e > edges[-1]:
            edges.append(e)
    return edges


def bin_counts(vals, edges):
    counts = [0] * (len(edges) + 1)
    for v in vals:
        idx = 0
        while idx < len(edges) and v >= edges[idx]:
            idx += 1
        counts[idx] += 1
    return counts


def psi_verdict(v, minor, major):
    return "major drift (intervene)" if v > major else "minor drift (monitor)" if v > minor else "stable"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("mode", choices=["numeric", "categorical"])
    ap.add_argument("baseline", help="baseline (historical) sample file")
    ap.add_argument("current", help="current sample file")
    ap.add_argument("--bins", type=int, default=10, help="numeric PSI bins from baseline quantiles")
    ap.add_argument("--eps", type=float, default=1e-6, help="floor added to every bin share")
    ap.add_argument("--psi-minor", type=float, default=0.1)
    ap.add_argument("--psi-major", type=float, default=0.25)
    ap.add_argument("--ks-stat", type=float, default=0.1)
    ap.add_argument("--ks-alpha", type=float, default=0.05)
    ap.add_argument("--kl-max", type=float, default=0.5)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    out = {"mode": a.mode}
    if a.mode == "numeric":
        b, c = read_numbers(a.baseline), read_numbers(a.current)
        d, p = ks_2samp(b, c)
        edges = quantile_edges(b, a.bins)
        bc, cc = bin_counts(b, edges), bin_counts(c, edges)
        v = psi(bc, cc, a.eps)
        out.update({"n_baseline": len(b), "n_current": len(c),
                    "mean_baseline": sum(b) / len(b), "mean_current": sum(c) / len(c),
                    "ks_statistic": d, "ks_p_value": p,
                    "ks_drift": d > a.ks_stat and p < a.ks_alpha,
                    "psi": v, "psi_verdict": psi_verdict(v, a.psi_minor, a.psi_major),
                    "bin_edges": edges, "baseline_bins": bc, "current_bins": cc})
        if min(len(b), len(c)) < 30:
            out["warning"] = "small sample: KS and PSI are unstable below ~30 per side"
    else:
        b, c = read_counts(a.baseline), read_counts(a.current)
        labels = sorted(set(b) | set(c))
        bc, cc = [b.get(l, 0) for l in labels], [c.get(l, 0) for l in labels]
        v, k = psi(bc, cc, a.eps), kl(bc, cc, a.eps)
        bs, cs = normalize(bc, 0), normalize(cc, 0)
        out.update({"labels": labels, "baseline_share": bs, "current_share": cs,
                    "psi": v, "psi_verdict": psi_verdict(v, a.psi_minor, a.psi_major),
                    "kl_baseline_to_current": k, "kl_drift": k > a.kl_max,
                    "new_labels": [l for l in labels if b.get(l, 0) == 0]})
    if a.json:
        print(json.dumps(out, indent=2, sort_keys=True))
        return
    for key in sorted(out):
        val = out[key]
        if isinstance(val, float):
            val = f"{val:.4f}"
        elif isinstance(val, list) and val and isinstance(val[0], float):
            val = "[" + ", ".join(f"{x:.3f}" for x in val) + "]"
        print(f"{key}: {val}")


if __name__ == "__main__":
    main()
