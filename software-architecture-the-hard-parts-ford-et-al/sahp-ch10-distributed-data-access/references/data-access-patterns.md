# Data Access Patterns: Inter-service Calls, Column Replication, Data Domain

## Contents
- The problem shape
- Inter-service communication
- Column schema replication
- Shared data domain
- Quick comparison in words
- Glossary

## The problem shape

Once each service owns its tables, the owner is the only writer. Any other service that wants to display or compute with those fields has a read-access problem. Illustration used throughout: an Orders service shows each order line with the product name, but product names live in a Products service's table. In the monolith this was one join; now the reader must obtain the field some other way.

Capture before choosing: which fields, how often they are read, how many rows exist, how often they change, how fresh they must be, how sensitive they are, and the expected peak instance count of both services.

## Inter-service communication

**Mechanics.** The reader calls the owner (REST, gRPC, request/reply messaging) passing the keys and gets back the fields.

**Why teams pick it.** It is the most common and simplest approach; the owner keeps full control, there is no duplicated data, and data volume is irrelevant because nothing is stored on the reader side.

**Costs.**
- Latency stacks up in three layers. Network transmission each way, commonly tens to a few hundred milliseconds (book range about 30 to 300 ms). Security checks at the target endpoint, which vary widely with the auth scheme (about 20 to 400 ms). Data latency, because the owner must run its own query instead of the reader doing a join (about 10 to 50 ms). Worst cases approach a second for one lookup.
- Availability coupling: the reader is only as available as the owner. The services are coupled both statically (the call path) and semantically (meaning of the data).
- Scaling coupling: when the reader scales out for load, the owner must scale too, because every reader request becomes an owner request.
- A contract between the services must be defined and versioned.
- Changing protocol (REST to messaging) does not help; the caller still waits for data to come back.

**Fit.** Low read frequency, tolerant latency budgets, owner with high availability, or data too large or volatile to copy.

**Pitfalls.** Calling per item in a loop instead of batching keys; ignoring auth overhead in latency budgets; forgetting that the owner's capacity planning now includes the reader's traffic.

## Column schema replication

**Mechanics.** Add the needed columns to the reader's own table (for example a product_name column on order lines). The owner publishes create, update and delete changes, and the reader applies them.

**Strengths.** Reads are local and fast (ordinary joins within the reader's schema), the reader stays up when the owner is down, and the two services scale independently.

**Costs.**
- Synchronization machinery is mandatory. Use asynchronous channels (queue, topic, event stream) unless the business truly needs immediate transactional sync; async keeps the owner responsive and avoids an availability link.
- Consistency lag: the copy is stale until the change arrives, and lost or out-of-order events leave lasting divergence.
- Ownership drift: because the copy sits in the reader's table, the reader's code can update it. Those edits are invisible to the owner and create further inconsistency. Enforce read-only treatment by convention, tests, or database permissions.
- The services are still coupled through the sync channel and the event schema.

**Fit.** The authors generally steer away from it for routine lookups like the product name case. Consider it for data aggregation, reporting, or when the other patterns fail because of very large volume, very tight response times, or very high fault tolerance requirements.

**Pitfalls.** No reconciliation job to repair drift; replicating far more columns than needed; letting the copied column become a de facto second source of truth.

## Shared data domain

**Mechanics.** Move the owner's table and the reader's table into one shared schema that both services connect to. Reading becomes a plain join. This reuses the data domain idea from joint ownership, applied to reads.

**Strengths.**
- No runtime dependency between the services, so availability, responsiveness, throughput and scaling issues of remote calls vanish.
- Responsiveness is very good because the database does the join; no in-service aggregation is required (unlike stitching cache data together in code).
- Consistency and integrity are strong: nothing is copied, foreign keys can be enforced across the tables, and views, stored procedures and triggers can live in the domain. Keeping such constraints and artifacts is itself a valid reason to choose this pattern.
- No separate data-transfer contract is needed.

**Costs.**
- The table schema is the contract. Contracts in the other patterns hide table structure behind an API or cache shape, keeping changes inside one service. Here the bounded context widens, and altering a table may force coordinated changes in several services.
- Ownership becomes collective and needs governance (who approves schema changes, who may write which tables).
- Security exposure: each service connected to the schema can see all of its data. A tight bounded context with contracts can filter what leaves the owner; a shared schema cannot do that by default. Mitigate with per-service database roles or views if the platform allows.
- Generally discouraged in distributed architectures, so it needs explicit justification.

**Fit.** Strong consistency or referential integrity is required, the data is large, the owner is unreliable or slow, and the services belong to a closely related domain. Not viable when a service is already attached to another shared schema and cannot connect to a second, or when the services sit in clearly different business domains.

## Quick comparison in words

- Fastest reads: replicated cache (memory), then data domain and column replication (local SQL), with remote calls last.
- Best consistency: data domain (single copy); replicated cache is kept in sync by the product; column replication lags; remote calls always read current data.
- Best ownership protection: inter-service calls and replicated cache (owner is sole writer); weakest: column replication and data domain.
- Volume tolerance: remote calls, column replication and data domain handle large data; replicated cache does not.
- Contract stability: remote calls and caches insulate table changes; data domain exposes them.

## Glossary

- **Security latency**: time spent authenticating and authorizing a call at the target endpoint.
- **Data latency**: extra database round trips caused by splitting what used to be one join.
- **Broader bounded context**: a context enlarged to cover several services that share a schema, so change control spans all of them.
