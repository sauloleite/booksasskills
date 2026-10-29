# Selecting a Database Type per Data Domain

## Contents
- The paradox of choice
- Seven evaluation characteristics
- Relational
- Aggregate orientation (concept)
- Key-value
- Sharding (concept)
- Document
- Schema-less is never truly schema-less
- Column family
- Graph
- NewSQL
- Cloud native
- Time series
- Quick selection guide
- Justifying a new database type
- Aggregate design: embed or reference
- Pitfalls

## The paradox of choice

Since roughly 2005 the number of database products has exploded. More choice means more trade-offs to analyze; every product optimizes for something. Software and data architects should choose jointly, per data domain, against the domain's actual needs. Never pick by popularity.

## Seven evaluation characteristics

Score every candidate type on these, qualitatively, for the domain at hand:

1. **Learning curve:** how quickly developers, modelers and DBAs become productive (SQL is near universal; a graph query language is niche).
2. **Data modeling ease:** how naturally the domain maps onto the model, and how easily the model changes later.
3. **Scalability / throughput:** horizontal, vertical or both, and how hard it is.
4. **Availability / partition tolerance:** support for HA topologies (replica sets, tunable consistency) and behavior under network partitions.
5. **Consistency:** ACID versus BASE / eventual consistency, and whether consistency is tunable per operation.
6. **Ecosystem:** language drivers, maturity, SQL support, community size, ease of hiring.
7. **Read/write priority:** where on the spectrum from read-optimized to write-optimized the engine sits (a slider, not a binary).

## Relational

Examples: PostgreSQL, Oracle, Microsoft SQL Server, MySQL; all available as managed cloud services.

- Learning: easiest; taught everywhere, documentation abundant.
- Modeling: very flexible; tables and rows feel natural, can emulate key-value, document and simple graph shapes, and new read patterns can be served by adding indexes. Arbitrary-depth graph traversal is the weak spot.
- Scalability: usually scaled up on bigger machines; replication and automatic failover are possible but complex to set up.
- Availability: favors consistency over availability and partition tolerance.
- Consistency: full ACID, which shields developers from low-level concurrency concerns. This is the main reason relational engines dominated for decades.
- Ecosystem: mature patterns for design and operations, many drivers, a large (vendor-fragmented) community; weaker on newer ideas such as reactive streaming APIs.
- Read/write: balanced; the model can be tuned toward either. SQL makes it easy to serve several read models over one write model.
- Look elsewhere when ACID is not needed at very high volume or traffic, or when the schema must be highly flexible (form-like or questionnaire data).

## Aggregate orientation (concept)

Aggregate (from Evans' Domain-Driven Design) means a cluster of related data handled as one unit, such as an order with its lines or a customer with dependent records. Aggregate-oriented storage keeps that unit together.

- Benefits: the whole unit can be copied across cluster nodes, so distribution is easy; fewer joins, so faster reads and writes; less impedance mismatch between application objects and storage.
- Costs: finding the right aggregate boundary is hard and changing it later is expensive; analysis across many aggregates is awkward.

All NoSQL families are built around aggregates, which is where their performance and clustered availability come from.

## Key-value

Examples: Amazon DynamoDB, Riak KV, Redis (persistence configurable), MemcacheDB (non-persistent). Background reading: Sadalage and Fowler, "NoSQL Distilled".

Think of a hash table: a key and an opaque value the database neither understands nor indexes. Operations are get, put and delete; no joins, filters or sorting.

- Learning: simple concept, but relational habits must be unlearned (you cannot ask for "all keys" casually). Aggregate design matters because changing it means rewriting all stored values.
- Modeling: the value can be any structure (arrays, maps, blobs). The client must already know the key, so pick keys the caller already holds, such as a cart ID, a login ID or an invoice number.
- Scalability: key lookups are very fast, enabling easy scaling and high throughput.
- Availability: varies widely by product and configuration; some allow per-request quorum settings (one node, a majority, all nodes). Never assume all key-value stores behave alike.
- Consistency: tunable per write as well; stronger consistency costs latency and, when all nodes must acknowledge, partition tolerance. A majority quorum is a sensible default compromise.
- Ecosystem: good driver support, active open source communities, often an HTTP API.
- Read/write: read-leaning. Typical uses: session storage, caching user preferences and profile properties, reference lookup codes.

## Sharding (concept)

Partitioning splits a table into sets on one server. Sharding is the distributed form: horizontal partitions placed on different nodes, which cooperate to locate or place data according to a shard key. Choosing the shard key is a lasting, hard-to-change design decision.

## Document

Examples: MongoDB, Couchbase, AWS DocumentDB.

Values are self-describing, hierarchical, human-readable documents (JSON, XML). Unlike key-value stores, the engine understands document structure and can index attributes, so queries can use fields other than the key.

- Learning: easy; teams already handle JSON and XML in APIs and front ends.
- Modeling: model aggregates (orders, tickets, profiles). More forgiving than key-value because inner parts can be indexed and queried.
- Scalability: scales well, but heavy indexing hurts, and growing data eventually forces sharding with its shard-key decision and complexity.
- Availability: configurable for HA; replicated clusters of sharded collections get complicated, though managed offerings ease it.
- Consistency: some products offer ACID within a collection, with edge cases; quorum-based tuning for reads and writes.
- Ecosystem: the most popular NoSQL family, with many drivers and tutorials.
- Read/write: read-leaning thanks to aggregates and secondary indexes.

## Schema-less is never truly schema-less

NoSQL entries can differ in attributes and repeat attribute names in every record. That flexibility changes change-control dynamics but does not remove schema: it is implicit, living in application code or elsewhere. Applications must cope with multiple schema versions coming back from the same store. Treat schema evolution as a real concern even in a document or key-value store.

## Column family

Examples: Apache Cassandra, ScyllaDB, Amazon SimpleDB. Also called wide-column or big-table databases.

Rows hold varying sets of name-value pairs (column key and column value) under a row key; some values are themselves maps of columns (super columns). Related data read together is grouped together.

- Learning: hard; rows with differing columns and super columns take time to absorb.
- Modeling: requires iterating on the row key design; SQL-like dialects such as CQL lower the barrier.
- Scalability: very high, horizontal for both reads and writes.
- Availability: clustered by nature, node loss is transparent to clients, and data is typically replicated three times by default; quorum tuning per operation.
- Consistency: tunable per operation, from a level where any single node accepting the write is enough (acceptable when some loss is tolerable under huge write volume) to requiring every replica. Higher levels reduce availability and partition tolerance.
- Ecosystem: active communities; SQL-like interfaces eased adoption.
- Read/write: write-optimized (commit log, memtables, SSTables) and good with sparse data. Ideal for very high write volumes.

## Graph

Examples: Neo4j, InfiniteGraph, TigerGraph.

Entities are nodes with properties; relationships are explicit, typed, directed edges stored as first-class objects, so traversal does not compute joins at query time.

- Direction matters: an edge can be traversed outgoing from one node or incoming at the other, and inconsistent direction choices make queries painful.
- Several relationship types may connect the same pair of nodes (an article "authored by" and "reviewed by" the same person).
- Changing a relationship type is expensive: every affected edge must be recreated, visiting both endpoint nodes. Design edge types carefully up front.
- Learning: steep. Modeling: hard; beginners overload edges with properties, while experienced modelers promote such properties into nodes with extra relationship types, which improves traversal.
- Scalability: read replicas scale reads; graphs are hard to shard, so write throughput depends on the product. Traversal is very fast because relationships are stored, not derived.
- Availability: distributed products with leader promotion exist.
- Consistency: many support ACID (Neo4j does).
- Ecosystem: built-in algorithms (shortest path such as Dijkstra, node similarity), Gremlin across many products, Cypher in Neo4j.
- Read/write: read-heavy workloads.

## NewSQL

Examples: VoltDB, ClustrixDB, SingleStore (formerly MemSQL), CockroachDB. The term was coined by Matthew Aslett for engines aiming at NoSQL-style scale while keeping relational features.

- Keep SQL and ACID, add automatic partitioning or sharding with multiple active nodes (unlike classic relational leader/follower setups).
- Learning: easy for relational teams, though DBaaS-only products can make hands-on learning harder.
- Modeling: familiar; the extra design dimension is shard placement, including geographic placement.
- Scalability and availability: high, from multiple active nodes; some survive disk, machine and data-center failures.
- Consistency: strong ACID.
- Ecosystem: many open source options; some are wire-compatible with existing relational engines, allowing drop-in replacement.
- Read/write: like relational, with geographic distribution and indexing used to favor reads or writes.

## Cloud native

Examples: Snowflake, AWS Redshift, Datomic, Azure Cosmos DB.

- Reduce operational burden, make cost visible, need no upfront investment, so experimentation is cheap.
- Learning: varies. Redshift feels relational; Snowflake has SQL but different storage and compute separation; Datomic models immutable atomic facts and uses Clojure heavily.
- Modeling: Datomic has no tables and no predeclared entity shape (only attribute definitions); Snowflake and Redshift target warehousing workloads. Know the modeling paradigm before choosing.
- Scalability: resources scale automatically for money; the trade-off is mostly price.
- Availability: Datomic in its production topology has no single point of failure; Snowflake replicates across regions and accounts; Redshift runs in one availability zone and needs multiple clusters for higher availability.
- Consistency: these products support ACID.
- Ecosystem: young, so experienced staff are scarce, and experimenting requires a cloud account. Less DBA toil, more developer learning.
- Read/write: Snowflake and Redshift lean toward reads (warehouse); Datomic handles both through multiple index orderings (entity-attribute-value-transaction first, and others).

## Time series

Examples: InfluxDB, kdb+, TimescaleDB, Amazon Timestream. Driven by IoT, observability, microservices telemetry and autonomous vehicles.

- Every point carries a timestamp; data is appended and almost never updated or deleted. Teams used to fixing errors with updates must unlearn that.
- Model changes over time with tags; one fact per tag (`status=open`, `device_id=88` rather than a combined `info=open.88`).
- Scalability: TimescaleDB inherits PostgreSQL scaling patterns; InfluxDB clusters split metadata nodes from data nodes.
- Availability: replication factor and node roles improve it in clustered products.
- Consistency: ACID when built on a relational engine, otherwise tunable levels (any, one, quorum), trading availability for consistency.
- Ecosystem: growing quickly; SQL-like dialects such as InfluxQL.
- Read/write: append-only writes, queries over time windows; read-heavy analysis. Not general purpose.

## Quick selection guide

| Domain need | Lean toward |
|---|---|
| Strong integrity, mixed reads and writes, team knows SQL | Relational |
| Relational semantics plus horizontal scale or multi-region | NewSQL |
| Lookup by known ID, sessions, caches, reference codes | Key-value |
| Self-contained aggregates rendered or exchanged as a whole, frequently changing shape | Document |
| Massive write volume, sparse wide rows, always-on clusters | Column family |
| Questions about paths, neighbors and relationship patterns | Graph |
| Measurements over time windows, append-only | Time series |
| Warehousing or minimal ops with pay-per-use | Cloud native |

## Justifying a new database type

The chapter's story shows a team that wants a document store for survey data and a data architect who refuses to add a new database type without justification; the team wins by finding the business pain (slow, costly survey changes) rather than arguing developer convenience. Practice:

- Translate the technical benefit into business outcomes: faster change turnaround, lower change cost, fewer abandoned change requests.
- Validate with the product owner that the pain is real and recurring.
- Involve the data architecture team as co-owners of the decision.
- Record the decision in an ADR covering context, decision, and consequences such as duplication and migration downtime.

## Aggregate design: embed or reference

Invented example: a field-inspection app stores checklist templates (template plus items) in a document store.

**Single aggregate (embed items in the template):**
- One read returns everything; the UI renders it directly.
- Items shared across templates are duplicated; changing a shared item means updating every template that contains it.

**Split aggregates (template holds item IDs plus ordering; items are separate documents):**
- Items are reusable and updated in one place.
- Retrieval needs multiple reads and assembly; rendering is harder.

Decision heuristics: embed when the number of parents is small, most changes add or remove children within one parent, and read or render simplicity dominates. Reference when children are widely shared, updated independently, or large. Whichever is chosen, document the duplication or assembly cost as a consequence, and plan for migration downtime when moving from relational tables.

```json
{ "templateId": "T-7", "title": "Boiler inspection",
  "items": [ { "itemId": "I-1", "text": "Pressure valve tested", "answer": "yes/no", "order": 1 } ] }
```

## Pitfalls

- Treating "NoSQL" as one category; key-value, document, column family and graph differ sharply.
- Assuming every key-value or document product has the same consistency and availability behavior.
- Choosing an aggregate boundary casually; changing it later means rewriting stored data.
- Using a time-series or warehouse engine as a general-purpose operational store.
- Adding a database type for developer convenience alone, without a business case or ops buy-in.
