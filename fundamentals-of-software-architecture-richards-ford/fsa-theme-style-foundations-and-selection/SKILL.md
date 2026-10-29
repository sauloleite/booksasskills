---
name: fsa-theme-style-foundations-and-selection
description: Theme skill on architecture styles in general and how to choose one, from Richards and Ford's "Fundamentals of Software Architecture" (2nd ed.) (chapters 9, 19 and 20). Use when classifying styles (monolithic vs distributed, technical vs domain partitioning), weighing the fallacies of distributed computing, matching team topologies, choosing a style from characteristics and context, deciding data placement and sync vs async communication, or applying cross-style patterns (sidecar and service mesh, orchestration vs choreography, CQRS, broker topologies).
---

# Style foundations, selection and patterns (Fundamentals of Software Architecture, ch. 9, 19, 20)

Before picking a specific style, understand what styles are, what distribution really costs, and how patterns cut across all of them.

## Cross-chapter rules

1. **A style name is shorthand,** covering component topology, physical layout, deployment, communication and data. A pattern solves a narrower problem and can live inside many styles.
2. **Choose top-level partitioning early.** Technical partitioning scatters workflows across layers; domain partitioning repeats some customization code; the trend favors domain partitioning. Align teams with it (Conway's Law).
3. **Respect the fallacies.** Distributed styles pay for network latency, unreliability, bandwidth, security, versioning, compensation and observability. Quantify call chains with `scripts/call_chain_budget.py`.
4. **Gather context before choosing.** Domain, structural characteristics, data architecture, cloud costs, organizational forces and team maturity.
5. **Match the system's shape to the problem's shape.** Customization suggests microkernel, highly parallel discrete work suggests space-based, tightly interdependent workflows suggest coarser services.
6. **Decide in order.** Monolithic or distributed (via quanta), where data lives, then synchronous or asynchronous, defaulting to synchronous and justifying each asynchronous link.
7. **Deliver the decision as artifacts.** A topology, ADRs for the hardest choices, and fitness functions for structure and operations.
8. **Patterns carry trade-offs every time.** Standardize operational concerns (sidecar, mesh), choose orchestration for workflow control or choreography for decoupling and scale, use CQRS only when reads and writes truly differ, and weigh a single broker against per-domain brokers.

## Default workflow

1. Classify the candidate styles and check the distribution costs (ch09).
2. Run the selection sequence and produce topology, ADRs and fitness functions (ch19).
3. Pick supporting patterns and record their trade-offs (ch20).

<!-- BEGIN GENERATED: run tools/build_bundles.py to refresh -->

## References by chapter

Each link is one level deep; read only the files whose description matches the task.

### CH09: Foundations of Architecture Styles

- [ch09-distributed-fallacies.md](references/ch09-distributed-fallacies.md): read when evaluating any distributed design; contains all eleven fallacies with mitigations, stamp-coupling remedies, a compensation-failure code sketch, and a pre-distribution checklist.
- [ch09-styles-and-lineage.md](references/ch09-styles-and-lineage.md): read when defining or comparing styles versus patterns, diagnosing or rescuing a Big Ball of Mud, explaining client/server or three-tier history, or arguing for simplicity as future-proofing.
- [ch09-team-topologies.md](references/ch09-team-topologies.md): read when mapping stream-aligned, enabling, complicated-subsystem and platform teams onto an architecture, or when framing style choice by sweet spot.
- [ch09-top-level-partitioning.md](references/ch09-top-level-partitioning.md): read when choosing technical versus domain partitioning, aligning teams via Conway's Law, or walking through the Silicon Sandwiches kata and an invented worked example.

### CH19: Choosing the Appropriate Architecture Style

- [ch19-case-studies.md](references/ch19-case-studies.md): read for worked examples of the reasoning: a small customizable monolith (modular monolith vs microkernel with BFF adapters) and a high-scale auction system (microservices with selective async and five quanta).
- [ch19-style-determinations.md](references/ch19-style-determinations.md): read when actually choosing: shape matching (isomorphism) with fit/misfit heuristics, the monolith/data/communication determinations in detail, and the expected deliverables.
- [ch19-trends-and-prerequisites.md](references/ch19-trends-and-prerequisites.md): read when evaluating whether to adopt a trending style or tool, or when checking that enough context exists before recommending any style (the six prerequisite factors with probing questions).

### CH20: Architectural Patterns

- [ch20-broker-infrastructure-patterns.md](references/ch20-broker-infrastructure-patterns.md): read when deciding how many message brokers to run, who owns them, and how services discover topics.
- [ch20-communication-patterns.md](references/ch20-communication-patterns.md): read when choosing between orchestration and choreography for a workflow, or evaluating CQRS for a data path.
- [ch20-patterns-vs-styles-and-reuse.md](references/ch20-patterns-vs-styles-and-reuse.md): read when distinguishing pattern vs style vs tool vs "best practice", or when designing reuse of operational concerns (Hexagonal, Sidecar, Service Mesh, orthogonal coupling).

Merged section maps: [source-maps.md](references/source-maps.md).

## Scripts

Python 3 standard library only; run any script with `--help` for its arguments.

| Script | Purpose |
|---|---|
| `scripts/call_chain_budget.py` (ch09) | Estimate the cost of a chain of synchronous remote calls (fallacies 1-3). |

<!-- END GENERATED -->
