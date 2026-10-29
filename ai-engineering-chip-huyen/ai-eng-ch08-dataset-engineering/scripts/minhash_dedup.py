#!/usr/bin/env python3
"""Near-duplicate detection for a JSONL dataset with MinHash + LSH banding (stdlib only).

Input:  a JSONL file; --fields names the text field(s) to compare (joined with a space).
Method: text is lowercased, split into word tokens and turned into a set of word
        n-gram shingles (--shingle, default 5; texts shorter than that become one shingle).
        Each set gets a MinHash signature of --num-perm values built from seeded
        universal hashes over a stable 64-bit blake2b hash of each shingle.
        Signatures are cut into --bands bands; rows sharing any band bucket become
        candidate pairs. Every candidate's EXACT Jaccard similarity is then computed
        and pairs at or above --threshold are linked with union-find into clusters.
        With b bands of r rows, a pair of true Jaccard s becomes a candidate with
        probability 1 - (1 - s**r)**b; the script prints the threshold where that
        curve is steepest, approx (1/b)**(1/r), so you can tune bands.
Output: a report on stdout (clusters with line numbers and similarities).
        --keep-out FILE writes the deduplicated JSONL (first row of each cluster kept).
        --clusters-out FILE writes the clusters as JSON for auditing.
Deterministic for a given --seed; no network.
Example:
  python3 minhash_dedup.py data.jsonl --fields instruction response --threshold 0.8
"""
import argparse
import hashlib
import json
import random
import re
from collections import defaultdict

PRIME = (1 << 61) - 1
MAXH = (1 << 64) - 1


def shingles(text, k):
    toks = re.findall(r"\w+", text.lower())
    if not toks:
        return set()
    if len(toks) < k:
        return {" ".join(toks)}
    return {" ".join(toks[i:i + k]) for i in range(len(toks) - k + 1)}


def h64(s):
    return int.from_bytes(hashlib.blake2b(s.encode("utf-8"), digest_size=8).digest(), "big")


def signature(sh, coeffs):
    hs = [h64(s) for s in sh]
    return tuple(min((a * x + b) % PRIME for x in hs) for a, b in coeffs)


def jaccard(a, b):
    return len(a & b) / len(a | b) if (a or b) else 1.0


class UnionFind:
    def __init__(self, n):
        self.p = list(range(n))

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[max(ra, rb)] = min(ra, rb)  # smallest index stays representative


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", help="input JSONL")
    ap.add_argument("--fields", nargs="+", required=True, help="text field(s) to compare")
    ap.add_argument("--shingle", type=int, default=5, help="word n-gram size (default 5)")
    ap.add_argument("--num-perm", type=int, default=128, help="MinHash signature length (default 128)")
    ap.add_argument("--bands", type=int, default=32, help="LSH bands; must divide --num-perm (default 32)")
    ap.add_argument("--threshold", type=float, default=0.8, help="exact Jaccard needed to call a duplicate")
    ap.add_argument("--seed", type=int, default=13, help="hash seed for reproducibility")
    ap.add_argument("--keep-out", help="write deduplicated JSONL here")
    ap.add_argument("--clusters-out", help="write duplicate clusters JSON here")
    a = ap.parse_args()
    if a.num_perm % a.bands:
        ap.error("--bands must divide --num-perm")
    rows_per_band = a.num_perm // a.bands

    rng = random.Random(a.seed)
    coeffs = [(rng.randrange(1, PRIME), rng.randrange(0, PRIME)) for _ in range(a.num_perm)]

    raw, sets, lines = [], [], []
    with open(a.path, encoding="utf-8") as fh:
        for ln, line in enumerate(fh, 1):
            if not line.strip():
                continue
            obj = json.loads(line)
            text = " ".join(str(obj.get(f, "")) for f in a.fields)
            raw.append(line.rstrip("\n"))
            sets.append(shingles(text, a.shingle))
            lines.append(ln)

    buckets = defaultdict(list)
    for i, sh in enumerate(sets):
        if not sh:
            continue  # empty texts are reported by inspection, not clustered here
        sig = signature(sh, coeffs)
        for b in range(a.bands):
            band = sig[b * rows_per_band:(b + 1) * rows_per_band]
            buckets[(b, band)].append(i)

    candidates = set()
    for members in buckets.values():
        for x in range(len(members)):
            for y in range(x + 1, len(members)):
                candidates.add((members[x], members[y]))

    uf = UnionFind(len(sets))
    pair_sim = {}
    for i, j in sorted(candidates):
        s = jaccard(sets[i], sets[j])
        if s >= a.threshold:
            uf.union(i, j)
            pair_sim[(i, j)] = s

    clusters = defaultdict(list)
    for i in range(len(sets)):
        clusters[uf.find(i)].append(i)
    dup_clusters = [sorted(m) for m in clusters.values() if len(m) > 1]
    dup_clusters.sort()
    removed = {i for m in dup_clusters for i in m[1:]}

    print(f"Rows: {len(sets)}  shingle={a.shingle}  num_perm={a.num_perm}  "
          f"bands={a.bands} x rows={rows_per_band}")
    print(f"LSH curve steepest near Jaccard ~{(1 / a.bands) ** (1 / rows_per_band):.2f}; "
          f"verification threshold {a.threshold}")
    print(f"Candidate pairs: {len(candidates)}  confirmed pairs: {len(pair_sim)}")
    print(f"Duplicate clusters: {len(dup_clusters)}  rows to drop: {len(removed)}  "
          f"rows kept: {len(sets) - len(removed)}")
    out_clusters = []
    for m in dup_clusters:
        sims = [round(s, 3) for (i, j), s in sorted(pair_sim.items()) if i in m and j in m]
        print(f"  keep line {lines[m[0]]}, drop lines {[lines[i] for i in m[1:]]}, pair Jaccards {sims}")
        out_clusters.append({"keep": lines[m[0]], "drop": [lines[i] for i in m[1:]], "pair_jaccards": sims})

    if a.keep_out:
        with open(a.keep_out, "w", encoding="utf-8") as fh:
            for i, r in enumerate(raw):
                if i not in removed:
                    fh.write(r + "\n")
    if a.clusters_out:
        with open(a.clusters_out, "w", encoding="utf-8") as fh:
            json.dump(out_clusters, fh, indent=2)


if __name__ == "__main__":
    main()
