# Communication Infrastructure: Local Calls, A2A, Brokers, Actors, Workflow Engines

## Contents
1. The escalation path
2. Local versus distributed communication
3. Agent-to-Agent (A2A) protocol
4. Message brokers and event buses
5. Actor frameworks: Ray, Orleans, Akka
6. Orchestration and workflow engines
7. Selection guide
8. Pitfalls

## 1. The escalation path

Communication choices trade development effort against latency, scalability, reliability and cost. There is no single right answer; move up a level only when the current one breaks:

1. In-process function calls or an in-memory router inside one container.
2. A message broker so agents run as independent processes or services.
3. An actor framework when agents need per-agent state, fine-grained distribution and automatic recovery.
4. A workflow engine on top when multistep processes must survive crashes, retries and long waits.
5. A2A when agents cross team, vendor or framework boundaries and must discover each other.

Levels 2 to 5 are not exclusive: a production system often combines a broker (transport), actors (execution and state) and a workflow engine (sequencing and durability). Treat communication design as a first-class architectural concern, because it shapes what each agent can perceive and how fast it can react.

## 2. Local versus distributed communication

Inside a single process, agents can share memory, call each other directly or pass messages through an in-memory queue; frameworks like AutoGen ship in-memory routers for this. That is efficient and fine for research and prototypes. Once agents live in separate services, containers or nodes, communication must become explicit, asynchronous and tolerant of failure (timeouts, retries, lost messages, partial results).

Signals you have outgrown local communication: you need to scale one specialist independently; a crash in one agent kills the whole request; you need to replay or audit interactions; agents are deployed by different teams.

## 3. Agent-to-Agent (A2A) protocol

A2A, introduced by Google, standardizes how heterogeneous agents find each other, agree to collaborate and exchange structured requests over HTTP-based transports without exposing their internals. The aspiration is to make calling another agent as routine as calling a microservice.

Key elements:
- **Agent Card**: a machine-readable JSON self-description containing identity, explicit capabilities (each with input and output schemas), endpoint, supported authentication methods (for example OAuth 2 or API keys) and optional metadata such as version and supported media.
- **Discovery**: cards are served at a well-known path (`/.well-known/agent.json`) and collected in a registry, centralized or distributed.
- **Handshake**: the caller fetches the peer's card and negotiates session terms such as protocol version, timeouts and payload size limits, checking that the required capability exists.
- **Transport**: the reference implementation is JSON-RPC 2.0 over HTTPS, which standardizes requests, results and errors (for example code -32601 for an unknown method). The design is transport-agnostic, so gRPC, WebSocket or other streaming transports are possible.

Status and risk: the protocol is young. Authentication plugs in, yet fine-grained permissions, throttling, establishing trust between strangers and resisting misuse all remain open problems. Expect vulnerabilities, gaps between implementations and spec changes.

Adoption checklist:
- Use A2A at organizational or vendor boundaries; inside one codebase plain function calls or a broker are cheaper.
- Verify card authenticity (signed cards or a trusted registry) before acting on advertised capabilities.
- Enforce your own authorization and per-peer rate limits; do not rely on the protocol for them.
- Validate every request and response against the declared schemas; treat peer output as untrusted input (it can carry prompt injection).
- Pin and check versions during the handshake; fail closed on mismatch.
- Log every cross-agent call with correlation IDs.

Minimal capability check before delegating:

```python
def can_delegate(card: dict, capability: str, min_version: str) -> bool:
    if capability not in card.get("capabilities", []):
        return False
    if card.get("version", "0") < min_version:   # use proper semver parsing in practice
        return False
    if "none" in card.get("auth_methods", []):
        return False                              # refuse unauthenticated peers in production
    return capability in card.get("schemas", {})
```

## 4. Message brokers and event buses

Direct point-to-point calls become brittle as agents multiply. A broker decouples producers from consumers: agents publish to and consume from shared topics or streams asynchronously. Gains: independent scaling of each specialist, replay of missed or failed messages, logging-based observability, and adding agents without rewiring a graph. Costs: eventual consistency, more complex error handling, and some added latency.

Options:
- **Apache Kafka**: high throughput, durable, partitioned topics for parallelism, consumer groups for coordination. Best when every interaction should be kept and replayable (log-centric architecture).
- **Redis Streams**: memory-based and very fast, simple to deploy, weaker durability. Good for prototypes and low-latency decoupling.
- **RabbitMQ**: lightweight queueing for simpler, lower-throughput setups with easy deployment.
- **NATS**: lightweight, cloud-native, low latency at high throughput; supports publish/subscribe and request/reply, and with JetStream adds durable streams and replay. Suits real-time coordination in microservice and edge deployments.

Supervisor/specialist over a broker:
1. The supervisor decides the target specialist and publishes a task message carrying a unique task ID, the target, task metadata and serialized history.
2. Each specialist runs in its own process, consumes tasks meant for it, executes its normal logic and publishes a result tagged with the same task ID to a response stream.
3. The caller waits on the response stream for its task ID with a timeout.

Hardening beyond the basic pattern:
- Give each specialist its own stream or use consumer groups so workers do not read and discard everyone else's traffic, and so multiple replicas share load.
- Acknowledge only after successful processing; route repeated failures to a dead-letter stream.
- Make handlers idempotent (keyed by task ID) because redelivery happens.
- Version the message schema and serialize message history explicitly.
- Always set a response timeout and define what the user sees when it fires.

## 5. Actor frameworks: Ray, Orleans, Akka

Brokers move data; actor frameworks unify messaging with computation. Each actor owns its state and behavior and handles its messages one at a time, which removes race conditions and shared-state bugs. Compare this with the common first deployment, one container running all agents with synchronous model calls and in-memory orchestration: easy to prototype, but a single failure point that wastes resources when idle and is hard to parallelize across roles.

Use actors when you need: persistent per-agent memory (conversation history, learned behavior), high concurrency (real-time bidding, IoT coordination), heterogeneous agents across a cluster, location transparency (actors can move or replicate without code changes) and supervision that restarts failed actors automatically. The chapter's threshold: the infrastructure investment pays off roughly beyond 10 to 20 agents, under variable load, when downtime is expensive, or when latency demands tighten. Below that, stay with a broker or a monolithic service.

Framework choice:
- **Ray**: Python-native. Stateful actors via a remote decorator, asynchronous method calls, resource-aware scheduling, optional restarts and retries, clustering. Pairs naturally with Python agent stacks; favors ease and speed of prototyping.
- **Orleans**: .NET virtual actors that are always logically addressable and are created, deactivated or recovered on demand; handles persistence, concurrency and lifecycle with little boilerplate. Can host each agent as a scalable service with stable identity (works alongside AutoGen).
- **Akka**: mature JVM option (Java, Scala). High performance with fine control over concurrency; Akka Cluster adds sharding, persistence, supervision and adaptive load balancing. Proven in telecom and trading.

Per-session isolation pattern: create one actor per (session ID, specialist type), managed by a session-manager actor that creates them lazily and returns handles. Each session gets isolated history and caches, calls within a session execute in order, and different sessions run in parallel across the cluster. Add what the basic pattern lacks: idle eviction of session actors, a cap on live actors, and persistence of state you cannot afford to lose on node failure.

Caveats: infrastructure and operational investment, framework lock-in, and the sequential-per-actor rule, which turns a hot actor into a throughput limit.

## 6. Orchestration and workflow engines

Messaging and execution do not by themselves sequence steps, track dependencies, retry failures or survive restarts. Workflow engines add that layer, separating coordination logic from transport, and give idempotency, recoverability and durable state.

Use one when processes depend on unreliable externals (APIs, model calls, human approvals), may fail midway, or run for a long time (a procurement flow that waits days for a supplier). Prioritize them in high-stakes domains such as financial transactions and compliance-heavy operations. For quick, low-risk experiments a script is enough.

- **Temporal**: durable stateful workflows; each agent step is an activity with its own timeout and retry policy; progress is checkpointed so a failure in step three retries step three without rerunning steps one and two; signals let a running workflow wait for human input or pause.
- **Apache Airflow**: DAG-based, mature ecosystem and visualization; best for scheduled, batch or dependency-heavy pipelines (ETL, model training). A poor match for live, rapidly changing conversations between agents.
- **Dagger**: pipelines written as code that compose containers and model calls, cache results automatically and are type checked; runs the same locally, in CI/CD and in production, which suits local-first prototyping.
- **Conductor**: named in the chapter alongside Temporal as a production workflow engine option.

Design rules: make every activity idempotent; set explicit per-step timeouts and retry limits; pass state between steps explicitly; keep model calls inside activities (not in deterministic workflow code) so replay stays deterministic.

## 7. Selection guide

| Situation | Pick |
|---|---|
| Prototype, few agents, tight latency, one team | Single container with in-process calls |
| Agents must scale or fail independently; replay needed | Broker (Redis Streams to start, Kafka for durable logs, NATS for real-time/edge) |
| Stateful agents per user or session, high concurrency, more than about 10 to 20 agents | Actor framework (Ray for Python, Orleans for .NET, Akka for JVM) |
| Long-running, multistep, must resume after failure or wait for humans | Temporal-style durable workflow engine |
| Scheduled batch pipelines that include agent steps | Airflow |
| Agents owned by other teams or vendors, discovered at run time | A2A, with your own authz and validation |

## 8. Pitfalls

- Staying on in-memory routing in production and losing in-flight work on every deploy.
- Brokers without idempotent consumers, dead-letter handling or response timeouts.
- Adopting actors or a cluster for three agents and low traffic.
- Long-running agent workflows built from ad hoc retries instead of a durable engine.
- Trusting A2A peers because they presented a card.
