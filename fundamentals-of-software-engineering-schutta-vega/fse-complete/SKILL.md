---
name: fse-complete
description: Whole-book guide to Schutta and Vega's "Fundamentals of Software Engineering: From Coder to Engineer". Use for broad questions about growing from programmer to engineer or when a task spans several areas (reading and writing code, testing, modeling, UI, data, architecture, production delivery, productivity, learning, AI-assisted coding, soft skills, career). Routes to per-topic references from all 15 chapters and bundles 10 tested scripts.
---

# Fundamentals of Software Engineering, complete (Schutta and Vega, O'Reilly 2025)

Operating model for engineering work condensed from the whole book. This file holds the cross-cutting rules and the router; depth lives in `references/` (chapter-prefixed topic files) and checks in `scripts/`. Theme skills (`fse-theme-*`) cover the same material in smaller slices.

## Core rules (apply without opening references)

1. **Engineer, not just coder.** Own the whole lifecycle and its qualities; code is communication with people first.
2. **Problem before solution.** Find the real need, the root cause and the shared vocabulary before writing code.
3. **Read before you write.** Get context from people and history, trace real flows, read tests first, and reuse before building.
4. **Simple, readable, small.** Tiny focused units, honest names, no clever code, reviews about substance.
5. **Change safely.** Tests as a habit, characterization tests before refactors, small reversible commits, coverage as a signal only.
6. **Design is trade-offs.** Name the factors, rank quality attributes, pick the least-bad option, and record why in ADRs.
7. **Design for real users and real data.** Accessibility and internationalization from the start; data choices fit the workload and the cost of being wrong.
8. **Production from day one.** Externalized configuration and secrets, flags with expiry, graceful failure, layered security, automated pipelines, progressive rollout, monitoring after launch.
9. **Invest in multipliers deliberately.** Tool fluency, automation that pays back, spaced learning, and AI used with full ownership and review.
10. **Grow through people and plans.** Clear communication, influence without authority, protected focus, and a career planned backward with evidence of wins.

## Map of the book

| Area | Question | Theme skill | Chapters |
|---|---|---|---|
| Mindset | What makes someone an engineer? | fse-theme-career-and-collaboration | 1 |
| Code craft | How do I read, write and safely change code? | fse-theme-code-craft | 2, 3, 6 |
| Testing and delivery | How do I keep changes safe and ship them? | fse-theme-testing-and-delivery | 5, 10 |
| Design and architecture | How do I make and record design decisions? | fse-theme-design-and-architecture | 4, 7, 8, 9 |
| Multipliers | How do I work faster, keep learning and use AI well? | fse-theme-productivity-learning-ai | 11, 12, 15 |
| People and career | How do I communicate, influence and grow? | fse-theme-career-and-collaboration | 13, 14 |

For a task-by-task playbook, a symptom-to-fix map and a growth checklist, read [references/engineering-playbook.md](references/engineering-playbook.md).

## Default workflow

1. Place the task in an area above. If it spans areas, start with [references/engineering-playbook.md](references/engineering-playbook.md).
2. Apply the core rules; open only the references whose "read when" line matches.
3. Run the matching script whenever a measurable check applies.
4. State assumptions and which rule or reference drove each recommendation.

<!-- BEGIN GENERATED: run tools/build_bundles.py to refresh -->

## References by chapter

Each link is one level deep; read only the files whose description matches the task.

### CH01: Programmer to Engineer

- [ch01-engineer-mindset-and-growth.md](references/ch01-engineer-mindset-and-growth.md): read when someone asks how to grow, what separates a programmer from an engineer, whether their background (boot camp, self-taught, no CS degree, weak math) holds them back, what school did not teach them, or how to plan learning and find mentors. Also holds the practice suggestions and resource list.
- [ch01-legacy-code-fresh-eyes-and-golden-rule.md](references/ch01-legacy-code-fresh-eyes-and-golden-rule.md): read when someone joins a team or inherits an unfamiliar codebase, wants to question an established practice without offending anyone, or needs guidance on writing readable code, documentation and diagrams for future maintainers.
- [ch01-problem-first-engineering.md](references/ch01-problem-first-engineering.md): read when a developer is about to jump into code, faces a solution-shaped request, needs root-cause analysis (Five Whys), is choosing between quick fix and real fix, is tempted to build something that may already exist, or is weighing overengineering versus pragmatism and shift-left practices.

### CH02: Reading Code

- [ch02-ide-navigation-and-reading-tests.md](references/ch02-ide-navigation-and-reading-tests.md): read when choosing concrete IDE techniques (usages, implementations, jump to definition, call and type hierarchies, structure views, inspections, habit of learning one feature a week) or when using tests to learn intended behavior, workflows, and edge cases.
- [ch02-mindset-biases-and-ai.md](references/ch02-mindset-biases-and-ai.md): read when framing why existing code is hard (four problems, legacy framing, code dating), when a developer or team is arguing from bias, when deciding how far to trust AI explanations, or when building a code-reading practice plan.
- [ch02-onboarding-and-software-archeology.md](references/ch02-onboarding-and-software-archeology.md): read when joining a project or exploring an unfamiliar repository; covers onboarding order, lightweight docs, the misleading-metric pitfall, landmark tracing, debugger confirmation, version-control hotspots, and generated diagrams.

### CH03: Writing Code

- [ch03-code-review-practice.md](references/ch03-code-review-practice.md): read when performing or receiving a code review, fixing a rubber-stamp review culture, or wording critical feedback.
- [ch03-learning-and-deliberate-practice.md](references/ch03-learning-and-deliberate-practice.md): read when a developer asks how to improve, which language to learn next, or wants a practice routine and further reading.
- [ch03-readable-simple-code.md](references/ch03-readable-simple-code.md): read when refactoring, sizing classes and methods, naming things, deciding whether a comment belongs, documenting behavior through tests or contracts, or spotting clever and error-prone code.
- [ch03-reuse-and-quality-metrics.md](references/ch03-reuse-and-quality-metrics.md): read when deciding whether to build or reuse, choosing or interpreting code metrics, or introducing a linter or analyzer to an existing codebase.

### CH04: Modeling

- [ch04-diagram-catalog.md](references/ch04-diagram-catalog.md): read when choosing which diagram to create, judging formality for an audience, or explaining why and when modeling pays off; includes a selection matrix and workshop techniques.
- [ch04-modeling-practices-and-tools.md](references/ch04-modeling-practices-and-tools.md): read when drawing, reviewing or cleaning up a diagram, setting team diagram standards, choosing a tool, deciding on diagrams as code, or planning practice exercises.

### CH05: Automated Testing

- [ch05-code-coverage.md](references/ch05-code-coverage.md): read when interpreting a coverage report, setting or challenging a coverage gate, or detecting coverage gaming.
- [ch05-practice-plan.md](references/ch05-practice-plan.md): read when coaching someone to build the habit, or planning improvements to an under-tested codebase.
- [ch05-test-pyramid-and-mix.md](references/ch05-test-pyramid-and-mix.md): read when choosing between unit, integration and E2E tests, sizing a suite, or diagnosing a slow or flaky top-heavy suite.
- [ch05-why-test-and-what-to-skip.md](references/ch05-why-test-and-what-to-skip.md): read when justifying testing to a skeptic, using tests to learn a codebase, spotting design smells via testability, or deciding what to leave untested.
- [ch05-writing-tests-playbook.md](references/ch05-writing-tests-playbook.md): read when actually writing tests: setup, TDD vs test-last, assertions, SUT, mocking, integration and API-level E2E recipes, naming, AI-assisted test writing.

### CH06: Exploring and Modifying Unfamiliar Systems

- [ch06-mental-models.md](references/ch06-mental-models.md): read when the developer feels overwhelmed, needs to pick a slice to study, or wants to diagram a flow (diagram selection, Mermaid progression, scope ladder, AI drafting).
- [ch06-orientation-and-onboarding.md](references/ch06-orientation-and-onboarding.md): read when someone is joining a project or asks where to start; covers who to ask, documentation pitfalls, recognizing architecture from layout, and a ten-step first-week checklist.
- [ch06-practice-drills.md](references/ch06-practice-drills.md): read when the developer wants exercises to build these skills or reading suggestions.
- [ch06-safe-change-playbook.md](references/ch06-safe-change-playbook.md): read before any refactor, bug fix or feature in legacy code; covers characterization tests, the refactor-or-defer table, change management, splitting work, commits, branches and PRs.
- [ch06-tracing-execution-flow.md](references/ch06-tracing-execution-flow.md): read when tracing behavior or a bug through a system, locating entry points or dependencies, probing an API, or facing an in-house framework.

### CH07: User Interface Design

- [ch07-accessibility-and-globalization.md](references/ch07-accessibility-and-globalization.md): read when planning or reviewing accessibility, localization, internationalization, RTL support or cultural fit.
- [ch07-discoverability-errors-and-destructive-actions.md](references/ch07-discoverability-errors-and-destructive-actions.md): read when deciding what to expose or hide, designing shortcuts, writing error messages, building delete or other irreversible flows, or setting practice exercises.
- [ch07-usability-qualities-and-prioritization.md](references/ch07-usability-qualities-and-prioritization.md): read when auditing usability or deciding which qualities to optimize for a product's usage pattern; includes the efficiency multiplier example.
- [ch07-user-research-and-defaults.md](references/ch07-user-research-and-defaults.md): read when gathering user requirements, considering secondary users, or choosing, persisting and instrumenting defaults.
- [ch07-visual-design-principles.md](references/ch07-visual-design-principles.md): read when laying out or critiquing a screen's visual hierarchy, grouping, alignment and consistency.

### CH08: Working with Data

- [ch08-consistency-caching-and-growth.md](references/ch08-consistency-caching-and-growth.md): read when choosing consistency models, reasoning about CAP, designing or rejecting a cache, or planning scaling (replicas, sharding) and growth reviews.
- [ch08-data-types-and-formats.md](references/ch08-data-types-and-formats.md): read when deciding structured versus unstructured handling, choosing JSON, XML, CSV or YAML, or handling binary data, timestamps or datasets too large for memory.
- [ch08-database-selection-and-persistence.md](references/ch08-database-selection-and-persistence.md): read when picking a database family, choosing between raw SQL, a repository and an ORM, or setting up connection pools and transaction boundaries.
- [ch08-migration-and-schema-evolution.md](references/ch08-migration-and-schema-evolution.md): read when planning a data migration, ETL or dual-running sync, or adding versioned schema and data migrations.
- [ch08-query-performance.md](references/ch08-query-performance.md): read when a query or endpoint is slow, when designing indexes or pagination, reading EXPLAIN output, sizing a pool from metrics, or trading ORM readability for SQL speed.

### CH09: Software Architecture

- [ch09-adrs-and-architecture-diagrams.md](references/ch09-adrs-and-architecture-diagrams.md): read when writing or reviewing an ADR, managing ADR status, or choosing a diagram for an audience.
- [ch09-architecture-thinking-and-trade-offs.md](references/ch09-architecture-thinking-and-trade-offs.md): read when scoping a new system, running a trade-off analysis (library vs service worked example), or deciding whether something is architecture or design.
- [ch09-evolutionary-architecture-and-fitness-functions.md](references/ch09-evolutionary-architecture-and-fitness-functions.md): read when working in Agile teams, writing a hypothesis for an architectural change, or designing and maintaining fitness functions (includes sample checks).
- [ch09-practice-with-architectural-katas.md](references/ch09-practice-with-architectural-katas.md): read when the user wants to practice architecture, run a kata session or interview, or asks for further reading.
- [ch09-quality-attributes-and-styles.md](references/ch09-quality-attributes-and-styles.md): read when extracting and ranking quality attributes from requirements, persuading stakeholders, or choosing between monolithic and distributed styles.

### CH10: To Production

- [ch10-configuration-flags-and-secrets.md](references/ch10-configuration-flags-and-secrets.md): read when externalizing config, choosing config files vs env vars vs secret managers, or designing and cleaning up feature flags.
- [ch10-deployment-pipeline-and-release.md](references/ch10-deployment-pipeline-and-release.md): read when choosing a branching model, naming branches, writing deploy or rollback automation, picking a rollout strategy, or building CI/CD.
- [ch10-monitoring-maintenance-and-practice.md](references/ch10-monitoring-maintenance-and-practice.md): read when setting up post-launch monitoring, using AI on logs, writing an update policy, or coaching production habits.
- [ch10-production-gap-performance-and-errors.md](references/ch10-production-gap-performance-and-errors.md): read when debugging prod-only failures, choosing performance optimizations, or designing error handling and log content.
- [ch10-security-and-compliance.md](references/ch10-security-and-compliance.md): read when touching TLS, authentication, sessions, MFA, PII, encryption at rest, GDPR/CCPA, HIPAA, PCI DSS or SBOMs.

### CH11: Powering Up Your Productivity

- [ch11-command-line-and-keyboard.md](references/ch11-command-line-and-keyboard.md): read when teaching shell composition, aliases, history and fuzzy finding, alternative shells, touch typing, shortcut layers, Emacs/vi bindings, clipboard managers or text expanders.
- [ch11-environment-and-ergonomics.md](references/ch11-environment-and-ergonomics.md): read when tuning an IDE, OS or physical workspace, choosing fonts/themes/keyboards, handling Git safety basics, or warning about customization time sinks.
- [ch11-learning-habits-and-knowledge.md](references/ch11-learning-habits-and-knowledge.md): read when building learning cadence, team knowledge sharing, keeping up with language releases, setting up personal knowledge management, or planning practice exercises and further reading.
- [ch11-strategic-automation.md](references/ch11-strategic-automation.md): read when deciding whether and how far to automate a task, including the decision procedure, worked example and pitfalls.

### CH12: Learning to Learn

- [ch12-evaluating-new-technology.md](references/ch12-evaluating-new-technology.md): read when someone feels FOMO, wants to adopt a hyped tool, or needs a method to judge staying power (resume-driven development, pendulum patterns, radars, network sharding).
- [ch12-how-learning-works.md](references/ch12-how-learning-works.md): read when explaining why cramming fails, designing retention (stories, spacing), helping someone who is stuck, or tailoring guidance to Shu Ha Ri or Dreyfus stage.
- [ch12-introducing-technology-to-teams.md](references/ch12-introducing-technology-to-teams.md): read when spreading knowledge or proposing a technology inside an organization: book clubs, hack days, showcases, talks, internal conferences, architectural briefings, workshops, legacy constraints, trial projects.
- [ch12-learning-habit-and-cadence.md](references/ch12-learning-habit-and-cadence.md): read when building a personal learning plan: depth levels, weekly/monthly/yearly cadence, calendar blocks, learning out loud, AI-assisted study, avoiding burnout, practice projects.

### CH13: Mastering Soft Skills in the Tech World

- [ch13-communication-channels-and-meetings.md](references/ch13-communication-channels-and-meetings.md): read when choosing a channel, writing workplace messages, attending or organizing meetings, preparing presentations, or arguing that code should communicate.
- [ch13-enterprise-operator-and-audience.md](references/ch13-enterprise-operator-and-audience.md): read when a distorted message, rumored standard, or hostile room appears, or when translating technical work for business or executive audiences.
- [ch13-influence-and-stakeholders.md](references/ch13-influence-and-stakeholders.md): read when the user must persuade without authority, pick a messenger, or map and manage stakeholders on the power/interest grid.
- [ch13-time-management-and-focus.md](references/ch13-time-management-and-focus.md): read for calendar defense, maker versus manager schedules, interruption recovery, Pomodoro and habit techniques, and the practice plan and further reading.

### CH14: Career Management

- [ch14-career-paths-and-planning.md](references/ch14-career-paths-and-planning.md): read when the user is choosing a direction, comparing tracks or company types, building a milestone plan, or weighing an offer against life circumstances; also holds the practice exercises and further reading.
- [ch14-deliberate-learning-and-tech-radar.md](references/ch14-deliberate-learning-and-tech-radar.md): read when deciding what to learn, building a T-shaped profile, or creating and maintaining a personal technology radar.
- [ch14-interviewing-playbook.md](references/ch14-interviewing-playbook.md): read when preparing for, conducting, or recovering from an interview, including AI-assisted research and mock interviews.
- [ch14-sustainability-and-remote-work.md](references/ch14-sustainability-and-remote-work.md): read when the user reports stress, burnout, trouble disconnecting, distributed-team friction, or is deciding whether remote work suits them.
- [ch14-wins-confidence-and-network.md](references/ch14-wins-confidence-and-network.md): read when setting up a wins log, coaching through imposter syndrome, or planning community involvement and relationship maintenance.

### CH15: The AI-Powered Software Engineer

- [ch15-ai-coding-assistants-and-usage-policy.md](references/ch15-ai-coding-assistants-and-usage-policy.md): read when choosing between chatbot, inline and agentic tools, setting up an agentic task, or writing personal or team AI usage guidelines.
- [ch15-ai-concepts-capabilities-limits.md](references/ch15-ai-concepts-capabilities-limits.md): read when explaining AI, ML, deep learning, GenAI or LLM concepts, picking a temperature, or deciding whether a task suits AI given its strengths and its known limitations.
- [ch15-prompt-engineering-playbook.md](references/ch15-prompt-engineering-playbook.md): read when writing, critiquing or rewriting a prompt, or choosing zero/one/few-shot, delimited structure or task decomposition.
- [ch15-reviewing-ai-code-and-career-shift.md](references/ch15-reviewing-ai-code-and-career-shift.md): read when reviewing AI-generated code, judging whether vibe coding is acceptable, addressing job-loss worries, reframing productivity, or planning practice exercises.

Merged section maps: [source-maps.md](references/source-maps.md).

## Scripts

Python 3 standard library only; run any script with `--help` for its arguments.

| Script | Purpose |
|---|---|
| `scripts/code_shape_report.py` (ch03) | Report shape warnings for Python source: long functions, deep nesting, |
| `scripts/coverage_hotspots.py` (ch05) | Summarize a Cobertura coverage.xml into actionable hotspots. |
| `scripts/git_hotspots.py` (ch06) | Rank files in an unfamiliar repository by change activity, from git history. |
| `scripts/contrast_check.py` (ch07) | WCAG 2.x color contrast checker for foreground/background pairs. |
| `scripts/migration_batch_planner.py` (ch08) | Plan batches and timing for a big bang or phased data migration. |
| `scripts/adr_tool.py` (ch09) | Create and lint Architectural Decision Records (ADRs) kept as Markdown files. |
| `scripts/audit_feature_flags.py` (ch10) | Audit a feature-flag registry for hygiene problems. |
| `scripts/scan_config_risks.py` (ch10) | Scan source and config files for production-readiness risks in configuration. |
| `scripts/automation_payback.py` (ch11) | Automation payback calculator (Strategic Automation, FSE Chapter 11). |
| `scripts/spaced_review_schedule.py` (ch12) | Spaced-repetition review scheduler for things you are learning. |

<!-- END GENERATED -->

## Provenance

Original synthesis for agent use; it does not reproduce the book's text, code, tables or figures. `references/source-maps.md` maps every chapter section to the file that covers it. This folder is regenerated from the chapter skills by `tools/build_bundles.py`.
