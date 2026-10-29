---
name: sahp-ch07-service-granularity
description: Decides how big services should be by weighing six granularity disintegrators (scope, volatility, scalability, fault tolerance, security, extensibility) against four integrators (ACID transactions, workflow, shared domain code, data relationships), then framing the conflict as business trade-off statements. Based on Chapter 7 of Ford, Richards, Sadalage and Dehghani's "Software Architecture: The Hard Parts". Use when splitting or merging services, challenging "make it smaller" or "single responsibility" arguments, sizing microservices, or writing a granularity ADR.
---

# SAHP Chapter 7: Service Granularity

## Purpose

Once a system has been divided into parts (modularity), the hard question is how large each part should be (granularity). This skill replaces opinion-driven debates ("micro means small", "it is a separate thing") with an evidence-based balance: disintegrators justify splitting, integrators justify keeping or merging, and the business chooses between the competing benefits. Apply it whenever an agent proposes, reviews or challenges a service boundary.

## Key decision rules

1. **Granularity is about behavior, not code size.** Measure size with statement counts and public operation counts, tracked over time; never with class or line counts.
2. **Always evaluate both forces.** Listing only reasons to split is the classic mistake. The right size is the equilibrium between disintegrators and integrators.
3. **Scope alone is weak evidence.** "Single responsibility" is interpretive. Split on scope only when cohesion is clearly weak (functions share just a broad noun); otherwise confirm with measurable drivers.
4. **Measure the measurable drivers.** Volatility from version-control change frequency per area; scalability from real peak load per operation group; fault tolerance from incident history; security from which operations touch regulated data.
5. **Fault-tolerance and performance gains vanish under synchronous coupling.** If the pieces must call each other to finish a request, splitting buys no request-level resilience and adds latency (example: five hops at about 300 ms each adds about 1.5 s).
6. **Check leftover cohesion with the naming test.** After carving out one function, every remaining service must have a clean, self-describing name. "Other X" or "Non-Y" services mean the cut is wrong; split further or not at all.
7. **Secure access paths, not just storage.** Sensitive data in a separate schema is not enough if routine and sensitive operations share one service.
8. **Extensibility only with a confirmed pattern.** Split per variant when new variants are planned or intrinsic to the domain (payment methods, carriers); wait when growth is speculative.
9. **A required all-or-nothing operation across the boundary argues for one service.** Confirm the atomicity requirement with the business; the alternative is compensating sagas.
10. **Request-mix rule.** Around 30 percent cross-service workflow and 70 percent atomic is usually tolerable; reversed, lean toward merging. A single latency-critical request in the workflow share can justify merging on its own. Back-end flows with no waiting user get more leeway.
11. **Shared code: domain logic only.** Infrastructure libraries (logging, auth, monitoring) never justify merging. Shared domain code does when it is a large share of the group (the book's illustration: over 40 percent), changes often, or carries fixes that must reach every consumer at once.
12. **Bidirectional data dependencies mean merge.** Assign each table to its writing service; if two services need each other's tables routinely, keep them together. Reshaping the data model just to enable a split is rarely feasible.
13. **Let the business break ties.** Translate each driver into business value and ask a product owner or sponsor which matters more now. Facilitate; do not argue to win.
14. **Mitigate the loser through design.** Internal namespaces isolate volatile code inside one service; layered security libraries (gateway plus service mesh) can protect sensitive operations without a deployment boundary. Record what remains unmitigated.

## Default workflow

1. List the candidate pieces and the operations each serves.
2. Collect evidence per piece: change frequency, peak load, incidents, sensitivity, expected new variants, statement and operation counts.
3. Evaluate the six disintegrators; apply the naming test to every proposed result.
4. Evaluate the four integrators: atomicity needs, request mix and criticality, synchronous coupling, shared domain code, table ownership (run `datamap`).
5. Run `assess` to list active drivers and draft trade-off statements.
6. Take one statement per conflict to the business owner; decide.
7. Apply design-level mitigations for the losing side and write an ADR with consequences and a revisit trigger.

## References

- [references/sizing-metrics-and-disintegrators.md](references/sizing-metrics-and-disintegrators.md): read when measuring service size or judging any reason to split, including the leftover-cohesion naming test and extensibility caution.
- [references/granularity-integrators.md](references/granularity-integrators.md): read when checking whether to keep or merge services: transactions, workflow (request-mix rule, latency math), shared domain code, and table-ownership analysis.
- [references/balancing-and-trade-off-negotiation.md](references/balancing-and-trade-off-negotiation.md): read when drivers conflict and you must frame trade-off statements, facilitate a stakeholder decision, mitigate through design, or write the ADR; includes worked examples and case-study lessons.
- [references/source-map.md](references/source-map.md): read to find which file covers a given chapter section.

## Scripts

- Run `python3 scripts/granularity_drivers.py assess worksheet.json` to compute which disintegrators and integrators are active from measured signals, a weighted lean using team-supplied weights, and the pairwise trade-off statements to bring to the business. `assess --example` prints a worksheet template; thresholds are tunable (`--volatility-ratio`, `--throughput-ratio`, `--workflow-pct`, `--shared-pct`, `--shared-changes`). The lean is an input to discussion, never the decision.
- Run `python3 scripts/granularity_drivers.py datamap spec.json` to compute table ownership under a proposed split, ownership conflicts, cross-service reads that become calls, and bidirectional dependencies (strong merge candidates). `datamap --example` prints a spec template. Add `--json` to either command for machine-readable output.
