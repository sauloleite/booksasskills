#!/usr/bin/env python3
"""Classify table ownership after a data split (single, joint, common).

Applies the "writer owns the table" heuristic from Chapter 9 of
"Software Architecture: The Hard Parts" and flags the resolution options
for joint and common ownership.

INPUT: a CSV file with a header row and these columns:
    table    table name
    service  service name
    access   CRUD letters the service performs on the table, e.g. CRUD, RU, R.
             Also accepted: "read"/"r" (read only), "write"/"w" (treated as U).
    columns  optional; semicolon-separated non-key columns the service WRITES.
             Used to judge whether a table split is feasible.
Optional --domains CSV with header "service,domain" to check whether joint
writers share a domain.

OUTPUT: a text report (default) or JSON (--json) listing, per table, the
classification, the owner or candidate owners, readers outside the owner's
context, and for joint/common tables the applicable techniques with hints.
Also lists services that would end up connected to more than one schema if a
shared data domain were used.

Classification rules:
    0 writers                         -> unowned (assign whoever maintains it)
    1 writer                          -> single
    writers >= --common-ratio * total services and >= --common-min -> common
    otherwise (2+ writers)            -> joint
"""
import argparse
import csv
import json
import sys
from collections import defaultdict

WRITE_OPS = set("CUD")


def parse_access(raw):
    v = raw.strip().upper()
    if v in ("READ", "R", "RO"):
        return {"R"}
    if v in ("WRITE", "W", "RW"):
        return {"R", "U"} if v == "RW" else {"U"}
    ops = set(v)
    bad = ops - set("CRUD")
    if bad:
        raise ValueError(f"unknown access letters {''.join(sorted(bad))!r} in {raw!r}")
    return ops


def load(path):
    tables = defaultdict(dict)  # table -> service -> {"ops": set, "cols": set}
    with open(path, newline="") as fh:
        for i, row in enumerate(csv.DictReader(fh), start=2):
            t, s = row["table"].strip(), row["service"].strip()
            if not t or not s:
                raise ValueError(f"line {i}: table and service are required")
            entry = tables[t].setdefault(s, {"ops": set(), "cols": set()})
            entry["ops"] |= parse_access(row.get("access") or "R")
            cols = (row.get("columns") or "").strip()
            if cols:
                entry["cols"] |= {c.strip() for c in cols.split(";") if c.strip()}
    return tables


def load_domains(path):
    if not path:
        return {}
    with open(path, newline="") as fh:
        return {r["service"].strip(): r["domain"].strip() for r in csv.DictReader(fh)}


def classify(tables, total_services, ratio, common_min):
    out = []
    for t in sorted(tables):
        svc = tables[t]
        writers = sorted(s for s, e in svc.items() if e["ops"] & WRITE_OPS)
        readers = sorted(s for s, e in svc.items() if not e["ops"] & WRITE_OPS)
        n = len(writers)
        if n == 0:
            kind = "unowned"
        elif n == 1:
            kind = "single"
        elif n >= common_min and n >= ratio * total_services:
            kind = "common"
        else:
            kind = "joint"
        out.append({"table": t, "classification": kind, "writers": writers,
                    "readers": readers, "detail": svc})
    return out


def joint_hints(rec, domains, single_owned_by):
    d = rec["detail"]
    w = rec["writers"]
    hints = {}
    col_sets = {s: d[s]["cols"] for s in w}
    if all(col_sets.values()):
        pairwise = {c for a in w for b in w if a < b for c in col_sets[a] & col_sets[b]}
        if pairwise:
            hints["table_split"] = f"not clean: writers share columns {sorted(pairwise)}"
        else:
            hints["table_split"] = ("feasible: disjoint write columns; plan create/delete "
                                    "sync and choose availability vs consistency")
    else:
        hints["table_split"] = "unknown: supply written columns per writer to judge"
    # delegate candidates
    score = {s: len(d[s]["ops"] & set("CD")) * 2 + len(d[s]["ops"] & WRITE_OPS) for s in w}
    best = max(score.values())
    primary = sorted(s for s in w if score[s] == best)
    hints["delegate_primary_domain"] = (
        f"candidate owner {primary[0]} (does most entity create/delete)" if len(primary) == 1
        else f"tie between {primary}; pick the service representing the entity's domain")
    hints["delegate_operational"] = ("alternative: the writer with the highest write rate or "
                                     "strictest performance/availability; usually prefer domain priority plus caching")
    conflicts = {s: single_owned_by[s] for s in w if single_owned_by.get(s)}
    if conflicts:
        hints["data_domain"] = ("risky: writers already own other tables "
                                f"{conflicts}; a shared schema would put them on two schemas "
                                "or pull those tables in (drift back to a monolithic database)")
    else:
        hints["data_domain"] = ("possible: no runtime dependency, but coordinated schema change "
                                "and write governance; re-ask why the services are separate")
    if domains:
        ds = {domains.get(s, "?") for s in w}
        if len(ds) > 1:
            hints["domain_check"] = (f"writers span domains {sorted(ds)}; joint ownership is "
                                     "usually intra-domain, so prefer delegate over data domain or consolidation")
    hints["consolidation"] = ("restores ACID and performance; costs coarse scaling, wider tests, "
                              "higher deployment risk, shared failure")
    return hints


def build_report(tables, domains, ratio, common_min, total_override):
    services = {s for t in tables.values() for s in t}
    total = total_override or len(services)
    recs = classify(tables, total, ratio, common_min)
    single_owned_by = defaultdict(list)
    for r in recs:
        if r["classification"] == "single":
            single_owned_by[r["writers"][0]].append(r["table"])
    for r in recs:
        if r["classification"] == "single":
            r["owner"] = r["writers"][0]
            r["external_readers"] = r["readers"]
        elif r["classification"] == "common":
            r["owner"] = f"new dedicated service for {r['table']}"
            r["hints"] = {"dedicated_owner": "others send data to it",
                          "no_reply_needed": "fire-and-forget on a persistent queue",
                          "reply_needed": "synchronous call or request-reply"}
        elif r["classification"] == "joint":
            r["owner"] = None
            r["hints"] = joint_hints(r, domains, single_owned_by)
        else:
            r["owner"] = None
        del r["detail"]
    return {"total_services": total, "tables": recs}


def print_text(rep):
    print(f"Services considered: {rep['total_services']}")
    order = {"single": 0, "common": 1, "joint": 2, "unowned": 3}
    for r in sorted(rep["tables"], key=lambda x: (order[x["classification"]], x["table"])):
        print(f"\n[{r['classification'].upper()}] {r['table']}")
        print(f"  writers: {', '.join(r['writers']) or '-'}")
        print(f"  readers: {', '.join(r['readers']) or '-'}")
        if r["owner"]:
            print(f"  owner: {r['owner']}")
        if r.get("external_readers"):
            print(f"  needs read-access technique: {', '.join(r['external_readers'])}")
        for k, v in r.get("hints", {}).items():
            print(f"  {k}: {v}")


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0],
                                formatter_class=argparse.RawDescriptionHelpFormatter,
                                epilog="Example: data_ownership.py access.csv --domains domains.csv")
    p.add_argument("access_csv", help="CSV with columns table,service,access[,columns]")
    p.add_argument("--domains", help="optional CSV with columns service,domain")
    p.add_argument("--common-ratio", type=float, default=0.75,
                   help="share of all services that must write a table for common ownership (default 0.75)")
    p.add_argument("--common-min", type=int, default=3,
                   help="minimum writer count for common ownership (default 3)")
    p.add_argument("--total-services", type=int, default=0,
                   help="override the service count (default: services seen in the CSV)")
    p.add_argument("--json", action="store_true", help="emit JSON instead of text")
    a = p.parse_args(argv)
    try:
        rep = build_report(load(a.access_csv), load_domains(a.domains),
                           a.common_ratio, a.common_min, a.total_services)
    except (OSError, KeyError, ValueError) as err:
        print(f"error: {err}", file=sys.stderr)
        return 2
    if a.json:
        print(json.dumps(rep, indent=2, sort_keys=True))
    else:
        print_text(rep)
    return 0


if __name__ == "__main__":
    sys.exit(main())
