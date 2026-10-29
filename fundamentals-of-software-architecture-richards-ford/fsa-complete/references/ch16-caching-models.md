# Caching Models: Replicated, Distributed, Near-Cache

The style removes direct database reads and writes from transaction processing; that is how it gets its scalability, elasticity and performance. The cache model is therefore the central design choice. Replicated caching is the default; distributed caching is the main alternative.

## Replicated caching (default)

- Each unit holds a full in-memory copy of each named cache it uses; the grid keeps copies in sync.
- Very fast (local memory reads).
- Highly fault tolerant: no central cache server, so no single point of failure. Caveat: a few products still rely on an external replication controller, though the trend is away from that.

When it breaks down:
1. **Large data volume.** Once a cache grows beyond roughly 100 MB per unit, every instance carries that weight. Containers and VMs have bounded memory, so fewer instances fit, which undercuts the elasticity and scalability the style exists for.
2. **High update frequency.** If updates arrive faster than the replication engine can propagate them, copies drift apart and consistency suffers (see data collisions in the risk reference).

## Distributed caching

- Data sits in an external, central cache service. Units hold nothing locally and fetch over a (usually proprietary) protocol.
- Strong consistency: one copy, no replication to reconcile.
- Slower: every access is a remote call, adding latency.
- Weaker fault tolerance: if the cache server fails, no unit can read or write. Mirroring the server reduces the risk, but an abrupt primary failure can lose updates that had not reached the mirror, which reintroduces inconsistency.

## Choosing between them

When the cache is small (under about 100 MB) and the update rate is within what replication can sustain, both models work and the choice is a priority call: consistency (distributed) versus speed and resilience (replicated). Neither model wins on both axes, ever.

Signals pointing toward replicated: the goal is speed; each copy stays well under 100 MB; data is read-mostly; losing a central cache server would be unacceptable.

Signals pointing toward distributed: correctness of shared values beats latency; the data set is large (several hundred MB per copy is clearly past the replicated comfort zone); values churn constantly, often on the same keys; a cache-server outage is tolerable or mitigated by mirroring.

The type of data often settles it. Counts that must never be wrong under contention (inventory, seats, balances) push toward distributed. Lookup data that rarely changes (codes, descriptions, name/value settings) pushes toward replicated.

### Mix models per processing unit

Do not force one model across the whole system. Each unit can choose. Example: the inventory unit uses a distributed cache for consistency while the customer-profile unit uses a replicated cache for speed and resilience. Treat a uniform model as a compromise to avoid, not a simplification to aim for.

The 100 MB figure is a heuristic, not a hard limit; test it against your container memory budget and target instance count. Rough per-unit check: cache size times instance count is the cluster-wide memory cost of replication, and per-instance cache plus application footprint must fit the container limit with headroom.

## Near-cache (hybrid) and why to avoid it here

Structure: a distributed cache acts as the full backing cache; each unit keeps a smaller front cache holding a subset. Front caches evict to make room using one of three policies:
- most recently used items kept,
- most frequently used items kept,
- random replacement (reasonable when there is no data analysis justifying recency or frequency).

Front caches stay in sync with the backing cache but not with each other. Two units serving the same data context (say, one customer) may hold different subsets, so the same request can be fast on one instance and slow on another. That uneven responsiveness is why the authors advise against near-caches in space-based systems. If an agent sees a near-cache proposed, flag the inconsistency risk and ask whether a per-unit choice between plain replicated and plain distributed would serve better.

## Quick decision procedure

1. For each named cache, estimate size per instance, write rate at peak, and how harmful a stale or conflicting value would be.
2. If size is well above 100 MB, or conflicting values are unacceptable (contended counters), choose distributed and plan mirroring for failover.
3. Else if write rate is high on shared keys, compute the collision estimate (script in this skill). If the collision percentage is unacceptable, choose distributed or reduce contention (fewer instances, partition keys, dedicated units).
4. Else choose replicated.
5. Record the choice per cache, with the measured or assumed replication latency, in an ADR.

## Pitfalls

- Assuming "in memory" means "free": replicated memory multiplies with instance count.
- Using one cache model everywhere because it is simpler to explain.
- Choosing distributed for consistency and forgetting it is now a single point of failure.
- Adopting a near-cache to "get both" and getting uneven latency instead.
