---
name: fsa-theme-architecture-characteristics
description: Theme skill on architecture characteristics from Richards and Ford's "Fundamentals of Software Architecture" (2nd ed.) (chapters 4 to 7). Use when deciding whether a requirement is an architecture characteristic, eliciting and prioritizing characteristics from stakeholders and requirements, defining them measurably, governing them with fitness functions (cycles, layering, complexity), or scoping them per architecture quantum to decide between monolithic and distributed designs.
---

# Architecture characteristics (Fundamentals of Software Architecture, ch. 4 to 7)

Characteristics are the success criteria that drive structure. This theme covers defining, finding, measuring, governing and scoping them.

## Cross-chapter rules

1. **Apply the three-part test.** A characteristic is not domain behavior, it influences structure, and it is critical to success. Prefer "characteristics" over "non-functional requirements".
2. **Find explicit and implicit ones.** Translate business language into characteristics, ask what the domain silently assumes, and decompose composites (agility, for example) into measurable parts.
3. **Keep the list short.** Every characteristic adds cost; aim for a handful of drivers, have stakeholders pick an unordered top three, and accept the least-bad set.
4. **Decide architecture versus design per characteristic.** Some need structural support, others can be met in code; decide with the implementation team.
5. **Make every characteristic measurable.** Define operational, structural and process measures; track percentiles and baselines, not just averages; build a shared vocabulary.
6. **Govern with fitness functions.** Automate checks for cycles and layer rules (`scripts/dependency_fitness.py`), complexity (`scripts/complexity_gate.py`) and runtime behavior; design them with developers.
7. **Scope characteristics per quantum.** A quantum is the smallest independently deployable unit including its data; shared databases and synchronous calls fuse quanta (`scripts/quantum_finder.py`).
8. **One set of characteristics suggests a monolith; several sets suggest distributed.** Then decide quanta, persistence and communication, and re-check, since synchronous links can redraw boundaries.

## Default workflow

1. Elicit candidate characteristics and filter them with the three-part test (ch04, ch05).
2. Prioritize to a short list and define objective measures (ch05, ch06).
3. Scope them per quantum and decide monolith versus distributed (ch07).
4. Encode the important ones as fitness functions in CI (ch06).

<!-- BEGIN GENERATED: run tools/build_bundles.py to refresh -->

## References by chapter

Each link is one level deep; read only the files whose description matches the task.

### CH04: Architectural Characteristics Defined

- [ch04-characteristics-catalog.md](references/ch04-characteristics-catalog.md): read when you need definitions and examples per category (operational, structural, cloud, cross-cutting), the ISO-style families, ambiguous term pairs, or guidance on building a glossary.
- [ch04-qualifying-characteristics.md](references/ch04-qualifying-characteristics.md): read when deciding whether a specific concern is an architecture characteristic, explaining implicit vs. explicit, or arguing about terminology (non-functional requirements, quality attributes).
- [ch04-trade-offs-least-worst.md](references/ch04-trade-offs-least-worst.md): read when pruning a list, explaining why characteristics cannot all be maximized, framing a least-worst decision, or reviewing an analysis with self-check questions.

### CH05: Identifying Architectural Characteristics

- [ch05-elicitation-and-translation.md](references/ch05-elicitation-and-translation.md): read when extracting characteristics from business goals or requirements, decomposing a composite goal, separating explicit from implicit, or distinguishing scalability, elasticity and performance.
- [ch05-katas-and-requirement-walkthrough.md](references/ch05-katas-and-requirement-walkthrough.md): read when running or simulating an architecture kata, doing a requirement-by-requirement analysis, or deciding whether a characteristic belongs in architecture or design.
- [ch05-limiting-and-prioritizing.md](references/ch05-limiting-and-prioritizing.md): read when the candidate list is too long, when facilitating a stakeholder prioritization session with the worksheet, or when choosing the top three.

### CH06: Measuring and Governing Architecture Characteristics

- [ch06-defining-and-measuring-characteristics.md](references/ch06-defining-and-measuring-characteristics.md): read when a characteristic is vague or disputed, when choosing operational or process metrics (latency statistics, performance budgets, page weight, coverage, deployability), or when building a shared glossary.
- [ch06-fitness-functions-and-governance.md](references/ch06-fitness-functions-and-governance.md): read when designing architecture governance, writing cycle, layer or main-sequence fitness functions, handling metric gaming, or planning chaos-style production checks.
- [ch06-structural-metrics-and-complexity.md](references/ch06-structural-metrics-and-complexity.md): read when assessing code structure, computing or interpreting Cyclomatic Complexity, setting CC thresholds, or reviewing AI-generated code for accidental complexity.

### CH07: The Scope of Architectural Characteristics

- [ch07-architecture-quantum-and-coupling.md](references/ch07-architecture-quantum-and-coupling.md): read when defining or testing a quantum, classifying a coupling (semantic, implementation, static, dynamic), or explaining brittleness and why code metrics miss scope.
- [ch07-communication-and-dynamic-coupling.md](references/ch07-communication-and-dynamic-coupling.md): read when a sync call joins services with different scalability, availability or performance profiles, or when weighing a queue as a buffer.
- [ch07-scoping-decision-playbook.md](references/ch07-scoping-decision-playbook.md): read when choosing monolith vs distributed, sizing quanta, picking persistence and communication, working a kata like Going Green, or scoping cloud-hosted systems.

Merged section maps: [source-maps.md](references/source-maps.md).

## Scripts

Python 3 standard library only; run any script with `--help` for its arguments.

| Script | Purpose |
|---|---|
| `scripts/complexity_gate.py` (ch06) | Cyclomatic-complexity fitness function for Python source. |
| `scripts/dependency_fitness.py` (ch06) | Structural fitness function: dependency cycles, layer rules, main-sequence distance. |
| `scripts/quantum_finder.py` (ch07) | Find architecture quanta in a system description. |

<!-- END GENERATED -->
