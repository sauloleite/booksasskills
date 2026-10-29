---
name: sahp-ch10-distributed-data-access
description: Guides how a service reads data owned by another service once databases are split, comparing four read-access patterns (inter-service communication, column schema replication, replicated in-memory caching, shared data domain) on latency, coupling, consistency, ownership, volume and security. Based on Chapter 10 of Ford, Richards, Sadalage and Dehghani's "Software Architecture: The Hard Parts". Use when a service needs data it does not own, when a cross-service join disappears after a data split, when sizing a replicated cache, or when writing an ADR for read access.
---

# Distributed Data Access (SAHP Chapter 10)

After data is decomposed, writes have an owner, but other services still need to read that data. A single SQL join in the monolith becomes a design decision with four main answers, each trading performance, availability, consistency, ownership and contract stability differently. This skill helps an agent pick one, size it, and record the decision. It covers read access only; write ownership and joint ownership belong to the previous chapter (ownership and transactions).

## Key decision rules

1. **Frame the question as read access to a non-owned table.** Identify the owner (sole writer), the reader, which columns are needed, the read frequency, data volume, update rate, and consistency need. Never let the reader become a writer as a side effect of the chosen pattern.
2. **Inter-service communication is the default but not free.** Each request pays network latency (roughly 30 to 300 ms), security latency (roughly 20 to 400 ms for auth on the target endpoint) and data latency (an extra query on the owner side, roughly 10 to 50 ms). Summed, a single lookup can approach one second. It also couples availability (owner down means reader down) and scaling (reader growth forces owner growth), and needs a contract.
3. **Switching transport does not remove the dependency.** Messaging instead of REST still waits for an answer; a request/reply over a queue is the same synchronous dependency.
4. **Column schema replication** copies the needed columns into the reader's table. It wins on speed, fault tolerance and scale but brings synchronization, consistency lag and ownership drift (readers may start editing copies). Prefer async propagation (queue, topic, event stream) unless immediate transactional sync is mandatory. Reserve it for aggregation, reporting, very large volumes, or extreme responsiveness or fault tolerance needs; avoid it for ordinary lookups.
5. **Replicated in-memory cache** (not a single local cache, not a distributed cache server): the owner is the only writer, readers hold read-only replicas kept in sync by the cache product. Best for read-heavy, relatively static, modest-size data. Check four costs: first-instance startup dependency on the owner, memory (cache size times every instance that holds it; feasibility drops sharply beyond about 500 MB per cache), high update rates that replication cannot keep up with, and peer discovery configuration that is hard in cloud and container networks.
6. **A distributed cache server does not solve this problem.** It moves the availability dependency to the cache server, keeps a network hop, and lets any service write, which breaks ownership unless governed.
7. **Shared data domain** puts the owner's and reader's tables in one shared schema: plain joins, full consistency, foreign keys, views, procedures and triggers survive, and no transfer contract is needed. The cost: the schema itself becomes the contract (a table change can ripple to every service in the domain), ownership needs governance, and every service sees everything in the schema. Use when integrity constraints matter, consistency must be strong, and the other patterns fail on volume or reliability.
8. **Eliminate, then confirm.** Rule options out by hard constraints (volume, consistency, reliability of the owner, domain boundaries, a service already bound to another schema), then state a hypothesis for the survivor and actively hunt for its negatives before committing.
9. **Count operational and skill risk as trade-offs.** Product licensing, deployment limits (availability zones, firewalls), and team inexperience with a technique belong in the analysis; mitigate with a proof of concept.
10. **Everything is a trade-off.** If an option looks free of downsides, the downside has not been found yet; keep looking.

## Default workflow

1. Capture the access profile: owner, reader, fields, reads per request, peak instances of each service, record size and count, update frequency, consistency tolerance, security sensitivity.
2. Apply hard eliminations (see the decision reference) to the four patterns.
3. For replicated caching, compute total memory with the sizing script; for inter-service calls, estimate the per-request latency budget.
4. State a hypothesis for the best survivor and list its negatives (startup order, licensing, skills, contract churn, security exposure).
5. Plan mitigations (startup ordering, PoC, field-level contracts, read-only access, async sync channel).
6. Record an ADR: context (options considered), decision (including who is sole writer), consequences.

## References

- [references/data-access-patterns.md](references/data-access-patterns.md): read when you need the mechanics, strengths, weaknesses, fit and pitfalls of inter-service communication, column schema replication and the shared data domain.
- [references/replicated-caching.md](references/replicated-caching.md): read when replicated caching is a candidate, to compare caching models, check the four limiting trade-offs, size memory and plan startup and cloud configuration.
- [references/choosing-and-recording.md](references/choosing-and-recording.md): read when you must pick among the patterns, run a hypothesis-based trade-off session, work through an example, or draft the ADR.
- [references/source-map.md](references/source-map.md): read to trace each chapter section to the reference that covers it.

## Scripts

- `scripts/replicated_cache_sizing.py`: run to compute the per-instance and total memory a replicated cache needs across all services holding it, and to flag the size threshold.
  - `python3 scripts/replicated_cache_sizing.py --record-bytes 1300 --records 900 --instances owner=2 reader=4`
  - `python3 scripts/replicated_cache_sizing.py --cache-mb 500 --instances catalog=3 wishlist=5 --threshold-mb 500`
  - Add `--json` for machine-readable output.
