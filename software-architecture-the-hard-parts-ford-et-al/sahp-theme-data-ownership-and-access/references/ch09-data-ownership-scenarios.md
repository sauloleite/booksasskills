# Assigning Table Ownership After a Data Split

## Contents

1. The core rule and its limits
2. Classifying each table (single, common, joint)
3. Single ownership playbook
4. Common ownership playbook
5. Joint ownership: four resolution techniques
   - Table split
   - Shared data domain
   - Delegate (primary domain priority vs operational characteristics priority)
   - Service consolidation
6. Choosing among the joint techniques
7. Validating the result against workflows
8. Lessons from the chapter's story
9. Worked example (invented)
10. Pitfalls checklist
11. Glossary

## 1. The core rule and its limits

Once a monolithic database has been broken apart, every table needs an owning service, and the owner plus its tables form a bounded context. The starting heuristic: **whoever writes to a table owns it.** Readers never determine ownership. A service that only queries a table gets no claim on it, no matter how often or how critically it reads; read access across contexts is solved separately (replication, caching, remote calls, data domains), not by moving ownership.

The heuristic is easy when exactly one service writes. It becomes hard when several services write, and hardest when nearly every service does. So the first job is to classify.

A related constraint from the chapter's database governance: several services may share one schema, but a single service should not connect to several databases or schemas. Keep this in mind whenever a proposed fix would make a service span two schemas.

## 2. Classifying each table

For every table, list which services insert, update or delete rows (writers) and which only read (readers). Then:

| Writers | Classification | Typical resolution |
|---|---|---|
| Exactly one service | Single ownership | Assign to that writer |
| A small number of services, usually inside one domain | Joint ownership | Table split, shared data domain, delegate, or consolidation |
| Most or all services (cross-cutting) | Common ownership | Dedicated owner service that everyone sends writes to |
| None (reference or seed data) | Not covered by the chapter | Treat as single ownership by whoever maintains it |

The difference between joint and common is breadth and domain locality. Joint ownership is a couple of related services in one domain fighting over a table (catalog and stock levels on a product table). Common ownership is a cross-cutting concern such as auditing, logging of user actions or notifications, where the writer list grows with every new service.

## 3. Single ownership playbook

1. Resolve these first. They are the easy cases, and clearing them out shrinks the problem so the joint and common cases stand out.
2. Place the table inside the writer's bounded context. When diagramming, draw the table within the service's boundary box; this visual convention communicates ownership at a glance.
3. List every reader that lives outside that context. Those readers lose direct database access and must use some read-access technique, which brings latency and fault-tolerance costs. Record that consequence explicitly.

## 4. Common ownership playbook

Putting a cross-cutting table in a shared schema that every service connects to looks simple but brings back all of the shared-database problems the decomposition was meant to remove: coordinated schema change, connection starvation, scaling limits and a shared failure point.

The preferred move is to **create a dedicated service that is the sole writer** (and usually the sole reader) of that table. Every other service hands its data to that service rather than writing directly.

Pick the communication style by whether the caller needs anything back:

- **No response needed** (audit entries, activity records): asynchronous fire-and-forget messages on a persistent queue. Callers do not wait, and persistence (the broker writing messages to disk) means messages survive a crash of the broker or of the owner service, giving guaranteed delivery.
- **Response needed** (a generated key, a confirmation number): a synchronous call such as REST or gRPC, or request-reply messaging, which behaves pseudo-synchronously.

If other services later need to read the common data, use read-access techniques rather than reopening direct table access.

## 5. Joint ownership: four resolution techniques

Joint ownership is the most frequent hard case. Each technique below converts or tolerates it with different costs.

### 5.1 Table split

Break the shared table into separate tables so each writer owns only the slice it is responsible for. The mechanics, taken from database refactoring practice: create the new table with the key plus the moved columns, back-fill it from the original table, then drop the moved columns from the original.

Illustrative sequence (generic SQL, invented names):

```sql
-- Move pricing columns out of a shared Course table
CREATE TABLE course_pricing (course_id VARCHAR(12) PRIMARY KEY,
                             list_price DECIMAL(10,2), currency CHAR(3));
INSERT INTO course_pricing (course_id, list_price, currency)
  SELECT course_id, list_price, currency FROM course;
ALTER TABLE course DROP COLUMN list_price;
ALTER TABLE course DROP COLUMN currency;
```

Result: two single-ownership tables. The catch is that the two tables still describe the same entity, so creating or deleting that entity now requires one owner to tell the other. That raises two linked decisions:

- **Availability versus consistency.** If the other service is down, does entity creation proceed anyway (availability, with a missing row to fix later) or fail (consistency, the two tables never diverge)? With network partitions unavoidable, the CAP theorem says you cannot have both.
- **Synchronous versus asynchronous.** If the creator must know the companion row exists, call synchronously: more consistent, slower. If not, fire-and-forget: faster, but consistency is weaker.

Strengths: keeps each bounded context tight and yields single ownership. Weaknesses: schema restructuring, no atomic transaction across the two tables, synchronization logic to build and maintain, possible duplication of data, and windows of inconsistency.

When it does not work: when writers modify the same columns or the row structure cannot be cleanly partitioned by responsibility (the story's survey table is such a case).

### 5.2 Shared data domain

Put the jointly written tables in a schema shared by the writing services, forming a wider bounded context that spans those services and that data. Draw the table outside both service boxes but inside a common boundary, signalling it belongs to neither alone.

Why choose it: neither service depends on the other at runtime. Each reads and writes directly, so access is fast, consistency is preserved by the database, and there is no throughput or availability coupling between the services.

Costs:

- Schema changes now require coordinating several services, which widens testing and raises deployment risk.
- Write governance gets harder. If only one service should change certain columns, you must enforce that with extra rules (grants, column-level permissions, review policy), because the database no longer guarantees it by structure.
- Repeated use slides back toward a monolithic database, especially when a service already sits in another shared schema and the only way to comply with the one-schema-per-service rule is to merge schemas.

Mandatory check: when the data is this intertwined, ask again whether these really need to be separate services. Legitimate reasons to keep them apart include different scalability or throughput needs, different fault-tolerance needs, and isolating code that changes at very different rates. If none apply, consolidation may be the honest answer.

### 5.3 Delegate

Make one service the sole owner (the delegate). Other writers send their updates to it, and it performs them on their behalf.

Choosing the delegate:

- **Primary domain priority.** The owner is the service that best represents the entity's domain, normally the one doing most of the entity's create, read, update and delete work (for a product table, the catalog service that adds and retires products).
- **Operational characteristics priority.** The owner is the service with the most demanding operational needs: performance, scalability, availability, throughput (for a product table, the stock service that adjusts counts on every sale).

Trade-off between the two: operational priority keeps the hottest, most volatile writes local, fast and strongly consistent, but it hands a service domain responsibilities (and error handling) that do not belong to it. The authors usually prefer **primary domain priority**, then mitigate the performance and fault-tolerance cost for the non-owner with caching (a replica cached in memory inside the non-owner, or a distributed cache).

Communication from non-owner to delegate:

- Synchronous: the non-owner waits; slower but consistent.
- Asynchronous: the non-owner is fast, but the data is only eventually consistent, and if the delegate fails while applying the update the non-owner has no assurance the change ever landed, which is an integrity risk, not just a timing one.

General profile: single ownership, good control over schema change, and the table structure is hidden behind the owner's API. On the other side: strong coupling between services, slow writes for non-owners, no atomic transaction for non-owner writes, and non-owners fail when the delegate is unavailable. Best fit: writes that do not need atomicity and can tolerate eventual consistency via asynchronous messages.

### 5.4 Service consolidation

Merge the jointly writing services into one coarser service so the table has a single owner again. This removes service-to-service dependency and the network hop, and it restores ACID transactions over the data with good performance.

Costs: a bigger service means a wider testing surface and higher deployment risk (any change can break unrelated behaviour), weaker fault isolation because everything fails together, and coarse scaling, where low-demand functionality (back-office catalog editing) must scale with high-demand functionality (stock updates).

## 6. Choosing among the joint techniques

Ask these in order:

1. **Can the table be partitioned by responsibility** (disjoint columns per writer, with only the key shared)? If yes and you can live with cross-service synchronization on entity create and delete, prefer **table split**.
2. **Do the writers need atomic, immediately consistent updates and high throughput on the shared data?** If yes, consider **consolidation**, or a **shared data domain** if there are real reasons (scale, fault tolerance, volatility) to keep separate deployables.
3. **Are non-owner writes infrequent, tolerant of eventual consistency, and expressible as requests to a domain owner?** If yes, use **delegate** with primary domain priority, and add caching for the non-owner's reads.
4. **Would a shared domain force a service onto two schemas** or pull more and more tables into one schema? If so, avoid it; prefer delegate or consolidation.
5. **Is the non-owner already sending the owner a message** in the workflow? If so, piggyback the data it used to write onto that message. This is a cheap, natural delegate.

Then record the decision as an ADR naming the technique, why the others were rejected, and the consistency and coupling consequences.

## 7. Validating the result against workflows

Ownership assignment is provisional until checked against real business workflows. For each workflow that writes to more than one table, note which owners participate and what the transaction requirements are. If a workflow needs atomicity across owners, you have created a distributed transaction: either accept eventual consistency with an explicit pattern, or revisit the boundaries (consolidate, shared domain). See also the eventual consistency patterns reference.

## 8. Lessons from the chapter's story

The framing story shows a development team and a data team arguing over a table one service reads constantly and another service maintains. The resolution reinforces that writes, not reads, determine ownership, and that data ownership cannot be settled by developers or DBAs alone. A second episode shows a jointly written table where splitting is impossible and a shared schema would push the team back toward a monolithic database; the team instead makes the downstream service the owner and passes the needed fields in the event the upstream service already emits.

## 9. Worked example (invented)

An online learning platform has these writers after the data split:

- `Enrollment` table: written only by Enrollment service. Readers: Progress, Certificates. Single ownership, owned by Enrollment. Progress and Certificates need a read-access technique.
- `ActivityLog` table: written by Enrollment, Progress, Payments, Courses, Certificates. Common ownership. Create an Activity service; others publish fire-and-forget messages to a persistent queue.
- `Course` table: Courses service creates and retires courses and edits descriptions; Pricing service updates price columns daily. Joint ownership with disjoint columns, so table split works: Pricing owns `course_pricing`. Course creation sends the new course id to Pricing asynchronously; a missing price row is tolerable for minutes, so availability wins.
- `Certificate` table: Progress service writes the completion date; Certificates service writes the issued certificate. The same rows and lifecycle, no clean split. Progress already emits a "course completed" event that Certificates consumes, so Certificates becomes the delegate and the completion date travels in the event payload.

## 10. Pitfalls checklist

- Granting ownership to the heaviest reader. Reads never confer ownership.
- Solving a cross-cutting table with a shared schema for everyone.
- Splitting a table and forgetting the create and delete synchronization path, or its failure behaviour when the peer is down.
- Choosing a shared data domain without re-asking whether the services should exist separately.
- A service connecting to two schemas to make a shared domain work.
- Delegate over asynchronous messaging with no confirmation or dead-letter handling, then assuming the write happened.
- Operational-priority delegation that leaves a service handling another domain's errors.
- Consolidating and then discovering that one part's scaling needs dominate the cost of the whole.

## 11. Glossary

- **Bounded context (data sense):** a service together with the tables it alone owns; nothing outside reaches the tables directly.
- **Single, joint, common ownership:** one writer; a few related writers; most or all services as writers.
- **Data domain:** a schema intentionally shared by a small set of services, forming a wider bounded context.
- **Delegate:** the single owning service that applies writes on behalf of others.
- **Primary domain priority / operational characteristics priority:** the two rules for picking the delegate.
- **Persistent queue / guaranteed delivery:** broker stores messages on disk, so they survive broker or consumer failure.
