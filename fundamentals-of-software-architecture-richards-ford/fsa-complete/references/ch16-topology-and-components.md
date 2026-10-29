## Contents
- Why the style exists
- Component inventory at a glance
- Processing units
- Virtualized middleware: messaging grid, data grid, processing grid, deployment manager
- How a replicated data grid keeps instances in sync
- Data pumps
- Data writers
- Data readers and the reverse pump
- Data abstraction layer versus data access layer
- Glossary

# Space-Based Topology and Components

## Why the style exists

A classic web stack (web tier, app tier, database) scales unevenly. Adding web servers is cheap, but each fix pushes the choke point one tier deeper, and the database is the hardest and most expensive tier to widen. Picture the capacity of the system as a funnel: broad at the web layer, narrowest at the database. Under heavy concurrent load the database ends up capping how many transactions can run at once, and bolting caches or database scaling products onto that shape only goes so far.

Space-based architecture attacks the funnel itself. It takes the database out of the synchronous request path. Working data lives in memory inside each processing unit, is replicated between the units that share it, and is written to the database later and asynchronously. Units are started and stopped as load rises and falls. The name comes from "tuple space", a parallel-computing idea in which processors coordinate through shared memory.

Use the style as a deliberate architectural answer to extreme or erratic concurrency, rather than trying to stretch a database-bound design.

## Component inventory at a glance

| Component | Role in one line | Required? |
|---|---|---|
| Processing unit | Runs application logic plus its in-memory data grid | Yes |
| Messaging grid | Routes incoming requests to an available unit, holds session state | Yes |
| Data grid | Replicates and synchronizes cached data between units | Yes |
| Deployment manager | Starts and tears down unit instances based on load | Yes |
| Processing grid | Orchestrates one business request across several unit types | Optional |
| Data pump | Asynchronously ships cache changes toward the database | Yes |
| Data writer | Consumes pump messages and applies them to the database | Yes |
| Data reader | Loads database data into caches when no live copy exists | Yes |

The first four plus the processing grid together are called the virtualized middleware. Architects may also park other cross-cutting infrastructure there (security, metrics collection for observability).

## Processing units

- Hold business logic, often including the web-facing parts as well as backend logic.
- Granularity varies: a small web app might be a single unit; a large one is split by functional area; units can also be small single-purpose services similar to microservices.
- Each unit embeds an in-memory data grid and a replication engine. Typical products named: Hazelcast, Apache Ignite, Oracle Coherence.
- A unit may hold several named caches, as many as its work requires.
- When a unit needs data it does not cache, it can either call another unit directly (choreography) or go through the processing grid (orchestration).

## Virtualized middleware

No single product covers all of it. Expect to assemble web servers, load balancers, caching products, service orchestrators and deployment tooling.

### Messaging grid
- Receives each request, decides which active unit should take it, and forwards it there.
- Routing can be as simple as round-robin or as smart as next-available (tracking which unit has the most headroom).
- Commonly a load-balancing web server such as HAProxy or Nginx.
- Consequence for design: because any unit may get any request, every instance of a unit must see the same data. That is what the data grid guarantees.

### Data grid
- Arguably the most important piece of the middleware.
- In most modern setups it lives entirely inside the processing units as a replicated in-memory cache. Only when the product needs an external controller, or when a distributed cache is used, does part of it sit in the middleware as a separate component.
- Replication between units is normally asynchronous and typically finishes in under 100 ms.

### Processing grid
- Optional. Needed only when one business request spans more than one type of processing unit (for example, ordering plus payment).
- Modern practice, especially with fine-grained units, favors several small orchestrator units, one per major workflow, over one big central orchestration engine. Example: an orchestrator unit for order placement coordinates order, payment and inventory units; separate orchestrators handle returns and restocking.

### Deployment manager
- Watches response times and user load, launches units as load climbs and removes them as it falls.
- It is the piece that delivers elasticity.
- Cloud platforms and container orchestrators such as Kubernetes usually provide this capability.
- Tip from the ticketing example: if a spike is predictable (a scheduled sale), pre-start instances shortly before the event rather than waiting for the load signal.

## How a replicated data grid keeps instances in sync

Units that declare a cache with the same name form a replication group. Mechanics an agent should be able to explain:

1. A new instance announces itself through the caching product, asking to join peers that host the same named cache.
2. Peers respond and connect. One of them, usually the first to connect, streams the current cache contents to the newcomer, so it starts in sync without touching the database.
3. Every instance keeps a membership list (address and port of each peer, itself included). The list grows as instances join and shrinks automatically when one dies.
4. When any instance writes to the cache, the product pushes that change asynchronously to every other member.

Implication: as long as at least one instance of a named cache is alive, new instances never need the database to warm up. Database reads become the exception, not the rule.

Illustrative sketch (pseudo-code, product neutral):

```python
grid = DataGrid.join(cluster="orders")          # discovers peers by name
profiles = grid.replicated_map("CustomerProfile")

def change_address(customer_id, new_addr):
    p = profiles.get(customer_id)
    p.bill_to = new_addr
    profiles.put(customer_id, p)                 # replicated to peers async
    pump.send({"entity": "CustomerProfile", "action": "update",
               "id": customer_id, "bill_to": new_addr})
```

## Data pumps

- A pump hands a data change to another processor that will update the database. They exist because units never read or write the database directly.
- Always asynchronous, so the cache and the database are eventually consistent.
- The instance that applied an update to its cache owns that update and is responsible for putting it on the pump.
- Usually built on messaging, which brings asynchrony, guaranteed delivery, persistence and FIFO ordering, and decouples units from writers: if a writer is down, units keep processing.
- Most systems have several pumps. Common alignments: one per domain or subdomain (customer, inventory); one per cache type (profile, wishlist); or one per unit domain that also hosts a larger general cache.
- Each pump has a contract: payload plus an action (add, update, delete). Formats can be JSON Schema, XML Schema, a typed object, or a map of name/value pairs.
- Update messages normally carry only the changed values plus the key and the action, not the whole record.

## Data writers

- Consume pump messages and apply them to the database.
- Can be services, applications, or data-hub products (Ab Initio is the example given).
- Two granularities:
  - **Domain-based writer**: one writer owns all database logic for a domain and listens to several pumps (for example, profile, wishlist, wallet and preference pumps all feeding one customer writer). Fewer components, more centralized logic.
  - **Dedicated writer per pump**: each unit class gets its own pump and writer. More components, but better scalability and agility because unit, pump and writer line up one to one.

## Data readers and the reverse pump

Readers fetch from the database and deliver to units. They are invoked in only three situations:
1. Every instance of a named cache has crashed.
2. Every instance of a named cache is being redeployed at once.
3. Archived data that is not in the cache must be retrieved.

Cold-start sequence after a full outage or redeploy:
1. Restarting instances compete for a lock on the cache. The winner becomes the temporary cache owner; the rest wait. (Details vary by product, but there is always one primary loader.)
2. The owner posts a load request on a queue.
3. A data reader picks it up, runs the queries, and posts results on a separate queue, the reverse data pump.
4. The owner fills its cache, releases the lock, peers synchronize from it, and processing begins.

As with writers, a reader may serve a whole domain or a single unit class; the per-unit-class option is seen more often. Implementation options match the writers.

## Data abstraction layer versus data access layer

Readers and writers together form a layer between caches and the database. Which kind matters:
- **Access layer**: units reach the database only through readers and writers, but their cache structures mirror the table schema, so they stay coupled to it.
- **Abstraction layer**: units speak in their own contracts; readers and writers translate. The cache schema can differ from the database schema.

The style generally uses the abstraction layer. Payoff: schema changes (column type changes, dropped columns or tables) can be absorbed by transformation logic in readers and writers, buffering the change until the unit caches are updated. Incremental database evolution does not ripple straight into processing units.

## Glossary

- **Named cache**: a cache identified by name; all units declaring the same name replicate with one another.
- **Member list**: each instance's view of the peers in its replication group.
- **Cache owner (of an update)**: the instance that applied the change and must publish it to the pump.
- **Temporary cache owner**: the instance that wins the lock during a cold start and loads data from the reader.
- **Reverse data pump**: the queue that carries reader results back to units.
- **Replication latency (RL)**: time for an update to reach every same-named cache.
