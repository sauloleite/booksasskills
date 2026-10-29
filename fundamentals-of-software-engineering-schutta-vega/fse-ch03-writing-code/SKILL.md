---
name: fse-ch03-writing-code
description: Guidance for writing code humans can read, based on Chapter 3 of Schutta and Vega's "Fundamentals of Software Engineering". Covers reuse before building, quality metrics and analyzers, cohesion and coupling, composition, short methods, naming, comments versus tests and contracts, avoiding clever code, humane code reviews, and learning languages. Use when deciding whether to write or reuse code, refactoring or reviewing code (human or AI-generated), adding linters to a legacy project, choosing metrics, or planning a developer's coding practice.
---

# Writing Code (FSE Chapter 3)

Purpose: help a developer, or an agent acting for one, produce and review code whose first audience is the next human reader. The compiler accepts any valid syntax; the real test is whether a teammate can grasp intent quickly and change it safely. This matters more with AI assistants, not less: reviewing generated code well requires the judgment that comes from writing good code yourself, and AI will happily write code for problems that should not need new code at all.

## Decision rules (apply even without opening references)

1. Reuse before writing. Check, in order: existing codebase, language and standard library, the framework in use, utility libraries already on the classpath, any other existing dependency, reputable open source. Write new code only if all fail. Vet new dependencies' transitive footprint and follow org policy.
2. Question inherited patterns. Today's best practice can be tomorrow's anti-pattern. Do not copy code (from the repo, the web or an AI) you cannot explain.
3. Metrics inform, never dictate. Contextualize (a facade is supposed to be highly coupled), tie metrics to goals, watch trends over short horizons, and never rate people by lines of code.
4. Retrofit analyzers with a ratchet. On an existing project, enable a few team-agreed rules, fix to zero, add a couple more, repeat. Never turn on every rule at once.
5. Make desired metrics visible. Publishing and celebrating a number (for example coverage) changes behavior.
6. High cohesion, low coupling is the root principle behind most design advice.
7. Smaller is better: less code, less boilerplate (generated code still costs maintenance), classes that fit on one screen.
8. Prefer composition; use inheritance only for a genuine, stable "is-a". Reuse is a side effect, not a reason to inherit.
9. Methods: aim for single-digit lines, one job each. A name containing "and", "or" or "but", or a name you cannot find, means split it.
10. Separate intent from implementation: a function's name should tell the reader what it does without opening the body. Lay out classes like an inverted pyramid (headline, summary, details).
11. Comments: rename or simplify first. Keep comments only for "why", non-obvious choices, and warnings. Delete change-history banners; version control owns history.
12. Document behavior with tests; document service APIs with consumer-driven contracts.
13. Cut accidental complexity; accept essential complexity. Default to simple, and be skeptical of revolutionary claims.
14. Ban error-prone forms (such as brace-less single-line `if`) in team standards and enforce with static analysis.
15. Reviews: automate style; spend human attention on names, readability, duplication, observability, interface consistency, error-prone forms, model correctness and abstraction choice. Work in small batches so review is real.
16. Review tone: about the code, not the coder; questions over verdicts; note positives; no sarcasm; raise serious concerns one-on-one.
17. Grow deliberately: learn contrasting-paradigm languages, and practice with katas, open source and periodic refreshers.

## Default workflow

1. Before coding: walk the reuse ladder and state which rung solves the need, or why none does.
2. While coding: write tests alongside; keep methods tiny and intention-named; compose; avoid error-prone forms; let IDE analyzers flag issues as you type.
3. Before review: run the shape report (below) or the team's analyzer; fix or justify each flag; replace "what" comments with better names.
4. In review (giving or receiving): follow the attention order in rule 15 and the tone rules in rule 16; push back on oversized batches.
5. Afterward: share interesting defects with the team; schedule the next practice item.

## References

- [references/reuse-and-quality-metrics.md](references/reuse-and-quality-metrics.md): read when deciding whether to build or reuse, choosing or interpreting code metrics, or introducing a linter or analyzer to an existing codebase.
- [references/readable-simple-code.md](references/readable-simple-code.md): read when refactoring, sizing classes and methods, naming things, deciding whether a comment belongs, documenting behavior through tests or contracts, or spotting clever and error-prone code.
- [references/code-review-practice.md](references/code-review-practice.md): read when performing or receiving a code review, fixing a rubber-stamp review culture, or wording critical feedback.
- [references/learning-and-deliberate-practice.md](references/learning-and-deliberate-practice.md): read when a developer asks how to improve, which language to learn next, or wants a practice routine and further reading.
- [references/source-map.md](references/source-map.md): read to check which file covers a given chapter section.

## Scripts

Run `python3 scripts/code_shape_report.py <files-or-dirs>` to compute, for Python source, functions and classes that exceed shape thresholds: body lines (default over 9), block nesting (over 2), parameters (over 4), cyclomatic complexity (over 5), class length (over 60 lines), plus names containing and/or/but/then. Add `--json` for machine-readable output, `--fail-on-findings` to exit 1 in CI, and `--max-body-lines`, `--max-nesting`, `--max-params`, `--max-complexity`, `--max-class-lines` to tune. Treat every flag as a question for judgment (rule 3), not as a defect.
