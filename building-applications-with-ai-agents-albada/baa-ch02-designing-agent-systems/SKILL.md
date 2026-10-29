---
name: baa-ch02-designing-agent-systems
description: Guides end-to-end design of an agent system, based on Chapter 2 of Michael Albada's "Building Applications with AI Agents" (O'Reilly, 2025). Covers scoping a first bounded workflow, model selection (size, modality, open vs proprietary, routing, VRAM), tools, memory, orchestration, speed/scale/reliability/cost trade-offs, single vs multiagent choice, evaluation and phased rollout. Use when starting an agent project, choosing or pricing models, deciding whether to go multiagent, or planning agent testing and production launch.
---

# Designing Agent Systems (Albada, Chapter 2)

Purpose: help an engineer go from a messy problem and an API key to a small, tested, useful agent, then grow it deliberately. The chapter is the book's quick-start overview: scope a narrow slice, assemble the core components (model, tools, memory, orchestration), make the main trade-offs explicit, choose single or multiagent structure, and adopt iterative design, layered evaluation and staged real-world testing. Its running example is an ecommerce support agent that cancels orders, issues refunds and changes addresses.

## Key decision rules

**Scoping**
- Start with a slice humans already do by rule: read text, look up a record, press a button, reply.
- Reject scopes that are too narrow (trivial impact), too broad (edge-case flood) or vague (no success test).
- A good slice has concrete inputs, structured outputs (tool call plus confirmation) and a fast automatic check.
- Expand to sibling intents that share inputs and output shape before broader categories.

**Evaluate before expanding**
- "An untested agent is an untrusted agent."
- Per case check: right tool, right arguments, correct confirmation. In aggregate: tool precision/recall, parameter accuracy, task success, reply quality. Include negative cases.

**Model selection** (start from task complexity)
- Open-ended, ambiguous, multistep: large frontier model. Narrow, repetitive, latency- or hardware-bound: small model; it can win by being practical.
- Multimodal only if decisions truly combine modalities; otherwise text-only is faster and simpler.
- Open weights for privacy, regulation, deep customization (you pay in engineering). Proprietary APIs for speed to market (you pay in usage and limited control).
- Custom domain training only for specialized, high-stakes domains; otherwise pretrained plus prompting or light tuning.
- Use tiered or dynamic routing: cheap model for routine requests, strong model for hard ones.
- Benchmarks (MMLU via HELM) are a rough common ruler; price does not track score. Decide by price per unit of performance on your own task set.
- Hardware: about 2 to 2.5 GB VRAM per billion params at 16-bit; up to roughly 14B fits one 24 GB consumer GPU; beyond that use 40/80 GB server GPUs; frontier models need a dozen-plus GPUs, so use hosted per-token APIs.
- Revisit model choice periodically; it is not a one-time decision.

**Tools, memory, orchestration**
- Tool types: local (internal logic), API-based (external services), MCP (standardized context and capabilities). Build each tool as a swappable module; keep hard business rules in tools, not only prompts.
- Short-term memory: rolling window. Long-term: databases, knowledge graphs or fine-tuned weights. Index, filter for relevance, forget stale data, weight recency.
- Orchestration composes and supervises steps: plan a few steps, re-evaluate, reroute when the environment changes.

**Trade-offs**
- Speed vs accuracy: real-time domains favor speed, legal/medical favor accuracy, interactive cases use fast-then-refine.
- Scale GPUs by utilization first (dynamic allocation, elastic provisioning, priority queues, async execution, load balancing), then capacity (horizontal nodes, hybrid cloud burst, off-peak batch). Adding GPUs alone is not scaling.
- Reliability: fault tolerance with redundancy, testing on edge and adversarial inputs, production monitoring with feedback loops. Size it to failure consequences.
- Cost: count development and operational spend against value; prefer rules or lean models when they match, pay-as-you-go cloud, open-source tooling.

**Architecture**
- Default to a single agent for well-defined, narrow work.
- Go multiagent only for real specialization, parallelism, scale or fault isolation; it adds coordination complexity and token overhead. Decide on task complexity, scalability need and expected system lifespan.

**Delivery**
- Iterate: fast prototype, feedback, refine.
- Evaluate in layers: functional (correctness, boundaries, domain metrics), generalization, UX signals (NPS/CSAT, completion, explicit and implicit feedback), expert review to calibrate automated graders, end-to-end in realistic environments.
- Roll out in phases, monitoring response time, accuracy, satisfaction and stability, feeding findings back.

## Default workflow

1. Mine the request stream; pick one bounded, high-volume intent; write the success test.
2. Map the human procedure to tools and a minimal model-tool-model loop.
3. Build an eval set (positives, negatives, edge cases) and pass it before adding scope.
4. Choose the model by task complexity, modality, openness and measured price per performance; run the cost script.
5. Add memory and orchestration only as the workflow needs them.
6. Fill in the trade-off worksheet (latency budget, failure cost, load shape, lifespan).
7. Stay single-agent unless the multiagent criteria clearly hold.
8. Release in phases with monitoring and feedback controls; iterate.

## References

- [references/scoping-the-first-agent.md](references/scoping-the-first-agent.md): read when defining a first agent's scope, mapping a manual process to tools, or writing its first evaluation harness.
- [references/core-components.md](references/core-components.md): read when choosing a model, reading benchmark and price data, sizing GPUs, designing tool categories, memory, or orchestration.
- [references/design-trade-offs.md](references/design-trade-offs.md): read when balancing latency against accuracy, planning GPU scaling, setting reliability investment, or estimating development and operating cost.
- [references/architecture-patterns.md](references/architecture-patterns.md): read when deciding between single-agent and multiagent designs.
- [references/evaluation-and-rollout.md](references/evaluation-and-rollout.md): read when planning iterative development, an evaluation framework, user feedback signals, or a phased production launch.
- [references/source-map.md](references/source-map.md): read to find which file covers a given chapter section.

## Scripts

Python 3 standard library, deterministic, `--help` on every subcommand.

- Run `python3 scripts/model_cost_compare.py cost models.json --in-tokens 1500 --out-tokens 300 --requests 100000` to compute cost per request, monthly cost and cost per successful task for candidate models (JSON list of `name`, `in_price`, `out_price` per million tokens, `score` = success rate on your eval). Add `--route "small=0.8,large=0.2"` to price a hybrid routing blend, and `--failure-cost 0.5` to include the cost of handling failures in the ranking.
- Run `python3 scripts/model_cost_compare.py vram --params 14 --bytes-per-param 2` to estimate VRAM for an open-weight model and how many 24, 40 or 80 GB GPUs it needs.
