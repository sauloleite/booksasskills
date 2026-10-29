#!/usr/bin/env python3
"""Compute retrieval quality metrics for a RAG retriever.

Input: a JSON file (or '-' for stdin) holding a list of query records:
  [
    {"query": "q1",
     "retrieved": ["d3", "d1", "d7"],          # ranked list, best first
     "relevant": ["d1", "d2"]                    # binary labels, or
     # "relevant": {"d1": 3, "d2": 1}            # graded labels (gain) for NDCG
    },
    ...
  ]

Output: per-query and mean values of
  precision@k  (context precision: relevant share of the top k retrieved)
  recall@k     (context recall: share of all relevant docs found in top k)
  RR           (reciprocal rank of the first relevant doc; mean is MRR)
  AP@k         (average precision; mean is MAP). Normalized by
               min(number of relevant docs, k).
  NDCG@k       (gain / log2(rank + 1), normalized by the ideal ordering)

k defaults to the length of each retrieved list. Queries with no relevant
docs get recall, AP and NDCG of 0. Results are printed as a table, or as
JSON with --json. Deterministic, standard library only.
"""
import argparse
import json
import math
import sys


def gains(relevant):
    if isinstance(relevant, dict):
        return {d: float(g) for d, g in relevant.items() if float(g) > 0}
    return {d: 1.0 for d in relevant}


def score_query(retrieved, relevant, k):
    g = gains(relevant)
    top = retrieved[:k] if k else list(retrieved)
    kk = len(top)
    hits = [1 if d in g else 0 for d in top]
    n_rel = len(g)
    precision = sum(hits) / kk if kk else 0.0
    recall = sum(hits) / n_rel if n_rel else 0.0
    rr = 0.0
    for i, h in enumerate(hits, start=1):
        if h:
            rr = 1.0 / i
            break
    ap_sum, found = 0.0, 0
    for i, h in enumerate(hits, start=1):
        if h:
            found += 1
            ap_sum += found / i
    denom = min(n_rel, kk)
    ap = ap_sum / denom if denom else 0.0
    dcg = sum(g.get(d, 0.0) / math.log2(i + 1) for i, d in enumerate(top, start=1))
    ideal = sorted(g.values(), reverse=True)[:kk]
    idcg = sum(v / math.log2(i + 1) for i, v in enumerate(ideal, start=1))
    ndcg = dcg / idcg if idcg else 0.0
    return {"precision": precision, "recall": recall, "rr": rr, "ap": ap, "ndcg": ndcg}


def main():
    p = argparse.ArgumentParser(description="Precision@k, recall@k, MRR, MAP and NDCG for ranked retrieval results.")
    p.add_argument("path", help="JSON file with query records, or '-' for stdin")
    p.add_argument("-k", type=int, default=0, help="cutoff (default: full retrieved list)")
    p.add_argument("--json", action="store_true", help="print JSON instead of a table")
    a = p.parse_args()
    data = json.load(sys.stdin if a.path == "-" else open(a.path))
    rows = []
    for i, rec in enumerate(data):
        m = score_query(rec["retrieved"], rec["relevant"], a.k)
        m["query"] = rec.get("query", f"q{i + 1}")
        rows.append(m)
    keys = ["precision", "recall", "rr", "ap", "ndcg"]
    mean = {key: sum(r[key] for r in rows) / len(rows) for key in keys} if rows else {}
    if a.json:
        print(json.dumps({"k": a.k or None, "per_query": rows, "mean": mean}, indent=2))
        return
    label = f"@{a.k}" if a.k else ""
    print(f"{'query':<20}{'P' + label:>9}{'R' + label:>9}{'RR':>9}{'AP' + label:>9}{'NDCG' + label:>10}")
    for r in rows:
        print(f"{r['query'][:19]:<20}" + "".join(f"{r[x]:>9.3f}" for x in keys[:4]) + f"{r['ndcg']:>10.3f}")
    print(f"{'MEAN':<20}" + "".join(f"{mean[x]:>9.3f}" for x in keys[:4]) + f"{mean['ndcg']:>10.3f}")
    print("(mean RR = MRR, mean AP = MAP)")


if __name__ == "__main__":
    main()
