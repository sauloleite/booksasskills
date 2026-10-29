#!/usr/bin/env python3
"""Report cross-domain database dependencies that must be broken before a split.

Inputs
  domains file (required): one assignment per line, "object, domain".
      Objects are tables, and optionally views/procedures/triggers/functions
      (to state which domain an artifact lives in). '#' starts a comment.
  dependencies file (required): one artifact per line,
      "kind, name, object1 object2 ..." where kind is fk, view, trigger,
      proc, function or synonym and the objects are the tables it touches.
      For an fk list child then parent table.
  access file (optional, --access): "service, table, r|w|rw" per line,
      the service-to-table access matrix used to check that every service
      reads and writes a single data domain.

Outputs (text, or JSON with --json)
  - unassigned tables referenced by dependencies or access lines
  - every cross-domain artifact with the domains and foreign tables involved
  - coupling count per domain pair, flagging pairs at or above
    --merge-threshold as candidates to merge into one broader domain
  - services that touch more than one domain, and domains written by
    services whose home domain (most-written domain) differs
Exit code: 0 if no cross-domain artifacts or service violations, 1 otherwise
(2 on input errors). Deterministic; standard library only.
"""
import argparse
import json
import sys
from collections import Counter, defaultdict

KINDS = {"fk", "view", "trigger", "proc", "function", "synonym"}


def rows(path):
    with open(path, encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            line = line.split("#", 1)[0].strip()
            if line:
                yield n, [p.strip() for p in line.split(",")]


def load_domains(path):
    mapping = {}
    for n, parts in rows(path):
        if len(parts) != 2 or not all(parts):
            raise ValueError(f"{path}:{n}: expected 'object, domain'")
        mapping[parts[0].lower()] = parts[1]
    return mapping


def load_deps(path):
    deps = []
    for n, parts in rows(path):
        if len(parts) != 3 or parts[0].lower() not in KINDS:
            raise ValueError(f"{path}:{n}: expected 'kind, name, tables...' with kind in {sorted(KINDS)}")
        tables = [t.lower() for t in parts[2].split()]
        if not tables:
            raise ValueError(f"{path}:{n}: no tables listed")
        deps.append({"kind": parts[0].lower(), "name": parts[1], "tables": tables})
    return deps


def load_access(path):
    acc = []
    for n, parts in rows(path):
        if len(parts) != 3 or parts[2].lower() not in {"r", "w", "rw"}:
            raise ValueError(f"{path}:{n}: expected 'service, table, r|w|rw'")
        acc.append((parts[0], parts[1].lower(), parts[2].lower()))
    return acc


def analyze(domains, deps, access, threshold):
    unassigned = set()
    cross, pairs = [], Counter()
    for d in deps:
        tdoms = {}
        for t in d["tables"]:
            if t in domains:
                tdoms[t] = domains[t]
            else:
                unassigned.add(t)
        if not tdoms:
            continue
        # Home domain: explicit assignment of the artifact, else first table
        # (for an fk the child table, which holds the constraint).
        home = domains.get(d["name"].lower()) or tdoms.get(d["tables"][0]) or next(iter(tdoms.values()))
        involved = sorted(set(tdoms.values()) | {home})
        if len(involved) > 1:
            foreign = sorted(t for t, dm in tdoms.items() if dm != home)
            cross.append({**d, "home": home, "domains": involved, "foreign_tables": foreign})
            for other in involved:
                if other != home:
                    pairs[tuple(sorted((home, other)))] += 1
    pair_list = [{"pair": list(p), "links": c, "merge_candidate": c >= threshold}
                 for p, c in sorted(pairs.items(), key=lambda x: (-x[1], x[0]))]

    svc_issues = []
    if access:
        per_svc = defaultdict(lambda: {"read": set(), "write": Counter()})
        for svc, table, mode in access:
            if table not in domains:
                unassigned.add(table)
                continue
            dom = domains[table]
            if "r" in mode:
                per_svc[svc]["read"].add(dom)
            if "w" in mode:
                per_svc[svc]["write"][dom] += 1
        writers = defaultdict(set)
        for svc in sorted(per_svc):
            info = per_svc[svc]
            home = (sorted(info["write"].items(), key=lambda x: (-x[1], x[0]))[0][0]
                    if info["write"] else (sorted(info["read"])[0] if info["read"] else None))
            for dom in info["write"]:
                writers[dom].add(svc)
            touched = sorted(info["read"] | set(info["write"]))
            if len(touched) > 1:
                svc_issues.append({"service": svc, "home": home,
                                   "foreign_reads": sorted(info["read"] - {home}),
                                   "foreign_writes": sorted(set(info["write"]) - {home})})
        shared_writes = {dom: sorted(s) for dom, s in sorted(writers.items()) if len(s) > 1}
    else:
        shared_writes = {}
    return {"unassigned": sorted(unassigned), "cross_domain": cross, "pairs": pair_list,
            "service_violations": svc_issues, "multi_writer_domains": shared_writes}


def print_text(r, threshold):
    if r["unassigned"]:
        print("Unassigned tables (assign before deciding):", ", ".join(r["unassigned"]))
    print(f"Cross-domain artifacts to break: {len(r['cross_domain'])}")
    for c in r["cross_domain"]:
        print(f"  [{c['kind']}] {c['name']}: home={c['home']} domains={'/'.join(c['domains'])}"
              f" foreign tables={', '.join(c['foreign_tables']) or '-'}")
    if r["pairs"]:
        print(f"Domain-pair coupling (merge candidate at >= {threshold} links):")
        for p in r["pairs"]:
            flag = "  <- consider merging or keep together" if p["merge_candidate"] else ""
            print(f"  {p['pair'][0]} <-> {p['pair'][1]}: {p['links']}{flag}")
    if r["service_violations"]:
        print("Services touching more than one domain (route through owning service):")
        for s in r["service_violations"]:
            print(f"  {s['service']}: home={s['home']} foreign reads={s['foreign_reads'] or '-'}"
                  f" foreign writes={s['foreign_writes'] or '-'}")
    if r["multi_writer_domains"]:
        print("Domains written by several services (shared ownership to resolve):")
        for dom, svcs in r["multi_writer_domains"].items():
            print(f"  {dom}: {', '.join(svcs)}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("domains", help="file of 'object, domain' lines")
    ap.add_argument("dependencies", help="file of 'kind, name, table1 table2 ...' lines")
    ap.add_argument("--access", help="optional file of 'service, table, r|w|rw' lines")
    ap.add_argument("--merge-threshold", type=int, default=3,
                    help="links between two domains that flag a merge candidate (default 3)")
    ap.add_argument("--json", action="store_true", help="emit JSON")
    a = ap.parse_args()
    try:
        r = analyze(load_domains(a.domains), load_deps(a.dependencies),
                    load_access(a.access) if a.access else [], a.merge_threshold)
    except (OSError, ValueError) as e:
        print(e, file=sys.stderr)
        return 2
    if a.json:
        print(json.dumps(r, indent=2))
    else:
        print_text(r, a.merge_threshold)
    return 1 if r["cross_domain"] or r["service_violations"] else 0


if __name__ == "__main__":
    sys.exit(main())
