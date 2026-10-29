#!/usr/bin/env python3
"""Structural checks for Architectural Decision Records (ADRs) and approval routing.

Subcommands
-----------
lint PATH [PATH ...]
    Inputs: ADR files (.md, .adoc, .txt) or directories searched recursively.
    Sections are recognized as Markdown headings ("## Status") or label lines
    ("STATUS" or "Status: Accepted"). The title is the first non-empty line and
    must carry a number ("# 23. Use X", "ADR 23. Use X").
    Checks per file: required sections (Status, Context, Decision, Consequences),
    recommended sections (Compliance, Notes), valid status value, RFC deadline,
    affirmative "We will" voice and hedging words in Decision, alternatives named
    in Context, governance method named in Compliance, length (about two pages).
    Checks across files: supersession links exist in both directions, a
    superseding ADR is Accepted, only Accepted ADRs get superseded (Proposed
    or RFC drafts are edited instead), duplicate numbers.
    Output: one line per finding (ERROR/WARN) or JSON with --json.
    Exit code 1 if any ERROR, else 0.

route --hours H --fte-rate R [--fees F] [--hardware W] --threshold T
      [--cross-team] [--security]
    Computes decision cost = hours * FTE rate + fees + hardware and reports
    whether the architect may accept the ADR alone or must mark it Proposed and
    escalate (cost above threshold, cross-team impact, or security impact).

Stdlib only, deterministic, no network.
"""
import argparse
import json
import pathlib
import re
import sys

REQUIRED = ["status", "context", "decision", "consequences"]
RECOMMENDED = ["compliance", "notes"]
KNOWN = set(REQUIRED + RECOMMENDED + ["alternatives"])
HEDGES = ["i think", "i believe", "might", "maybe", "perhaps", "probably",
          "could be", "would be the best", "we should consider", "it seems"]
OPTION_CUES = [" or ", "option", "alternative", " versus ", " vs ", "either"]
GOVERN_CUES = ["manual", "review", "automat", "fitness", "test", "archunit",
               "netarchtest", "lint", "check"]
MAX_WORDS = 1000  # rough ceiling for "one to two pages"

HEAD_RE = re.compile(r"^\s*#{1,6}\s*([A-Za-z ]+?)\s*:?\s*$")
LABEL_RE = re.compile(r"^\s*([A-Za-z]+)\s*:\s*(.*)$")
TITLE_NUM_RE = re.compile(r"^\s*#*\s*(?:ADR[\s-]*)?(\d+)[.:)\s]")


def parse(text):
    lines = text.splitlines()
    title = next((l.strip() for l in lines if l.strip()), "")
    m = TITLE_NUM_RE.match(title)
    number = int(m.group(1)) if m else None
    sections, current = {}, None
    for line in lines[1:] if lines else []:
        name, rest = None, ""
        h = HEAD_RE.match(line)
        if h:  # any Markdown heading starts a new section, known or not
            name = h.group(1).strip().lower()
        elif line.strip().upper() == line.strip() and line.strip().lower() in KNOWN:
            name = line.strip().lower()
        else:
            lm = LABEL_RE.match(line)
            if lm and lm.group(1).lower() in KNOWN:
                name, rest = lm.group(1).lower(), lm.group(2)
        if name:
            current = name
            sections.setdefault(name, [])
            if rest:
                sections[name].append(rest)
        elif current:
            sections[current].append(line)
    body = {k: "\n".join(v).strip() for k, v in sections.items()}
    return title, number, body


def classify_status(status):
    s = status.lower()
    if s.startswith("superseded"):
        return "superseded"
    if s.startswith("accepted") or s.startswith("approved"):
        return "accepted"
    if s.startswith("proposed"):
        return "proposed"
    if s.startswith("request for comment") or s.startswith("rfc"):
        return "rfc"
    return None


def lint_file(path):
    text = path.read_text(encoding="utf-8")
    title, number, body = parse(text)
    f = []
    add = lambda lvl, msg: f.append({"file": str(path), "level": lvl, "msg": msg})
    if number is None:
        add("ERROR", "title has no sequential number: %r" % title[:60])
    for s in REQUIRED:
        if not body.get(s):
            add("ERROR", "missing or empty required section: %s" % s.title())
    for s in RECOMMENDED:
        if not body.get(s):
            add("WARN", "recommended section absent: %s" % s.title())
    status = body.get("status", "").splitlines()[0].strip() if body.get("status") else ""
    kind = classify_status(status) if status else None
    sup_by = re.search(r"superseded\s+by\s+(?:adr\s*)?(\d+)", status, re.I)
    sup_of = re.search(r"supersedes\s+(?:adr\s*)?(\d+)", status, re.I)
    if status and kind is None:
        add("ERROR", "unknown status %r (use Proposed, Accepted, Superseded, RFC)" % status)
    if kind == "superseded" and not sup_by:
        add("ERROR", "Superseded status must name the replacing ADR number")
    if kind == "rfc" and not re.search(r"\d{1,4}[-/ ]\w+[-/ ]\d{2,4}", status):
        add("WARN", "RFC status should carry a review deadline date")
    dec = body.get("decision", "")
    if dec:
        low = dec.lower()
        if "we will" not in low:
            add("WARN", "Decision lacks affirmative 'We will ...' statement")
        hits = sorted({h for h in HEDGES if re.search(r"\b%s\b" % re.escape(h), low)})
        if hits:
            add("WARN", "hedging language in Decision: %s" % ", ".join(hits))
    ctx = body.get("context", "")
    if ctx and not any(c in " %s " % ctx.lower() for c in OPTION_CUES):
        add("WARN", "Context does not appear to name alternatives")
    comp = body.get("compliance", "")
    if comp and not any(c in comp.lower() for c in GOVERN_CUES):
        add("WARN", "Compliance does not say how conformance is checked (manual or automated)")
    words = len(re.findall(r"\w+", text))
    if words > MAX_WORDS:
        add("WARN", "ADR is %d words; aim for one to two pages" % words)
    rec = {"file": str(path), "number": number, "kind": kind,
           "superseded_by": int(sup_by.group(1)) if sup_by else None,
           "supersedes": int(sup_of.group(1)) if sup_of else None}
    return rec, f


def cross_check(recs):
    f = []
    by_num = {}
    for r in recs:
        if r["number"] is None:
            continue
        if r["number"] in by_num:
            f.append({"file": r["file"], "level": "ERROR",
                      "msg": "duplicate ADR number %d (also %s)" % (r["number"], by_num[r["number"]]["file"])})
        by_num.setdefault(r["number"], r)
    for r in recs:
        n = r["superseded_by"]
        if n is not None:
            other = by_num.get(n)
            if not other:
                f.append({"file": r["file"], "level": "ERROR", "msg": "superseding ADR %d not found" % n})
            else:
                if other["supersedes"] != r["number"]:
                    f.append({"file": other["file"], "level": "ERROR",
                              "msg": "should state 'supersedes %s'" % r["number"]})
                if other["kind"] != "accepted":
                    f.append({"file": other["file"], "level": "WARN",
                              "msg": "superseding ADR is not Accepted"})
        m = r["supersedes"]
        if m is not None:
            old = by_num.get(m)
            if not old:
                f.append({"file": r["file"], "level": "WARN", "msg": "superseded ADR %d not found" % m})
            elif old["kind"] in ("proposed", "rfc"):
                f.append({"file": r["file"], "level": "ERROR",
                          "msg": "ADR %d is %s; edit it until Accepted instead of superseding it" % (m, old["kind"])})
            elif old["superseded_by"] != r["number"]:
                f.append({"file": old["file"], "level": "ERROR",
                          "msg": "status should be 'Superseded by %s'" % r["number"]})
    return f


def collect(paths):
    out = []
    for p in map(pathlib.Path, paths):
        if p.is_dir():
            out += sorted(q for q in p.rglob("*") if q.suffix in (".md", ".adoc", ".txt"))
        elif p.is_file():
            out.append(p)
        else:
            sys.exit("not found: %s" % p)
    return out


def cmd_lint(a):
    recs, findings = [], []
    files = collect(a.paths)
    for p in files:
        r, f = lint_file(p)
        recs.append(r)
        findings += f
    findings += cross_check(recs)
    findings.sort(key=lambda x: (x["file"], x["level"], x["msg"]))
    if a.json:
        print(json.dumps({"files": len(files), "findings": findings}, indent=2))
    else:
        for x in findings:
            print("%-5s %s: %s" % (x["level"], x["file"], x["msg"]))
        errs = sum(x["level"] == "ERROR" for x in findings)
        print("checked %d file(s): %d error(s), %d warning(s)" % (len(files), errs, len(findings) - errs))
    return 1 if any(x["level"] == "ERROR" for x in findings) else 0


def cmd_route(a):
    labor = a.hours * a.fte_rate
    total = labor + a.fees + a.hardware
    reasons = []
    if total > a.threshold:
        reasons.append("cost %.2f exceeds threshold %.2f" % (total, a.threshold))
    if a.cross_team:
        reasons.append("affects other teams or systems")
    if a.security:
        reasons.append("has security implications")
    res = {"labor_cost": round(labor, 2), "total_cost": round(total, 2),
           "threshold": a.threshold, "escalate": bool(reasons), "reasons": reasons,
           "status": "Proposed (needs higher-level approval)" if reasons else "Accepted (within your authority)"}
    if a.json:
        print(json.dumps(res, indent=2))
    else:
        print("labor cost: %.2f  total cost: %.2f  threshold: %.2f" % (labor, total, a.threshold))
        print("status: %s" % res["status"])
        for r in reasons:
            print("  - %s" % r)
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    l = sub.add_parser("lint", help="check ADR files or directories")
    l.add_argument("paths", nargs="+")
    l.add_argument("--json", action="store_true")
    r = sub.add_parser("route", help="decide whether an ADR needs escalation")
    r.add_argument("--hours", type=float, required=True, help="estimated implementation hours")
    r.add_argument("--fte-rate", type=float, required=True, help="standard FTE hourly rate")
    r.add_argument("--fees", type=float, default=0.0, help="license or purchase fees")
    r.add_argument("--hardware", type=float, default=0.0, help="additional hardware cost")
    r.add_argument("--threshold", type=float, required=True, help="agreed self-approval cost limit")
    r.add_argument("--cross-team", action="store_true", help="decision affects other teams/systems")
    r.add_argument("--security", action="store_true", help="decision has security implications")
    r.add_argument("--json", action="store_true")
    a = ap.parse_args()
    sys.exit(cmd_lint(a) if a.cmd == "lint" else cmd_route(a))


if __name__ == "__main__":
    main()
