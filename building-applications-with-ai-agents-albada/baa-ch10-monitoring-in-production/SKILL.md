---
name: baa-ch10-monitoring-in-production
description: Production monitoring for LLM agents, based on Chapter 10 of Michael Albada's "Building Applications with AI Agents" (O'Reilly, 2025). Covers failure-versus-noise triage, a layered metric taxonomy, stack choice (Grafana/Loki/Tempo, ELK, Phoenix, SigNoz, Langfuse), OpenTelemetry span design, dashboards and alerts, shadow and canary releases, regression traces, self-healing fallbacks, user feedback, drift tests (KS, KL, PSI) and RACI ownership. Use when instrumenting, observing, alerting on, rolling out or debugging deployed agents.
---

# Monitoring Agents in Production

Agents are probabilistic, tool-chaining systems facing unbounded input, so pre-release tests cannot be exhaustive and most failures are silent (a "successful" tool call that corrupts later steps, a fluent but wrong answer, a half-finished plan). This skill turns monitoring into the learning loop of an agent system: instrument every step, route telemetry into the same platform that watches other services, separate real regressions from normal nondeterminism, ship changes behind shadow and canary gates, detect drift statistically, and give product, ML and SRE shared ownership of the signals.

## Key decision rules

1. **Triage before reacting.** Output meets the bar (e.g. eval > 0.8)? Only watch trends. Otherwise rerun 3 to 5 times: failing in over 80% of reruns means a systematic bug for engineering. Not reproducible: within variance bounds (e.g. judge score > 0.7, KL to baseline < 0.2) is expected noise, log it for drift watch; outside bounds is anomalous, so check input drift (PSI > 0.1) and mitigate.
2. **Measure four layers**, not just infra: infrastructure (CPU/memory, uptime, P50/P95/P99), workflow (task success, tokens, tool error rate, rate-limit hits, retries, fallbacks), output quality (token cost, hallucination indicator, embedding drift), user (rephrase rate, abandonment, ratings). Collect what detects meaningful change, not everything.
3. **No separate AI monitoring island.** Agent metrics go into the existing Prometheus/Grafana (or vendor) platform used by SREs.
4. **Stack choice:** already on Splunk, Datadog, New Relic or similar? Extend it with OTel. Add Langfuse or Phoenix only for LLM-native evals, ELK for heavy search. Greenfield: Grafana + Loki + Tempo, or SigNoz.
5. **One span per agent step** (plan, tool, generation) with tool name, status, error code, latency, prompt/template version, token counts, model, session and request IDs, agent version, and product tags (workflow ID, feature flag, customer tier). Add events for retries and fallbacks; record exceptions. Scope tightly: enough for a coherent evidence trail, not noise.
6. **Every log line carries trace and span IDs** so you can pivot from a log spike to the exact run.
7. **Protect telemetry:** scrub or hash PII before export, isolate sensitive data in RBAC-controlled, encrypted, audited clusters.
8. **Default alerts** (calibrate): hallucination rate > 5% over 30 min; > 3 retry loops in a session; critical tool mean latency up > 50%. Page via PagerDuty; add Sentry for code exceptions.
9. **Release ladder:** shadow (no user exposure, shared request ID, compare tool choice, latency, tokens, hallucinations) then canary at 1% to 5% with version-tagged dashboards and auto-rollback alerts, then gradual ramp.
10. **Every failure becomes a test.** Export failing, low-rated and exemplary traces into CI; a fix is done when the replayed trace passes.
11. **Self-healing is logged.** Repeated tool failure leads to a simpler plan or a clarifying question; latency spike leads to skipping optional reasoning; high hallucination score leads to a disclaimer or human review. Trace every fallback and check whether it helped.
12. **Drift thresholds:** KS > 0.1 with p < 0.05 (continuous); KL > 0.5 (token or frequency mixes); PSI < 0.1 stable, 0.1 to 0.25 monitor, > 0.25 intervene; mean embedding similarity < 0.8 review. Business symptoms: accuracy down 5 to 10% in 24 h, abandonment > 15%, retries in > 20% of sessions. Retrain when PSI > 0.25 holds 48 h; validate fixes by A/B.
13. **Shared ownership:** model output is the product; latency is often a design choice. Use a RACI with exactly one Accountable per metric, shared dashboards, joint triage after launches, and no lower bar for model latency.

## Default workflow

1. Define success criteria and pick metrics per layer.
2. Choose or extend the stack; wire OTel exporters to traces, logs and metrics backends with PII scrubbing.
3. Instrument each node; tag with version and product context.
4. Build dashboards (tokens per agent per hour, P95 per node, success by workflow and prompt version, fallbacks by tool, drift) and alerts.
5. Ship changes via shadow, then canary, then ramp.
6. Run the triage tree on bad outputs; export failures and wins to the regression suite.
7. Run drift checks on a schedule; respond by severity.
8. Review telemetry cross-functionally against the RACI.

## References

- [references/failure-triage-and-metrics.md](references/failure-triage-and-metrics.md): read when deciding whether a bad output is a bug or noise, choosing what to measure, or handling PII in telemetry.
- [references/stack-instrumentation-and-alerting.md](references/stack-instrumentation-and-alerting.md): read when selecting a monitoring stack, designing OTel spans and attributes, or building Grafana dashboards and alert routing.
- [references/release-patterns-and-feedback.md](references/release-patterns-and-feedback.md): read when rolling out a new model, prompt or planner, building a regression corpus, adding self-healing fallbacks, or wiring user feedback into monitoring.
- [references/drift-detection.md](references/drift-detection.md): read when picking or interpreting KS, KL, PSI or embedding drift tests and planning the response.
- [references/metric-ownership-governance.md](references/metric-ownership-governance.md): read when assigning metric ownership across product, ML and SRE or setting up triage rituals.
- [references/source-map.md](references/source-map.md): chapter section to reference file mapping.

## Scripts

Python 3 stdlib only; `--help` documents inputs.

- Run `python3 scripts/trace_summary.py spans.jsonl --p95-ms 1500 --max-error-rate 0.05 --max-retries 3` to compute per-step count, error rate, P50/P95/P99 latency and token totals, per-trace retry and fallback rates, the slowest traces, and threshold flags from OTel-like JSON-lines spans. Add `--group-by agent.version` to compare canary or shadow against baseline; `--json` for machine output.
- Run `python3 scripts/drift_check.py numeric baseline.txt current.txt` to compute KS (statistic, p-value) and quantile-binned PSI for a numeric feature such as query length or latency.
- Run `python3 scripts/drift_check.py categorical baseline_labels.txt current_counts.csv` to compute PSI and KL(baseline||current) for label mixes such as tool or intent usage (one label per line, or `label,count` lines), with verdicts against the default thresholds.
