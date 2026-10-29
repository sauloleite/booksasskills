---
name: fsa-theme-distributed-styles
description: Theme skill on the distributed architecture styles from Richards and Ford's "Fundamentals of Software Architecture" (2nd ed.) (chapters 14 to 18). Use when designing, reviewing or choosing among service-based, event-driven, space-based, orchestration-driven SOA and microservices architectures, sizing service granularity, choosing data topologies, designing events and payloads, handling async errors and data loss, estimating replicated-cache collisions, or governing coupling between services.
---

# Distributed styles (Fundamentals of Software Architecture, ch. 14 to 18)

Distributed styles buy scalability, elasticity, fault tolerance and evolvability at the price of complexity, cost and the fallacies of distributed computing. Each one spends that budget differently.

## Cross-chapter rules

1. **Service-based is the pragmatic default.** A handful of coarse domain services, often over a shared database split into logical domains; keeps local transactions and is a stepping stone toward finer services where needed.
2. **Event-driven trades control for responsiveness.** Separate events (facts) from messages (commands); emit derived events as extension hooks but avoid loops; choose payloads per event; protect against data loss and errors with persistent queues, acknowledgments and repair workflows. Lint flows with `scripts/event_flow_lint.py`.
3. **Space-based removes the database from the request path.** In-memory grids plus asynchronous persistence give extreme elasticity at high cost and low testability; estimate collision risk with `scripts/collision_rate.py`.
4. **Orchestration-driven SOA is mainly a lesson.** Enterprise reuse through shared services and a central bus couples everything; keep integration hubs for integration only (`scripts/integration_flow_guard.py`).
5. **Microservices put bounded contexts into physical form.** Granularity decides success: find boundaries by purpose, transactions and chattiness; prefer database per service; keep gateways free of business logic; reuse operational code via sidecars, not domain code. Audit coupling with `scripts/coupling_audit.py`.
6. **Avoid distributed transactions.** Regroup services instead; use sagas and compensation as exceptions.
7. **Governance is about coupling.** Watch shared libraries, shared databases, synchronous call chains and contract changes.
8. **Teams must match.** Domain-aligned teams fit service-based and microservices; technically split teams struggle there.

## Default workflow

1. Confirm distribution is justified and identify quanta (characteristics theme).
2. Start coarse (service-based) unless characteristics demand more, and split only volatile or high-scale domains.
3. Choose data topology and communication per boundary; design events and error handling for asynchronous parts.
4. Add coupling fitness functions and revisit granularity as the system evolves.

<!-- BEGIN GENERATED: run tools/build_bundles.py to refresh -->

## References by chapter

Each link is one level deep; read only the files whose description matches the task.

### CH14: Service-Based Architecture Style

- [ch14-characteristics-fit-and-migration.md](references/ch14-characteristics-fit-and-migration.md): read when deciding whether the style fits, explaining its strengths and weaknesses, counting quanta, studying the worked recycling example, or planning a stepping-stone migration.
- [ch14-data-topologies.md](references/ch14-data-topologies.md): read when choosing database topology, assessing schema-change impact, or fixing a shared entity library antipattern.
- [ch14-risks-governance-and-teams.md](references/ch14-risks-governance-and-teams.md): read when reviewing an existing service-based system for risk, writing fitness functions, or mapping teams and Team Topologies onto the services.
- [ch14-topology-and-service-design.md](references/ch14-topology-and-service-design.md): read when laying out services, choosing internal service design, reasoning about ACID vs. compensating updates, picking UI variants, adding a gateway, or deploying to cloud.

### CH15: Event-Driven Architecture Style

- [ch15-async-reliability-patterns.md](references/ch15-async-reliability-patterns.md): read when designing error handling, ordering after repair, loss prevention across producer, broker and consumer, or request-reply.
- [ch15-event-payload-and-granularity.md](references/ch15-event-payload-and-granularity.md): read when choosing payload style per event, estimating bandwidth, or reviewing for stamp coupling, anemic events or Swarm of Gnats.
- [ch15-mediator-and-data-topologies.md](references/ch15-mediator-and-data-topologies.md): read when deciding choreography vs mediator, choosing mediator technology, or picking a database topology.
- [ch15-style-fit-risks-and-governance.md](references/ch15-style-fit-risks-and-governance.md): read when judging style fit, describing characteristics, counting quanta, listing risks, writing fitness functions, or assessing team topology fit.
- [ch15-topology-and-event-semantics.md](references/ch15-topology-and-event-semantics.md): read when sketching flows, classifying events vs messages, or explaining derived, extensible and poison events, responsiveness vs performance, and quantum detangling.

### CH16: Space-Based Architecture Style

- [ch16-caching-models.md](references/ch16-caching-models.md): read when choosing replicated, distributed or near-cache for a unit, or sizing cache memory.
- [ch16-data-risks-and-collisions.md](references/ch16-data-risks-and-collisions.md): read when assessing data risks, computing collision rates, picking a database topology, or proposing a hybrid cloud deployment.
- [ch16-governance-teams-and-fit.md](references/ch16-governance-teams-and-fit.md): read when defining fitness functions, aligning teams, describing the style's strengths and weaknesses, quanta, or judging fit against use cases.
- [ch16-topology-and-components.md](references/ch16-topology-and-components.md): read when explaining or designing the parts (processing units, messaging grid, data grid replication mechanics, processing grid, deployment manager, pumps, writers, readers, abstraction layer).

### CH17: Orchestration-Driven Service-Oriented Architecture

- [ch17-modern-esb-integration-and-governance.md](references/ch17-modern-esb-integration-and-governance.md): read when deciding whether and how to use an ESB today, assessing cloud or hybrid integration, preventing Accidental SOA, or writing governance fitness functions.
- [ch17-reuse-coupling-and-characteristics.md](references/ch17-reuse-coupling-and-characteristics.md): read when analyzing shared or canonical services, cross-layer change cost, team-structure problems, the single-quantum argument, or the qualitative characteristics profile; includes a diagnostic checklist and review questions.
- [ch17-taxonomy-and-orchestration.md](references/ch17-taxonomy-and-orchestration.md): read when you need the historical forces, the four service layers and their granularity test, the orchestration engine's roles, message flow, the data topology, or why declarative transactions failed.

### CH18: Microservices Architecture

- [ch18-boundaries-granularity-and-transactions.md](references/ch18-boundaries-granularity-and-transactions.md): read when drawing or reviewing service boundaries, resolving granularity disputes, or deciding whether a saga is justified.
- [ch18-communication-and-infrastructure.md](references/ch18-communication-and-infrastructure.md): read when designing the API layer, sidecars, service mesh, discovery, frontends, protocols, or choreography vs orchestration.
- [ch18-data-topologies.md](references/ch18-data-topologies.md): read when choosing where data lives, handling shared tables, or arguing against a shared database.
- [ch18-risks-governance-teams-and-fit.md](references/ch18-risks-governance-teams-and-fit.md): read when assessing fit, reviewing a design for common risks, setting up coupling governance, mapping team topologies, or deploying to cloud or serverless.

Merged section maps: [source-maps.md](references/source-maps.md).

## Scripts

Python 3 standard library only; run any script with `--help` for its arguments.

| Script | Purpose |
|---|---|
| `scripts/event_flow_lint.py` (ch15) | Structural lint for a choreographed event-driven architecture model. |
| `scripts/collision_rate.py` (ch16) | Estimate replicated-cache data collisions in a space-based architecture. |
| `scripts/integration_flow_guard.py` (ch17) | Integration write-direction fitness function for ESB / integration-hub logs. |
| `scripts/coupling_audit.py` (ch18) | Coupling audit for a microservices call map (governance fitness function). |

<!-- END GENERATED -->
