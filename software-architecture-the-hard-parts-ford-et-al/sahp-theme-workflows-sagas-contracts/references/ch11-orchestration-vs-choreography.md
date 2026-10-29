## Contents

- Where coordination fits
- Orchestration: shape and behavior
- Choreography: shape and behavior
- Error-path walkthrough (invented example)
- Strengths and weaknesses, qualitatively
- Decision framework: state owner, coupling and complexity
- Mapping to the saga patterns
- Scenario-driven comparison and ADR
- Pitfalls
- Glossary

# Orchestration vs Choreography

## Where coordination fits

Dynamic quantum coupling has three interacting dimensions: communication (synchronous or asynchronous), consistency (atomic or eventual) and coordination (orchestrated or choreographed). This file covers coordination: how several services, each owning its own bounded context and data, are combined to carry out one piece of domain work. The two named patterns are only anchor points; real systems mix the dimensions in many permutations, so reason from the forces rather than from pattern names.

The topological difference is simple: orchestration has a coordinating component in the middle, choreography does not.

## Orchestration: shape and behavior

- A dedicated orchestrator (also called a mediator) drives the workflow. It holds workflow state, decides what runs next, handles optional steps and errors, and triggers notifications.
- Domain services stay focused on their own context. The orchestrator should carry no domain behavior beyond the workflow it coordinates.
- In microservices, create one orchestrator per workflow. A single enterprise-wide coordinator (the ESB model) couples everything to one component and works against the style's decoupling goal.
- Within one orchestrated flow, choose sync or async per call. Calls whose result gates the next step (payment authorization, credit check) are synchronous; calls without tight timing (fulfillment batches that run a few times a day, emails) can be asynchronous, avoiding needless blocking.
- Key property: when an error occurs, the orchestrator reacts using the same links it already has to each service. Error handling does not create new service-to-service paths.

Minimal sketch of an orchestrator's error handling (original, framework-agnostic):

```python
def run_booking(req, svc):
    state = {"id": req.id, "step": "start"}
    svc.reservations.create(req)                 # sync, must succeed
    state["step"] = "reserved"
    try:
        svc.payments.authorize(req)              # sync, gates next step
    except PaymentDeclined:
        svc.reservations.mark_failed(req.id)
        svc.notify.send_async(req.user, "declined")
        return {**state, "step": "failed_payment"}
    state["step"] = "paid"
    svc.vehicles.allocate_async(req)             # loose timing
    svc.notify.send_async(req.user, "confirmed")
    return {**state, "step": "allocating"}
```

## Choreography: shape and behavior

- The request enters the first service in a chain of responsibility. Each service does its part and emits a message that the next service consumes. The flow is designed in advance by the architect; it is not improvised, only executed without a conductor.
- The happy path looks leaner: no extra component, just a chain of events or commands.
- Error paths are where cost appears. When a late step fails after earlier steps have committed their own local transactions, the failing service must emit events (often a broadcast) that earlier services consume to compensate. Each such scenario tends to add communication links that the happy path never needed, and each domain service must learn more about the workflow.

## Error-path walkthrough (invented example)

Workflow: a car-rental booking with Reservation, Payment, Vehicle Allocation and Notification services.

| Scenario | Orchestrated handling | Choreographed handling |
|---|---|---|
| Happy path | Orchestrator calls each service in turn | Reservation emits, Payment consumes and emits, Allocation consumes and emits, Notification consumes |
| Card declined | Payment reports to orchestrator; it marks reservation failed and asks Notification to inform the user. No new links. | Payment must now emit a failure event consumed by Notification and Reservation. One new link (Payment to Reservation). |
| No car available at pickup branch | Orchestrator receives the failure, asks Payment to refund, Reservation to update status, Notification to inform. No new links. | Allocation must broadcast a failure; Payment, Reservation and Notification all subscribe and compensate. Several new links, and Allocation now knows the booking workflow. |
| Customer cancels mid-flow | Orchestrator knows the current step and compensates only what has completed | Each service must decide whether it has acted yet and whether to compensate, with no single view of progress |

Lesson: compare styles by counting new links and workflow knowledge leaked into services as the error list grows.

## Strengths and weaknesses, qualitatively

The two styles are near mirror images.

Orchestration is strong where choreography is weak:
- Centralized workflow: as complexity rises, one component holding state and sequencing pays off.
- Error handling: a clear owner of workflow state makes error branches tractable.
- Recoverability: the orchestrator can retry a step when a domain service has a brief outage.
- State management: workflow status and other transient data have an obvious, queryable home.

Orchestration is weak where choreography is strong:
- Responsiveness: every interaction passes through the mediator, which can throttle throughput.
- Fault tolerance: if the orchestrator goes down, the whole workflow stops; redundancy mitigates this at the cost of more moving parts.
- Scalability: an extra coordination point reduces parallelism.
- Coupling: the orchestrator is coupled to every participating service; sometimes that is acceptable and even necessary.

Choreography's mirror: fewer choke points, independent scaling, resilience through many instances and low coupling, against a distributed workflow with no owner, awkward state management, error handling that requires domain services to understand the workflow, and recovery without a natural place for retries.

## Decision framework: state owner, coupling and complexity

1. Workflow state lives somewhere: in an orchestrator, or in a domain service acting as front controller, or in messages, or nowhere (rebuilt on demand). Removing the mediator increases inter-service communication. That can be a fine trade.
2. Usefulness of an orchestrator grows roughly in proportion to workflow semantic complexity (steps, branches, error conditions).
3. Choreography's sweet spot: workflows that need responsiveness and scale, whose error scenarios are either simple or rare.
4. Orchestration's sweet spot: complex workflows with meaningful boundary and error conditions; it gives up some scale but usually removes a lot of complexity.
5. Quick heuristic questions:
   - How many distinct error or alternate paths exist, and how often do they fire?
   - Does anyone (customer, operations, metrics) need the current status of an in-flight instance?
   - Is peak throughput or elasticity a top driving characteristic for this workflow?
   - Would compensation require late steps to notify several earlier ones?
   - Can the orchestrator be made redundant at acceptable cost?

## Mapping to the saga patterns

The saga names encode communication, consistency and coordination (s/a, a/e, o/c):

- Choreographed, high throughput, harder error handling: Phone Tag (sync, atomic), Time Travel (sync, eventual), Anthology (async, eventual).
- Choreographed trap: Horror Story (async, atomic), where choreography combined with atomic consistency and async messaging becomes extremely hard to implement.
- Orchestrated, more manageable complexity: Epic (sync, atomic), Fairy Tale (sync, eventual), Fantasy Fiction (async, atomic), Parallel (async, eventual).

When each service keeps its own local transaction (as in Fairy Tale or Anthology), failures late in a flow require compensating updates in earlier services. A common business mitigation is to defer irreversible steps, for example capturing payment at shipment rather than at order.

## Scenario-driven comparison and ADR

When both designs look viable, do not argue in the abstract. Use this method:

1. List the concrete concerns the business has raised for this workflow.
2. For each concern, ask which style handles it better. Give credit to both when both can satisfy it (status queries, for example, can come from an orchestrator, from querying services, or from stamp coupling). The comparison is not zero-sum.
3. Stop when no further non-obvious concerns appear; the tally plus the weight of each concern decides.
4. Capture the decision in an ADR, including the consequence you accept and the trigger for revisiting.

Invented example: an insurance claim workflow (intake, adjuster assignment, field inspection, payout, satisfaction survey). Concerns: claims that stall unnoticed (favors orchestration: one owner sees stuck instances), live claim status for call-center agents (both can do it), adjuster reassignment and claimant withdrawal (favors orchestration: complex compensation). Result: orchestration, with the stated consequence that the claim orchestrator must be made redundant and the choice revisited if volume grows beyond what it can serve.

ADR skeleton (generic):

```
Title: Coordination style for <workflow>
Context: steps, error paths, stakeholder concerns, both options sketched
Decision: <orchestration | choreography + state approach>
Concerns considered: <concern -> favored style(s)>
Consequences: <accepted weaknesses>; revisit if <trigger>
```

## Pitfalls

- Picking choreography because "decoupled is always better" without drawing error paths.
- One orchestrator shared across many workflows (rebuilding an ESB).
- Domain rules creeping into the orchestrator.
- Treating the orchestrator as free: forgetting it needs redundancy and can cap throughput.
- In choreography, adding error links ad hoc until services form a mesh that nobody can reason about.
- Ignoring that both styles can sometimes satisfy a concern, which biases the comparison.

## Glossary

- **Mediator / orchestrator**: per-workflow component owning sequencing, state, retries and error handling.
- **Chain of responsibility**: in choreography, the ordered handoff of work from one service to the next.
- **Compensating message**: an event or command that asks a service to undo or adjust work it already committed.
- **Coordination point**: any component through which interactions must pass; it limits parallelism.
