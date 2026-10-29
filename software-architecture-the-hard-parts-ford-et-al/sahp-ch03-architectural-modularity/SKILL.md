---
name: sahp-ch03-architectural-modularity
description: Guides when and why to break a system into smaller parts by tying decomposition to business drivers (speed-to-market, competitive advantage) through five characteristics: maintainability, testability, deployability, scalability/elasticity and fault tolerance. Based on Chapter 3 of Ford, Richards, Sadalage and Dehghani's "Software Architecture: The Hard Parts". Use when justifying or challenging a monolith migration, writing the business case or ADR for a split, choosing modular monolith vs. services, or checking whether inter-service coupling cancels the benefits.
---

# Architectural Modularity (SAHP Chapter 3)

Purpose: help an agent decide whether splitting a system is justified, and build an evidence-based case for it. Business and technical environments keep changing, so architecture must be able to change too. Modularity creates headroom for growth and makes change cheaper, but only when a real business driver exists and when the resulting parts are not tightly bound to each other. This skill turns the chapter into rules for matching observed problems to modularity drivers, for spotting where distribution would erase its own gains, and for documenting the trade-offs.

## Key decision rules (apply without opening references)

1. **No driver, no split.** Decompose only for a clear business driver: speed-to-market or competitive advantage. Frustration with patching is not a driver.
2. **The driver chain.** Speed-to-market comes from agility = maintainability + testability + deployability. Competitive advantage = speed-to-market + scalability + fault tolerance/availability. Every proposed split must move at least one of these five, for a named problem.
3. **Modularity is not automatically distribution.** Maintainability, testability and deployability can come from a modular monolith (domain partitioning) or a microkernel (plug-ins). Reach for separate deployment units mainly when scalability, elasticity or fault isolation is the problem.
4. **Change scope ladder.** Layered monolith: changes touch the whole application and several teams. Coarse domain services: changes stay within one domain. Fine-grained services: changes stay within one function. More modularity means smaller change scope.
5. **Testability = ease AND completeness.** Many tests do not mean good testability if tests are disabled, stale, or missing on critical flows, or if every change runs the entire suite.
6. **Deployability = ease, frequency AND risk.** Long release intervals bundle changes and raise risk; still match cadence to what users can absorb.
7. **Lockstep is failure.** If services must be deployed together or in a fixed order, merge them back. That state is a distributed big ball of mud.
8. **Scalability vs. elasticity.** Scalability (gradual growth) tracks modularity, meaning separate units. Elasticity (sudden spikes) tracks granularity and mean time to startup (MTTS). Coarse domain services scale better than a monolith but are not elastic.
9. **Fault tolerance needs async.** Separate units isolate crashes only if callers do not wait on them synchronously. Cloned monolith instances share the same bugs and are not real fault tolerance.
10. **Communication erodes everything.** The more services call each other to finish one business transaction, the worse testability, deployability, scalability, elasticity and fault tolerance become. Keep synchronous inter-service calls to a minimum.
11. **Measure maintainability by incoming coupling.** The von Zitzewitz maintainability level falls as more components depend on each component; also track coupling, cohesion, cyclomatic complexity, component size, and technical vs. domain partitioning.
12. **Split the data too.** If competing workloads (such as reporting vs. transactions) fight over one database, splitting only the code will not relieve the load.

## Default workflow

1. List the concrete pains (incidents, slow changes, release cadence, load failures), each with evidence.
2. Map each pain to one of the five characteristics, then to a business driver. Drop pains that map to none, or that are pure pipeline issues (note those separately).
3. For each mapped pain, pick the least distributed structure that fixes it (modular monolith or microkernel first for change-related pains; separate units for scale, spikes, and fault isolation).
4. Sketch the target units and their communication. Run the script on the dependency graph to check change scope, lockstep cycles and synchronous failure spread; redesign hot spots (make non-core calls async, break cycles).
5. Write the ADR: context (the symptoms), decision (each expected improvement tied to a symptom), consequences (migration slows features, extra cost, more deployment units to operate, database must be split).
6. Explain it to sponsors with a simple capacity analogy, then the evidence.

## References

- [references/modularity-drivers-and-business-case.md](references/modularity-drivers-and-business-case.md): read when deciding whether a split is justified, choosing modular monolith vs. distributed, or writing the business case and ADR.
- [references/change-characteristics.md](references/change-characteristics.md): read when assessing maintainability (ML formula, component metrics, change scope), testability or deployability, or when diagnosing lockstep deployments.
- [references/operational-characteristics.md](references/operational-characteristics.md): read when the problem is load growth, traffic spikes, MTTS, or one area taking down the rest of the system.
- [references/source-map.md](references/source-map.md): read to find which reference covers a given chapter section.

## Scripts

Run `python3 scripts/modularity_impact.py <edges.txt>` to compute, from a dependency edge list (`A -> B sync` or `A -> B async`, one per line), the simplified maintainability level (ML percent), each unit's change and test scope, the units that fail with it via synchronous calls, and lockstep groups (dependency cycles). Add `--direct` to count only direct incoming dependents for ML, and `--json` for machine-readable output. Treat ML as a trend indicator for comparing designs, not an absolute grade.
