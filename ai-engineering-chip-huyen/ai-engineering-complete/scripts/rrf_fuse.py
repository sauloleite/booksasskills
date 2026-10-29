#!/usr/bin/env python3
"""Merge several ranked retrieval lists with Reciprocal Rank Fusion (RRF).

score(D) = sum over lists i of 1 / (k + rank_i(D)), ranks starting at 1.
Lists that do not contain D contribute nothing. k defaults to 60.

Input: a JSON object mapping retriever name to a ranked list of doc ids
(best first), from a file or '-' for stdin, e.g.
  {"bm25": ["d1", "d2", "d3"], "dense": ["d3", "d1", "d9"]}
Output: the fused ranking with each document's RRF score and its rank in
each input list ('-' if absent). Ties are broken by best single rank,
then by doc id, so output is deterministic. Use --top to truncate and
--json for machine-readable output.
"""
import argparse
import json
import sys


def rrf(lists, k=60):
    scores, ranks = {}, {}
    for name, ranking in lists.items():
        seen = set()
        for r, doc in enumerate(ranking, start=1):
            if doc in seen:
                continue  # count only the first occurrence per list
            seen.add(doc)
            scores[doc] = scores.get(doc, 0.0) + 1.0 / (k + r)
            ranks.setdefault(doc, {})[name] = r
    order = sorted(scores, key=lambda d: (-scores[d], min(ranks[d].values()), d))
    return [(d, scores[d], ranks[d]) for d in order]


def main():
    p = argparse.ArgumentParser(description="Reciprocal Rank Fusion of ranked lists.")
    p.add_argument("path", help="JSON file {retriever: [doc ids best first]}, or '-' for stdin")
    p.add_argument("-k", type=float, default=60, help="RRF constant (default 60)")
    p.add_argument("--top", type=int, default=0, help="keep only the top N fused results")
    p.add_argument("--json", action="store_true", help="print JSON")
    a = p.parse_args()
    lists = json.load(sys.stdin if a.path == "-" else open(a.path))
    fused = rrf(lists, a.k)
    if a.top:
        fused = fused[: a.top]
    if a.json:
        print(json.dumps([{"doc": d, "score": s, "ranks": r} for d, s, r in fused], indent=2))
        return
    names = list(lists)
    print(f"{'rank':<6}{'doc':<14}{'rrf_score':>11}  " + "  ".join(f"{n[:10]:>10}" for n in names))
    for i, (d, s, r) in enumerate(fused, start=1):
        cols = "  ".join(f"{str(r.get(n, '-')):>10}" for n in names)
        print(f"{i:<6}{d[:13]:<14}{s:>11.5f}  {cols}")


if __name__ == "__main__":
    main()
