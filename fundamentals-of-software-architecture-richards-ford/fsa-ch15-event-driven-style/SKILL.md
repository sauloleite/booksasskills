---
name: fsa-ch15-event-driven-style
description: Guidance on the event-driven architecture style based on Chapter 15 of Richards and Ford's "Fundamentals of Software Architecture" (2nd ed.). Covers events vs messages, derived and extensible events, payload design (data-based vs key-based, anemic events, Swarm of Gnats), error handling, data-loss prevention, request-reply, mediator vs choreography, data topologies, risks, governance and team fit. Use when deciding whether EDA fits, designing or reviewing event flows and contracts, choosing a mediator or database topology, or writing fitness functions for an event-driven system.
---

# Event-Driven Architecture Style (FSA Chapter 15)

Purpose: help an agent decide whether an event-driven architecture (EDA) suits a problem and, if so, design, review and govern it using the chapter's criteria. EDA is treated as a full style (not just a pattern): decoupled processors react asynchronously to facts, giving top-tier performance, scalability, fault tolerance and evolvability at the price of simplicity, testability, workflow control, error handling and recoverability.

## Key decision rules (apply without opening references)

Style fit
- Request model for structured, data-driven requests where certainty and workflow control matter; event model for things that *happened* and need responsive, scalable, dynamic reaction. If most processing is request-based, consider microservices instead.
- Frequent synchronous calls between processors signal EDA is the wrong style.
- Only eventual consistency is available; outcomes of a flow are less certain and harder to test.

Events and flows
- Event = past fact, usually no reply, one-to-many, topic/stream. Message = command or query, usually replied to, one-to-one, queue. Broadcasting a command does not make it an event.
- Every processor publishes what it did, even with zero subscribers (extensible hook for future features).
- Guard against poison events: no derived event chain may loop back into itself.
- Emit one derived event per distinct outcome when consumers differ by outcome; emit one event per business action, not per field changed (Swarm of Gnats). Size events around the outcome or state change.
- Async improves responsiveness (time to acknowledge), not performance (end-to-end time). It also detangles quanta that synchronous calls would fuse; but you then need a later path to report errors.

Payloads (decide per event type)
- Data-based: faster, fewer DB reads, works without DB access; costs multiple systems of record, contract and versioning burden, stamp coupling, bandwidth (rate x size x subscribers).
- Key-based: single system of record, trivial stable contract, minimal bandwidth; costs DB load from parallel lookups and trouble reaching other contexts' data.
- Core trade: scale and performance versus contract stability, bandwidth and integrity. For updates, avoid anemic key-only events: include changed fields with before and after values.

Reliability
- Errors: Workflow Event pattern. Consumer delegates the failure to a repair processor and moves on; repair resubmits to the original queue; unrepaired items go to a human dashboard. Repaired items arrive out of order, so park same-context messages FIFO if order matters.
- Data loss: persistent queues plus synchronous send (producer side); client acknowledge mode (consumer crash); ACID commit plus last participant support (data error). Streaming platforms such as Kafka need their own techniques.
- Request-reply: prefer correlation ID with a message selector over temporary reply queues (per-request queues slow the broker at volume). Request-reply still fuses the two processors into one quantum.

Topology and data
- Choreography maximizes decoupling, performance, scale; mediator (commands on point-to-point queues, central state, restart) maximizes control and error handling. Hybrids are common.
- Pick mediator tech by complexity: simple routing (Camel, Mule, Spring Integration), complex conditional (BPEL), long-running with human steps (BPM such as jBPM). Classify events simple/hard/complex and route all through a simple mediator that delegates.
- Use one mediator per domain to avoid a single point of failure.
- Data topology: monolithic (no sync calls, but one quantum, shared failure, scale and change limits), domain (better isolation; watch cross-domain sync calls), dedicated (best isolation and scale, costliest, most sync coupling). Inventory each processor's data needs first; if sync chatter grows, move toward coarser topology or redraw domains.

Governance and teams
- Govern static coupling (contract change rate, unused fields per consumer) and dynamic coupling (every sync call tracked by fitness function and justified).
- Quanta merge on shared databases and request-reply links.
- EDA is technically partitioned. Platform and complicated-subsystem teams fit well; stream-aligned teams struggle as flows grow; enabling teams fit poorly.

## Default workflow

1. Classify the main interactions as requests or facts; apply the style-fit rule and list the characteristics that justify EDA.
2. Sketch flows: initiating events, processors, derived events. Name events as facts, commands as messages.
3. For each event type choose payload style and granularity; estimate bandwidth.
4. Decide choreography, mediator, or hybrid per workflow (control and restart needs vs scale).
5. Choose data topology from the processors' data needs; list every resulting sync call or request-reply link.
6. Add error handling, data-loss safeguards and completion tracking.
7. Run the lint script on the flow model; count quanta; fix cycles and orphans.
8. Record decisions in ADRs and define fitness functions for contracts and sync calls.

## References

- [references/topology-and-event-semantics.md](references/topology-and-event-semantics.md): read when sketching flows, classifying events vs messages, or explaining derived, extensible and poison events, responsiveness vs performance, and quantum detangling.
- [references/event-payload-and-granularity.md](references/event-payload-and-granularity.md): read when choosing payload style per event, estimating bandwidth, or reviewing for stamp coupling, anemic events or Swarm of Gnats.
- [references/async-reliability-patterns.md](references/async-reliability-patterns.md): read when designing error handling, ordering after repair, loss prevention across producer, broker and consumer, or request-reply.
- [references/mediator-and-data-topologies.md](references/mediator-and-data-topologies.md): read when deciding choreography vs mediator, choosing mediator technology, or picking a database topology.
- [references/style-fit-risks-and-governance.md](references/style-fit-risks-and-governance.md): read when judging style fit, describing characteristics, counting quanta, listing risks, writing fitness functions, or assessing team topology fit.
- [references/source-map.md](references/source-map.md): read to find which file covers a given chapter section.

## Scripts

Run `python3 scripts/event_flow_lint.py model.json` to check an event-flow model (JSON described in the script docstring) for event-type cycles (poison events), extensible hooks, orphan subscriptions, high fan-out handlers, quanta formed by shared databases, request-reply and sync calls, and payload bandwidth versus bytes actually needed. Add `--json` for machine output and `--fanout N` to change the fan-out threshold (default 4, a heuristic). Exits 1 on cycles or orphans, so it can serve as a fitness function in CI.
