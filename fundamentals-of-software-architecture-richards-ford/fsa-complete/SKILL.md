---
name: fsa-complete
description: Whole-book guide to Richards and Ford's "Fundamentals of Software Architecture: A Modern Engineering Approach" (2nd ed.). Use for broad architecture questions or tasks spanning several areas: trade-off analysis, modularity and components, architecture characteristics and fitness functions, choosing among monolithic and distributed styles, patterns, ADRs, risk, diagrams, teams, negotiation and ecosystem alignment. Routes to per-topic references from all 27 chapters and bundles 18 tested scripts.
---

# Fundamentals of Software Architecture, complete (Richards and Ford, O'Reilly 2nd ed.)

Operating model for software architecture condensed from the whole book. This file holds the cross-cutting rules and the router; depth lives in `references/` (chapter-prefixed topic files) and checks in `scripts/`. Theme skills (`fsa-theme-*`) cover the same material in smaller slices.

## Core rules (apply without opening references)

1. **Everything is a trade-off.** Look for the hidden cost, weight factors in context, and aim for the least-bad option.
2. **Why beats how.** Record rationale in ADRs; diagrams show structure, ADRs explain it.
3. **Decisions sit on spectrums.** Place each one deliberately rather than choosing an extreme.
4. **Characteristics drive structure.** Keep a short, measurable list; scope it per quantum; govern it with fitness functions.
5. **Logical before physical.** Identify components by role, measure cohesion and coupling, and keep modularity from decaying.
6. **Style follows analysis.** Decide monolith versus distributed from quanta, then data placement, then synchronous versus asynchronous; match the system's shape to the problem's shape.
7. **Distribution is never free.** Account for the fallacies, avoid distributed transactions, and govern coupling between services.
8. **Reuse plumbing, not domain logic.** Reuse creates coupling; domain code changes fastest.
9. **Make risk visible.** Score impact times likelihood, risk storm with the team, and negotiate mitigation cost with budget holders.
10. **Architecture is a people job.** Right-size your involvement, negotiate with evidence, lead by example, and align implementation, infrastructure, data, teams and business context.

## Map of the book

| Area | Question | Theme skill | Chapters |
|---|---|---|---|
| Thinking | How do architects reason and divide systems? | fsa-theme-architectural-thinking | 1, 2, 3, 8, 27 |
| Characteristics | What must the system be good at, measurably and where? | fsa-theme-architecture-characteristics | 4 to 7 |
| Style choice | What do styles cost, how do I choose, which patterns help? | fsa-theme-style-foundations-and-selection | 9, 19, 20 |
| Monoliths | Layered, modular monolith, pipeline or microkernel? | fsa-theme-monolithic-styles | 10 to 13 |
| Distributed | Service-based, event-driven, space-based, SOA or microservices? | fsa-theme-distributed-styles | 14 to 18 |
| Documentation | How do I decide, assess risk and draw it? | fsa-theme-decisions-risk-diagrams | 21 to 23 |
| People | How do I lead teams, negotiate and align the ecosystem? | fsa-theme-teams-and-leadership | 24 to 26 |

For an end-to-end architecture playbook, a symptom-to-fix map and a review checklist, read [references/architecture-playbook.md](references/architecture-playbook.md).

## Default workflow

1. Place the task in an area above. If it spans areas, start with [references/architecture-playbook.md](references/architecture-playbook.md).
2. Apply the core rules; open only the references whose "read when" line matches.
3. Run the matching script whenever a measurable or structural check applies.
4. State assumptions, the trade-offs considered and which rule or reference drove each recommendation.

<!-- BEGIN GENERATED: run tools/build_bundles.py to refresh -->

## References by chapter

Each link is one level deep; read only the files whose description matches the task.

### CH01: Introduction

- [ch01-architect-expectations-playbook.md](references/ch01-architect-expectations-playbook.md): read when separating architectural from technical decisions, planning compliance or vitality reviews, assessing an architect's skills, or handling stakeholder pushback and politics.
- [ch01-architecture-definition-and-context.md](references/ch01-architecture-definition-and-context.md): read when scoping an architecture, explaining what "architecture" includes, ordering the analysis, or arguing that context determines the right answer; also covers the book's three-part structure.
- [ch01-laws-and-trade-off-analysis.md](references/ch01-laws-and-trade-off-analysis.md): read when evaluating options, challenging "best practice" or "no downside" claims, writing decision rationale, or resisting one-size-fits-all standards.

### CH02: Architectural Thinking

- [ch02-architecture-vs-design.md](references/ch02-architecture-vs-design.md): read when deciding whether a choice is architectural or design-level, who should own it, or how much rigor it deserves.
- [ch02-hands-on-coding-balance.md](references/ch02-hands-on-coding-balance.md): read when an architect asks how much to code, what to code, or how to stay technical without slowing the team.
- [ch02-technical-breadth-and-radar.md](references/ch02-technical-breadth-and-radar.md): read when planning learning, advising a developer becoming an architect, building a personal technology radar, or spotting Frozen Caveman reasoning.
- [ch02-trade-off-analysis.md](references/ch02-trade-off-analysis.md): read when comparing options, writing a recommendation, translating business drivers into characteristics, or needing the worked messaging example (shared topic versus per-consumer queues).

### CH03: Modularity

- [ch03-cohesion-and-lcom.md](references/ch03-cohesion-and-lcom.md): read when deciding where an operation belongs, labeling cohesion levels, computing or interpreting LCOM, or auditing utility classes before a restructure.
- [ch03-connascence.md](references/ch03-connascence.md): read when naming a coupling problem precisely, reviewing cross-boundary contracts, choosing a refactoring toward weaker coupling, or estimating migration cost from shared state and ordering assumptions.
- [ch03-coupling-metrics-and-main-sequence.md](references/ch03-coupling-metrics-and-main-sequence.md): read when computing or interpreting Ca, Ce, abstractness, instability or distance from the main sequence, explaining the zones of pain and uselessness, or turning metrics into governance checks.
- [ch03-modularity-granularity-and-packaging.md](references/ch03-modularity-granularity-and-packaging.md): read when someone proposes splitting or merging modules or services, confuses modularity with granularity, asks about packaging, namespaces or logical versus physical separation, or needs the historical context for module mechanisms.

### CH04: Architectural Characteristics Defined

- [ch04-characteristics-catalog.md](references/ch04-characteristics-catalog.md): read when you need definitions and examples per category (operational, structural, cloud, cross-cutting), the ISO-style families, ambiguous term pairs, or guidance on building a glossary.
- [ch04-qualifying-characteristics.md](references/ch04-qualifying-characteristics.md): read when deciding whether a specific concern is an architecture characteristic, explaining implicit vs. explicit, or arguing about terminology (non-functional requirements, quality attributes).
- [ch04-trade-offs-least-worst.md](references/ch04-trade-offs-least-worst.md): read when pruning a list, explaining why characteristics cannot all be maximized, framing a least-worst decision, or reviewing an analysis with self-check questions.

### CH05: Identifying Architectural Characteristics

- [ch05-elicitation-and-translation.md](references/ch05-elicitation-and-translation.md): read when extracting characteristics from business goals or requirements, decomposing a composite goal, separating explicit from implicit, or distinguishing scalability, elasticity and performance.
- [ch05-katas-and-requirement-walkthrough.md](references/ch05-katas-and-requirement-walkthrough.md): read when running or simulating an architecture kata, doing a requirement-by-requirement analysis, or deciding whether a characteristic belongs in architecture or design.
- [ch05-limiting-and-prioritizing.md](references/ch05-limiting-and-prioritizing.md): read when the candidate list is too long, when facilitating a stakeholder prioritization session with the worksheet, or when choosing the top three.

### CH06: Measuring and Governing Architecture Characteristics

- [ch06-defining-and-measuring-characteristics.md](references/ch06-defining-and-measuring-characteristics.md): read when a characteristic is vague or disputed, when choosing operational or process metrics (latency statistics, performance budgets, page weight, coverage, deployability), or when building a shared glossary.
- [ch06-fitness-functions-and-governance.md](references/ch06-fitness-functions-and-governance.md): read when designing architecture governance, writing cycle, layer or main-sequence fitness functions, handling metric gaming, or planning chaos-style production checks.
- [ch06-structural-metrics-and-complexity.md](references/ch06-structural-metrics-and-complexity.md): read when assessing code structure, computing or interpreting Cyclomatic Complexity, setting CC thresholds, or reviewing AI-generated code for accidental complexity.

### CH07: The Scope of Architectural Characteristics

- [ch07-architecture-quantum-and-coupling.md](references/ch07-architecture-quantum-and-coupling.md): read when defining or testing a quantum, classifying a coupling (semantic, implementation, static, dynamic), or explaining brittleness and why code metrics miss scope.
- [ch07-communication-and-dynamic-coupling.md](references/ch07-communication-and-dynamic-coupling.md): read when a sync call joins services with different scalability, availability or performance profiles, or when weighing a queue as a buffer.
- [ch07-scoping-decision-playbook.md](references/ch07-scoping-decision-playbook.md): read when choosing monolith vs distributed, sizing quanta, picking persistence and communication, working a kata like Going Green, or scoping cloud-hosted systems.

### CH08: Component-Based Thinking

- [ch08-component-coupling.md](references/ch08-component-coupling.md): read when measuring afferent/efferent coupling, looking for temporal coupling, or applying the Law of Demeter with a worked redistribution example.
- [ch08-logical-architecture-and-identification.md](references/ch08-logical-architecture-and-identification.md): read when defining components from code, contrasting logical and physical views, seeding components (Workflow, Actor/Action), diagnosing the Entity Trap, or assigning user stories.
- [ch08-refining-components.md](references/ch08-refining-components.md): read when judging cohesion, splitting for architecture characteristics, planning ongoing restructuring, or using the auction case study pattern and trade-off framing.

### CH09: Foundations of Architecture Styles

- [ch09-distributed-fallacies.md](references/ch09-distributed-fallacies.md): read when evaluating any distributed design; contains all eleven fallacies with mitigations, stamp-coupling remedies, a compensation-failure code sketch, and a pre-distribution checklist.
- [ch09-styles-and-lineage.md](references/ch09-styles-and-lineage.md): read when defining or comparing styles versus patterns, diagnosing or rescuing a Big Ball of Mud, explaining client/server or three-tier history, or arguing for simplicity as future-proofing.
- [ch09-team-topologies.md](references/ch09-team-topologies.md): read when mapping stream-aligned, enabling, complicated-subsystem and platform teams onto an architecture, or when framing style choice by sweet spot.
- [ch09-top-level-partitioning.md](references/ch09-top-level-partitioning.md): read when choosing technical versus domain partitioning, aligning teams via Conway's Law, or walking through the Silicon Sandwiches kata and an invented worked example.

### CH10: Layered Architecture Style

- [ch10-layer-design-and-isolation.md](references/ch10-layer-design-and-isolation.md): read when designing or reviewing the layer stack, deciding open vs closed layers, adding a layer, or diagnosing pass-through (sinkhole) overhead.
- [ch10-operations-governance-and-teams.md](references/ch10-operations-governance-and-teams.md): read when dealing with data topology, cloud or hybrid placement, availability and fault-tolerance risk, writing layer fitness functions, or aligning teams to the style.
- [ch10-style-fit-and-tradeoffs.md](references/ch10-style-fit-and-tradeoffs.md): read when deciding whether to use layering at all, explaining its strengths and weaknesses qualitatively, planning a future migration, or using OS and network-stack analogies.

### CH11: The Modular Monolith Architecture Style

- [ch11-fit-teams-and-example.md](references/ch11-fit-teams-and-example.md): read when deciding whether to adopt the style, explaining its strengths and weaknesses, aligning team topologies, or wanting a worked example and review questions.
- [ch11-risks-and-governance.md](references/ch11-risks-and-governance.md): read when reviewing an existing modular monolith, writing fitness functions, setting a coupling budget, or deciding how to remediate boundary erosion or size problems.
- [ch11-structure-and-communication.md](references/ch11-structure-and-communication.md): read when laying out namespaces, choosing single code base vs separate artifacts, picking direct calls vs a mediator, choosing a data topology, or assessing cloud deployment.

### CH12: Pipeline Architecture Style

- [ch12-fit-tradeoffs-and-examples.md](references/ch12-fit-tradeoffs-and-examples.md): read when deciding whether to use the style, explaining its qualitative strengths and weaknesses, comparing it to alternatives, or needing worked examples (telemetry routing, ETL, EDI, integration frameworks) and review questions.
- [ch12-risks-governance-and-teams.md](references/ch12-risks-governance-and-teams.md): read when assessing risks (overloaded filters, bidirectional pipes, error handling, contract drift), setting up role-tagging governance, or mapping team topologies onto a pipeline.
- [ch12-topology-filters-and-pipes.md](references/ch12-topology-filters-and-pipes.md): read when designing or reviewing the structure: filter roles in depth, compositional reuse, pipe rules, data topologies, monolithic versus distributed and cloud deployment options (step-function workflows, serverless, containers).

### CH13: Microkernel Architecture Style

- [ch13-core-plugin-design.md](references/ch13-core-plugin-design.md): read when designing or reviewing the core, plug-in packaging, binding mode, remote plug-ins, registry, contracts or data ownership.
- [ch13-fit-tradeoffs-and-use-cases.md](references/ch13-fit-tradeoffs-and-use-cases.md): read when deciding whether to use the style, explaining its characteristic profile, placing a system on the microkern-ality spectrum, choosing cloud placement, or looking for analogous examples.
- [ch13-risks-governance-teams.md](references/ch13-risks-governance-teams.md): read when auditing an existing plug-in system, writing fitness functions, handling plug-in dependencies, or organizing teams around core and plug-ins.

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

### CH19: Choosing the Appropriate Architecture Style

- [ch19-case-studies.md](references/ch19-case-studies.md): read for worked examples of the reasoning: a small customizable monolith (modular monolith vs microkernel with BFF adapters) and a high-scale auction system (microservices with selective async and five quanta).
- [ch19-style-determinations.md](references/ch19-style-determinations.md): read when actually choosing: shape matching (isomorphism) with fit/misfit heuristics, the monolith/data/communication determinations in detail, and the expected deliverables.
- [ch19-trends-and-prerequisites.md](references/ch19-trends-and-prerequisites.md): read when evaluating whether to adopt a trending style or tool, or when checking that enough context exists before recommending any style (the six prerequisite factors with probing questions).

### CH20: Architectural Patterns

- [ch20-broker-infrastructure-patterns.md](references/ch20-broker-infrastructure-patterns.md): read when deciding how many message brokers to run, who owns them, and how services discover topics.
- [ch20-communication-patterns.md](references/ch20-communication-patterns.md): read when choosing between orchestration and choreography for a workflow, or evaluating CQRS for a data path.
- [ch20-patterns-vs-styles-and-reuse.md](references/ch20-patterns-vs-styles-and-reuse.md): read when distinguishing pattern vs style vs tool vs "best practice", or when designing reuse of operational concerns (Hexagonal, Sidecar, Service Mesh, orthogonal coupling).

### CH21: Architectural Decisions

- [ch21-adr-practice-storage-and-ai.md](references/ch21-adr-practice-storage-and-ai.md): read when deciding where ADRs live, turning standards into ADRs, documenting an existing system, or using generative AI to assist a decision.
- [ch21-adr-structure-and-authoring.md](references/ch21-adr-structure-and-authoring.md): read when writing or reviewing an ADR, setting status and supersession links, defining approval criteria, or designing a compliance check; includes an invented full example and a checklist.
- [ch21-decision-antipatterns-and-significance.md](references/ch21-decision-antipatterns-and-significance.md): read when a team is stalling, re-debating or losing decisions, when choosing a business justification, or when judging whether something is architectural at all.

### CH22: Analyzing Architecture Risk

- [ch22-mitigation-patterns-and-case-study.md](references/ch22-mitigation-patterns-and-case-study.md): read when choosing mitigations for availability, elasticity, security or third-party risk, or when you need a worked end-to-end example.
- [ch22-risk-matrix-and-assessment.md](references/ch22-risk-matrix-and-assessment.md): read when scoring a single risk, building or presenting a criteria-by-context assessment, filtering it for stakeholders, or adding trend direction.
- [ch22-risk-storming-playbook.md](references/ch22-risk-storming-playbook.md): read when planning, facilitating or reviewing a risk-storming session, resolving disagreements, negotiating mitigation cost, setting cadence, or scoring user-story risk in grooming.

### CH23: Diagramming Architecture

- [ch23-standards-and-visual-guidelines.md](references/ch23-standards-and-visual-guidelines.md): read when choosing between UML, C4 and ArchiMate, setting an organizational standard, or drawing or reviewing a diagram against the titles, lines, shapes, labels, color and keys guidelines (contains the review checklist).
- [ch23-tools-fidelity-and-layers.md](references/ch23-tools-fidelity-and-layers.md): read when deciding how polished an artifact should be, diagnosing artifact attachment, choosing tool features, structuring layers, or mapping layers and stencils onto diagrams-as-code.
- [ch23-views-and-representational-consistency.md](references/ch23-views-and-representational-consistency.md): read when planning a multi-view explanation, a slide sequence, or a detail diagram that needs context; includes a worked zoom example and pre-presentation checklist.

### CH24: Making Teams Effective

- [ch24-checklists-for-teams.md](references/ch24-checklists-for-teams.md): read when drafting or reviewing a definition of done, test checklist or release checklist, or when checklists are being ignored.
- [ch24-collaboration-and-architect-personalities.md](references/ch24-collaboration-and-architect-personalities.md): read when the architect-team relationship is strained, when deciding what level of detail an architect should specify, or to diagnose control-freak or armchair behavior; includes diagnostic questions.
- [ch24-design-principles-guidance.md](references/ch24-design-principles-guidance.md): read when setting library or technology decision rights, handling a developer pushing a new technology, or generalizing tiered decision rights to other areas.
- [ch24-elastic-leadership-involvement.md](references/ch24-elastic-leadership-involvement.md): read when deciding how involved to be with a team or how many teams one architect can carry; includes invented scored examples and caveats.
- [ch24-team-warning-signs.md](references/ch24-team-warning-signs.md): read when a team seems too large, someone proposes adding headcount, meetings hide disagreement, or work is being dropped.

### CH25: Negotiation and Leadership Skills

- [ch25-leadership-principles.md](references/ch25-leadership-principles.md): read when reviewing a design for accidental complexity, balancing vision with practicality, rephrasing directives, framing requests as favors, or advising on greetings, boundaries and mentoring.
- [ch25-negotiation-playbook.md](references/ch25-negotiation-playbook.md): read when preparing for any negotiation with stakeholders, other architects or developers; includes ordered techniques, invented examples, pitfalls and a pre-negotiation checklist.
- [ch25-team-integration-and-meetings.md](references/ch25-team-integration-and-meetings.md): read when an architect is overloaded with meetings, disconnected from the team, protecting developer flow, or working with remote teams; includes a weekly calendar audit procedure.

### CH26: Architectural Intersections

- [ch26-data-topology-alignment.md](references/ch26-data-topology-alignment.md): read when choosing a database topology or database types, or when data shape or read/write balance seems to fight the style.
- [ch26-generative-ai-intersection.md](references/ch26-generative-ai-intersection.md): read when embedding an LLM into a system or when deciding how far to trust AI help on architecture decisions.
- [ch26-implementation-and-infrastructure-alignment.md](references/ch26-implementation-and-infrastructure-alignment.md): read for the nine-intersection audit table, code versus design conflicts, structural governance, constraint definition, and infrastructure or cloud deployment mismatches.
- [ch26-organizational-and-business-alignment.md](references/ch26-organizational-and-business-alignment.md): read when assessing engineering practices, fitness functions for agility, team structure, external integrations, enterprise standards, business direction, unknown unknowns or residuality theory.

### CH27: The Laws of Software Architecture, Revisited

- [ch27-hidden-trade-offs-and-reuse.md](references/ch27-hidden-trade-offs-and-reuse.md): read when someone proposes a "pure win", pushes for broad code reuse, asks for both decoupling and reuse, or wants a one-time decision to become a standing rule.
- [ch27-trade-off-analysis-method.md](references/ch27-trade-off-analysis-method.md): read when running a concrete trade-off analysis, building or weighting a factor matrix, or working through shared library vs shared service and queue vs topic; includes the Out of Context antipattern and an invented worked example.
- [ch27-why-and-spectrum-thinking.md](references/ch27-why-and-spectrum-thinking.md): read when documenting rationale, deciding whether something is architecture or design, framing a choice as a spectrum, coaching on uncertainty, or setting up practice katas.

Merged section maps: [source-maps.md](references/source-maps.md).

## Scripts

Python 3 standard library only; run any script with `--help` for its arguments.

| Script | Purpose |
|---|---|
| `scripts/modularity_metrics.py` (ch03) | Modularity metrics calculator (Martin package metrics plus class-level LCOM). |
| `scripts/complexity_gate.py` (ch06) | Cyclomatic-complexity fitness function for Python source. |
| `scripts/dependency_fitness.py` (ch06) | Structural fitness function: dependency cycles, layer rules, main-sequence distance. |
| `scripts/quantum_finder.py` (ch07) | Find architecture quanta in a system description. |
| `scripts/component_coupling.py` (ch08) | Compute afferent (Ca) and efferent (Ce) coupling per logical component. |
| `scripts/component_lint.py` (ch08) | Flag Entity Trap names and low-cohesion responsibility statements. |
| `scripts/call_chain_budget.py` (ch09) | Estimate the cost of a chain of synchronous remote calls (fallacies 1-3). |
| `scripts/layer_rules_check.py` (ch10) | Check a layered architecture's access rules and sinkhole share. |
| `scripts/check_module_boundaries.py` (ch11) | Check modular-monolith boundaries: module membership, coupling budget, forbidden pairs. |
| `scripts/event_flow_lint.py` (ch15) | Structural lint for a choreographed event-driven architecture model. |
| `scripts/collision_rate.py` (ch16) | Estimate replicated-cache data collisions in a space-based architecture. |
| `scripts/integration_flow_guard.py` (ch17) | Integration write-direction fitness function for ESB / integration-hub logs. |
| `scripts/coupling_audit.py` (ch18) | Coupling audit for a microservices call map (governance fitness function). |
| `scripts/adr_check.py` (ch21) | Structural checks for Architectural Decision Records (ADRs) and approval routing. |
| `scripts/risk_storm.py` (ch22) | Risk scoring, risk-storming aggregation and risk-assessment tables (FSA ch. 22). |
| `scripts/involvement_score.py` (ch24) | Elastic-leadership involvement calculator (FSA Chapter 24 five-factor scale). |
| `scripts/availability_budget.py` (ch25) | Translate availability targets ("nines") into concrete downtime budgets, and back. |
| `scripts/tradeoff_matrix.py` (ch27) | Weighted trade-off matrix (FSA Chapter 27: contextual weighting of trade-offs). |

<!-- END GENERATED -->

## Provenance

Original synthesis for agent use; it does not reproduce the book's text, code, tables, rating matrices, figures or discussion questions. `references/source-maps.md` maps every chapter section to the file that covers it. This folder is regenerated from the chapter skills by `tools/build_bundles.py`.
