---
name: sahp-ch09-data-ownership-and-transactions
description: Assigns table ownership after a database split (single, common and joint ownership; table split, shared data domain, delegate and service consolidation) and manages distributed transactions with ACID vs BASE reasoning and three eventual consistency patterns (background sync, orchestrated request-based, event-based). Based on Chapter 9 of Ford, Richards, Sadalage and Dehghani's "Software Architecture: The Hard Parts". Use when deciding which service owns a table, resolving several services writing one table, or choosing how to keep service-owned data consistent.
---

# Data Ownership and Distributed Transactions (SAHP Chapter 9)

## Purpose

After a monolithic database is broken apart, the pieces have to work together again. This skill helps an agent decide which service owns each table, resolve tables that several services write, recognize when a business request has become a distributed transaction, and pick an eventual consistency pattern with its error handling. Every choice here trades consistency, performance, coupling and change cost against each other; present the trade-off, recommend, and record it as an ADR.

## Key decision rules

1. **Writers own, readers do not.** The service that writes a table owns it, however heavily others read it. Readers outside the owner's context use a read-access technique (replica, cache, remote call), not direct access.
2. **Classify every table by its writers:** one writer = single; a few related writers = joint; most or all services = common.
3. **Settle single ownership first** to clear the field, then tackle common and joint cases.
4. **Common ownership: create a dedicated owner service.** Others send it their data: fire-and-forget on a persistent queue when no reply is needed, synchronous call or request-reply when they need a key or confirmation. Do not put the table in a schema everyone shares.
5. **Joint ownership has four fixes**, each with a price:
   - *Table split*: each writer owns its columns; entity create and delete now require cross-service sync, forcing an availability vs consistency choice (CAP) and a sync vs async choice.
   - *Shared data domain*: writers share a schema; fast, consistent, no runtime dependency, but coordinated schema changes, wider tests, deployment risk and write governance. Always re-ask why the services are separate (scale, throughput, fault tolerance, code volatility).
   - *Delegate*: one owner applies writes for others. Prefer **primary domain priority** (the service doing most of the entity's CRUD) over operational characteristics priority, and offset non-owner performance with an in-memory or distributed cache. Costs: tight coupling; non-owners get slower, non-atomic writes and fail when the owner is down. Best when writes tolerate eventual consistency.
   - *Service consolidation*: merge the writers; regains ACID and speed, loses fine-grained scaling and fault isolation, raises test scope and deployment risk.
6. **One service, one schema.** Several services may share a schema; a service must not connect to several. A shared data domain that breaks this, or keeps absorbing tables, is drifting back to a monolithic database.
7. **Piggyback when possible.** If the non-owner already notifies the owner in the workflow, send the data in that message and make the receiver the delegate.
8. **Validate ownership against workflows.** Any request that writes tables of more than one owner is a distributed transaction and loses ACID at the request level: no request-wide atomicity, cross-service constraints, isolation of partial results or durability of the whole.
9. **Expect BASE:** basic availability, soft state (partial or unknown progress), eventual consistency whose speed depends on the pattern and on error handling.
10. **Pick the consistency pattern deliberately:**
    - *Background synchronization*: slowest and breaks bounded contexts (the job writes everyone's tables and duplicates their rules). Use only between closed, independent systems.
    - *Orchestrated request-based*: data agrees before the user gets an answer; slower, with complex error handling and usually compensations. Prefer a dedicated orchestrator over burdening a domain service. Run the step most likely to veto first.
    - *Event-based*: the common default; fast responses, fast parallel convergence, high decoupling. Requires durable subscribers or retained streams, retries, a dead letter queue, an automated repair step and human escalation.
11. **Compensation is not rollback.** It needs the data to restore state, must avoid side effects of re-creation, and can itself fail, which typically ends with a human repair.

## Default workflow

1. Build an access inventory: table, service, CRUD letters, columns written. Run the script below.
2. Assign single-ownership tables; list cross-context readers and their read-access needs.
3. For common tables, design the dedicated owner and its messaging.
4. For each joint table, walk the selection order: split if columns divide cleanly; consolidation or shared domain if atomic, high-throughput shared writes are essential; otherwise delegate by domain priority, piggybacking on existing messages.
5. Trace each business workflow across owners; mark distributed transactions and the ACID properties the business truly needs.
6. Choose an eventual consistency pattern per workflow and write its error playbook (retry, idempotency, compensation, DLQ, escalation, max soft-state time).
7. Record ADRs: technique chosen, alternatives rejected, consistency and coupling consequences.

## References

- [references/data-ownership-scenarios.md](references/data-ownership-scenarios.md): read when assigning table owners, resolving joint or common ownership, choosing between split, data domain, delegate and consolidation, or picking the delegate.
- [references/acid-vs-base-distributed-transactions.md](references/acid-vs-base-distributed-transactions.md): read when explaining which ACID guarantees a cross-service request loses, reasoning about soft state, or deciding whether atomicity is truly required.
- [references/eventual-consistency-patterns.md](references/eventual-consistency-patterns.md): read when choosing background sync, orchestrated request-based or event-based consistency, designing compensations, durable subscriptions or DLQ handling.
- [references/source-map.md](references/source-map.md): read to find which reference covers a given chapter section.

## Scripts

- `scripts/data_ownership.py`: run `python3 scripts/data_ownership.py access.csv [--domains domains.csv] [--json]` to classify each table as single, joint, common or unowned from a CSV of `table,service,access,columns` (access as CRUD letters, columns semicolon-separated). It names owners, lists readers needing read access, and for joint tables reports whether a table split is clean, the primary-domain delegate candidate, whether a shared data domain would put a service on two schemas, and cross-domain writers. Tune common ownership with `--common-ratio` (default 0.75) and `--common-min` (default 3). Treat output as a starting point; operational priorities and workflow needs still require judgment.
