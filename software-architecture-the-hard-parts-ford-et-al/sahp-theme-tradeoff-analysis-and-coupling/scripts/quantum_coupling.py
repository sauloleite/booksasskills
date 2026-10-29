#!/usr/bin/env python3
"""Architecture quantum and coupling analyzer (static + dynamic).

Input: a JSON file describing services, their bootstrap dependencies and the
runtime calls between them:

{
  "dependencies": {
    "orders-db":  {"kind": "database"},
    "event-bus":  {"kind": "broker"},
    "web-shell":  {"kind": "ui"},
    "commons-lib": {"kind": "library", "fuses": true}
  },
  "services": {
    "checkout": {"uses": ["orders-db", "event-bus"],
                 "requires_services": [],
                 "deploy_unit": "checkout",
                 "characteristics": {"elasticity": 10, "availability": "high"}},
    "fraud":    {"uses": ["fraud-db"], "characteristics": {"elasticity": 1}}
  },
  "calls": [
    {"from": "checkout", "to": "fraud", "communication": "sync",
     "consistency": "eventual", "coordination": "orchestrated",
     "workflow": "place-order"}
  ]
}

Rules applied:
- Static coupling: services sharing a fusing dependency, sharing a
  deploy_unit, or listing another service in requires_services (needed to
  bootstrap) fall into the same static quantum. Kinds that fuse by default:
  database, datastore, mediator, orchestrator, ui. Other kinds (broker,
  library, platform, runtime, micro-frontend, other) do not fuse unless
  "fuses": true; shared non-fusing dependencies are listed for review.
- Dynamic coupling: each call is placed on communication (sync/async),
  consistency (atomic/eventual) and coordination (orchestrated/choreographed),
  labeled with the corresponding pattern name, and given a tightening count
  (number of choices among sync, atomic, orchestrated; 0 = loosest, 3 = tightest).
- Runtime quanta: static quanta joined by synchronous calls.
- Warnings: async + atomic, atomic + choreographed, atomic calls that cross
  static quanta, sync calls between quanta with different characteristic
  values, undeclared dependencies or services.

Output: a text report on stdout (or JSON with --json). Exit code 0 on success,
2 on invalid input. Deterministic; standard library only; no network.
"""
import argparse
import json
import sys

FUSING_KINDS = {"database", "datastore", "mediator", "orchestrator", "ui"}

COMM = {"sync": "sync", "synchronous": "sync", "async": "async", "asynchronous": "async"}
CONS = {"atomic": "atomic", "eventual": "eventual"}
COORD = {"orchestrated": "orchestrated", "orchestration": "orchestrated",
         "centralized": "orchestrated", "mediated": "orchestrated",
         "choreographed": "choreographed", "choreography": "choreographed",
         "distributed": "choreographed"}

PATTERNS = {
    ("sync", "atomic", "orchestrated"): "Epic Saga",
    ("sync", "atomic", "choreographed"): "Phone Tag Saga",
    ("sync", "eventual", "orchestrated"): "Fairy Tale Saga",
    ("sync", "eventual", "choreographed"): "Time Travel Saga",
    ("async", "atomic", "orchestrated"): "Fantasy Fiction Story",
    ("async", "atomic", "choreographed"): "Horror Story",
    ("async", "eventual", "orchestrated"): "Parallel Saga",
    ("async", "eventual", "choreographed"): "Anthology Saga",
}


class DSU:
    def __init__(self, items):
        self.p = {i: i for i in items}

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            if rb < ra:
                ra, rb = rb, ra
            self.p[rb] = ra
            return True
        return False

    def groups(self):
        g = {}
        for x in sorted(self.p):
            g.setdefault(self.find(x), []).append(x)
        return sorted(g.values(), key=lambda m: m[0])


def norm(value, table):
    if value is None:
        return "unspecified"
    return table.get(str(value).strip().lower(), "invalid:" + str(value))


def analyze(model):
    deps = model.get("dependencies", {}) or {}
    services = model.get("services", {}) or {}
    calls = model.get("calls", []) or []
    if not isinstance(services, dict) or not services:
        raise ValueError("'services' must be a non-empty object")
    warnings = []
    names = sorted(services)
    static = DSU(names)
    reasons = []

    users = {}
    for s in names:
        for d in services[s].get("uses", []) or []:
            users.setdefault(d, []).append(s)
    shared_nonfusing = []
    for d in sorted(users):
        meta = deps.get(d)
        if meta is None:
            warnings.append(f"dependency '{d}' is not declared; treated as non-fusing kind 'other'")
            meta = {"kind": "other"}
        kind = str(meta.get("kind", "other")).lower()
        fuses = meta.get("fuses", kind in FUSING_KINDS)
        us = sorted(set(users[d]))
        if len(us) < 2:
            continue
        if fuses:
            for other in us[1:]:
                static.union(us[0], other)
            reasons.append(f"shared {kind} '{d}' fuses: {', '.join(us)}")
        else:
            shared_nonfusing.append({"dependency": d, "kind": kind, "services": us})

    units = {}
    for s in names:
        u = services[s].get("deploy_unit")
        if u:
            units.setdefault(u, []).append(s)
    for u in sorted(units):
        if len(units[u]) > 1:
            for other in units[u][1:]:
                static.union(units[u][0], other)
            reasons.append(f"shared deploy unit '{u}' fuses: {', '.join(units[u])}")

    for s in names:
        for r in services[s].get("requires_services", []) or []:
            if r not in services:
                warnings.append(f"service '{s}' requires unknown service '{r}'")
                continue
            static.union(s, r)
            reasons.append(f"'{s}' needs '{r}' to bootstrap")

    static_groups = static.groups()
    qid = {}
    for i, g in enumerate(static_groups, 1):
        for s in g:
            qid[s] = f"Q{i}"

    runtime = DSU([f"Q{i}" for i in range(1, len(static_groups) + 1)])
    call_rows, fusing_calls = [], []
    for idx, c in enumerate(calls, 1):
        src, dst = c.get("from"), c.get("to")
        if src not in services or dst not in services:
            warnings.append(f"call #{idx} references unknown service ({src} -> {dst}); skipped")
            continue
        comm = norm(c.get("communication"), COMM)
        cons = norm(c.get("consistency"), CONS)
        coord = norm(c.get("coordination"), COORD)
        for label, v in (("communication", comm), ("consistency", cons), ("coordination", coord)):
            if v.startswith("invalid:"):
                warnings.append(f"call #{idx} {src}->{dst}: invalid {label} '{v[8:]}'")
        pattern = PATTERNS.get((comm, cons, coord), "n/a (incomplete coordinates)")
        tight = sum([comm == "sync", cons == "atomic", coord == "orchestrated"])
        cross = qid[src] != qid[dst]
        notes = []
        if comm == "async" and cons == "atomic":
            notes.append("atomic consistency over async communication is fragile")
        if cons == "atomic" and coord == "choreographed":
            notes.append("atomic without an orchestrator: no single place tracks transaction state")
        if cons == "atomic" and cross:
            notes.append("distributed transaction across static quanta")
        if comm == "sync" and cross:
            if runtime.union(qid[src], qid[dst]):
                fusing_calls.append(f"{src} -> {dst} joins {qid[src]} and {qid[dst]}")
            ca = services[src].get("characteristics", {}) or {}
            cb = services[dst].get("characteristics", {}) or {}
            for k in sorted(set(ca) & set(cb)):
                if ca[k] != cb[k]:
                    notes.append(f"sync call across differing '{k}' ({ca[k]} vs {cb[k]}): caller inherits callee limits")
        call_rows.append({"call": idx, "from": src, "to": dst, "workflow": c.get("workflow", ""),
                          "communication": comm, "consistency": cons, "coordination": coord,
                          "pattern": pattern, "tightening": tight, "crosses_static_quanta": cross,
                          "notes": notes})

    runtime_groups = []
    for g in runtime.groups():
        members = sorted(s for s in names if qid[s] in g)
        runtime_groups.append({"static_quanta": g, "services": members})

    return {
        "static_quanta": [{"id": f"Q{i}", "services": g} for i, g in enumerate(static_groups, 1)],
        "static_fusion_reasons": reasons,
        "shared_non_fusing_dependencies": shared_nonfusing,
        "calls": call_rows,
        "runtime_quanta": runtime_groups,
        "sync_calls_fusing_quanta": fusing_calls,
        "warnings": warnings,
    }


def render(r):
    out = [f"STATIC QUANTA: {len(r['static_quanta'])}"]
    for q in r["static_quanta"]:
        out.append(f"  {q['id']}: {', '.join(q['services'])}")
    if r["static_fusion_reasons"]:
        out.append("Static fusion reasons:")
        out += [f"  - {x}" for x in r["static_fusion_reasons"]]
    if r["shared_non_fusing_dependencies"]:
        out.append("Shared but non-fusing (confirm each can change/deploy independently):")
        for d in r["shared_non_fusing_dependencies"]:
            out.append(f"  - {d['kind']} '{d['dependency']}': {', '.join(d['services'])}")
    out.append("")
    out.append("DYNAMIC COUPLING PER CALL (tightening 0=loosest .. 3=tightest):")
    for c in r["calls"]:
        wf = f" [{c['workflow']}]" if c["workflow"] else ""
        x = "cross-quantum" if c["crosses_static_quanta"] else "intra-quantum"
        out.append(f"  #{c['call']} {c['from']} -> {c['to']}{wf}: {c['communication']}/"
                   f"{c['consistency']}/{c['coordination']} = {c['pattern']}; "
                   f"tightening {c['tightening']}; {x}")
        out += [f"      ! {n}" for n in c["notes"]]
    out.append("")
    out.append(f"RUNTIME QUANTA (static quanta joined by sync calls): {len(r['runtime_quanta'])}")
    for g in r["runtime_quanta"]:
        out.append(f"  {'+'.join(g['static_quanta'])}: {', '.join(g['services'])}")
    if r["sync_calls_fusing_quanta"]:
        out.append("Sync calls that fuse separate static quanta:")
        out += [f"  - {x}" for x in r["sync_calls_fusing_quanta"]]
    if r["warnings"]:
        out.append("")
        out.append("WARNINGS:")
        out += [f"  - {w}" for w in r["warnings"]]
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(
        description="Compute static architecture quanta, per-call dynamic coupling "
                    "(communication, consistency, coordination) and runtime quanta fused by sync calls.",
        epilog="See the module docstring (python3 -c 'import quantum_coupling; help(quantum_coupling)') "
               "or the top of this file for the JSON schema.")
    ap.add_argument("model", help="path to the system JSON file")
    ap.add_argument("--json", action="store_true", help="emit machine-readable JSON instead of text")
    a = ap.parse_args()
    try:
        with open(a.model) as fh:
            model = json.load(fh)
        result = analyze(model)
    except (OSError, ValueError, AttributeError, TypeError) as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(2)
    print(json.dumps(result, indent=2, sort_keys=True) if a.json else render(result))


if __name__ == "__main__":
    main()
