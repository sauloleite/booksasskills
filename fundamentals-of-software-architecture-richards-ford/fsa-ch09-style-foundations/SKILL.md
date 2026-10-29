---
name: fsa-ch09-style-foundations
description: Foundational decision rules for architecture styles, based on Chapter 9 of Richards and Ford's "Fundamentals of Software Architecture" (2nd ed.). Covers style versus pattern, Big Ball of Mud, client/server and three-tier lineage, technical versus domain top-level partitioning, Conway's Law, monolithic versus distributed, the eleven fallacies of distributed computing, and team topologies. Use when choosing monolith versus distributed, deciding how to partition components, reviewing a plan to split a system into services, or estimating latency, availability and bandwidth of remote call chains.
---

# Architecture Style Foundations (FSA Chapter 9)

This skill gives an agent the vocabulary and screening rules that precede any choice of a specific architecture style: what a style name actually commits a system to, how the top-level partitioning decision shapes code and teams, and what every distributed design must pay for in network-related costs. Apply it before recommending a style, when reviewing a proposal to break up a monolith, and when an architecture decision record needs its trade-offs made explicit.

## Key decision rules

1. **Expand every style name into five dimensions**: component topology, physical architecture (one deployable or many), deployment granularity and cadence, communication (in-process or remote), and data topology. Confirm each; disagreements often hide in data topology. A pattern is a narrower contextual solution usable inside many styles.
2. **Style names are labels, not instructions.** "Microservices" does not mean "make services as small as possible".
3. **Structure decays without governance.** Big Ball of Mud is the default outcome of years of speed-first work; prevent it with automated structural checks (dependency rules, cycle and coupling limits), not good intentions.
4. **Decide top-level partitioning early and explicitly.** Technical (layers by capability) versus domain (components by workflow). Neither is universally right; recent industry direction favors domain. Lean domain when change requests arrive per business capability, teams are or should be cross-functional, or a later move to distributed is plausible. Lean technical when one cross-cutting concern must stay isolated and the system is small and stable. Record the accepted cost: scattered workflows (technical) or repeated cross-cutting code (domain).
5. **Classify by the top level only.** Nested layers inside domain components do not make a system technically partitioned.
6. **Check team structure against partitioning (Conway's Law).** Skill-based teams pull code toward technical layers. If the target is domain partitioning, propose matching team changes (Inverse Conway Maneuver) or expect boundaries to erode.
7. **Monolithic versus distributed is the primary style split.** Distributed styles buy scalability, availability and performance at scale but always pay the fallacy costs. Never endorse a distributed style without measured production numbers: average and p95 to p99 round-trip latency, synchronous chain depth, payload sizes, request rates.
8. **The tail decides feasibility.** Sequential hops add latency linearly, and the share of requests that hit at least one slow hop grows quickly with chain length. Availability compounds multiplicatively.
9. **Send only what the caller needs.** Stamp coupling (returning large structures for a few fields) wastes bandwidth and worsens latency and reliability.
10. **Every endpoint is an attack surface**, internal ones included; securing every hop also costs latency.
11. **Network topology, administrators and vendors are moving targets.** Establish channels with network and ops owners; alert on latency drift.
12. **Distribution costs real money** (gateways, proxies, subnets, servers). Assume the infrastructure is not already in place; analyze capacity, bandwidth, latency and security zones first.
13. **"We'll version the contract" is a decision with four open questions**: scope (service or system), reach, how many live versions, how deprecation is coordinated.
14. **Compensations can fail.** Every cross-service transactional workflow needs a path for when the update and its reversal both fail.
15. **Observability is mandatory in distributed styles**, not optional: correlation IDs, per-hop metrics, traces, centralized logs.
16. **Prefer simple designs as future-proofing.** Avoid baking a fashionable style into hard-to-change foundations (languages, wire formats, shared schemas); record the future assumptions a decision depends on.
17. **Recommend a style only by naming its sweet spot**: the characteristics it serves and those it sacrifices for this problem.

## Default workflow

1. Describe the current or proposed system on the five style dimensions.
2. Identify how change requests arrive and how teams are organized; choose top-level partitioning and note the Conway's Law implications and team types needed (stream-aligned, enabling, complicated-subsystem, platform).
3. Decide monolithic versus distributed. A modular monolith gives domain boundaries without network costs; consider it before distribution.
4. If distributed is on the table, run the pre-distribution checklist (fallacies 1 to 11) and quantify the critical call chains with the script below.
5. Write the ADR: chosen partitioning and physical architecture, measured numbers, accepted costs, and the assumptions that would trigger revisiting it.

## References

- [references/styles-and-lineage.md](references/styles-and-lineage.md): read when defining or comparing styles versus patterns, diagnosing or rescuing a Big Ball of Mud, explaining client/server or three-tier history, or arguing for simplicity as future-proofing.
- [references/top-level-partitioning.md](references/top-level-partitioning.md): read when choosing technical versus domain partitioning, aligning teams via Conway's Law, or walking through the Silicon Sandwiches kata and an invented worked example.
- [references/distributed-fallacies.md](references/distributed-fallacies.md): read when evaluating any distributed design; contains all eleven fallacies with mitigations, stamp-coupling remedies, a compensation-failure code sketch, and a pre-distribution checklist.
- [references/team-topologies.md](references/team-topologies.md): read when mapping stream-aligned, enabling, complicated-subsystem and platform teams onto an architecture, or when framing style choice by sweet spot.
- [references/source-map.md](references/source-map.md): read to locate which reference covers a given chapter heading.

## Scripts

Run `python3 scripts/call_chain_budget.py --hops 6 --avg-ms 40 --p95-ms 250 --availability 0.999 --budget-ms 800` to compute the average and pessimistic tail latency of a synchronous chain, the share of requests touching a tail-latency hop, compounded availability, and a budget pass or fail.

Run `python3 scripts/call_chain_budget.py --hops 1 --avg-ms 100 --payload-bytes 500000 --needed-bytes 200 --rps 2000` to compute bandwidth sent versus bandwidth needed and the stamp-coupling waste ratio.

Add `--json` for machine-readable output. The script assumes independent hops; treat its tail figure as an upper bound and its availability figure as an estimate.
