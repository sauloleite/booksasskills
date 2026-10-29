---
name: fsa-ch10-layered-style
description: Guidance for evaluating, designing and governing the layered (n-tier) architecture style, based on Chapter 10 of Richards and Ford's "Fundamentals of Software Architecture" (2nd ed.). Covers logical and physical layer topology, open vs closed layers, layers of isolation, the Architecture Sinkhole 80/20 check, cloud, risk, governance and team fit. Use when choosing or rejecting a layered monolith, reviewing layer dependencies, deciding which layers may be skipped, writing layer fitness functions, or diagnosing a layered system that is outgrowing itself.
---

# Layered Architecture Style (FSA Chapter 10)

Purpose: help an agent decide whether a layered (n-tier) monolith fits a problem, design its layers and access rules so change stays contained, govern those rules automatically, and recognize when the system has outgrown the style. Layering is the cheapest, most familiar style and the one teams fall into by default when nobody chooses deliberately, so the agent's main job is to make the choice and its trade-offs explicit.

## Key decision rules

1. **Make the style a decision, not an accident.** If a team "just started coding," assume they built layers by implication. Name it, record it in an ADR, and state the trade-offs.
2. **Default topology is four logical layers**: Presentation, Business, Persistence, Database. Three is fine for small apps; five or more (Rules, Services) for large ones. Logical layers are independent of deployables: one unit, UI split from backend, or everything including an embedded DB.
3. **Technical partitioning has a price.** Each domain concept spans every layer, so domain changes touch all of them. Layering suits specialist teams per technical concern, and fits poorly with DDD and domain-aligned ownership.
4. **Close the layers on the main request path.** Isolation (changes stay inside a layer while contracts hold) only works if callers cannot skip layers. Letting the UI hit Persistence directly couples both upper layers to it and makes the system brittle.
5. **Use structure to enforce a restriction.** If upper layers must not use some shared code, move it into a new layer under a closed layer, and mark the new layer open so it does not force pass-through calls.
6. **Document every open layer and why.** Undocumented access rules lead to coupling that is hard to test, maintain and deploy. Encode the map as a fitness function in CI.
7. **Measure sinkholes with the 80/20 heuristic.** Pass-through requests (no layer adds logic) are normal at about 20% of requests; near 80% the style is likely wrong. Opening all layers removes the waste but forfeits isolation.
8. **Expect size decay.** Simplicity, cost, maintainability, testability and deployability are good when small and degrade as the codebase grows.
9. **Know the hard weaknesses.** Single architecture quantum, so elasticity and scalability are capped; one failing component crashes everything; restarts take roughly 2 to 15+ minutes, hurting availability through MTTR; every change redeploys the whole unit.
10. **Choose it when** the system is small or simple, budget and time are tight, feasibility dominates, or the architecture is still undecided but work must begin. **Avoid it when** the system is or will be large, or needs independent scaling, fault isolation, or frequent low-risk deploys.
11. **Build to leave.** If starting with layers, keep reuse low, inheritance shallow, and group code by domain inside each layer so a later migration has seams.
12. **Cloud split caution.** Layers map neatly onto separate hosting, but nearly every request crosses most layers, so an on-prem to cloud boundary adds latency to almost all traffic.

## Default workflow

1. Elicit the top driving characteristics and the system's current and expected size.
2. Check fit against rule 10; if feasibility, cost or simplicity lead and size is modest, layering is a candidate.
3. Define layers top to bottom, mark each open or closed, and justify every open one.
4. Choose a physical deployment variant and, if relevant, a cloud placement; estimate cross-boundary calls per request.
5. Generate the allowed-access map and turn it into a structural test (run the script below).
6. Estimate or measure the sinkhole share; act per rule 7.
7. Record risks (MTTR, fault tolerance, scaling ceiling) and growth indicators in the ADR, along with the migration-friendly practices from rule 11.
8. Map teams: stream-aligned teams own flows end to end; enabling, complicated-subsystem and platform teams attach to specific layers.

## References

- [references/layer-design-and-isolation.md](references/layer-design-and-isolation.md): read when designing or reviewing the layer stack, deciding open vs closed layers, adding a layer, or diagnosing pass-through (sinkhole) overhead.
- [references/operations-governance-and-teams.md](references/operations-governance-and-teams.md): read when dealing with data topology, cloud or hybrid placement, availability and fault-tolerance risk, writing layer fitness functions, or aligning teams to the style.
- [references/style-fit-and-tradeoffs.md](references/style-fit-and-tradeoffs.md): read when deciding whether to use layering at all, explaining its strengths and weaknesses qualitatively, planning a future migration, or using OS and network-stack analogies.
- [references/source-map.md](references/source-map.md): read to find which file covers a given chapter section.

## Scripts

Run `python3 scripts/layer_rules_check.py --spec layers.json --emit-allowed` to compute which layer may call which from the ordered open/closed flags and to flag observed dependencies that call upward or skip a closed layer (exit code 1 on violations, so it can gate CI). The spec holds `layers` (top to bottom, each `{"name", "open"}`), optional `dependencies` (`{"from", "to", "count"}`) and optional `requests` (`{"total", "pass_through"}`).

Run `python3 scripts/layer_rules_check.py --total 60 --pass-through 41` to compute the sinkhole share and classify it against the 20% and 80% bands.

Add `--json` for machine-readable output.
