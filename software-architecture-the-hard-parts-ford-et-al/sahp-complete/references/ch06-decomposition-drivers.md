# Data Decomposition Drivers: Should This Database Be Split?

## Contents
- Why data is harder to split than code
- The balancing model
- Disintegrator 1: change control (and contract abstraction)
- Disintegrator 2: connection management (quotas and tuning)
- Disintegrator 3: scalability
- Disintegrator 4: fault tolerance
- Disintegrator 5: architectural quantum
- Disintegrator 6: database type optimization
- Integrator 1: data relationships
- Integrator 2: database transactions
- Building the justification for skeptical stakeholders
- Worked example
- Pitfalls

## Why data is harder to split than code

Splitting a database carries more risk than splitting application code. Data is usually the most valuable asset the business owns, so a botched migration hurts more, and tables are entangled with application logic in ways that hide natural seams. Treat the decision as its own trade-off analysis, not a by-product of having split the services.

Architecture style matters. Microservices expect each service to own its data inside a bounded context. Service-based architecture tolerates services sharing one database. Do not assume every distributed system must split its data.

The modularity vocabulary from code carries over to data:

| Code concept | Data equivalent |
|---|---|
| Component | Data domain |
| Class / source file | Table |
| Coupling between classes | Foreign keys, views, triggers, stored procedures, functions |

## The balancing model

Two opposing sets of forces decide data granularity:

- **Disintegrators** answer "why pull this data apart?" There are six: change control, connection management, scalability, fault tolerance, architectural quantum, database type optimization.
- **Integrators** answer "why keep (or put back) this data together?" There are two: data relationships and database transactions.

Neither list wins automatically. For each candidate split, state which disintegrators apply, which integrators apply, and which matters more to this business. Example framings: is controlling breaking schema changes worth losing a foreign key? Is isolating failures worth losing a materialized view? The answer sets both whether to split and how coarse the resulting schemas should be.

## Disintegrator 1: change control

**Question to ask:** how many separately deployed services break when one table changes?

- Breaking changes: dropping a table or column, renaming either, changing a column type. These break the SQL that reads or writes the table.
- Non-breaking changes: adding a table or a column usually leaves existing queries working.
- Relational stores feel this most, but other database types can suffer too.

Two costs grow with the number of services sharing the data:
1. **Coordination cost.** Every affected service must be modified, tested and released in lockstep with the schema change.
2. **Forgotten-consumer risk.** The bigger danger is the service nobody remembered. It keeps failing in production until someone patches and redeploys it. Impact analysis and regression testing mitigate this in small estates; with hundreds of services sharing one clustered database, tracking down every consumer becomes impractical.

**Remedy: bounded contexts around services plus the data they own.** "Own" means the service writes the data; read-only access is not ownership. A service outside the context must not query the tables directly; it asks the owning service (access techniques belong to later chapters on distributed data access).

**Contract abstraction.** The owning service returns data through a contract (JSON, XML, an object) that need not mirror its schema. Field names and types can differ from columns, so the schema can change underneath while the contract stays stable. If a column is dropped, only the owner changes immediately; it can keep emitting a sentinel (a far-future date, a zero) until the contract itself is versioned.

Invented illustration: a `loyalty` service stores `tier_code CHAR(1)` and `joined_on DATE`, but publishes:

```json
{ "memberId": "M-102", "tier": "GOLD", "memberSinceEpochMs": 1672531200000 }
```

Renaming `tier_code` or switching `joined_on` to a timestamp only touches the loyalty service's mapping layer.

## Disintegrator 2: connection management

**Question to ask:** can the database cope with the connections that many independently scaled services will open?

In a monolith the application server owns a single pool. In a distributed system every service instance carries its own pool, so connection demand multiplies by services times instances.

Arithmetic to run before migrating: total = sum over services of (pool size x instance count). An invented case: a monolith used a pool of 150. Split into 40 services, each with a pool of 8 and at least 2 instances, demand becomes 640 before any autoscaling. If a quarter of the services then run 6 instances, demand reaches 640 + 10 x 8 x 4 = 960.

**Symptom to look for first:** connection waits, the time a request spends waiting for a pooled connection. They often surface disguised as request timeouts or open circuit breakers, so check waits whenever those appear on a shared database.

**Governance: connection quotas.** A quota caps how many connections a service may hold in its pool; when exhausted, the service waits for one of its own connections to free up rather than starving others. Two allocation styles:

| Style | When | Strength | Weakness |
|---|---|---|---|
| Even distribution | First deployment, usage unknown | Simple | Wasteful: idle connections sit with quiet services while busy ones wait |
| Variable distribution | Once usage is measured | Efficient use of a fixed connection budget | Requires knowledge of each service's function and scaling profile |

Recommended path:
1. Start even.
2. Add fitness functions that stream per-service peak concurrent connections and wait events.
3. Keep quota values in an external configuration service so they can be changed without redeploying, manually or by a simple automated tuner.
4. Iterate: take connections from services whose peak usage sits well below quota and give them to services that report waits. Repeat until no service waits and each keeps some buffer.
5. Keep tracking how close total peak usage is to the database maximum and each service's buffer between quota and peak.

The script `connection_budget.py` automates steps 4 and 5.

## Disintegrator 3: scalability

**Question to ask:** will the database scale with the services in front of it? A system scales only as far as its least scalable part, and container or VM autoscaling does nothing for a single shared database.

Factors: connections, storage capacity, throughput, and query performance.

The quota trap: quotas that sum exactly to the database maximum stop being valid the moment services scale out, because each instance gets its own full quota. Multiply per-instance peak by instance count and compare with the maximum; demand of two or three times capacity is easy to reach, with waits, degraded latency and timeouts following.

Splitting into data domains, or a database per service, means each database serves fewer connections and less load, so both connection pressure and query load fall per database.

## Disintegrator 4: fault tolerance

**Question to ask:** how many services go dark when the database crashes or is down for maintenance?

Here fault tolerance means some parts keep running while another part fails. A shared database is a single point of failure: when it is down, every service is down regardless of how well the services themselves were split. Splitting the data confines an outage to the services that depend on the failed database. Use this driver when specific capabilities (checkout, ticket intake, order capture) must keep working while less critical ones (surveys, reporting) fail.

## Disintegrator 5: architectural quantum

**Question to ask:** is one shared database welding services with different architecture characteristics into a single quantum?

An architecture quantum is a unit that deploys independently, is functionally cohesive, is bound together by strong static coupling, and communicates synchronously inside itself. A shared database counts toward that static binding. If two services need, say, elastic scalability and high availability while three others need neither, they cannot become a separate quantum while all five share one database. Splitting the data lets each group, with its own data, form its own quantum with its own operational characteristics.

## Disintegrator 6: database type optimization

**Question to ask:** would some of this data be better served by a different kind of database?

A monolithic database forces every dataset into one engine. Example: lookup codes (currency codes, warehouse codes, product category codes) are really key-value pairs, awkward in relational form and a natural fit for a key-value store. Splitting first is what makes polyglot persistence possible. See the database type selection reference for choosing the target type.

## Integrator 1: data relationships

**Question to ask:** do foreign keys, triggers, views or stored procedures bind these tables tightly?

- These artifacts exist to protect integrity and consistency; they are not clutter.
- Data can also be logically related without a physical constraint (an order and its order-status history).
- Any artifact that crosses a proposed boundary must be removed when the data moves to a separate schema or database; artifacts inside one domain can stay.
- Removing every foreign key and view in a large database is rarely feasible, which is exactly why a strict database-per-service goal can be unrealistic. Data domains (coarser groupings) let most relationships survive.

## Integrator 2: database transactions

**Question to ask:** must several writes commit or roll back as one unit to keep the data correct?

Inside one database or schema, a service can wrap writes to several tables in a single ACID transaction. Once those tables live in different schemas or databases owned by different services, the writes travel over remote calls and one can commit while another fails, leaving inconsistent data. Distributed transaction management and sagas are handled in later chapters; at this stage, treat a strong need for atomic multi-table writes as a reason to keep those tables together.

## Building the justification for skeptical stakeholders

The chapter's story shows an architect who must win over a data architect who owns the databases and resists splitting. Lessons, phrased as practice:

- Involve the database team from the start; excluding them creates resistance before any technical argument is heard.
- Bring evidence, not opinions: logs showing one workload (reporting queries using parallel threads) exhausting connections and freezing another (ticket handling); projected connection counts from planned services, instance counts and growth forecasts; outage history tied to the shared database.
- Map each piece of evidence to a named disintegrator.
- Pre-empt integrator objections: explain that data domains keep most foreign keys and views, and commit that no service will connect to more than one schema.

## Worked example (invented)

A clinic-booking platform shares one database across 18 services.

| Evidence | Driver |
|---|---|
| Nightly analytics queries cause booking timeouts | Connection management, scalability |
| Booking must stay up when the newsletter module's DB is patched | Fault tolerance |
| Booking needs elasticity; billing does not | Architectural quantum |
| Practitioner availability is a graph of rooms, people, specialties | Database type optimization |
| `invoice` and `invoice_line` must be written atomically | Database transactions (keep together) |
| `appointment` has FKs to `patient` and `room` | Data relationships (weigh) |

Outcome: split analytics, newsletter and booking into separate domains; keep `invoice` and `invoice_line` in one billing domain; decide on the `appointment`-to-`patient` FK by whether booking's change isolation outweighs referential integrity (usually yes, enforced instead by the booking service validating patient IDs through the patient service).

## Pitfalls

- Splitting data simply because services were split, without a named disintegrator.
- Ignoring integrators and then discovering that critical invariants relied on foreign keys or atomic commits.
- Treating quotas as static: they must be re-tuned as instance counts change.
- Assuming a non-relational database is free of change-control problems; implicit schemas still break readers.
- Letting a consumer read another domain's tables "just this once"; it defeats the contract abstraction.
