---
name: fsa-ch17-orchestration-driven-soa
description: Guidance on orchestration-driven service-oriented architecture (SOA) and its modern legacy, based on Chapter 17 of Richards and Ford's "Fundamentals of Software Architecture". Covers the layered service taxonomy, orchestration engines and ESBs, reuse-versus-coupling trade-offs, canonical entity pitfalls, single-quantum characteristics, the Accidental SOA antipattern, and fitness functions for integration hubs. Use when evaluating an ESB or central workflow engine, reviewing shared "canonical" services, diagnosing slow cross-layer change, or designing legacy-to-modern integration.
---

# Orchestration-Driven SOA (FSA Chapter 17)

## Purpose

Help an agent reason about orchestration-driven SOA as a cautionary and still partly useful style: recognize it (or drift toward it) in real systems, explain why its reuse-first, technically partitioned design fails at change, and apply its surviving building blocks (ESB as integration hub plus orchestrator) safely in legacy and hybrid integration work. The chapter's core message is that a logical organizational idea (maximal reuse through a strict service taxonomy) ignored the first law of architecture: every choice is a trade-off.

## Key decision rules

1. **Judge styles by their era's forces.** The style answered late-1990s constraints (per-machine OS licensing, costly databases, mergers creating duplicate entities). Before adopting or rejecting any style, check whether its motivating constraints still apply.
2. **Disambiguate "service".** A SOA enterprise service, a service-based architecture service and a microservice differ in granularity, data and deployment. Clarify which is meant before reasoning.
3. **Reuse is coupling.** Every shared service couples all its consumers to it; changes ripple, forcing coordinated deploys and holistic testing. Evaluate shared components by change frequency and consumer diversity, not by duplication removed.
4. **Avoid canonical enterprise entities.** One shared entity must carry the union of all contexts' needs (for example, driver's license data burdening a disability-insurance team). Prefer per-bounded-context models, as DDD recommends.
5. **Extreme technical partitioning makes domain changes span many layers.** If a typical story touches several technical layers, multiple teams and a shared schema, the partitioning is wrong for the change profile.
6. **Do not let infrastructure own transactions.** Declarative, configurable transactional scope and bus-managed distributed transactions leak: they breed near-duplicate entities and unresolvable failure edge cases. Transactions cannot be cleanly abstracted away.
7. **A central orchestrator collapses quanta.** A shared database plus a mediator that every request crosses yields a single architecture quantum: distributed costs with monolithic coupling.
8. **Expect Conway's Law at the bus.** The team owning the central engine becomes a political force and a bottleneck.
9. **Use an ESB only for integration-heavy problems** needing both a hub (protocol and contract transformation) and an orchestrator, typically legacy or packaged systems meeting modern ones, or cloud plus on-prem workflows. Never build the whole architecture around it.
10. **Guard against Accidental SOA.** Set explicit encapsulation boundaries for what orchestration may do, watch transaction boundaries, and enforce with automated fitness functions (for example, read-only sources may write only to approved targets).

## Qualitative profile

Strengths: elasticity and scalability achievable with heavy vendor effort; flexible implementation behind enterprise services (packaged, legacy or bespoke). Weaknesses: deployability, testability, performance, simplicity, cost and evolvability; change scope is unpredictable, so teams fear every change request.

## Default workflow

1. Identify the question: assessing an existing system, evaluating an ESB/workflow engine, or designing a shared service.
2. Map the system against the taxonomy (business, enterprise, application, infrastructure services; orchestration engine) and the diagnostic checklist.
3. Trace one representative change request through the layers; count services, teams, schema changes and coordinated releases.
4. Weigh reuse against coupling for each shared component; propose bounded-context ownership where coupling dominates.
5. If an ESB is justified, define what it may and may not do and add fitness functions (logging consistency first, then write-direction and boundary guards).
6. Record the decision with the trade-offs and the forces that justify it.

## References

- [references/taxonomy-and-orchestration.md](references/taxonomy-and-orchestration.md): read when you need the historical forces, the four service layers and their granularity test, the orchestration engine's roles, message flow, the data topology, or why declarative transactions failed.
- [references/reuse-coupling-and-characteristics.md](references/reuse-coupling-and-characteristics.md): read when analyzing shared or canonical services, cross-layer change cost, team-structure problems, the single-quantum argument, or the qualitative characteristics profile; includes a diagnostic checklist and review questions.
- [references/modern-esb-integration-and-governance.md](references/modern-esb-integration-and-governance.md): read when deciding whether and how to use an ESB today, assessing cloud or hybrid integration, preventing Accidental SOA, or writing governance fitness functions.
- [references/source-map.md](references/source-map.md): read to see which file covers each chapter section.

## Scripts

Run `python3 scripts/integration_flow_guard.py --log interactions.jsonl --allow erp=accounting --allow sales=accounting --window-hours 24` to check integration logs for write operations from a source to a target that is not on its allowed list (exit code 1 on violations or malformed entries). Input is JSON Lines with `source`, `operation`, `target` and optional `timestamp`; add `--json` for machine-readable output and `--now` to fix the window's reference time. See `--help` for all options.
