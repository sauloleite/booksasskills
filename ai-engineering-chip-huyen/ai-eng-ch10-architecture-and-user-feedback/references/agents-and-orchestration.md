# Agent Patterns, Write Actions, and Pipeline Orchestration

## Contents
- From sequential to agentic flow
- Write actions: gating checklist
- Complexity budget and modularity
- What an orchestrator does
- Build without one first; evaluating candidates
- Latency: parallelize independent steps
- Worked example: research agent rollout
- Pitfalls

## From sequential to agentic flow

Through Step 4, each query runs in a straight line: route, retrieve, generate, score, return. Step 5 lets output flow back into context construction, enabling:
- **Loops**: the system judges the task incomplete, retrieves more, and passes draft plus new context to the same or another model.
- **Parallel execution** of independent sub-tasks.
- **Conditional branching** on router or scorer decisions.

## Write actions: gating checklist

Read actions gather information; write actions change the world (send email, place an order, start a bank transfer). They raise capability and risk sharply, since a mistake or a successful injection now has side effects. Before enabling one:
1. **Need**: could the agent draft the action for a human to execute instead?
2. **Least privilege**: credentials scoped to one action and resource.
3. **Reversibility**: human approval for irreversible or high-value actions (money, external messages, deletion).
4. **Caps**: rate and value limits per session and user.
5. **Audit**: log every write with request ID, inputs, and result.
6. **Injection exposure**: the more untrusted content (web pages, tool output) the planner reads, the tighter its write permissions.

Rollout order: read-only tools, then loops, then writes behind approval, then selective auto-approval for low-risk writes once logs show reliability.

## Complexity budget and modularity

Each component can make the system more capable, safer, or faster, and each adds failure modes and places to debug. Before adding one, write down the weakness it fixes and the failures it introduces, and confirm tracing covers it.

Keep components separate for maintainability but expect overlap: guardrails in the inference service, gateway, or a standalone service; caching in the gateway or app; scorers with models or with output guardrails. Many AI problems are system problems: a failure may be fixable in several components or need several to cooperate, so debug with the whole pipeline in view.

## What an orchestrator does

An AI pipeline orchestrator defines how models, data sources, and tools combine end to end and moves data between them, in two phases:
- **Component definition**: register models (easier behind a gateway), retrieval sources, tools, and evaluation or monitoring hooks.
- **Chaining**: function composition of those components into the steps from raw query to finished task. Typical chain: normalize the query, retrieve with it, assemble the prompt, generate, evaluate, then return the answer or route to a human.

A good orchestrator validates that each step's output matches the next step's expected input and alerts on broken flow (component failure, data mismatch). It is a different category from batch workflow schedulers such as Airflow or Metaflow. Examples: LangChain, LlamaIndex, Haystack, Flowise, Langflow; many RAG and agent frameworks double as orchestrators.

## Build without one first; evaluating candidates

Resist starting inside a framework. Every external tool adds complexity, and an orchestrator can hide exactly what you need to debug (the real prompt, the calls made). Revisit once hand-written glue becomes the bottleneck.

| Criterion | Questions |
|---|---|
| Integration and extensibility | Supports your current and planned models, stores, tools (for example a specific open model family)? Since nothing supports everything, how hard is adding a missing one? |
| Complex pipelines | Branching, parallel steps, conditional logic, error handling? |
| Ease of use, performance, scale | Clear APIs, good docs, active community? No hidden API calls or added latency? Scales with apps, developers, and traffic? |

Red flags: undocumented extra model calls, prompt templates you cannot inspect, forced coupling to one vendor's store or gateway, no access to intermediate outputs for tracing.

## Latency: parallelize independent steps

On tight latency budgets run independent steps concurrently. Classic pair: routing and PII removal, which do not depend on each other; join before generation. Others: retrievals from several sources, input moderation with intent classification, and double-sampling as a retry strategy (two generations at once, keep the better).

## Worked example: research agent rollout

Goal: an agent researches a company and emails a briefing.
1. V1 without a framework: a Python loop calling the gateway, a search tool, and a fetch tool, every step logged under one request ID.
2. Add a small next-action router (search, fetch, finish) with a cap of eight iterations.
3. Add a reflection loop: a scorer checks required sections; if missing, one more retrieval round.
4. Sending email is a write action: the agent drafts, a human sends. After a month of clean audit logs, auto-send is allowed for internal recipients only.
5. Only when three agents share components does the team evaluate an orchestrator against the table above, confirming it exposes every intermediate prompt.

## Pitfalls

- Write permissions granted before read-only behavior is reliable and traced.
- Loops with no iteration or spend cap.
- Starting inside a heavy framework and losing sight of real prompts and calls.
- Confusing an AI pipeline orchestrator with a batch workflow scheduler.
- Serial execution of independent steps on a latency-critical path.
