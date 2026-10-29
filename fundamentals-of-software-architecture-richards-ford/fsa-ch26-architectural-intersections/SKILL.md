---
name: fsa-ch26-architectural-intersections
description: Applies Chapter 26 of Richards and Ford's "Fundamentals of Software Architecture" (2nd ed.) on architectural intersections, the nine facets an architecture must align with: implementation (operational concerns, structure, constraints), infrastructure, data topologies, engineering practices, team topologies, systems integration, enterprise standards, business environment, and generative AI. Use when validating a design, diagnosing why a sound style fails in production, choosing a database type or topology, checking team or pipeline fit, or adding LLMs to a system.
---

# Architectural Intersections (FSA Chapter 26)

## Purpose

Picking the right style for the right characteristics is necessary but not sufficient. An architecture works only when the code, infrastructure, data, engineering practices, teams, integrated systems, enterprise rules, business situation and any embedded LLMs all pull in the same direction. This skill helps an agent audit those nine alignments, explain failures as misalignments rather than bad design, and propose concrete realignment, relying on the architect's communication and collaboration rather than style selection alone.

## Key decision rules (apply even without opening references)

1. **Never wave a concern away as merely an implementation matter.** Code must honor the driving characteristics, the logical component structure, and the declared constraints.
2. **Check every local optimization against the driving characteristics.** A fix for latency or coupling (for example, per-instance replicated caches) can break the scalability the style was chosen for. Multiply per-instance state by peak instance count.
3. **Source layout must mirror logical components.** Govern it automatically (ArchUnit, ArchUnitNet, NetArchTest, PyTestArch, TSArch) plus ongoing collaboration.
4. **State constraints with their reason and govern them.** A layered system chosen for cheap schema change only works if all data access stays in the persistence layer and no layer is skipped.
5. **A style's operational strengths are only potential.** Infrastructure must deliver them. Multi-zone or multi-region deployment can cancel cache benefits; co-locating services on one VM gains speed but loses scalability, fault tolerance, availability and elasticity.
6. **Topology follows style:** microservices needs database-per-service; service-based tolerates shared or domain databases; distributed data trades consistency and integrity for scale and change isolation.
7. **Database type must amplify the style's strengths** and fit the data: relational for interdependent data, document for JSON payloads, key-value for ID lookups; columnar for write-heavy, key-value/document/graph for read-heavy, relational/NewSQL for balanced. Prefer polyglot persistence when data shapes differ.
8. **Practices must match the style.** Microservices presumes automated provisioning, testing and deployment. Iterative processes fit architecture better; Agile eases style migrations (Strangler Fig, feature toggles).
9. **Measure the alignment with fitness functions.** Agility (maintainability + testability + deployability) is only real if practices deliver it.
10. **Team cut must match architecture cut:** domain teams for domain-partitioned styles, layer teams for layered, business-logic plus data-sync teams for space-based.
11. **Integrations must be compatible:** availability, scale and responsiveness of the callee, protocol, contract type, and preservation of each system's quantum.
12. **Conform to enterprise standards** or the solution gets scrapped as a one-off, however good it is.
13. **Match style to business situation** (domain-to-architecture isomorphism): no costly distributed styles under cost cutting; no rigid monolith during M&A growth.
14. **Design for unknown unknowns** through iterative and evolutionary architecture, not Big Design Up Front.
15. **Put LLMs behind an abstraction** with guardrails, evals and observability so models can be swapped and compared.
16. **As an AI assistant, list trade-offs; do not hand down style verdicts** without the full context of all intersections.

## Default workflow

1. Record the selected style, its top driving characteristics, and its constraints.
2. Walk the nine intersections in order; for each, ask the check question and note aligned, misaligned or unknown.
3. For each misalignment, name the characteristic it erodes and the evidence (load test, metric, org chart, standard).
4. Propose a realignment of either side (change the code, infrastructure, data, practices, teams or the architecture itself) and record it as an ADR with consequences.
5. Add a fitness function or structural test that would catch recurrence.
6. For unknowns, list the questions and who owns the answer (infrastructure, enterprise architecture, business sponsor).

## References

- [references/implementation-and-infrastructure-alignment.md](references/implementation-and-infrastructure-alignment.md): read for the nine-intersection audit table, code versus design conflicts, structural governance, constraint definition, and infrastructure or cloud deployment mismatches.
- [references/data-topology-alignment.md](references/data-topology-alignment.md): read when choosing a database topology or database types, or when data shape or read/write balance seems to fight the style.
- [references/organizational-and-business-alignment.md](references/organizational-and-business-alignment.md): read when assessing engineering practices, fitness functions for agility, team structure, external integrations, enterprise standards, business direction, unknown unknowns or residuality theory.
- [references/generative-ai-intersection.md](references/generative-ai-intersection.md): read when embedding an LLM into a system or when deciding how far to trust AI help on architecture decisions.
- [references/source-map.md](references/source-map.md): read to see which reference covers each chapter section.

## Scripts

None. The chapter supplies alignment criteria and checklists, not calculations.
