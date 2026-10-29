#!/usr/bin/env python3
"""Integration write-direction fitness function for ESB / integration-hub logs.

Checks that integration points only write to the targets they are allowed to
write to (for example: ERP and sales systems are read-only sources and may
only write to accounting). Supports guarding an ESB against data or bounded
contexts leaking where they should not.

Inputs
  --log FILE        JSON Lines file; one interaction per line with keys
                    "source", "operation", "target" and optional "timestamp"
                    (ISO 8601, e.g. 2026-10-29T10:00:00Z).
  --allow SRC=T1,T2 Allowed write targets for a source (repeatable). Sources
                    with no --allow entry may not write anywhere.
  --sources S1,S2   Only check these sources (default: all sources in log).
  --write-ops OPS   Comma-separated operations treated as writes
                    (default: create,update,delete,upsert).
  --window-hours H  Only check entries within H hours before --now.
  --now TS          Reference time for the window (ISO 8601). Default: latest
                    timestamp in the log, which keeps runs deterministic.

Outputs
  A text report (or JSON with --json) listing violations and a summary.
  Exit code 0 = pass, 1 = violations found, 2 = input error.
  Entries missing required keys are reported as malformed (they also fail
  the check, since consistent logging is a precondition of the guard).
"""
import argparse
import json
import sys
from datetime import datetime, timedelta, timezone

REQUIRED = ("source", "operation", "target")


def parse_ts(value):
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def parse_allow(items):
    allowed = {}
    for item in items:
        if "=" not in item:
            raise ValueError(f"--allow must look like SRC=T1,T2, got {item!r}")
        src, targets = item.split("=", 1)
        allowed.setdefault(src.strip().lower(), set()).update(
            t.strip().lower() for t in targets.split(",") if t.strip())
    return allowed


def load(path):
    entries, malformed = [], []
    with open(path, encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            if not line.strip():
                continue
            try:
                e = json.loads(line)
            except json.JSONDecodeError:
                malformed.append({"line": n, "reason": "invalid JSON"})
                continue
            missing = [k for k in REQUIRED if k not in e]
            if missing:
                malformed.append({"line": n, "reason": "missing " + ",".join(missing)})
                continue
            e["_line"] = n
            entries.append(e)
    return entries, malformed


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--log", required=True)
    ap.add_argument("--allow", action="append", default=[])
    ap.add_argument("--sources", default="")
    ap.add_argument("--write-ops", default="create,update,delete,upsert")
    ap.add_argument("--window-hours", type=float)
    ap.add_argument("--now")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    try:
        allowed = parse_allow(a.allow)
        entries, malformed = load(a.log)
        now = parse_ts(a.now) if a.now else None
        if a.window_hours is not None:
            stamped = [parse_ts(e["timestamp"]) for e in entries if "timestamp" in e]
            now = now or (max(stamped) if stamped else None)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    sources = {s.strip().lower() for s in a.sources.split(",") if s.strip()}
    write_ops = {o.strip().lower() for o in a.write_ops.split(",") if o.strip()}
    checked, violations = 0, []
    for e in entries:
        src, op, tgt = (str(e[k]).lower() for k in REQUIRED)
        if sources and src not in sources:
            continue
        if a.window_hours is not None and now is not None:
            if "timestamp" not in e:
                continue
            ts = parse_ts(e["timestamp"])
            if ts < now - timedelta(hours=a.window_hours) or ts > now:
                continue
        checked += 1
        if op in write_ops and tgt not in allowed.get(src, set()):
            violations.append({"line": e["_line"], "source": src,
                               "operation": op, "target": tgt})

    ok = not violations and not malformed
    if a.json:
        print(json.dumps({"pass": ok, "checked": checked, "violations": violations,
                          "malformed": malformed}, indent=2))
    else:
        for v in violations:
            print(f"VIOLATION line {v['line']}: {v['source']} -> {v['target']} "
                  f"({v['operation']}) not an allowed write path")
        for m in malformed:
            print(f"MALFORMED line {m['line']}: {m['reason']}")
        print(f"checked={checked} violations={len(violations)} "
              f"malformed={len(malformed)} result={'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
