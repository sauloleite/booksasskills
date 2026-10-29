#!/usr/bin/env python3
"""Granularity driver worksheet for service split/merge decisions.

Based on the disintegrator/integrator framework of Chapter 7 ("Service
Granularity") of "Software Architecture: The Hard Parts". The script does NOT
decide; it turns measured evidence into a list of active drivers on each side
and the trade-off questions to put to the business.

Subcommands
-----------
assess   INPUT: JSON worksheet (see --example). Evaluates the six
         disintegrators and four integrators from measured signals using
         tunable heuristic thresholds, applies optional team-supplied weights,
         and prints active drivers, a weighted lean, and pairwise trade-off
         statements. OUTPUT: text report (or JSON with --json).
datamap  INPUT: JSON with functions -> {"writes": [...], "reads": [...]} and a
         proposed split {service: [functions]}. Assigns table ownership by
         writer, reports ownership conflicts, cross-service reads and
         bidirectional dependencies (merge candidates). OUTPUT: text or JSON.

Deterministic, stdlib only, no network. Exit code 2 on invalid input.
"""
import argparse
import json
import sys

EXAMPLE_ASSESS = {
    "service": "Notification",
    "parts": [
        {"name": "sms", "changes_per_month": 0.2, "peak_rpm": 220000,
         "crash_prone": False, "sensitive": False},
        {"name": "email", "changes_per_month": 0.2, "peak_rpm": 500,
         "crash_prone": True, "sensitive": False},
        {"name": "letter", "changes_per_month": 4, "peak_rpm": 1,
         "crash_prone": False, "sensitive": False},
    ],
    "cohesion": "strong",
    "extensibility": {"new_variants_expected": False, "pattern_confirmed": False},
    "acid_required_across_parts": False,
    "workflow": {"cross_part_request_pct": 10, "critical_request_crosses": False,
                 "user_waiting": True, "hops_per_request": 1,
                 "latency_per_hop_ms": 300, "parts_sync_coupled": False},
    "shared_code": {"shared_domain_pct": 5, "shared_changes_per_month": 0,
                    "unversionable_changes_per_quarter": 0},
    "cross_part_data_dependencies": 0,
    "bidirectional_data_dependency": False,
    "weights": {}
}

EXAMPLE_DATAMAP = {
    "functions": {
        "A": {"writes": ["t1", "t2", "t4", "t6"], "reads": []},
        "B": {"writes": ["t3"], "reads": ["t5"]},
        "C": {"writes": ["t5"], "reads": ["t3"]},
    },
    "split": {"svcA": ["A"], "svcB": ["B"], "svcC": ["C"]},
}

DISINTEGRATORS = ["scope", "volatility", "scalability", "fault_tolerance",
                  "security", "extensibility"]
INTEGRATORS = ["transactions", "workflow", "shared_code", "data_relationships"]

BENEFIT = {
    "scope": "single-purpose, tightly cohesive services",
    "volatility": "agility (smaller test scope, lower deployment risk)",
    "scalability": "lower cost and faster response under uneven load",
    "fault_tolerance": "better uptime for the healthy functions",
    "security": "tighter access control over sensitive operations",
    "extensibility": "easier addition of new variants (time to market)",
    "transactions": "atomic data integrity and consistency",
    "workflow": "end-to-end fault tolerance, latency and reliability",
    "shared_code": "simpler maintenance and synchronized change",
    "data_relationships": "correct data without chatty cross-service reads",
}


def fail(msg):
    print("error: " + msg, file=sys.stderr)
    sys.exit(2)


def ratio(values):
    vals = [v for v in values if v is not None]
    if len(vals) < 2:
        return None
    lo, hi = min(vals), max(vals)
    if lo <= 0:
        return float("inf") if hi > 0 else 1.0
    return hi / lo


def assess(ws, a):
    parts = ws.get("parts") or []
    if len(parts) < 2:
        fail("worksheet needs at least two 'parts' (candidate pieces of the service)")
    names = [p.get("name", "?") for p in parts]
    found = {}  # driver -> reason

    if str(ws.get("cohesion", "")).lower() == "weak":
        found["scope"] = "cohesion rated weak (functions share only a broad noun)"

    r = ratio([p.get("changes_per_month") for p in parts])
    if r is not None and r >= a.volatility_ratio:
        hot = max(parts, key=lambda p: p.get("changes_per_month") or 0)["name"]
        found["volatility"] = "change-rate skew %.1fx (hottest: %s)" % (r, hot)

    r = ratio([p.get("peak_rpm") for p in parts])
    if r is not None and r >= a.throughput_ratio:
        found["scalability"] = "peak-load skew %.0fx across parts" % r

    wf = ws.get("workflow") or {}
    crash = [p["name"] for p in parts if p.get("crash_prone")]
    notes = []
    if crash and len(crash) < len(parts):
        if wf.get("parts_sync_coupled"):
            notes.append("fault tolerance claimed for %s but parts are synchronously "
                         "coupled: splitting gives no request-level gain" % ", ".join(crash))
        else:
            found["fault_tolerance"] = "unstable part(s): %s" % ", ".join(crash)

    sens = [p["name"] for p in parts if p.get("sensitive")]
    if sens and len(sens) < len(parts):
        found["security"] = "sensitive operations in: %s" % ", ".join(sens)

    ext = ws.get("extensibility") or {}
    if ext.get("new_variants_expected"):
        if ext.get("pattern_confirmed"):
            found["extensibility"] = "confirmed pipeline of new variants"
        else:
            notes.append("extensibility expected but unconfirmed: wait for a pattern "
                         "before using it as the primary reason to split")

    if ws.get("acid_required_across_parts"):
        found["transactions"] = "business requires all-or-nothing across parts"

    pct = wf.get("cross_part_request_pct")
    hops = wf.get("hops_per_request") or 0
    lat = wf.get("latency_per_hop_ms") or 0
    reasons = []
    if pct is not None and pct > a.workflow_pct:
        reasons.append("%s%% of requests cross parts (> %s%%)" % (pct, a.workflow_pct))
    if wf.get("critical_request_crosses"):
        reasons.append("a latency-critical request needs several parts")
    if wf.get("parts_sync_coupled"):
        reasons.append("parts are synchronously coupled")
    if reasons:
        if not wf.get("user_waiting", True) and not wf.get("critical_request_crosses"):
            notes.append("workflow pressure is back-end only (no user waiting): "
                         "weaker integrator; " + "; ".join(reasons))
        else:
            found["workflow"] = "; ".join(reasons)
    if hops and lat:
        notes.append("added latency per workflow request ~%d ms (%d hops x %d ms)"
                     % (hops * lat, hops, lat))

    sc = ws.get("shared_code") or {}
    reasons = []
    if (sc.get("shared_domain_pct") or 0) >= a.shared_pct:
        reasons.append("shared domain code %s%% (>= %s%%)" % (sc["shared_domain_pct"], a.shared_pct))
    if (sc.get("shared_changes_per_month") or 0) >= a.shared_changes:
        reasons.append("shared domain library changes %s/month" % sc["shared_changes_per_month"])
    if (sc.get("unversionable_changes_per_quarter") or 0) >= 1:
        reasons.append("%s must-apply-everywhere changes/quarter"
                       % sc["unversionable_changes_per_quarter"])
    if reasons:
        found["shared_code"] = "; ".join(reasons)

    deps = ws.get("cross_part_data_dependencies") or 0
    if ws.get("bidirectional_data_dependency"):
        found["data_relationships"] = "parts read each other's tables (bidirectional)"
    elif deps > 0:
        found["data_relationships"] = "%d cross-part table read(s) would become calls" % deps

    weights = ws.get("weights") or {}
    for k in weights:
        if k not in DISINTEGRATORS + INTEGRATORS:
            fail("unknown weight key '%s'" % k)
    w = lambda k: float(weights.get(k, 1))
    dis = [k for k in DISINTEGRATORS if k in found]
    integ = [k for k in INTEGRATORS if k in found]
    split_score = sum(w(k) for k in dis)
    merge_score = sum(w(k) for k in integ)
    if split_score > merge_score:
        lean = "lean SPLIT"
    elif merge_score > split_score:
        lean = "lean KEEP TOGETHER"
    else:
        lean = "BALANCED"
    statements = []
    for d in dis:
        for i in integ:
            statements.append(
                "Splitting %s gives %s but costs %s. Which matters more for the business now?"
                % (ws.get("service", "the service"), BENEFIT[d], BENEFIT[i]))
    return {
        "service": ws.get("service"), "parts": names,
        "disintegrators": {k: found[k] for k in dis},
        "integrators": {k: found[k] for k in integ},
        "split_score": split_score, "merge_score": merge_score, "lean": lean,
        "notes": notes, "trade_off_statements": statements,
    }


def datamap(spec):
    funcs = spec.get("functions") or {}
    split = spec.get("split") or {}
    svc_of = {}
    for svc, fns in split.items():
        for f in fns:
            if f in svc_of:
                fail("function '%s' assigned to two services" % f)
            if f not in funcs:
                fail("split references unknown function '%s'" % f)
            svc_of[f] = svc
    missing = sorted(set(funcs) - set(svc_of))
    if missing:
        fail("functions not assigned to any service: " + ", ".join(missing))
    owners = {}
    for f in sorted(funcs):
        for t in funcs[f].get("writes", []):
            owners.setdefault(t, set()).add(svc_of[f])
    conflicts = {t: sorted(s) for t, s in sorted(owners.items()) if len(s) > 1}
    deps = {}
    for f in sorted(funcs):
        me = svc_of[f]
        for t in funcs[f].get("reads", []):
            own = owners.get(t)
            if not own:
                continue
            for o in sorted(own):
                if o != me:
                    deps.setdefault((me, o), set()).add(t)
    pairs = sorted({tuple(sorted(k)) for k in deps if (k[1], k[0]) in deps})
    return {
        "table_owner": {t: sorted(s) for t, s in sorted(owners.items())},
        "ownership_conflicts": conflicts,
        "cross_service_reads": [{"reader": a, "owner": b, "tables": sorted(ts)}
                                for (a, b), ts in sorted(deps.items())],
        "bidirectional_merge_candidates": [list(p) for p in pairs],
    }


def print_assess(r):
    print("Service: %s  parts: %s" % (r["service"], ", ".join(r["parts"])))
    print("\nActive disintegrators (reasons to split):")
    for k, v in r["disintegrators"].items() or []:
        print("  - %s: %s" % (k, v))
    if not r["disintegrators"]:
        print("  (none)")
    print("\nActive integrators (reasons to keep together):")
    for k, v in r["integrators"].items():
        print("  - %s: %s" % (k, v))
    if not r["integrators"]:
        print("  (none)")
    print("\nWeighted split=%.1f merge=%.1f -> %s" % (r["split_score"], r["merge_score"], r["lean"]))
    print("(A lean is an input to the business conversation, not a decision.)")
    if r["notes"]:
        print("\nNotes:")
        for n in r["notes"]:
            print("  - " + n)
    if r["trade_off_statements"]:
        print("\nTrade-off statements to take to the product owner:")
        for s in r["trade_off_statements"]:
            print("  - " + s)
    if r["disintegrators"]:
        print("\nReminder: check that every leftover piece can be named cleanly.")


def print_datamap(r):
    print("Table ownership (by writer):")
    for t, s in r["table_owner"].items():
        print("  %s -> %s" % (t, ", ".join(s)))
    if r["ownership_conflicts"]:
        print("\nOwnership conflicts (table written by several services):")
        for t, s in r["ownership_conflicts"].items():
            print("  %s: %s" % (t, ", ".join(s)))
    print("\nCross-service reads (each becomes an inter-service call):")
    for d in r["cross_service_reads"]:
        print("  %s reads %s from %s" % (d["reader"], ", ".join(d["tables"]), d["owner"]))
    if not r["cross_service_reads"]:
        print("  (none)")
    print("\nBidirectional dependencies (strong merge candidates):")
    for p in r["bidirectional_merge_candidates"]:
        print("  %s <-> %s" % tuple(p))
    if not r["bidirectional_merge_candidates"]:
        print("  (none)")


def load(path):
    try:
        with open(path) as fh:
            return json.load(fh)
    except (OSError, ValueError) as e:
        fail("cannot read %s: %s" % (path, e))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("assess", help="evaluate disintegrators vs integrators")
    p.add_argument("worksheet", nargs="?", help="JSON worksheet path")
    p.add_argument("--example", action="store_true", help="print a sample worksheet and exit")
    p.add_argument("--volatility-ratio", type=float, default=4.0,
                   help="max/min change-rate ratio that activates volatility (default 4)")
    p.add_argument("--throughput-ratio", type=float, default=10.0,
                   help="max/min peak-load ratio that activates scalability (default 10)")
    p.add_argument("--workflow-pct", type=float, default=50.0,
                   help="cross-part request share above which workflow activates (default 50)")
    p.add_argument("--shared-pct", type=float, default=40.0,
                   help="shared domain code share that activates shared code (default 40)")
    p.add_argument("--shared-changes", type=float, default=2.0,
                   help="shared library changes/month that activate shared code (default 2)")
    p.add_argument("--json", action="store_true", help="emit JSON")
    q = sub.add_parser("datamap", help="analyze table ownership under a proposed split")
    q.add_argument("spec", nargs="?", help="JSON spec path")
    q.add_argument("--example", action="store_true", help="print a sample spec and exit")
    q.add_argument("--json", action="store_true", help="emit JSON")
    a = ap.parse_args()
    if a.cmd == "assess":
        if a.example:
            print(json.dumps(EXAMPLE_ASSESS, indent=2))
            return
        if not a.worksheet:
            fail("worksheet path required (or --example)")
        r = assess(load(a.worksheet), a)
        print(json.dumps(r, indent=2)) if a.json else print_assess(r)
    else:
        if a.example:
            print(json.dumps(EXAMPLE_DATAMAP, indent=2))
            return
        if not a.spec:
            fail("spec path required (or --example)")
        r = datamap(load(a.spec))
        print(json.dumps(r, indent=2)) if a.json else print_datamap(r)


if __name__ == "__main__":
    main()
