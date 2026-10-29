#!/usr/bin/env python3
"""Validate the structure of an agent orchestration graph before building it.

Input: a JSON file such as
  {"start": "START", "end": "END",
   "edges": [["START", "classify"], ["classify", "billing"],
             ["classify", "tech"], ["billing", "reply"],
             ["tech", "reply"], ["reply", "END"]]}

"start" and "end" default to "START" and "END". Edges are directed
[from, to] pairs; conditional and consolidation edges are listed the same way.

Checks and output:
  - nodes unreachable from start
  - nodes that cannot reach end (dead ends or closed loops)
  - cycles (reported as one example node sequence per strongly connected group)
  - max branching factor (out-degree) and the node holding it
  - longest start-to-end path length in edges and number of distinct
    start-to-end paths (only when the reachable graph is acyclic)
Exit code 1 if any structural problem is found or a cap given with
--max-depth / --max-branching is exceeded; 0 otherwise.

Deterministic, standard library only, no network access.
"""
import argparse
import json
import sys
from collections import defaultdict


def load(path):
    with open(path, encoding="utf-8") as fh:
        g = json.load(fh)
    start, end = g.get("start", "START"), g.get("end", "END")
    succ, pred = defaultdict(list), defaultdict(list)
    nodes = {start, end}
    for e in g.get("edges", []):
        if not (isinstance(e, list) and len(e) == 2):
            sys.exit(f"bad edge {e!r}: expected [from, to]")
        a, b = e
        if b not in succ[a]:
            succ[a].append(b)
            pred[b].append(a)
        nodes.update((a, b))
    return start, end, sorted(nodes), succ, pred


def reach(origin, adj):
    seen, stack = {origin}, [origin]
    while stack:
        for nxt in adj[stack.pop()]:
            if nxt not in seen:
                seen.add(nxt)
                stack.append(nxt)
    return seen


def cycles(nodes, succ):
    """Tarjan SCC; returns SCCs with >1 node or a self-loop."""
    index, low, on, stack, out, counter = {}, {}, set(), [], [], [0]

    def visit(v):
        index[v] = low[v] = counter[0]
        counter[0] += 1
        stack.append(v)
        on.add(v)
        for w in succ[v]:
            if w not in index:
                visit(w)
                low[v] = min(low[v], low[w])
            elif w in on:
                low[v] = min(low[v], index[w])
        if low[v] == index[v]:
            comp = []
            while True:
                w = stack.pop()
                on.discard(w)
                comp.append(w)
                if w == v:
                    break
            if len(comp) > 1 or v in succ[v]:
                out.append(sorted(comp))

    sys.setrecursionlimit(max(1000, 4 * len(nodes)))
    for v in nodes:
        if v not in index:
            visit(v)
    return sorted(out)


def paths_and_depth(start, end, succ, allowed):
    memo = {}

    def go(v):  # returns (path_count, longest_len) to end, or (0, None)
        if v == end:
            return 1, 0
        if v in memo:
            return memo[v]
        count, longest = 0, None
        for w in succ[v]:
            if w not in allowed:
                continue
            c, d = go(w)
            if c:
                count += c
                longest = d + 1 if longest is None else max(longest, d + 1)
        memo[v] = (count, longest)
        return memo[v]

    return go(start)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("graph", help="path to JSON graph file")
    ap.add_argument("--max-depth", type=int, help="fail if longest start-to-end path exceeds this many edges")
    ap.add_argument("--max-branching", type=int, help="fail if any node has more successors than this")
    ap.add_argument("--json", action="store_true", help="print machine-readable JSON")
    args = ap.parse_args()

    start, end, nodes, succ, pred = load(args.graph)
    fwd, back = reach(start, succ), reach(end, pred)
    unreachable = [n for n in nodes if n not in fwd]
    no_exit = [n for n in nodes if n in fwd and n not in back]
    cyc = cycles(nodes, succ)
    branch_node = max(nodes, key=lambda n: (len(succ[n]), n == start, n)) if nodes else None
    branching = len(succ[branch_node]) if branch_node else 0
    reachable_cyclic = any(set(c) & fwd for c in cyc)
    if not reachable_cyclic and start in back:
        n_paths, depth = paths_and_depth(start, end, succ, fwd)
    else:
        n_paths, depth = None, None

    problems = []
    if unreachable:
        problems.append(f"unreachable from {start}: {unreachable}")
    if no_exit:
        problems.append(f"cannot reach {end}: {no_exit}")
    if cyc:
        problems.append(f"cycles: {cyc}")
    if args.max_branching is not None and branching > args.max_branching:
        problems.append(f"branching {branching} at '{branch_node}' exceeds cap {args.max_branching}")
    if args.max_depth is not None and depth is not None and depth > args.max_depth:
        problems.append(f"longest path {depth} exceeds depth cap {args.max_depth}")

    result = {
        "nodes": len(nodes), "edges": sum(len(v) for v in succ.values()),
        "unreachable": unreachable, "cannot_reach_end": no_exit, "cycles": cyc,
        "max_branching": branching, "max_branching_node": branch_node,
        "longest_path_edges": depth, "start_to_end_paths": n_paths,
        "problems": problems, "ok": not problems,
    }
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"nodes={result['nodes']} edges={result['edges']}")
        print(f"max branching factor: {branching} (at '{branch_node}')")
        print(f"longest start-to-end path (edges): {depth if depth is not None else 'n/a (cyclic or no path)'}")
        print(f"distinct start-to-end paths: {n_paths if n_paths is not None else 'n/a'}")
        print("problems:" if problems else "OK: no structural problems found")
        for p in problems:
            print(f"  - {p}")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
