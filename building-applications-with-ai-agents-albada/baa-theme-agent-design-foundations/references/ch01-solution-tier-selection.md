# Solution Tier Selection: Code, Workflow, RAG or Agent

## Contents
- What counts as an agent
- The four selection factors
- The tier ladder with entry and exit criteria
- What you give up at each step up
- Five gating questions
- Asynchronous operation as a reason to choose agents
- Worked examples
- Pitfalls
- Decision record template

## What counts as an agent

Agency is a spectrum, not a label. Many products marketed as agents run fixed scripts or tightly scripted flows. The test to apply: does the system make real decisions at run time (choosing which action, tool or path to take based on context), or does it replay a path a developer enumerated in advance? Only the former is an agent in Albada's sense.

Two terms to keep distinct:
- **Agent**: the decision-making component, usually a foundation model that emits structured tool calls (function name plus arguments) which an orchestrator executes.
- **Agentic system**: everything that lets the agent run reliably: tools, memory, the model, orchestration logic and the surrounding infrastructure. Most engineering effort lives here, not in the model.

What made modern agents practical is that models now emit structured function signatures and parameter choices, not just prose. Protocols for remote tools (MCP) and agent-to-agent collaboration (A2A) extend reach further, which raises the stakes for measurement and alignment.

## The four selection factors

Score the problem on each before picking an architecture:
1. **Input variability**: fixed schema, a few known formats, free text within a domain, or open-ended and novel.
2. **Reasoning complexity**: a transformation, a known branch tree, lookup plus synthesis, or multistep planning that reacts to intermediate results.
3. **Performance and compliance constraints**: latency budget, determinism, auditability and certification requirements.
4. **Maintenance burden**: who keeps it working as inputs and requirements change, and at what cost.

## The tier ladder

Climb only as far as the problem forces you. Each step up adds capability and adds cost, latency and governance work.

**Tier 0: Plain code (no model at all)**
- Choose when inputs are fully predictable, every output can be specified ahead of time, the problem domain is static, latency must be in milliseconds, or a regulator demands deterministic and auditable logic (medical devices, aviation, some finance).
- Any single one of these conditions usually settles it in favor of code.
- Benefits: cheapest, fastest, easiest to test.

**Tier 1: Deterministic or semiautomated workflow**
- Choose when the logic fits a finite set of steps and branches, and you know in advance where humans must approve or where errors need special handling.
- Workflow engines (Airflow, AWS Step Functions, or disciplined scripts) give explicit control over retries with exponential backoff, approval pauses and failure paths.
- Rule: if you can list every decision branch up front and need tight, auditable control of each one, use a workflow. It scales better than a pile of ad hoc scripts and avoids agent cost.

**Tier 2: Traditional chatbot or RAG**
- Choose when the main job is answering questions over a corpus (manuals, wikis, legal archives) with little need for external API calls or orchestration of decisions.
- RAG surfaces information; it does not decide on follow-up actions such as opening a ticket or booking a callback.
- Ongoing cost is mostly keeping embeddings fresh and refining prompts, lower than agents. The price: no multistep planning and no learning loop.

**Tier 3: Autonomous agent**
- Choose when inputs are unstructured, novel or highly variable AND the task needs dynamic multistep planning, parallel subtask orchestration, or improvement from feedback.
- Justification rule: the extra compute and maintenance of a foundation model is only warranted when you need contextual reasoning, parallel orchestration or ongoing self-improvement that would make code, workflows or chatbots too brittle or too costly to maintain.

## What you give up at each step up

- Code to workflow: you trade some speed and simplicity for explicit branch handling, retries and approval gates. Audit stays easy because each branch leaves a trail.
- Workflow to RAG: you gain tolerance for free-text questions but accept probabilistic answers and a corpus to keep fresh.
- RAG to agent: you gain the ability to plan, act and adapt, and you pay with the highest latency, opaque decisions that need extra tracing and evaluation tooling to audit, and the largest compute and governance bill.
- Moving down is equally valid: if a pilot agent mostly follows the same few paths, freeze those paths into a workflow.

## Five gating questions

Ask in this order; a "no" to the first three usually means you do not need an agent.
1. Are the inputs unstructured or unpredictable?
2. Does the work need multistep planning that adapts to what earlier steps returned?
3. Is surfacing documents insufficient, so the system must itself decide and act?
4. Should the system get better over time with little human intervention?
5. Can the product tolerate model latency and the long-term operating burden?

If 1 to 3 are "yes" but 5 is "no", redesign: shrink the agent's scope, precompute asynchronously, or route part of the traffic to a cheaper tier.

## Asynchronous operation as a reason to choose agents

Classic software runs step by step and blocks on each action, which wastes time when waiting on external inputs or large data volumes. Agents can run many tasks concurrently, absorb new information mid-flight and reprioritize. Design implications:
- Prefer "work arrives prepared" patterns: the agent acts before the human opens the item. Examples of the pattern: a drafted reply attached to an incoming email, payment fields filled in on an invoice, a ticket that already carries a candidate patch and tests, a support case with a proposed answer and next action, a security alert already enriched with threat intel.
- The human role shifts from doing the task to supervising it: reviewing, approving, handling exceptions and making strategic calls. Design review queues, approval UX and escalation paths accordingly; this is where the value lands.
- Fan-out is a strong agent signal: a SOC triage that queries threat feeds, scans telemetry and detonates a sample in a sandbox at once benefits from concurrency that a one-step-at-a-time workflow lacks.

## Worked examples

- **Fixed-format log parsing** (every line is a timestamp then a message): a regex parser in a few lines. Tier 0.
- **Sensor loop on embedded hardware with a millisecond deadline**: no time for a model call. Tier 0.
- **Invoices from a handful of vendors in CSV, JSON or PDF**: route by format to a parser, reconcile fields, stop for human review on mismatch. Tier 1.
- **Employees asking how to reset VPN credentials**: retrieve the current runbook and summarize steps. Tier 2.
- **Free-form support email ranging from hardware safety hazards to disputed charges**: intent parsing, entity extraction, knowledge lookup, drafting and escalation without a pre-enumerated branch list. Tier 3.
- **Supply chain replanning from live inventory, supplier lead times and forecasts**: a workflow would need endless manual updates for new exceptions. Tier 3.

## Pitfalls

- Calling a scripted flow an "agent" and then budgeting or governing it as one (or the reverse).
- Reaching for an agent where a workflow fits, producing an overengineered system that is hard to maintain.
- Using a workflow where inputs are wildly variable; it breaks on each new exception.
- Expecting a RAG bot to take actions; it needs an orchestration layer to do so.
- Underestimating agent operating cost: compute plus the engineering to monitor, tune and govern.
- Ignoring explainability: agents need added tracing and evaluation tooling to reach the audit level a workflow gives for free.

## Decision record template

```
Problem:
Input variability (fixed / few formats / free text / novel):
Reasoning (transform / known branches / lookup+synthesis / adaptive multistep):
Constraints (latency budget, determinism, audit, certification):
Gating answers Q1..Q5:
Chosen tier and why the tier below is insufficient:
Parts routed to cheaper tiers:
Human checkpoints and escalation paths:
Review trigger (what change would move us up or down a tier):
```

See also: principles-and-organization.md for how to build the chosen agent so it stays maintainable.
