# Communication Patterns: Orchestration, Choreography, CQRS

## Contents
- Patterns hidden inside styles
- Orchestration vs choreography
- Choosing between them
- Worked example
- CQRS
- CQRS decision checklist
- Pitfalls
- Review questions

## Patterns hidden inside styles

Many communication patterns originated in event-driven architecture but apply to any distributed system that talks via messages or events (microservices, event-driven, service-based variants). Teams frequently implement them without naming them. Naming them lets you reuse their known trade-offs instead of rediscovering them. "Mediator" (event-driven terminology) and "orchestrator" (microservices terminology) are the same pattern under two names.

## Orchestration vs choreography

Setup: several domain services must cooperate to complete one workflow. With orchestration, an extra coordinating service directs the steps. With choreography, services react to each other's events and no single component owns the flow.

### Orchestration

Strengths
- Centralized workflow: one component holds state, behavior and edge-case rules; this pays off more as workflow complexity rises.
- Error handling: a clear owner of the workflow's state makes compensations and error paths easier to express.
- Recoverability: because the orchestrator tracks progress, it can retry a step when a domain service has a brief outage.
- State management: workflow state is queryable in one place, and the orchestrator can also hold transient state used by other workflows.

Weaknesses
- Responsiveness: every interaction passes through the orchestrator, which can become a throughput bottleneck.
- Fault tolerance: domain services become more recoverable, but the orchestrator itself is a single point of failure for the workflow. Redundancy helps but adds complexity.
- Scalability: extra coordination points reduce parallelism, so it scales worse than choreography.
- Coupling: the orchestrator is tightly bound to the domain services. Sometimes that is necessary, but microservices culture generally discourages it.

### Choreography

Strengths
- Responsiveness: fewer chokepoints, more parallel work.
- Scalability: no coordinator, so each service scales independently.
- Fault tolerance: no single coordinator to lose; multiple service instances can absorb failures. (Running several orchestrators is possible, but since all traffic flows through them, the workflow's fault tolerance stays tied to them.)
- Decoupling: no central component binding the services together.

Weaknesses
- Distributed workflow: with no owner, errors and boundary conditions are hard to manage.
- State management: no single holder of in-progress state.
- Error handling: each domain service must know more about the overall workflow to react correctly.
- Recoverability: no central actor to retry or remediate.

Observation: the two lists are near mirror images. What orchestration gains in control it pays for in throughput and coupling, and vice versa.

## Choosing between them

Lean toward orchestration when:
- The workflow has many steps, branches or compensations.
- Business stakeholders need to query "where is order X right now?"
- Retries and remediation must be consistent and auditable.
- Throughput is moderate and the coordinator can be made redundant.

Lean toward choreography when:
- The workflow is short and mostly the happy path.
- Peak throughput, elasticity and independent scaling dominate.
- Teams must evolve services independently with minimal coordination.
- Losing a coordinator would be unacceptable and redundancy is too costly.

Hybrid: orchestrate the error-prone core and choreograph peripheral notifications. Whatever the choice, record the trade-off and revisit it when workflow complexity or load changes.

## Worked example

An insurance claim flow: intake, fraud screening, adjuster assignment, payout, notification. Fraud and payout require compensations and regulators ask for per-claim status. Volume is a few thousand claims a day.

Assessment: complexity, error handling and queryable state dominate; throughput is modest. Choose orchestration for intake through payout, deploy the orchestrator with an active-standby replica, and let notification subscribe to a "claim paid" event (choreographed) so it can scale and fail independently.

Contrast: a clickstream enrichment pipeline at 50k events per second with idempotent steps and no compensations favors choreography.

## CQRS

Command Query Responsibility Segregation divides one combined read/write path to a database into two paths.

- Baseline: the application reads and writes the same database as part of its own infrastructure. Fine for most systems.
- CQRS: writes go to one store (usually a database, sometimes a durable queue); that store propagates changes, usually asynchronously, to a separate store that serves reads.

Why use it
- Read and write volumes differ sharply.
- Reads must be isolated from writes for security or compliance.
- Read and write sides need different architecture characteristics (for example, the write side needs strong consistency and durability; the read side needs elastic scale and low latency).
- Each side benefits from a different data model.

It is classified as both a communication and a data pattern, and it shows up in many distributed systems and some monoliths.

Costs to state explicitly
- Asynchronous propagation means readers can see stale data; define the acceptable lag and how the UI handles it.
- Two stores, a sync mechanism and its monitoring add operational burden.
- Failure in the sync path must be detected and replayable.

Minimal illustration (original, framework-agnostic):

```python
# Write side: validate, persist, then publish a change event.
def place_order(cmd, write_db, outbox):
    order = write_db.insert_order(cmd.customer_id, cmd.items)
    outbox.publish({"type": "OrderPlaced", "id": order.id,
                    "total": order.total, "customer": cmd.customer_id})
    return order.id

# Projector: consumes events and maintains a read-optimized view.
def project(event, read_db):
    if event["type"] == "OrderPlaced":
        read_db.upsert("orders_by_customer", key=event["customer"],
                       append={"id": event["id"], "total": event["total"]})

# Read side: answers queries only from the projection.
def orders_for(customer_id, read_db):
    return read_db.get("orders_by_customer", customer_id) or []
```

## CQRS decision checklist

1. Can you show a measurable asymmetry between reads and writes (volume, latency target, security boundary, model shape)? If not, skip CQRS.
2. What staleness can readers tolerate, in seconds?
3. Which characteristics differ per side? List them; they justify the split.
4. Who owns the sync mechanism, and how is lag monitored and alerted?
5. Can the read store be rebuilt from the write side or an event log?

## Pitfalls

- Treating orchestration or choreography as tied to a style; either works in any distributed style.
- Assuming one decision holds forever; workflow growth can flip the answer.
- Adopting CQRS for symmetry or fashion, then fighting eventual consistency with no benefit.
- Hidden coupling in choreography: services that embed knowledge of downstream steps are a sign that an owner is missing.

## Review questions

- For each workflow, who answers "what state is this in?" today?
- What happens to an in-flight workflow if the coordinator restarts?
- What business harm results if the read model lags by 30 seconds?
