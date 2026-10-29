---
name: baa-theme-agent-design-foundations
description: Theme skill covering the foundations of agent design from Michael Albada's "Building Applications with AI Agents" (chapters 1 to 3). Use when deciding whether a problem needs an agent at all, scoping a first agent, choosing models and frameworks, laying out core components and architecture, or designing the user experience (modality, sync vs async, autonomy levels, clarification, failure handling and trust).
---

# Agent design foundations (Building Applications with AI Agents, ch. 1 to 3)

Covers the decisions made before any tool or memory work: whether to build an agent, what the first one should do, how it is put together, and how people will experience it. References and scripts from the three chapters are bundled below.

## Cross-chapter rules

1. **Pick the lowest tier that works.** Plain code, then a fixed workflow, then a chatbot or RAG, then an autonomous agent. Climb only when inputs are open-ended and the work needs adaptive multistep planning, real actions or learning from feedback, and the gain outweighs latency, cost, opacity and governance burden.
2. **Scope the first agent narrowly.** Choose a bounded task people already do by rule, with concrete inputs, a structured output (a tool call plus a confirmation) and a fast automatic check of success.
3. **Four components, each replaceable.** Model, tools, memory and orchestration. Keep tools modular and the model swappable; route easy requests to small models and hard ones to strong models, choosing by cost per successful task on your own eval set.
4. **Default to one agent.** Add agents only for real specialization, parallelism, scale or fault isolation.
5. **Test before trust.** Measure tool choice, argument accuracy and confirmations on hundreds of real cases before widening scope.
6. **Design the experience deliberately.** Choose modality by the user's situation, decide sync or async for every flow, expose capabilities explicitly in text and voice, and make autonomy a visible, adjustable setting that rises only with a track record.
7. **Calibrate and fail well.** Match stated confidence to stakes, ask specific clarifying questions for the most critical gap first, and on failure acknowledge, explain, preserve progress and offer a next step or a human.

## Default workflow

1. Run the tier decision and the gating questions (ch01 references).
2. Write the first agent's scope, success check and eval cases (ch02).
3. Sketch components, model routing and the architecture pattern (ch02); use `scripts/model_cost_compare.py` to price candidates.
4. Design interaction: modality, sync or async, autonomy levels, context retention, failure paths (ch03).
5. Hand off to the tools, memory, evaluation and security themes for the next layers.

<!-- BEGIN GENERATED: run tools/build_bundles.py to refresh -->

## References by chapter

Each link is one level deep; read only the files whose description matches the task.

### CH01: Introduction to Agents

- [ch01-agent-types-and-use-cases.md](references/ch01-agent-types-and-use-cases.md): read when classifying a request into an agent type (including browser, voice, video) or borrowing actions and risks from the book's seven reference agents.
- [ch01-models-and-frameworks.md](references/ch01-models-and-frameworks.md): read when choosing a model, planning small-model routing, judging benchmark gaps, mapping needed model capabilities, or picking among LangGraph, AutoGen, CrewAI, OpenAI Agents SDK or no framework.
- [ch01-principles-and-organization.md](references/ch01-principles-and-organization.md): read when reviewing an agent design for scalability, modularity, learning, resilience and future-proofing, or advising how teams should explore, standardize and govern agent work.
- [ch01-solution-tier-selection.md](references/ch01-solution-tier-selection.md): read when deciding between code, workflow, RAG and agent, defining what counts as an agent, designing asynchronous prepared-work flows, or writing a tier decision record.

### CH02: Designing Agent Systems

- [ch02-architecture-patterns.md](references/ch02-architecture-patterns.md): read when deciding between single-agent and multiagent designs.
- [ch02-core-components.md](references/ch02-core-components.md): read when choosing a model, reading benchmark and price data, sizing GPUs, designing tool categories, memory, or orchestration.
- [ch02-design-trade-offs.md](references/ch02-design-trade-offs.md): read when balancing latency against accuracy, planning GPU scaling, setting reliability investment, or estimating development and operating cost.
- [ch02-evaluation-and-rollout.md](references/ch02-evaluation-and-rollout.md): read when planning iterative development, an evaluation framework, user feedback signals, or a phased production launch.
- [ch02-scoping-the-first-agent.md](references/ch02-scoping-the-first-agent.md): read when defining a first agent's scope, mapping a manual process to tools, or writing its first evaluation harness.

### CH03: User Experience Design for Agentic Systems

- [ch03-autonomy-and-engagement-timing.md](references/ch03-autonomy-and-engagement-timing.md): read when setting human-approval levels, deciding sync vs async, or designing notifications and proactive behavior.
- [ch03-capabilities-uncertainty-clarification.md](references/ch03-capabilities-uncertainty-clarification.md): read when users do not know what the agent can do, when expressing confidence, or when writing clarifying-question logic.
- [ch03-context-and-personalization.md](references/ch03-context-and-personalization.md): read when deciding where context lives, handling state for anonymous or logged-in users at scale, or adding personalization.
- [ch03-graceful-failure-and-trust.md](references/ch03-graceful-failure-and-trust.md): read when designing error handling, fallbacks and escalation, or reviewing an agent for trust, predictability and reliability.
- [ch03-interaction-modalities.md](references/ch03-interaction-modalities.md): read when choosing or combining text, GUI, generative UI, voice or video, or when building a voice agent with interruptions.

Merged section maps: [source-maps.md](references/source-maps.md).

## Scripts

Python 3 standard library only; run any script with `--help` for its arguments.

| Script | Purpose |
|---|---|
| `scripts/model_cost_compare.py` (ch02) | Compare candidate models by cost per successful task, and estimate VRAM fit. |

<!-- END GENERATED -->
