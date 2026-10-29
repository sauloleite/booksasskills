---
name: fse-ch05-automated-testing
description: Operational guidance on automated testing based on Chapter 5 of Schutta and Vega's "Fundamentals of Software Engineering" (O'Reilly, 2025). Covers why tests pay off (documentation, design feedback, confidence, regression safety), the test pyramid and choosing a mix, what not to test, code coverage as feedback, and the mechanics of unit, mocked, integration and end-to-end tests. Use when writing or reviewing tests, deciding which test level fits, fixing a bug, setting coverage policy, reading unfamiliar code through its tests, or coaching a developer to build a testing habit.
---

# Automated Testing (FSE Chapter 5)

## Purpose

Help a developer treat testing as a steady habit that produces documentation, better design and the freedom to change code, not as a coverage chore. Apply the rules below by default; open a reference only when the task needs depth.

## Key decision rules

1. **Small and steady beats big-bang.** Add one meaningful test with each change; on weak codebases improve incrementally (for example, one new test per developer per day).
2. **Read tests before code.** In unfamiliar areas, read test names first; they list supported and unsupported behaviors. Negative tests often explain "bugs" that are really unsupported features.
3. **Hard-to-test means badly designed.** If one method needs a database, logger and mailer to test, it violates single responsibility; split and inject collaborators instead of piling on mocks.
4. **Follow the pyramid.** Many fast unit tests, fewer integration tests, very few E2E tests. Cost, slowness and brittleness rise toward the top; confidence about the whole system rises too.
5. **Pick the lowest level that can catch the defect.** Logic: unit. Wiring between your components or with a datastore: integration. A critical user journey: one E2E happy path, with edge cases pushed down.
6. **No universal ratio.** Tailor the mix to complexity, stack, criticality and organizational standards.
7. **Do not test** language or framework internals, generated code (accessors, builders, generated DTOs), or private methods directly. Do not call real external services; mock them in unit tests and use test doubles in integration tests.
8. **Coverage is a flashlight, not a score.** Low coverage on critical business logic needs attention; high coverage on data carriers or config suggests wasted tests. 100% is a vanity target, and global 80% to 90% gates invite assertion-free tests.
9. **Every test must assert behavior.** Executing code without a meaningful check adds coverage but no protection.
10. **Bugs start with a failing test.** Reproduce, fix, keep as regression guard, refactor under its protection.
11. **Unit means isolated.** If the SUT uses its real collaborators, it is an integration test; mock dependencies and test them in their own unit tests.
12. **Automate instead of manual passes.** Run the suite on every check-in in CI; manual scripts drift and do not repeat reliably.
13. **Test-first or test-last are both valid**; prefer test-first for clear requirements and bug fixes.
14. **AI drafts, humans verify.** Give the assistant sample tests from the suite so it matches conventions; use it for edge-case ideas and boilerplate, then check that each test would fail if the code were wrong.

## Default workflow

1. Locate and read existing tests for the area; summarize what they reveal.
2. Classify the change: logic, wiring or user journey. Choose the test level (rule 5).
3. For a bug, write the failing reproduction first. For a feature, write behavior-named tests (before or right after the code).
4. Isolate the SUT with mocks for unit tests; use real collaborators with fresh per-test setup for integration; reset data and use a random port for API-level E2E.
5. Cover typical inputs, boundaries and failure paths; assert outcomes, not just execution.
6. If testing is painful, propose the design split that would make it easy.
7. Check coverage for dark spots in critical code; ignore trivial code.
8. Ensure the tests run in CI on every change, with integration and E2E on their own cadence if slow.

## References

- [references/why-test-and-what-to-skip.md](references/why-test-and-what-to-skip.md): read when justifying testing to a skeptic, using tests to learn a codebase, spotting design smells via testability, or deciding what to leave untested.
- [references/test-pyramid-and-mix.md](references/test-pyramid-and-mix.md): read when choosing between unit, integration and E2E tests, sizing a suite, or diagnosing a slow or flaky top-heavy suite.
- [references/code-coverage.md](references/code-coverage.md): read when interpreting a coverage report, setting or challenging a coverage gate, or detecting coverage gaming.
- [references/writing-tests-playbook.md](references/writing-tests-playbook.md): read when actually writing tests: setup, TDD vs test-last, assertions, SUT, mocking, integration and API-level E2E recipes, naming, AI-assisted test writing.
- [references/practice-plan.md](references/practice-plan.md): read when coaching someone to build the habit, or planning improvements to an under-tested codebase.
- [references/source-map.md](references/source-map.md): read to find which file covers a given chapter section.

## Scripts

- `scripts/coverage_hotspots.py`: run `python3 scripts/coverage_hotspots.py coverage.xml --critical 'src/billing/*' --trivial '*dto*' --top 10` to compute overall line and branch rates from a Cobertura report, list the least-covered files and functions, and flag critical code under `--critical-min` (default 0.80) and trivial code at or above `--trivial-max` (default 0.90). Add `--json` for machine-readable output. Advisory only; it never fails a build.
