---
name: fsa-ch27-laws-revisited
description: Applies Chapter 27 of Richards and Ford's "Fundamentals of Software Architecture" (2nd ed.), which revisits the three laws of software architecture: trade-offs are unavoidable, rationale outranks mechanism, and decisions sit on spectrums rather than binaries. Covers contextual trade-off matrices, weighting, hidden trade-offs (reuse vs volatility, reuse vs decoupling), and the Out of Context antipattern. Use when comparing options (shared library vs shared service, queue vs topic), when someone claims a free win or a universal best practice, or when recording why a choice was made.
---

# The Laws of Software Architecture, Revisited (FSA Chapter 27)

## Purpose

This skill turns the book's closing chapter into a working discipline for any architecture conversation. The chapter restates three laws (every choice costs something; the reasoning behind a choice matters more than its mechanics; real decisions are positions on a continuum, not yes/no switches), adds two corollaries to the first law, names one antipattern about ignoring context, and closes with advice on practicing the craft. An agent using this skill acts as an objective arbiter of trade-offs: it surfaces the forces in play, weights them against the organization's actual goals, recommends a position on the spectrum, and makes sure the reasoning is written down.

## Key decision rules (apply even without opening references)

1. **Never answer "which is better?" without context.** "It depends" is only acceptable when followed by the specific factors it depends on and how each one tips the decision.
2. **Be an arbiter, not an evangelist.** Present both sides neutrally. Advocacy ties credibility to a choice that the ecosystem will eventually erode; today's best practice often becomes a later antipattern.
3. **Build the factor list from this organization and this solution**: platforms in use, team skills, budget, change rate, security posture, growth plans. Generic factor lists are a starting point, not an answer.
4. **Score each option per factor, then weight.** A raw count of pluses is not a decision. Ask which factors the stakeholders actually care about; one or two heavily weighted factors can overturn a lopsided tally (avoid the Out of Context antipattern).
5. **Map the analysis back to organizational goals** before choosing. Example: priority on confidentiality pushes toward per-consumer queues; priority on adding consumers rapidly pushes toward a broadcast topic.
6. **If something looks free of downsides, keep digging.** No visible trade-off means you have not found it yet.
7. **Reuse needs two conditions**: a clean abstraction used from several call sites, and low volatility. Reuse of fast-changing code spreads churn and coordination cost to every caller.
8. **Reuse technical plumbing, not domain logic.** Frameworks, libraries and platforms change slowly; the domain changes fastest. Bounded contexts deliberately do not share implementation.
9. **High decoupling and high institutional reuse cannot coexist**, because reuse is implemented through coupling. Tell stakeholders this plainly when they ask for both.
10. **Redo the analysis each time.** Do not convert one analysis into a permanent rule (for example "always choreography"). Small shifts in any of many variables can flip the result.
11. **Record the why, not only the how.** Pair diagrams (how) with ADRs (why), including the weights, rejected options, known compromises and limitations.
12. **Litmus test for "architectural"**: a decision is architectural when every option carries significant trade-offs. If one option has no meaningful cost, it is closer to design.
13. **Do not force binaries.** Express recommendations as a point on a spectrum (for example, how much orchestration versus choreography, how coarse a service) and accept decisions made under incomplete information.

## Default workflow

1. Restate the decision and the candidate options; check rule 12 to confirm it is architectural.
2. Elicit context: business drivers, constraints, team and platform landscape, expected change rate.
3. List contextual factors (rule 3); for each, note which option it favors and why.
4. Hunt for hidden trade-offs (rules 6 to 9), especially around reuse, coupling, security and extensibility.
5. Assign weights from stakeholder priorities; compare the weighted result with the raw tally and explain any flip.
6. Recommend a position on the spectrum, naming the compromises accepted and what to mitigate.
7. Draft an ADR capturing factors, weights, rejected options and limitations; note what change in context would trigger re-analysis.

## References

- [references/trade-off-analysis-method.md](references/trade-off-analysis-method.md): read when running a concrete trade-off analysis, building or weighting a factor matrix, or working through shared library vs shared service and queue vs topic; includes the Out of Context antipattern and an invented worked example.
- [references/hidden-trade-offs-and-reuse.md](references/hidden-trade-offs-and-reuse.md): read when someone proposes a "pure win", pushes for broad code reuse, asks for both decoupling and reuse, or wants a one-time decision to become a standing rule.
- [references/why-and-spectrum-thinking.md](references/why-and-spectrum-thinking.md): read when documenting rationale, deciding whether something is architecture or design, framing a choice as a spectrum, coaching on uncertainty, or setting up practice katas.
- [references/source-map.md](references/source-map.md): read to see which reference covers each chapter section.

## Scripts

- Run `python3 scripts/tradeoff_matrix.py factors.csv` to compute, from a CSV of `factor,weight,<option1>,<option2>,...` rows with cells `+`, `-` or `0`, the unweighted tally and the weighted score per option, and to flag when weighting changes the winner (an Out of Context warning sign). Add `--json` for machine output. Run with `--help` for the format.
