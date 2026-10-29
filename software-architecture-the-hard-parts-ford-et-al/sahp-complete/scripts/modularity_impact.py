#!/usr/bin/env python3
"""Modularity impact check for a component or service dependency graph.

Computes the signals Chapter 3 of "Software Architecture: The Hard Parts"
ties to architectural modularity: a simplified maintainability level, how far
a change spreads (test and deployment scope), which units must ship together,
and how far a failure spreads through synchronous calls.

Input
  A plain-text edge file. One entry per line; blank lines and text after '#'
  are ignored.
      A -> B sync      A calls or depends on B synchronously
      A -> B async     A talks to B through a queue, event or other async channel
      A -> B           same as sync (the conservative default)
      C                a unit with no edges (still counts toward k)

Outputs (stdout; text by default, JSON with --json)
  ML      Simplified maintainability level in percent (0..100, higher is better):
              ML = 100 * (1/k) * sum_i (1 - c_i / k)
          k = number of units, c_i = number of other units that depend on unit i
          (transitively by default, direct only with --direct). This is the
          initial form of Alexander von Zitzewitz's metric; his full version
          also condenses cycles and weights by level, so treat this as a trend
          indicator, not an absolute score.
  per unit
      dependents   c_i used above
      change_scope units to retest and possibly redeploy when this unit changes
                   (itself plus everything that depends on it, any channel)
      fail_radius  units that become unavailable when this unit fails, following
                   only synchronous edges (async edges stop the spread)
  lockstep groups  strongly connected components of size > 1: units that depend
                   on each other in a loop and therefore cannot be deployed
                   independently (a "distributed big ball of mud" warning sign)

Deterministic, standard library only, no network access.
"""
import argparse
import json
import sys


def parse(path):
    nodes, edges = set(), []
    with open(path, encoding="utf-8") as fh:
        for lineno, raw in enumerate(fh, 1):
            line = raw.split("#", 1)[0].strip()
            if not line:
                continue
            if "->" not in line:
                nodes.add(line)
                continue
            left, right = (p.strip() for p in line.split("->", 1))
            parts = right.split()
            if not left or not parts:
                sys.exit(f"line {lineno}: cannot parse '{raw.rstrip()}'")
            target = parts[0]
            mode = parts[1].lower() if len(parts) > 1 else "sync"
            if mode not in ("sync", "async"):
                sys.exit(f"line {lineno}: mode must be sync or async, got '{mode}'")
            nodes.update((left, target))
            edges.append((left, target, mode))
    return sorted(nodes), edges


def reverse_reach(start, rev):
    """All units that reach `start` through the reversed adjacency `rev`."""
    seen, stack = set(), [start]
    while stack:
        cur = stack.pop()
        for nxt in rev.get(cur, ()):
            if nxt not in seen and nxt != start:
                seen.add(nxt)
                stack.append(nxt)
    return seen


def strongly_connected(nodes, fwd):
    """Tarjan's algorithm, iterative, deterministic order."""
    index, low, on_stack, stack, out, counter = {}, {}, set(), [], [], [0]
    for root in nodes:
        if root in index:
            continue
        work = [(root, iter(sorted(fwd.get(root, ()))))]
        index[root] = low[root] = counter[0]; counter[0] += 1
        stack.append(root); on_stack.add(root)
        while work:
            node, it = work[-1]
            advanced = False
            for nxt in it:
                if nxt not in index:
                    index[nxt] = low[nxt] = counter[0]; counter[0] += 1
                    stack.append(nxt); on_stack.add(nxt)
                    work.append((nxt, iter(sorted(fwd.get(nxt, ())))))
                    advanced = True
                    break
                if nxt in on_stack:
                    low[node] = min(low[node], index[nxt])
            if advanced:
                continue
            work.pop()
            if work:
                low[work[-1][0]] = min(low[work[-1][0]], low[node])
            if low[node] == index[node]:
                comp = []
                while True:
                    w = stack.pop(); on_stack.discard(w); comp.append(w)
                    if w == node:
                        break
                if len(comp) > 1:
                    out.append(sorted(comp))
    return sorted(out)


def analyse(nodes, edges, direct):
    fwd, rev_all, rev_sync = {}, {}, {}
    for a, b, mode in edges:
        if a == b:
            continue
        fwd.setdefault(a, set()).add(b)
        rev_all.setdefault(b, set()).add(a)
        if mode == "sync":
            rev_sync.setdefault(b, set()).add(a)
    k = len(nodes)
    units, total = [], 0.0
    for n in nodes:
        dependents = set(rev_all.get(n, ())) if direct else reverse_reach(n, rev_all)
        c = len(dependents)
        total += 1 - c / k
        units.append({
            "unit": n,
            "dependents": c,
            "change_scope": sorted({n} | reverse_reach(n, rev_all)),
            "fail_radius": sorted({n} | reverse_reach(n, rev_sync)),
        })
    ml = 100.0 * total / k if k else 0.0
    return {
        "k": k,
        "ml_percent": round(ml, 1),
        "coupling_mode": "direct" if direct else "transitive",
        "units": units,
        "lockstep_groups": strongly_connected(nodes, fwd),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("edges", help="edge file (see module docstring for format)")
    ap.add_argument("--direct", action="store_true",
                    help="count only direct incoming dependents for ML")
    ap.add_argument("--json", action="store_true", help="emit JSON")
    args = ap.parse_args()
    nodes, edges = parse(args.edges)
    if not nodes:
        sys.exit("no units found")
    res = analyse(nodes, edges, args.direct)
    if args.json:
        print(json.dumps(res, indent=2))
        return
    print(f"units k={res['k']}  ML={res['ml_percent']}% ({res['coupling_mode']} incoming coupling)")
    print("unit | dependents | change scope | fail radius (sync only)")
    for u in res["units"]:
        print(f"{u['unit']} | {u['dependents']} | {', '.join(u['change_scope'])} | "
              f"{', '.join(u['fail_radius'])}")
    if res["lockstep_groups"]:
        print("lockstep groups (cannot deploy independently):")
        for g in res["lockstep_groups"]:
            print("  " + ", ".join(g))
    else:
        print("lockstep groups: none")


if __name__ == "__main__":
    main()
