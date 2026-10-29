---
name: sahp-theme-data-ownership-and-access
description: Theme skill on distributed data from "Software Architecture: The Hard Parts" (Ford, Richards, Sadalage, Dehghani) (chapters 9 and 10). Use when assigning table ownership to services (single, joint, common), resolving joint ownership, replacing ACID with eventual consistency patterns, designing compensations, or choosing how a service reads data it does not own (inter-service calls, column replication, replicated caching, shared data domain).
---

# Data ownership and distributed data access (Software Architecture: The Hard Parts, ch. 9 and 10)

Once data is split, two questions dominate: who owns each piece of data, and how others reach it.

## Cross-chapter rules

1. **Writers own data.** Reading never confers ownership. Classify tables as single, joint or common ownership and resolve single cases first (`scripts/data_ownership.py`).
2. **Give common data a dedicated owner service** that others write to asynchronously or synchronously as needed.
3. **Resolve joint ownership deliberately.** Split the table, share a data domain, delegate to one owner, or consolidate services; each has costs in consistency, coupling or scale. Prefer the owner that represents the entity's main domain.
4. **One service, one schema.**
5. **Distributed writes lose ACID.** Choose an eventual consistency pattern: background sync only between independent systems, orchestrated request-based when consistency is needed before replying, event-based as the usual default with durable delivery and repair paths. Compensations are not rollbacks and can fail.
6. **Treat read access as a design decision.** Inter-service calls are simple but add latency and availability coupling; column replication is fast but drifts; replicated in-memory caches suit small, slow-changing data (`scripts/replicated_cache_sizing.py`); a shared data domain keeps integrity but widens the bounded context.
7. **Rule out options by hard constraints, then test the survivor for downsides.**

## Default workflow

1. Classify ownership from the service-to-table access map (ch09).
2. Validate ownership against real workflows and pick consistency patterns (ch09).
3. Choose a read-access pattern for each cross-service read (ch10).

<!-- BEGIN GENERATED: run tools/build_bundles.py to refresh -->

## References by chapter

Each link is one level deep; read only the files whose description matches the task.

### CH09: Data Ownership and Distributed Transactions

- [ch09-acid-vs-base-distributed-transactions.md](references/ch09-acid-vs-base-distributed-transactions.md): read when explaining which ACID guarantees a cross-service request loses, reasoning about soft state, or deciding whether atomicity is truly required.
- [ch09-data-ownership-scenarios.md](references/ch09-data-ownership-scenarios.md): read when assigning table owners, resolving joint or common ownership, choosing between split, data domain, delegate and consolidation, or picking the delegate.
- [ch09-eventual-consistency-patterns.md](references/ch09-eventual-consistency-patterns.md): read when choosing background sync, orchestrated request-based or event-based consistency, designing compensations, durable subscriptions or DLQ handling.

### CH10: Distributed Data Access

- [ch10-choosing-and-recording.md](references/ch10-choosing-and-recording.md): read when you must pick among the patterns, run a hypothesis-based trade-off session, work through an example, or draft the ADR.
- [ch10-data-access-patterns.md](references/ch10-data-access-patterns.md): read when you need the mechanics, strengths, weaknesses, fit and pitfalls of inter-service communication, column schema replication and the shared data domain.
- [ch10-replicated-caching.md](references/ch10-replicated-caching.md): read when replicated caching is a candidate, to compare caching models, check the four limiting trade-offs, size memory and plan startup and cloud configuration.

Merged section maps: [source-maps.md](references/source-maps.md).

## Scripts

Python 3 standard library only; run any script with `--help` for its arguments.

| Script | Purpose |
|---|---|
| `scripts/data_ownership.py` (ch09) | Classify table ownership after a data split (single, joint, common). |
| `scripts/replicated_cache_sizing.py` (ch10) | Replicated cache memory sizing for distributed data access. |

<!-- END GENERATED -->
