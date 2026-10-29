# Asynchronous Reliability: Error Handling, Data Loss, Request-Reply

## Contents
- Workflow Event pattern (error handling)
- Preserving order after repair
- Preventing data loss: three failure points and their fixes
- Request-reply (pseudosynchronous) messaging: correlation ID vs temporary queue
- Checklists

## Workflow Event pattern

Problem: in async flows there is no caller waiting to fix a bad input, so a consumer that hits an error can only log it, or worse, stall while it investigates and delay everything queued behind it.

Pattern (from reactive architecture), built on delegation, containment and repair:
1. Consumer fails on a message.
2. It immediately hands the message plus error details to a **workflow processor** (the workflow delegate) over an async channel and moves on to the next message. Throughput and responsiveness are unchanged.
3. The workflow processor diagnoses the problem without human help: deterministic rules for known faults, or anomaly detection (ML or AI) for unknown ones. It repairs the data and puts it back on the **original** queue.
4. The consumer sees the repaired message as new and processes it.
5. If the delegate cannot repair it, it routes it to another queue feeding a dashboard for a knowledgeable human, who fixes it and resubmits to the original queue (typically via a reply-to header).

Benefit: resiliency and responsiveness together. Typical use: you receive data from a party you do not control and must fix their errors yourself.

Invented example: a partner sends a batch of shipment records `ORDER,CARRIER,WEIGHT_KG`. One record has `12.5kg` in the numeric weight field. The intake service fails to parse it, forwards record plus parse exception to an intake-repair service, and carries on with the next record. The repair service recognizes a unit suffix rule, strips it, and requeues `12.5`. The intake service then processes it as a fresh record.

Sketch of the consumer side (pseudocode, broker-agnostic):

```python
def on_message(msg):
    try:
        process(msg.body)
    except Exception as err:
        publish("repair.requests", {
            "original": msg.body,
            "error": repr(err),
            "reply_to": msg.source_queue,
        })
    # either way, ack and move to the next message
    msg.ack()
```

### Preserving order after repair
Consequence: repaired messages re-enter the queue late, so they are processed out of sequence. If order matters within a context (for example, all instructions for one account must apply in sequence), handle it explicitly:
- When a message for context K fails, record K as "blocked".
- Park subsequent messages for K in a temporary FIFO store instead of processing them.
- When the repaired message for K succeeds, drain the parked messages for K in order and unblock K.
Complex but feasible. Decide up front whether any flow needs per-context ordering.

## Preventing data loss

Broker implementations differ:
- **AMQP brokers** (the chapter lists RabbitMQ, Solace, Amazon SNS, Azure Event Hubs as examples): producers publish to an exchange; consumer binding rules route a copy to a queue per subscriber. Supports the Event Forwarding pattern.
- **Jakarta Messaging (formerly JMS)**: topics without the exchange-to-queue step. Event Forwarding still works if subscribers are **durable subscribers**, meaning the topic holds the event for a subscriber that is down until it returns.
- **Event streaming (Kafka)**: loss-prevention techniques are different; consult the product's own documentation rather than applying the steps below blindly.

Scenario: producer A publishes; consumer B reads and writes the payload to a database. Loss can happen at three points, and the Event Forwarding pattern covers each:

| # | Failure point | Fix |
|---|---|---|
| 1 | A crashes before the broker acknowledges, or the broker acknowledges then crashes before delivery | **Persistent queues** (guaranteed delivery: broker writes to disk as well as memory) plus **synchronous send** (A blocks until the broker confirms it persisted the event). The event is always either still at A or durably in the broker. |
| 2 | B dequeues the event and crashes before processing | **Client acknowledge mode** instead of the default auto acknowledge. The event stays in the queue, tagged with B's client ID so no other consumer takes it, until B confirms. |
| 3 | B cannot persist because of a data error | **ACID database commit**, then **last participant support (LPS)**: the event is removed from the persistent queue only after B confirms both processing and the commit. |

Together these guarantee nothing is lost between A and the database. Note the cost: synchronous send adds latency on the producer, and persistence costs broker throughput; apply where loss is unacceptable.

## Request-reply messaging

Use when a processor needs something back before it can continue (a confirmation ID, an acknowledgment). In EDA this is done with messaging rather than direct calls, sometimes called pseudosynchronous. Each such channel pairs two queues: one for requests, one for replies. The producer sends, may do other work, then blocks waiting on the reply queue.

### Technique 1: correlation ID (preferred default)
1. Producer sends the request and remembers its message ID.
2. Producer blocks on the shared reply queue with a **message selector** (filter) matching correlation ID = that message ID. Replies meant for other requesters are skipped.
3. Consumer processes, builds a reply, and sets its correlation ID header to the original message ID.
4. Consumer posts the reply; the producer's selector matches it.

### Technique 2: temporary queue
1. Producer creates (or the broker auto-creates) a queue dedicated to this one request and names it in the reply-to header.
2. Producer blocks on that queue; no selector needed because only its reply can arrive there.
3. Consumer replies to the named queue.
4. Producer reads the reply and deletes the queue.

Trade-off: temporary queues are simpler, but creating and deleting a queue per request can noticeably slow the broker under high volume and concurrency. The authors usually recommend correlation IDs.

Architectural warning: request-reply, though built on async messaging, still binds the two processors into one architecture quantum, because the requester cannot proceed if the responder is down. Count every request-reply link when reasoning about quanta and fault tolerance.

## Checklists

Error handling
- Is there a later channel to tell the user about failures accepted asynchronously?
- Is there a workflow delegate for each consumer that ingests external or dirty data?
- Is there a human fallback queue and dashboard?
- Does any flow require per-context ordering, and is the park-and-drain logic designed?

Data loss
- Persistent queues and synchronous send on producers of critical events?
- Client acknowledge on consumers?
- Queue removal only after the database commit?
- If on a streaming platform, product-specific durability settings reviewed?

Request-reply
- Each request-reply link justified (could the data travel in the event payload instead?).
- Correlation IDs used unless volume is low.
- Timeouts and quantum impact documented.
