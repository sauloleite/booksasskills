---
name: baa-theme-evaluation-and-operations
description: Theme skill on measuring, operating and improving agents in production, from Michael Albada's "Building Applications with AI Agents" (chapters 9 to 11). Use when building eval sets and release gates, scoring tool recall, precision and parameter accuracy, instrumenting agents with OpenTelemetry, setting alerts and drift thresholds, triaging production failures, running shadow, A/B, bandit or canary rollouts, tuning human escalation, or closing the feedback loop.
---

# Evaluation, monitoring and improvement (Building Applications with AI Agents, ch. 9 to 11)

One loop in three stages: validate before release, observe in production, and turn what you observe into tested improvements. Each stage feeds the next.

## Cross-chapter rules

1. **Evaluation is automatic and versioned.** Run it on every merge and model change. Each case fixes the starting state, history and expected end state (tool calls with arguments plus required phrases), so scoring needs no judgment.
2. **Score agents on actions.** Tool recall, tool precision, parameter accuracy and task success with confidence intervals, plus consistency across reruns (`scripts/agent_eval_report.py`). Never optimize a single number.
3. **Set release criteria in advance** and enforce them with automatic gates, pilot sign-off and fast rollback.
4. **Monitor four layers.** Infrastructure, workflow (success, tokens, tool errors, retries, fallbacks), output quality and user signals. Agent failures are often silent, so infrastructure health alone proves little.
5. **Extend the existing observability stack.** One span per agent step with version, session and token attributes; trace IDs on every log line; PII scrubbed. Summarize with `scripts/trace_summary.py`.
6. **Triage before reacting.** Reproduce several times to separate systematic bugs from noise, then check input drift (`scripts/drift_check.py`) against explicit thresholds.
7. **Every failure becomes a regression test.** Diagnose root cause in order (trace, localize, check recurrence, assess impact), fix prompts and tools before architecture or retraining, and prioritize a deduplicated backlog.
8. **Escalate to humans by risk.** Combine uncertainty and consequence, and tune the threshold to a review budget (`scripts/escalation_tuner.py`).
9. **Release through a ladder.** Staging, shadow, A/B or bandit, then canary or gradual ramp. Size tests and read results with `scripts/ab_test_analyzer.py`; shift traffic adaptively with `scripts/bandit_allocator.py`.

## Default workflow

1. Write hero-scenario eval cases and release gates (ch09).
2. Instrument, dashboard and alert by layer; define drift thresholds and ownership (ch10).
3. Turn incidents and feedback into diagnosed, prioritized fixes; validate each through the rollout ladder; promote proven in-context fixes into prompts, tools or weights (ch11).

<!-- BEGIN GENERATED: run tools/build_bundles.py to refresh -->

## References by chapter

Each link is one level deep; read only the files whose description matches the task.

### CH09: Validation and Measurement

- [ch09-component-testing.md](references/ch09-component-testing.md): read when writing unit tests for tools, planners, memory stores or learning loops, or when interpreting low recall, precision or parameter accuracy.
- [ch09-deployment-readiness.md](references/ch09-deployment-readiness.md): read when defining release criteria, configuring quality gates, or planning pilot, monitoring and rollback.
- [ch09-metrics-and-evaluation-sets.md](references/ch09-metrics-and-evaluation-sets.md): read when choosing metrics, wiring evals into CI, designing the case schema, or planning how to grow and diversify an eval set.
- [ch09-system-level-evaluation.md](references/ch09-system-level-evaluation.md): read when building an end-to-end harness or testing consistency, coherence, hallucination or robustness to odd and hostile inputs.

### CH10: Monitoring in Production

- [ch10-drift-detection.md](references/ch10-drift-detection.md): read when picking or interpreting KS, KL, PSI or embedding drift tests and planning the response.
- [ch10-failure-triage-and-metrics.md](references/ch10-failure-triage-and-metrics.md): read when deciding whether a bad output is a bug or noise, choosing what to measure, or handling PII in telemetry.
- [ch10-metric-ownership-governance.md](references/ch10-metric-ownership-governance.md): read when assigning metric ownership across product, ML and SRE or setting up triage rituals.
- [ch10-release-patterns-and-feedback.md](references/ch10-release-patterns-and-feedback.md): read when rolling out a new model, prompt or planner, building a regression corpus, adding self-healing fallbacks, or wiring user feedback into monitoring.
- [ch10-stack-instrumentation-and-alerting.md](references/ch10-stack-instrumentation-and-alerting.md): read when selecting a monitoring stack, designing OTel spans and attributes, or building Grafana dashboards and alert routing.

### CH11: Improvement Loops

- [ch11-continuous-learning.md](references/ch11-continuous-learning.md): read when deciding whether a fix should live in context, in prompts/tools, or in retrained weights; managing context for in-session adaptation; planning offline retraining.
- [ch11-experimentation-and-rollouts.md](references/ch11-experimentation-and-rollouts.md): read when choosing between staging, shadow, A/B, bandit, canary or blue/green; running a shadow safely; handling stateful agents in A/B tests; configuring a bandit.
- [ch11-feedback-pipelines-and-diagnosis.md](references/ch11-feedback-pipelines-and-diagnosis.md): read when setting up telemetry and failure clustering, choosing between DSPy, Trace and APO, running RCA, or designing HITL escalation criteria, uncertainty signals and review procedure.
- [ch11-refinement-and-prioritization.md](references/ch11-refinement-and-prioritization.md): read when turning findings into prompt or tool changes, building an optimizer dataset, writing change records, or organizing and ranking the improvement backlog.

Merged section maps: [source-maps.md](references/source-maps.md).

## Scripts

Python 3 standard library only; run any script with `--help` for its arguments.

| Script | Purpose |
|---|---|
| `scripts/agent_eval_report.py` (ch09) | Score agent runs against expected final states and apply release gates. |
| `scripts/drift_check.py` (ch10) | Compare a baseline and a current sample for distribution shift (PSI, KS, KL). |
| `scripts/trace_summary.py` (ch10) | Summarize agent spans exported as JSON lines (OTel-like) for monitoring review. |
| `scripts/ab_test_analyzer.py` (ch11) | Two-proportion A/B test analyzer and sample-size planner for agent experiments. |
| `scripts/bandit_allocator.py` (ch11) | Beta-Bernoulli Thompson-sampling allocator for adaptive agent experiments. |
| `scripts/escalation_tuner.py` (ch11) | Tune human-in-the-loop escalation thresholds from historical agent decisions. |

<!-- END GENERATED -->
