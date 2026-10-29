#!/usr/bin/env python3
"""Check modular-monolith boundaries: module membership, coupling budget, forbidden pairs.

Inputs
  --modules        comma-separated module prefixes (e.g. shop.cart,shop.billing)
  one source of dependencies (at least one required):
    --edges FILE   text file, one dependency per line: "from.ns -> to.ns" or "from.ns,to.ns"
                   (blank lines and lines starting with # are ignored). Export it from
                   your platform's dependency tool (jdeps, NDepend, madge, etc.).
    --python-root DIR  scan .py files under DIR; namespace = dotted path relative to DIR;
                   edges come from import statements (relative imports resolved).
  --namespaces FILE  optional extra namespaces to check for membership (one per line).
  --max-coupling N   per-module budget for incoming + outgoing cross-module dependencies (default 5).
  --count links|refs links = distinct module-to-module pairs (default);
                     refs  = distinct namespace-to-namespace pairs that cross modules.
  --forbid A:B       module A must not depend on module B (repeatable).
  --exempt M         module excluded from the budget, e.g. a mediator (repeatable).
  --json             emit JSON instead of a text report.

Outputs
  Report listing namespaces outside any module (parent packages of modules are allowed), per-module in/out/total coupling with
  budget breaches, and forbidden dependencies found. Exit code 0 if clean, 1 if any
  violation, 2 on usage error. Deterministic: all lists are sorted.
"""
import argparse
import ast
import json
import os
import sys


def owner(ns, modules):
    """Return the longest module prefix owning namespace ns, or None."""
    best = None
    for m in modules:
        if ns == m or ns.startswith(m + "."):
            if best is None or len(m) > len(best):
                best = m
    return best


def read_edges(path):
    edges = set()
    with open(path, encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            sep = "->" if "->" in line else ","
            parts = [p.strip() for p in line.split(sep)]
            if len(parts) != 2 or not all(parts):
                sys.exit(f"error: {path}:{n}: cannot parse edge '{line}'")
            edges.add((parts[0], parts[1]))
    return edges


def scan_python(root):
    namespaces, edges = set(), set()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for fn in sorted(filenames):
            if not fn.endswith(".py"):
                continue
            rel = os.path.relpath(os.path.join(dirpath, fn), root)[:-3]
            parts = rel.split(os.sep)
            is_pkg = parts[-1] == "__init__"
            if is_pkg:
                parts = parts[:-1]
            if not parts:
                continue
            ns = ".".join(parts)
            namespaces.add(ns)
            pkg = parts if is_pkg else parts[:-1]
            with open(os.path.join(dirpath, fn), encoding="utf-8") as fh:
                tree = ast.parse(fh.read(), filename=fn)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for a in node.names:
                        edges.add((ns, a.name))
                elif isinstance(node, ast.ImportFrom):
                    if node.level:
                        base = pkg[: len(pkg) - (node.level - 1)] if node.level > 1 else pkg
                        target = ".".join(base + ([node.module] if node.module else []))
                    else:
                        target = node.module or ""
                    if target:
                        edges.add((ns, target))
    return namespaces, edges


def analyze(modules, namespaces, edges, budget, mode, forbids, exempt):
    def is_ancestor(ns):
        return any(m.startswith(ns + ".") for m in modules)
    outside = sorted(ns for ns in namespaces
                     if owner(ns, modules) is None and not is_ancestor(ns))
    incoming = {m: set() for m in modules}
    outgoing = {m: set() for m in modules}
    forbidden = set()
    for src, dst in edges:
        ms, md = owner(src, modules), owner(dst, modules)
        if ms is None or md is None or ms == md:
            continue
        key = (ms, md) if mode == "links" else (src, dst)
        outgoing[ms].add(key)
        incoming[md].add(key)
        if (ms, md) in forbids:
            forbidden.add((ms, md, src, dst))
    coupling = []
    for m in sorted(modules):
        i, o = len(incoming[m]), len(outgoing[m])
        coupling.append({"module": m, "in": i, "out": o, "total": i + o,
                         "exempt": m in exempt,
                         "over_budget": m not in exempt and i + o > budget})
    return {
        "outside_modules": outside,
        "coupling": coupling,
        "budget": budget,
        "count_mode": mode,
        "forbidden": [dict(zip(("from_module", "to_module", "from_ns", "to_ns"), f))
                      for f in sorted(forbidden)],
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--modules", required=True)
    ap.add_argument("--edges")
    ap.add_argument("--python-root")
    ap.add_argument("--namespaces")
    ap.add_argument("--max-coupling", type=int, default=5)
    ap.add_argument("--count", choices=["links", "refs"], default="links")
    ap.add_argument("--forbid", action="append", default=[])
    ap.add_argument("--exempt", action="append", default=[])
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    modules = sorted({m.strip() for m in a.modules.split(",") if m.strip()})
    if not modules or not (a.edges or a.python_root):
        ap.error("need --modules and at least one of --edges / --python-root")
    forbids = set()
    for f in a.forbid:
        if f.count(":") != 1:
            ap.error(f"--forbid expects A:B, got '{f}'")
        forbids.add(tuple(x.strip() for x in f.split(":")))

    namespaces, edges = set(), set()
    if a.edges:
        edges |= read_edges(a.edges)
        namespaces |= {s for s, _ in edges}
    if a.python_root:
        n, e = scan_python(a.python_root)
        namespaces |= n
        edges |= e
    if a.namespaces:
        with open(a.namespaces, encoding="utf-8") as fh:
            namespaces |= {l.strip() for l in fh if l.strip() and not l.startswith("#")}

    r = analyze(modules, namespaces, edges, a.max_coupling, a.count, forbids, set(a.exempt))
    bad = bool(r["outside_modules"] or r["forbidden"]
               or any(c["over_budget"] for c in r["coupling"]))
    if a.json:
        print(json.dumps(r, indent=2, sort_keys=True))
    else:
        print(f"Namespaces outside declared modules: {len(r['outside_modules'])}")
        for ns in r["outside_modules"]:
            print(f"  ALERT {ns}")
        print(f"Coupling ({r['count_mode']}, budget {r['budget']}):")
        for c in r["coupling"]:
            flag = "EXEMPT" if c["exempt"] else ("ALERT" if c["over_budget"] else "ok")
            print(f"  {flag:6} {c['module']}: in={c['in']} out={c['out']} total={c['total']}")
        print(f"Forbidden dependencies: {len(r['forbidden'])}")
        for f in r["forbidden"]:
            print(f"  ALERT {f['from_module']} -> {f['to_module']} ({f['from_ns']} -> {f['to_ns']})")
        print("RESULT:", "VIOLATIONS" if bad else "CLEAN")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
