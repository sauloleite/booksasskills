# Engineering playbook and cross-chapter decisions (Fundamentals of Software Engineering)

Whole-book synthesis: playbooks for common engineering tasks, a symptom-to-fix map that crosses chapters, and a growth checklist. Chapter tags such as (ch06) point to the `chNN-*` reference files in this folder.

## Contents
- Task playbooks
- Symptom-to-fix map
- Growth checklist
- Book-wide pitfalls

## Task playbooks

### Joining a team or an unfamiliar codebase (ch02, ch06, ch01)
1. Learn the purpose from people before the code: product owner, current engineers, original authors.
2. Read the README, wiki and ADRs, and note where they disagree with reality.
3. Read the folder structure to infer the architecture; list external dependencies from config and container files.
4. Run `scripts/git_hotspots.py` on the history to find volatile files and their owners.
5. Trace one real request end to end; sketch a slice-sized model and have a teammate check it.
6. Write down a glossary of domain terms and fix the docs you found wrong.

### Implementing a change in existing code (ch06, ch03, ch05)
1. Clarify the real need and the root cause before deciding on a solution.
2. Search for existing code, framework features or vetted libraries first.
3. Pin current behavior with characterization tests if coverage is thin.
4. Separate refactoring commits from behavior changes; keep each change small and reversible.
5. Keep methods small and names honest; run `scripts/code_shape_report.py`.
6. Add tests with the change and ask for a review focused on design and correctness.

### Designing a new feature or system (ch09, ch04, ch08, ch07)
1. Ask the discovery questions and rank the top quality attributes.
2. Sketch options, compare them by weighted priorities, and choose the least-bad one.
3. Choose data formats, storage, consistency and caching by workload and cost of error.
4. Design the interface with real users in mind, including accessibility, localization and error handling; check contrast with `scripts/contrast_check.py`.
5. Record the decision as an ADR (`scripts/adr_tool.py`) and add fitness functions for the key qualities.
6. Draw only the diagrams the audience needs, kept accurate or generated.

### Shipping to production (ch10, ch05)
1. Externalize configuration and secrets; scan with `scripts/scan_config_risks.py`.
2. Put new behavior behind flags with owners and expiry; audit with `scripts/audit_feature_flags.py`.
3. Design the unhappy path: graceful degradation, clear messages, leveled logs without secrets.
4. Apply the security baseline (TLS, proven authentication, session limits, encryption at rest, dependency scanning).
5. Automate build, tests and deployment with tested rollback; pick a rollout strategy that fits risk and monitoring maturity.
6. Monitor against baselines after launch and hold a retrospective.

### Migrating data (ch08)
1. Run a proof of concept to measure throughput.
2. Plan phased batches with `scripts/migration_batch_planner.py`.
3. Version schema changes like code, keep them backward compatible, and reconcile while old and new systems run together.

### Adopting a new technology or AI tool (ch12, ch15, ch11)
1. Check fit against goals and longevity; avoid resume-driven choices.
2. Brief the team, run a workshop on real constraints, then a low-risk trial.
3. For AI tools: write a personal usage policy, give rich prompts, treat output as a draft, and review it as strictly as human code.
4. Automate repeated work only when it pays back (`scripts/automation_payback.py`).

### Growing as an engineer (ch14, ch13, ch12)
1. Set a 3 to 5 year target and work backward to milestones, including soft skills.
2. Keep a personal technology radar and a spaced review schedule (`scripts/spaced_review_schedule.py`).
3. Log wins with measurable results; review quarterly.
4. Build relationships before you need them; protect focus time; communicate in the channel that fits.

## Symptom-to-fix map

| Symptom | Likely cause | First move | Then |
|---|---|---|---|
| Afraid to touch a module | No tests, unclear behavior | Characterization tests (ch06) | Small refactors, coverage on critical logic (ch05) |
| Same files keep breaking | Hotspot with mixed responsibilities | Hotspot and coupling analysis (ch06) | Split responsibilities, add tests (ch03, ch05) |
| Reviews are rubber stamps | Large changes, style debates | Smaller PRs, automate style (ch03) | Review checklist on substance (ch03) |
| Built the wrong thing | Requested solution, not need | Ask why repeatedly, glossary (ch01) | Stakeholder mapping and earlier feedback (ch13) |
| Works locally, fails in production | Environment gap, hardcoded config | Externalize config, staging parity (ch10) | Containers, observability, canary release (ch10) |
| Architecture drifting from intent | No guardrails | Fitness functions in CI (ch09) | ADRs with governance links (ch09) |
| Slow queries as data grows | Missing indexes, N+1, no plan review | Check query plans and app traces (ch08) | Caching or scaling only after measuring (ch08) |
| Users make errors or give up | Unclear defaults and messages | Error prevention and better messages (ch07) | Quick user research, accessibility review (ch07) |
| AI-generated bugs slipping in | Weak review of generated code | Same tests and review as human code (ch15) | Personal AI policy, scale rigor to risk (ch15) |
| Feeling stuck or behind | No plan, scattered learning | Career target and radar (ch14) | Spaced learning cadence, wins log (ch12, ch14) |

## Growth checklist

- [ ] I can explain the purpose and main flows of the system I work on.
- [ ] My changes come with tests and are small enough to review well.
- [ ] I search and reuse before building, and can justify my dependencies.
- [ ] I write down design decisions and their trade-offs.
- [ ] My code is ready for production: configuration, errors, security and monitoring.
- [ ] I know my tools deeply and automate what pays back.
- [ ] I review AI output as strictly as any other code.
- [ ] I have a learning cadence and a technology radar.
- [ ] I communicate in the right channel and can explain technical work in business terms.
- [ ] I have a career target, milestones and a wins log, reviewed regularly.

## Book-wide pitfalls

- Solving the request as stated instead of the underlying problem.
- Rewriting or "improving" inherited code without first understanding and pinning its behavior.
- Chasing metrics (coverage, lines of code, utilization) instead of what they are meant to indicate.
- Adding technology for novelty rather than fit.
- Treating production readiness, accessibility or security as late add-ons.
- Letting AI or tooling replace understanding rather than amplify it.
- Neglecting communication, focus time and a deliberate career plan.
