---
name: fsa-ch07-scope-of-characteristics
description: Scopes architecture characteristics with the architecture quantum (independently deployable, cohesive unit with its data) and uses that scope to pick monolithic vs distributed styles, draw service boundaries, choose persistence and sync vs async communication, and scope cloud-hosted parts. Based on Chapter 7 of Richards and Ford's "Fundamentals of Software Architecture" (2nd ed). Use when deciding whether one set of characteristics fits the whole system, finding quanta, spotting shared-database or shared-library coupling, or diagnosing failing calls between services with mismatched scalability.
---

# Scope of Architecture Characteristics (architecture quantum)

## Purpose

Older characteristic frameworks assumed one set of "-ilities" for the whole system. Modern distributed systems often need different characteristics in different parts, and code-level metrics (coupling, cohesion, complexity) cannot see the things that most constrain operational characteristics, such as the database a service depends on. This skill gives the agent the architecture quantum as the unit of scope: identify quanta, attach characteristics to each quantum rather than to the system, and let the number and shape of quanta drive style, boundary, persistence and communication decisions.

## Key decision rules (apply without opening references)

1. **Scope characteristics per quantum, not per system.** Ask "which part needs this?" before recording any characteristic.
2. **A quantum includes everything it needs to run**, including its database. A system deployed against one database is a single quantum, however many services or modules it has.
3. **Quantum tests:** deploys independently; does one purposeful thing (high functional cohesion, ideally one bounded context); has low implementation static coupling to other quanta; its communication with other quanta is recognized as dynamic coupling (synchronous calls can fuse quanta at runtime).
4. **Shared coupling points merge quanta.** Two services that depend on the same database, shared library or shared component belong to the same quantum, because a change to that point can break both.
5. **Coupling tolerance scales with scope.** In the book's words, "Higher coupling is allowed for narrower scopes": tight inside a service, loose across services. Wide-reaching tight coupling makes the architecture brittle (one field rename breaks distant callers).
6. **Semantic coupling cannot be designed away.** Domain change is requirement change; architecture only controls implementation coupling.
7. **Synchronous calls between parts with different operational characteristics are the main failure mode.** The slower or less scalable callee caps the caller. Prefer an async buffer (queue) when bursts are expected, but remember a queue only absorbs bursts, not a sustained overload.
8. **One characteristic set means monolith.** If a single set suffices, choose a monolith with a single database and move on to choosing a monolithic style.
9. **Multiple incompatible clusters mean distributed.** Let the clusters of characteristics propose the quantum boundaries; it is a first cut at granularity, refined later.
10. **In distributed designs, decide persistence (shared vs per-service) and then communication (sync vs async), and re-check quanta afterwards**, because sync choices can redraw boundaries set by static coupling.
11. **In the cloud, the provider owns part of your characteristics.** For containers, evaluate container plus orchestrator constraints; for managed building blocks, evaluate the advertised (and actually honored) capabilities of each service.

## Default workflow

1. List candidate characteristics from requirements and domain concerns.
2. Ask, for each characteristic, which capability area needs it; cluster areas whose needs agree.
3. If one cluster: monolith, single database, done. If several conflicting clusters: distributed.
4. Draw tentative quanta around clusters; check each against the quantum tests (rule 3).
5. Map static coupling (shared databases, libraries, components). Run the script to see true quanta.
6. Choose persistence: shared database (common for event-driven) or partitioned per service (microservices).
7. Choose communication between quanta; mark every synchronous edge that crosses mismatched characteristics and justify or convert it.
8. For cloud-hosted parts, add provider and orchestrator constraints to each quantum's characteristic list.
9. Record the per-quantum characteristics and the trade-offs accepted.

## References

- [references/architecture-quantum-and-coupling.md](references/architecture-quantum-and-coupling.md): read when defining or testing a quantum, classifying a coupling (semantic, implementation, static, dynamic), or explaining brittleness and why code metrics miss scope.
- [references/communication-and-dynamic-coupling.md](references/communication-and-dynamic-coupling.md): read when a sync call joins services with different scalability, availability or performance profiles, or when weighing a queue as a buffer.
- [references/scoping-decision-playbook.md](references/scoping-decision-playbook.md): read when choosing monolith vs distributed, sizing quanta, picking persistence and communication, working a kata like Going Green, or scoping cloud-hosted systems.
- [references/source-map.md](references/source-map.md): read to find which reference covers a given chapter section.

## Scripts

- `scripts/quantum_finder.py`: run `python3 scripts/quantum_finder.py system.json` to compute architecture quanta from services, their data stores, shared components and calls. It reports static quanta (shared stores and components), runtime quanta (static plus synchronous calls), sync edges that fused otherwise separate quanta, and characteristic conflicts inside each quantum. Add `--json` for machine-readable output; run with `--help` for the input schema.
