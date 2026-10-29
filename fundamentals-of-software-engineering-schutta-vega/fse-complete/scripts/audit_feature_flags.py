#!/usr/bin/env python3
"""Audit a feature-flag registry for hygiene problems.

Rules applied (flag types: release, experiment, permission):
  MISSING_FIELD      every flag needs name, type, owner and purpose; release and
                     experiment flags also need an expiry date.
  BAD_TYPE           type is not one of release / experiment / permission.
  EXPIRED            release or experiment flag whose expiry date is before --as-of.
  EXPIRING_SOON      expiry falls within --warn-days after --as-of.
  OVERLONG_LIFESPAN  planned lifespan (expires - created) of a temporary flag exceeds
                     --max-lifespan-days.
  CLEANUP_CANDIDATE  release flag already at 100% rollout (or "on") for longer than
                     --full-rollout-days since created; remove the flag and dead branch.
  ABANDONED          flag at 0% (or "off") older than --full-rollout-days.
Permission flags are long-lived by design: they need owner and purpose but no expiry.

Input : CSV with header, or JSON list of objects. Columns/keys:
        name,type,owner,purpose,created,expires,rollout
        Dates are YYYY-MM-DD. rollout is 0-100, or on/off/true/false.
Output: one line per finding "RULE name: detail", then counts per rule and per type;
        or JSON with --json. Exit 1 if --strict and any finding exists.
Deterministic: pass --as-of to fix "today" (defaults to the current date).

Example:
  python3 audit_feature_flags.py flags.csv --as-of 2026-10-29 --strict
"""
import argparse
import csv
import datetime as dt
import json
import sys

TYPES = {"release", "experiment", "permission"}
TEMPORARY = {"release", "experiment"}


def parse_date(text):
    text = (text or "").strip()
    if not text:
        return None
    return dt.date.fromisoformat(text)


def parse_rollout(text):
    t = str(text if text is not None else "").strip().lower().rstrip("%")
    if t in {"on", "true", "yes"}:
        return 100.0
    if t in {"off", "false", "no"}:
        return 0.0
    try:
        return float(t)
    except ValueError:
        return None


def load(path):
    with open(path, newline="", encoding="utf-8") as fh:
        if path.lower().endswith(".json"):
            return json.load(fh)
        return list(csv.DictReader(fh))


def audit(flags, as_of, warn_days, max_life, full_days):
    findings = []
    for row in flags:
        name = (row.get("name") or "<unnamed>").strip()
        ftype = (row.get("type") or "").strip().lower()
        add = lambda rule, detail: findings.append({"rule": rule, "flag": name, "type": ftype, "detail": detail})
        for field in ("name", "type", "owner", "purpose"):
            if not str(row.get(field) or "").strip():
                add("MISSING_FIELD", f"no {field}")
        if ftype and ftype not in TYPES:
            add("BAD_TYPE", f"unknown type '{ftype}'")
        try:
            created, expires = parse_date(row.get("created")), parse_date(row.get("expires"))
        except ValueError as exc:
            add("MISSING_FIELD", f"unparseable date ({exc})")
            continue
        rollout = parse_rollout(row.get("rollout"))
        age = (as_of - created).days if created else None
        if ftype in TEMPORARY:
            if not expires:
                add("MISSING_FIELD", "no expiry date for a temporary flag")
            elif expires < as_of:
                add("EXPIRED", f"expired {expires} ({(as_of - expires).days} days ago)")
            elif (expires - as_of).days <= warn_days:
                add("EXPIRING_SOON", f"expires {expires} (in {(expires - as_of).days} days)")
            if created and expires and (expires - created).days > max_life:
                add("OVERLONG_LIFESPAN", f"planned lifespan {(expires - created).days} days > {max_life}")
        if age is not None and age > full_days and rollout is not None:
            if ftype == "release" and rollout >= 100:
                add("CLEANUP_CANDIDATE", f"fully rolled out, {age} days old")
            elif rollout <= 0:
                add("ABANDONED", f"rollout 0%, {age} days old")
    return findings


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("registry", help="CSV or JSON flag registry")
    ap.add_argument("--as-of", type=dt.date.fromisoformat, default=dt.date.today(),
                    help="reference date YYYY-MM-DD (default: today)")
    ap.add_argument("--warn-days", type=int, default=14, help="EXPIRING_SOON window (default 14)")
    ap.add_argument("--max-lifespan-days", type=int, default=90,
                    help="max planned lifespan for release/experiment flags (default 90)")
    ap.add_argument("--full-rollout-days", type=int, default=30,
                    help="age after which a 100%% release flag or a 0%% flag is reported (default 30)")
    ap.add_argument("--json", action="store_true", help="emit JSON")
    ap.add_argument("--strict", action="store_true", help="exit 1 when any finding exists")
    args = ap.parse_args(argv)

    flags = load(args.registry)
    findings = audit(flags, args.as_of, args.warn_days, args.max_lifespan_days, args.full_rollout_days)
    by_rule, by_type = {}, {}
    for f in findings:
        by_rule[f["rule"]] = by_rule.get(f["rule"], 0) + 1
    for row in flags:
        t = (row.get("type") or "?").strip().lower() or "?"
        by_type[t] = by_type.get(t, 0) + 1

    if args.json:
        print(json.dumps({"as_of": str(args.as_of), "flags": len(flags), "by_type": by_type,
                          "by_rule": by_rule, "findings": findings}, indent=2, sort_keys=True))
    else:
        for f in findings:
            print(f"{f['rule']:<18} {f['flag']}: {f['detail']}")
        print(f"\n{len(flags)} flag(s) as of {args.as_of}; {len(findings)} finding(s)")
        print("  by type: " + ", ".join(f"{k}={v}" for k, v in sorted(by_type.items())))
        if by_rule:
            print("  by rule: " + ", ".join(f"{k}={v}" for k, v in sorted(by_rule.items())))
    return 1 if args.strict and findings else 0


if __name__ == "__main__":
    sys.exit(main())
