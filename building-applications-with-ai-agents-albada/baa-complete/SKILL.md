---
name: baa-complete
description: Whole-book guide to Michael Albada's "Building Applications with AI Agents" for designing, building, evaluating, operating and securing agentic and multiagent systems end to end. Use when a task spans several stages or it is unclear which chapter applies. Routes to per-topic references from all 13 chapters and bundles 15 tested scripts (tool linting, topology checks, context budgets, eval reports, trace and drift analysis, A/B and bandit analysis, permission audits).
---

# Building Applications with AI Agents, complete (Michael Albada, O'Reilly 2025)

Operating model for agentic systems condensed from the whole book. This file holds the cross-cutting rules and the router; depth lives in `references/` (chapter-prefixed topic files) and calculations in `scripts/`. Theme skills (`baa-theme-*`) cover the same material in smaller slices.

## Core rules (apply without opening references)

1. **Simplest tier that works.** Code, workflow, chatbot or RAG, then agent; add agents to a system only after single-agent fixes fail.
2. **Narrow first scope, tested before trusted.** Bounded task, structured outputs, automatic success checks, hundreds of real cases.
3. **Tools are contracts.** Precise names, distinct descriptions, strict schemas, least privilege, validation, retries, fallbacks and logs around every call.
4. **Orchestrate with the least machinery.** Pick the cheapest archetype and topology that meet requirements; engineer the context of every call.
5. **Escalate memory and learning on evidence.** Keyword and window first, then vectors, RAG, experience memory, GraphRAG; in-context learning before fine-tuning.
6. **Measure actions, not vibes.** Tool recall, precision, parameter accuracy and task success, automated on every change, with release gates set in advance.
7. **Observe agent behavior, not just servers.** Spans per step, four monitoring layers, explicit drift thresholds, failures turned into regression tests.
8. **Improve through a controlled loop.** Diagnose, fix prompts and tools first, validate through shadow, A/B or bandit and canary, then embed.
9. **Secure outside the model.** Defense in depth, threat modeling in layers, continuous red teaming, end-to-end data protection, contained failures.
10. **Grow autonomy with trust.** Visible autonomy levels, progressive delegation with a way back down, scope-based governance, explicit escalation and accountability.

## Lifecycle at a glance

| Stage | Question | Theme skill | Chapters |
|---|---|---|---|
| Decide and scope | Does this need an agent, and what is the first slice? | baa-theme-agent-design-foundations | 1, 2 |
| Design the experience | How will people interact with and trust it? | baa-theme-agent-design-foundations | 3 |
| Act | Which tools, archetype, topology and context? | baa-theme-tools-orchestration-multiagent | 4, 5 |
| Remember and learn | What does it know, remember and improve on? | baa-theme-memory-and-learning | 6, 7 |
| Scale out | Is a multiagent design justified, and how is it wired? | baa-theme-tools-orchestration-multiagent | 8 |
| Validate | Does it meet predefined gates? | baa-theme-evaluation-and-operations | 9 |
| Operate | What is happening in production, and is it drifting? | baa-theme-evaluation-and-operations | 10 |
| Improve | Which fixes, validated how, embedded where? | baa-theme-evaluation-and-operations | 11 |
| Protect and govern | Is it safe, accountable and compliant? | baa-theme-security-and-governance | 12, 13 |

For the stage-by-stage playbook, a symptom-to-fix map and a universal checklist, read [references/lifecycle-playbook.md](references/lifecycle-playbook.md).

## Default workflow

1. Place the task in a lifecycle stage. If it spans stages, start with [references/lifecycle-playbook.md](references/lifecycle-playbook.md).
2. Apply the core rules; open only the references whose "read when" line matches.
3. Run the matching script whenever numbers or structural checks are involved.
4. State assumptions and which rule or reference drove each recommendation.

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

### CH04: Tool Use

- [ch04-automated-tool-development.md](references/ch04-automated-tool-development.md): read when having a model generate tool wrappers from specs, or when deciding whether an agent may write and execute code at runtime.
- [ch04-mcp-integration.md](references/ch04-mcp-integration.md): read when exposing a service over MCP, connecting an agent to stdio or HTTP MCP servers, or reviewing MCP security.
- [ch04-stateful-tool-safety.md](references/ch04-stateful-tool-safety.md): read before giving an agent access to databases, files or any system whose data persists, or when reviewing an incident caused by a tool call.
- [ch04-tool-definition-and-invocation.md](references/ch04-tool-definition-and-invocation.md): read when writing or reviewing tool names, descriptions and schemas, wiring the bind/call/append loop, choosing a tool_choice mode, or building retry and fallback logic.
- [ch04-tool-types-and-selection.md](references/ch04-tool-types-and-selection.md): .

### CH05: Orchestration

- [ch05-agent-archetypes.md](references/ch05-agent-archetypes.md): read when choosing between reflex, ReAct, planner-executor, query-decomposition, reflection and deep research agents, or explaining their trade-offs.
- [ch05-context-engineering-and-planning-choice.md](references/ch05-context-engineering-and-planning-choice.md): read when assembling per-step context windows or running the final checklist for choosing and evaluating a planning approach.
- [ch05-tool-selection-and-execution.md](references/ch05-tool-selection-and-execution.md): read when designing how an agent picks tools from a catalog, writing tool descriptions, or handling parametrization, validation, timeouts and retries.
- [ch05-tool-topologies.md](references/ch05-tool-topologies.md): read when deciding between single-call, parallel, chain and graph execution, or designing and testing a branching graph.

### CH06: Knowledge and Memory

- [ch06-context-and-keyword-memory.md](references/ch06-context-and-keyword-memory.md): read when separating knowledge from memory, structuring memory as orchestration nodes, sizing or trimming the context window, or setting up BM25 keyword memory.
- [ch06-graphrag-and-knowledge-graphs.md](references/ch06-graphrag-and-knowledge-graphs.md): read when deciding whether GraphRAG is justified, choosing tooling, building or loading a knowledge graph, or writing multihop queries.
- [ch06-long-context-and-dynamic-graphs.md](references/ch06-long-context-and-dynamic-graphs.md): read when weighing long context against retrieval, considering a continuously updated graph, or choosing the overall memory architecture (escalation ladder and worked example).
- [ch06-semantic-memory-and-rag.md](references/ch06-semantic-memory-and-rag.md): read when adding embeddings and a vector store, building a RAG pipeline, designing semantic experience memory, or applying self-notes.

### CH07: Learning in Agentic Systems

- [ch07-fine-tuning-decisions.md](references/ch07-fine-tuning-decisions.md): read when deciding whether to fine-tune, which method to use, or whether a small or large model fits; includes decision walkthroughs.
- [ch07-nonparametric-learning.md](references/ch07-nonparametric-learning.md): read when designing exemplar banks, Reflexion loops or insight lists, or choosing between them; includes a worked example and pitfalls.
- [ch07-sft-dpo-rlvr-playbook.md](references/ch07-sft-dpo-rlvr-playbook.md): read when building tool-calling SFT data, configuring LoRA/SFT or DPO runs, designing RLVR graders, or combining both learning families.

### CH08: From One Agent to Many

- [ch08-agent-count-and-decomposition.md](references/ch08-agent-count-and-decomposition.md): read when deciding single vs multiagent, splitting an overloaded agent, considering a swarm, or justifying a new agent (includes a worked decomposition and the six-principle checklist).
- [ch08-communication-infrastructure.md](references/ch08-communication-infrastructure.md): read when moving beyond in-process calls: A2A cards and handshakes, broker patterns and hardening, Ray/Orleans/Akka and per-session actors, Temporal/Airflow/Dagger, plus a selection table.
- [ch08-coordination-strategies.md](references/ch08-coordination-strategies.md): read when choosing democratic, manager or hierarchical structure, designing an actor-critic loop, or evaluating ADAS / Meta Agent Search (loop steps and reported benchmark results).
- [ch08-state-and-persistence.md](references/ch08-state-and-persistence.md): read when deciding where agent memory, shared task state and artifacts live, and how to survive mid-workflow failures.

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

### CH12: Protecting Agentic Systems

- [ch12-agent-risks-and-threat-vectors.md](references/ch12-agent-risks-and-threat-vectors.md): read when explaining why agents need special security, designing human oversight, or building an attack taxonomy and test cases.
- [ch12-agent-safeguards-and-resilience.md](references/ch12-agent-safeguards-and-resilience.md): read when scoping agent permissions, hardening against external attackers, setting monitoring KPIs, or planning fallbacks, chaos experiments and postmortems.
- [ch12-data-protection.md](references/ch12-data-protection.md): read when handling PII or confidential data, designing encryption, provenance, integrity checks, audit trails, retention or cross-party data sharing.
- [ch12-maestro-threat-modeling.md](references/ch12-maestro-threat-modeling.md): read when running a structured threat model of an agent or multiagent system.
- [ch12-model-selection-defenses-red-teaming.md](references/ch12-model-selection-defenses-red-teaming.md): read when picking a model/hosting option, designing input/output guardrails, benchmarking detectors, or planning a red-team program and tooling.

### CH13: Human-Agent Collaboration

- [ch13-compliance-and-next-steps.md](references/ch13-compliance-and-next-steps.md): read when mapping regulations, building compliance into CI/CD, or writing a first-steps plan for an organization starting with agents.
- [ch13-roles-adoption-and-scaling.md](references/ch13-roles-adoption-and-scaling.md): read when choosing human roles, interface patterns per role, planning stakeholder alignment or a phased rollout, or deciding how an agent should grow from individual to enterprise use.
- [ch13-scope-access-and-memory.md](references/ch13-scope-access-and-memory.md): read when classifying an agent's scope, setting RBAC and per-scope policies, or designing shared memory and context-flow boundaries.
- [ch13-trust-accountability-and-escalation.md](references/ch13-trust-accountability-and-escalation.md): read when designing progressive delegation, trust repair, audits, logging and traceability, or escalation thresholds and oversight roles.

Merged section maps: [source-maps.md](references/source-maps.md).

## Scripts

Python 3 standard library only; run any script with `--help` for its arguments.

| Script | Purpose |
|---|---|
| `scripts/model_cost_compare.py` (ch02) | Compare candidate models by cost per successful task, and estimate VRAM fit. |
| `scripts/lint_tool_definitions.py` (ch04) | Lint a set of agent tool definitions for selection and safety problems. |
| `scripts/tool_selection_eval.py` (ch05) | Evaluate agent tool selection against labeled expectations. |
| `scripts/topology_check.py` (ch05) | Validate the structure of an agent orchestration graph before building it. |
| `scripts/context_budget.py` (ch06) | Plan a per-call context-window budget for an agent with layered memory. |
| `scripts/validate_finetune_jsonl.py` (ch07) | Validate a fine-tuning JSONL file for agent SFT (chat + tool calls) or DPO. |
| `scripts/topology_overhead.py` (ch08) | Coordination-overhead estimator for multiagent topologies (stdlib only, deterministic). |
| `scripts/agent_eval_report.py` (ch09) | Score agent runs against expected final states and apply release gates. |
| `scripts/drift_check.py` (ch10) | Compare a baseline and a current sample for distribution shift (PSI, KS, KL). |
| `scripts/trace_summary.py` (ch10) | Summarize agent spans exported as JSON lines (OTel-like) for monitoring review. |
| `scripts/ab_test_analyzer.py` (ch11) | Two-proportion A/B test analyzer and sample-size planner for agent experiments. |
| `scripts/bandit_allocator.py` (ch11) | Beta-Bernoulli Thompson-sampling allocator for adaptive agent experiments. |
| `scripts/escalation_tuner.py` (ch11) | Tune human-in-the-loop escalation thresholds from historical agent decisions. |
| `scripts/audit_tool_manifest.py` (ch12) | Static audit of an agent tool manifest for risky, under-guarded permissions. |
| `scripts/check_agent_kpis.py` (ch12) | Check an agent metrics snapshot against default alert thresholds. |

<!-- END GENERATED -->

## Provenance

Original synthesis for agent use; it does not reproduce the book's text, code, tables or figures. `references/source-maps.md` maps every chapter section to the file that covers it. This folder is regenerated from the chapter skills by `tools/build_bundles.py`.
