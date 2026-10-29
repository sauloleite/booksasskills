#!/usr/bin/env python3
"""Summarize agent spans exported as JSON lines (OTel-like) for monitoring review.

Input: a JSONL file, one span per line. Recognized fields (others ignored):
  trace_id (str, required)   name (str, required)
  start / end                epoch seconds or milliseconds (numbers), or
  start_time / end_time      ISO-8601 strings; or duration_ms directly
  status                     "OK" / "ERROR" (also accepts status.code or status_code)
  attributes                 dict; token keys read: input_tokens, output_tokens,
                             tokens, tokens.total, gen_ai.usage.input_tokens,
                             gen_ai.usage.output_tokens; plus optional
                             retry / fallback booleans and any --group-by key.

Output (stdout): per-step table with count, error rate, P50/P95/P99 latency (ms),
token totals; per-trace stats (step count, wall time, tokens, retries/fallbacks);
slowest traces; optional threshold flags. --json emits the same as JSON.

Percentiles use the nearest-rank method. Deterministic, stdlib only, no network.
"""
import argparse
import json
import math
import sys
from collections import defaultdict
from datetime import datetime

TOKEN_IN = ("input_tokens", "gen_ai.usage.input_tokens", "tokens.input")
TOKEN_OUT = ("output_tokens", "gen_ai.usage.output_tokens", "tokens.output")
TOKEN_TOTAL = ("tokens", "tokens.total", "total_tokens")


def to_ms(v):
    if v is None:
        return None
    if isinstance(v, (int, float)):
        # Heuristic: values above 1e11 are epoch ms, otherwise epoch seconds.
        return float(v) if v > 1e11 else float(v) * 1000.0
    s = str(v).replace("Z", "+00:00")
    return datetime.fromisoformat(s).timestamp() * 1000.0


def pct(sorted_vals, p):
    if not sorted_vals:
        return None
    k = max(1, math.ceil(p / 100.0 * len(sorted_vals)))
    return sorted_vals[k - 1]


def first_num(attrs, keys):
    for k in keys:
        if k in attrs and isinstance(attrs[k], (int, float)):
            return attrs[k]
    return None


def is_error(span):
    st = span.get("status", span.get("status_code"))
    if isinstance(st, dict):
        st = st.get("code", st.get("status_code"))
    return str(st).upper() in ("ERROR", "2", "STATUS_CODE_ERROR")


def load(path):
    spans = []
    fh = sys.stdin if path == "-" else open(path, encoding="utf-8")
    with fh:
        for n, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                sp = json.loads(line)
            except json.JSONDecodeError as e:
                sys.exit(f"line {n}: invalid JSON ({e})")
            if "trace_id" not in sp or "name" not in sp:
                sys.exit(f"line {n}: missing trace_id or name")
            spans.append(sp)
    return spans


def summarize(spans, group_by, top):
    steps = defaultdict(lambda: {"lat": [], "err": 0, "n": 0, "tin": 0, "tout": 0})
    traces = defaultdict(lambda: {"start": None, "end": None, "steps": 0, "errors": 0,
                                  "tokens": 0, "retries": 0, "fallbacks": 0})
    for sp in spans:
        attrs = sp.get("attributes", {}) or {}
        key = sp["name"]
        if group_by:
            key = f"{key} [{group_by}={attrs.get(group_by, '-')}]"
        s = to_ms(sp.get("start", sp.get("start_time")))
        e = to_ms(sp.get("end", sp.get("end_time")))
        dur = sp.get("duration_ms")
        if dur is None and s is not None and e is not None:
            dur = e - s
        st = steps[key]
        st["n"] += 1
        if dur is not None:
            st["lat"].append(float(dur))
        err = is_error(sp)
        st["err"] += err
        tin = first_num(attrs, TOKEN_IN) or 0
        tout = first_num(attrs, TOKEN_OUT) or 0
        if not tin and not tout:
            tin = first_num(attrs, TOKEN_TOTAL) or 0
        st["tin"] += tin
        st["tout"] += tout
        tr = traces[sp["trace_id"]]
        tr["steps"] += 1
        tr["errors"] += err
        tr["tokens"] += tin + tout
        tr["retries"] += bool(attrs.get("retry"))
        tr["fallbacks"] += bool(attrs.get("fallback"))
        if s is not None:
            tr["start"] = s if tr["start"] is None else min(tr["start"], s)
        if e is not None:
            tr["end"] = e if tr["end"] is None else max(tr["end"], e)

    step_rows = []
    for k in sorted(steps):
        st = steps[k]
        lat = sorted(st["lat"])
        step_rows.append({"step": k, "count": st["n"], "error_rate": st["err"] / st["n"],
                          "p50_ms": pct(lat, 50), "p95_ms": pct(lat, 95), "p99_ms": pct(lat, 99),
                          "input_tokens": st["tin"], "output_tokens": st["tout"]})
    trace_rows = []
    for tid in sorted(traces):
        tr = traces[tid]
        wall = None if tr["start"] is None or tr["end"] is None else tr["end"] - tr["start"]
        trace_rows.append({"trace_id": tid, "wall_ms": wall, "steps": tr["steps"],
                           "errors": tr["errors"], "tokens": tr["tokens"],
                           "retries": tr["retries"], "fallbacks": tr["fallbacks"]})
    slowest = sorted([t for t in trace_rows if t["wall_ms"] is not None],
                     key=lambda t: (-t["wall_ms"], t["trace_id"]))[:top]
    n_tr = len(trace_rows) or 1
    totals = {"spans": len(spans), "traces": len(trace_rows),
              "traces_with_error": sum(t["errors"] > 0 for t in trace_rows) / n_tr,
              "traces_with_retry": sum(t["retries"] > 0 for t in trace_rows) / n_tr,
              "traces_with_fallback": sum(t["fallbacks"] > 0 for t in trace_rows) / n_tr,
              "total_tokens": sum(t["tokens"] for t in trace_rows)}
    return {"totals": totals, "steps": step_rows, "slowest_traces": slowest, "traces": trace_rows}


def flags(rep, a):
    out = []
    for r in rep["steps"]:
        if a.max_error_rate is not None and r["error_rate"] > a.max_error_rate:
            out.append(f"step '{r['step']}' error rate {r['error_rate']:.1%} > {a.max_error_rate:.1%}")
        if a.p95_ms is not None and r["p95_ms"] is not None and r["p95_ms"] > a.p95_ms:
            out.append(f"step '{r['step']}' P95 {r['p95_ms']:.0f} ms > {a.p95_ms:.0f} ms")
    for t in rep["traces"]:
        if a.max_retries is not None and t["retries"] > a.max_retries:
            out.append(f"trace {t['trace_id']} has {t['retries']} retries > {a.max_retries}")
    return out


def fmt(v, spec):
    return "-" if v is None else format(v, spec)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("spans", help="JSONL span file, or - for stdin")
    ap.add_argument("--group-by", help="attribute to split steps by, e.g. agent.version")
    ap.add_argument("--top", type=int, default=5, help="number of slowest traces to list")
    ap.add_argument("--max-error-rate", type=float, help="flag steps above this error rate (0-1)")
    ap.add_argument("--p95-ms", type=float, help="flag steps whose P95 latency exceeds this")
    ap.add_argument("--max-retries", type=int, help="flag traces with more retries than this")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of tables")
    a = ap.parse_args()
    rep = summarize(load(a.spans), a.group_by, a.top)
    rep["flags"] = flags(rep, a)
    if a.json:
        rep.pop("traces")
        print(json.dumps(rep, indent=2, sort_keys=True))
        return
    t = rep["totals"]
    print(f"spans={t['spans']} traces={t['traces']} tokens={t['total_tokens']} "
          f"traces_with_error={t['traces_with_error']:.1%} "
          f"with_retry={t['traces_with_retry']:.1%} with_fallback={t['traces_with_fallback']:.1%}")
    print(f"\n{'step':40} {'n':>5} {'err%':>6} {'p50':>8} {'p95':>8} {'p99':>8} {'tok_in':>8} {'tok_out':>8}")
    for r in rep["steps"]:
        print(f"{r['step'][:40]:40} {r['count']:>5} {r['error_rate']*100:>6.1f} "
              f"{fmt(r['p50_ms'], '.0f'):>8} {fmt(r['p95_ms'], '.0f'):>8} {fmt(r['p99_ms'], '.0f'):>8} "
              f"{r['input_tokens']:>8} {r['output_tokens']:>8}")
    print(f"\nslowest traces:")
    for r in rep["slowest_traces"]:
        print(f"  {r['trace_id']}: {r['wall_ms']:.0f} ms, {r['steps']} steps, {r['errors']} errors, "
              f"{r['tokens']} tokens, {r['retries']} retries, {r['fallbacks']} fallbacks")
    if rep["flags"]:
        print("\nflags:")
        for f in rep["flags"]:
            print("  " + f)


if __name__ == "__main__":
    main()
