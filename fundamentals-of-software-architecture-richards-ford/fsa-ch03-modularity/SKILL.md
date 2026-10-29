---
name: fsa-ch03-modularity
description: Modularity analysis for architects, based on Chapter 3 of Richards and Ford's "Fundamentals of Software Architecture" (2nd ed.). Covers modularity versus granularity, the cohesion scale, LCOM, afferent/efferent coupling, abstractness, instability, distance from the main sequence (zones of pain and uselessness) and connascence (forms, strength, locality, degree). Use when sizing or splitting modules or services, reviewing coupling, assessing a code base before a migration, measuring technical debt, or naming a coupling problem in a code or design review.
---

# FSA Ch. 3: Modularity

This skill helps an agent reason about how code is grouped and how the groups depend on each other, the way Chapter 3 of Richards and Ford frames it. Modularity is an implicit architecture characteristic: nobody requests it, every sustainable code base needs it, and it erodes unless someone keeps investing in it. The chapter gives three lenses (cohesion, coupling, connascence) plus a few derived metrics, and warns that every metric needs interpretation. Use them to decide where boundaries go, how big pieces should be, and which dependencies are acceptable across a boundary.

## Key decision rules

**Modularity and granularity**
1. Separate two questions: whether and where to divide (modularity) and how big each piece is (granularity). Dividing is usually good; wrong size is where trouble starts.
2. Judge granularity by the coupling between pieces, not by their size. Pieces that must be called, changed or deployed together signal a distributed monolith or distributed big ball of mud.
3. Keep logical modularity distinct from physical separation. Assess logical boundaries inside a monolith before planning any decomposition; loose logical partitioning is what blocks later migration.
4. Packaging is an architecture decision: tightly coupled packages cannot be reused individually. Agree on which language construct represents a component.

**Cohesion**
5. Rank cohesion from best to worst: functional, sequential, communicational, procedural, temporal, logical, coincidental. Treat `*Utils`, `Common` and startup grab bags (logical or temporal cohesion) as suspects.
6. Do not split a cohesive module: it only adds coupling and hurts readability.
7. To decide whether operations move out, weigh: is the new module too thin to stand alone, will the current one keep growing, and would the split need deep knowledge of the original (heavy coupling)?
8. Use LCOM to find classes whose methods form disjoint groups over fields, especially shared utility classes before a migration. LCOM sees structure only, never intent; confirm every finding with domain judgment (why matters more than how).

**Coupling and derived metrics**
9. Afferent (Ca) is incoming, efferent (Ce) is outgoing.
10. Abstractness A = abstract / (abstract + concrete). Instability I = Ce / (Ce + Ca). Distance D = |A + I - 1|.
11. Healthy components sit near the line A + I = 1: depended-upon things abstract, leaf things concrete.
12. Zone of pain (low A, low I): concrete code with many dependents; brittle when it must change. Zone of uselessness (high A, high I): abstractions nobody uses. Pain zone is harmless only for code that never changes.
13. Code metrics are blunt and need interpretation (cyclomatic complexity cannot tell essential from accidental complexity). Baseline them and enforce trends as fitness functions rather than chasing absolute numbers.

**Connascence**
14. Two elements are connascent if changing one forces a change in the other. It is vocabulary, not a count.
15. Static forms, weaker to stronger: name, type, meaning, position, algorithm. Dynamic forms (execution, timing, values, identity) are generally stronger and harder to find. Prefer static over dynamic.
16. Strength: refactor toward weaker forms (meaning to name via a named constant). Locality: strong forms are tolerable close together, not across modules or services. Degree: the more elements affected, the worse; degree grows with the code base.
17. Encapsulate to minimize total connascence, minimize what crosses boundaries, and maximize what stays inside. Weirich's rules: convert strong forms to weak ones; the farther apart elements are, the weaker their connascence must be.
18. Across service or component boundaries, aim for name and type only. Shared values across separate databases (all change or none) is the expensive case.

## Default workflow

1. Clarify the question: boundary placement, piece size, dependency health, or migration readiness.
2. Map logical modules and their dependencies (tool output or a quick dependency graph).
3. Cohesion pass: label suspicious modules with their cohesion level; compute LCOM on large or utility classes.
4. Coupling pass: compute Ca, Ce, A, I, D per component; inspect the top D outliers and classify pain versus uselessness; check that dependencies point toward stable, abstract components.
5. Connascence pass: for each cross-boundary dependency, name the form, locality and degree; flag anything stronger than type.
6. Recommend: keep, merge, split or add abstractions, with the trade-off stated (added coupling, extra hops, team ownership, rate of change).
7. Govern: propose baselines and fitness functions for D, LCOM or complexity so the structure does not drift.

## References

- [references/modularity-granularity-and-packaging.md](references/modularity-granularity-and-packaging.md): read when someone proposes splitting or merging modules or services, confuses modularity with granularity, asks about packaging, namespaces or logical versus physical separation, or needs the historical context for module mechanisms.
- [references/cohesion-and-lcom.md](references/cohesion-and-lcom.md): read when deciding where an operation belongs, labeling cohesion levels, computing or interpreting LCOM, or auditing utility classes before a restructure.
- [references/coupling-metrics-and-main-sequence.md](references/coupling-metrics-and-main-sequence.md): read when computing or interpreting Ca, Ce, abstractness, instability or distance from the main sequence, explaining the zones of pain and uselessness, or turning metrics into governance checks.
- [references/connascence.md](references/connascence.md): read when naming a coupling problem precisely, reviewing cross-boundary contracts, choosing a refactoring toward weaker coupling, or estimating migration cost from shared state and ordering assumptions.
- [references/source-map.md](references/source-map.md): read to see which reference covers each chapter section.

## Scripts

Run `python3 scripts/modularity_metrics.py components.json` to compute abstractness, instability, distance from the main sequence and a zone flag (pain, uselessness, balanced) per component, plus LCOM1, LCOM96b and disconnected method clusters (split candidates) per class.

- Input JSON: `{"components": [{"name", "ca", "ce", "abstract", "concrete"}], "classes": [{"name", "methods": {"method": ["field", ...]}}]}`; either key may be omitted.
- `--threshold 0.4` changes the distance above which a component is flagged (default 0.5, a tool default rather than a book value).
- `--json` emits machine-readable output for fitness functions or dashboards.
- Undefined cases (no couplings, no types) are reported as such, not forced to a number.
