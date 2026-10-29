# Dynamic Quantum Coupling: Communication, Consistency, Coordination

## Contents
- The three interlocking forces
- Communication: synchronous or asynchronous
- Consistency: atomic or eventual
- Coordination: orchestrated or choreographed
- Why the forces cannot be chosen separately
- The eight-corner space and its pattern names
- Runtime entanglement of quanta (elasticity example)
- Decision playbook
- Pitfalls

## The three interlocking forces

Dynamic coupling describes how quanta behave together while a workflow runs. Every inter-service interaction sits at a point defined by three forces:
- **Communication:** does the caller block for a reply (synchronous) or hand off and continue (asynchronous)?
- **Consistency:** must all participants commit or fail together (atomic), or may they converge over time (eventual)?
- **Coordination:** does a central orchestrator drive the steps, or do services react to each other (choreography)?

Because dynamic coupling only exists at runtime, governance for it must be continuous: monitors, tracing and call metrics, not build-time scans.

## Communication: synchronous or asynchronous

- **Synchronous:** the caller sends a request (gRPC, HTTP and similar) and does no further work until the receiver returns a value, a status or an error.
- **Asynchronous:** the caller posts a message, receives an acknowledgment that it will be handled, and resumes its own work. If a result is needed, the receiver answers later, for example through a reply queue, so caller and receiver progress in parallel.
- Queues are the usual mechanism but not the only one; libraries and frameworks can also provide asynchrony. Many diagrams omit the queue icon and just mark the arrow as asynchronous. When reading or drawing diagrams, make the convention explicit.

The communication choice ripples into synchronization, error handling, transactional behavior, scalability and performance. Never treat it as a transport detail.

## Consistency: atomic or eventual

Consistency is how strict transactional integrity must be across the calls in a workflow. One end of the spectrum is the atomic, all-or-nothing transaction that keeps data consistent during the request; the other end is a range of eventual consistency levels. Getting several services to take part in one atomic transaction is among the hardest things to build in a distributed system, which is why the usual guidance is to avoid cross-service transactions where possible. Data ownership, distributed transactions and consistency patterns are developed in the book's later data and saga chapters.

## Coordination: orchestrated or choreographed

Coordination is how much steering a workflow needs. Orchestration (a central coordinator) and choreography (services reacting to one another) are the two generic options. A single request answered by a single service needs no special thought here; the need for coordination grows with workflow complexity (more steps, more participants, more error paths).

## Why the forces cannot be chosen separately

Each choice pulls on the others. Two reliable tendencies:
- Atomic transactions are easiest when calls are synchronous and a mediator coordinates them.
- The highest scale comes from asynchronous, eventually consistent, choreographed interactions.

Picture a cube with one axis per force. A design decision is a point in that cube; moving along one axis changes what is easy or hard on the others. Mapping the forces this way is what turns a vague debate into criteria for trade-off analysis.

## The eight-corner space and its pattern names

Taking each force as binary gives eight combinations. The book names each one so later chapters can discuss them precisely (the full analysis comes in its transactional saga chapter):

- **Epic Saga:** synchronous, atomic, orchestrated. The tightest corner; closest to how a monolith behaves.
- **Phone Tag Saga:** synchronous, atomic, choreographed.
- **Fairy Tale Saga:** synchronous, eventual, orchestrated.
- **Time Travel Saga:** synchronous, eventual, choreographed.
- **Fantasy Fiction Story:** asynchronous, atomic, orchestrated.
- **Horror Story:** asynchronous, atomic, choreographed.
- **Parallel Saga:** asynchronous, eventual, orchestrated.
- **Anthology Saga:** asynchronous, eventual, choreographed. The loosest corner.

Qualitative reading (your own heuristic, not a rating chart): each move toward synchronous, atomic or centralized tightens runtime coupling, and each move toward asynchronous, eventual or distributed loosens it. Two names are warnings: insisting on atomicity while communicating asynchronously is a fragile pairing, worst when there is also no orchestrator to track state.

## Runtime entanglement of quanta (elasticity example)

Statically separate quanta can still be bound together during a call. Example (invented): a Checkout service is designed to burst to many times the instance count of a Fraud Scoring service. If Checkout calls Fraud Scoring synchronously, every checkout waits on the slower, less elastic service, so the pair behaves as one unit for elasticity, latency and availability while the call is in flight. If Checkout instead places a scoring request on a queue and continues, the queue absorbs the burst, each service scales on its own, and Checkout learns the result when it is ready.

Reminder of the two terms: scalability is handling many concurrent users over time; elasticity is absorbing a sudden spike of requests in a short window.

Takeaway: static coupling sets the default scope of operational characteristics; synchronous calls can temporarily enlarge that scope to include every quantum on the call path.

## Decision playbook

For each interaction in a workflow:
1. Record its three coordinates (communication, consistency, coordination).
2. Ask which business rule actually requires atomicity. If none, default to eventual and design the visible inconsistency window.
3. If atomicity is required, prefer synchronous plus an orchestrator, or reconsider the service boundary so the transaction stays inside one quantum.
4. If the participants have different scale or elasticity profiles, prefer asynchronous communication, or document why the slower service's limits are acceptable for the caller.
5. Add an orchestrator once the workflow has several steps or meaningful error handling; keep simple request and reply interactions free of coordination machinery.
6. Name the resulting corner and state what it gives up.

Example sketch (illustrative pseudocode of the two communication styles):

```python
# synchronous: caller inherits callee latency and availability
score = fraud_client.score(order)          # blocks
if score.ok: confirm(order)

# asynchronous: caller hands off, result arrives later
queue.publish("fraud.score.requested", order.id)
mark_pending(order)                         # continue serving traffic
# ... later, a reply handler:
def on_fraud_scored(msg): confirm_or_hold(msg.order_id, msg.result)
```

## Pitfalls

- Choosing the communication style first and discovering later that the consistency requirement contradicts it.
- Assuming that fine-grained services plus a saga is free; every split moves work into coordination and consistency.
- Measuring dynamic coupling only from code; it needs runtime observation.
- Treating a queue as a cure for sustained overload; it buffers bursts, it does not add capacity.
