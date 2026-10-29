---
name: sahp-ch15-trade-off-analysis
description: Gives a repeatable method for building custom trade-off analyses in distributed architectures, based on Chapter 15 of Ford, Richards, Sadalage and Dehghani's "Software Architecture: The Hard Parts". Covers finding entangled dimensions, static coupling inventories, rating options in isolation then in a matrix, MECE comparisons, the out-of-context trap, domain scenario modeling, bottom-line framing for stakeholders and resisting evangelism. Use when comparing architecture options, building a trade-off table, presenting a decision to non-technical stakeholders, or challenging a silver-bullet proposal.
---

# SAHP Chapter 15: Building Custom Trade-Off Analyses

## Purpose

The book's ready-made analyses (sagas, communication styles, granularity forces) are a starting point; real systems always have extra entangled concerns no generic table covers. This skill teaches an agent to run the analysis itself: discover which concerns are braided together, model combinations cheaply, rate options qualitatively, narrow to the context that matters, and hand stakeholders one clear bottom-line question. Use it whenever an architect must choose between options whose consequences interact, and whenever someone claims an option is simply better.

## Key decision rules (apply without opening references)

1. **Three steps, in order.** Find entangled parts; analyze how they couple; assess trade-offs by asking what a change in one part forces on the parts that depend on it.
2. **Coupling test.** If changing X could force Y to change, X and Y are coupled and both belong in the analysis.
3. **Static coupling inventory per quantum:** OS or container base, frameworks and transitive libraries, data stores and platform services, startup integration points (config, secrets, registry, identity), and messaging infrastructure. Services linked only by a shared workflow are statically independent but dynamically coupled; analyze them separately.
4. **Derive dimensions from many examples.** Pick the concerns your systems repeatedly prove sensitive to (the book found communication, consistency, coordination). Involve ops and data people in discovery.
5. **Model lightly, prune early.** Enumerate combinations as small sketches; drop infeasible ones with a note.
6. **Rate each option in isolation, then consolidate** into one matrix. Read it for correlations: more coupling usually means worse scale/elasticity (strongly) and worse responsiveness/availability (less strictly).
7. **Fix the most fundamental dimension first** (often sync versus async), then re-analyze the choices it opens or forces. When the entangled decisions are settled, the rest is design.
8. **Qualitative by default.** Two architectures differ too much for honest numeric comparison. Build relative ratings from many examples or local spikes; test objectively where you can.
9. **Compare MECE sets.** Candidates must be the same kind of thing (no queue versus full integration platform; compare only the overlapping capability) and the set must be exhaustive, including recently arrived options for long-lived decisions.
10. **Beware the out-of-context trap.** A matrix that favors an option "overall" can still be wrong once the specific context (languages, change rate, regulation, load) is applied. Balance the relevant trade-offs, not all of them. Narrow context shrinks the option space, which is how designs stay simple.
11. **Model domain scenarios, escalating.** Single change, new variant, multi-variant or multi-service workflow, failure mid-workflow. The hard trade-offs usually appear in the complex workflows.
12. **Semantic coupling only grows.** Implementation can add coupling to what the domain requires but never remove it; skipping an orchestrator relocates coordination logic, it does not delete it.
13. **Bottom line over evidence.** Collapse detail into a few outcome-level points and ask stakeholders one "which matters more: A or B?" question.
14. **No evangelism.** Demand stated downsides for every option; counter anecdotes with scenario modeling; refuse to be cast as the opposing side; if trialing a contested option, guard its known risks with metrics and fitness functions.
15. **Testing is the rigor.** Reduce a problem to a few trade-offs small enough to test; objective results move analysis from speculation toward engineering.

## Default workflow

1. State the decision and its category in one sentence; check the candidate list is MECE.
2. With the relevant roles, list entangled dimensions and build the static coupling inventory for the affected quanta.
3. Enumerate feasible combinations; choose the forces to rate (coupling, complexity, availability, scale, plus local ones).
4. Rate each option alone, then build the consolidated matrix; note correlations.
5. Write down the specific context and model at least three domain scenarios, including a complex workflow and a failure.
6. Fix the most fundamental dimension, re-run for dependent choices, stop when only design remains.
7. Optionally run the worksheet script to see deciding factors, fragility and context shifts.
8. Present the bottom-line question to stakeholders; record the decision and trade-offs in an ADR; add fitness functions for accepted risks.

## References

- [references/three-step-analysis-process.md](references/three-step-analysis-process.md): read when setting up an analysis from scratch: finding entangled dimensions, building a static coupling inventory, enumerating and rating combinations, reading matrix correlations, ordering decisions.
- [references/trade-off-techniques.md](references/trade-off-techniques.md): read when checking whether a comparison is valid: qualitative versus quantitative ratings, MECE candidate sets, the out-of-context trap, and escalating domain scenario modeling with an invented worked example.
- [references/communicating-and-staying-objective.md](references/communicating-and-staying-objective.md): read when presenting a decision to stakeholders, facing a tool champion or a forced debate, choosing between a shared topic and per-consumer queues, or adding fitness functions to guard a trial; also summarizes the chapter's framing story and epilog.
- [references/source-map.md](references/source-map.md): read to see which reference covers each chapter section.

## Scripts

- `scripts/tradeoff_worksheet.py`: Run `python3 scripts/tradeoff_worksheet.py matrix.json` to compute weighted totals for options x factors (scores 1-5 or very low to very high, team-supplied weights, `lower_is_better` for cost-like factors), list the deciding factors between the top two options, flag non-discriminating factors, detect fragile rankings (one factor's removal flips the winner), and show the winner under alternative context weightings. Add `--json` for machine-readable output and `--top N` to limit deciding factors. Input format is in the script's docstring; run with `--help` for options. Treat the numbers as an aid to qualitative reasoning, not a measurement.
