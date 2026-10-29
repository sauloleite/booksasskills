---
name: fsa-ch20-architectural-patterns
description: Applies Chapter 20 of Richards and Ford's "Fundamentals of Software Architecture" (2nd ed.) on architectural patterns as contextual solutions distinct from styles, best practices and tools. Covers separating domain from operational coupling (Hexagonal/Ports and Adapters, Sidecar, Service Mesh, orthogonal reuse), orchestration vs choreography, CQRS, and Single-Broker vs Domain-Broker infrastructure. Use when choosing or naming a pattern, standardizing cross-cutting concerns across services, designing workflow coordination, splitting reads from writes, or deciding broker topology in event-driven systems.
---

# Architectural Patterns (FSA Chapter 20)

## Purpose

This skill helps an agent reason about architectural patterns the way the chapter frames them: a pattern is a named, contextualized solution to a recurring problem, and it lives one level below an architecture style (a style is a whole topology; a pattern is a reusable move inside or across styles). The chapter's teaching device is to separate three things people routinely blur together: the pattern, the tool or framework that implements it, and the "best practice" label that discourages analysis. It then walks through representative patterns in three families (reuse, communication, infrastructure) and gives each a qualitative trade-off profile. Use the skill to identify which pattern a situation calls for, pick an implementation that fits the style in use, and state the trade-offs explicitly instead of declaring a winner.

## Key decision rules (apply even without opening references)

1. **Pattern first, implementation second.** Name the problem-solution pair (for example "separate operational from domain concerns") before choosing a product, framework or library. Tools often bundle several patterns with varying fidelity; judge them against the pattern you need.
2. **No pattern is a "best practice".** Treat every pattern as context-dependent and re-run trade-off analysis when context changes (trade-off analysis is never finished once and for all).
3. **In distributed systems, prefer duplication over coupling for domain code**, but deliberately centralize operational concerns (monitoring, logging, authN/authZ, circuit breakers). Leaving each team to wire these in independently drifts into chaos: no verifiable compliance and no coordinated upgrades.
4. **Recognize orthogonal coupling.** When a concern cuts across the primary partitioning (domains), reuse it through a cross-cutting but consistent layer (sidecar) rather than bending the domain structure around it.
5. **"Hexagonal" is ambiguous; clarify intent.** Using it as shorthand for domain/operational separation is fine. Taken literally, it treats the database as a swappable adapter, which conflicts with the microservices principle that the schema is part of the domain and moves with it. For distributed systems, implement the separation with Sidecar plus Service Mesh instead.
6. **Sidecar/Service Mesh costs:** one sidecar per platform or language, risk of the sidecar bloating, and drift if ownership is spread across teams. Decide ownership (central, per team, or hybrid) explicitly.
7. **Orchestration vs choreography is a pattern choice in any distributed style.** Favor an orchestrator as workflow complexity, error handling, recoverability and queryable state matter more. Favor choreography when responsiveness, scale, fault tolerance and decoupling dominate and the workflow is simple enough to survive without an owner.
8. **Use CQRS only when reads and writes genuinely differ** (very different volumes, separate security posture, different data models or characteristics). Expect asynchronous sync from write store to read store and plan for the staleness it implies.
9. **Broker topology is an infrastructure-coupling decision.** A single broker gives easy discovery, central governance and minimal infrastructure but is a single point of failure and a throughput ceiling. Domain-scoped brokers (one per group of related services) follow domain boundaries and improve isolation, scale and elasticity, at the cost of harder discovery, more cost and more moving parts. Neither is a default.
10. **In event choreography the sender typically owns the topic/queue**, so a broker belongs to the producing service's infrastructure footprint.

## Default workflow

1. Restate the problem in one sentence and list the architecture characteristics at stake (fault tolerance, scalability, responsiveness, consistency, security, evolvability).
2. Identify the governing pattern family: reuse/coupling, communication/workflow, data access split, or infrastructure ownership.
3. Name candidate patterns (at least two) and the current style's constraints (monolith vs distributed, domain partitioning).
4. Build a qualitative trade-off comparison for the candidates against the characteristics from step 1; mark which risks have mitigations (redundancy, central ownership, catalogs).
5. Choose the pattern, then choose the implementation; record why, what would change the decision, and when to revisit it.
6. Flag vocabulary hazards (for example "hexagonal") so stakeholders agree on what the name means.

## References

- [references/patterns-vs-styles-and-reuse.md](references/patterns-vs-styles-and-reuse.md): read when distinguishing pattern vs style vs tool vs "best practice", or when designing reuse of operational concerns (Hexagonal, Sidecar, Service Mesh, orthogonal coupling).
- [references/communication-patterns.md](references/communication-patterns.md): read when choosing between orchestration and choreography for a workflow, or evaluating CQRS for a data path.
- [references/broker-infrastructure-patterns.md](references/broker-infrastructure-patterns.md): read when deciding how many message brokers to run, who owns them, and how services discover topics.
- [references/source-map.md](references/source-map.md): read to see which reference covers each chapter section.

## Scripts

None. The chapter offers qualitative trade-offs rather than calculations, so no script is provided.
