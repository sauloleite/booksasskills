# Granularity Integrators

## Contents
- Role of integrators
- Integrator 1: database transactions
- Integrator 2: workflow and choreography
  - Fault tolerance
  - Performance and responsiveness (the request-mix rule)
  - Reliability and data integrity
- Integrator 3: shared code
- Integrator 4: data relationships
- Integrator checklist
- Pitfalls

## Role of integrators

Integrators push in the opposite direction from disintegrators: they justify merging services, or declining to split one. There are four: database transactions, workflow and choreography, shared code, and data relationships. When you present one to stakeholders, name the business quality it protects (atomic consistency, end-to-end resilience and latency, ease of maintenance, correct data) so it can be weighed against the agility, cost, uptime or security benefit claimed by the competing disintegrator.

## Integrator 1: database transactions

Monoliths and coarse domain services typically rely on a single local ACID transaction to keep related writes consistent. Splitting the functions across services with separate databases removes that guarantee for any operation that spans them.

Invented example: an Employee service and a separate Payroll Credentials service (bank account and tax ID, split out for access control). Onboarding an employee writes the employee record, commits, then calls the credentials service, which writes and commits separately. If the second call fails, an employee exists without payroll details. Recovery now requires compensating logic (delete the employee record, or mark it incomplete and retry), which is complex and itself error-prone. The book's later chapters on distributed transactions and transactional sagas cover these BASE-style alternatives.

Rule: if the business genuinely requires all-or-nothing behavior for an operation that crosses the proposed boundary, keep the functions in one service. Confirm the requirement with the business owner; do not assume it either way. Typical triggers are registration, account closure, order placement with payment capture, and any operation where a partial record is a compliance or customer-facing defect.

Note the interaction with security: splitting sensitive functions for access control (a disintegrator) and needing a single transaction across them (an integrator) is one of the most common head-on conflicts.

## Integrator 2: workflow and choreography

Inter-service calls (also called east-west traffic) are normal in distributed systems. As granularity becomes finer, the volume of such calls grows until it hurts three qualities.

### Fault tolerance

Synchronous call chains create transitive dependencies. If several services each depend, directly or indirectly, on one shared service, that one service becomes a single point of failure for all of them. A split made for fault tolerance gains nothing if the separated pieces must call each other to finish a request.

Rule: before splitting, check whether the pieces are tightly and synchronously coupled at runtime. If every business request needs all of them, the user-facing request still fails when any one fails, so fault tolerance is not actually improved. Consider keeping them together.

### Performance and responsiveness (the request-mix rule)

Every hop adds network and security latency. If a screen needs data assembled from five services via choreography, and each hop costs about 300 ms in network and security overhead, the user waits roughly 1.5 seconds of pure overhead. One service would eliminate it. (Orchestration, covered in the book's workflow chapter, is an alternative way to reduce this cost.)

Use a request-mix heuristic:

1. Classify the requests the candidate services will serve as **atomic** (handled entirely by one service) or **workflow** (needs two or more services).
2. If roughly 30 percent are workflow and 70 percent atomic, separate services are usually acceptable.
3. If the ratio is reversed (most requests cross services), lean toward merging.
4. Override by criticality: if a request that must be very fast falls into the workflow group, consider merging even when most traffic is atomic.
5. Relax for back-end processing where no user is waiting; latency matters less there.

This rule only applies when performance actually matters for the operations in question.

### Reliability and data integrity

When one business operation spans several services, each with its own commit, a mid-sequence failure leaves some services committed and others not. Worse, the committed data may already have been read by another process or announced via an event. Fixing it needs compensating transactions or explicit state tracking so the operation can resume, which is the messy territory of transactional sagas.

Rule: if data integrity and consistency are important or critical for the operation, consider putting the services back together.

## Integrator 3: shared code

Shared code is normal and necessary: logging, security helpers, formatters, converters and similar utilities. It is usually packaged as a compile-time library (JAR, gem, DLL, npm package, wheel). It influences granularity only in specific situations. (Code reuse patterns are covered in the book's Chapter 8.)

What does NOT justify merging: infrastructure cross-cutting code (monitoring, logging, audit trails, authn/authz helpers). Every service uses it; it is no argument for consolidation or for returning to a monolith.

What MAY justify merging (shared **domain** code, meaning business logic):

1. **High proportion of shared domain logic.** If a group of candidate services would share a domain library that is a large share of their combined code (the authors use more than 40 percent as an illustrative level), splitting leaves nearly half the logic in a library used only by that group. Consider one service that owns the shared logic, particularly if it changes often.
2. **Frequent shared-code changes.** Regardless of size, a frequently changing shared domain library forces frequent coordinated changes and deployments across every consumer. Library versioning can delay the coordination, but every consumer must eventually adopt the newest version.
3. **Changes that cannot be versioned.** Some changes must reach every consumer simultaneously, such as a defect fix or a business-rule change that must apply everywhere at once. If these happen often, merging simplifies life.

Symptom to watch: several services that must always be changed, tested and deployed together, or that drift out of sync because they run different versions of the same domain library.

## Integrator 4: data relationships

This driver assumes each service owns its data inside a bounded context; other services may not read or write that data directly. That ownership rule exists so a team can change its schema without breaking others. For example, if the owner drops a column, any outside service querying the table directly would break.

Procedure:

1. List each function in the candidate service and the tables it touches.
2. Mark **owner** for tables the function writes (writes imply reads) and **access** for tables it only reads.
3. Assign each table to the service that writes it under the proposed split.
4. For every read of a table owned by another service, record a cross-service data dependency. That read must now become a service call.
5. If two proposed services depend on each other's tables (bidirectional), or a service needs another's data on nearly every operation, merge them. Otherwise they will exchange constant calls, adding latency, fault-tolerance risk and scalability coupling.

Invented example: an inventory service has functions Receive Stock (writes `stock_lot`, `bin`), Reserve (writes `reservation`, reads `stock_lot`) and Replenish (writes `purchase_suggestion`, reads `reservation`). Splitting Receive Stock out is fine if Reserve can tolerate a call or a cached replica for lot data, but if Reserve also must read `purchase_suggestion` on every call, Reserve and Replenish depend on each other and should stay together.

The authors present this integrator last because it has the fewest trade-offs. Reorganizing table relationships just to enable a service split is rarely practical, although a migration occasionally does justify reshaping the data. Breaking apart data is treated in the book's Chapter 6.

The bundled script can do this analysis mechanically: `scripts/granularity_drivers.py datamap`.

## Integrator checklist

- [ ] Does any business operation require atomicity across the proposed boundary? Confirmed by the business?
- [ ] What share of requests are workflow versus atomic? Are any critical, latency-sensitive requests in the workflow share?
- [ ] Are the parts synchronously coupled at runtime so that one failing takes down the request?
- [ ] How many hops and what per-hop latency would a typical user request incur?
- [ ] What fraction of the combined code is shared domain logic? How often does it change? How often must a change hit everyone at once?
- [ ] After assigning tables to owners, which cross-service reads remain? Any bidirectional dependencies?

## Pitfalls

- Treating infrastructure libraries as a reason to merge.
- Assuming eventual consistency is acceptable without asking the business.
- Ignoring transitive call chains when claiming fault-tolerance gains.
- Using the request-mix percentage while ignoring the one critical request in the workflow group.
- Splitting services and then quietly letting them share tables, which reintroduces coupling without the transactional benefits.
