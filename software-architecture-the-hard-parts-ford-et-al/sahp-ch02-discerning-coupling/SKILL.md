---
name: sahp-ch02-discerning-coupling
description: Untangles coupling before any distributed-architecture trade-off: the architecture quantum (independently deployable, functionally cohesive, statically coupled unit), static coupling via the bootstrap test, and dynamic coupling along communication, consistency and coordination with the eight named saga combinations. Based on Chapter 2 of Ford, Richards, Sadalage and Dehghani's "Software Architecture: The Hard Parts". Use when sizing services, counting real quanta, spotting shared database, mediator or UI coupling, choosing sync vs async calls, or framing a trade-off analysis.
---

# Discerning Coupling in Software Architecture

## Purpose

Generic advice says "decouple", yet a system with no coupling does nothing. Once microservices pulled each database inside a service boundary, transactions and workflows became architecture problems, and decisions about service size and communication stopped having universal answers. This skill gives the agent the chapter's vocabulary and procedure for separating the forces before weighing them: define coupling by change impact, find real architecture quanta through static coupling, characterize each runtime interaction by its three dynamic forces, and only then assess trade-offs. It is the foundation the rest of the book builds on (decomposition, data ownership, granularity, sagas, contracts).

## Key decision rules (apply without opening references)

1. **Coupling means change impact.** Two parts are coupled if changing one may force a change in the other. Ask this of every pair in scope.
2. **Untangle before you trade off.** Step 1: find the entangled parts. Step 2: classify how each pair is coupled (static or dynamic; for dynamic, the three forces). Step 3: assess options by the impact of change. Refuse tool-versus-tool comparisons until step 2 is done.
3. **No best practice, only least worst.** Present options with what each buys and costs for this context; never give a context-free recommendation on granularity or communication.
4. **Coupling is a dose.** Too-fine services push pain into transactions, orchestration and asynchrony; too-coarse services hurt scale and deployment. Tune, do not minimize.
5. **A quantum must pass all four tests:** independently deployable, high functional cohesion (roughly one bounded context), high internal static coupling (it carries everything it needs to run), and runtime interaction with other quanta through dynamic coupling, where synchronous calls can bind them.
6. **Bootstrap test for static coupling:** list everything needed to start and operate the unit from nothing (runtime, frameworks, transitive libraries, data store, broker presence, platform, required services, bound UI). Shared items that force joint change or deployment fuse units into one quantum.
7. **Holistic coupling points collapse quanta.** A shared database (especially one with its own release cadence), a central mediator, or a tightly coupled UI makes everything attached to it one quantum. Distributed topology makes multiple quanta possible, never guaranteed.
8. **Count quanta, not services.** Monoliths, service-based architecture and mediator event-driven designs are one quantum; broker event-driven with a shared database is still one; only separated data and no shared coupling points yield many.
9. **Static coupling scopes operational characteristics.** Scale, elasticity, availability and security targets apply per quantum; fused services share them.
10. **Broker presence is static; messages through it are dynamic.** Measure static coupling from build artifacts, dynamic coupling continuously from runtime telemetry.
11. **Dynamic coupling has three interlocking forces:** communication (sync or async), consistency (atomic or eventual), coordination (orchestrated or choreographed). Choosing one shifts the others: atomicity is easiest with sync plus an orchestrator; peak scale comes from async, eventual, choreographed.
12. **Sync calls temporarily fuse quanta.** A synchronous call across quanta with different elasticity or scale makes the caller inherit the callee's limits; use an async buffer when profiles differ.
13. **Avoid cross-service atomic transactions** where possible; pairing atomicity with async communication is fragile, worse without an orchestrator.
14. **Use the micro-frontend pattern** (each service supplies its own UI fragment, loosely connected) when the UI would otherwise collapse independent services into one quantum.

## Default workflow

1. Restate the decision and list every element involved (services, stores, brokers, UIs, orchestrators, shared libraries, workflows).
2. For each service, run the bootstrap test and record dependencies; flag shared ones and decide whether each truly forces joint change.
3. Compute static quanta (use the script) and compare with what the team believes.
4. For each workflow interaction, record communication, consistency and coordination; name the combination.
5. Mark sync calls that cross quanta with differing characteristics, and atomic requirements that span quanta.
6. Generate two or more candidate designs; for each, trace change impact and which characteristics become shared or independent.
7. Recommend the least-worst option with explicit trade-offs and what to monitor at runtime.

## References

- [references/trade-off-analysis-framing.md](references/trade-off-analysis-framing.md): read when framing a trade-off discussion, explaining why microservices made decisions harder, applying the three-step method, or answering "how big should this service be".
- [references/architecture-quantum-static-coupling.md](references/architecture-quantum-static-coupling.md): read when testing whether something is a quantum, counting quanta in a topology, handling shared databases, mediators, UIs or micro-frontends, or building a static quantum diagram of a legacy estate.
- [references/dynamic-coupling-dimensions.md](references/dynamic-coupling-dimensions.md): read when choosing sync vs async, atomic vs eventual, orchestration vs choreography, naming a saga combination, or diagnosing runtime entanglement between services with different scale profiles.
- [references/source-map.md](references/source-map.md): read to find which reference covers a given chapter section.

## Scripts

- `scripts/quantum_coupling.py`: run `python3 scripts/quantum_coupling.py system.json` to compute static quanta (shared fusing dependencies, shared deploy units, bootstrap service dependencies), each call's dynamic coordinates with its pattern name and a 0 to 3 tightening count, runtime quanta fused by synchronous calls, and warnings (async plus atomic, atomic without orchestrator, cross-quantum transactions, sync calls across differing characteristics). Add `--json` for machine-readable output; the JSON schema is in the script's docstring.
