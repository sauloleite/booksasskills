# Monitoring-Aware Release Patterns and User Feedback

## Contents
- Pattern selection
- Shadow mode
- Canary deployments
- Regression trace collection
- Self-healing agents
- User feedback as telemetry
- Worked example

## Pattern selection

Once telemetry exists, use it to de-risk changes to a system you cannot fully predict. Escalating exposure:

| Pattern | User exposure | Use it to answer |
|---|---|---|
| Shadow mode | None | Is the candidate better or worse on live inputs? What breaks? |
| Canary | Small slice (e.g. 1% to 5%) | Does it hold up with real users before wider rollout? |
| Regression trace collection | n/a (offline) | Did the fix work, and will this failure ever return? |
| Self-healing | Runtime | Can the agent degrade gracefully when telemetry shows trouble? |

Typical path for a new model, planner or prompt: shadow, then canary, then gradual ramp; feed every failure into the regression corpus throughout.

## Shadow mode

Run the candidate agent in parallel on the same inputs as production; never return its output to users.
- Share one request ID across both runs; label shadow spans and logs (e.g. `deployment.role=shadow`).
- Compare tool choices, latency, token use, hallucination frequency.
- Best for trialing new model versions, planning strategies or prompting techniques.
- Collects comparison data continuously alongside normal traffic.
- Watch side effects: a shadow agent must not execute write actions (refunds, emails); stub or sandbox mutating tools.

## Canary deployments

Serve the candidate to a small share of real users while the rest stay on baseline.
- Tag every metric and trace with version; filter dashboards by that tag to compare success, latency, tool use, errors.
- Alert when the canary regresses significantly against baseline.
- Healthy: widen gradually. Unhealthy: roll back at once; blast radius is small.

Minimal comparison gate (original sketch):

```python
def canary_ok(base, canary, max_success_drop=0.02, max_p95_ratio=1.2,
              max_error_ratio=1.5, min_runs=500):
    if canary["runs"] < min_runs:
        return None  # not enough evidence yet
    if base["success"] - canary["success"] > max_success_drop:
        return False
    if canary["p95_ms"] > base["p95_ms"] * max_p95_ratio:
        return False
    if canary["error_rate"] > base["error_rate"] * max_error_ratio:
        return False
    return True
```

## Regression trace collection

Every production failure (hallucination, bad plan, tool misuse) is a free test case.
- Export failing traces from the trace store or log snapshots automatically into the test suite.
- After a fix, the replayed trace must pass.
- Over time the eval set fills with real edge cases and repeat failures are blocked.
- Also export exemplary successes as golden paths, and traces with low user ratings for post hoc review.

## Self-healing agents

Let the agent read its own live telemetry and pick a fallback:
- Repeated tool failure: switch to a simpler plan or ask the user to clarify.
- Latency spike: drop optional reasoning steps.
- High hallucination score: attach a disclaimer or hand off to human review.

Log and trace every fallback decision with its trigger, so the team can audit when fallbacks fired and whether they actually resolved the problem. Fallback frequency is itself a dashboard metric.

## User feedback as telemetry

Two kinds, both belong in the monitoring stack:
- **Implicit**: rephrasing or requerying, abandonment, hesitation. Aggregate like any other metric; these are early friction indicators.
- **Explicit**: thumbs down, star ratings, free-text comments. Attach to the specific trace; alert when dissatisfaction spikes.

Combine sentiment panels with trace-based technical panels so latency or failure changes can be correlated with frustration. Close the loop:
- Low-rated traces go to the evaluation set.
- Repeated abandonment of one flow signals the planning strategy or prompt needs rework.

## Worked example

A team swaps the planner model. Shadow for a week: candidate cuts tokens 30% but picks the wrong tool on 4% of billing queries versus 1% baseline. They fix the tool descriptions, re-shadow, then canary at 5%. The gate above passes after 2,000 runs; rollout widens to 25%, then 100%. The billing misroutes found during shadow are now permanent regression tests.
