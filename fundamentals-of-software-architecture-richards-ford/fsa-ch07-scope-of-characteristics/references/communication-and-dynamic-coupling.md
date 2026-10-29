# Communication between quanta and dynamic coupling

## Why communication matters for scope

When quanta call each other at runtime, their operational characteristics (performance, scalability, elasticity, availability, responsiveness) interact through timing and blocking. A synchronous call makes the caller wait on the callee, so for the duration of that interaction the two behave as one unit and the weaker profile wins. This is why the quantum definition talks about communication, and why sync choices can redraw boundaries that static coupling analysis drew.

## The mismatch pattern

Shape of the problem: an upstream service with high or bursty throughput calls a downstream service with lower capacity, synchronously.

Invented example: a Ticketing service sells concert seats and, on each sale, calls a FraudCheck service synchronously. Ticketing scales horizontally and can absorb a flash sale of thousands of purchases per second. FraudCheck relies on a third-party scoring API limited to about 50 requests per second. During a flash sale the first calls succeed, then latency climbs, timeouts cascade, and Ticketing starts failing even though Ticketing itself is healthy. The two services were scoped with different scalability profiles, but the synchronous edge tied them into a single runtime scope with FraudCheck's ceiling.

(The book makes the same point with an auction that pushes payment details to a payment service that can only process one payment per 500 ms; many auctions closing together overwhelm it.)

## Why async is more forgiving

Putting a message queue between the two lets each side run at its own pace. The queue holds a burst until the consumer catches up, so the producer's spike does not become the consumer's outage. Limits to keep in view:
- A queue buffers bursts; it does not fix a sustained rate mismatch. If the producer always outpaces the consumer, the backlog grows until the queue fills or messages expire.
- Async changes the user-facing contract: the caller no longer gets an immediate answer, so the workflow must tolerate eventual results (status polling, notifications, compensating actions).
- Monitoring shifts from request latency to queue depth, age of oldest message and consumer lag.

## Decision checklist for each cross-quantum edge

1. Does the caller need the answer before it can respond to its own client? If not, default to async.
2. Compare the operational profiles on both sides (peak rate, latency budget, availability target). If they differ meaningfully, a sync edge is a risk that must be justified.
3. Is the load bursty or sustained? Bursty favors a queue; sustained mismatch requires scaling the consumer, throttling or shedding load at the producer, or redesigning the workflow.
4. If the edge must stay synchronous, treat both ends as one quantum for operational characteristics: give them aligned scalability and availability targets, or protect the caller (timeouts, circuit breaker, fallback, bulkhead).
5. Re-run the quantum analysis after deciding, because each new sync edge may merge quanta.

## Small illustration (original, framework-agnostic)

```python
# Sync: caller inherits callee capacity
def sell_ticket(order):
    verdict = fraud_client.check(order, timeout=0.3)   # blocks
    return confirm(order) if verdict.ok else reject(order)

# Async: caller and callee keep separate scopes
def sell_ticket_async(order):
    reserve(order, status="PENDING_FRAUD_CHECK")
    queue.publish("fraud-check-requested", order.id)   # returns at once
    return {"status": "pending", "order": order.id}

def on_fraud_verdict(msg):                             # consumer runs at its own pace
    confirm(msg.order_id) if msg.ok else release(msg.order_id)
```

## Pitfalls
- Declaring two services "independently scalable" while a synchronous call chain links them.
- Treating a queue as infinite capacity.
- Converting to async without redesigning the user experience around pending states.
- Evaluating each service's characteristics in isolation and never checking the edges.
