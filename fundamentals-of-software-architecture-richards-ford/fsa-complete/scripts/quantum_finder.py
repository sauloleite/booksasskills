#!/usr/bin/env python3
"""Find architecture quanta in a system description.

Input: a JSON file (or '-' for stdin) shaped like:
{
  "services": [
    {"name": "auction",
     "datastores": ["auction_db"],          # optional; shared names merge services
     "shared_components": ["address_lib"],  # optional; shared libs/schemas merge too
     "characteristics": {"scalability": "high", "availability": "99.9"}}  # optional
  ],
  "calls": [
    {"from": "auction", "to": "payment", "mode": "sync"}   # mode: sync | async
  ]
}

Output (text, or JSON with --json):
  * static quanta: groups joined by shared datastores or shared components
  * runtime quanta: static quanta further joined by synchronous calls
  * fusing sync edges: sync calls that join two otherwise separate static quanta
  * characteristic conflicts: inside each runtime quantum, characteristics whose
    declared values differ between members (a scope mismatch to justify or fix)
  * warnings: calls naming unknown services

Exit code 0 on success, 2 on invalid input. Deterministic, stdlib only.
"""
import argparse
import json
import sys


class DisjointSet:
    def __init__(self, items):
        self.parent = {i: i for i in items}

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            lo, hi = sorted((ra, rb))
            self.parent[hi] = lo

    def groups(self):
        out = {}
        for item in sorted(self.parent):
            out.setdefault(self.find(item), []).append(item)
        return sorted(out.values(), key=lambda g: (g[0], len(g)))


def load(path):
    text = sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()
    data = json.loads(text)
    services = data.get("services")
    if not isinstance(services, list) or not services:
        raise ValueError("'services' must be a non-empty list")
    names = [s.get("name") for s in services]
    if any(not isinstance(n, str) or not n for n in names):
        raise ValueError("every service needs a non-empty string 'name'")
    if len(set(names)) != len(names):
        raise ValueError("service names must be unique")
    for c in data.get("calls", []):
        if c.get("mode", "sync") not in ("sync", "async"):
            raise ValueError("call mode must be 'sync' or 'async': %r" % c)
    return services, data.get("calls", [])


def analyze(services, calls):
    by_name = {s["name"]: s for s in services}
    static = DisjointSet(by_name)
    owners = {}
    for s in services:
        for key, kind in (("datastores", "datastore"), ("shared_components", "component")):
            for res in s.get(key, []):
                owners.setdefault((kind, res), []).append(s["name"])
    shared = {}
    for (kind, res), members in sorted(owners.items()):
        for other in members[1:]:
            static.union(members[0], other)
        if len(members) > 1:
            shared["%s:%s" % (kind, res)] = sorted(members)

    warnings, fusing = [], []
    runtime = DisjointSet(by_name)
    for a in by_name:
        runtime.union(a, static.find(a))
    for c in calls:
        src, dst, mode = c.get("from"), c.get("to"), c.get("mode", "sync")
        if src not in by_name or dst not in by_name:
            warnings.append("call %s -> %s names an unknown service" % (src, dst))
            continue
        if mode == "sync":
            if static.find(src) != static.find(dst):
                fusing.append({"from": src, "to": dst})
            runtime.union(src, dst)

    def conflicts(group):
        found = {}
        keys = sorted({k for m in group for k in by_name[m].get("characteristics", {})})
        for k in keys:
            vals = {m: by_name[m]["characteristics"][k] for m in group
                    if k in by_name[m].get("characteristics", {})}
            if len(set(map(str, vals.values()))) > 1:
                found[k] = vals
        return found

    runtime_q = []
    for g in runtime.groups():
        runtime_q.append({"members": g, "conflicts": conflicts(g)})
    return {
        "static_quanta": static.groups(),
        "shared_coupling_points": shared,
        "runtime_quanta": runtime_q,
        "fusing_sync_edges": sorted(fusing, key=lambda e: (e["from"], e["to"])),
        "warnings": warnings,
    }


def render(r):
    lines = ["Static quanta (shared datastores/components): %d" % len(r["static_quanta"])]
    lines += ["  S%d: %s" % (i + 1, ", ".join(g)) for i, g in enumerate(r["static_quanta"])]
    if r["shared_coupling_points"]:
        lines.append("Shared coupling points:")
        lines += ["  %s used by %s" % (k, ", ".join(v)) for k, v in r["shared_coupling_points"].items()]
    lines.append("Runtime quanta (static + synchronous calls): %d" % len(r["runtime_quanta"]))
    for i, q in enumerate(r["runtime_quanta"]):
        lines.append("  R%d: %s" % (i + 1, ", ".join(q["members"])))
        for k, vals in q["conflicts"].items():
            detail = ", ".join("%s=%s" % (m, v) for m, v in vals.items())
            lines.append("      CONFLICT %s: %s" % (k, detail))
    if r["fusing_sync_edges"]:
        lines.append("Sync edges fusing separate static quanta (consider async or aligned targets):")
        lines += ["  %s -> %s" % (e["from"], e["to"]) for e in r["fusing_sync_edges"]]
    lines += ["WARNING: " + w for w in r["warnings"]]
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("input", help="path to JSON file, or '-' for stdin")
    p.add_argument("--json", action="store_true", help="emit JSON instead of text")
    args = p.parse_args()
    try:
        services, calls = load(args.input)
    except (OSError, ValueError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 2
    result = analyze(services, calls)
    print(json.dumps(result, indent=2, sort_keys=True) if args.json else render(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
