---
name: fsa-ch19-choosing-a-style
description: Guides selection of an architecture style (monolith vs distributed, layered, modular monolith, microkernel, microservices, event-driven, space-based, service-based) from domain knowledge, architecture characteristics, data, cloud, organizational and team factors, and domain/architecture shape fit. Based on Chapter 19 of Richards and Ford's "Fundamentals of Software Architecture" (2nd ed.). Use when asked which architecture style to pick, whether to split a system, where data should live, sync vs async between services, or how to judge an industry architecture trend.
---

# Choosing an Architecture Style (FSA Chapter 19)

Picking a style is the end point of earlier analysis (characteristics, components, domain, strategy), not a starting point. No style is universally right, so the agent's job is to make sure the prerequisite knowledge exists, test each candidate style's shape against the problem's shape, settle three structural questions in order, and hand back a topology plus the records and checks that protect it. The goal is the set of trade-offs that hurts least, never a "correct" answer.

## Key decision rules

1. **Refuse to choose early.** Do not recommend a style until the domain, the driving architecture characteristics, data constraints, cloud vs on-prem context, organizational forces, and team/process maturity are understood well enough. If any are missing, ask or flag them as assumptions.
2. **Characteristics, not domain, separate the styles.** Almost any generic style can implement almost any domain. Compare candidates on how well they support the required characteristics; the domain only decides when it demands unusual operational traits (extreme scale, elasticity).
3. **Match shapes (domain/architecture isomorphism).** Prefer a style whose topology mirrors the problem: customization-heavy products suit microkernel plug-ins; many independent parallel computations suit space-based processing units. Reject styles whose shape fights the problem: very high concurrency fights a tightly coupled monolith; deeply interdependent workflows (each step depends on prior context) fight fine-grained microservices, and suit a deliberately coarser style such as service-based.
4. **Monolith vs distributed is a quantum question.** One set of architecture characteristics for the whole system points to a monolith; parts needing different characteristics point to distribution (unless other factors override). Use architecture quantum analysis to decide.
5. **Then decide where data lives.** Monoliths usually get one (or a few) relational databases. In distributed systems, decide which services own persistence and trace how data flows to assemble workflows. Iterate on structure and behavior together.
6. **Then decide communication, defaulting to synchronous.** Sync is easier to design, build and debug; switch to async only where needed, e.g. to buffer between services with very different throughput, to avoid timeouts at load spikes, or to add reliability around a fragile dependency. Async brings sync-of-data, race, deadlock and debugging costs.
7. **Team maturity is a hard constraint.** Styles that depend on strong engineering practice (microservices needs mature Agile, automation, operations collaboration) will struggle in organizations lacking it.
8. **Organizational and external forces count.** Vendor cost can veto the ideal design; planned mergers or acquisitions favor open, integration-friendly architectures; licensing changes can force migration.
9. **Design toward known weak points.** When the best-fitting style is weak on a needed characteristic (e.g. performance in microservices, usually hurt by heavy orchestration or over-split data), design specifically to mitigate it rather than switching styles reflexively.
10. **Keep a migration path.** In a monolith, align table/schema groupings with domain components when affordable so a later move to distribution is cheap.
11. **Treat fashion critically.** Know current trends and why they arose (past pain, ecosystem churn, new capabilities, accelerating change, domain and technology shifts, external pressures), then decide deliberately which to follow and where to deviate.

## Default workflow

1. Inventory the prerequisite factors (rule 1); list gaps and assumptions.
2. Run or reuse an architecture characteristics analysis; mark which characteristics vary by part of the system.
3. Determine quanta; decide monolith vs distributed.
4. Shortlist styles by characteristic support, then filter by shape fit and anti-fit (rule 3) and by team/org constraints.
5. Decide data ownership and data flow per component or service.
6. Decide sync vs async per connection, justifying every async link.
7. Identify the chosen style's weak spots against requirements and add design mitigations.
8. Produce outputs: a topology (style plus any hybrid elements), ADRs for the hardest decisions, and fitness functions guarding key principles and operational characteristics.
9. State explicitly that this is the least-bad option under current assumptions and what would change it.

## References

- [references/trends-and-prerequisites.md](references/trends-and-prerequisites.md): read when evaluating whether to adopt a trending style or tool, or when checking that enough context exists before recommending any style (the six prerequisite factors with probing questions).
- [references/style-determinations.md](references/style-determinations.md): read when actually choosing: shape matching (isomorphism) with fit/misfit heuristics, the monolith/data/communication determinations in detail, and the expected deliverables.
- [references/case-studies.md](references/case-studies.md): read for worked examples of the reasoning: a small customizable monolith (modular monolith vs microkernel with BFF adapters) and a high-scale auction system (microservices with selective async and five quanta).
- [references/source-map.md](references/source-map.md): read to locate which reference covers a given chapter section.

## Scripts

None. The chapter offers qualitative decision criteria rather than calculations, so no script is provided.
