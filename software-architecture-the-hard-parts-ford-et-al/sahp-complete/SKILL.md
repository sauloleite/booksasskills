---
name: sahp-complete
description: Whole-book guide to "Software Architecture: The Hard Parts" (Ford, Richards, Sadalage, Dehghani) for distributed architecture decisions without best practices. Use for broad questions or tasks spanning several areas: coupling and quanta, breaking up a monolith, splitting data, service granularity, code reuse, data ownership and access, workflows, sagas, contracts, analytical data and trade-off analysis. Routes to per-topic references from all 15 chapters and bundles 13 tested scripts.
---

# Software Architecture: The Hard Parts, complete (Ford, Richards, Sadalage, Dehghani)

Operating model for the hardest decisions in distributed architectures, condensed from the whole book. This file holds the cross-cutting rules and the router; depth lives in `references/` (chapter-prefixed topic files) and checks in `scripts/`. Theme skills (`sahp-theme-*`) cover the same material in smaller slices.

## Core rules (apply without opening references)

1. **No best practices, only least-bad options.** Analyze trade-offs for this context and record them.
2. **Coupling is change impact.** Map static coupling (what a unit needs to run) and dynamic coupling (communication, consistency, coordination).
3. **Quanta set the scope of characteristics.** Shared data, mediators and synchronous calls bind services together.
4. **Split for business reasons, in order.** Check decomposability, choose component-based decomposition or tactical forking, and stop at service-based before going finer.
5. **Data is the hard part.** Split by data domain, assign ownership to writers, and choose read-access patterns deliberately.
6. **Size services by balancing forces.** Weigh disintegrators against integrators with measurements, and settle the trade-off with the business.
7. **Reuse slow-changing code, duplicate fast-changing domain code,** and use sidecars for operational concerns.
8. **Relax atomicity when you can.** Eventual consistency with explicit state management usually beats distributed atomic transactions.
9. **Coordinate on purpose.** Orchestration for complex workflows and error handling, choreography for simple high-throughput flows; keep contracts as loose as governance allows.
10. **Analytics deserves its own design.** Domain-owned data products, kept eventually consistent with their services.

## Map of the book

| Area | Question | Theme skill | Chapters |
|---|---|---|---|
| Method | How do I analyze trade-offs and coupling? | sahp-theme-tradeoff-analysis-and-coupling | 1, 2, 15 |
| Pulling code apart | Why and how do I break up the monolith? | sahp-theme-modularity-and-decomposition | 3, 4, 5 |
| Pulling data apart | How do I split the database and serve analytics? | sahp-theme-data-decomposition-and-analytics | 6, 14 |
| Service size | How big should services be, and how do they share code? | sahp-theme-granularity-and-reuse | 7, 8 |
| Distributed data | Who owns data and how do others read it? | sahp-theme-data-ownership-and-access | 9, 10 |
| Putting it back together | How do services coordinate, transact and agree on contracts? | sahp-theme-workflows-sagas-contracts | 11, 12, 13 |

For a migration playbook, a symptom-to-fix map and a review checklist, read [references/hard-parts-playbook.md](references/hard-parts-playbook.md).

## Default workflow

1. Place the task in an area above. If it spans areas, start with [references/hard-parts-playbook.md](references/hard-parts-playbook.md).
2. Apply the core rules; open only the references whose "read when" line matches.
3. Run the matching script whenever a measurable or structural check applies.
4. State assumptions, the trade-offs considered and which rule or reference drove each recommendation.

<!-- BEGIN GENERATED: run tools/build_bundles.py to refresh -->

## References by chapter

Each link is one level deep; read only the files whose description matches the task.

### CH01: What Happens When There Are No Best Practices?

- [ch01-data-vocabulary-and-running-example.md](references/ch01-data-vocabulary-and-running-example.md): read when data ownership or transactions are at stake, when classifying operational vs analytical data, when terms like coupling, contract, orchestration or atomicity need pinning down, or when assessing a struggling monolith before decomposition.
- [ch01-fitness-functions-governance.md](references/ch01-fitness-functions-governance.md): read when planning architecture governance, writing cycle, layer or load-dependent checks, deciding between a fitness function and a unit test, handling manual checks, or designing an enterprise pipeline governance stage.
- [ch01-trade-off-mindset-and-decision-records.md](references/ch01-trade-off-mindset-and-decision-records.md): read when the user wants "the best" approach, when weighing options or judging a legacy style against its historical constraints, when separating architecture from design, or when drafting or reviewing an ADR (includes a worked example).

### CH02: Discerning Coupling in Software Architecture

- [ch02-architecture-quantum-static-coupling.md](references/ch02-architecture-quantum-static-coupling.md): read when testing whether something is a quantum, counting quanta in a topology, handling shared databases, mediators, UIs or micro-frontends, or building a static quantum diagram of a legacy estate.
- [ch02-dynamic-coupling-dimensions.md](references/ch02-dynamic-coupling-dimensions.md): read when choosing sync vs async, atomic vs eventual, orchestration vs choreography, naming a saga combination, or diagnosing runtime entanglement between services with different scale profiles.
- [ch02-trade-off-analysis-framing.md](references/ch02-trade-off-analysis-framing.md): read when framing a trade-off discussion, explaining why microservices made decisions harder, applying the three-step method, or answering "how big should this service be".

### CH03: Architectural Modularity

- [ch03-change-characteristics.md](references/ch03-change-characteristics.md): read when assessing maintainability (ML formula, component metrics, change scope), testability or deployability, or when diagnosing lockstep deployments.
- [ch03-modularity-drivers-and-business-case.md](references/ch03-modularity-drivers-and-business-case.md): read when deciding whether a split is justified, choosing modular monolith vs. distributed, or writing the business case and ADR.
- [ch03-operational-characteristics.md](references/ch03-operational-characteristics.md): read when the problem is load growth, traffic spikes, MTTS, or one area taking down the rest of the system.

### CH04: Architectural Decomposition

- [ch04-decomposability-assessment.md](references/ch04-decomposability-assessment.md): read when evaluating whether a codebase can be decomposed, interpreting Ca, Ce, A, I and D values, or explaining the zones of pain and uselessness; includes a worked example and pitfalls.
- [ch04-decomposition-approaches.md](references/ch04-decomposition-approaches.md): read when choosing between component-based decomposition and tactical forking, planning a service-based stepping stone, running a tactical fork, or drafting the ADR for the choice.

### CH05: Component-Based Decomposition Patterns

- [ch05-common-domain-and-flattening.md](references/ch05-common-domain-and-flattening.md): read when deciding whether to consolidate duplicated business logic, handling orphaned classes, choosing a flattening direction, or measuring shared code.
- [ch05-component-inventory-and-sizing.md](references/ch05-component-inventory-and-sizing.md): read when cataloging components, choosing size thresholds, interpreting outliers, splitting an oversized component, or writing architecture stories.
- [ch05-dependencies-domains-and-domain-services.md](references/ch05-dependencies-domains-and-domain-services.md): read when estimating migration feasibility and effort, reducing coupling, defining component domains, or planning domain-service extraction.
- [ch05-fitness-functions-catalog.md](references/ch05-fitness-functions-catalog.md): read when automating governance in CI/CD for any of the six patterns; includes original example checks.

### CH06: Pulling Apart Operational Data

- [ch06-database-type-selection.md](references/ch06-database-type-selection.md): read when choosing a database type for a domain, comparing relational, key-value, document, column family, graph, NewSQL, cloud native or time-series stores, or designing aggregates.
- [ch06-decomposition-drivers.md](references/ch06-decomposition-drivers.md): read when deciding whether to split, weighing a specific disintegrator or integrator, doing connection or quota math, or building evidence for a skeptical data team.
- [ch06-five-step-decomposition.md](references/ch06-five-step-decomposition.md): read when defining data domains, cutting cross-domain views and FKs, using synonyms, isolating connections, or planning server migration and cutover.

### CH07: Service Granularity

- [ch07-balancing-and-trade-off-negotiation.md](references/ch07-balancing-and-trade-off-negotiation.md): read when drivers conflict and you must frame trade-off statements, facilitate a stakeholder decision, mitigate through design, or write the ADR; includes worked examples and case-study lessons.
- [ch07-granularity-integrators.md](references/ch07-granularity-integrators.md): read when checking whether to keep or merge services: transactions, workflow (request-mix rule, latency math), shared domain code, and table-ownership analysis.
- [ch07-sizing-metrics-and-disintegrators.md](references/ch07-sizing-metrics-and-disintegrators.md): read when measuring service size or judging any reason to split, including the leftover-cohesion naming test and extensibility caution.

### CH08: Reuse Patterns

- [ch08-replication-and-shared-libraries.md](references/ch08-replication-and-shared-libraries.md): read when considering copying code into services, sizing or splitting shared libraries, or designing versioning, release communication and deprecation policies.
- [ch08-reuse-value-and-platforms.md](references/ch08-reuse-value-and-platforms.md): read when someone argues for reuse as a goal, proposes a central entity service, asks how to compare all four techniques side by side, or wants the platform approach.
- [ch08-shared-services.md](references/ch08-shared-services.md): read when a shared service is proposed (including a shared data access service), to assess change risk, versioning, latency, scaling and availability, and for a worked library-versus-service analysis.
- [ch08-sidecars-and-orthogonal-reuse.md](references/ch08-sidecars-and-orthogonal-reuse.md): read when standardizing cross-cutting operational behavior, deciding what belongs in a sidecar, choosing sidecar ownership, or explaining duplicate-versus-couple and orthogonal coupling.

### CH09: Data Ownership and Distributed Transactions

- [ch09-acid-vs-base-distributed-transactions.md](references/ch09-acid-vs-base-distributed-transactions.md): read when explaining which ACID guarantees a cross-service request loses, reasoning about soft state, or deciding whether atomicity is truly required.
- [ch09-data-ownership-scenarios.md](references/ch09-data-ownership-scenarios.md): read when assigning table owners, resolving joint or common ownership, choosing between split, data domain, delegate and consolidation, or picking the delegate.
- [ch09-eventual-consistency-patterns.md](references/ch09-eventual-consistency-patterns.md): read when choosing background sync, orchestrated request-based or event-based consistency, designing compensations, durable subscriptions or DLQ handling.

### CH10: Distributed Data Access

- [ch10-choosing-and-recording.md](references/ch10-choosing-and-recording.md): read when you must pick among the patterns, run a hypothesis-based trade-off session, work through an example, or draft the ADR.
- [ch10-data-access-patterns.md](references/ch10-data-access-patterns.md): read when you need the mechanics, strengths, weaknesses, fit and pitfalls of inter-service communication, column schema replication and the shared data domain.
- [ch10-replicated-caching.md](references/ch10-replicated-caching.md): read when replicated caching is a candidate, to compare caching models, check the four limiting trade-offs, size memory and plan startup and cloud configuration.

### CH11: Managing Distributed Workflows

- [ch11-choreography-workflow-state.md](references/ch11-choreography-workflow-state.md): read when a choreographed workflow needs status tracking or shared context and you must choose between front controller, stateless choreography and stamp coupling.
- [ch11-orchestration-vs-choreography.md](references/ch11-orchestration-vs-choreography.md): read when comparing the two coordination styles, tracing error paths, mapping the choice to saga patterns, or building a scenario-by-scenario trade-off comparison and ADR.
- [ch11-semantic-vs-implementation-coupling.md](references/ch11-semantic-vs-implementation-coupling.md): read when judging whether an architecture adds avoidable complexity to a workflow, explaining technical vs domain partitioning, or justifying an orchestrator by workflow complexity.

### CH12: Transactional Sagas

- [ch12-compensation-vs-state-management.md](references/ch12-compensation-vs-state-management.md): read when deciding how a saga handles a failed step, diagnosing compensation problems (side effects, failed undo, isolation), or converting an atomic saga to eventual consistency.
- [ch12-saga-pattern-catalog.md](references/ch12-saga-pattern-catalog.md): read when choosing or critiquing a saga pattern, explaining one of the eight variants, or redesigning a slow or fragile atomic workflow.
- [ch12-saga-state-machines-and-tooling.md](references/ch12-saga-state-machines-and-tooling.md): read when modeling a saga as a state machine, writing its transition table, or setting up saga annotations and an inventory tool.

### CH13: Contracts

- [ch13-consumer-driven-contracts.md](references/ch13-consumer-driven-contracts.md): read when services own separate bounded-context models, when loose contracts need verification, or when setting up CDC tests and judging team readiness for them.
- [ch13-stamp-coupling.md](references/ch13-stamp-coupling.md): read when payloads are large or shared, when estimating bandwidth, when a consumer breaks on fields it ignores, or when choreographing a complex workflow that must carry its own state.
- [ch13-strict-vs-loose-contracts.md](references/ch13-strict-vs-loose-contracts.md): read when deciding where a contract sits on the spectrum, comparing gRPC, REST, GraphQL and name/value formats, designing a versioning policy, or assigning different strictness to edges of one workflow.

### CH14: Managing Analytical Data

- [ch14-centralized-analytics-patterns.md](references/ch14-centralized-analytics-patterns.md): read when evaluating or migrating away from a data warehouse or data lake, explaining star schemas, or diagnosing brittleness, PII and staleness in existing pipelines.
- [ch14-data-mesh-and-dpq-design.md](references/ch14-data-mesh-and-dpq-design.md): read when designing a Data Mesh, choosing DPQ types, setting coupling and communication rules, defining governance, or deciding whether mesh fits.
- [ch14-dpq-worked-example-and-fitness-functions.md](references/ch14-dpq-worked-example-and-fitness-functions.md): read when building an aggregate or ML-oriented DPQ, writing its ADR, or defining completeness and contract fitness functions.

### CH15: Build Your Own Trade-Off Analysis

- [ch15-communicating-and-staying-objective.md](references/ch15-communicating-and-staying-objective.md): read when presenting a decision to stakeholders, facing a tool champion or a forced debate, choosing between a shared topic and per-consumer queues, or adding fitness functions to guard a trial; also summarizes the chapter's framing story and epilog.
- [ch15-three-step-analysis-process.md](references/ch15-three-step-analysis-process.md): read when setting up an analysis from scratch: finding entangled dimensions, building a static coupling inventory, enumerating and rating combinations, reading matrix correlations, ordering decisions.
- [ch15-trade-off-techniques.md](references/ch15-trade-off-techniques.md): read when checking whether a comparison is valid: qualitative versus quantitative ratings, MECE candidate sets, the out-of-context trap, and escalating domain scenario modeling with an invented worked example.

Merged section maps: [source-maps.md](references/source-maps.md).

## Scripts

Python 3 standard library only; run any script with `--help` for its arguments.

| Script | Purpose |
|---|---|
| `scripts/quantum_coupling.py` (ch02) | Architecture quantum and coupling analyzer (static + dynamic). |
| `scripts/modularity_impact.py` (ch03) | Modularity impact check for a component or service dependency graph. |
| `scripts/decomposability_metrics.py` (ch04) | Compute component coupling and balance metrics to judge whether a codebase is decomposable. |
| `scripts/component_sizing.py` (ch05) | Component inventory and sizing analyzer (component-based decomposition). |
| `scripts/connection_budget.py` (ch06) | Check and rebalance per-service connection quotas against a shared database. |
| `scripts/data_domain_check.py` (ch06) | Report cross-domain database dependencies that must be broken before a split. |
| `scripts/granularity_drivers.py` (ch07) | Granularity driver worksheet for service split/merge decisions. |
| `scripts/data_ownership.py` (ch09) | Classify table ownership after a data split (single, joint, common). |
| `scripts/replicated_cache_sizing.py` (ch10) | Replicated cache memory sizing for distributed data access. |
| `scripts/saga_check.py` (ch12) | saga_check.py: lint a transactional saga definition. |
| `scripts/contract_usage.py` (ch13) | Contract field-usage analyzer: detects stamp coupling and bandwidth waste. |
| `scripts/daily_completeness_check.py` (ch14) | Daily completeness fitness function for a data product feed. |
| `scripts/tradeoff_worksheet.py` (ch15) | Weighted trade-off worksheet: options x factors, with team-supplied weights. |

<!-- END GENERATED -->

## Provenance

Original synthesis for agent use; it does not reproduce the book's text, story dialogue, code, rating tables, figures or appendix lists. `references/source-maps.md` maps every chapter section to the file that covers it. This folder is regenerated from the chapter skills by `tools/build_bundles.py`.
