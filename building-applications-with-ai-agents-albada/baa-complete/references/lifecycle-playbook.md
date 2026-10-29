# Lifecycle playbook and cross-chapter decisions (Building Applications with AI Agents)

Whole-book synthesis: a stage-by-stage playbook, a symptom-to-fix map that crosses chapters, and a universal checklist. Chapter tags such as (ch05) point to the `chNN-*` reference files in this folder.

## Contents
- Stage-by-stage playbook
- Symptom-to-fix map
- The escalation ladders
- Universal checklist
- Book-wide pitfalls

## Stage-by-stage playbook

### 1. Decide and scope (ch01, ch02)
- Ask whether inputs are unpredictable, whether plans must adapt to intermediate results, whether the system must act, whether it should improve itself, and whether model latency and upkeep are acceptable. Mostly "no" means code or a workflow.
- Pick a first slice that people already handle by rule, with structured outputs and a cheap automatic check.
- Start with a strong general model, keep it swappable, and plan to route easy traffic to cheaper models later.
- Choose a framework by stage: fast prototyping tools early, controllable graph or multi-agent frameworks for production; no framework is a valid choice.

### 2. Design the experience (ch03)
- Choose modality by context of use; let journeys move across modalities on shared state.
- Decide synchronous or asynchronous for each flow and give async work status, progress and a summary.
- Expose capabilities, offer autonomy levels the user controls, ask targeted clarifying questions, and design graceful failure with preserved progress.

### 3. Act: tools and orchestration (ch04, ch05)
- Define tools with distinct descriptions and strict schemas; restrict stateful tools; wrap calls with validation, retries, fallbacks and logs.
- Choose the archetype by task: reactive loops for simple tasks, planner-executor for longer plans, reflection where errors are costly, deep research for open investigation.
- Choose selection by catalog size and topology by need, capping depth and branching. Rebuild a lean, structured context for every call.

### 4. Remember and learn (ch06, ch07)
- Separate knowledge from memory, budget the window, and escalate retrieval only after evals show failure.
- Add nonparametric learning with a per-attempt quality signal; fine-tune only with aligned need, data and operations, matching the method to the available signal.

### 5. Scale out (ch08)
- Before adding agents, improve descriptions, group tools and retrieve tools semantically.
- If splitting is justified, apply the six principles (decomposition, specialization, parsimony, coordination, robustness, efficiency), choose a coordination pattern, and add infrastructure in steps.
- Persist state by type and checkpoint workflow progress.

### 6. Validate (ch09)
- Build eval cases from experts, production logs and reviewed synthetic variants; stress them adversarially.
- Test components in isolation (tools, memory, learning) and the whole system on success, consistency, coherence, robustness and hallucination.
- Set gates before release and block automatically on failure.

### 7. Operate (ch10)
- Instrument each step as a span, monitor four layers, alert on behavior as well as infrastructure.
- Triage by reproduction and drift checks; release through shadow and canary with dashboards split by version.
- Assign metric owners across product, engineering and data roles.

### 8. Improve (ch11)
- Automate the first pass of clustering and root cause, keep humans for approval and priority.
- Fix prompts and tools first, prioritize a deduplicated backlog, validate through the rollout ladder, and promote proven in-context fixes into durable form.

### 9. Protect and govern (ch12, ch13)
- Threat model in layers, defend in depth, red team continuously, protect data end to end, and contain failures.
- Expand autonomy stage by stage with entry criteria, govern by scope, and make escalation, accountability and compliance explicit and automated.

## Symptom-to-fix map

| Symptom | Likely cause | First move | Then |
|---|---|---|---|
| Agent picks the wrong tool | Overlapping descriptions, large catalog | Rewrite and lint descriptions (ch04) | Semantic or hierarchical selection (ch05), then split agents (ch08) |
| Right tool, wrong arguments | Loose schema, missing context | Strict schema, validation and repair loop (ch04, ch05) | Inject needed context; fine-tune function calling (ch07) |
| Forgets earlier sessions or drifts on long tasks | No durable memory, poor budget | Experience memory with a reserved slice (ch06) | Experiential rules or GraphRAG (ch06, ch07) |
| Repeats the same mistakes | No learning signal | Reflexion on failures (ch07) | Rule list, then fine-tuning on stable patterns (ch07) |
| Looping or runaway cost | Unbounded topology | Depth, branching and retry caps (ch05) | Simpler archetype; alert on retry loops (ch10) |
| Multiagent system slow or expensive | Too many hops | Measure overhead (ch08) | Merge agents, change coordination pattern (ch08) |
| Quality dropped with no code change | Input or model drift | Drift checks and triage (ch10) | Regression tests and controlled rollout of fixes (ch11) |
| Users rephrase or abandon | UX or capability gap | Clarification and discoverability (ch03) | Feedback pipeline into prioritized fixes (ch11) |
| Injected instructions or data leak | Missing layered defenses | Separate untrusted content, least privilege (ch12) | Red teaming and data protection controls (ch12) |
| Stakeholders do not trust the agent | Opaque or overreaching autonomy | Visible confidence and easy override (ch03, ch13) | Progressive delegation with clear escalation (ch13) |

## The escalation ladders

- **Solution tier:** code, workflow, chatbot or RAG, agent, multiagent.
- **Tool topology:** single call, parallel fan-out, chain, graph.
- **Tool selection:** all in prompt, semantic retrieval, hierarchical.
- **Memory:** window and keyword, BM25, vectors, RAG, experience memory, GraphRAG, dynamic graphs.
- **Learning:** static examples, retrieved examples, Reflexion, experiential rules, fine-tuning.
- **Communication:** in-process, message broker, actor framework, durable workflow engine.
- **Release:** staging, shadow, A/B or bandit, canary or gradual ramp.
- **Autonomy:** executor, reviewer, collaborator, governor.

## Universal checklist

- [ ] The tier decision is documented and an agent is justified.
- [ ] First scope, success check and eval cases exist before building.
- [ ] Tools are linted, least-privileged and wrapped with validation, retries, fallbacks and logs.
- [ ] Archetype, selection strategy and topology are the simplest that pass evals; caps are set.
- [ ] Context budget is explicit; retrieval and learning loops were added on evidence.
- [ ] Any multiagent split has a written justification and an overhead estimate.
- [ ] Release gates are predefined and enforced automatically.
- [ ] Every step emits spans; alerts cover behavior, quality and user signals; drift thresholds are set.
- [ ] Failures flow into regression tests and a prioritized backlog; fixes ship through the rollout ladder.
- [ ] Threat model, permission audit, red-team schedule and data protection controls are in place.
- [ ] Autonomy levels, escalation thresholds, owners and compliance checks are explicit.

## Book-wide pitfalls

- Building an agent where a workflow would do, or splitting into many agents to fix a tool-description problem.
- Shipping on demos and judging quality by eye instead of automated, versioned evals.
- Granting broad tool power and trusting the model to restrain itself.
- Treating infrastructure health as agent health, and missing silent failures.
- Letting automated improvement proposals reach production without validation.
- Expanding autonomy faster than measured reliability, with no path back.
