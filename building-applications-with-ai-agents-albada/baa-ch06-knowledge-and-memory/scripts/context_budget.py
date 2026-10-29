#!/usr/bin/env python3
"""Plan a per-call context-window budget for an agent with layered memory.

Models the assembly pattern from Chapter 6 of Albada's "Building Applications
with AI Agents": a fixed system message and latest user input, an optional
reserved slice for retrieved memory (semantic experience memory or RAG hits),
and a rolling FIFO window of recent turns that fills whatever remains.

Inputs (all sizes accept a unit suffix; bare numbers are tokens):
  1200   -> 1200 tokens
  300w   -> 300 words, converted at ~0.75 words per token (ceil)
  4000c  -> 4000 characters, converted at ~4 characters per token (ceil)

  --context-length   model input ceiling for one call
  --output-reserve   tokens held back for the model's reply
  --system, --user   system message and latest user input
  --pinned           items that must never be evicted (goal, constraints)
  --memory-share     fraction of the context length reserved for memory hits
  --memory-hits      retrieved item sizes, best match first; included greedily
                     in rank order, stopping at the first that does not fit
  --turns            prior turns, oldest first; newest kept first (FIFO)
  --reclaim          give unused memory reservation back to the turn window

Output: a plain-text report (or JSON with --json) of the allocation, which
memory hits and turns are kept or evicted, and warnings. Deterministic, no I/O
beyond stdout.
"""
import argparse
import json
import math
import sys


def to_tokens(value):
    v = str(value).strip().lower()
    if v.endswith("w"):
        return math.ceil(float(v[:-1]) / 0.75)
    if v.endswith("c"):
        return math.ceil(float(v[:-1]) / 4)
    return math.ceil(float(v))


def plan(a):
    warn = []
    ctx = to_tokens(a.context_length)
    out = to_tokens(a.output_reserve)
    system, user = to_tokens(a.system), to_tokens(a.user)
    pinned = [to_tokens(x) for x in a.pinned]
    hits = [to_tokens(x) for x in a.memory_hits]
    turns = [to_tokens(x) for x in a.turns]

    fixed = out + system + user + sum(pinned)
    if fixed > ctx:
        warn.append("Fixed parts (reply reserve, system, user, pinned) exceed "
                    "the context length; shrink them before anything else.")
    free = max(0, ctx - fixed)

    mem_reserved = min(free, int(ctx * a.memory_share))
    mem_kept, mem_used = [], 0
    for i, h in enumerate(hits):
        if mem_used + h > mem_reserved:
            break
        mem_kept.append(i)
        mem_used += h
    if hits and not mem_kept:
        warn.append("Top memory hit does not fit the reserved slice; raise "
                    "--memory-share or truncate/summarize hits.")

    turn_budget = free - (mem_used if a.reclaim else mem_reserved)
    kept, used = [], 0
    for i in range(len(turns) - 1, -1, -1):
        if used + turns[i] > turn_budget:
            break
        kept.append(i)
        used += turns[i]
    kept.reverse()
    evicted = [i for i in range(len(turns)) if i not in kept]
    if turns and not kept:
        warn.append("No prior turn fits; the agent will lose all recent "
                    "conversation. Pin key facts or lower other allocations.")
    if evicted:
        warn.append(f"FIFO evicts {len(evicted)} oldest turn(s) regardless of "
                    "importance; pin anything that must survive.")

    total = fixed + mem_used + used
    return {
        "context_length": ctx,
        "fixed": {"output_reserve": out, "system": system, "user": user,
                  "pinned": sum(pinned)},
        "memory": {"reserved": mem_reserved, "used": mem_used,
                   "hits_kept": mem_kept,
                   "hits_dropped": list(range(len(mem_kept), len(hits)))},
        "turns": {"budget": turn_budget, "used": used, "kept": kept,
                  "evicted": evicted},
        "total_used": total,
        "utilization_pct": round(100 * total / ctx, 1) if ctx else 0.0,
        "warnings": warn,
    }


def main(argv=None):
    p = argparse.ArgumentParser(
        description="Allocate a context window across system prompt, pinned "
                    "facts, retrieved memory and recent turns (FIFO).")
    p.add_argument("--context-length", required=True)
    p.add_argument("--output-reserve", default="0")
    p.add_argument("--system", default="0")
    p.add_argument("--user", default="0")
    p.add_argument("--pinned", nargs="*", default=[])
    p.add_argument("--memory-share", type=float, default=0.0)
    p.add_argument("--memory-hits", nargs="*", default=[])
    p.add_argument("--turns", nargs="*", default=[])
    p.add_argument("--reclaim", action="store_true")
    p.add_argument("--json", action="store_true")
    a = p.parse_args(argv)
    if not 0.0 <= a.memory_share < 1.0:
        p.error("--memory-share must be in [0, 1)")
    r = plan(a)
    if a.json:
        print(json.dumps(r, indent=2))
        return 0
    f = r["fixed"]
    print(f"Context length:     {r['context_length']}")
    print(f"Fixed:              reply {f['output_reserve']}, system "
          f"{f['system']}, user {f['user']}, pinned {f['pinned']}")
    m = r["memory"]
    print(f"Memory slice:       reserved {m['reserved']}, used {m['used']}, "
          f"hits kept {m['hits_kept']}, dropped {m['hits_dropped']}")
    t = r["turns"]
    print(f"Recent turns:       budget {t['budget']}, used {t['used']}, "
          f"kept {t['kept']}, evicted {t['evicted']}")
    print(f"Total used:         {r['total_used']} "
          f"({r['utilization_pct']}% of context)")
    for w in r["warnings"]:
        print(f"WARNING: {w}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
