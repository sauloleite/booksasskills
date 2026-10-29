---
name: fse-theme-testing-and-delivery
description: Theme skill on testing and getting software safely into production from Schutta and Vega's "Fundamentals of Software Engineering" (chapters 5 and 10). Use when designing a test suite or test mix, interpreting code coverage, writing unit, integration or end-to-end tests, closing the gap between local and production, handling configuration, secrets and feature flags, error handling and logging, security baselines, deployment pipelines, rollout strategies and post-launch maintenance.
---

# Testing and delivery to production (Fundamentals of Software Engineering, ch. 5 and 10)

Automated tests make change safe; a production mindset makes it real. Both work best as habits built in from the first commit rather than phases at the end.

## Cross-chapter rules

1. **Quality is a habit.** Add tests continuously (with every change and every bug fix), not in a big push later.
2. **Tests are documentation and design feedback.** Name them for behavior; if code is hard to test, it has too many responsibilities.
3. **Shape the mix like a pyramid,** adapted to context: many fast unit tests, fewer integration tests, few end-to-end tests. Skip framework, generated and trivial code.
4. **Coverage is a signal, not a target.** Look for low coverage on critical logic and wasted tests on trivial code (`scripts/coverage_hotspots.py`).
5. **Design for production from day one.** Performance, configuration, error handling and security are not release-week tasks.
6. **Close the environment gap.** Containers, staging parity and observability; real users are the final test, so limit exposure with canaries.
7. **Configuration never lives in code.** Per-environment files for plain settings, a secrets manager or environment variables for secrets, separate credentials per environment. Scan with `scripts/scan_config_risks.py`.
8. **Flags separate deploy from release** and need owners, purposes and expiry dates (`scripts/audit_feature_flags.py`).
9. **Most effort is the unhappy path.** Degrade gracefully, keep users informed, put detail in leveled logs, never log secrets or personal data.
10. **Automate the pipeline incrementally.** Build and test first, then checks, then progressive delivery; script deployments and test rollback; keep patching and monitoring after launch.

## Default workflow

1. Define the test mix and add tests with every change (ch05).
2. Externalize configuration and secrets, add flags with expiry, design error handling and logging (ch10).
3. Build the pipeline: environments, branching, scripted deploy and rollback, CI gates (ch10).
4. Choose a rollout strategy, monitor against baselines, and run a retrospective after each release (ch10).

<!-- BEGIN GENERATED: run tools/build_bundles.py to refresh -->

## References by chapter

Each link is one level deep; read only the files whose description matches the task.

### CH05: Automated Testing

- [ch05-code-coverage.md](references/ch05-code-coverage.md): read when interpreting a coverage report, setting or challenging a coverage gate, or detecting coverage gaming.
- [ch05-practice-plan.md](references/ch05-practice-plan.md): read when coaching someone to build the habit, or planning improvements to an under-tested codebase.
- [ch05-test-pyramid-and-mix.md](references/ch05-test-pyramid-and-mix.md): read when choosing between unit, integration and E2E tests, sizing a suite, or diagnosing a slow or flaky top-heavy suite.
- [ch05-why-test-and-what-to-skip.md](references/ch05-why-test-and-what-to-skip.md): read when justifying testing to a skeptic, using tests to learn a codebase, spotting design smells via testability, or deciding what to leave untested.
- [ch05-writing-tests-playbook.md](references/ch05-writing-tests-playbook.md): read when actually writing tests: setup, TDD vs test-last, assertions, SUT, mocking, integration and API-level E2E recipes, naming, AI-assisted test writing.

### CH10: To Production

- [ch10-configuration-flags-and-secrets.md](references/ch10-configuration-flags-and-secrets.md): read when externalizing config, choosing config files vs env vars vs secret managers, or designing and cleaning up feature flags.
- [ch10-deployment-pipeline-and-release.md](references/ch10-deployment-pipeline-and-release.md): read when choosing a branching model, naming branches, writing deploy or rollback automation, picking a rollout strategy, or building CI/CD.
- [ch10-monitoring-maintenance-and-practice.md](references/ch10-monitoring-maintenance-and-practice.md): read when setting up post-launch monitoring, using AI on logs, writing an update policy, or coaching production habits.
- [ch10-production-gap-performance-and-errors.md](references/ch10-production-gap-performance-and-errors.md): read when debugging prod-only failures, choosing performance optimizations, or designing error handling and log content.
- [ch10-security-and-compliance.md](references/ch10-security-and-compliance.md): read when touching TLS, authentication, sessions, MFA, PII, encryption at rest, GDPR/CCPA, HIPAA, PCI DSS or SBOMs.

Merged section maps: [source-maps.md](references/source-maps.md).

## Scripts

Python 3 standard library only; run any script with `--help` for its arguments.

| Script | Purpose |
|---|---|
| `scripts/coverage_hotspots.py` (ch05) | Summarize a Cobertura coverage.xml into actionable hotspots. |
| `scripts/audit_feature_flags.py` (ch10) | Audit a feature-flag registry for hygiene problems. |
| `scripts/scan_config_risks.py` (ch10) | Scan source and config files for production-readiness risks in configuration. |

<!-- END GENERATED -->
