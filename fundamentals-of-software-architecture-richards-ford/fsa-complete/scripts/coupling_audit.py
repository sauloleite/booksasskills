#!/usr/bin/env python3
"""Coupling audit for a microservices call map (governance fitness function).

Implements the static and dynamic coupling checks suggested in Chapter 18 of
Richards and Ford's "Fundamentals of Software Architecture": build a map of
interservice calls (from logs or a service registry), then measure it.

INPUT: a JSON file shaped like
  {
    "services": {
      "orders":  {"calls": ["inventory", "payment"],
                  "database": "orders_db",
                  "libraries": ["acme-logging", "acme-domain-model"]},
      "payment": {"calls": [], "database": "payment_db", "libraries": []}
    },
    "operational_libraries": ["acme-logging"]
  }
  "calls", "database" and "libraries" are optional per service.
  "operational_libraries" (optional) lists shared libs that are acceptable
  operational reuse (logging, metrics); all other shared libs are flagged.

OUTPUT: a text report (or JSON with --json) listing per-service fan-out and
fan-in, mutual call pairs, call cycles, calls to unknown services, databases
and how many services share each, and custom libraries shared across services.
Exit code 0 if no FAIL findings, 1 otherwise, 2 on bad input.

Thresholds: --max-db-sharers defaults to 6 (the chapter's "five or six"
guideline). --max-fan-out has no value in the book; the default of 5 is a
placeholder the team should set deliberately.
"""
import argparse
import json
import sys
from collections import defaultdict


def find_cycles(graph):
    """Tarjan's SCC; returns sorted lists of services in cycles of size > 1."""
    index, low, stack, on_stack, out = {}, {}, [], set(), []
    counter = [0]

    def visit(v):
        index[v] = low[v] = counter[0]
        counter[0] += 1
        stack.append(v)
        on_stack.add(v)
        for w in sorted(graph.get(v, ())):
            if w not in index:
                visit(w)
                low[v] = min(low[v], low[w])
            elif w in on_stack:
                low[v] = min(low[v], index[w])
        if low[v] == index[v]:
            comp = []
            while True:
                w = stack.pop()
                on_stack.discard(w)
                comp.append(w)
                if w == v:
                    break
            if len(comp) > 1:
                out.append(sorted(comp))

    for v in sorted(graph):
        if v not in index:
            visit(v)
    return sorted(out)


def audit(data, max_fan_out, max_db_sharers, strict_libs):
    services = data.get("services")
    if not isinstance(services, dict) or not services:
        raise ValueError('input needs a non-empty "services" object')
    allowed = set(data.get("operational_libraries", []))
    graph = {s: set(c.get("calls", [])) - {s} for s, c in services.items()}
    fan_in = defaultdict(set)
    unknown = []
    for s, targets in graph.items():
        for t in targets:
            fan_in[t].add(s)
            if t not in services:
                unknown.append((s, t))
    findings = []
    per_service = {}
    for s in sorted(services):
        fo, fi = len(graph[s]), len(fan_in[s])
        per_service[s] = {"fan_out": fo, "fan_in": fi}
        if fo > max_fan_out:
            findings.append(("FAIL", f"{s} calls {fo} services (limit {max_fan_out})"))
    mutual = sorted({tuple(sorted((a, b))) for a in graph for b in graph[a]
                     if b in graph and a in graph[b]})
    for a, b in mutual:
        findings.append(("WARN", f"mutual calls {a} <-> {b}: consider merging"))
    cycles = find_cycles(graph)
    for c in cycles:
        if len(c) > 2:
            findings.append(("FAIL", "call cycle among " + ", ".join(c)))
    for s, t in sorted(unknown):
        findings.append(("WARN", f"{s} calls undeclared service {t}"))
    dbs = defaultdict(list)
    libs = defaultdict(list)
    for s, c in services.items():
        if c.get("database"):
            dbs[c["database"]].append(s)
        for lib in c.get("libraries", []):
            libs[lib].append(s)
    db_report = {d: sorted(v) for d, v in sorted(dbs.items())}
    for d, users in db_report.items():
        n = len(users)
        if n > max_db_sharers:
            findings.append(("FAIL", f"database {d} shared by {n} services (limit {max_db_sharers})"))
        elif n > 1:
            findings.append(("INFO", f"database {d} shared by {n}: document as one broader bounded context"))
    shared_libs = {l: sorted(v) for l, v in sorted(libs.items()) if len(v) > 1 and l not in allowed}
    for l, users in shared_libs.items():
        level = "FAIL" if strict_libs else "WARN"
        findings.append((level, f"library {l} shared by {len(users)} services: {', '.join(users)}"))
    return {"services": per_service, "mutual_pairs": mutual, "cycles": cycles,
            "databases": db_report, "shared_libraries": shared_libs,
            "findings": [{"level": l, "message": m} for l, m in findings]}


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("input", help="path to the service call-map JSON file")
    p.add_argument("--max-fan-out", type=int, default=5,
                   help="max outgoing service dependencies per service (team-chosen; default 5)")
    p.add_argument("--max-db-sharers", type=int, default=6,
                   help="max services sharing one database or schema (default 6)")
    p.add_argument("--strict-libs", action="store_true",
                   help="treat shared non-operational libraries as FAIL instead of WARN")
    p.add_argument("--json", action="store_true", help="emit JSON instead of text")
    a = p.parse_args()
    try:
        with open(a.input) as fh:
            result = audit(json.load(fh), a.max_fan_out, a.max_db_sharers, a.strict_libs)
    except (OSError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    if a.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("service              fan_out  fan_in")
        for s, m in result["services"].items():
            print(f"{s:<20} {m['fan_out']:>7} {m['fan_in']:>7}")
        print("\nfindings:")
        for f in result["findings"] or [{"level": "OK", "message": "none"}]:
            print(f"  [{f['level']}] {f['message']}")
    return 1 if any(f["level"] == "FAIL" for f in result["findings"]) else 0


if __name__ == "__main__":
    sys.exit(main())
