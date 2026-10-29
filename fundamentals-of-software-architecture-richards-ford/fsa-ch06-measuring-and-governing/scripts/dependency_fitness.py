#!/usr/bin/env python3
"""Structural fitness function: dependency cycles, layer rules, main-sequence distance.

Inputs
  EDGES (positional): text file, one dependency per line, "source -> target".
      Blank lines and lines starting with '#' are ignored.
  --rules FILE (optional): layer rules in INI-like form:
        [layers]
        controller = app.web.*        # fnmatch globs, comma separated
        service    = app.service.*
        [allow]
        controller -> service         # same-layer edges are always allowed
        service -> persistence
      Any edge between two different layers that is not listed under [allow]
      is a violation. Modules matching no layer are reported as unassigned.
  --abstractness FILE (optional): lines "module abstract_types total_types".
      Enables the distance-from-the-main-sequence check, D = |A + I - 1|,
      with I = Ce / (Ca + Ce) computed from EDGES (module-level fan-in/out).
  --tolerance X: maximum allowed D (default 0.5).
  --allow-cycles: report cycles without failing.
  --json: machine-readable output.

Output
  Human-readable report (or JSON) on stdout.
  Exit code 0 when clean, 1 when any violation is found, 2 on input errors.
Deterministic, standard library only, no network.
"""
import argparse
import fnmatch
import json
import sys
from collections import defaultdict


def read_edges(path):
    edges = []
    with open(path) as fh:
        for n, line in enumerate(fh, 1):
            line = line.split("#", 1)[0].strip()
            if not line:
                continue
            if "->" not in line:
                sys.exit(f"error: {path}:{n}: expected 'source -> target'")
            a, b = (p.strip() for p in line.split("->", 1))
            if not a or not b:
                sys.exit(f"error: {path}:{n}: empty module name")
            edges.append((a, b))
    return sorted(set(edges))


def read_rules(path):
    layers, allow, section = {}, set(), None
    with open(path) as fh:
        for n, line in enumerate(fh, 1):
            line = line.split("#", 1)[0].strip()
            if not line:
                continue
            if line.startswith("[") and line.endswith("]"):
                section = line[1:-1].strip().lower()
            elif section == "layers" and "=" in line:
                name, globs = (p.strip() for p in line.split("=", 1))
                layers[name] = [g.strip() for g in globs.split(",") if g.strip()]
            elif section == "allow" and "->" in line:
                a, b = (p.strip() for p in line.split("->", 1))
                allow.add((a, b))
            else:
                sys.exit(f"error: {path}:{n}: cannot parse '{line}'")
    for a, b in allow:
        if a not in layers or b not in layers:
            sys.exit(f"error: allow rule {a} -> {b} names an undefined layer")
    return layers, allow


def layer_of(module, layers):
    for name in layers:  # first matching layer wins, in file order
        if any(fnmatch.fnmatchcase(module, g) for g in layers[name]):
            return name
    return None


def find_cycles(nodes, adj):
    """Tarjan SCC (iterative). Returns sorted list of cyclic components."""
    index, low, on_stack, stack, comps, counter = {}, {}, set(), [], [], [0]
    for root in nodes:
        if root in index:
            continue
        work = [(root, iter(adj[root]))]
        index[root] = low[root] = counter[0]; counter[0] += 1
        stack.append(root); on_stack.add(root)
        while work:
            v, it = work[-1]
            pushed = False
            for w in it:
                if w not in index:
                    index[w] = low[w] = counter[0]; counter[0] += 1
                    stack.append(w); on_stack.add(w)
                    work.append((w, iter(adj[w])))
                    pushed = True
                    break
                if w in on_stack:
                    low[v] = min(low[v], index[w])
            if pushed:
                continue
            work.pop()
            if work:
                low[work[-1][0]] = min(low[work[-1][0]], low[v])
            if low[v] == index[v]:
                comp = []
                while True:
                    w = stack.pop(); on_stack.discard(w); comp.append(w)
                    if w == v:
                        break
                if len(comp) > 1 or v in adj[v]:
                    comps.append(sorted(comp))
    return sorted(comps)


def example_cycle(comp, adj):
    """Return one concrete cycle path inside a strongly connected component."""
    members, start = set(comp), comp[0]
    prev, queue = {start: None}, [start]
    while queue:
        v = queue.pop(0)
        for w in adj[v]:
            if w == start:
                path = [v]
                while prev[path[-1]] is not None:
                    path.append(prev[path[-1]])
                return list(reversed(path)) + [start]
            if w in members and w not in prev:
                prev[w] = v
                queue.append(w)
    return [start, start]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("edges", help="edge list file: 'source -> target' per line")
    ap.add_argument("--rules", help="layer rules file ([layers] and [allow])")
    ap.add_argument("--abstractness", help="file: 'module abstract total' per line")
    ap.add_argument("--tolerance", type=float, default=0.5,
                    help="max distance from main sequence (default 0.5)")
    ap.add_argument("--allow-cycles", action="store_true",
                    help="report cycles but do not fail on them")
    ap.add_argument("--json", action="store_true", help="emit JSON")
    args = ap.parse_args()

    edges = read_edges(args.edges)
    adj, fan_in = defaultdict(list), defaultdict(set)
    nodes = set()
    for a, b in edges:
        adj[a].append(b); fan_in[b].add(a); nodes.update((a, b))
    for v in adj:
        adj[v].sort()
    nodes = sorted(nodes)

    report = {"modules": len(nodes), "edges": len(edges)}
    failed = False

    cycles = [{"members": c, "example": example_cycle(c, adj)}
              for c in find_cycles(nodes, adj)]
    report["cycles"] = cycles
    if cycles and not args.allow_cycles:
        failed = True

    if args.rules:
        layers, allow = read_rules(args.rules)
        viol, unassigned = [], sorted(m for m in nodes if layer_of(m, layers) is None)
        for a, b in edges:
            la, lb = layer_of(a, layers), layer_of(b, layers)
            if la and lb and la != lb and (la, lb) not in allow:
                viol.append({"edge": f"{a} -> {b}", "layers": f"{la} -> {lb}"})
        report["layer_violations"], report["unassigned"] = viol, unassigned
        failed = failed or bool(viol)

    if args.abstractness:
        rows = []
        with open(args.abstractness) as fh:
            for line in fh:
                parts = line.split("#", 1)[0].split()
                if not parts:
                    continue
                if len(parts) != 3:
                    sys.exit(f"error: bad abstractness line: {line.strip()}")
                m, abstract, total = parts[0], int(parts[1]), int(parts[2])
                if total <= 0 or not 0 <= abstract <= total:
                    sys.exit(f"error: invalid counts for {m}")
                ce, ca = len(set(adj[m])), len(fan_in[m])
                inst = ce / (ca + ce) if ca + ce else 0.0
                a_val = abstract / total
                d = abs(a_val + inst - 1)
                rows.append({"module": m, "A": round(a_val, 3), "I": round(inst, 3),
                             "D": round(d, 3), "fail": d > args.tolerance})
        report["distance"] = sorted(rows, key=lambda r: (-r["D"], r["module"]))
        failed = failed or any(r["fail"] for r in rows)

    report["result"] = "FAIL" if failed else "PASS"
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"modules={report['modules']} edges={report['edges']}")
        print(f"cycles: {len(cycles)}" + (" (not enforced)" if args.allow_cycles else ""))
        for c in cycles:
            print("  " + " -> ".join(c["example"]) + f"   [component of {len(c['members'])}]")
        if args.rules:
            print(f"layer violations: {len(report['layer_violations'])}")
            for v in report["layer_violations"]:
                print(f"  {v['edge']}   ({v['layers']} not allowed)")
            if report["unassigned"]:
                print("unassigned modules (no layer): " + ", ".join(report["unassigned"]))
        if args.abstractness:
            print(f"distance from main sequence (tolerance {args.tolerance}):")
            for r in report["distance"]:
                flag = "FAIL" if r["fail"] else "ok"
                print(f"  {r['module']}: A={r['A']} I={r['I']} D={r['D']} {flag}")
        print(f"result: {report['result']}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
