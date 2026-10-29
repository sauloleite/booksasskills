---
name: sahp-theme-tradeoff-analysis-and-coupling
description: Theme skill on trade-off analysis and coupling from "Software Architecture: The Hard Parts" (Ford, Richards, Sadalage, Dehghani) (chapters 1, 2 and 15). Use when no best practice applies and a decision needs structured trade-off analysis, when identifying architecture quanta and static versus dynamic coupling, classifying interactions by communication, consistency and coordination, writing ADRs or fitness functions, or presenting a trade-off to stakeholders.
---

# Trade-off analysis and coupling (Software Architecture: The Hard Parts, ch. 1, 2, 15)

The method that runs through the whole book: when no ready answer exists, find what is entangled, understand how it is coupled, and weigh options against the specific context.

## Cross-chapter rules

1. **Seek the least-bad option.** Hard problems are specific to one organization; generic best practices are a starting point at most.
2. **Define coupling by change impact.** Two parts are coupled when changing one may force a change in the other.
3. **Find the quanta.** Shared databases, mediators, tightly bound UIs, shared deploy units and startup dependencies merge services into one quantum; synchronous calls join quanta at runtime (`scripts/quantum_coupling.py`).
4. **Separate static and dynamic coupling.** Static coupling decides the scope of operational characteristics; dynamic coupling has three linked forces: communication (sync or async), consistency (atomic or eventual) and coordination (orchestrated or choreographed).
5. **Analyze in three steps.** Identify entangled dimensions, analyze how they couple, then judge options by what a change does to their dependents. Decide the most fundamental dimension first and iterate.
6. **Compare like with like and stay in context.** Use complete, non-overlapping option sets; weight factors for this situation (`scripts/tradeoff_worksheet.py`); model escalating domain scenarios.
7. **Present the bottom line.** Give stakeholders one outcome-level question, not the full evidence.
8. **Record and enforce.** ADRs capture context, decision and consequences; fitness functions enforce what an ADR alone cannot.
9. **Avoid evangelism.** Insist on downsides, prefer scenarios over anecdotes, and guard trials with automated checks.

## Default workflow

1. Map quanta and coupling for the area in question (ch02).
2. List entangled dimensions and options; analyze and weight them in context (ch15).
3. Record the decision in an ADR and add fitness functions (ch01).

<!-- BEGIN GENERATED: run tools/build_bundles.py to refresh -->

## References by chapter

Each link is one level deep; read only the files whose description matches the task.

### CH01: What Happens When There Are No Best Practices?

- [ch01-data-vocabulary-and-running-example.md](references/ch01-data-vocabulary-and-running-example.md): read when data ownership or transactions are at stake, when classifying operational vs analytical data, when terms like coupling, contract, orchestration or atomicity need pinning down, or when assessing a struggling monolith before decomposition.
- [ch01-fitness-functions-governance.md](references/ch01-fitness-functions-governance.md): read when planning architecture governance, writing cycle, layer or load-dependent checks, deciding between a fitness function and a unit test, handling manual checks, or designing an enterprise pipeline governance stage.
- [ch01-trade-off-mindset-and-decision-records.md](references/ch01-trade-off-mindset-and-decision-records.md): read when the user wants "the best" approach, when weighing options or judging a legacy style against its historical constraints, when separating architecture from design, or when drafting or reviewing an ADR (includes a worked example).

### CH02: Discerning Coupling in Software Architecture

- [ch02-architecture-quantum-static-coupling.md](references/ch02-architecture-quantum-static-coupling.md): read when testing whether something is a quantum, counting quanta in a topology, handling shared databases, mediators, UIs or micro-frontends, or building a static quantum diagram of a legacy estate.
- [ch02-dynamic-coupling-dimensions.md](references/ch02-dynamic-coupling-dimensions.md): read when choosing sync vs async, atomic vs eventual, orchestration vs choreography, naming a saga combination, or diagnosing runtime entanglement between services with different scale profiles.
- [ch02-trade-off-analysis-framing.md](references/ch02-trade-off-analysis-framing.md): read when framing a trade-off discussion, explaining why microservices made decisions harder, applying the three-step method, or answering "how big should this service be".

### CH15: Build Your Own Trade-Off Analysis

- [ch15-communicating-and-staying-objective.md](references/ch15-communicating-and-staying-objective.md): read when presenting a decision to stakeholders, facing a tool champion or a forced debate, choosing between a shared topic and per-consumer queues, or adding fitness functions to guard a trial; also summarizes the chapter's framing story and epilog.
- [ch15-three-step-analysis-process.md](references/ch15-three-step-analysis-process.md): read when setting up an analysis from scratch: finding entangled dimensions, building a static coupling inventory, enumerating and rating combinations, reading matrix correlations, ordering decisions.
- [ch15-trade-off-techniques.md](references/ch15-trade-off-techniques.md): read when checking whether a comparison is valid: qualitative versus quantitative ratings, MECE candidate sets, the out-of-context trap, and escalating domain scenario modeling with an invented worked example.

Merged section maps: [source-maps.md](references/source-maps.md).

## Scripts

Python 3 standard library only; run any script with `--help` for its arguments.

| Script | Purpose |
|---|---|
| `scripts/quantum_coupling.py` (ch02) | Architecture quantum and coupling analyzer (static + dynamic). |
| `scripts/tradeoff_worksheet.py` (ch15) | Weighted trade-off worksheet: options x factors, with team-supplied weights. |

<!-- END GENERATED -->
