#!/usr/bin/env python3
"""Risk scoring, risk-storming aggregation and risk-assessment tables (FSA ch. 22).

Subcommands
-----------
score       Score one risk: impact x likelihood (each 1..3) -> 1..9 and band.
            Likelihood may be "unknown" (treated as 3). --unknown-tech forces 9.

storm       Aggregate individual (phase 1) risk-storming ratings.
            Input CSV columns (header required):
              participant, area, criterion, impact, likelihood[, note]
            impact/likelihood are 1..3; likelihood may be "unknown" (-> 3);
            either field may be "unknown-tech" to force a score of 9.
            Each row is one sticky note. A participant who left no note on an
            area is counted as "saw no risk" there.
            Output: one line per (area, criterion) with every score, the band of
            each, a status (AGREED, DIVERGENT, LONE, UNKNOWN-TECH) and a
            discussion order (unknown tech and high scores first).

assess      Build a criteria x context risk-assessment table.
            Input CSV columns: criterion, context, score[, previous]
            Output: matrix with row and column totals, the highest-risk criterion
            and context, direction markers when "previous" is given
            (^ worse, v better, o unchanged), and --high-only to blank out
            low/medium cells for a stakeholder view.

downtime    Convert an availability percentage (e.g. 99.9) to allowed downtime
            per year, month and week, to check an SLA/SLO against a need.

All output is plain text (or JSON with --json on storm/assess). Deterministic,
standard library only, no network access.
"""
import argparse
import csv
import json
import statistics
import sys
from collections import defaultdict

BANDS = ((1, 2, "low"), (3, 4, "medium"), (6, 9, "high"))


def band(score):
    for lo, hi, name in BANDS:
        if lo <= score <= hi:
            return name
    raise ValueError(f"invalid risk score {score}; valid products are 1,2,3,4,6,9")


def parse_level(value, field):
    v = str(value).strip().lower()
    if v in ("unknown-tech", "unknown_tech", "tech"):
        return "TECH"
    if v in ("unknown", "?", ""):
        if field == "impact":
            raise ValueError("impact cannot be unknown; decide impact first")
        return 3  # unsure of likelihood: assume high until confirmed
    n = int(v)
    if n not in (1, 2, 3):
        raise ValueError(f"{field} must be 1, 2 or 3 (got {value})")
    return n


def rate(impact, likelihood):
    i, l = parse_level(impact, "impact"), parse_level(likelihood, "likelihood")
    if "TECH" in (i, l):
        return 9, True
    return i * l, False


def cmd_score(a):
    s, tech = rate("3" if a.unknown_tech else a.impact, "unknown-tech" if a.unknown_tech else a.likelihood)
    print(f"risk={s} band={band(s)}" + (" (unknown/unproven technology)" if tech else ""))


def read_csv(path, required):
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        sys.exit(f"{path}: no rows")
    missing = [c for c in required if c not in rows[0]]
    if missing:
        sys.exit(f"{path}: missing columns {missing}")
    return [{k.strip(): (v or "").strip() for k, v in r.items() if k} for r in rows]


def cmd_storm(a):
    rows = read_csv(a.csv, ["participant", "area", "criterion", "impact", "likelihood"])
    people = sorted(set(a.participants.split(",")) if a.participants else {r["participant"] for r in rows})
    notes = defaultdict(dict)
    for r in rows:
        s, tech = rate(r["impact"], r["likelihood"])
        notes[(r["area"], r["criterion"])][r["participant"]] = (s, tech, r.get("note", ""))
    out = []
    for (area, crit), byp in notes.items():
        scores = [v[0] for v in byp.values()]
        bands = {band(s) for s in scores}
        tech = any(v[1] for v in byp.values())
        silent = [p for p in people if p not in byp]
        if tech:
            status = "UNKNOWN-TECH"
        elif len(byp) == 1 and len(people) > 1:
            status = "LONE"
        elif len(set(scores)) == 1 and not silent:
            status = "AGREED"
        else:
            status = "DIVERGENT"
        out.append({
            "area": area, "criterion": crit, "status": status,
            "scores": {p: byp[p][0] for p in sorted(byp)}, "silent": silent,
            "max": max(scores), "median": statistics.median(scores),
            "bands": sorted(bands), "discuss": status != "AGREED",
            "notes": {p: byp[p][2] for p in sorted(byp) if byp[p][2]},
        })
    rank = {"UNKNOWN-TECH": 0, "LONE": 1, "DIVERGENT": 1, "AGREED": 2}
    out.sort(key=lambda d: (rank[d["status"]], -d["max"], d["area"], d["criterion"]))
    if a.json:
        print(json.dumps({"participants": people, "areas": out}, indent=2))
        return
    crits = sorted({d["criterion"] for d in out})
    print(f"participants: {', '.join(people)}")
    if len(crits) > 1:
        print(f"WARNING: {len(crits)} criteria mixed ({', '.join(crits)}); discuss each separately")
    print(f"{'#':>2}  {'status':<12} {'max':>3} {'med':>4}  area / criterion  -> scores")
    for i, d in enumerate(out, 1):
        sc = ", ".join(f"{p}={s}" for p, s in d["scores"].items())
        sil = f"; no risk seen: {', '.join(d['silent'])}" if d["silent"] else ""
        print(f"{i:>2}  {d['status']:<12} {d['max']:>3} {d['median']:>4g}  {d['area']} / {d['criterion']}  -> {sc}{sil}")
        for p, n in d["notes"].items():
            print(f"      {p}: {n}")
    agreed = [d for d in out if d["status"] == "AGREED"]
    print(f"\n{len(out) - len(agreed)} to discuss, {len(agreed)} already agreed (no discussion needed)")


def cmd_assess(a):
    rows = read_csv(a.csv, ["criterion", "context", "score"])
    crits, ctxs, cell, prev = [], [], {}, {}
    for r in rows:
        c, x, s = r["criterion"], r["context"], int(r["score"])
        band(s)
        if c not in crits:
            crits.append(c)
        if x not in ctxs:
            ctxs.append(x)
        cell[(c, x)] = s
        if r.get("previous"):
            prev[(c, x)] = int(r["previous"])
    rt = {c: sum(cell.get((c, x), 0) for x in ctxs) for c in crits}
    ct = {x: sum(cell.get((c, x), 0) for c in crits) for x in ctxs}

    def arrow(k):
        if k not in prev:
            return " "
        return "^" if cell[k] > prev[k] else "v" if cell[k] < prev[k] else "o"

    if a.json:
        print(json.dumps({"cells": [{"criterion": c, "context": x, "score": s, "band": band(s),
                                     "direction": arrow((c, x)).strip() or None}
                                    for (c, x), s in cell.items()],
                          "criterion_totals": rt, "context_totals": ct}, indent=2))
        return
    w = max(len(c) for c in crits + ["criterion"]) + 2
    cw = max(10, max(len(x) for x in ctxs) + 2)
    print("criterion".ljust(w) + "".join(x.rjust(cw) for x in ctxs) + ("" if a.high_only else "total".rjust(8)))
    for c in crits:
        line = c.ljust(w)
        for x in ctxs:
            k = (c, x)
            if k not in cell or (a.high_only and band(cell[k]) != "high"):
                line += "".rjust(cw)
            else:
                line += f"{cell[k]}{arrow(k)}".rjust(cw)
        print(line + ("" if a.high_only else str(rt[c]).rjust(8)))
    if not a.high_only:
        print("total".ljust(w) + "".join(str(ct[x]).rjust(cw) for x in ctxs))
        print(f"\nhighest-risk criterion: {max(crits, key=lambda c: rt[c])} ({max(rt.values())}); "
              f"lowest: {min(crits, key=lambda c: rt[c])} ({min(rt.values())})")
        print(f"highest-risk context: {max(ctxs, key=lambda x: ct[x])} ({max(ct.values())}); "
              f"lowest: {min(ctxs, key=lambda x: ct[x])} ({min(ct.values())})")
    if prev:
        print("key: ^ risk rising, v risk falling, o unchanged")
    print("bands: 1-2 low, 3-4 medium, 6-9 high" + ("; only high cells shown" if a.high_only else ""))


def cmd_downtime(a):
    down = 1 - a.availability / 100.0
    year_min = down * 365.25 * 24 * 60
    print(f"{a.availability}% availability allows: {year_min:.2f} min/year "
          f"({year_min / 60:.2f} h), {year_min / 12:.2f} min/month, {year_min / 52.1786:.2f} min/week")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("score", help="score one risk")
    s.add_argument("--impact", default="3", help="1..3")
    s.add_argument("--likelihood", default="unknown", help="1..3 or 'unknown' (treated as 3)")
    s.add_argument("--unknown-tech", action="store_true", help="unproven/unknown technology: force 9")
    s.set_defaults(fn=cmd_score)
    s = sub.add_parser("storm", help="aggregate phase-1 risk-storming notes")
    s.add_argument("csv")
    s.add_argument("--participants", help="comma list of all invitees (default: everyone in the CSV)")
    s.add_argument("--json", action="store_true")
    s.set_defaults(fn=cmd_storm)
    s = sub.add_parser("assess", help="criteria x context risk-assessment table")
    s.add_argument("csv")
    s.add_argument("--high-only", action="store_true", help="show only high (6-9) cells")
    s.add_argument("--json", action="store_true")
    s.set_defaults(fn=cmd_assess)
    s = sub.add_parser("downtime", help="availability %% to allowed downtime")
    s.add_argument("availability", type=float, help="e.g. 99.95")
    s.set_defaults(fn=cmd_downtime)
    a = p.parse_args()
    try:
        a.fn(a)
    except ValueError as e:
        sys.exit(f"error: {e}")


if __name__ == "__main__":
    main()
