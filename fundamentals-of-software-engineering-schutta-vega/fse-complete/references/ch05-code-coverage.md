# Code Coverage as Feedback, Not a Target

## Contents
- What coverage measures
- Where coverage shows up
- Limits and the gaming problem
- How to read a coverage report
- Policy guidance for teams
- Checklist
- Script

## What coverage measures

Coverage is the share of code that executes while tests run. The chapter's image is a video game map that starts dark and lights up where you have walked: lit areas were visited, dark areas are where defects can hide unseen. Reports usually break this into:
- **Line coverage**: fraction of executable lines run.
- **Branch coverage**: fraction of decision outcomes taken (both sides of each `if`). Usually lower than line coverage and more telling.
- **Function/method coverage**: fraction of functions entered at least once.

## Where coverage shows up

- In the IDE, for immediate feedback while writing tests.
- In CI/CD, where a tool can enforce a minimum; dropping below it fails the build and can block the pull request from merging.

## Limits and the gaming problem

Coverage measures execution, not verification. A test that calls a method and asserts nothing meaningful still raises the number while guarding against nothing. Organizations sometimes demand 80% to 90% before deployment; the intent is good, yet hard thresholds can push people to write such hollow tests. The chapter calls chasing 100% a vanity metric.

Signs a suite is gaming coverage:
- Tests with no assertions, or assertions only that "no exception was thrown."
- Assertions that restate the implementation (calling the same formula in the test).
- Many tests on DTOs, configuration or accessors.
- Coverage rose sharply in a commit that added no bug-catching scenarios.

A quick quality probe: deliberately break a covered line (flip a comparison, return a constant). If no test fails, that coverage was decorative. Mutation-testing tools automate this idea (an extension beyond the chapter).

## How to read a coverage report

Use it to direct attention, in this order:
1. **Low coverage on business-critical logic** (pricing, payments, authorization, data integrity): highest priority; add behavior-checking tests here.
2. **Low branch coverage on otherwise "covered" code**: untested error paths and edge cases.
3. **High coverage on data carriers or config**: probable wasted effort; consider removing or not extending those tests.
4. **Low coverage on trivial or generated code**: usually fine to leave.

## Policy guidance for teams

- If a gate is mandated, prefer gating on *no decrease* for changed files, or on critical modules, rather than one global percentage.
- Pair any threshold with code review of test assertions.
- Report branch coverage next to line coverage.
- State the purpose explicitly: the goal of testing is confidence in what ships, not reaching a number.

## Checklist

- [ ] Every new test asserts an observable outcome.
- [ ] Critical modules have both happy-path and failure-path tests.
- [ ] Coverage report reviewed for dark spots in critical code, not just the headline figure.
- [ ] No tests added purely to lift the percentage.

## Script

`scripts/coverage_hotspots.py` reads a Cobertura `coverage.xml` and prints overall line and branch rates, the least-covered files and functions, critical files below a minimum and trivial files above a maximum. It is advisory and never fails a build.
