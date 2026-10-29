---
name: fsa-theme-monolithic-styles
description: Theme skill on the monolithic architecture styles from Richards and Ford's "Fundamentals of Software Architecture" (2nd ed.) (chapters 10 to 13). Use when designing, reviewing or choosing among layered, modular monolith, pipeline and microkernel (plug-in) architectures, enforcing layer and module boundaries, detecting the architecture sinkhole, structuring filters and pipes, designing a stable core with plug-ins, or planning a later migration out of a monolith.
---

# Monolithic styles (Fundamentals of Software Architecture, ch. 10 to 13)

All four styles deploy as one unit, so they share the same broad profile: simple and inexpensive, weak on elasticity, scalability and fault tolerance. They differ in how they partition code.

## Cross-chapter rules

1. **Monoliths are a valid choice** under tight budget or time, uncertain direction, or modest operational demands. Choose deliberately; an unchosen structure tends to become layered by accident and then a big ball of mud.
2. **Layered: partitioned by technical role.** Keep the main path closed for isolation, justify each open layer, and watch the share of pass-through requests (`scripts/layer_rules_check.py`). Good for small systems and teams organized by technical skill; poor for frequent domain changes.
3. **Modular monolith: partitioned by domain.** Make every namespace belong to a declared module, budget cross-module coupling, forbid specific dependencies, and route necessary calls through a mediator (`scripts/check_module_boundaries.py`). A natural starting point that can later split into services.
4. **Pipeline: ordered one-way steps.** Filters are stateless and single-purpose (producer, transformer, tester, consumer); pipes carry governed contracts. If the flow branches unpredictably, switch to event-driven.
5. **Microkernel: a stable core plus plug-ins.** Push variant-specific logic into plug-ins behind one contract per plug-in type, keep plug-ins independent of each other, and treat a volatile core as a warning sign.
6. **Plan the exit.** Keep reuse low, data grouped by domain and boundaries enforced so a later split stays affordable.

## Default workflow

1. Confirm a single set of characteristics justifies a monolith (see the characteristics theme).
2. Pick the partitioning that matches how changes arrive: technical (layered, pipeline) or domain (modular monolith, microkernel).
3. Encode boundary rules as fitness functions and review drift regularly.

<!-- BEGIN GENERATED: run tools/build_bundles.py to refresh -->

## References by chapter

Each link is one level deep; read only the files whose description matches the task.

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

Merged section maps: [source-maps.md](references/source-maps.md).

## Scripts

Python 3 standard library only; run any script with `--help` for its arguments.

| Script | Purpose |
|---|---|
| `scripts/layer_rules_check.py` (ch10) | Check a layered architecture's access rules and sinkhole share. |
| `scripts/check_module_boundaries.py` (ch11) | Check modular-monolith boundaries: module membership, coupling budget, forbidden pairs. |

<!-- END GENERATED -->
