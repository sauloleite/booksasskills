---
name: fse-ch10-to-production
description: Production readiness and delivery guidance based on Chapter 10 of Schutta and Vega's "Fundamentals of Software Engineering" (O'Reilly, 2025). Covers the dev-to-prod gap, performance levers, per-environment config, feature flags, secrets, error handling and logging, HTTPS, authentication, PII, encryption, compliance, Git Flow and other branching models, deployment scripts, rollback, big bang vs gradual rollout, CI/CD, monitoring and maintenance. Use when preparing code for release, reviewing for production readiness, debugging "works on my machine", or designing a deployment pipeline.
---

# To Production

Production is where code meets real users, real data, real load and real partners, and it exposes everything local testing hid. This skill helps an agent coach a developer to think production-ready from the first line of code: externalize configuration, plan for failure, secure by default, ship through an automated and reversible pipeline, and keep watching and patching after launch. Users do not care that it runs on your laptop; they care that it runs for them.

## Key decision rules

1. **Production readiness is designed in, not bolted on.** Before coding a feature, list what can fail, what you will need to log, and which settings differ outside your machine.
2. **"Cannot reproduce" means an environment difference.** Check platform and resources, database vendor and version, dependency versions, configuration, concurrency, data shape and volume, external services, and security controls (firewall, TLS, CORS). Close the gap with containers, observability, staging parity and CI/CD; limit real-user risk with canaries and A/B tests.
3. **Performance is a habit aimed at user experience.** Pick the lever for the measured bottleneck: async (with care), batched calls, caching stable hot data, indexes and no N+1, and for frontends minify, bundle and tree-shake, lazy-load, serve from a CDN.
4. **No environment-specific literals in code.** Inject config; non-sensitive values in per-environment files, sensitive or rotating values via environment variables or a secrets manager so rotation needs no redeploy.
5. **Feature flags decouple deploy from release.** Types: release (hide unfinished work), experiment (compare experiences), permission (tier or role gating). Give every temporary flag an owner, purpose and expiry, and clean up on a schedule.
6. **Secrets:** never committed (a leak means rewriting history), stored in a manager, rotated automatically, least-privilege access, distinct per environment.
7. **Plan for the unhappy path.** Rough split: happy path about 20% of code, failures about 80% of effort. Use graceful degradation, plain-language user messages, technical detail only in logs, and fallbacks for critical dependencies.
8. **Log deliberately.** ERROR, WARN, INFO, DEBUG used consistently; less verbose in production. Always timestamps and user or request IDs; errors at ERROR. Never secrets, PII, full payloads, or duplicates across layers. Expire old logs.
9. **Security in layers.** Follow OWASP. HTTPS on everything with redirect, auto-renewed certs, TLS 1.2+. Never write your own auth; use a mature framework and adaptive salted hashing.
10. **Account defaults to suggest:** passwords of 12+ characters checked against breach lists and reuse; login backoff from about 5 s rising to 30 min or more, CAPTCHA after repeated failures, new-device alerts; high-entropy session tokens with idle (about 30 min) and absolute (about 8 h) timeouts, revoked-token blocklist; MFA via authenticator, key or biometrics over SMS or email, also during recovery, with backup codes.
11. **Data duties.** Tag PII fields so they get masked; encrypt sensitive data in transit and at rest (AES-GCM, fresh IV, 128-bit minimum, 256 for long-term); know GDPR/CCPA, HIPAA and PCI DSS triggers (never store CVV); keep an SBOM. When code touches regulated data, involve the security team.
12. **Pipeline = environments + branching + automation + CI/CD.** Ladder: local, test/QA, staging, production, with config handled at every promotion. Git Flow suits formal or scheduled releases; GitHub Flow, trunk-based or release trains suit other cadences. Hotfixes branch from main and merge back into both main and develop.
13. **Script every deployment, with a tested rollback.** Backup first, fail loudly, health-check after start, keep several versions, document migration reversal, rehearse.
14. **Choose rollout by complexity, downtime tolerance and monitoring maturity.** Big bang for small, low-traffic or non-prod systems; gradual (canary, rolling) for large or closely watched systems; blue-green or rolling for zero downtime. Start simple and evolve.
15. **CI/CD grows in steps:** build and test first, then more checks, keep it fast, review it, document it, later canaries and blue-green.
16. **After launch, watch and maintain.** Read metrics against baselines; start with latency, error counts and resource use. Apply security patches promptly; scan dependencies automatically; keep a written update policy.

## Default workflow

1. Classify the request: diagnosis of a prod-only bug, readiness review, config or secrets, security, pipeline design, or operations.
2. For reviews, run the scripts below on the repo and flag registry, then walk rules 1 to 11 against the diff.
3. For pipeline or release work, pick environments, branching model and rollout strategy explicitly and state the rollback path.
4. Close with post-release steps: what to watch for the first hour or two, and a short retrospective.
5. Coach incrementally: suggest one or two new habits per phase per feature rather than everything at once.

## References

- [references/production-gap-performance-and-errors.md](references/production-gap-performance-and-errors.md): read when debugging prod-only failures, choosing performance optimizations, or designing error handling and log content.
- [references/configuration-flags-and-secrets.md](references/configuration-flags-and-secrets.md): read when externalizing config, choosing config files vs env vars vs secret managers, or designing and cleaning up feature flags.
- [references/security-and-compliance.md](references/security-and-compliance.md): read when touching TLS, authentication, sessions, MFA, PII, encryption at rest, GDPR/CCPA, HIPAA, PCI DSS or SBOMs.
- [references/deployment-pipeline-and-release.md](references/deployment-pipeline-and-release.md): read when choosing a branching model, naming branches, writing deploy or rollback automation, picking a rollout strategy, or building CI/CD.
- [references/monitoring-maintenance-and-practice.md](references/monitoring-maintenance-and-practice.md): read when setting up post-launch monitoring, using AI on logs, writing an update policy, or coaching production habits.
- [references/source-map.md](references/source-map.md): chapter section to reference file mapping.

## Scripts

Python 3 stdlib only; each has `--help`.

- Run `python3 scripts/scan_config_risks.py <repo-or-files> [--fail-on HIGH|MEDIUM|LOW|NONE] [--json]` to find hardcoded secrets, localhost endpoints outside dev/test files, plain-HTTP URLs to remote hosts, TLS below 1.2, and DEBUG logging in prod-named config. Exits 1 at or above the chosen severity, so it can gate CI. Heuristic: confirm each hit.
- Run `python3 scripts/audit_feature_flags.py flags.csv --as-of YYYY-MM-DD [--strict] [--json]` to audit a flag registry (columns name,type,owner,purpose,created,expires,rollout; CSV or JSON) for missing owner, purpose or expiry, expired or soon-expiring temporary flags, overlong lifespans, fully rolled-out release flags to delete, and abandoned 0% flags. Thresholds (`--warn-days`, `--max-lifespan-days`, `--full-rollout-days`) are team policy, not book values.
