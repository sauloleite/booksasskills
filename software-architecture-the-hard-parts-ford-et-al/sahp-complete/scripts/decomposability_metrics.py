#!/usr/bin/env python3
"""Compute component coupling and balance metrics to judge whether a codebase is decomposable.

Inputs
  --components CSV (required), header row with columns:
      component, abstract, concrete            (counts of abstract / concrete artifacts)
      optional: ca, ce                         (afferent / efferent coupling counts)
  --edges CSV (optional), header row with columns: source, target
      One row per dependency "source depends on target" between components.
      When given, Ca and Ce are derived from the distinct component-to-component
      edges and override any ca/ce columns. Self-edges and edges to unknown
      components are ignored (unknown targets are reported).

Metrics per component
  Ca  afferent coupling (incoming dependencies)
  Ce  efferent coupling (outgoing dependencies)
  A   abstractness = abstract / (abstract + concrete)   [Martin's bounded form]
      use --abstractness-denominator concrete for abstract / concrete (capped at 1)
  I   instability = Ce / (Ce + Ca); components with Ca + Ce = 0 are flagged "isolated" (I = 0)
  D   normalized distance from the main sequence = |A + I - 1|
  zone  "pain" (low A, low I side), "uselessness" (high A, high I side) or "balanced",
        using --zone-threshold on D (heuristic default 0.5; the book gives no cut-off)

Outputs
  A table sorted by D (worst first), the most widely used components (highest Ca,
  i.e. shared assets that need an ownership decision before splitting), and a summary
  with mean D, share of components in each zone and a heuristic decomposability hint.
  --json prints the same data as JSON. Deterministic; standard library only.
"""

import argparse
import csv
import json
import sys


def read_components(path):
    comps = {}
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        required = {"component", "abstract", "concrete"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            sys.exit(f"components CSV missing columns: {', '.join(sorted(missing))}")
        for row in reader:
            name = row["component"].strip()
            if not name:
                continue
            comps[name] = {
                "abstract": int(row["abstract"]),
                "concrete": int(row["concrete"]),
                "ca": int(row["ca"]) if row.get("ca") not in (None, "") else 0,
                "ce": int(row["ce"]) if row.get("ce") not in (None, "") else 0,
            }
    if not comps:
        sys.exit("components CSV has no rows")
    return comps


def apply_edges(comps, path):
    edges, unknown = set(), set()
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if not {"source", "target"} <= set(reader.fieldnames or []):
            sys.exit("edges CSV needs columns: source, target")
        for row in reader:
            s, t = row["source"].strip(), row["target"].strip()
            if s == t:
                continue
            for n in (s, t):
                if n not in comps:
                    unknown.add(n)
            if s in comps and t in comps:
                edges.add((s, t))
    for c in comps.values():
        c["ca"] = c["ce"] = 0
    for s, t in sorted(edges):
        comps[s]["ce"] += 1
        comps[t]["ca"] += 1
    return sorted(unknown)


def compute(comps, denom, threshold):
    rows = []
    for name in sorted(comps):
        c = comps[name]
        na, nc = c["abstract"], c["concrete"]
        if denom == "total":
            a = na / (na + nc) if (na + nc) else 0.0
        else:
            a = min(1.0, na / nc) if nc else (1.0 if na else 0.0)
        total = c["ca"] + c["ce"]
        i = c["ce"] / total if total else 0.0
        signed = a + i - 1
        d = abs(signed)
        if d < threshold:
            zone = "balanced"
        elif signed < 0:
            zone = "pain"
        else:
            zone = "uselessness"
        rows.append({
            "component": name, "abstract": na, "concrete": nc,
            "ca": c["ca"], "ce": c["ce"], "A": round(a, 3), "I": round(i, 3),
            "D": round(d, 3), "zone": zone, "isolated": total == 0,
        })
    return rows


def summarize(rows, threshold):
    n = len(rows)
    mean_d = sum(r["D"] for r in rows) / n
    counts = {z: sum(1 for r in rows if r["zone"] == z) for z in ("balanced", "pain", "uselessness")}
    off = (counts["pain"] + counts["uselessness"]) / n
    if off <= 0.2 and mean_d < threshold:
        hint = ("most components sit near the main sequence: structure looks salvageable; "
                "next decide between component-based decomposition and tactical forking")
    elif off <= 0.5:
        hint = ("mixed: decomposable with effort; fix or isolate the outlier components "
                "before extracting services")
    else:
        hint = ("most components are in the zones of pain or uselessness: repairing structure may "
                "not pay off; consider tactical forking or a rewrite, and confirm by inspecting code")
    return {"components": n, "mean_D": round(mean_d, 3), "zone_counts": counts,
            "share_outside_balanced": round(off, 3), "hint": hint}


def main():
    p = argparse.ArgumentParser(
        description="Coupling, abstractness, instability and distance-from-main-sequence "
                    "metrics for a set of components (decomposability check).")
    p.add_argument("--components", required=True, help="CSV: component,abstract,concrete[,ca,ce]")
    p.add_argument("--edges", help="CSV: source,target dependency edges (overrides ca/ce)")
    p.add_argument("--abstractness-denominator", choices=["total", "concrete"], default="total",
                   help="total: A = abstract/(abstract+concrete) (default); concrete: abstract/concrete capped at 1")
    p.add_argument("--zone-threshold", type=float, default=0.5,
                   help="D at or above this marks a component as pain/uselessness (heuristic, default 0.5)")
    p.add_argument("--top-shared", type=int, default=5, help="how many highest-Ca components to list")
    p.add_argument("--json", action="store_true", help="emit JSON instead of text")
    args = p.parse_args()

    comps = read_components(args.components)
    unknown = apply_edges(comps, args.edges) if args.edges else []
    rows = compute(comps, args.abstractness_denominator, args.zone_threshold)
    summary = summarize(rows, args.zone_threshold)
    shared = sorted(rows, key=lambda r: (-r["ca"], r["component"]))[: args.top_shared]

    if args.json:
        print(json.dumps({"components": rows, "most_shared": [r["component"] for r in shared],
                          "unknown_in_edges": unknown, "summary": summary}, indent=2))
        return

    hdr = f"{'component':<28}{'Na':>5}{'Nc':>5}{'Ca':>5}{'Ce':>5}{'A':>7}{'I':>7}{'D':>7}  zone"
    print(hdr)
    print("-" * len(hdr))
    for r in sorted(rows, key=lambda r: (-r["D"], r["component"])):
        flag = " (isolated)" if r["isolated"] else ""
        print(f"{r['component']:<28}{r['abstract']:>5}{r['concrete']:>5}{r['ca']:>5}{r['ce']:>5}"
              f"{r['A']:>7.3f}{r['I']:>7.3f}{r['D']:>7.3f}  {r['zone']}{flag}")
    print()
    print("Most widely used (highest Ca, decide ownership before splitting):")
    for r in shared:
        print(f"  {r['component']}: Ca={r['ca']}")
    if unknown:
        print(f"\nIgnored edges referencing unknown components: {', '.join(unknown)}")
    print()
    s = summary
    print(f"components={s['components']} mean_D={s['mean_D']:.3f} "
          f"balanced={s['zone_counts']['balanced']} pain={s['zone_counts']['pain']} "
          f"uselessness={s['zone_counts']['uselessness']}")
    print(f"hint: {s['hint']}")


if __name__ == "__main__":
    main()
