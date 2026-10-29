## Contents

- Origins and philosophy
- Topology essentials
- Bounded context as the driving rule
- Granularity: finding the right size
- Transactions and sagas
- Worked example: splitting an order domain
- Review questions

# Boundaries, Granularity and Transactions

## Origins and philosophy

- Unlike most styles, which get a name only after a pattern has spread, microservices was labeled early, via the 2014 Lewis and Fowler article that enumerated its characteristics. Their description became the reference definition.
- The style is a physical rendering of domain-driven design's bounded context. Inside a context, code and schema may be tightly bound; nothing crosses the edge (no shared class, no shared table). That is why people call it a "share nothing" architecture.
- Reuse is not free: getting it means inheritance or composition, and both add coupling. Because maximal decoupling is the style's main goal, the architect accepts duplication as the price. This is a direct application of the book's first law (every choice is a trade-off).

## Topology essentials

- Services are single-purpose and therefore smaller than in service-based, event-driven or orchestration-driven SOA styles.
- Each service carries everything it needs to run on its own, including its own data store and dependencies, and runs in its own process (container or VM).
- Process-per-service solves two problems of shared hosting (such as one application server running many apps): one tenant's growth starving shared resources, and weak isolation between tenants. Cheap cloud provisioning and containers made this level of separation practical.
- Cost: every hop is a network call plus a security check at the endpoint. Granularity therefore drives performance as well as design quality.
- The single most important design variable is granularity; transactions across boundaries are discouraged from the outset.

## Bounded context as the driving rule

Each service models one function, subdomain or workflow, and owns its classes, components, schema and database. Consequences an agent should apply:

- When two services both need a concept (address, money, customer summary), give each its own copy shaped for its own needs. Do not create a shared domain library.
- Treat microservices as domain partitioning taken to its limit. Any proposal that adds a technical layer spanning services (a shared business-rules service, a shared entity model) works against the style.

## Granularity: finding the right size

The common failure is reading "micro" literally. Services cut too thin must then be stitched back together with calls, producing a distributed ball of mud. The name was chosen to contrast with the very large services of early-2000s SOA, not to prescribe size. Some natural boundaries are large because some business processes are inherently tightly coupled.

Three boundary tests, applied together:

| Test | Question to ask | Signal to merge or split |
|---|---|---|
| Purpose | Does the service provide one significant, cohesive behavior for the application? | Two unrelated behaviors suggest split; a fragment of a behavior suggests merge |
| Transactions | Which entities must change atomically together? | Entities sharing a transaction usually belong in one service |
| Choreography (communication) | How much must this group talk to do its job? | Heavy mutual chatter suggests consolidating into a coarser service |

Process guidance:

- Iterate. The right granularity, data dependencies and communication style rarely emerge on the first pass; refine as domain knowledge grows.
- Granularity also interacts with data isolation (see the data topologies reference) and communication volume.
- Avoid the Entity Trap: one service per database entity creates anemic services and heavy interservice traffic.

## Transactions and sagas

Default stance: do not build transactions across service boundaries. They break the decoupling principle and create the strongest form of dynamic connascence (connascence of values, where several parts must change values together). When a design seems to need one, the usual fix is to regroup the services so the transaction lives inside one context.

Legitimate exception: two parts need clearly different architecture characteristics (for example, very different scalability or availability needs) and therefore separate services, yet must stay consistent. After weighing the trade-offs, use a saga.

How a mediator-based saga works:

1. A coordinating service calls each participant and tracks success or failure of each step.
2. If all steps succeed, the outcome is committed everywhere.
3. If any step fails, the coordinator issues compensating requests to every participant that already succeeded, asking it to undo its work.
4. A common implementation keeps each participant's change in a pending state until the coordinator confirms overall success.

Costs and warnings:

- Pending state gets hard when new requests arrive that depend on not-yet-confirmed data.
- Compensation multiplies network traffic regardless of protocol.
- A few cross-service transactions are acceptable; if they are the dominant feature of the system, choose a different style.
- The authors catalog eight saga variants in "Software Architecture: The Hard Parts" (chapter 12) for deeper study.

Minimal original sketch of compensation logic:

```python
def run_saga(steps):
    done = []
    for step in steps:
        try:
            step.execute()          # participant moves to PENDING
            done.append(step)
        except Exception:
            for prior in reversed(done):
                prior.compensate()  # undo already-applied work
            return "rolled_back"
    for step in done:
        step.confirm()              # PENDING -> COMMITTED
    return "committed"
```

## Worked example: splitting an order domain

A team proposes services Order, OrderLine, Price, Discount and Tax. Placing an order must atomically write lines, compute price with discount and tax, and save the order.

- Purpose test: none of OrderLine, Price, Discount or Tax provides a significant standalone behavior; they are fragments of "price and place an order".
- Transaction test: all five change together in one business transaction.
- Communication test: every order request fans out to four services synchronously.

Recommendation: merge into one Ordering service. Keep Tax separate only if it has distinct characteristics (for example an external compliance cadence or very different scaling); in that case it becomes a read-only call, not a transaction participant.

## Review questions

- Which entities in this design must commit together, and do they live in one service?
- Which services exist only because the domain has a table of that name?
- If we deleted the "micro" from the name, would we still draw these boundaries?
- Is any shared library carrying domain logic between contexts?
