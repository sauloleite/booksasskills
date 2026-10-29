---
name: ai-eng-ch10-architecture-and-user-feedback
description: Production architecture and user feedback for LLM apps, based on Chapter 10 of Chip Huyen's "AI Engineering". Covers build order (context, guardrails, routers, gateways, caches, agents, write actions), observability (metrics, logs, traces, drift), orchestration, and feedback design and bias. Use when designing or reviewing an LLM system, adding a gateway or semantic cache, handling PII sent to external APIs, setting up monitoring, choosing an orchestrator, mining chat logs for implicit signals, or planning to train on user feedback.
---

# AI Engineering Architecture and User Feedback (Chip Huyen, Chapter 10)

This skill helps an agent design, review, and operate a production foundation-model application as a whole system, then close the loop with user feedback. The chapter grows an architecture from a single model call by adding one component per observed weakness, makes observability a design requirement, and treats user feedback as both an evaluation signal and proprietary training data that carries bias and privacy risk. Use the rules below directly; open a reference file when you need the full playbook, worked example, or checklist for one area.

## Key decision rules

**Architecture growth**
- Start from the bare path (query to model, response back). Add components only when a named need appears. Usual order: context, guardrails, router and gateway, caches, agent loops and write actions. Reorder to fit your risk profile.
- Every component adds capability and new failure modes. Write down both before adding it, and make sure tracing covers it.
- Components overlap (guardrails can sit in the inference service, gateway, or standalone). Place them by ownership and observability.

**Context**
- Prototype with provider-native file upload and tools; move to a dedicated retrieval stack when document count, formats, chunking control, or tool execution modes (parallel calls, long jobs) outgrow the provider.

**Guardrails**
- Input guardrails address two risks: private data leaving via external APIs, and malicious prompts. Neither reaches zero.
- Scan all three leak paths: user input, the system prompt, and tool results. On detection, block the query or mask with numbered typed placeholders plus a per-request reverse map for unmasking.
- Output guardrails must both detect and apply a per-failure policy: retry for empty or malformed output, block or regenerate for quality and safety failures, hand off to a human on trigger phrases, detected anger, or too many turns.
- Sequential retry roughly doubles latency for failed requests; parallel double-sampling keeps latency flat but pays for redundant calls.
- Always report false refusal rate next to safety metrics.
- Streaming defeats output checks on partial text. Buffer, check at sentence boundaries, or disable streaming on risky routes.
- Skipping guardrails for latency is a documented risk decision, never a default.

**Routing and gateway**
- Routers (intent classifier, next-action predictor, memory-tier selector) must be small, fast, and cheap. Use them for specialization, cost, out-of-scope declines without a generation call, and clarifying ambiguous queries.
- Predefine what happens when gathered context exceeds the routed model's window: truncate or reroute to a larger-window model.
- Add a model gateway once there are multiple models or teams: unified interface, no raw provider keys in apps, per-model permissions, quotas and cost tracking, fallback on outages and rate limits, logging.

**Caching**
- Exact cache for expensive, repeated, multi-step work, including vector search results. Set an eviction policy.
- Never cache user-specific or time-sensitive answers, nor any answer built from personal context under a generic key (cross-user leak).
- Semantic cache only after measuring a high hit rate, a tuned threshold with acceptable wrong-hit rate, and savings that exceed the per-query lookup cost.

**Agents and orchestration**
- Add read-only tools and loops before write actions. Gate writes with least privilege, caps, audit logs, and human approval for irreversible actions.
- Build without an orchestration framework first. When adopting one, judge integration and extensibility, complex pipeline support, and ease of use, performance, and scale; reject hidden calls or added latency.
- Run independent steps in parallel (routing and PII removal) on latency-critical paths.

**Observability**
- Know MTTD, MTTR, and CFR. Unknown CFR means the platform needs redesign; high CFR means pre-deployment evaluation is leaking bad changes.
- Derive every metric from a failure mode you want to catch. Start with format failures, then quality, safety, conversational, per-component, latency (TTFT, TPOT, total), and cost metrics.
- Slice metrics by user, release, prompt or chain version and type, and time. Correlate with north star metrics.
- Log everything with IDs and low ingestion delay. Emit per-request traces with step timing and cost.
- Watch three drift sources: silent system prompt edits, user behavior adapting to the product, and model updates behind an unchanged API name.
- Read a sample of production data daily and feed every incident into evaluation.

**User feedback**
- Use feedback for evaluation, development (including preference pairs), and personalization. It is user data: respect privacy, explain usage, get consent before capturing context.
- Explicit feedback is clear but sparse and skewed negative; implicit feedback is abundant but ambiguous. Combine signals and study your users before trusting any one.
- Collect at onboarding (only if required), on failure, on low confidence, and sparingly on success (a small random slice). Embed collection in the workflow so it costs nothing extra.
- Always offer an abstain option; never ask users to judge what they cannot evaluate; test scale direction.
- Before training on feedback, correct for leniency, randomness, position, length, and recency bias, reserve exploration traffic against degenerate loops, and test for sycophancy.

## Default workflow

1. Clarify the app's tasks, risk profile, latency budget, and whether the model is hosted or self-hosted.
2. Map the current architecture against the build order; list missing components and the weakness each would fix.
3. Specify guardrail policies per failure type, including leak-path coverage and streaming handling.
4. Decide on router, gateway, and cache with the criteria above; run `scripts/cache_savings.py` before adopting any cache.
5. Gate agent write actions; keep orchestration hand-written until complexity justifies a framework.
6. Define failure-mode metrics, slicing, logging, tracing, and drift checks before launch.
7. Design feedback touchpoints and consent; after launch, run `scripts/implicit_feedback.py` on conversation logs and review bias before any training use.

## References

- [references/context-and-guardrails.md](references/context-and-guardrails.md): read when deciding on context construction, PII masking, input or output guardrail policies, retries, human handoff, or streaming versus safety.
- [references/routing-gateway-and-caching.md](references/routing-gateway-and-caching.md): read when adding routers, a model gateway, or an exact or semantic cache, or when checking cacheability and cross-user leak risk.
- [references/agents-and-orchestration.md](references/agents-and-orchestration.md): read when adding agent loops or write actions, choosing or avoiding an orchestration framework, or cutting pipeline latency with parallelism.
- [references/observability.md](references/observability.md): read when defining production metrics, logging and tracing, incident debugging, or drift detection.
- [references/conversational-feedback-signals.md](references/conversational-feedback-signals.md): read when extracting explicit or implicit feedback from conversations, building a complaint taxonomy, or interpreting ambiguous user actions.
- [references/feedback-design-and-limitations.md](references/feedback-design-and-limitations.md): read when designing feedback UI and timing, handling consent and visibility, or preparing feedback for training while controlling bias, degenerate loops, and sycophancy.
- [references/source-map.md](references/source-map.md): read when you need to locate which reference covers a given chapter section.

## Scripts

Python 3 standard library only; each supports `--help`.

- Run `python3 scripts/cache_savings.py --gen-latency 1.2 --gen-cost 0.004 --lookup-latency 0.04 --lookup-cost 0.0001 --hit-rate 0.30 --wrong-hit-share 0.02 --wrong-hit-penalty 0.05 --queries-per-day 100000` to compute mean latency and cost per query with and without a cache, daily cost, expected wrong answers served, and the break-even hit rates for latency and cost.
- Run `python3 scripts/implicit_feedback.py conversations.jsonl --per-conversation` to compute per-conversation implicit signals (early stop, regenerate, edit, correction, rephrase, confirmation request, refusal, negative sentiment, loop) and their rates across a JSONL conversation log; add `--json` for machine-readable output. The input schema is in the script docstring.
