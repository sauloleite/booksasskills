# Single-Agent vs Multiagent Architecture

Architecture determines how agents are structured, how they touch their environment and how work is split; it governs scalability, maintainability and flexibility. The chapter introduces the two families here; later chapters go deeper.

## Single agent

One agent perceives, decides, plans and acts with no peers.

Choose it when:
- The task is narrow and well defined (FAQ and order-tracking bots, data entry, file handling).
- One entity can handle the workload and there is no strong scaling need.
- You want the fastest path to design, build and deploy, with no coordination, messaging or synchronization layer.

Typical fits: customer service bots, general assistants, code-generation agents. The first support agent in this chapter is single-agent by design.

## Multiagent

Several agents pursue a shared goal, independently, in parallel or under coordination.

| Benefit | Meaning | Example |
|---|---|---|
| Specialization | Each agent owns a role | Collector, processor, user-facing agent |
| Parallelism | Subtasks run at once | Planning many delivery routes simultaneously |
| Scalability | Add agents as load or scope grows | New agent per region or domain |
| Resilience | One agent failing need not stop the rest; peers can take over | Backup agent absorbs a failed agent's queue |

| Cost | Meaning |
|---|---|
| Coordination and communication | Agents must share information and avoid duplicate work, conflicting actions and contention; without orchestration they become chaotic |
| Complexity | Protocols, coordination strategies and synchronization make design and maintenance harder |
| Lower efficiency | Context sharing and messaging burn extra tokens; cost rises and tasks can get slower unless communication is optimized |

Typical fits: complex, distributed or specialization-heavy domains such as financial trading, security investigations and collaborative research platforms.

## Decision rule

Pick by three factors: task complexity, need for scalability, and expected lifespan of the system.

1. Default to a single agent.
2. Move to multiagent only when at least one holds: distinct subproblems need different expertise or tools; independent subtasks would gain real wall-clock time from parallelism; scale or fault isolation demands separate units.
3. Before switching, estimate the token overhead of inter-agent context passing and confirm the gain outweighs it.
4. Once multiagent, define roles, message contracts and an orchestrator up front.

## Worked example (invented)

Support agent v1 handles cancel, refund, address change: single agent, three tools. Product asks to add fraud review of refunds over a threshold and product recommendations.

- Fraud review needs different data, a stricter model and an audit trail: candidate for a separate specialist agent, invoked only on flagged refunds.
- Recommendations are a different skill with a different success metric: separate agent or separate service.
- Routine intents stay with the original agent. Result: a small coordinator plus two specialists, adopted only for the paths that justify the coordination cost.
