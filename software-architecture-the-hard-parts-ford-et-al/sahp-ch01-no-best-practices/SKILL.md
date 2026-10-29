---
name: sahp-ch01-no-best-practices
description: Frames architecture work as least-worst trade-off analysis rather than best-practice lookup, records decisions as lightweight ADRs, governs them with fitness functions (atomic, holistic, dynamic, manual), and treats data ownership as a first-class architecture concern. Based on Chapter 1 of Ford, Richards, Sadalage and Dehghani's "Software Architecture: The Hard Parts". Use when an architect asks for "the best" design, drafts an ADR, plans architecture governance or CI checks, separates operational from analytical data, or needs shared vocabulary before decomposing a monolith.
---

# No Best Practices: Trade-offs, ADRs and Fitness Functions (SAHP Chapter 1)

Purpose: set the decision-making stance for distributed-architecture work (decomposition, data splitting, service sizing, workflows, transactions, contracts). Hard architecture problems are specific to one organization's context, so there is rarely a general answer to look up. The agent's job is to surface the trade-offs on each side of a consequential decision, recommend the least-worst balance for this context, document it, and make it enforceable.

## Key decision rules (apply without opening references)

1. **Never sell a "best practice" as the answer.** Treat each consequential problem as novel; generic patterns are inputs, not verdicts. Distrust any option presented with no downside (no silver bullets).
2. **Aim for the least-worst set of trade-offs.** No characteristic will be maximized; pick the option whose weaknesses land on the concerns the business ranks lowest, and say explicitly what is sacrificed.
3. **Analyze before implementing: why beats how.** Settle the trade-offs of a concept (for example sync vs async) before discussing products or code.
4. **Reserve full analysis for the "hard" parts.** If reversing a decision would require redeploying units, migrating data or renegotiating team contracts, it is architecture: analyze and record it. Cheap-to-change choices are design.
5. **Judge styles by their constraints, not fashion.** Ask which conditions made a style rational and whether they still hold here (centralized SOA made sense when environments were costly and open source was off-limits; free, automatable infrastructure enabled microservices).
6. **Data is architecture.** Data outlives systems, and once services own their data, transactionality becomes an architecture concern. Ask where each dataset lives, who owns it, and which workflows depend on one ACID transaction before endorsing any split.
7. **Separate operational (OLTP) from analytical data.** Different purpose, shape and outage impact; reporting coupled to the operational schema is a decomposition blocker.
8. **Record each decision as an ADR**: title (noun phrase), context (problem plus alternatives), decision (choice plus justification), consequences (including trade-offs and negatives). One decision per record.
9. **Documenting is not governing.** Pair checkable structural decisions with fitness functions: any mechanism giving an objective assessment of one or more architecture characteristics.
10. **Make characteristics measurable.** Decompose composites (agility into deployability, testability, cycle time). Unmeasurable usually means too vague.
11. **Fitness function vs test:** if the check needs domain knowledge, write a regular test; if not, a fitness function.
12. **Choose scope and type deliberately:** atomic (one characteristic) or holistic (interacting ones, e.g. security vs performance, scalability vs elasticity); static threshold, dynamic (threshold depends on context such as load), or manual (e.g. legal review as a pipeline approval stage).
13. **Run them continuously** in CI, triggered by changes to code, schema, deployment config or the checks themselves. A check that never runs validates nothing.
14. **Give governance an enterprise slot.** A shared pipeline stage lets a central team (e.g. security) push one check to every project at once, such as failing builds on a vulnerable library version.
15. **Don't over-govern.** Keep fitness functions a small, runnable checklist guarding principles that matter but never feel urgent, built with developers, not an ivory-tower maze.
16. **Use simple, explicit vocabulary.** Coupling means a change in one artifact may force a change in another. Label every workflow separately on communication (sync/async), coordination (orchestrated/choreographed) and consistency (atomic/eventual).

## Default workflow

1. Restate the decision and confirm it is architectural (hard to reverse).
2. Gather context: business drivers, ranked characteristics, constraints, data involved (operational or analytical, current transactional boundaries).
3. List at least two options and, for each, qualitative strengths and weaknesses against the ranked characteristics.
4. Eliminate options that break hard constraints; recommend the least-worst survivor and name what it sacrifices.
5. Draft an ADR (context with alternatives, decision with justification, consequences with negatives).
6. Propose fitness functions that protect the decision: scope, type, threshold, pipeline stage, owner.
7. Output: recommendation, ADR draft, fitness-function list, and open questions the architect must answer.

## References

- [references/trade-off-mindset-and-decision-records.md](references/trade-off-mindset-and-decision-records.md): read when the user wants "the best" approach, when weighing options or judging a legacy style against its historical constraints, when separating architecture from design, or when drafting or reviewing an ADR (includes a worked example).
- [references/fitness-functions-governance.md](references/fitness-functions-governance.md): read when planning architecture governance, writing cycle, layer or load-dependent checks, deciding between a fitness function and a unit test, handling manual checks, or designing an enterprise pipeline governance stage.
- [references/data-vocabulary-and-running-example.md](references/data-vocabulary-and-running-example.md): read when data ownership or transactions are at stake, when classifying operational vs analytical data, when terms like coupling, contract, orchestration or atomicity need pinning down, or when assessing a struggling monolith before decomposition.
- [references/source-map.md](references/source-map.md): read to find which file covers a given chapter section.

## Scripts

None. The chapter is conceptual and offers no calculation that a script would add value to; the fitness-function reference contains short illustrative snippets instead.
