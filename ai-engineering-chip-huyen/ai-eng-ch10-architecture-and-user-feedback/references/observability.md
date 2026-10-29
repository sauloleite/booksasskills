# Monitoring, Observability, Logs, Traces, and Drift

## Contents
- Goals and meta-metrics
- Monitoring versus observability
- Designing metrics from failure modes
- Metric catalogue
- Slicing, sampling, north star correlation
- Logs
- Traces and the debugging workflow
- Drift detection
- Daily data review
- Pitfalls and glossary

## Goals and meta-metrics

Design observability in from day one; its importance grows with complexity. General software observability is mature, so this file covers what is specific to foundation-model apps. Monitoring shares evaluation's goals: mitigate risks (failures, attacks, drift), find opportunities (quality gains, cost savings), and provide accountability.

Judge the observability practice itself with three DevOps metrics:

| Metric | Measures |
|---|---|
| MTTD, mean time to detection | Delay from incident start to awareness |
| MTTR, mean time to response | Delay from detection to resolution |
| CFR, change failure rate | Share of deployments needing a fix or rollback |

- Not knowing CFR means the platform must be made more observable.
- High CFR is not necessarily a monitoring failure; it usually means pre-deployment evaluation lets bad changes through. Fix evaluation.
- Offline and online metrics must agree: what scores well in evaluation should score well in production, and production issues must flow back into evaluation sets.

## Monitoring versus observability

**Monitoring** tracks external outputs to notice that something is wrong, with no guarantee those outputs explain why. **Observability** assumes the system emits enough runtime information that internal state can be inferred from logs and metrics, so a failure can be diagnosed without deploying new code. Working usage: monitoring is the tracking; observability is the full loop of instrumenting, tracking, and debugging.

## Designing metrics from failure modes

A metric earns its place by flagging a problem or an improvement; a relevance score that drives no decision is noise.
1. List the failures you most want to catch.
2. Design a metric that moves when each happens. Hallucination: share of outputs inferable from the provided context. Runaway spend: input and output tokens per request, cache cost, cache hit rate.
3. Choose exhaustive or sampled computation.
4. Attach a threshold and an owner.

Open-ended outputs fail in many ways, so metric design needs analysis, statistics, and creativity, and is app-specific.

## Metric catalogue

- **Format** (start here, easy to verify): invalid structured output rate, and among invalid outputs the share trivially repairable (missing closing bracket) versus structurally wrong (required keys absent).
- **Open-ended quality**: factual consistency; app-relevant traits like conciseness, creativity, positivity; often scored by AI judges.
- **Safety**: toxicity; sensitive data in inputs and outputs; guardrail trigger rate; refusal rate; anomalous queries, which expose edge cases and prompt attacks.
- **Conversational**: share of generations stopped midway; turns per conversation; mean input tokens (harder tasks, or users learning to write tighter prompts?); mean output tokens (is one model wordier; which query types run long?); output token distribution over time (diversity rising or falling?). Length metrics also drive latency and cost.
- **Per-component**: retrieval context relevance and precision; vector DB index storage and query latency.
- **Latency**: TTFT, TPOT, total latency, tracked per user to see scaling.
- **Cost and capacity**: query volume, token volume, TPS, and RPS against provider rate limits to avoid interruptions.

## Slicing, sampling, north star correlation

- **Slice** every metric by user, release, prompt or chain version, prompt or chain type, and time; aggregates hide regressions.
- **Spot vs exhaustive**: sampled checks are cheap; exhaustive checks score every request. Mix by budget (exhaustive for cheap format checks, sampled for judge-based scores).
- **North star**: correlate metrics with DAU, session duration, or subscriptions. Strong correlates suggest levers; uncorrelated metrics tell you what not to optimize.

## Logs

Metrics aggregate and say that something changed; logs are an append-only event record that say what happened and whether it happened before. Because future needs are unknown, log everything:
- Configuration: endpoint, model name, sampling parameters (temperature, top-p, top-k, stop conditions), prompt template and version.
- Data: raw query, final assembled prompt, intermediate and final outputs.
- Tool invocations and their results.
- Component lifecycle: start, end, crash.
- Tags and IDs on every record identifying component and request.

Log freshness matters: if logs lag 15 minutes, an incident from 5 minutes ago cannot be investigated yet. Volume grows fast, so rely on automated (often AI-based) log analysis and anomaly detection.

## Traces and the debugging workflow

A trace links related events into one timeline for a request: query, actions, retrieved documents, final prompt, response, with time and cost per step (LangSmith is one visualizer). It should pinpoint whether a bad answer came from query processing (bad rewrite or route), irrelevant retrieval, or wrong generation from good context.

Debugging workflow:
1. A metric alert fires; cause unknown.
2. Pull logs around that time; check for precedent.
3. Correlate log errors with the metric shift to confirm the cause.
4. Open traces of affected requests to find the failing step.
5. Check the drift sources below.
6. Fix, add a regression case to evaluation, record MTTD and MTTR.

## Drift detection

- **System prompt changes.** A shared template is updated or someone fixes a typo, unannounced. Hash or diff the rendered system prompt per release and alert on change.
- **User behavior changes.** Users adapt to technology (search query phrasing, SEO tactics, even pedestrians learning to bully self-driving cars). Your users will learn what works, such as asking for brevity, so mean response length may drift down gradually. The metric shows the trend, not the cause; investigate actual queries.
- **Underlying model changes.** Providers may update the model behind an unchanged API name without notice. Published comparisons found clear benchmark differences between the March and June 2023 snapshots of GPT-4 and GPT-3.5, and Voiceflow reported about a 10% drop moving between two dated GPT-3.5-turbo snapshots. Pin dated versions, run a scheduled canary evaluation, and re-evaluate before any switch.

## Daily data review

Automation does not replace reading real traffic. Shankar et al. (2024) found developers' judgment of good and bad output shifts as they see more data, prompting both prompt rewrites and new evaluation checks. Review a sample of production conversations daily.

## Pitfalls and glossary

Pitfalls: observability deferred; metrics tied to no failure mode or business goal; no slicing by prompt version or release; logs without request IDs or arriving late; trusting a fixed API name; blaming monitoring for a CFR that evaluation should have prevented.

- **TTFT / TPOT**: time to first token, time per output token.
- **TPS / RPS**: tokens per second, requests per second.
- **North star metric**: core business outcome.
- **Trace**: linked, timed record of one request through all components.
