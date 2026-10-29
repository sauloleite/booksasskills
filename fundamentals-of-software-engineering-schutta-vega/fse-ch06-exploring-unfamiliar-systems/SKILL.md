---
name: fse-ch06-exploring-unfamiliar-systems
description: Guides onboarding to and safely changing existing or legacy codebases, based on Chapter 6 of Schutta and Vega's "Fundamentals of Software Engineering". Covers big-picture discovery, reading architecture from folder layout, entry points, request tracing, dependencies, homegrown frameworks, incremental mental models, characterization tests, the scout rule, and small reversible commits and PRs. Use when joining a new project, exploring an unfamiliar repo, tracing a bug through layers, planning a refactor in legacy code, or deciding whether cleanup is worth doing now.
---

# Exploring and Modifying Unfamiliar Systems

Most engineering work happens inside systems someone else built. This skill turns Chapter 6 into a procedure an agent can follow when helping a developer understand an unfamiliar codebase and then change it without breaking it: learn why the system exists, read its shape, follow real execution paths, build a mental model one slice at a time, and only then change it in small, tested, reversible steps.

## Key decision rules

Apply these even without opening the references.

**Understanding**
1. Purpose before code. Establish the business reason, stakeholders, customers and importance of the system before reading implementation details. Ask a product person first, then current engineers, original authors if reachable, and a tech lead or architect for the reasoning behind decisions.
2. Docs are leads, not truth. Read everything (including ADRs and setup guides), log gaps for a later docs fix, and confirm with a teammate that a document matches the running version before investing time in it.
3. Name the architecture from the folder layout first: by layer, by feature, hexagonal (ports and adapters) or microservices, often a blend. It tells you where to look.
4. Start from an entry point, never a random file: main/bootstrap, controllers, listeners, scheduled jobs, lifecycle hooks, extension points, message consumers, CLI parsers, DB triggers.
5. Trace a real request with an escalating toolset: browser network tab, then an API client, then logs, then the debugger. Traces show actual behavior; docs and tests show intended behavior.
6. Inventory external dependencies from config files and container/orchestration manifests before assuming the app is self-contained.
7. For homegrown frameworks: usage examples first, then their tests, then git history; take notes; judge whether they still earn their maintenance cost.
8. Model one flow or one feature at a time. Widen scope in order: method, class plus collaborators, feature flow, cross-cutting concerns (security, transactions). Rough sketches are fine; validate them with a teammate.

**Changing**
9. Pure refactors keep tests unchanged. Run the relevant tests after every small step.
10. No coverage, no refactor: first write characterization tests that pin current behavior, including suspected bugs. Fix bugs in a separate later change.
11. Scout rule, bounded: leave touched files slightly better (names, docs, dead code, splitting long methods) but never let cleanup displace the assigned task.
12. Refactor now if the code is hard to understand, you are adding a feature or fixing a bug there, it hurts performance, or many developers change it often. Defer if it works and rarely changes, a deadline is tight, risk exceeds benefit, the change would sprawl past the task, or tests are inadequate.
13. Prefer small, reversible changes. Each change should be visible (why and how), verified (tests, review, static analysis), revertible (rollback plan) and monitored (observability).
14. Split oversized requests; push back if needed. Extract one responsibility at a time with tests between steps.
15. Commits: atomic, frequent, messages that state what and why. Branches: feature-scoped, merged within days, rebased onto main carefully (never casually on shared branches). PRs: one concern each, with problem, approach and linked issues; reviews target the solution, not the person.

## Default workflow

1. **Orient**: capture purpose, stakeholders and users; skim docs and ADRs; note doc gaps.
2. **Set up**: clone, read README and standards, review build scripts, dependencies, structure and CI/CD, install toolchain; build, test and run locally (IDE and command line), keeping shared notes.
3. **Map history**: run the hotspot script to see where change concentrates and which files move together.
4. **Trace**: pick one entry point relevant to the task and follow one request end to end.
5. **Model**: sketch the slice (flowchart or sequence diagram), refine as you learn, get it checked.
6. **Protect**: confirm or add tests that pin current behavior around the change.
7. **Change**: small atomic commits, run tests after each, scout-rule tweaks as separate commits, focused PR, rollback plan, watch monitoring after release.

When advising, say explicitly which step the developer is on and what to skip. Remind them that partial understanding is normal; even veterans do not know the whole system.

## References

- [references/orientation-and-onboarding.md](references/orientation-and-onboarding.md): read when someone is joining a project or asks where to start; covers who to ask, documentation pitfalls, recognizing architecture from layout, and a ten-step first-week checklist.
- [references/tracing-execution-flow.md](references/tracing-execution-flow.md): read when tracing behavior or a bug through a system, locating entry points or dependencies, probing an API, or facing an in-house framework.
- [references/mental-models.md](references/mental-models.md): read when the developer feels overwhelmed, needs to pick a slice to study, or wants to diagram a flow (diagram selection, Mermaid progression, scope ladder, AI drafting).
- [references/safe-change-playbook.md](references/safe-change-playbook.md): read before any refactor, bug fix or feature in legacy code; covers characterization tests, the refactor-or-defer table, change management, splitting work, commits, branches and PRs.
- [references/practice-drills.md](references/practice-drills.md): read when the developer wants exercises to build these skills or reading suggestions.
- [references/source-map.md](references/source-map.md): read to find which file covers a given chapter section.

## Scripts

- `scripts/git_hotspots.py`: run it to compute, from git history, per-file commit counts, churn (lines added plus deleted), distinct authors, last change and recent activity, plus temporal coupling (file pairs that change in the same commits). Use the output to choose what to study first and to feed the refactor-or-defer rule (rule 12).

```bash
git log --numstat --date=iso | python3 scripts/git_hotspots.py --top 15 --recent-days 90
git log --numstat --date=iso --since="1 year ago" > /tmp/log.txt
python3 scripts/git_hotspots.py /tmp/log.txt --min-shared 3 --max-files 30 --json
```

Interpretation: high commits plus several authors marks a busy shared area where refactoring pays off; low commits and old last-change marks stable code to leave alone; a high coupling degree between files in different modules signals a hidden dependency worth adding to the mental model. Bulk commits above `--max-files` are excluded from coupling.
