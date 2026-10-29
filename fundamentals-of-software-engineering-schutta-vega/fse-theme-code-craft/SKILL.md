---
name: fse-theme-code-craft
description: Theme skill on day-to-day work with code from Schutta and Vega's "Fundamentals of Software Engineering" (chapters 2, 3 and 6). Use when reading or onboarding onto an unfamiliar or legacy codebase, tracing execution, finding hotspots in git history, writing readable and simple code, deciding what to reuse, reviewing or receiving code reviews, or making safe, small changes and refactors in existing systems.
---

# Code craft: reading, writing and changing code (Fundamentals of Software Engineering, ch. 2, 3, 6)

Most engineering time goes into code that already exists. This theme joins reading it, writing code others can read, and changing inherited systems without breaking them.

## Cross-chapter rules

1. **Reading is the main activity.** Train it deliberately, and expect AI-generated code to raise its importance.
2. **Context before code.** Ask people first (product owner, current engineers, original authors), then docs and ADRs, verifying them against the running system.
3. **Explore from landmarks.** Start at entry points or a visible UI element, trace a real request with growing depth (devtools, API client, logs, debugger), and read tests before implementation.
4. **Let history guide attention.** Files that change often and with many authors are where risk and knowledge live; measure with `scripts/git_hotspots.py`.
5. **Watch your biases.** Familiarity and ownership make code look better than it is; check names and catch-all exception handlers before trusting them.
6. **Reuse before writing.** Codebase, language, framework, vetted libraries, then open source; question patterns you cannot explain, including AI suggestions.
7. **Write for the reader.** Small single-purpose methods, intention-revealing names, comments only for why and warnings, no clever code. Check shape with `scripts/code_shape_report.py`.
8. **Metrics inform, never rule.** Read them in context and over time; never rate people by lines of code; adopt static analysis rules gradually.
9. **Reviews are for substance.** Automate style, keep changes small, critique code not people.
10. **Change safely.** Pin current behavior with characterization tests before refactoring, keep refactors separate from behavior changes, and ship small, reversible, monitored commits with clear refactor-now-or-later criteria.

## Default workflow

1. Orient: purpose, people, docs, folder structure, dependencies (ch06, ch02).
2. Trace one real flow end to end and sketch a slice-sized mental model (ch06).
3. Read the tests and hotspots around the area you must change (ch02, ch06).
4. Pin behavior, change in small steps, keep the code readable, and request a substantive review (ch06, ch03).

<!-- BEGIN GENERATED: run tools/build_bundles.py to refresh -->

## References by chapter

Each link is one level deep; read only the files whose description matches the task.

### CH02: Reading Code

- [ch02-ide-navigation-and-reading-tests.md](references/ch02-ide-navigation-and-reading-tests.md): read when choosing concrete IDE techniques (usages, implementations, jump to definition, call and type hierarchies, structure views, inspections, habit of learning one feature a week) or when using tests to learn intended behavior, workflows, and edge cases.
- [ch02-mindset-biases-and-ai.md](references/ch02-mindset-biases-and-ai.md): read when framing why existing code is hard (four problems, legacy framing, code dating), when a developer or team is arguing from bias, when deciding how far to trust AI explanations, or when building a code-reading practice plan.
- [ch02-onboarding-and-software-archeology.md](references/ch02-onboarding-and-software-archeology.md): read when joining a project or exploring an unfamiliar repository; covers onboarding order, lightweight docs, the misleading-metric pitfall, landmark tracing, debugger confirmation, version-control hotspots, and generated diagrams.

### CH03: Writing Code

- [ch03-code-review-practice.md](references/ch03-code-review-practice.md): read when performing or receiving a code review, fixing a rubber-stamp review culture, or wording critical feedback.
- [ch03-learning-and-deliberate-practice.md](references/ch03-learning-and-deliberate-practice.md): read when a developer asks how to improve, which language to learn next, or wants a practice routine and further reading.
- [ch03-readable-simple-code.md](references/ch03-readable-simple-code.md): read when refactoring, sizing classes and methods, naming things, deciding whether a comment belongs, documenting behavior through tests or contracts, or spotting clever and error-prone code.
- [ch03-reuse-and-quality-metrics.md](references/ch03-reuse-and-quality-metrics.md): read when deciding whether to build or reuse, choosing or interpreting code metrics, or introducing a linter or analyzer to an existing codebase.

### CH06: Exploring and Modifying Unfamiliar Systems

- [ch06-mental-models.md](references/ch06-mental-models.md): read when the developer feels overwhelmed, needs to pick a slice to study, or wants to diagram a flow (diagram selection, Mermaid progression, scope ladder, AI drafting).
- [ch06-orientation-and-onboarding.md](references/ch06-orientation-and-onboarding.md): read when someone is joining a project or asks where to start; covers who to ask, documentation pitfalls, recognizing architecture from layout, and a ten-step first-week checklist.
- [ch06-practice-drills.md](references/ch06-practice-drills.md): read when the developer wants exercises to build these skills or reading suggestions.
- [ch06-safe-change-playbook.md](references/ch06-safe-change-playbook.md): read before any refactor, bug fix or feature in legacy code; covers characterization tests, the refactor-or-defer table, change management, splitting work, commits, branches and PRs.
- [ch06-tracing-execution-flow.md](references/ch06-tracing-execution-flow.md): read when tracing behavior or a bug through a system, locating entry points or dependencies, probing an API, or facing an in-house framework.

Merged section maps: [source-maps.md](references/source-maps.md).

## Scripts

Python 3 standard library only; run any script with `--help` for its arguments.

| Script | Purpose |
|---|---|
| `scripts/code_shape_report.py` (ch03) | Report shape warnings for Python source: long functions, deep nesting, |
| `scripts/git_hotspots.py` (ch06) | Rank files in an unfamiliar repository by change activity, from git history. |

<!-- END GENERATED -->
