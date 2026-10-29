---
name: sahp-ch05-component-decomposition-patterns
description: Applies six ordered refactoring patterns that turn a namespace-structured monolith into domain services (size components by statements, gather common domain logic, flatten namespaces, map component coupling, group into domains, extract domain services), each with CI fitness functions. Based on Chapter 5 of Ford, Richards, Sadalage and Dehghani's "Software Architecture: The Hard Parts". Use when sizing or cataloging components, judging migration feasibility and effort, deciding what to consolidate or flatten, grouping components into domains, or sequencing a move to service-based architecture.
---

# SAHP Chapter 5: Component-Based Decomposition Patterns

## Purpose

This skill gives an agent a structured, incremental playbook for breaking apart a monolith whose code is already grouped by namespaces or directories. Instead of guessing service boundaries, the agent refactors toward well-sized, flat, domain-aligned components inside the monolith, measures coupling to judge feasibility, and only then extracts coarse-grained domain services. Every step is backed by automated governance so the structure survives the months of ongoing maintenance that happen during a migration. Unplanned, intuition-driven migrations rarely end well; this is the antidote.

## Key decision rules (apply without opening references)

1. **Fixed order on the first pass:** identify and size, gather common domain, flatten, determine dependencies, create component domains, create domain services. Afterwards, reapply any single pattern when its fitness function alerts.
2. **A component is a leaf-node namespace containing code.** A namespace with children is a sub-domain (root namespace) and must contain no code; files there are orphaned and must be moved.
3. **Measure size in statements**, summed per component, never in files, classes or lines. Report each component's percent of total statements.
4. **Keep sizes consistent:** most components within one to two sample standard deviations of the mean; percent of code roughly even. Scale percent limits to component count (about 30 percent with 10 components, about 10 percent with 50).
5. **Split oversized components only along real sub-domains** (functional or DDD analysis), with common code in its own shared leaf. No natural seams means leave it alone. Fix the largest outlier first, then recompute, because one giant inflates the standard deviation and hides others.
6. **Many statements in very few files** means god classes: refactor classes, not necessarily the component boundary. A name that does not reveal the responsibility needs renaming.
7. **Consolidate shared domain logic, not infrastructure.** Domain logic (notification, auditing, validation) is shared by some workflows; infrastructure (logging, metrics, security) by all. Before merging, compare afferent coupling before and after; merging is fine if the total stays the same, risky if it creates a new dependency hotspot.
8. **Flatten in the direction the code justifies:** split a root's code into new leaves when the children are complex or volatile; collapse children into the parent when they are small, stable and separated without reason.
9. **Use one distinctive shared-code leaf name company-wide** (for example `.sharedcode`). Share of statements in those leaves predicts shared-library pain (a share near 45 percent is a red flag); their count predicts how many shared libraries or services you will carry.
10. **Analyze component-level coupling only**, both CA (incoming) and CE (outgoing); CT is their sum. Classify the picture as golf ball, basketball or airliner to answer: feasible? effort? refactor or rewrite? Filter out compile-time shared library components before judging.
11. **Split high-CA components when only a subset of dependents use a small slice**; this concentrates the coupling in a small piece.
12. **Services contain many components.** Group components into domains reflected in namespaces (`app.domain.subdomain.component`) together with business stakeholders; every component must land in exactly one cohesive domain.
13. **Go to service-based architecture first** (UI plus coarse domain services over a shared database). Do not jump to fine-grained microservices and inherit data splitting, distributed transactions and heavy operations before they are needed.
14. **Extract no domain service until every domain is identified and refactored**, then migrate one domain at a time.
15. **Record each structural refactoring as an architecture story** tied to a business driver or characteristic, separate from tech-debt cleanup.

## Default workflow

1. Build the inventory: name, namespace, statements, percent, files. Run the sizing script.
2. Resize outliers; rename unclear components; write architecture stories.
3. Hunt duplicated domain logic (shared classes, repeated leaf names); check coupling; consolidate.
4. Flatten: remove all code from root namespaces; move shared code into the shared leaf; compute shared-code share and count.
5. Generate a component dependency diagram, hide shared library components, classify golf ball, basketball or airliner, and report feasibility, effort and refactor versus rewrite.
6. Agree domains with the business; refactor namespaces so each component sits under its domain.
7. Extract domain services one at a time; keep each service's components under one prefix.
8. Add the matching fitness function after each step; then continue to data decomposition and granularity decisions.

## References

- [references/component-inventory-and-sizing.md](references/component-inventory-and-sizing.md): read when cataloging components, choosing size thresholds, interpreting outliers, splitting an oversized component, or writing architecture stories.
- [references/common-domain-and-flattening.md](references/common-domain-and-flattening.md): read when deciding whether to consolidate duplicated business logic, handling orphaned classes, choosing a flattening direction, or measuring shared code.
- [references/dependencies-domains-and-domain-services.md](references/dependencies-domains-and-domain-services.md): read when estimating migration feasibility and effort, reducing coupling, defining component domains, or planning domain-service extraction.
- [references/fitness-functions-catalog.md](references/fitness-functions-catalog.md): read when automating governance in CI/CD for any of the six patterns; includes original example checks.
- [references/source-map.md](references/source-map.md): read to see which reference covers each chapter section.

## Scripts

Run `python3 scripts/component_sizing.py inventory.csv` to compute each component's percent of statements, sample-standard-deviation z-score, and flags (TOO_LARGE, TOO_SMALL, ORPHAN for code in root namespaces), plus shared-code share/count and repeated leaf names. CSV columns: `namespace,statements` and optionally `name,files`.

Useful options:
- `--sd-threshold 2` (default 2; use 3 for CI governance)
- `--max-percent 20` to flag components above a share of the codebase
- `--max-stmts-per-file 500` to flag god-class components (DENSE)
- `--shared-leaf sharedcode` and `--exclude-leaf validate util`
- `--json` for machine output; `--fail-on-flags` to use it as a pipeline fitness function (exit 1 on any flag)
