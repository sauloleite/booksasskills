## Contents

- Two ways to handle a failed step
- Compensating updates: how they work
- The failure modes of compensation
- State management with eventual consistency
- Choosing between them
- Playbook: converting an atomic saga to state management
- Worked example (invented)
- Checklist

# Compensating Updates vs. State Management

Any of the eight saga patterns can be implemented in more than one way. The chapter contrasts two error-handling approaches: atomic distributed transactions repaired by compensating updates, and saga state management with eventual consistency. Whichever you pick, one rule holds: the current state of every distributed transaction must be known and actively managed.

## Two ways to handle a failed step

| Question | Compensating updates | State management |
|---|---|---|
| Goal on failure | Return every participant to its pre-saga state | Record where the saga stands and repair forward |
| Caller experience | Waits for all undo calls, then receives an error | Gets a success (or partial success) quickly |
| Who fixes the problem | The caller retries the whole operation | The system retries in the background, then escalates to a human |
| Data during repair | Briefly inconsistent while undo runs | Out of sync until the repair completes |

## Compensating updates: how they work

A compensating update reverses a write that another service already committed during the saga: undo an update, re-insert a deleted row, or delete an inserted one. A coordinator (the orchestrator in an Epic Saga, or each service in a Phone Tag Saga) tracks which participants succeeded and, when a later one fails, asks each earlier participant to reverse its work.

Strength: if every undo succeeds, all data returns to its prior state, and the whole operation can be retried or restarted cleanly.

## The failure modes of compensation

1. **No isolation.** A distributed transaction does not hide intermediate state. Between the original write and its reversal, other services and users can read and act on the "committed" value.
2. **Irreversible side effects.** If the original write triggered downstream work (an event to analytics, an email, a payment capture), reversing the source record does not undo that work. Telling every consumer to disregard earlier data needs intricate timing logic, and those consumers may have triggered further consumers. The chain of undo can go arbitrarily deep.
3. **Compensation can itself fail.** Teams tend to assume undo always works. When it fails, the system sits in a state that is neither the original nor the intended one, and the caller cannot be told anything coherent. A retry of the original request may now fail with "already done", confusing users further. The coordinator needs explicit logic for "the rollback did not happen".
4. **Poor responsiveness.** The caller waits for the forward calls, the failure, and every compensating call before learning that it failed. Issuing compensations asynchronously (as Parallel or Anthology sagas can) helps, but atomic sagas with compensation are generally slower.
5. **Locking dilemma.** While a saga is in flight, should participants accept other requests that depend on the pending value? Allowing them risks decisions made on data that may be reversed (worse with asynchronous calls). Blocking them preserves correctness but destroys throughput and scale.
6. **Semantic coupling of the user.** Atomic sagas make the person who started the workflow responsible for steps they do not care about. A field technician closing a job should not be blocked because a follow-up survey email failed.

Underlying point: a transaction forces every participant to pause and agree on one value. That is cheap inside one relational database, which is why it was overused in monoliths, and it gets harder the wider the scope. Few problems in distributed design are tougher than cross-service transactional coordination.

## State management with eventual consistency

Instead of undoing, the saga is modeled as a finite state machine. When a step fails, the coordinator moves the saga into an explicit error state (for example SURVEY_PENDING rather than CLOSED), returns a useful response to the caller, and then works in the background:

1. Retry the failed step, with analysis of the error.
2. If retries cannot fix it, route the case to an administrator or supervisor queue for manual repair.
3. Once fixed, advance the saga to its normal terminal state.

Benefits: the caller gets a fast answer and can move on; errors are hidden from users who do not own them; the business always knows exactly which sagas are incomplete and why.

Costs: participants' data is out of sync while errors are open, and reaching consistency may take noticeable time. Downstream readers must tolerate seeing partial outcomes.

This approach pairs naturally with the Fairy Tale and Parallel sagas, which keep an orchestrator to own the state and the repair loop.

## Choosing between them

The decision is a trade-off between responsiveness and consistency, made per workflow:

- Choose **compensation** only when the business genuinely cannot tolerate any window of partial completion and the participants' writes have no external side effects, or those side effects can be held until the saga completes. Keep the saga short and plan explicitly for compensation failure.
- Choose **state management** when the initiating user should not be coupled to secondary steps, when downstream side effects make undo unreliable, when responsiveness matters, or when participants are often unavailable.
- If atomicity concerns surface later, the state-managed Fairy Tale or Parallel designs are the first alternatives to evaluate, not a faster atomic saga.

## Playbook: converting an atomic saga to state management

1. List every step and mark which ones the initiating user actually needs before getting a response. Those form the synchronous critical path.
2. For each remaining step, define the error state the saga enters if that step fails and the repair action (retry policy, escalation target, deadline).
3. Remove compensations whose only purpose was to keep secondary steps atomic with the primary one.
4. For steps that emit events, decide whether consumers must ever see a reversal. If not, the side-effect problem disappears; if so, keep compensation local and explicit.
5. Make repair actions idempotent so background retries are safe.
6. Expose saga state to operations (dashboards, queues of stuck sagas) so the "out of sync" window is visible rather than silent.

## Worked example (invented)

An insurance claims system approves a claim, schedules a payout, and notifies the customer's broker. The original design is atomic: if the broker notification fails, the approval and payout schedule are reversed and the adjuster sees an error. Meanwhile the approval event has already reached the fraud-scoring service, which flagged the claim as "approved and paid quickly", so the reversal leaves fraud data wrong. Once, the payout reversal itself failed, leaving a scheduled payment on a claim shown as unapproved.

Redesign: the adjuster's request completes once approval and payout scheduling succeed. Broker notification failure moves the saga to BROKER_NOT_NOTIFIED; a background job retries with backoff for 24 hours and then raises a task for the broker-relations team. No reversals reach fraud scoring, and the adjuster is never blocked by a broker outage.

## Checklist

- [ ] Every saga has a defined, queryable current state.
- [ ] Each step's failure has a named outcome: compensate, retry, or escalate.
- [ ] Compensation failure has its own handling path and user-facing message.
- [ ] Side effects of each write are listed, with a decision on whether they can be reversed.
- [ ] The initiating user waits only for steps they own.
- [ ] The tolerated duration of inconsistency is agreed with the business.
- [ ] Locking policy during in-flight sagas is explicit, with its throughput cost acknowledged.
