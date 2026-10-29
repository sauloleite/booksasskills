# ACID, Distributed Transactions and BASE

Use this when a business request touches data owned by more than one service and someone assumes it will still behave like a single database transaction. The authors insist that an architect cannot judge when to accept a distributed transaction without understanding precisely which ACID guarantees are lost.

## Contents

1. The four ACID properties, stated operationally
2. When a request becomes a distributed transaction
3. How each ACID property breaks across services
4. BASE: what you get instead
5. Diagnostic questions for an agent
6. Worked example (invented)

## 1. The four ACID properties, stated operationally

- **Atomicity:** every update inside the unit of work commits together or rolls back together, however many statements it contains. If the third of three inserts fails, the first two disappear.
- **Consistency:** at no point does the transaction leave the database violating its declared constraints. You cannot insert a child row whose parent does not exist; foreign keys hold during the transaction (some engines defer the check to commit, but it is still enforced).
- **Isolation:** other transactions cannot see data the current transaction has written but not yet committed.
- **Durability:** once commit reports success, the changes survive later crashes.

A single service with an ACID-capable database still has all four, but only for the tables it owns. Each service can commit and roll back its own part locally.

## 2. When a request becomes a distributed transaction

The moment one atomic business request (register a customer, place an order) requires database updates in more than one separately deployed service, the request as a whole is a distributed transaction. ACID survives at the service level only; the business request can no longer be ACID.

## 3. How each ACID property breaks across services

| Property | What happens across services |
|---|---|
| Atomicity | Each service commits its own piece. Atomicity is scoped to a service, not to the business request. |
| Consistency | If one participant fails, the others have already committed, so their tables disagree. Cross-service referential constraints cannot be declared or checked at each local commit. |
| Isolation | A participant's committed data is immediately visible to everyone else, even though the overall request has not finished (or may later be reversed). |
| Durability | Holds per service commit, but nothing guarantees the full set of changes for the request becomes permanent. |

Practical consequences an agent should raise:

- Readers can act on half-finished requests (an account visible before its billing record exists).
- Reversal must be coded as new forward operations (compensations), not database rollbacks.
- Integrity rules that used to live in foreign keys must move into application logic, events or reconciliation jobs.

## 4. BASE: what you get instead

The authors frame distributed transactions as BASE, the chemical opposite of ACID:

- **Basic availability:** every participant is expected to be up to take part. Asynchronous messaging relaxes this (a participant can be down and catch up later), but the price is a longer time until the whole request is consistent.
- **Soft state:** while the request is in progress its overall state is partial, and sometimes unknown. One participant has committed while others have not. If participants run in parallel, nobody can say what the overall state is until all report back. With asynchronous workflows, even the final state can be hard to determine.
- **Eventual consistency:** given enough time, every participant completes and the data agrees. How long that takes, and whether it is reached at all after failures, depends on the eventual consistency pattern chosen and on how errors are handled.

The architecture-level reason to accept BASE: distributed systems trade immediate consistency for better performance, scalability, elasticity, fault tolerance and availability. Accepting BASE is a deliberate trade, not a defect, but it must be designed for.

## 5. Diagnostic questions for an agent

1. Which tables does this business request write, and who owns each? If more than one owner: distributed transaction.
2. Which ACID property does the business actually need across those tables? Often only eventual agreement is needed; sometimes (money movement, stock reservation) it is not.
3. What may other requests observe mid-flight, and is that harmful? (Isolation loss.)
4. What happens if participant N fails after N-1 committed? Who repairs it, and how fast?
5. How long may the soft state last before users or downstream processes notice?
6. If true atomicity is required, should the participating services be consolidated or share a data domain instead?

## 6. Worked example (invented)

A clinic booking flow writes an appointment (Scheduling service), a pre-authorization (Insurance service) and a reminder schedule (Notifications service). In a single service with one database, a failed pre-authorization would roll back the appointment and the reminders. After decomposition:

- Scheduling commits the appointment; it is immediately visible to the front desk (no isolation).
- Insurance fails; the appointment now exists without authorization (no atomicity, no consistency).
- Notifications may already have scheduled a reminder for an appointment that will be cancelled (soft state).

Design response: decide whether a booked-but-unauthorized appointment is acceptable for minutes (eventual consistency with compensation or a status flag such as PENDING_AUTH), or whether booking and authorization belong in one service.
