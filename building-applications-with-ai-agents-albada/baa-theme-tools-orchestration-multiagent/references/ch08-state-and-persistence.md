# State and Persistence in Multiagent Systems

Multiagent systems carry state that outlives a single call: shared task state, each agent's memory, and task metadata spanning several executions, workflows or restarts. Durability, consistency and access patterns get harder as agents multiply.

## Three questions before choosing storage

1. What kind of memory is it (task scratch, long-term knowledge, workflow progress)?
2. What happens if it is lost mid-task (retry cheaply, redo expensive work, or corrupt an external side effect)?
3. Who reads it, how often, and by what key (exact lookup, query, semantic similarity, archival retrieval)?

## Map memory type to storage

- **Episodic memory** (short-lived, task-specific): in-memory or transient storage; little durability needed.
- **Semantic memory** (long-term knowledge reused across interactions): durable storage with search or vector indexing.
- **Workflow durability** (survive failure in the middle of a process): an engine that checkpoints automatically, such as Temporal or Orleans.

## Storage options and their trade-offs

- **Databases (PostgreSQL, Redis)**: flexible, queryable, inexpensive, fully controllable per agent. You are responsible for the schema, for keeping reads and writes consistent, for caches and for recovery, which adds engineering effort and room for subtle bugs. Best for custom systems with many queries.
- **Vector stores (for example Pinecone)**: semantic retrieval over scalable embeddings; cost more and need specialized setup. Best for knowledge-heavy agents.
- **Object storage (Amazon S3, Azure Blob Storage)**: cheap, durable and highly available for large or unstructured outputs such as plans, tool traces and JSON blobs. Access is slower and there is no native index, so you need a separate tracking table that links each artifact to its task, agent and state. Best for immutable, archival outputs.
- **Stateful orchestration frameworks (Temporal, Orleans)**: persistence is built into the workflow or actor lifecycle. Temporal checkpoints progress, replays deterministically and handles failures transparently; Orleans gives each actor durable, event-driven state with little boilerplate. Less code and better resilience, at the price of lock-in to the framework's serialization formats, execution model and language bindings.

## Choosing between workflow-native and explicit database state

Prefer workflow-native persistence when: SLAs are tight, agents depend on each other's results across steps, or coordination is real time. Prefer explicit database-driven state when: the system is modular or research-oriented and you value control over schema and visibility into every write.

Most real systems combine them: workflow engine for progress, database for queryable business state, vector store for knowledge, object store for bulky artifacts.

## Worked example

A multiagent procurement assistant:
- Per-request scratch notes from the negotiation specialist: in process memory, discarded after the task.
- Supplier history and past contract clauses: vector store plus a relational table for exact fields such as supplier ID and rating.
- Generated purchase-order drafts and full tool traces: object storage, with a table row holding task ID, agent, artifact URI and status.
- The multi-day approval flow (draft, legal review, human sign-off, issue PO): a durable workflow so a crash after legal review does not resend the request to legal.

## Checklist

- Every piece of state has an owner agent and a declared lifetime.
- Shared state has a single writer or an explicit concurrency rule.
- Artifacts in object storage are indexed back to task and agent.
- Recovery is tested: kill a worker mid-task and confirm the system resumes without duplicate side effects.
- Session state is isolated so one user's history cannot leak into another's run.

## Pitfalls

- Keeping long-term memory in process memory and losing it on restart.
- Using a vector store for exact lookups that a relational query answers better and cheaper.
- Dumping artifacts into object storage with no index.
- Adopting a stateful framework without checking its serialization and language constraints against your stack.
