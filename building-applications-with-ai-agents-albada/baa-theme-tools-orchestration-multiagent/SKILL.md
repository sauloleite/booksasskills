---
name: baa-theme-tools-orchestration-multiagent
description: Theme skill on how agents act and coordinate, from Michael Albada's "Building Applications with AI Agents" (chapters 4, 5 and 8). Use when defining or auditing tools (local, API, MCP, stateful), choosing tool selection and agent archetypes (ReAct, planner-executor, reflection), designing chains and graphs, doing context engineering, or deciding whether and how to split into multiple agents and wire their communication and state.
---

# Tools, orchestration and multiagent systems (Building Applications with AI Agents, ch. 4, 5, 8)

How an agent changes the world and how work is routed inside one agent or across many. The chapters form one escalation path: better tools, then better orchestration, then more agents only if the first two run out.

## Cross-chapter rules

1. **Tool definitions are interfaces.** Narrow names, descriptions that clearly separate tools, strict schemas and enums. Overlapping descriptions are the main cause of wrong picks; lint them with `scripts/lint_tool_definitions.py`.
2. **Least power for stateful tools.** Narrow single-purpose operations instead of free-form SQL or shell, no write tools for read-only agents, minimum-privilege credentials, prepared statements and logging when free-form access is unavoidable.
3. **Wrap every model turn.** Validate arguments against the schema, retry with backoff only what failed, fall back (backup model, cache, ask the user, safe default) and log everything.
4. **Match the archetype to the task.** Reflex, ReAct, planner-executor, query decomposition, reflection and deep research cost progressively more; use reflection where mistakes are irreversible.
5. **Selection strategy follows catalog size.** Put all tools in the prompt for small catalogs, retrieve the top candidates semantically for most cases, and group hierarchically for large catalogs of similar tools.
6. **Climb the topology ladder slowly.** Single call, parallel fan-out, chain, graph. Cap chain length and graph depth and branching, unit-test routers, and check graphs for cycles and dead ends (`scripts/topology_check.py`).
7. **Exhaust single-agent fixes before splitting.** Improve descriptions, group tools, retrieve tools semantically; split into agents only when tool selection still degrades. Every extra agent adds at least one model round trip.
8. **Choose coordination by the robustness vs speed trade-off.** Manager (fast, single point of failure), hierarchical (scales, adds delay), democratic (robust, message-heavy), swarm (emergent, hard to observe). Estimate overhead with `scripts/topology_overhead.py`. Add actor-critic when judging is easier than producing.
9. **Escalate infrastructure only as needed.** In-process calls, then a broker (Kafka, Redis Streams, NATS), then actor frameworks for larger fleets, then durable workflow engines. Persist state by memory type and keep workflow progress checkpointed.

## Default workflow

1. Define and lint the tool set (ch04).
2. Pick archetype, selection strategy and topology; engineer the context for each call (ch05).
3. Evaluate tool selection (`scripts/tool_selection_eval.py`) and fix descriptions first.
4. Only if selection still fails at scale, decompose into agents, pick a coordination pattern and communication layer, and plan state (ch08).

<!-- BEGIN GENERATED: run tools/build_bundles.py to refresh -->

## References by chapter

Each link is one level deep; read only the files whose description matches the task.

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

### CH08: From One Agent to Many

- [ch08-agent-count-and-decomposition.md](references/ch08-agent-count-and-decomposition.md): read when deciding single vs multiagent, splitting an overloaded agent, considering a swarm, or justifying a new agent (includes a worked decomposition and the six-principle checklist).
- [ch08-communication-infrastructure.md](references/ch08-communication-infrastructure.md): read when moving beyond in-process calls: A2A cards and handshakes, broker patterns and hardening, Ray/Orleans/Akka and per-session actors, Temporal/Airflow/Dagger, plus a selection table.
- [ch08-coordination-strategies.md](references/ch08-coordination-strategies.md): read when choosing democratic, manager or hierarchical structure, designing an actor-critic loop, or evaluating ADAS / Meta Agent Search (loop steps and reported benchmark results).
- [ch08-state-and-persistence.md](references/ch08-state-and-persistence.md): read when deciding where agent memory, shared task state and artifacts live, and how to survive mid-workflow failures.

Merged section maps: [source-maps.md](references/source-maps.md).

## Scripts

Python 3 standard library only; run any script with `--help` for its arguments.

| Script | Purpose |
|---|---|
| `scripts/lint_tool_definitions.py` (ch04) | Lint a set of agent tool definitions for selection and safety problems. |
| `scripts/tool_selection_eval.py` (ch05) | Evaluate agent tool selection against labeled expectations. |
| `scripts/topology_check.py` (ch05) | Validate the structure of an agent orchestration graph before building it. |
| `scripts/topology_overhead.py` (ch08) | Coordination-overhead estimator for multiagent topologies (stdlib only, deterministic). |

<!-- END GENERATED -->
