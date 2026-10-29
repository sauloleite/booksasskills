#!/usr/bin/env python3
"""Modularity metrics calculator (Martin package metrics plus class-level LCOM).

Inputs
  A JSON file with either or both top-level keys:

  "components": list of objects
      name      str   component, package or module name
      ca        int   afferent (incoming) coupling count
      ce        int   efferent (outgoing) coupling count
      abstract  int   number of abstract types (interfaces, abstract classes, protocols)
      concrete  int   number of concrete types

  "classes": list of objects
      name      str
      methods   object mapping method name -> list of field names it reads or writes

Outputs (stdout, text table by default, JSON with --json)
  Per component: Abstractness A = abstract / (abstract + concrete),
  Instability I = ce / (ce + ca), Distance D = |A + I - 1|, signed offset
  (A + I - 1), and a zone flag:
      pain        offset < 0 and D > threshold (concrete and heavily depended on)
      uselessness offset > 0 and D > threshold (abstract and nobody depends on it)
      balanced    D <= threshold
  Per class: LCOM1 (Chidamber-Kemerer pair count, P - Q floored at 0),
  LCOM96b (Henderson-Sellers, 0 = fully cohesive, near 1 = no sharing) and
  the number of disconnected method/field clusters (a split hint).

The threshold is a tool default, not a value from the book; tune it per code base.
Deterministic, standard library only, no network access.
"""
import argparse
import itertools
import json
import sys


def component_metrics(c, threshold):
    ab, co = c.get("abstract", 0), c.get("concrete", 0)
    ca, ce = c.get("ca", 0), c.get("ce", 0)
    a = ab / (ab + co) if ab + co else None
    i = ce / (ce + ca) if ce + ca else None
    row = {"name": c["name"], "A": a, "I": i, "D": None, "offset": None, "zone": "undefined"}
    if a is None or i is None:
        row["note"] = "no types" if a is None else "no couplings (isolated)"
        return row
    off = a + i - 1
    d = abs(off)
    zone = "balanced" if d <= threshold else ("pain" if off < 0 else "uselessness")
    row.update(A=round(a, 4), I=round(i, 4), D=round(d, 4), offset=round(off, 4), zone=zone)
    return row


def class_metrics(k):
    methods = {m: set(f) for m, f in sorted(k.get("methods", {}).items())}
    names = list(methods)
    p = q = 0
    for x, y in itertools.combinations(names, 2):
        if methods[x] & methods[y]:
            q += 1
        else:
            p += 1
    lcom1 = max(p - q, 0)
    fields = sorted(set().union(*methods.values())) if methods else []
    m, a = len(names), len(fields)
    lcom96b = None
    if m and a:
        lcom96b = sum((m - sum(1 for s in methods.values() if f in s)) / m for f in fields) / a
    # clusters: methods linked when they share a field (union-find)
    parent = {n: n for n in names}

    def find(n):
        while parent[n] != n:
            parent[n] = parent[parent[n]]
            n = parent[n]
        return n

    for x, y in itertools.combinations(names, 2):
        if methods[x] & methods[y]:
            parent[find(x)] = find(y)
    groups = {}
    for n in names:
        groups.setdefault(find(n), []).append(n)
    clusters = sorted(sorted(g) for g in groups.values())
    return {"name": k["name"], "methods": m, "fields": a, "LCOM1": lcom1,
            "LCOM96b": None if lcom96b is None else round(lcom96b, 4), "clusters": len(clusters), "cluster_members": clusters}


def fmt(v):
    return "-" if v is None else f"{v:.2f}"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("input", help="path to JSON input (see module docstring)")
    ap.add_argument("--threshold", type=float, default=0.5,
                    help="distance above which a component is flagged (default 0.5)")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of text")
    args = ap.parse_args()
    with open(args.input) as fh:
        data = json.load(fh)
    comps = [component_metrics(c, args.threshold) for c in data.get("components", [])]
    classes = [class_metrics(k) for k in data.get("classes", [])]
    if args.json:
        json.dump({"threshold": args.threshold, "components": comps, "classes": classes},
                  sys.stdout, indent=2)
        print()
        return
    if comps:
        print(f"{'component':<24}{'A':>6}{'I':>6}{'D':>6}{'A+I-1':>7}  zone")
        for r in comps:
            print(f"{r['name']:<24}{fmt(r['A']):>6}{fmt(r['I']):>6}{fmt(r['D']):>6}"
                  f"{fmt(r['offset']):>7}  {r['zone']}{' (' + r['note'] + ')' if 'note' in r else ''}")
    if classes:
        print(f"\n{'class':<24}{'meth':>5}{'fld':>5}{'LCOM1':>7}{'LCOM96b':>9}{'clusters':>9}")
        for r in classes:
            print(f"{r['name']:<24}{r['methods']:>5}{r['fields']:>5}{r['LCOM1']:>7}"
                  f"{fmt(r['LCOM96b']):>9}{r['clusters']:>9}")
            if r["clusters"] > 1:
                print(f"    split candidates: {r['cluster_members']}")


if __name__ == "__main__":
    main()
