---
name: sahp-ch11-distributed-workflows
description: Guidance for choosing and designing coordination of multi-service workflows (orchestration vs choreography), based on Chapter 11 of Ford, Richards, Sadalage and Dehghani's "Software Architecture: The Hard Parts". Covers error-path analysis, semantic vs implementation coupling, workflow state options in choreography (front controller, stateless, stamp coupling) and scenario-driven trade-off tables. Use when deciding who coordinates a distributed workflow, modeling its failure paths, placing workflow state, or writing the ADR for that choice.
---

# Managing Distributed Workflows (SAHP Chapter 11)

Purpose: help an agent decide how two or more services cooperate to complete one business workflow. Coordination is one of the three dynamic coupling forces (with communication and consistency), and the choice is between a per-workflow orchestrator (mediator) and choreography (services hand work to each other with no central coordinator). Neither is universally correct; the agent's job is to model the workflow's real error and alternate paths, then pick the style whose trade-offs match the workflow's complexity and its scale, responsiveness and error-handling needs.

## Key decision rules

1. **No absolutes.** Reject blanket policies such as "always choreograph to stay decoupled." Decide per workflow.
2. **Judge on the error paths, not the happy path.** Choreography usually looks simpler for the success case; the difference shows up once you draw rejections, back-orders, cancellations, reassignments and compensations.
3. **Complexity drives the need for an orchestrator.** The more steps, branches, error conditions and retries a workflow has, the more valuable a central owner becomes. Few and rare error cases plus a need for throughput favor choreography.
4. **Count new links per error path.** In orchestration, error handling reuses the paths already present for the happy path. In choreography, each error scenario tends to add service-to-service links and pushes workflow knowledge into domain services. A growing link count is a warning sign.
5. **One orchestrator per workflow, never a global one.** A shared enterprise-bus-style coordinator becomes a coupling point that defeats the purpose of microservices. Keep domain logic out of the orchestrator; it owns only workflow state, sequencing, retries, notifications and error handling.
6. **Orchestration buys** a single place for workflow logic, easier error handling, retry-based recovery from brief outages, and queryable workflow state. **It costs** a throughput choke point, a potential single point of failure (redundancy helps but adds complexity), less parallelism, and tighter coupling between orchestrator and services.
7. **Choreography buys** responsiveness, independent scaling, fault tolerance through many instances, and loose coupling. **It costs** a scattered workflow, no natural state owner, harder error handling (services must know more of the workflow), and harder recovery.
8. **Semantic coupling is a floor.** The domain's inherent workflow coupling cannot be removed by any implementation; implementation choices can only add to it. Align the implementation with the domain workflow (domain partitioning) unless a specific, stated benefit justifies extra structure.
9. **Choreography still needs a state decision.** Pick explicitly among a front controller (first service owns workflow state), stateless choreography (rebuild status by querying services) and stamp coupling (state travels in the message). Each moves cost to a different place.
10. **Mix sync and async inside one workflow.** Use synchronous calls where the next step depends on the result in time (for example payment authorization) and asynchronous ones where timing is loose (fulfillment, notifications).
11. **Link to sagas.** Choreographed sagas (Phone Tag, Time Travel, Anthology) trade error-handling ease for throughput; Horror Story is the trap when choreography meets atomicity and async. Orchestrated sagas (Epic, Fairy Tale, Fantasy Fiction, Parallel) trade scale for manageable complexity.
12. **Record the choice** in an ADR with the scenarios that decided it and the condition under which to revisit (for example a scale requirement that the orchestrator cannot meet).

## Default workflow

1. Write down the workflow steps and mark which are customer-facing (latency-sensitive) and which run in the background.
2. Enumerate alternate and error paths: rejections, timeouts, cancellations, out-of-stock or reassignment, partial completion that needs compensation.
3. Sketch both styles. For each error path, note who detects it, who must be told, and whether a new communication link appears.
4. List the forces that matter to stakeholders (workflow control, status queries, error handling, throughput, elasticity, fault tolerance) and credit each to orchestration, choreography or both. A force can favor both.
5. Pick the style; if choreography, also pick the workflow state approach (rule 9).
6. Decide sync vs async per call (rule 10) and the transaction model per service.
7. Write the ADR: context, decision, the scenarios considered, consequences and revisit triggers.

## References

- [references/orchestration-vs-choreography.md](references/orchestration-vs-choreography.md): read when comparing the two coordination styles, tracing error paths, mapping the choice to saga patterns, or building a scenario-by-scenario trade-off comparison and ADR.
- [references/choreography-workflow-state.md](references/choreography-workflow-state.md): read when a choreographed workflow needs status tracking or shared context and you must choose between front controller, stateless choreography and stamp coupling.
- [references/semantic-vs-implementation-coupling.md](references/semantic-vs-implementation-coupling.md): read when judging whether an architecture adds avoidable complexity to a workflow, explaining technical vs domain partitioning, or justifying an orchestrator by workflow complexity.
- [references/source-map.md](references/source-map.md): read to find which file covers a given chapter section.

## Scripts

None. The chapter's analysis is qualitative and scenario-driven; no calculation it supports would add value over the checklists in the references.
