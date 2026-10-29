---
name: sahp-theme-modularity-and-decomposition
description: Theme skill on breaking apart a monolith from "Software Architecture: The Hard Parts" (Ford, Richards, Sadalage, Dehghani) (chapters 3, 4 and 5). Use when building the business case for modularity, assessing whether a codebase is decomposable (coupling, abstractness, instability and main-sequence distance), choosing between component-based decomposition and tactical forking, or applying the component decomposition patterns (inventory and sizing, common domain components, flattening, dependencies, component domains, domain services).
---

# Modularity and decomposition (Software Architecture: The Hard Parts, ch. 3 to 5)

Why to split a monolith, whether it can be split, and the ordered patterns that move code from a tangled codebase to domain services.

## Cross-chapter rules

1. **Split only for a business driver.** Speed to market and competitive advantage, traced to concrete problems in maintainability, testability, deployability, scalability, elasticity or fault tolerance. Model change scope and failure spread with `scripts/modularity_impact.py`.
2. **Modular does not have to mean distributed.** A modular monolith captures many benefits; scalability, elasticity and fault isolation need separate deployment units and asynchronous communication.
3. **Check decomposability first.** Read coupling, abstractness, instability and main-sequence distance together with the code itself (`scripts/decomposability_metrics.py`).
4. **Choose the approach by structure.** Identifiable components suggest component-based decomposition; an unstructured codebase suggests tactical forking, accepting leftover and duplicated code.
5. **Avoid piecemeal extraction.** Pulling out the easiest parts without a plan tends to produce a distributed monolith.
6. **Apply the component patterns in order,** then keep each as a CI check: inventory and size components by statements (`scripts/component_sizing.py`), gather shared domain logic, flatten so code lives only in leaf namespaces, analyze dependencies, group components into domains with the business, then extract domain services.
7. **Go to service-based first.** Coarse domain services over a shared database let you learn before splitting data and moving to finer services.

## Default workflow

1. Write the business case and record it in an ADR (ch03).
2. Assess decomposability and pick an approach (ch04).
3. Run the component patterns, adding fitness functions as you go (ch05).
4. Extract domain services one domain at a time (ch05).

<!-- BEGIN GENERATED: run tools/build_bundles.py to refresh -->

## References by chapter

Each link is one level deep; read only the files whose description matches the task.

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

Merged section maps: [source-maps.md](references/source-maps.md).

## Scripts

Python 3 standard library only; run any script with `--help` for its arguments.

| Script | Purpose |
|---|---|
| `scripts/modularity_impact.py` (ch03) | Modularity impact check for a component or service dependency graph. |
| `scripts/decomposability_metrics.py` (ch04) | Compute component coupling and balance metrics to judge whether a codebase is decomposable. |
| `scripts/component_sizing.py` (ch05) | Component inventory and sizing analyzer (component-based decomposition). |

<!-- END GENERATED -->
