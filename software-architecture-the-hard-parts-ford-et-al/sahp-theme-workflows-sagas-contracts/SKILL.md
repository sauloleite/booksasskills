---
name: sahp-theme-workflows-sagas-contracts
description: Theme skill on how distributed services cooperate, from "Software Architecture: The Hard Parts" (Ford, Richards, Sadalage, Dehghani) (chapters 11, 12 and 13). Use when choosing orchestration or choreography, placing workflow state, choosing among the transactional saga patterns, handling errors with compensation or state management, modeling sagas as state machines, or designing strict versus loose contracts, consumer-driven contracts and avoiding stamp coupling.
---

# Workflows, sagas and contracts (Software Architecture: The Hard Parts, ch. 11 to 13)

Coordination, transactional behavior and contracts are the dynamic side of coupling. Each choice here trades control and consistency against scale and decoupling.

## Cross-chapter rules

1. **Compare coordination styles on failure paths.** Orchestration centralizes workflow, error handling and state at the cost of responsiveness and a bottleneck; choreography is the mirror image. Use one orchestrator per workflow, without domain logic.
2. **Decide where choreographed state lives:** a front-controller service, stateless reconstruction, or state carried in messages.
3. **Treat sagas as eight variants of three forces.** Communication, consistency and coordination combine into the named saga patterns; relaxing atomic consistency usually brings the biggest gains, while adding asynchrony to an atomic saga creates the most complexity.
4. **Prefer state management to compensation where possible.** Compensations lack isolation, cannot undo side effects and can fail; an explicit error state with retries and human escalation is often safer. Model sagas as state machines (`scripts/saga_check.py`).
5. **Own distributed transactions in code.** Keep a central list of sagas and tag service entry points that take part in them.
6. **Choose contract strictness before protocol.** Strict contracts give fidelity and checks but lock components together; loose contracts decouple but need governance. Semantic coupling can move but never disappear.
7. **Use consumer-driven contracts** where teams are mature, and keep contracts to what consumers need; measure unused fields and wasted bandwidth (`scripts/contract_usage.py`).

## Default workflow

1. Choose coordination and workflow state handling (ch11).
2. Pick the saga variant and error-handling approach; model it as a state machine (ch12).
3. Define contract strictness per integration and add contract tests (ch13).

<!-- BEGIN GENERATED: run tools/build_bundles.py to refresh -->

## References by chapter

Each link is one level deep; read only the files whose description matches the task.

### CH11: Managing Distributed Workflows

- [ch11-choreography-workflow-state.md](references/ch11-choreography-workflow-state.md): read when a choreographed workflow needs status tracking or shared context and you must choose between front controller, stateless choreography and stamp coupling.
- [ch11-orchestration-vs-choreography.md](references/ch11-orchestration-vs-choreography.md): read when comparing the two coordination styles, tracing error paths, mapping the choice to saga patterns, or building a scenario-by-scenario trade-off comparison and ADR.
- [ch11-semantic-vs-implementation-coupling.md](references/ch11-semantic-vs-implementation-coupling.md): read when judging whether an architecture adds avoidable complexity to a workflow, explaining technical vs domain partitioning, or justifying an orchestrator by workflow complexity.

### CH12: Transactional Sagas

- [ch12-compensation-vs-state-management.md](references/ch12-compensation-vs-state-management.md): read when deciding how a saga handles a failed step, diagnosing compensation problems (side effects, failed undo, isolation), or converting an atomic saga to eventual consistency.
- [ch12-saga-pattern-catalog.md](references/ch12-saga-pattern-catalog.md): read when choosing or critiquing a saga pattern, explaining one of the eight variants, or redesigning a slow or fragile atomic workflow.
- [ch12-saga-state-machines-and-tooling.md](references/ch12-saga-state-machines-and-tooling.md): read when modeling a saga as a state machine, writing its transition table, or setting up saga annotations and an inventory tool.

### CH13: Contracts

- [ch13-consumer-driven-contracts.md](references/ch13-consumer-driven-contracts.md): read when services own separate bounded-context models, when loose contracts need verification, or when setting up CDC tests and judging team readiness for them.
- [ch13-stamp-coupling.md](references/ch13-stamp-coupling.md): read when payloads are large or shared, when estimating bandwidth, when a consumer breaks on fields it ignores, or when choreographing a complex workflow that must carry its own state.
- [ch13-strict-vs-loose-contracts.md](references/ch13-strict-vs-loose-contracts.md): read when deciding where a contract sits on the spectrum, comparing gRPC, REST, GraphQL and name/value formats, designing a versioning policy, or assigning different strictness to edges of one workflow.

Merged section maps: [source-maps.md](references/source-maps.md).

## Scripts

Python 3 standard library only; run any script with `--help` for its arguments.

| Script | Purpose |
|---|---|
| `scripts/saga_check.py` (ch12) | saga_check.py: lint a transactional saga definition. |
| `scripts/contract_usage.py` (ch13) | Contract field-usage analyzer: detects stamp coupling and bandwidth waste. |

<!-- END GENERATED -->
