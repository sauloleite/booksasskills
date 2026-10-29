## Contents

1. Monitoring after launch
2. AI assistance in operations
3. Maintenance and updates
4. Update policy template
5. Habit plan by phase
6. Further reading
7. Pitfalls

# Monitoring, maintenance and building production habits

## 1. Monitoring after launch

Shipping is a beginning, not an end. Without monitoring you cannot know how the system behaves now or over time, and "no complaints" is not evidence of health: dissatisfied users tend to leave without telling you.

Two complementary sources:

- **Real-time metrics** answer "what is happening now?": response time, server load, throughput, errors. Read every number against its baseline. A 300 ms response looks fine in isolation but is a sixfold regression if normal is 50 ms.
- **Logs** answer "what happened, and when?": the historical record for reconstructing incidents.

Minimum viable monitoring: response times, error counts and server resources (CPU, memory, disk). Add sophisticated tooling later.

Log rules hardened by incidents:

1. Capture the data you will need when diagnosing failures.
2. Stamp each entry with time and a user or request identifier.
3. Use the ERROR level for errors.
4. Exclude passwords and personal details.
5. Prune old logs on a schedule.

Practice: watch logs and dashboards for an hour or two after every deployment.

## 2. AI assistance in operations

Once metrics and logs exist, AI tools can scan large log volumes for anomalies and patterns that precede incidents, and can draft dashboards from metrics data that would otherwise need tedious manual setup. Treat the output as a starting point that a human verifies. AI cannot help with telemetry you never collected.

## 3. Maintenance and updates

Deferring maintenance while things look fine is a mistake: small cheap issues compound into expensive ones, and systems people depend on need steady upkeep just like physical infrastructure.

**System updates** (OS and platform patches) bring security fixes, performance gains, bug fixes and new capabilities. Rule: security patches go in promptly; feature upgrades may wait.

**Dependency management** is the most neglected part of maintenance. Applications pull in dozens to hundreds of libraries, each a potential vulnerability.

- Keep an accurate SBOM so a vulnerability advisory maps immediately to affected services.
- Scan dependencies automatically in CI (build tools such as Maven and Gradle have analyzers; dependency-check actions exist for hosted CI).
- Example: a pinned web framework version with a published CVE gets flagged by the scan, prompting an upgrade.

## 4. Update policy template

Write a short team policy covering five points:

| Element | Example decision |
|---|---|
| Cadence | Dependency and OS review on the first Monday of each month |
| Emergency path | Critical CVE: patch branch from main, deploy within 48 h, notify on-call |
| Automation | Dependency scan on every pull request and nightly on main |
| Process documentation | Runbook for upgrading framework and runtime versions |
| Change record | Log of what was updated, when, why and by whom |

Prevention is cheaper than recovery. Put review reminders on the calendar; automation does not replace human judgment.

## 5. Habit plan by phase

Adopt a couple of items per phase on each new feature rather than everything at once.

Before writing code:

- Brainstorm failure modes for the feature.
- Decide which diagnostic data you would want in the logs.
- List configuration that will differ outside your laptop.

During implementation:

- Start on a descriptively named branch.
- Handle the top three likely failures.
- Log key actions without sensitive data.
- Add a test that behaves like a real user.
- Externalize every value that varies by environment.

Before release:

- Record the deployment steps as you perform them (raw material for a script).
- Prepare a rollback, including how to switch the feature off.
- Ask a teammate to review specifically for production readiness.

After release:

- Watch logs for an hour or two.
- Hold a short retrospective: what went well, what hurt, what to change.

Coaching tone: early failures in production are normal and instructive; the skill grows with repetition.

## 6. Further reading

- Continuous Delivery (Humble, Farley)
- The Phoenix Project (Kim et al.)
- Head First Git (Gandhi)
- Learning GitHub Actions (Laster)
- Feature Flags (Nadel)

## 7. Pitfalls

- Declaring done at deploy time.
- Alerting on absolute numbers with no baseline.
- Postponing patches because nothing is broken.
- Unbounded log retention filling disks.
- Trusting AI-generated dashboards or anomaly reports without checking them.
