# Failure Triage and the Agent Metric Taxonomy

## Contents
- Why agents need monitoring as a learning loop
- Failure versus expected variation: triage procedure
- What to measure: four-layer metric taxonomy
- One pipeline, not a parallel stack
- Privacy and access control for telemetry
- Pitfalls
- Worked example

## Why agents need monitoring as a learning loop

Agents are probabilistic, chain tools together and accept unbounded input, so no pre-release test suite can be exhaustive. Production is where the real test distribution lives. Treat monitoring as the sensory layer of the deployed system, and as the engine of a feedback loop: teams that observe well iterate faster and ship more safely.

Root causes span three families, each needing its own detection and fix:
- Software bugs (wrappers, parsing, integration code).
- Foundation model variation (provider updates, sampling noise, prompt sensitivity).
- Architectural limits (planning depth, tool coverage, context constraints).

Most agent failures are quiet. Typical shapes:
- A tool call returns success, but its output poisons later steps.
- A fluent, confident answer that is wrong.
- A plan that executes partially and never reaches the user's goal.

None of these crash a process, so infrastructure health checks alone will miss them.

Every production trace is a candidate test case. Failures become regression tests; unusually good runs become "golden paths" to preserve. Feeding both into CI keeps the eval corpus aligned with production complexity, which shifts detection left into development.

## Failure versus expected variation: triage procedure

The core difficulty: outputs vary run to run even when the system is healthy. Use this ordered check before reacting to any bad output.

1. **Does the output meet success criteria?** (example bar: eval score above 0.8). If yes, no action; keep watching trends.
2. **Is it reproducible?** Rerun the same input 3 to 5 times. If it fails in more than 80% of reruns, classify as a systematic bug and route to engineering.
3. **If not reproducible, is it within normal variance?** Compare against baseline confidence and distribution bounds (example: LLM judge score above 0.7 and KL divergence from baseline under 0.2).
   - Inside bounds: expected nondeterminism. Log it and add to drift watch.
   - Outside bounds: anomalous failure. Check for input drift (example: PSI above 0.1) and apply mitigation such as guardrails, prompt fixes or retraining.

Encode this tree in alerting rules and dashboards so the on-call person does not chase noise, yet genuine degradation surfaces early. The numbers are starting points; calibrate them on your own baseline.

## What to measure: four-layer metric taxonomy

Collect what is needed to detect meaningful change and diagnose it quickly, not everything. Organize by layer:

| Layer | Signals | Typical response when it moves |
|---|---|---|
| Infrastructure | CPU and memory; availability; request latency at P50/P95/P99 | Scale out, slim memory-heavy tools, open an incident, tune caching or retry policy |
| Workflow | Task completion rate; tokens per workflow; tool call error rate; tool rate-limit breaches; retry count; fallback count | Inspect failing runs, revise prompts, patch tool wrappers, auto-fallback, adjust call budgets, debounce retries, fix planner logic, escalate to a human |
| Output quality | Input and output tokens (verbosity, cost); hallucination indicator; embedding drift versus baseline | Trim prompts or move to another model tier, add grounding or a critic step, adapt workflows or fine-tune |
| User | Rephrase/requery rate; abandonment rate; thumbs or star ratings | Improve intent recognition, simplify the flow or add clarifying questions, route low-rated runs to evaluation |

Notes:
- Token usage appears twice on purpose: at workflow level a sudden rise or fall is an anomaly signal; at output level it is a cost and verbosity signal.
- Semantic questions matter as much as infra ones: was intent understood, was the right tool picked, was content invented, did the user give up midway.

## One pipeline, not a parallel stack

Route agent telemetry into the same observability platform that already watches production services. The Prometheus that scrapes service health can also hold agent success rates; SRE dashboards can plot tool usage, the spread of model latency and semantic failure rates beside CPU. Agents deserve the same rigor as any critical service. Layer evaluation signals (hallucination scores, drift indicators from external critics) onto runtime events as they stream.

## Privacy and access control for telemetry

Agent telemetry carries user messages, tool arguments and intermediate generations. Controls:
- Separate monitoring clusters for sensitive data, with strict RBAC.
- Encryption at rest and access auditing on those backends.
- Redact, hash or mask PII before export. OpenTelemetry exporters and processors offer hooks to scrub span data at the application boundary.

Sketch of a scrubbing step applied before export (framework-agnostic):

```python
import hashlib, re
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
SENSITIVE_KEYS = {"user.message", "tool.args", "llm.completion"}

def scrub(attrs: dict) -> dict:
    out = {}
    for k, v in attrs.items():
        if k == "user.id":
            out[k] = hashlib.sha256(str(v).encode()).hexdigest()[:16]
        elif k in SENSITIVE_KEYS:
            out[k] = EMAIL.sub("<email>", str(v))
        else:
            out[k] = v
    return out
```

## Pitfalls

- Alerting on single bad outputs without the reproducibility check: floods on-call with noise.
- Watching only infra metrics: silent semantic failures pass as healthy.
- Building a separate "AI monitoring" island that SREs never see.
- Exporting raw prompts and completions to a broadly readable log store.

## Worked example

A support agent's eval score on a refund query drops to 0.55. Rerunning 5 times yields 2 failures (40%), so it is not systematic. Judge score on the failing runs is 0.62, below the 0.7 bound, so it is anomalous rather than routine noise. PSI on tool-intent categories this week versus last month is 0.14: minor input drift. Action: add the case to the regression set, add a clarifying-question guardrail for the new phrasing, and keep PSI on the dashboard.
