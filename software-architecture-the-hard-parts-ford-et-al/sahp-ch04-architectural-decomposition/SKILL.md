---
name: sahp-ch04-architectural-decomposition
description: Guides how to break a monolith apart: judging whether a codebase is decomposable with coupling metrics (afferent/efferent coupling, abstractness, instability, distance from the main sequence), then choosing between component-based decomposition and tactical forking, with service-based architecture as a stepping stone. Based on Chapter 4 of Ford, Richards, Sadalage and Dehghani's "Software Architecture: The Hard Parts". Use when planning a monolith migration, assessing a legacy codebase's structure, picking a decomposition approach, or writing the ADR for that choice.
---

# Architectural decomposition (SAHP Chapter 4)

Purpose: help an architect decide how to start splitting a monolithic application. Modularity drivers justify why to split; this chapter answers how. The workflow is a short decision tree: first establish whether the code is salvageable using structural metrics and inspection, then pick component-based decomposition (structured code) or tactical forking (unstructured code), and record the decision with its trade-offs. Concrete refactoring patterns for component-based decomposition, data decomposition and service granularity belong to later chapters; this skill stops at the choice of approach.

## Key decision rules

1. Never migrate by grabbing whatever looks easy first. Piecemeal, plan-less extraction (the Elephant Migration anti-pattern) tends to produce a distributed monolith. Start from a whole-system view.
2. Step one is always the decomposability question: is this codebase a candidate for decomposition patterns at all? No single metric answers it; combine metrics with code inspection.
3. Use afferent coupling (Ca, incoming) and efferent coupling (Ce, outgoing) to find shared assets. High-Ca classes that were fine to reuse in a monolith (addresses, money types, audit helpers) become cross-service coupling; decide their ownership before cutting services.
4. Compute abstractness A (abstract artifacts relative to concrete ones), instability I = Ce / (Ce + Ca) and distance D = |A + I - 1|. Read A and I together: low I with low A means rigid, not stable.
5. Zone of pain = low A, low I (concrete code everybody depends on). Zone of uselessness = high A, high I (abstractions nobody uses). Near the main sequence = balanced.
6. Mostly near the main sequence: decomposable. Mostly in the two zones: shoring up the structure may not repay the effort; consider forking or replacement.
7. Selection rule: identifiable components (even loose ones) lead to component-based decomposition; a big ball of mud with few observable components leads to tactical forking.
8. Build services from groups of components, never one service per component.
9. When the destination is microservices, land on service-based architecture first: coarse domain services, shared database kept, no new deployment platform required, no organisational change. Decide finer granularity and data splitting afterwards.
10. Tactical forking: clone the whole monolith per target service, then each team deletes what it does not need, verifying each deletion with the build and tests. Deleting beats extracting in highly coupled code.
11. Know the forking costs: latent leftover code in every service, unchanged code quality, duplicated shared code with drifting names, boundaries fixed upfront, more teams to coordinate. It is a tactical move for speed, not a structural fix.
12. Component-based decomposition is slower but safer, incremental, avoids duplicated shared code, and lets service boundaries emerge from grouping components.

## Default workflow

1. Gather a component inventory: namespaces or directories, abstract versus concrete artifact counts, and the component dependency graph (from tooling such as JDepend, NDepend or a language-specific dependency analyser).
2. Run `scripts/decomposability_metrics.py` (or equivalent tooling) to get Ca, Ce, A, I, D and zone labels. List the most-shared components.
3. Inspect the worst outliers and highest-Ca components in the source. Decide: salvageable or not.
4. If salvageable, classify the code as structured (components exist) or unstructured.
5. Choose the approach using the criteria in the decomposition reference: code structure, volume of shared infrastructure code, which quality attributes are hurting, time pressure, team topology, whether boundaries are known upfront.
6. For component-based decomposition, target service-based architecture first and keep the database shared. For tactical forking, define target services and teams, fork, delete, then schedule cleanup.
7. Write an ADR capturing context, decision, justification and consequences (duration, team organisation, follow-up work).

## Output expectations

When advising, state the metric evidence, the chosen approach, the main trade-off accepted, and the next concrete step (for example, which shared component needs an ownership decision first). Mark numeric thresholds as heuristics; the chapter supplies none.

## References

- [references/decomposability-assessment.md](references/decomposability-assessment.md): read when evaluating whether a codebase can be decomposed, interpreting Ca, Ce, A, I and D values, or explaining the zones of pain and uselessness; includes a worked example and pitfalls.
- [references/decomposition-approaches.md](references/decomposition-approaches.md): read when choosing between component-based decomposition and tactical forking, planning a service-based stepping stone, running a tactical fork, or drafting the ADR for the choice.
- [references/source-map.md](references/source-map.md): read when you need to locate which reference covers a given chapter section.

## Scripts

Run `python3 scripts/decomposability_metrics.py --components components.csv [--edges edges.csv]` to compute afferent/efferent coupling, abstractness, instability, normalized distance from the main sequence, zone labels, the most widely shared components and a heuristic decomposability hint.

- `components.csv` columns: `component,abstract,concrete` plus optional `ca,ce`.
- `edges.csv` columns: `source,target` (one dependency per row); when provided, Ca and Ce are derived from it.
- Options: `--abstractness-denominator concrete` uses abstract/concrete instead of abstract/(abstract+concrete); `--zone-threshold 0.5` sets the D cut-off for zone labels; `--json` emits machine-readable output; `--help` lists everything.
