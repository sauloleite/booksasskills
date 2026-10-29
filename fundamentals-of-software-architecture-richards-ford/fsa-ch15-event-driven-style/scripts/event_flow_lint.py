#!/usr/bin/env python3
"""Structural lint for a choreographed event-driven architecture model.

Input: a JSON file describing processors, the events each one handles and
the derived events each handler emits, plus optional databases, request-reply
links, synchronous calls and payload sizing. Shape:

{
  "initiating_events": ["place_order"],
  "processors": {
    "order_placement": {"db": "orders", "handles": {"place_order": ["order_placed"]}},
    "inventory": {"db": "stock", "handles": {"order_placed": ["inventory_updated"],
                                             "stock_replenished": []}}
  },
  "request_reply": [["order_placement", "inventory"]],
  "sync_calls": [["order_placement", "shipping"]],
  "events": {"order_placed": {"payload_bytes": 500000, "rate_per_sec": 500,
                               "needed_bytes": {"inventory": 30}}}
}

Output (stdout, text or --json):
  - event-type cycles: possible poison events (loops of derived events)
  - extensible hooks: emitted events with no subscriber (informational)
  - orphan subscriptions: handled events nobody produces and not initiating
  - fan-out: handlers emitting more than --fanout derived events for one
    input (possible Swarm of Gnats; threshold is a heuristic, tune it)
  - quanta: processors grouped by shared database, request-reply or sync call
  - sync calls: listed for governance review
  - bandwidth: per-subscriber and total egress, and waste vs needed bytes

Exit code 1 if any cycle or orphan is found (usable as a fitness function),
else 0. Deterministic, stdlib only, no network.
"""
import argparse
import json
import sys


def tarjan_scc(graph):
    index, low, stack, on_stack, out = {}, {}, [], set(), []
    counter = [0]

    def visit(v):
        index[v] = low[v] = counter[0]
        counter[0] += 1
        stack.append(v)
        on_stack.add(v)
        for w in sorted(graph.get(v, ())):
            if w not in index:
                visit(w)
                low[v] = min(low[v], low[w])
            elif w in on_stack:
                low[v] = min(low[v], index[w])
        if low[v] == index[v]:
            comp = []
            while True:
                w = stack.pop()
                on_stack.discard(w)
                comp.append(w)
                if w == v:
                    break
            out.append(sorted(comp))

    for v in sorted(graph):
        if v not in index:
            visit(v)
    return out


def analyze(model, fanout_limit):
    procs = model.get("processors", {})
    initiating = set(model.get("initiating_events", []))
    produced, subscribers, graph, fanout = {}, {}, {}, []
    for p, spec in sorted(procs.items()):
        for ev_in, outs in sorted(spec.get("handles", {}).items()):
            subscribers.setdefault(ev_in, set()).add(p)
            graph.setdefault(ev_in, set())
            if len(outs) > fanout_limit:
                fanout.append({"processor": p, "on": ev_in, "emits": len(outs)})
            for ev_out in outs:
                produced.setdefault(ev_out, set()).add(p)
                graph[ev_in].add(ev_out)
                graph.setdefault(ev_out, set())

    cycles = [c for c in tarjan_scc(graph)
              if len(c) > 1 or c[0] in graph.get(c[0], ())]
    hooks = sorted(e for e in produced if e not in subscribers)
    orphans = sorted(e for e in subscribers
                     if e not in produced and e not in initiating)

    # quanta via union-find
    parent = {p: p for p in procs}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)

    by_db = {}
    for p, spec in procs.items():
        if spec.get("db"):
            by_db.setdefault(spec["db"], []).append(p)
    for members in by_db.values():
        for m in members[1:]:
            union(members[0], m)
    links = model.get("request_reply", []) + model.get("sync_calls", [])
    for a, b in links:
        union(a, b)
    groups = {}
    for p in list(parent):
        groups.setdefault(find(p), []).append(p)
    quanta = sorted(sorted(g) for g in groups.values())

    bandwidth = []
    for ev, spec in sorted(model.get("events", {}).items()):
        size, rate = spec.get("payload_bytes"), spec.get("rate_per_sec")
        if size is None or rate is None:
            continue
        subs = sorted(subscribers.get(ev, ()))
        per_sub = size * rate
        row = {"event": ev, "subscribers": len(subs),
               "per_subscriber_Bps": per_sub,
               "total_egress_Bps": per_sub * len(subs), "waste": []}
        for consumer, need in sorted(spec.get("needed_bytes", {}).items()):
            row["waste"].append({"consumer": consumer, "needed_Bps": need * rate,
                                 "ratio_sent_to_needed": round(size / need, 1) if need else None})
        bandwidth.append(row)

    return {"cycles": cycles, "extensible_hooks": hooks, "orphans": orphans,
            "fanout": fanout, "quanta": quanta,
            "sync_calls": sorted(map(list, model.get("sync_calls", []))),
            "request_reply": sorted(map(list, model.get("request_reply", []))),
            "bandwidth": bandwidth}


def human(n):
    for unit in ("B/s", "KB/s", "MB/s", "GB/s"):
        if abs(n) < 1000 or unit == "GB/s":
            return f"{n:,.1f} {unit}"
        n /= 1000.0


def print_text(r):
    print("== Event-type cycles (possible poison events; members of each loop)")
    if not r["cycles"]:
        print("  none")
    for c in r["cycles"]:
        print("  {" + ", ".join(c) + "}")
    print("== Extensible hooks (emitted, no subscriber)")
    print("  " + (", ".join(r["extensible_hooks"]) or "none"))
    print("== Orphan subscriptions (handled, never produced, not initiating)")
    print("  " + (", ".join(r["orphans"]) or "none"))
    print("== High fan-out handlers (check for Swarm of Gnats)")
    for f in r["fanout"] or [None]:
        print("  none" if f is None else f"  {f['processor']} on {f['on']}: {f['emits']} events")
    print(f"== Quanta ({len(r['quanta'])})")
    for q in r["quanta"]:
        print("  [" + ", ".join(q) + "]")
    print("== Synchronous calls to review")
    for s in r["sync_calls"] or [["none"]]:
        print("  " + " -> ".join(s))
    print("== Bandwidth")
    if not r["bandwidth"]:
        print("  no sizing data")
    for b in r["bandwidth"]:
        print(f"  {b['event']}: {human(b['per_subscriber_Bps'])} per subscriber, "
              f"{b['subscribers']} subscribers, {human(b['total_egress_Bps'])} total")
        for w in b["waste"]:
            print(f"    {w['consumer']} needs {human(w['needed_Bps'])} "
                  f"(sent/needed = {w['ratio_sent_to_needed']}x)")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("model", help="path to the JSON event-flow model")
    ap.add_argument("--fanout", type=int, default=4,
                    help="flag handlers emitting more than N events per input (default 4)")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of text")
    args = ap.parse_args()
    with open(args.model, encoding="utf-8") as fh:
        model = json.load(fh)
    r = analyze(model, args.fanout)
    if args.json:
        print(json.dumps(r, indent=2, sort_keys=True))
    else:
        print_text(r)
    sys.exit(1 if r["cycles"] or r["orphans"] else 0)


if __name__ == "__main__":
    main()
