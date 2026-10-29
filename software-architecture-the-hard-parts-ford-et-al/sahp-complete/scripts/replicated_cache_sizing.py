#!/usr/bin/env python3
"""Replicated cache memory sizing for distributed data access.

Every service instance that participates in a replicated in-memory cache
(the owning service and each reader) holds a full copy of the cache, so
total memory = cache size x total instances. Feasibility drops quickly once
a single cache grows past roughly 500 MB.

Inputs (CLI):
  --record-bytes N --records M   estimate cache size from entries, or
  --cache-mb X                   give the cache size directly
  --instances NAME=COUNT ...     peak instance count per service holding it
  --threshold-mb T               per-cache size warning level (default 500)
  --overhead-pct P               padding for keys and product overhead (default 0)
  --json                         emit JSON instead of text

Output: cache size, per-service and total memory, and a verdict line.
Units: 1 KB = 1000 bytes, 1 MB = 1000 KB (decimal, matching rough estimates).
"""
import argparse
import json
import sys


def parse_instances(items):
    result = []
    for item in items:
        if "=" not in item:
            raise ValueError(f"instance spec '{item}' must look like name=count")
        name, count = item.split("=", 1)
        count = int(count)
        if count < 1:
            raise ValueError(f"instance count for '{name}' must be >= 1")
        result.append((name, count))
    return result


def size(cache_mb, instances, threshold_mb):
    total_instances = sum(c for _, c in instances)
    per_service = [
        {"service": n, "instances": c, "memory_mb": round(cache_mb * c, 3)}
        for n, c in instances
    ]
    total_mb = cache_mb * total_instances
    if cache_mb > threshold_mb:
        verdict = (f"OVER THRESHOLD: cache of {cache_mb:.1f} MB exceeds {threshold_mb} MB; "
                   "replicated caching is unlikely to be feasible")
    elif cache_mb > 0.5 * threshold_mb:
        verdict = (f"CAUTION: cache is over half the {threshold_mb} MB threshold; "
                   "verify heap per instance and growth")
    else:
        verdict = "OK: cache size is within the replicated caching comfort zone"
    return {
        "cache_mb": round(cache_mb, 3),
        "total_instances": total_instances,
        "per_service": per_service,
        "total_memory_mb": round(total_mb, 3),
        "threshold_mb": threshold_mb,
        "verdict": verdict,
    }


def main(argv=None):
    p = argparse.ArgumentParser(description="Size a replicated in-memory cache across all instances holding it.")
    p.add_argument("--record-bytes", type=float, help="approximate bytes per cached entry")
    p.add_argument("--records", type=int, help="number of cached entries")
    p.add_argument("--cache-mb", type=float, help="cache size in MB (alternative to record inputs)")
    p.add_argument("--instances", nargs="+", required=True, metavar="NAME=COUNT",
                   help="peak instances per service holding the cache, owner included")
    p.add_argument("--threshold-mb", type=float, default=500.0, help="per-cache warning size in MB (default 500)")
    p.add_argument("--overhead-pct", type=float, default=0.0, help="percent padding added to cache size (default 0)")
    p.add_argument("--json", action="store_true", help="print JSON")
    a = p.parse_args(argv)

    if a.cache_mb is not None:
        if a.record_bytes is not None or a.records is not None:
            p.error("use either --cache-mb or --record-bytes with --records, not both")
        cache_mb = a.cache_mb
    elif a.record_bytes is not None and a.records is not None:
        cache_mb = a.record_bytes * a.records / 1_000_000
    else:
        p.error("provide --cache-mb, or both --record-bytes and --records")
    cache_mb *= 1 + a.overhead_pct / 100.0

    try:
        instances = parse_instances(a.instances)
    except ValueError as e:
        p.error(str(e))

    r = size(cache_mb, instances, a.threshold_mb)
    if a.json:
        print(json.dumps(r, indent=2))
        return 0
    print(f"Cache size per instance: {r['cache_mb']} MB")
    for s in r["per_service"]:
        print(f"  {s['service']}: {s['instances']} instance(s) -> {s['memory_mb']} MB")
    print(f"Total instances: {r['total_instances']}")
    print(f"Total memory across instances: {r['total_memory_mb']} MB")
    print(r["verdict"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
