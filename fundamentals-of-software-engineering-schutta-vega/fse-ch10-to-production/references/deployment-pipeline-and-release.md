## Contents

1. Pipeline anatomy
2. Environment ladder
3. Branching strategies and Git Flow
4. Deployment automation and rollback
5. Choosing a deployment strategy
6. CI/CD workflow and growth path
7. Pitfalls

# Deployment pipeline, branching and release strategy

## 1. Pipeline anatomy

Think of the path to production as four interlocking parts:

1. **Environments**: the stages code runs in on its way to users, each validating something.
2. **Version control strategy**: how many people change one codebase safely, and how releases and emergencies are handled.
3. **Deployment automation**: the same scripted procedure every time instead of a human following a checklist.
4. **CI/CD**: automation that carries a commit through build, test and release.

## 2. Environment ladder

Names and counts vary by organization; the common ladder:

| Stage | Role | What it catches |
|---|---|---|
| Local | Personal sandbox, but teammates run similar setups | Logic errors, fast feedback |
| Test / QA | First shared checkpoint; QA happens here | Suite behaving differently off your laptop, integration with others' work |
| Staging | Production-like rehearsal | Performance testing, user acceptance, environment-specific config |
| Production | Real users | Everything else |

Configuration per stage is part of each promotion, decided up front, not patched afterward.

## 3. Branching strategies and Git Flow

In production settings branching serves stability, fast correction (roll back or roll forward with a fix) and audit trails for compliance.

| Strategy | Shape | Fits when |
|---|---|---|
| Git Flow | Long-lived main and develop plus feature, release and hotfix branches | Formal releases, scheduled windows, approval gates |
| GitHub Flow | Main plus short-lived feature branches, reviewed then shipped | Continuous web delivery, small teams |
| Trunk-based | Everyone integrates into main, branches live hours to about a day | High CI maturity, feature flags in use |
| Release train | Scheduled releases (weekly, monthly) bundle whatever is ready | Many teams coordinating, predictable cadence |

Git Flow in detail (useful for learning because its roles are explicit):

- **main**: always stable and deployable, the source of truth for production. Block direct commits (the goal is preventing accidents; review already happened upstream). Must pass all automated tests.
- **develop**: the shared integration line. Review happens on merges into it. It may hold incomplete features but must always build and pass basic tests. Run the full suite often to catch integration problems.
- **feature/\***: cut from develop, one per feature or bugfix, isolating experiments. Name branches by type plus intent, optionally with a ticket key, e.g. `feature/PAY-42-refund-endpoint` or `bugfix/session-expiry`; avoid opaque names like `temp`, `wip2` or a bare number.
- **release/\***: cut from develop to stabilize a version while new work continues on develop. Holds version bumps, final docs, deployment config, and is the frozen release candidate stakeholders approve. Needed only with formal processes or fixed release windows.
- **hotfix/\***: cut from main when production is broken and develop contains unfinished work. Changes only what is necessary, ships fast, and is merged back into both main and develop so the fix is not lost.

Lifecycle: feature to develop, develop to release to main, hotfix from main back into main and develop. Whatever model you use, the goals stay constant: protect stable code, isolate work in progress, and make integration a clear process.

## 4. Deployment automation and rollback

Manual deployment (package, test, prepare servers, execute, verify) is slow, stressful and error prone because a human must repeat every step perfectly. A script is executable documentation of the procedure.

A minimal deployment script should show:

- clear, ordered steps
- error checks that stop on failure with a nonzero exit
- a timestamped backup of the current version before replacing it
- a post-start health check

Even a crude script beats none; improve it incrementally.

Rollback plan prerequisites:

- Confirm a backup of the running version exists before deploying.
- Rehearse rollbacks routinely, not only during incidents.
- Write down how to reverse database migrations.
- Retain several previous versions, not just one.
- Watch the system while rolling back.

For a single feature, the simplest rollback may be turning off its flag.

Illustrative skeleton of the verify-or-revert step (Python, any target):

```python
import subprocess, sys, time, urllib.request

def healthy(url, attempts=5, wait=3):
    for _ in range(attempts):
        try:
            if urllib.request.urlopen(url, timeout=2).status == 200:
                return True
        except OSError:
            pass
        time.sleep(wait)
    return False

subprocess.run(["./deploy.sh"], check=True)
if not healthy("http://127.0.0.1:8080/health"):
    subprocess.run(["./rollback.sh"], check=True)
    sys.exit("deploy failed health check; rolled back")
```

## 5. Choosing a deployment strategy

| Strategy | Mechanism | Risk | Good for |
|---|---|---|---|
| All at once (big bang) | Replace the whole application in one step | High: every user hit at once, rollback is messy | Small apps with few users, dev and test environments, downtime-tolerant systems |
| Gradual (phased) | Expose a subset first: canary (small share of users) or rolling (servers one at a time) | Lower: problems found early and contained | Large-scale systems, features needing feedback, systems needing close watching |
| Zero-downtime techniques | Blue-green (two identical environments, flip traffic once the idle one is verified) or rolling updates | Lowest user impact, more setup | Mission-critical and high-traffic services |

Decision factors: system complexity, tolerance for downtime, and how good your monitoring is (gradual rollout is pointless if you cannot see the canary failing). Starting simple and evolving is legitimate.

## 6. CI/CD workflow and growth path

Definitions: continuous integration merges and tests everyone's changes automatically; continuous delivery keeps tested builds release-ready; continuous deployment pushes them to production automatically.

Why automate: consistent builds (attacks "works on my machine"), tests that run without relying on individual discipline, less deployment anxiety (scripts never skip steps), integration problems caught early, and shorter time from commit to users. Code delivers no value until users have it.

Baseline stages: commit, build, test, package (store the artifact), deploy. A hosted runner workflow (for example GitHub Actions) triggers on pushes and pull requests to main, runs each job in a fresh VM, and halts on the first failing step.

Growth path:

1. Automate build and tests first.
2. Add further checks gradually (dependency scanning, linting, security tests).
3. Keep the pipeline fast to protect feedback loops.
4. Review and tune it as team needs change.
5. Document it so the team can maintain it.
6. Later add canary releases and blue-green switching.

CI/CD is as much a culture of continuous improvement as a toolchain.

## 7. Pitfalls

- Hotfix applied to main but never merged into develop, so the bug returns next release.
- Long-lived feature branches that rot and conflict.
- Big bang deployments of large, high-traffic systems.
- A rollback script that was never tested or has no backup to restore.
- Database migrations with no reverse path.
- Pipelines so slow that developers bypass them.
