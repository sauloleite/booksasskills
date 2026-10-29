# Metric Ownership and Cross-Functional Governance

## The problem

Classic orgs split metrics cleanly: infra owns latency and uptime, product owns conversion, ML owns model health. Agents dissolve that split:
- The model's response is the product, not a model artifact.
- A chain of tool calls, retries and fallbacks is the user experience, not a backend detail.
- A slow plan generation is usually a prompt or workflow design choice, not an inherent model limit.

Consequence: agent logs, traces and eval signals must sit in the core observability platform next to service health. If they live only in product dashboards and ML notebooks, systemic problems stay hidden.

## Latency normalization trap

Teams that accept "LLMs are just slow" pile up delay: verbose prompts, needless retries, oversized plans. Without trace-level instrumentation this creep is invisible until the whole product feels sluggish, and the cause is design, not hardware. Fix: hold model-backed latency to the same bar as any other service.

## Shared views by role

- Product: planning latency and fallback rate plotted against abandonment.
- ML engineering: hallucination and drift next to user feedback.
- Infra/SRE: alerts on token spikes and flaky tools that threaten reliability.

Each function owns a slice; none can read the telemetry correctly alone.

## RACI for agent metrics

R = does the work, A = owns the outcome (exactly one per row), C = consulted, I = informed. Suggested starting assignment (adapt to org size):

| Metric or activity | Accountable | Responsible | Consulted | Informed |
|---|---|---|---|---|
| Latency (planning, tool calls) | Product | ML (prompts, models), SRE (infra causes) | Product (UX limits), SRE (scaling) | ML |
| Hallucination rate | ML | ML | Product (user context) | Product, SRE |
| Task success rate | Product | Product (defines success) | ML | SRE |
| Token usage and cost | SRE (budget, scaling) | ML (generation efficiency), SRE | Product (business impact) | ML |
| Distribution shift | ML | ML | SRE (pipeline stability) | Product |
| Fallback and retry frequency | SRE (reliability) | ML (planner logic) | Product (UX of fallbacks) | SRE |
| User feedback and sentiment | Product | Product | ML | SRE |
| Dashboards and triage rituals | SRE | SRE | Product, ML | (all) |

## Operating practices

- One set of shared dashboards with version tags and semantic metrics; teams improve the customer experience together instead of arguing about whose numbers are right.
- Stamp every span and log line with product tags: workflow ID, feature flag, customer tier.
- Hold joint triage sessions (product, infra, ML) on telemetry, especially after launches and major regressions.
- No double standard for model latency: user-facing slowness belongs to everyone.

## Diagnostic example

A trace shows one tool invoked four times in a loop, then a long generation, a vague reply and the user leaving. That is a product failure, visible only because spans and logs land in a shared platform. In triage: ML owns the loop (planner), product owns the abandonment impact and success criteria, SRE owns the retry alert that should have fired.
