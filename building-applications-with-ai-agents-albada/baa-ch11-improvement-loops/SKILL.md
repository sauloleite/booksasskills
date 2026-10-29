---
name: baa-ch11-improvement-loops
description: Designs feedback-driven improvement loops for production agent systems, based on Chapter 11 of Michael Albada's "Building Applications with AI Agents". Covers failure detection and root cause analysis, HITL escalation thresholds, prompt and tool refinement (DSPy, Trace, APO), backlog prioritization, shadow deployments, A/B tests, Bayesian Bandits, in-context adaptation and offline retraining. Use when an agent keeps failing in production, when planning how to validate or roll out a prompt/tool change, when sizing or reading an experiment, or when deciding how fixes should persist.
---

# Improvement Loops (Building Applications with AI Agents, Chapter 11)

This skill helps an agent design and run the cycle that makes a deployed agent system better over time: observe and diagnose failures, validate fixes safely, then embed them durably. It assumes failures in production are certain and judges a system by how quickly it turns them into improvements. The cycle has three stages (feedback pipelines, experimentation, continuous learning), and it is as much an organizational process (engineering, data science, product, UX, shared documentation) as a technical one.

## Key decision rules

Apply these even without opening a reference.

1. **Close the loop explicitly.** Shipping a pretrained model and patching by hand is not a loop. Every system needs: telemetry, failure clustering, a ranked backlog, a validation path, and a persistence mechanism.
2. **Automation first, humans for judgment.** Let pipelines monitor, cluster and propose; let engineers approve, override and set priorities. Automated proposals never go straight to production.
3. **Read clusters as hints of cause.** Repeated wrong skill choice suggests reasoning out of step with user intent; repeated tool execution errors suggest ambiguous parameter construction; a slow rise in one error type suggests drift.
4. **RCA order:** trace the workflow, localize the faulty component, check whether it is a pattern (cohort, input, state), then assess frequency and severity. Expect non-technical causes (vague task definitions, data gaps, metrics rewarding the wrong behavior).
5. **Escalate to humans on low certainty or high consequence.** Signals: self-reported certainty (escalate below about 0.7, stricter for sensitive calls), entropy, disagreement across 3 to 5 samples (above about 20%), a critic model. Rank by risk = uncertainty x consequence. Tune thresholds on history so escalations stay under about 10% of cases.
6. **Always escalate** persistent unexplained errors, regulated or ethical anomalies, failures in mission-critical tasks, and conflicting automated diagnoses.
7. **Fix prompts and tools before architecture or retraining.** Match symptom to lever: ambiguity, rewrite and specify format; off-task output, add constraints; brittleness, add exemplars or context; tangled multistep work, decompose. Tool issues: wrong selection, malformed parameters, missing capability, broken chaining.
8. **Put safety checks for dangerous actions inside the tool** (confirmation, impact check), not only in the prompt.
9. **Optimizer data:** a handful of synthetic examples is a demo; use 100+ annotated cases for agent modules, 50 to 200+ for tool classifiers, and a metric better than exact match.
10. **Document every change:** observed problem, change made, how success is measured. Change one lever at a time.
11. **Aggregate before prioritizing:** deduplicate, tag (root cause, workflow, impact, component), link traces and RCA. Rank by frequency, severity, feasibility, strategic alignment, recurrence risk. Re-rank regularly.
12. **Climb the rollout ladder:** staging/RC, then shadow, then A/B or bandit, then canary, rolling or blue/green. Ultra-high-risk changes also need approval gates.
13. **Shadow for risky changes** (planning, integrations, big prompt rewrites); sandbox side-effecting tools; replay or simulate human approvals.
14. **A/B for user-facing effects:** predefine metrics and sample size, prevent cross-contamination, use sticky assignment or per-arm state stores for stateful agents, watch long-term effects, read drops qualitatively.
15. **Bandits when traffic is precious or the environment moves:** reward must equal the true goal, priors neutral, keep an exploration floor, watch for self-reinforcing loops. Prefer A/B when you need a clean effect estimate.
16. **In context first, then promote.** Session-level fixes are instant and low risk but vanish when the session ends; promote proven ones into prompts, workflows, tools or retraining.
17. **Offline retraining for systemic issues:** curate balanced production data, update (few-shot optimization or LoRA-style fine-tuning), validate offline then shadow; schedule it and hold out recent data to catch drift.

## Default workflow

1. Instrument: trace reasoning, skill choices, tool calls with parameters, outputs and user signals; tag by agent version and environment.
2. Detect and cluster failures (rules, anomaly detection, statistical clustering); run RCA on the top clusters.
3. Define escalation triggers and thresholds; route risky cases to a mixed review team; log decisions and rationale.
4. Aggregate all findings into one backlog; score and rank; pick the top items.
5. Design the smallest fix (prompt or tool first); write the change record; build an evaluation set from reviewed failures.
6. Validate offline, then shadow, then A/B or bandit; size the test before starting.
7. Promote by canary or blue/green with rollback ready; monitor after release.
8. Persist: promote in-context wins, schedule offline retraining for recurring issues; feed lessons back into step 2.

## References

- [references/feedback-pipelines-and-diagnosis.md](references/feedback-pipelines-and-diagnosis.md): read when setting up telemetry and failure clustering, choosing between DSPy, Trace and APO, running RCA, or designing HITL escalation criteria, uncertainty signals and review procedure.
- [references/refinement-and-prioritization.md](references/refinement-and-prioritization.md): read when turning findings into prompt or tool changes, building an optimizer dataset, writing change records, or organizing and ranking the improvement backlog.
- [references/experimentation-and-rollouts.md](references/experimentation-and-rollouts.md): read when choosing between staging, shadow, A/B, bandit, canary or blue/green; running a shadow safely; handling stateful agents in A/B tests; configuring a bandit.
- [references/continuous-learning.md](references/continuous-learning.md): read when deciding whether a fix should live in context, in prompts/tools, or in retrained weights; managing context for in-session adaptation; planning offline retraining.
- [references/source-map.md](references/source-map.md): read to locate where each chapter section is covered.

## Scripts

All are Python 3 standard library, deterministic, with `--help`.

- Run `python3 scripts/ab_test_analyzer.py samplesize --baseline 0.41 --mde 0.03` to compute users per arm needed to detect an absolute lift (default alpha 0.05, power 0.8).
- Run `python3 scripts/ab_test_analyzer.py analyze --a-success 412 --a-total 1000 --b-success 455 --b-total 1000` to compute rates, lift, two-proportion z-test p-value and the confidence interval for B minus A.
- Run `python3 scripts/bandit_allocator.py --arm A:120:400 --arm B:150:400 --arm C:118:400` to compute Beta posteriors, the probability each variant is best, and next-round traffic shares with an exploration floor (`--min-share`).
- Run `python3 scripts/escalation_tuner.py cases.csv --budget 0.10 --always critical` to sweep risk thresholds (uncertainty x severity weight) over historical cases with columns `certainty,severity[,correct]` and report escalation rate and errors caught per threshold.
