#!/usr/bin/env python3
"""Coordination-overhead estimator for multiagent topologies (stdlib only, deterministic).

Rough, assumption-explicit model of what each coordination style costs per task,
following the trade-offs in Chapter 8 of "Building Applications with AI Agents":
single agent (no inter-agent traffic), manager (hub and spoke), hierarchical
(tree, path through several levels), democratic (all-to-all consensus rounds)
and swarm (local neighbor exchanges).

Subcommands
  compare       Table for one agent count N.
                Inputs: --agents, --latency (s per model call), --cost ($ per call),
                --msg-latency (s per network hop), --fanout (specialists per task,
                manager), --parallel, --branching (hierarchy), --rounds
                (democratic/swarm), --neighbors (swarm).
                Output: model calls, inter-agent messages, sequential calls on the
                critical path, estimated latency (s), estimated cost ($), and the
                largest number of direct links any single agent must handle.
  sweep         Same model for several agent counts (--agents-list 3,5,10,20),
                showing how messages and calls grow per topology.
  actor-critic  Expected rounds, model calls, latency, cost and acceptance
                probability for an actor-critic loop with per-round acceptance
                probability --p and hard cap --max-rounds (rounds assumed
                independent; feedback usually raises p, so this is conservative).

Model assumptions (all per task):
  single        1 call, 0 messages.
  manager       1 routing call + f specialist calls (+1 synthesis call if f > 1);
                2f messages; specialists sequential unless --parallel.
  hierarchical  N agents in a tree with branching b; task routed root to one leaf
                through d manager levels: d + 1 calls, 2d messages.
  democratic    R rounds, every agent calls the model and sends to all N-1 peers.
  swarm         R rounds, every agent calls the model and sends to k neighbors.

Democratic and swarm latency assume every agent in a round runs fully in parallel
and ignore the longer prompts caused by reading peer messages: treat them as lower
bounds. Use the numbers for relative comparison and capacity planning, not as forecasts.
"""
import argparse
import sys


def tree_depth(n_agents, branching):
    """Smallest number of manager levels d so a b-ary tree of depth d holds n agents."""
    if n_agents <= 1:
        return 0
    depth, capacity, level_size = 0, 1, 1
    while capacity < n_agents:
        depth += 1
        level_size *= branching
        capacity += level_size
    return depth


def estimate(n, a):
    """Return list of dict rows, one per topology, for n agents and args a."""
    L, C, m = a.latency, a.cost, a.msg_latency
    rows = []

    rows.append(dict(topology="single", calls=1, messages=0, crit_calls=1,
                     crit_msgs=0, max_links=0))

    workers = max(n - 1, 1)
    f = max(1, min(a.fanout, workers))
    synth = 1 if f > 1 else 0
    seq_specialists = 1 if a.parallel else f
    rows.append(dict(topology="manager", calls=1 + f + synth, messages=2 * f,
                     crit_calls=1 + seq_specialists + synth,
                     crit_msgs=2 if a.parallel else 2 * f, max_links=workers))

    d = tree_depth(n, a.branching)
    rows.append(dict(topology=f"hierarchical(b={a.branching},d={d})",
                     calls=d + 1, messages=2 * d, crit_calls=d + 1, crit_msgs=2 * d,
                     max_links=min(a.branching, workers) + (1 if d > 1 else 0)))

    R = a.rounds
    rows.append(dict(topology=f"democratic(R={R})", calls=R * n,
                     messages=R * n * (n - 1), crit_calls=R, crit_msgs=R,
                     max_links=n - 1))

    k = max(0, min(a.neighbors, n - 1))
    rows.append(dict(topology=f"swarm(R={R},k={k})", calls=R * n,
                     messages=R * n * k, crit_calls=R, crit_msgs=R, max_links=k))

    for r in rows:
        r["latency_s"] = r["crit_calls"] * L + r["crit_msgs"] * m
        r["cost_usd"] = r["calls"] * C
    return rows


def print_table(rows):
    hdr = ["topology", "calls", "messages", "crit_calls", "latency_s", "cost_usd", "max_links"]
    widths = [max(len(h), *(len(fmt(r[h])) for r in rows)) for h in hdr]
    print("  ".join(h.ljust(w) for h, w in zip(hdr, widths)))
    for r in rows:
        print("  ".join(fmt(r[h]).ljust(w) for h, w in zip(hdr, widths)))


def fmt(v):
    return f"{v:.4f}" if isinstance(v, float) else str(v)


def cmd_compare(a):
    print(f"# N={a.agents} agents, {a.latency}s/call, ${a.cost}/call, "
          f"{a.msg_latency}s/hop, fanout={a.fanout}, parallel={a.parallel}")
    print_table(estimate(a.agents, a))


def cmd_sweep(a):
    ns = [int(x) for x in a.agents_list.split(",") if x.strip()]
    for n in ns:
        print(f"\n# N={n}")
        print_table(estimate(n, a))


def cmd_actor_critic(a):
    p, M = a.p, a.max_rounds
    if not 0 < p <= 1 or M < 1:
        sys.exit("need 0 < p <= 1 and max-rounds >= 1")
    q = 1 - p
    exp_rounds = sum(q ** i for i in range(M))      # P(reach round i+1) summed
    p_accept = 1 - q ** M
    calls_per_round = 2                              # one actor call + one critic call
    print(f"# actor-critic: p={p}, max_rounds={M}, {a.latency}s/call, ${a.cost}/call")
    print(f"single-shot acceptance probability : {p:.4f}")
    print(f"acceptance within cap              : {p_accept:.4f}")
    print(f"expected rounds                    : {exp_rounds:.4f}")
    print(f"expected model calls               : {calls_per_round * exp_rounds:.4f}")
    print(f"expected latency (s)               : {calls_per_round * exp_rounds * a.latency:.4f}")
    print(f"worst-case latency (s)             : {calls_per_round * M * a.latency:.4f}")
    print(f"expected cost (USD)                : {calls_per_round * exp_rounds * a.cost:.4f}")
    print(f"cost multiplier vs one actor call  : {calls_per_round * exp_rounds:.4f}x")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(sp):
        sp.add_argument("--latency", type=float, default=2.0, help="seconds per model call (default 2.0)")
        sp.add_argument("--cost", type=float, default=0.01, help="USD per model call (default 0.01)")
        sp.add_argument("--msg-latency", type=float, default=0.05, help="seconds per network hop (default 0.05)")
        sp.add_argument("--fanout", type=int, default=1, help="specialists a manager invokes per task (default 1)")
        sp.add_argument("--parallel", action="store_true", help="manager invokes specialists concurrently")
        sp.add_argument("--branching", type=int, default=4, help="direct reports per manager in hierarchy (default 4)")
        sp.add_argument("--rounds", type=int, default=2, help="consensus/interaction rounds (default 2)")
        sp.add_argument("--neighbors", type=int, default=3, help="swarm neighbors per agent (default 3)")

    c = sub.add_parser("compare", help="compare topologies for one agent count")
    c.add_argument("--agents", type=int, required=True, help="total number of agents N")
    common(c)
    c.set_defaults(func=cmd_compare)

    s = sub.add_parser("sweep", help="compare topologies across agent counts")
    s.add_argument("--agents-list", default="3,5,10,20", help="comma-separated agent counts")
    common(s)
    s.set_defaults(func=cmd_sweep)

    k = sub.add_parser("actor-critic", help="expected cost of an actor-critic loop")
    k.add_argument("--p", type=float, required=True, help="per-round acceptance probability (0-1]")
    k.add_argument("--max-rounds", type=int, default=4, help="hard cap on rounds (default 4)")
    k.add_argument("--latency", type=float, default=2.0, help="seconds per model call (default 2.0)")
    k.add_argument("--cost", type=float, default=0.01, help="USD per model call (default 0.01)")
    k.set_defaults(func=cmd_actor_critic)

    a = ap.parse_args()
    if getattr(a, "branching", 2) < 2:
        sys.exit("--branching must be >= 2")
    a.func(a)


if __name__ == "__main__":
    main()
