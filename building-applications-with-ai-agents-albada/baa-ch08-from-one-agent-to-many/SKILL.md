---
name: baa-ch08-from-one-agent-to-many
description: Guidance for deciding when to move from one agent to many, how to split responsibilities, which coordination pattern to use (democratic, manager, hierarchical, swarm, actor-critic, automated design/ADAS), and which communication, execution and state infrastructure fits (A2A, Kafka/Redis/NATS, Ray/Orleans/Akka, Temporal/Airflow). Based on Chapter 8 of Michael Albada's "Building Applications with AI Agents". Use when an agent has too many tools, when designing a supervisor or multiagent topology, when adding an agent, or when choosing brokers, actors, workflow engines or persistence for agents.
---

# From One Agent to Many (Albada, Chapter 8)

Purpose: help an engineer decide whether a system needs more than one agent, how to decompose it, how agents should coordinate, and what plumbing (transport, execution model, workflow durability, storage) carries them from prototype to production. The chapter's stance is software-architecture common sense applied to agents: start simple, split only when evidence demands it, and treat every added agent as a cost that must earn its place.

## Decision rules (apply without opening references)

1. **Default to a single agent.** It is simpler, cheaper and faster; prefer it for moderate tasks, small toolsets, stable environments and latency-critical paths.
2. **The trigger to split is tool-selection degradation**, not ambition. When accuracy falls as tools and duties grow, first climb the ladder: sharpen tool descriptions, then group tools hierarchically, then retrieve tools semantically per request. Split into agents only if those fail.
3. **Split by cohesive responsibility** (each specialist gets a narrow prompt and tool subset; shared output tools are fine), and validate the router's output with a retry or escalation fallback instead of silently ending.
4. **Six-question gate before adding any agent:** clear subtask boundary (decomposition), distinct capability (specialization), no existing agent could absorb it (parsimony), defined inputs/outputs/conflict rules (coordination), no new single point of failure or adds redundancy (robustness), measured gain exceeds cost (efficiency). Parsimony carries the most weight.
5. **Pick coordination by constraints:**
   - Manager: few agents, clear task types, latency matters. Watch the hub as failure point and bottleneck.
   - Hierarchical: many agents or several domains; spreads load, adds propagation delay; keep depth minimal and add an urgent bypass.
   - Democratic: no agent may be a failure point and fairness or pooled judgment matters; accept heavy messaging and slow decisions.
   - Swarm: hundreds of simple agents, decentralized and distributed problems, robustness over precision; weak on predictability, observability and efficiency.
6. **Add an actor-critic loop where quality is the problem** and judging is easier than generating: needs a clear rubric, affordable extra calls, and a fuzzy or generative task. Always cap rounds and pass critic feedback back.
7. **ADAS / Meta Agent Search is an offline design-search tool**: archive-conditioned generation, code-defined agents, reflection, validation scoring. Sandbox generated code and keep a held-out test set.
8. **Escalate communication only when needed:** in-process calls, then a broker (Redis Streams for quick low latency, Kafka for durable replayable logs, NATS for real-time and edge), then actors (Ray/Orleans/Akka, worthwhile beyond roughly 10 to 20 agents or tight latency), then a durable workflow engine (Temporal) for long, failure-prone, multistep or human-in-the-loop flows. Airflow is for scheduled batch, not real-time.
9. **A2A is promising but immature:** use it at team or vendor boundaries, and supply your own authorization, rate limiting, schema validation and trust checks.
10. **Match persistence to memory type:** episodic in memory, semantic in durable indexed (vector) storage, workflow progress in checkpointing engines; artifacts in object storage with an index. Workflow-native state for tight SLAs and cross-agent dependencies; explicit databases for modular or research systems needing control.

## Default workflow

1. Build and evaluate a single agent; record tool-selection accuracy, latency and cost.
2. If accuracy degrades with tools, apply the scale-up ladder and re-measure.
3. If still short, draft a decomposition by responsibility and run each candidate agent through the six-question gate.
4. Choose a coordination structure (rule 5); add actor-critic only on quality-limited nodes.
5. Estimate overhead with the script before committing; compare against the latency budget.
6. Choose transport, execution and durability layers (rules 8 and 9) and persistence (rule 10).
7. Harden: idempotent handlers, timeouts, retries, dead letters, session isolation, fallback routing; re-run evals against the single-agent baseline.

## References

- [references/agent-count-and-decomposition.md](references/agent-count-and-decomposition.md): read when deciding single vs multiagent, splitting an overloaded agent, considering a swarm, or justifying a new agent (includes a worked decomposition and the six-principle checklist).
- [references/coordination-strategies.md](references/coordination-strategies.md): read when choosing democratic, manager or hierarchical structure, designing an actor-critic loop, or evaluating ADAS / Meta Agent Search (loop steps and reported benchmark results).
- [references/communication-infrastructure.md](references/communication-infrastructure.md): read when moving beyond in-process calls: A2A cards and handshakes, broker patterns and hardening, Ray/Orleans/Akka and per-session actors, Temporal/Airflow/Dagger, plus a selection table.
- [references/state-and-persistence.md](references/state-and-persistence.md): read when deciding where agent memory, shared task state and artifacts live, and how to survive mid-workflow failures.
- [references/source-map.md](references/source-map.md): read to locate which file covers a given chapter section.

## Scripts

- Run `python3 scripts/topology_overhead.py compare --agents 12 --fanout 2 --parallel` to compute per-task model calls, inter-agent messages, critical-path latency, cost and busiest-agent link count for single, manager, hierarchical, democratic and swarm topologies.
- Run `python3 scripts/topology_overhead.py sweep --agents-list 3,5,10,20` to see how messages and cost grow with agent count per topology.
- Run `python3 scripts/topology_overhead.py actor-critic --p 0.6 --max-rounds 4` to compute expected rounds, calls, latency, cost multiplier and acceptance probability of an actor-critic loop.
- Tune `--latency`, `--cost`, `--msg-latency`, `--branching`, `--rounds`, `--neighbors` to your stack. Outputs are relative estimates; democratic and swarm latency are lower bounds.
