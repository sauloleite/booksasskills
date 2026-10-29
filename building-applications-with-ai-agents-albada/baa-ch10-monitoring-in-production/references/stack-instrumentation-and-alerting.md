# Stack Selection, OTel Instrumentation, Dashboards and Alerts

## Contents
- Choosing a monitoring stack
- Option profiles
- Instrumenting agent steps with OpenTelemetry
- Role of each backend (Tempo, Loki, Grafana)
- Dashboards worth building
- Alert rules and escalation
- Pitfalls

## Choosing a monitoring stack

Decision order:
1. **Already on a managed enterprise platform** (Splunk, Datadog, New Relic and similar)? Keep it. Add OTel instrumentation for agent signals. Agents do not inherently need a new monitoring product.
2. Add a specialized tool only for a concrete gap:
   - Need LLM-native auto-evals, prompt A/B tests, session replay: Langfuse or Arize Phoenix.
   - Need heavy full-text, fuzzy or vector search across huge log volumes: ELK.
3. **Greenfield**: Grafana (with Loki and Tempo) or SigNoz give broad coverage.
4. Then weigh team expertise, data volume and integration needs. OTel lets you fan the same telemetry out to more than one backend, so hybrids are normal.

Commercial platforms in this space include Arize AX, Langfuse Cloud and WhyLabs; the chapter favors self-hostable, extensible open source. AgentOps.ai is an all-in-one agent option (tracing, metrics, evals, alerting, auto-scoring) that cuts setup work at the price of vendor dependency.

## Option profiles

**Grafana + Loki + Tempo (+ OTel).** Most composable; strong visualization; real-time semantic dashboards via plug-ins; alerts on anomalies such as retry spikes; low overhead self-hosted; no lock-in. Cost: several components to run, harder for teams without infra skills. Fits enterprises extending infra monitoring to agents. Used as the reference stack.

**ELK (Elasticsearch, Logstash or Fluentd, Kibana).** OTel collector feeds Elasticsearch; structured JSON events per node (tool params etc.). Strengths: full-text and vector search over outputs, fuzzy prompt matching for long-tail failures, built-in ML jobs for anomaly detection and forecasting tool failure rates, clustering for scale. Cost: memory-hungry, multi-service deployment. Fits teams with existing ELK investment.

**Arize Phoenix.** Python SDK tracing with attached evals (RAG quality, hallucination), notebook integration, OTel export, multiagent coordination metrics. Fast quality insight, light for prototyping. Cost: traces and evals only, needs a companion for logs and metrics; developer-oriented rather than ops. Fits research and ML teams.

**SigNoz.** Single OTel-native app holding metrics, traces and logs on ClickHouse; Python auto-instrumentation; anomaly detection on traces; LLM dashboards. Simple, light for small teams. Cost: smaller plug-in ecosystem, plainer visuals. Fits startups and ML-centric teams.

**Langfuse.** SDK wrappers around graph nodes capture prompts, outputs and custom scorers; token cost tracking; prompt A/B tests; session replay; self-host on PostgreSQL; traces exportable for regression tests. Cost: weak on infra metrics (pair with Prometheus), not built for non-LLM telemetry. Fits adding semantic monitoring onto an existing enterprise logging core.

Quick matrix (own summary):

| Need | First choice |
|---|---|
| Keep existing vendor, add agent signals | Existing stack + OTel |
| Composable self-hosted ops platform | Grafana + Loki + Tempo |
| Massive log search and analytics | ELK |
| Eval-heavy debugging during development | Phoenix |
| One small app for a small team | SigNoz |
| Prompt and session-level LLM semantics | Langfuse |

## Instrumenting agent steps with OpenTelemetry

Graph frameworks such as LangGraph already isolate each step (plan, tool call, generation) as a declared async node, which makes per-node spans natural. No architectural rewrite is needed: initialize the SDK once at startup, open a span per node with a context manager; trace context flows through async calls so branched flows stay correlated.

Attributes per node type:
- **Tool node**: tool name, method, latency, success or failure, error code.
- **Generation node**: prompt or template ID and version, input and output tokens, model latency, model name, confidence or hallucination-risk flags.
- **Every span**: request ID, session ID, agent config or version, skill name, eval signals, plus product tags (workflow ID, feature flag, customer tier).

Enrich spans with events (retry fired, fallback taken), child spans for downstream API calls, and recorded exceptions so errors are tagged automatically. Also emit metrics: invocation counts per tool, mean latency per planning node, failure percentage per model version.

Scoping rule: too much detail drowns the signal; too little blocks root cause analysis. Attach just the identifiers and state needed for a coherent, searchable evidence trail.

Illustrative decorator (original sketch):

```python
import functools, time
from opentelemetry import trace as otel
tracer = otel.get_tracer(__name__)

def traced_step(kind):
    def wrap(fn):
        @functools.wraps(fn)
        async def inner(state, *a, **kw):
            with tracer.start_as_current_span(f"{kind}:{fn.__name__}") as sp:
                sp.set_attribute("session.id", state.get("session_id", ""))
                sp.set_attribute("agent.version", state.get("version", ""))
                try:
                    out = await fn(state, *a, **kw)
                    sp.set_attribute("tokens.total", out.get("tokens", 0))
                    return out
                except Exception as e:
                    sp.record_exception(e)
                    sp.set_status(otel.Status(otel.StatusCode.ERROR))
                    raise
        return inner
    return wrap
```

## Role of each backend

- **Tempo** (or Jaeger): trace store. Query by span attribute, e.g. runs whose planning span exceeded 1.5 s, or tool calls failing with a specific error code. Best for multistep bugs that only appear under real traffic.
- **Loki**: structured JSON log aggregation. Emit events when a query arrives, a tool is called, a generation is ambiguous, a fallback fires. Stamp trace and span IDs on every log line. When you need richer text search, per-role log views or more ingest capacity, consider Elasticsearch, Datadog logs or Honeycomb.
- **Grafana**: unifies both. Browse span hierarchies per run, filter by latency, status, span name or custom attributes; filter logs by agent, session, error type or trace ID; jump from a log spike straight to the causing trace.

## Dashboards worth building

- Tokens per agent per hour (catches verbosity regressions).
- P95 latency for tool and planning nodes.
- Task success rate split by workflow and prompt template version.
- Fallback count split by tool or skill.
- Query-embedding similarity to baseline over time (drift).
- Cost, request rate and duration by model and vector store.

## Alert rules and escalation

Example thresholds to adapt:
- Hallucination rate above 5% over a 30-minute window.
- More than 3 retry loops inside one session.
- Mean latency of a critical tool up more than 50% versus baseline.

Route to Slack, email or PagerDuty; use PagerDuty for paging, acknowledgment and on-call escalation of high-severity events (hallucination or failure spikes). Add Sentry for exception capture in agent code (stack traces, breadcrumbs, release health), instrumented alongside OTel. Choose: Grafana plus PagerDuty/Sentry for robust ops, or an agent-specific platform for speed, based on operational maturity.

## Pitfalls

- Logs without trace IDs: no way to pivot from a symptom to the run.
- Spans without version tags: canary and shadow comparisons become impossible.
- Alerting only on dashboards someone must watch; alerts exist so nobody has to.
