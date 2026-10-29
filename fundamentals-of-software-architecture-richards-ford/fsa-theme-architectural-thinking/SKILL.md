---
name: fsa-theme-architectural-thinking
description: Theme skill on how architects think, from Richards and Ford's "Fundamentals of Software Architecture" (2nd ed.) (chapters 1, 2, 3, 8 and 27). Use when separating architecture from design, running trade-off analysis, building technical breadth, measuring modularity (cohesion, coupling, abstractness, instability, connascence), identifying logical components and their coupling, or applying the laws of software architecture to a decision.
---

# Architectural thinking, modularity and components (Fundamentals of Software Architecture, ch. 1, 2, 3, 8, 27)

The mental toolkit beneath every other theme: what counts as architecture, how to reason about trade-offs, and how to carve a system into well-bounded parts.

## Cross-chapter rules

1. **Every choice costs something.** If an option seems to have no downside, keep looking; a decision is architectural when all options carry significant trade-offs.
2. **Record why, not only how.** Structure can be recovered from code; rationale cannot.
3. **Think in spectrums.** Most decisions sit between extremes; place them deliberately instead of choosing a camp.
4. **Weight trade-offs in context.** List factors specific to this organization, mark which option each favors, then weight them; an unweighted tally misleads (`scripts/tradeoff_matrix.py`).
5. **Architecture is what is costly to reverse.** Use strategic versus tactical, effort to change, and size of trade-offs to place a decision between architecture and design.
6. **Breadth over depth.** Grow what you know exists, let stale expertise go, keep a personal radar, and stay hands-on without becoming the bottleneck.
7. **Modularity decays unless governed.** Distinguish modularity (where to divide) from granularity (how big). Measure cohesion and coupling, keep components near the main sequence (`scripts/modularity_metrics.py`), and prefer weaker, more local connascence.
8. **Logical before physical.** Identify components by role and action (not entity "managers"), test cohesion with a one-line responsibility statement, and let characteristics split components that look functionally alike (`scripts/component_coupling.py`, `scripts/component_lint.py`).
9. **Reuse plumbing, not domain logic.** Reuse is implemented through coupling, and domain code changes fastest.

## Default workflow

1. Frame the decision and place it on the architecture versus design spectrum (ch02).
2. Identify logical components and their responsibilities; iterate (ch08).
3. Measure modularity and coupling, and set thresholds (ch03).
4. Run a weighted trade-off analysis and record the why (ch27, ch01).

<!-- BEGIN GENERATED: run tools/build_bundles.py to refresh -->

## References by chapter

Each link is one level deep; read only the files whose description matches the task.

### CH01: Introduction

- [ch01-architect-expectations-playbook.md](references/ch01-architect-expectations-playbook.md): read when separating architectural from technical decisions, planning compliance or vitality reviews, assessing an architect's skills, or handling stakeholder pushback and politics.
- [ch01-architecture-definition-and-context.md](references/ch01-architecture-definition-and-context.md): read when scoping an architecture, explaining what "architecture" includes, ordering the analysis, or arguing that context determines the right answer; also covers the book's three-part structure.
- [ch01-laws-and-trade-off-analysis.md](references/ch01-laws-and-trade-off-analysis.md): read when evaluating options, challenging "best practice" or "no downside" claims, writing decision rationale, or resisting one-size-fits-all standards.

### CH02: Architectural Thinking

- [ch02-architecture-vs-design.md](references/ch02-architecture-vs-design.md): read when deciding whether a choice is architectural or design-level, who should own it, or how much rigor it deserves.
- [ch02-hands-on-coding-balance.md](references/ch02-hands-on-coding-balance.md): read when an architect asks how much to code, what to code, or how to stay technical without slowing the team.
- [ch02-technical-breadth-and-radar.md](references/ch02-technical-breadth-and-radar.md): read when planning learning, advising a developer becoming an architect, building a personal technology radar, or spotting Frozen Caveman reasoning.
- [ch02-trade-off-analysis.md](references/ch02-trade-off-analysis.md): read when comparing options, writing a recommendation, translating business drivers into characteristics, or needing the worked messaging example (shared topic versus per-consumer queues).

### CH03: Modularity

- [ch03-cohesion-and-lcom.md](references/ch03-cohesion-and-lcom.md): read when deciding where an operation belongs, labeling cohesion levels, computing or interpreting LCOM, or auditing utility classes before a restructure.
- [ch03-connascence.md](references/ch03-connascence.md): read when naming a coupling problem precisely, reviewing cross-boundary contracts, choosing a refactoring toward weaker coupling, or estimating migration cost from shared state and ordering assumptions.
- [ch03-coupling-metrics-and-main-sequence.md](references/ch03-coupling-metrics-and-main-sequence.md): read when computing or interpreting Ca, Ce, abstractness, instability or distance from the main sequence, explaining the zones of pain and uselessness, or turning metrics into governance checks.
- [ch03-modularity-granularity-and-packaging.md](references/ch03-modularity-granularity-and-packaging.md): read when someone proposes splitting or merging modules or services, confuses modularity with granularity, asks about packaging, namespaces or logical versus physical separation, or needs the historical context for module mechanisms.

### CH08: Component-Based Thinking

- [ch08-component-coupling.md](references/ch08-component-coupling.md): read when measuring afferent/efferent coupling, looking for temporal coupling, or applying the Law of Demeter with a worked redistribution example.
- [ch08-logical-architecture-and-identification.md](references/ch08-logical-architecture-and-identification.md): read when defining components from code, contrasting logical and physical views, seeding components (Workflow, Actor/Action), diagnosing the Entity Trap, or assigning user stories.
- [ch08-refining-components.md](references/ch08-refining-components.md): read when judging cohesion, splitting for architecture characteristics, planning ongoing restructuring, or using the auction case study pattern and trade-off framing.

### CH27: The Laws of Software Architecture, Revisited

- [ch27-hidden-trade-offs-and-reuse.md](references/ch27-hidden-trade-offs-and-reuse.md): read when someone proposes a "pure win", pushes for broad code reuse, asks for both decoupling and reuse, or wants a one-time decision to become a standing rule.
- [ch27-trade-off-analysis-method.md](references/ch27-trade-off-analysis-method.md): read when running a concrete trade-off analysis, building or weighting a factor matrix, or working through shared library vs shared service and queue vs topic; includes the Out of Context antipattern and an invented worked example.
- [ch27-why-and-spectrum-thinking.md](references/ch27-why-and-spectrum-thinking.md): read when documenting rationale, deciding whether something is architecture or design, framing a choice as a spectrum, coaching on uncertainty, or setting up practice katas.

Merged section maps: [source-maps.md](references/source-maps.md).

## Scripts

Python 3 standard library only; run any script with `--help` for its arguments.

| Script | Purpose |
|---|---|
| `scripts/modularity_metrics.py` (ch03) | Modularity metrics calculator (Martin package metrics plus class-level LCOM). |
| `scripts/component_coupling.py` (ch08) | Compute afferent (Ca) and efferent (Ce) coupling per logical component. |
| `scripts/component_lint.py` (ch08) | Flag Entity Trap names and low-cohesion responsibility statements. |
| `scripts/tradeoff_matrix.py` (ch27) | Weighted trade-off matrix (FSA Chapter 27: contextual weighting of trade-offs). |

<!-- END GENERATED -->
