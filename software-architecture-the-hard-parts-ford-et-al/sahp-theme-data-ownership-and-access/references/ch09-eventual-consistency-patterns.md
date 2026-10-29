# Eventual Consistency Patterns

## Contents

1. The three patterns at a glance
2. Background synchronization
3. Orchestrated request-based
4. Event-based
5. Selection guide
6. Error-handling playbook
7. Worked example (invented)
8. Pitfalls checklist

## 1. The three patterns at a glance

All three get several service-owned data stores back into agreement after a business request that spans them. They differ in who drives the synchronization and when.

| Pattern | Who drives it | When data converges | Core weakness |
|---|---|---|---|
| Background synchronization | An external batch job or periodic process | Slowest: next batch run or polling interval | Couples to every data store, breaks bounded contexts |
| Orchestrated request-based | An orchestrator, during the user's request | Before the response returns | Slower responses, hard error handling, compensations |
| Event-based | Participants reacting to published events or commands | Usually very soon, in parallel | Error handling when a consumer fails mid-processing |

Running scenario used below (invented): a subscriber cancels a meal-kit subscription. The Account service removes the subscriber; the Delivery service and the Invoicing service still hold that subscriber's rows.

## 2. Background synchronization

**Mechanics.** A separate process, either a nightly batch or a service that wakes up periodically, inspects the data stores and aligns them. It must learn what changed, using one of: an event stream, database triggers, or comparing source tables against target tables (deltas). Whatever the detection method, the process must know every table and data source the business request touches.

**When convergence is acceptable.** Often the stores do not need to agree immediately. After a cancellation, leftover delivery and invoice rows until tonight's run may harm nobody. The user gets an instant confirmation because only one service did work during the request.

**Why it is dangerous in service-based and microservice designs:**

- **Data-source coupling.** The sync process writes directly into tables owned by other services, so those tables effectively have shared ownership. Every bounded context it touches is broken.
- **Change control.** Renaming or dropping a column in any owned table now needs coordination with the sync job.
- **Duplicated business logic.** Deletion is rarely just deletion. Suppose Invoicing keeps cancelled accounts for 90 days by setting a removal date column (zero meaning active) and purges daily. The sync job must reproduce that rule, so the rule now lives in two places and will drift.
- Slowest convergence of the three, and a complex implementation.

**Where it fits.** Closed, self-contained, heterogeneous systems that do not otherwise talk to each other or share data. Example (invented): a warehouse management package and a separate accounting package on a different platform; a scheduled job pushes new and amended shipments into accounting so the two stay aligned. Not suited to architectures where tight coupling of data to the owning functionality is essential.

Strengths: services stay decoupled from each other; good responsiveness.

## 3. Orchestrated request-based

**Mechanics.** All stores are brought into agreement while the user waits. An orchestrator owns the workflow: knowledge of the business process and participants, multicasting (fan-out) logic, error handling and the contracts with participants.

**Who orchestrates:**

- *An existing primary service takes on the role.* Avoids a new deployable, but overloads that service with two jobs and tends to produce tight coupling and synchronous dependencies.
- *A dedicated orchestration service per business request.* The authors' general preference; the domain service stays focused on its domain.

**Typical flow (invented timings).** Cancel request arrives at a Cancellation orchestrator. It calls Account synchronously first (this step can veto the whole request, for example if the account has an unpaid balance, and then nothing needs undoing). On success it fans out in parallel to Delivery and Invoicing, waits for both acknowledgements, and only then confirms to the user. Running the first step in parallel would shave latency, but sequencing it first is a deliberate choice for simpler error handling.

**Trade-offs.** Consistency is prioritized over responsiveness: extra network hops and back-and-forth calls add latency, more so if calls are serial. Error handling is complex and usually needs compensating transactions. On the plus side: services stay decoupled from one another (they talk only to the orchestrator), data agrees by the time the user hears back, and the business request behaves atomically from the user's point of view.

**The failure dilemma.** Account and Delivery have committed; Invoicing fails. The orchestrator, with the user still waiting, can:

1. Retry Invoicing.
2. Compensate: ask Account and Delivery to undo their changes.
3. Tell the user it failed and to try later, while repairing the inconsistency.
4. Swallow the error, report success and hope something else fixes it.

Options 3 and 4 only make sense if some other mechanism will reconcile the data. When orchestration is the only consistency mechanism, that leaves retry and, ultimately, compensation. Compensation has preconditions: the orchestrator must hold enough data to recreate what was removed (re-insert the account, reset the removal date to zero), and re-creation must not trigger side effects (a new-account workflow that issues a welcome credit or starts a fresh contract). And compensation itself can fail, leaving the data more inconsistent with no automated process left to fix it; that situation usually needs a human. Transactional sagas formalize these choices.

## 4. Event-based

**Mechanics.** The service that handles the request commits its own change, publishes an event (subscription cancelled) or a command (cancel subscription) to a topic or event stream via asynchronous publish-and-subscribe, and responds to the user. Other participants subscribe and update their own data in parallel.

**Why it is popular.** It is a favored and dependable choice in today's microservice and event-driven systems. Convergence is usually very fast because consumers work in parallel, services are highly decoupled, and the user does not wait for downstream updates.

**Delivery guarantees you must configure:**

- With topic-based brokers (ActiveMQ, RabbitMQ, Amazon MQ and similar), consumers must be **durable subscribers**: like a persistent queue, the subscriber need not be online when the event is published and still receives it later, and neither a broker crash nor a consumer crash loses the event.
- With event streaming (Apache Kafka and similar), the broker must persist events and retain them in the topic long enough for slow or recovering consumers.

**The weak spot: error handling.** A consumer that is merely down is fine; it catches up when it returns. A consumer that receives the event and then fails while processing is the hard case. Brokers retry delivery a configured number of times, then park it in a **dead letter queue (DLQ)**. An automated process should read the DLQ and attempt repair; whatever it cannot fix goes to a person.

Sketch of a consumer with idempotent handling and DLQ fallback (generic pseudocode):

```python
def on_subscription_cancelled(event, attempt, max_attempts=5):
    if already_processed(event.id):          # idempotency guard for redelivery
        return ack()
    try:
        mark_for_removal(event.subscriber_id, days=90)
        record_processed(event.id)
        return ack()
    except TransientError:
        if attempt < max_attempts:
            return retry(backoff_seconds=2 ** attempt)
        return send_to_dlq(event, reason="retries exhausted")
    except BusinessRuleViolation as err:
        return send_to_dlq(event, reason=str(err))  # needs repair job or a human
```

## 5. Selection guide

- Need the user to know everything is consistent when they get a response, and can accept slower responses plus compensation logic: **orchestrated request-based**, with a dedicated orchestrator.
- Need fast responses, high decoupling and quick convergence, and can build DLQ handling and idempotent consumers: **event-based** (the usual default for microservices).
- Integrating closed, independent systems with no shared ownership concerns, and hours of lag are acceptable: **background synchronization**. Avoid it inside a microservices estate.
- If none is acceptable because the business needs true atomicity, revisit ownership (consolidate or share a data domain) rather than forcing a pattern.

## 6. Error-handling playbook

For any chosen pattern, write down:

1. Failure points: which participant can fail, and after which commits.
2. Retry policy: count, backoff, idempotency keys so retries and redeliveries are harmless.
3. Compensation: the inverse operation for each committed step, the data it needs, and any side effects of re-creating state.
4. What happens if compensation fails: alerting, a repair queue, an owner for manual fixes.
5. Maximum tolerated soft-state duration, and how it is monitored.
6. User messaging: what the user is told during and after a failure.

## 7. Worked example (invented)

Library system: a member closes their account. Member service owns members; Loans service owns open loans and fines; Holds service owns reservations.

- Background sync: nightly job deletes holds and loans for closed members. Rejected: the job would need to replicate the rule that unpaid fines block closure and that loan history is retained for a year.
- Orchestrated: a Closure orchestrator first asks Loans whether fines are outstanding (veto point), then removes the member, then clears holds. Chosen, because closure must be refused immediately when fines exist and the member must see a definitive result.
- Event-based alternative considered: Member publishes "member closed"; Holds and Loans react. Rejected here only because the fines check needs a synchronous answer before committing.

## 8. Pitfalls checklist

- Background job writing directly into other services' tables inside a microservices architecture.
- Re-implementing a service's business rules in a sync job.
- Orchestration logic embedded in a domain service that also does its own work.
- Fan-out before the step most likely to veto the request.
- Compensation designed without the data needed to restore state, or with side effects on re-creation.
- Non-durable subscribers, or stream retention shorter than plausible consumer downtime.
- No DLQ consumer, or DLQ with no human escalation path.
