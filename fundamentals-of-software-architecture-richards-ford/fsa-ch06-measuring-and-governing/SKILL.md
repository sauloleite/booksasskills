---
name: fsa-ch06-measuring-and-governing
description: Turns vague architecture characteristics into objective operational, structural and process measures, and governs them with automated fitness functions (cycle checks, layer rules, main-sequence distance, complexity gates, chaos-style production checks). Based on Chapter 6 of Richards and Ford's "Fundamentals of Software Architecture" (2nd ed.). Use when defining measurable "-ilities", choosing latency or deployability metrics, setting Cyclomatic Complexity thresholds, writing architecture tests for CI, or stopping modularity erosion.
---

# Measuring and Governing Architecture Characteristics (FSA Chapter 6)

Purpose: help an agent convert fuzzy quality goals ("fast", "agile", "modular") into agreed, measurable definitions, then protect them with automated, objective checks that keep working under deadline pressure. Measurement without governance decays; governance without agreed definitions breeds arguments. This skill covers both halves.

## Key decision rules (apply without opening references)

1. **Define before you measure.** Characteristics fail as targets because they are not physical quantities, mean different things to different departments, and are often composites. Decompose composites (agility into modularity, testability, deployability) until each leaf has a concrete metric, then record one organization-wide definition (a ubiquitous language for architecture).
2. **Classify each measure**: operational (runtime behavior), structural (code and component shape), or process (how the team builds and ships). The class decides tooling and when the check runs.
3. **Never govern latency by the mean alone.** A small slice of very slow requests disappears in an average; add max and high percentiles.
4. **Prefer statistical baselines over arbitrary numbers.** Model the metric's normal range over time and alert on deviation; a breach means either the model or the system is wrong, and both are worth learning.
5. **Ask which "performance".** Request/response time, per-part budgets (first visible render), and page-weight budgets in bytes are different targets; byte budgets follow from bandwidth physics and constrain framework choices.
6. **Cyclomatic Complexity is blunt.** It flags complexity but cannot say whether it is essential (hard problem) or accidental (poor design or poor partitioning). Check partitioning first. Industry ceiling is about 10; the authors prefer under 5; above 50 no test coverage redeems the code. Apply the same gate to AI-generated code, which tends toward brute-force accidental complexity.
7. **Coverage is not correctness.** 100% coverage with weak or absent assertions proves little; add an "every test asserts" rule or mutation testing.
8. **Process priorities drive structure.** If testability and deployability rank high, invest in modularity and isolation. Anything can become an architecture characteristic once it meets the three criteria (nondomain, structural influence, critical to success).
9. **Govern with fitness functions**: any mechanism that objectively assesses one or more characteristics. They are a lens over existing tools (architecture unit tests, metrics, monitors, chaos experiments), not a product to install.
10. **Guard the important-but-not-urgent automatically.** Modularity erodes through casual imports and "ask forgiveness" layer bypasses; code review is too late. Fail the build on cycles, forbidden layer edges, and excessive main-sequence distance.
11. **Build fitness functions with developers.** Explain each check's purpose before imposing it; ivory-tower rules get gamed or resented. Expect metric gaming and close the obvious loopholes; fitness functions mainly stop accidental lapses, not determined rule-breakers.
12. **Extend governance into production.** Chaos-style checks (failure and latency injection, conformity, security and orphan-service scans) treat failure as inevitable and rehearse it.
13. **Think checklist, not bureaucracy.** Fitness functions are lightweight automated reminders of principles that compete with many other priorities.

## Default workflow

1. Collect the characteristics in play (from requirements or prior chapters' analysis) and the stakeholders' exact wording.
2. Decompose composites; classify each leaf as operational, structural or process.
3. For each leaf, define metric, statistic, scope, measurement point and success rule (fixed budget or statistical baseline). Note owners.
4. Identify the structural consequences of the priorities (modularity, isolation, layering).
5. Pick fitness functions per characteristic and stage (build, deploy, production); run the scripts below for dependency and complexity checks.
6. Review each check with developers, set thresholds and a documented exception path, wire into CI or monitoring.
7. Output: a measurement glossary, a fitness-function list with thresholds and stages, and any violations found with suggested fixes.

## References

- [references/defining-and-measuring-characteristics.md](references/defining-and-measuring-characteristics.md): read when a characteristic is vague or disputed, when choosing operational or process metrics (latency statistics, performance budgets, page weight, coverage, deployability), or when building a shared glossary.
- [references/structural-metrics-and-complexity.md](references/structural-metrics-and-complexity.md): read when assessing code structure, computing or interpreting Cyclomatic Complexity, setting CC thresholds, or reviewing AI-generated code for accidental complexity.
- [references/fitness-functions-and-governance.md](references/fitness-functions-and-governance.md): read when designing architecture governance, writing cycle, layer or main-sequence fitness functions, handling metric gaming, or planning chaos-style production checks.
- [references/source-map.md](references/source-map.md): read when you need to know which file covers a given chapter section.

## Scripts

Python 3, standard library only; each supports `--help`. Both exit 1 on violations, so they can run directly as CI fitness functions.

- Run `python3 scripts/dependency_fitness.py edges.txt --rules layers.ini --abstractness abs.txt --tolerance 0.5` to detect dependency cycles (with an example path per cycle), report layer-rule violations, and compute distance from the main sequence (D = |A + I - 1|) per module. Edge file: `source -> target` per line; rules file: `[layers]` globs and `[allow]` edges; abstractness file: `module abstract_types total_types`. `--rules` and `--abstractness` are optional; add `--json` for machine output, `--allow-cycles` to report without failing.
- Run `python3 scripts/complexity_gate.py src/ --max 10 --target 5 --allow cc_allow.txt` to compute Cyclomatic Complexity per Python function, fail above `--max`, warn above `--target`, and exempt documented essential-complexity functions listed as `path::qualified_name`.
