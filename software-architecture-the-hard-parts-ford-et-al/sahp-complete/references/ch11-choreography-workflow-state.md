# Workflow State in Choreography

## The problem

Every workflow carries transient state: which steps finished, which remain, ordering, errors hit, retries attempted. Orchestration gives this an obvious home, the orchestrator (some designs deliberately make orchestrators stateless to scale further, pushing state to a store). Choreography has no natural owner, so the architect must choose one of several placements. Three common options follow; each moves cost somewhere different.

## Option 1: Front controller

The first service in the chain (the one receiving the initial request) owns workflow state in addition to its domain behavior. Downstream services call back to it to report progress or update status.

- Gains: behaves like a lightweight mediator inside a choreographed design; answering "where is instance X?" becomes a single lookup.
- Costs: a domain service now carries workflow concerns and grows more complex; extra callbacks increase communication overhead; the added chatter hurts performance and scale.
- Fit: choreography is preferred for throughput, but users or operators need a cheap, authoritative status view.

## Option 2: Stateless choreography

No service keeps workflow state. When someone asks for status, a query fans out to each participant and assembles a snapshot in real time.

- Gains: maximum decoupling and the best performance and scale for the workflow itself.
- Costs: status must be reconstructed on every query, which adds network chatter and costs in performance and scalability at query time; reconstruction logic becomes complicated quickly as the workflow grows.
- Fit: simple flows where status queries are rare or can tolerate latency.

Sketch of on-demand reconstruction (original):

```python
def booking_status(booking_id, clients):
    parts = {name: c.status_of(booking_id) for name, c in clients.items()}
    order = ["reservation", "payment", "allocation", "notification"]
    done = [s for s in order if parts.get(s) == "done"]
    failed = [s for s in order if parts.get(s) == "failed"]
    if failed:
        return {"state": "failed", "at": failed[0], "parts": parts}
    nxt = order[len(done)] if len(done) < len(order) else None
    return {"state": "complete" if nxt is None else "in_progress",
            "next": nxt, "parts": parts}
```

Note how this function must know the workflow's order: state knowledge did not disappear, it moved into the query path.

## Option 3: Stamp coupling

Workflow state rides inside the message contract. Each service updates its own section and forwards the enlarged message to the next participant, so any consumer of the message can see progress without asking anyone.

- Gains: no extra queries to a state owner; no need for a front controller; each service gets more context about the overall flow.
- Costs: larger contracts carrying data that individual services may not need; still no single place to ask for the current status of an in-flight instance, so it is only a partial answer to status queries.
- Fit: services benefit from seeing upstream results, and status queries can be served by whichever service last saw the message, or by a separate listener.

Example message shape (invented):

```json
{
  "bookingId": "B-981",
  "customer": {"id": "C-12"},
  "workflow": {
    "reservation": {"status": "done", "at": "2026-03-02T10:01Z"},
    "payment": {"status": "done", "authCode": "A77"},
    "allocation": {"status": "pending"}
  }
}
```

Contract design choices (how loosely or strictly such messages are specified) can raise or lower workflow coupling in choreographed systems; treat contract strictness as a separate decision.

## Choosing among the three

| Question | Leans toward |
|---|---|
| Need an authoritative, cheap status lookup? | Front controller |
| Throughput and decoupling dominate, status queries rare? | Stateless choreography |
| Downstream steps need upstream results anyway? | Stamp coupling |
| Status needed and workflow has many error paths? | Reconsider orchestration |

These options can be combined, for example stamp coupling for context plus a front controller for queries, but each addition reintroduces some of the coupling choreography was chosen to avoid.

## Pitfalls

- Assuming choreography means "no state": the state exists; only its placement is chosen.
- Letting a front controller accumulate so much workflow logic that it becomes an undeclared orchestrator with domain code mixed in.
- Stamp-coupled messages growing without bound, with every service parsing fields it does not own.
- Stateless reconstruction that silently encodes the workflow order in a reporting service nobody maintains.
