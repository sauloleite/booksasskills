#!/usr/bin/env python3
"""Check and rebalance per-service connection quotas against a shared database.

Inputs
  services CSV (required) with header: service,quota,max_used,instances[,waits]
      quota      connections allowed in ONE instance's pool
      max_used   peak concurrent connections observed in one instance
      instances  instance count to evaluate (current or projected)
      waits      yes/no, whether connection waits were observed
                 (defaults to yes when max_used >= quota)
  --db-max N (required): maximum concurrent connections the database allows.
  --headroom H: spare connections a donor keeps above its peak (default 2).
  --even: ignore the quota column and start from an even split of db-max.

Outputs (text, or JSON with --json)
  - per-service buffer (quota - max_used), quota demand (quota x instances)
    and observed demand (max_used x instances)
  - totals versus db-max at one instance each and at the given instance counts
  - a deterministic rebalance proposal that moves spare connections from
    services with buffer above the headroom to services reporting waits,
    keeping the sum of per-instance quotas within db-max
Exit code 1 when scaled quota demand exceeds db-max or any service still
waits after rebalancing, else 0 (2 on input errors). Standard library only.
"""
import argparse
import csv
import json
import sys


def load(path, db_max, even):
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        need = {"service", "max_used", "instances"} | (set() if even else {"quota"})
        if not reader.fieldnames or not need <= {f.strip() for f in reader.fieldnames}:
            raise ValueError(f"{path}: header must contain {sorted(need)}")
        svcs = []
        for row in reader:
            row = {k.strip(): (v or "").strip() for k, v in row.items() if k}
            s = {"service": row["service"], "max_used": int(row["max_used"]),
                 "instances": int(row["instances"]),
                 "quota": 0 if even else int(row["quota"])}
            w = row.get("waits", "").lower()
            s["waits_reported"] = w in {"yes", "y", "true", "1"} if w else None
            svcs.append(s)
    if not svcs:
        raise ValueError(f"{path}: no services")
    if even:
        base, extra = divmod(db_max, len(svcs))
        for i, s in enumerate(sorted(svcs, key=lambda x: x["service"])):
            s["quota"] = base + (1 if i < extra else 0)
    for s in svcs:
        if s["waits_reported"] is None:
            s["waits_reported"] = s["max_used"] >= s["quota"]
    return svcs


def rebalance(svcs, db_max, headroom):
    """Greedy: needy services (waiting) get connections from the largest spare."""
    quota = {s["service"]: s["quota"] for s in svcs}
    spare_pool = db_max - sum(quota.values())  # unallocated capacity first
    needy = sorted((s for s in svcs if s["waits_reported"]), key=lambda s: s["service"])
    moves = []
    for s in needy:
        # A waiting service hit its quota, so its true need is unknown; ask for
        # headroom above the current quota (and above the observed peak).
        want = max(s["quota"], s["max_used"]) + headroom - quota[s["service"]]
        while want > 0:
            if spare_pool > 0:
                take = min(want, spare_pool)
                spare_pool -= take
                moves.append(("(unallocated)", s["service"], take))
            else:
                donors = sorted(
                    ((quota[d["service"]] - d["max_used"] - headroom, d["service"])
                     for d in svcs if not d["waits_reported"]),
                    key=lambda x: (-x[0], x[1]))
                if not donors or donors[0][0] <= 0:
                    break
                take = min(want, donors[0][0])
                quota[donors[0][1]] -= take
                moves.append((donors[0][1], s["service"], take))
            quota[s["service"]] += take
            want -= take
    unmet = [s["service"] for s in needy
             if quota[s["service"]] < max(s["quota"], s["max_used"]) + headroom]
    return quota, moves, unmet


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("services", help="CSV: service,quota,max_used,instances[,waits]")
    ap.add_argument("--db-max", type=int, required=True, help="database connection limit")
    ap.add_argument("--headroom", type=int, default=2, help="spare kept above peak (default 2)")
    ap.add_argument("--even", action="store_true", help="start from an even split of db-max")
    ap.add_argument("--json", action="store_true", help="emit JSON")
    a = ap.parse_args()
    try:
        svcs = load(a.services, a.db_max, a.even)
    except (OSError, ValueError, KeyError) as e:
        print(f"input error: {e}", file=sys.stderr)
        return 2

    for s in svcs:
        s["buffer"] = s["quota"] - s["max_used"]
        s["quota_demand"] = s["quota"] * s["instances"]
        s["observed_demand"] = s["max_used"] * s["instances"]
    totals = {
        "quota_sum_one_instance": sum(s["quota"] for s in svcs),
        "peak_sum_one_instance": sum(s["max_used"] for s in svcs),
        "quota_demand_scaled": sum(s["quota_demand"] for s in svcs),
        "observed_demand_scaled": sum(s["observed_demand"] for s in svcs),
        "db_max": a.db_max,
    }
    new_quota, moves, unmet = rebalance(svcs, a.db_max, a.headroom)
    rebalanced_scaled = sum(new_quota[s["service"]] * s["instances"] for s in svcs)
    result = {"services": svcs, "totals": totals,
              "rebalance": {"quotas": new_quota, "moves": moves, "unmet": unmet,
                            "quota_demand_scaled": rebalanced_scaled}}

    if a.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"{'service':<16}{'quota':>6}{'peak':>6}{'buf':>5}{'inst':>5}"
              f"{'quotaxN':>9}{'peakxN':>8}  waits  new")
        for s in svcs:
            print(f"{s['service']:<16}{s['quota']:>6}{s['max_used']:>6}{s['buffer']:>5}"
                  f"{s['instances']:>5}{s['quota_demand']:>9}{s['observed_demand']:>8}"
                  f"  {'yes' if s['waits_reported'] else 'no ':<5}  {new_quota[s['service']]}")
        t = totals
        print(f"One instance each: quotas {t['quota_sum_one_instance']}, peaks "
              f"{t['peak_sum_one_instance']} of {a.db_max} available")
        print(f"At given instance counts: quota demand {t['quota_demand_scaled']}, "
              f"observed peak demand {t['observed_demand_scaled']} of {a.db_max}")
        if t["quota_demand_scaled"] > a.db_max:
            print(f"  OVER by {t['quota_demand_scaled'] - a.db_max}: quotas are invalid once "
                  "services scale; split the data, add capacity, or cap instances")
        for src, dst, n in moves:
            print(f"Move {n} from {src} to {dst}")
        if unmet:
            print("Still short after rebalancing: " + ", ".join(unmet))
    over = totals["quota_demand_scaled"] > a.db_max
    return 1 if over or unmet else 0


if __name__ == "__main__":
    sys.exit(main())
