## Contents

- Why data must be split
- Choosing a source of truth
- Why a shared database fails
- Database-per-service (default)
- Shared database within a broader bounded context
- Decision checklist
- Worked example

# Data Isolation and Data Topologies

## Why data must be split

- The bounded context includes the data. Using shared schemas or a shared database as an integration point is a form of coupling the style explicitly rejects.
- Microservices is the one style where breaking data apart is mandatory. Other distributed styles can get away with a single database or with domain-level databases; this one cannot, because of its fine granularity, its strict contexts and the sheer number of services.
- Upside: each team picks the storage technology that fits its service (budget, data shape, operational and processing needs) and can later swap it (for example relational to document) without touching other teams, since nobody else may depend on its internals.

## Choosing a source of truth

With data spread out, the relational habit of one authoritative store for every fact disappears. For each fact decide one of:

| Option | When it fits | Cost |
|---|---|---|
| One owning context; others call it | Fact changes often, consumers need current value | Runtime dependency and latency on every read |
| Replicate to consumers | Consumers need local reads at volume, slight staleness acceptable | Sync mechanism, eventual consistency |
| Cache in consumers | Reads dominate, fact changes rarely | Invalidation logic, stale reads |

Record the choice per fact; it is an architecture decision, not a coding detail.

## Why a shared database fails

Imagine dozens of services (the book uses sixty) on one database:

1. **Change control:** renaming a column or dropping a table forces coordinated change, test and release of every consuming service plus the schema migration. Practically unmanageable.
2. **Loss of the bounded context:** if every service shares the same structures, the physical context no longer exists. This is the most fundamental objection.
3. **Scalability and elasticity mismatch:** platforms add service instances automatically under load, but few databases scale out in step, causing slow responses and timeouts.
4. **Connection exhaustion:** each instance holds its own pool; as services and instances multiply, the database runs out of connections, adding waits and timeouts.
5. **Single point of failure:** a crash, maintenance window or backup takes the whole ecosystem down.

Domain-level databases (one per domain, shared by its services) are milder but suffer the same family of problems: scalability, connection management, availability and fault tolerance.

## Database-per-service (default)

Each service owns its tables in a separate database or schema. Others access the data only through the owner's contract.

Benefits:

- Context preserved; schema changes are local to the owner.
- Freedom to change database type without ripple effects.
- Strong scalability, elasticity, availability and fault tolerance, all of which degrade under shared topologies.
- Connection management stays simple and local.

## Shared database within a broader bounded context

Common, legitimate pressures: several services write the same table, or an outside service needs direct query access for performance. Then a small group may share one database or schema.

Rules:

- Keep the sharer count to roughly five or six at most. Beyond that, the shared-database problems return (change control, scaling, elasticity, availability, fault tolerance).
- Treat the group plus its database as one wider bounded context; draw it as such on diagrams.
- Typical justified cases: a payment area split by payment type (card, gift card, wallet, loyalty points) where all types touch the same payment records; a shipping area split by shipping method over shared shipment data.
- Trade-off accepted: schema changes now need coordinated change and deployment across the group, making them riskier and slower; scalability, elasticity and fault tolerance may also suffer depending on the case.

## Decision checklist

- Does any proposed design use one database across many services? Reject it and name the five failure modes above.
- For every shared schema: how many services share it, why, and is the group drawn as one context?
- For every fact read outside its owner: owner call, replica or cache, and what staleness is acceptable?
- Is any service merely a wrapper around one entity (the Entity Trap)?
- If sharing keeps spreading, would consolidating services remove the need?

## Worked example

A loyalty platform has Points Earn, Points Redeem, Points Expire and Points Transfer services, all mutating one balance ledger, plus a Reporting service that wants direct SQL access.

- The four points services form a broader context sharing the ledger schema (four sharers, within guideline). Document the coordinated-migration cost.
- Reporting stays outside: give it a replicated read model fed by ledger change events rather than a fifth or sixth direct connection, keeping the schema owned by the points group.
- If a seventh service later wants the ledger, prefer exposing an API from the points group or merging the requester into the group's context.
