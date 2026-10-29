---
name: fse-ch02-reading-code
description: Playbook for understanding unfamiliar or inherited codebases: reframing legacy code, spotting reader biases, onboarding order (people, docs, ADRs, standards), software archeology (callers, landmarks, debugger, churn, generated diagrams), IDE navigation and inspections, reading tests as specification, and verifying AI explanations. Based on Chapter 2 of Schutta and Vega's "Fundamentals of Software Engineering". Use when a developer joins a project, must change brownfield code, asks "what does this code do?", wants a code-reading study plan, or relies on AI to explain a repository.
---

# Reading Code (FSE Chapter 2)

## Purpose

Professional engineers spend most of their time inside code someone else wrote, yet most training starts from a blank file. This skill gives an agent a repeatable way to help a developer build a working mental model of an existing system: frame the task correctly, check personal bias, gather context cheaply before reading line by line, explore the code with tools rather than by scrolling, treat tests as the statement of intended behavior, and confirm every hunch (including anything an AI assistant claims). Understanding is incremental; the goal is enough model to act safely, not total mastery.

## Key decision rules (apply even without opening references)

1. **Name the four problems.** A change to existing code means solving: the business problem, the previous author's mindset, a possibly wrong abstraction, and accumulated layers of old practice. Diagnose which one is blocking before proposing a fix.
2. **Respect what already works.** Code that has earned years of investment is a success. Prefer neutral labels ("existing" or "heritage" code) and avoid contempt for the predecessor, who may be the reader's past self.
3. **Check for bias before judging a design.** Ask whether a preference comes from authorship (IKEA effect), familiarity (mere-exposure effect), or being unable to see the value of features one's own language lacks (Blub paradox). Apply the same test to colleagues and to yourself.
4. **Date the code.** Infer when code was written from the frameworks, idioms and language features it uses or avoids; judge it against the norms of its era, not today's.
5. **Context before code.** Order: teammates and onboarding, then README/wiki, ADRs, and coding standards, then the editor. Minutes of reading docs can save hours in a debugger. Treat docs as possibly stale: trust, then verify.
6. **Leave documentation behind.** If docs are stale, fix them while learning; if absent, write a lightweight version answering what the service does, how it works, what it depends on, and how to run it. Prefer executable documentation (behavior-style tests) because it cannot silently drift.
7. **Distrust single metrics.** High coverage proves code ran, not that behavior was checked. Inspect the tests themselves (assertions present? meaningful?) before trusting a number.
8. **Trace from a landmark.** Pick a concrete UI element, endpoint parameter, issue, or datastore write and map it to code, walking callers backward until you reach the user action. Confirm with a breakpoint; if the path surprises you, repeat.
9. **Names and exceptions can lie.** Do not assume a function does what its name says. Be extra skeptical of broad catch-all exception handlers; they hide the real failure modes.
10. **Start with hotspots.** Files that change most often (from version control history) and their recent authors are the best first targets and the best people to ask.
11. **Read tests before implementation.** Code shows how; tests show how it is supposed to behave. Use unit tests for contracts, end-to-end or integration tests for workflows, and edge-case tests for limits and past bugs.
12. **IDE suggestions are suggestions.** Review automated inspections as a way to learn idioms; accept them only when they help.
13. **AI is a copilot, not an oracle.** It can explain a snippet but lacks business purpose and cross-repository context and can hallucinate. The human must own the model of the system; check company policy before pasting proprietary code into external tools.

## Default workflow

1. Clarify the goal: which feature, bug, or change needs understanding, and which of the four problems is likely hardest.
2. Gather context: ask teammates, read README, ADRs, coding standards, and the issue tracker. Note what looks stale.
3. Survey structure: packaging and layout (by feature or by layer), monolith versus many services, domain vocabulary, class outlines with bodies collapsed, dependency or generated class diagrams.
4. Find hotspots: change frequency over the last year, commit messages, blame for recent owners.
5. Read relevant tests: contracts, workflows, edge cases.
6. Trace a landmark end to end: run the app, map an element to code, walk callers and callees, set a breakpoint, compare reality with expectations.
7. Verify hunches: names, exception handling, AI explanations. Record open questions and ask people.
8. Leave it better: update or create lightweight docs, add missing assertions or tests, and capture new IDE tricks in a personal notes file.

## Output expectations when helping a developer

- Give a short orientation map (entry points, key modules, data stores, external dependencies) with confidence levels and what was verified versus inferred.
- List concrete next probes (a file to open, a breakpoint to set, a test to read, a person or ADR to consult) rather than generic advice.
- Flag stale docs, assertion-free tests, misleading names, and catch-all exception handling explicitly.

## References

- [references/mindset-biases-and-ai.md](references/mindset-biases-and-ai.md): read when framing why existing code is hard (four problems, legacy framing, code dating), when a developer or team is arguing from bias, when deciding how far to trust AI explanations, or when building a code-reading practice plan.
- [references/onboarding-and-software-archeology.md](references/onboarding-and-software-archeology.md): read when joining a project or exploring an unfamiliar repository; covers onboarding order, lightweight docs, the misleading-metric pitfall, landmark tracing, debugger confirmation, version-control hotspots, and generated diagrams.
- [references/ide-navigation-and-reading-tests.md](references/ide-navigation-and-reading-tests.md): read when choosing concrete IDE techniques (usages, implementations, jump to definition, call and type hierarchies, structure views, inspections, habit of learning one feature a week) or when using tests to learn intended behavior, workflows, and edge cases.
- [references/source-map.md](references/source-map.md): read to see which reference covers each chapter section.

## Scripts

None. The chapter offers qualitative techniques; version-control history analysis is covered in depth by the Chapter 6 skill.
