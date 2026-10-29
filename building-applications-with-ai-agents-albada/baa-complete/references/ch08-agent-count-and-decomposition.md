# Deciding How Many Agents, and How to Split Them

## Contents
1. Default stance: one agent first
2. Saturation signals for a single agent
3. The scale-up ladder (exhaust it before splitting)
4. What a split buys you
5. What a split costs you
6. Worked example: splitting an overloaded claims agent
7. Swarms: many simple agents, no boss
8. The six principles for adding an agent (checklist)
9. Pitfalls
10. Glossary

## 1. Default stance: one agent first

The chapter's baseline is blunt: build the simplest thing, then add structure only when measurements show it helps. A single agent that loops over model call, tool call, model call (with a cap on tool iterations) is the right starting point when:

- the task is of moderate difficulty and the toolset is small;
- the environment is not highly dynamic;
- user-facing latency matters (every extra agent hop adds at least one more model round trip);
- you still need to validate that the core capability works at all.

Its advantages are easy implementation and debugging, less compute per request, and faster responses. A one-node graph with shared state (task metadata plus message history) carries no inter-agent communication at all, which is why it suits dashboards and real-time alerting.

## 2. Saturation signals for a single agent

The dominant failure mode is tool-selection degradation: as the number of tools and responsibilities grows, the system prompt has to describe every option and the model starts picking the wrong tool, chaining the wrong ones, or skipping a needed one. The chapter's illustration is a logistics agent carrying sixteen tools in one prompt. Watch for:

- tool-selection accuracy falling on your eval set as tools are added;
- the system prompt becoming a long catalog of loosely related duties;
- prompt instructions for one domain (for example compliance) contradicting another (for example speed of delivery);
- one subdomain needing a different model, temperature, or guardrail than the rest.

## 3. The scale-up ladder (exhaust it before splitting)

Apply in order and re-measure after each rung:

1. Tighten tool names, descriptions and argument schemas so they are mutually distinct.
2. Group tools hierarchically: expose a few coarse capability groups, then the concrete tools inside the chosen group.
3. Select tools semantically: embed tool descriptions, retrieve the top-k relevant ones per request, and bind only those (the book covers this under orchestration in its Chapter 5).
4. Only if accuracy is still unacceptable, decompose tools across distinct agents with clear responsibilities, accepting the coordination overhead.

## 4. What a split buys you

- **Specialization.** Each agent gets a narrow prompt and a short tool list, so selection errors drop and each piece can be tested, validated and reused on its own (the same reasons we avoid a single-file codebase or a monolithic backend).
- **Smaller context per call.** Specialists see only their own instructions and tools.
- **Parallelism.** Independent subtasks (for example one specialist re-planning deliveries while another audits a supplier) can run concurrently if the graph fans out.
- **Adaptability.** A router can reassign work as conditions change instead of following a fixed path; roles can be reallocated as new information arrives.
- **Fault isolation.** A specialist whose upstream API is down need not stall the others.

## 5. What a split costs you

- **Coordination complexity.** Agents need explicit communication and synchronization rules.
- **Communication overhead.** Staying aligned and avoiding duplicate work requires message exchange, which adds latency, tokens and infrastructure, and grows with scale.
- **Conflicts.** Agents with overlapping goals or unclear priorities can contradict each other, so you need conflict-resolution and resource-allocation rules.
- **Latency.** At minimum one extra model call (the router) per request, more if results must be merged.

Rule of thumb from the chapter: in complex environments the reliability and scalability gains usually outweigh the added latency; in simple, latency-critical ones they usually do not.

## 6. Worked example: splitting an overloaded claims agent

An insurance claims assistant has 14 tools: open_claim, fetch_policy, check_coverage, request_documents, ocr_document, detect_fraud_signals, estimate_damage, schedule_adjuster, compute_payout, issue_payment, freeze_payment, notify_customer, escalate_to_human, log_audit_event.

Evaluation shows 81% correct tool selection; errors cluster where fraud checks and payment tools are confused.

Step 1 (ladder). Rewriting descriptions lifts accuracy to 86%. Semantic top-5 tool retrieval lifts it to 89%. Target is 95%, so proceed.

Step 2 (decompose by cohesive responsibility, not by tool count):
- Intake specialist: open_claim, fetch_policy, request_documents, ocr_document.
- Assessment specialist: check_coverage, detect_fraud_signals, estimate_damage, schedule_adjuster.
- Settlement specialist: compute_payout, issue_payment, freeze_payment.
- Shared by all: notify_customer, escalate_to_human, log_audit_event (a uniform outbound channel avoids duplicating reporting logic).

Step 3 (coordination). A supervisor reads the request and the claim record and picks one specialist. Each specialist keeps a short prompt focused on its duty and the decision criteria that matter there (assessment weighs fraud risk; settlement weighs correctness and reversibility).

Step 4 (parsimony check). Could settlement live inside assessment? No: payment needs a stricter guardrail and a different human-approval rule, which justifies a separate agent. Could intake and assessment merge? Possibly; keep them apart only if evals show a gain.

A robust router validates the supervisor's choice instead of trusting free text:

```python
ALLOWED = {"intake", "assessment", "settlement"}

def route(supervisor_reply: str, retries_left: int = 1) -> str:
    choice = supervisor_reply.strip().lower()
    if choice in ALLOWED:
        return choice
    if retries_left > 0:
        return "reask_supervisor"      # re-prompt with the allowed list
    return "escalate_to_human"         # never silently end the run
```

The design point: an unrecognized routing label should trigger a retry or an escalation, not a silent termination of the graph.

## 7. Swarms: many simple agents, no boss

A swarm is a large population of individually simple agents, each following local rules with no global view, whose useful behavior emerges from repeated local interactions (broadcasting small updates, reacting to neighbors, following shared signals). Inspiration: bird flocks, fish schools, ant colonies.

Choose a swarm when:
- central control is impractical or undesirable;
- the problem is naturally distributed: broad data discovery, research across many sources, monitoring, distributed search, consensus formation;
- robustness and flexibility matter more than precision;
- you may need hundreds or thousands of agents (loose coupling keeps coordination overhead low).

Strengths: scale, no single point of failure (losing agents degrades gracefully), real-time adaptation, natural fit for distributed problem solving. Typical domains: edge computing, sensor networks, real-time collaborative systems.

Avoid or contain a swarm when you need predictable outputs, easy observability, or tight cost efficiency; these are its weak spots. If you adopt one, add aggregate metrics (coverage, convergence, duplicate work rate) because per-agent traces will not explain global behavior.

## 8. The six principles for adding an agent (checklist)

Ask every question before adding an agent; one "no" is a reason to pause.

| Principle | Question to answer yes to |
|---|---|
| Task decomposition | Does the new agent own a clearly bounded subtask with little overlap with existing ones? |
| Specialization | Does the role match a distinct capability (tools, prompt, model, guardrail) that the others lack? |
| Parsimony | Have you ruled out giving this duty to an existing agent or improving that agent instead? |
| Coordination | Is it clear who sends it work, who consumes its output, and how conflicts with peers are resolved? |
| Robustness | Does it improve fault tolerance (for example as a backup or redundant path) or at least not create a new single point of failure? |
| Efficiency | Does the measured gain exceed the added compute, latency and coordination cost? |

Parsimony deserves the most weight: every agent adds messages, coordination surface, resources and maintenance, and agent sprawl creates bottlenecks. Redundancy (agents that can take over when another fails) is the main exception where adding an agent is justified without new functionality, typically in high-stakes settings.

## 9. Pitfalls

- Jumping to multiagent before trying tool grouping or semantic tool retrieval.
- Splitting by tool count rather than by cohesive responsibility, which creates chatty agents that constantly need each other.
- Overlapping responsibilities with no tie-break rule.
- A router that ends the run on an unexpected label.
- Ignoring the latency budget: a supervisor plus specialist plus synthesizer is at least three sequential model calls.
- Claiming parallelism without actually fanning out edges to concurrent calls.

## 10. Glossary

- **Specialist**: an agent bound to a narrow tool subset and a focused prompt.
- **Supervisor / router**: an agent whose only job is choosing which specialist handles a request.
- **Emergent behavior**: system-level competence not programmed into any single agent, arising from local interactions.
- **Parsimony**: adding the minimum number of agents needed to reach the target performance.
