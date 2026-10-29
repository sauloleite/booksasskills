## Contents

- Consistency models
- CAP theorem trade-offs
- Choosing consistency per data type
- Caching: why, strategies, when not to
- Caching and consistency
- Distributed-system warnings
- Planning for growth: indicators and review cadence
- Scaling options and their order
- Read replicas versus caching
- Ongoing maintenance
- Pitfalls
- Practice drills

# Consistency, Caching and Growth

## Consistency models

Transactions protect integrity inside one operation. Consistency models decide how quickly, and in what order, a change becomes visible across servers, regions and concurrent users. (ACID "consistency" means constraints hold after each commit; the models below are about visibility across copies.)

| Model | Guarantee | Cost | Example |
|---|---|---|---|
| Strong | All readers see the latest committed value, in commit order | May block or refuse operations to keep the guarantee (accuracy over availability) | Account balance in a single PostgreSQL primary |
| Eventual | Replicas converge after a delay | Readers may briefly disagree | A price change propagating across DynamoDB regions over seconds |
| Causal | Operations that depend on each other appear in dependency order; unrelated ones may arrive in any order | Middle ground in complexity | In a shared editor, a reply to an edit never shows before the edit |
| Session | A single user always sees their own writes during the session | Other users may see older data | An item you added stays in your cart even if global stock counts lag |

## CAP theorem trade-offs

With data spread across nodes, you cannot guarantee all three at once:

- **C**onsistency: every node returns the same data.
- **A**vailability: the system keeps answering when some nodes are down.
- **P**artition tolerance: the system keeps working when the network between nodes splits.

| Design | Gives up | Behavior under trouble | Fits | Technologies |
|---|---|---|---|---|
| CP | Availability | Rejects requests rather than serve possibly wrong data | Banking, inventory, financial ledgers | HBase, Google Spanner |
| AP | Immediate consistency | Stays up, serves possibly stale data | CDNs, social feeds, recommendations | DynamoDB, Cassandra |
| CA | Partition tolerance | Works only on one node or a tightly coupled cluster on a reliable network | Non-distributed RDBMS | Single-node MySQL or PostgreSQL |

Intuition for AP: an old post in a feed is far better than an empty feed.

## Choosing consistency per data type

Match the model to the business impact of being wrong, and mix models within one system.

| Use | When | Typical data |
|---|---|---|
| Strong | Wrong data is costly; brief unavailability is tolerable | Payments, stock decrements, authentication |
| Eventual | Small delays are harmless; uptime and speed matter more | Activity logs, recommendations, content feeds |
| Session | Each user must see a coherent personal view; global sync unnecessary | Carts, preferences, drafts |

The choice is revisited as requirements change; decide for current needs.

## Caching

**Why:** every database call pays network and disk latency (tens to hundreds of milliseconds). An in-memory cache can answer 10x to 100x faster or more and offloads the database. **Cost:** freshness problems plus one more component that can fail, go stale or eat memory. So the real question is whether the benefit justifies the complexity, which is why you define a caching strategy that states how the cache relates to the source of truth.

### Strategies

| Strategy | Read path | Write path | Best for | Trade-off |
|---|---|---|---|---|
| Cache-aside (lazy loading) | App checks cache; on miss reads DB and fills cache | App writes DB (and invalidates or updates cache) | Read-heavy, selective caching with fine control | More app code; first read of each key is slow |
| Write-through | Reads hit warm cache | Each write goes to DB and cache together | Cache must match DB; reads matter more than writes | Slower writes; may cache data nobody reads |
| Write-behind (write-back) | Reads hit cache | Write to cache now, persist to DB asynchronously | Write-heavy streams where losing some points is tolerable (activity, logs, metrics) | Data loss if cache dies before flush |

```python
def get_product(pid, cache, db, ttl=300):
    hit = cache.get(f"product:{pid}")
    if hit is not None:
        return hit
    row = db.fetch_product(pid)          # miss: go to source of truth
    cache.set(f"product:{pid}", row, ttl=ttl)
    return row

def rename_product(pid, name, cache, db):
    db.update_product_name(pid, name)    # write-through variant
    cache.set(f"product:{pid}", db.fetch_product(pid))
```

### When to cache: the four questions

1. How often does this data change?
2. What does a stale read cost the user or the business?
3. How expensive is the current query?
4. Is there a measured bottleneck right now?

Worked contrast (numbers invented in the spirit of the chapter):

- **Store catalog:** a product page joins details, stock, reviews and price at roughly 200 ms. With 1,000 concurrent shoppers each triggering a handful of queries, the database absorbs thousands of near-simultaneous reads, mostly for data that changes rarely. Serving those from memory in a few milliseconds frees the database for orders and payments. Cache it.
- **Trading screen:** quotes change several times per second. Even a 30-second eviction shows wrong prices that cost users money. Invalidation complexity and stale-data risk outweigh the speedup. Do not cache, or cache only immutable reference data.

## Caching and consistency

- Cache-aside with a TTL gives eventual consistency: entries expire and refresh.
- Write-through keeps cache and database strongly aligned, paid for in write latency.
- Write-behind accepts temporary divergence for speed.

Map to the business: financial data leans write-through; a personal blog is fine with cache-aside plus TTL.

## Distributed-system warnings

Once you run across several servers, expect: harder cache coherence, possible need for distributed transactions, explicit eventual-consistency patterns, and replication and sharding decisions. Your persistence strategy must evolve with scale; flag these to senior engineers rather than improvising.

## Planning for growth

No plan is perfect, but having none is worse. Thinking about the data strategy early saves effort later.

**Review cadence:** for a growing application, hold a monthly review with developers, DBAs and operations so issues are fixed before they are incidents.

**Indicators to watch:**

- Query latency over an agreed threshold
- Database CPU persistently above an agreed percentage
- Memory use trending steadily upward
- Rising user complaints about slow pages

## Scaling options and their order

| Option | What it does | When | Caveat |
|---|---|---|---|
| Vertical scaling | Bigger server (CPU, RAM) | Usually the first move: simple, no architecture change | Hardware ceiling |
| Read replicas | Copies serving reads, off-loading the primary | First consideration for read-heavy load | Replicas lag (eventual consistency) |
| Horizontal scaling | Spread data across servers | Vertical limit reached, or global/geographic distribution needed | Architectural change |
| Sharding | Partition data across databases by a shard key | Data cannot fit on one server | Most complex; shard-key choice is hard to undo |

Default order: scale up, add replicas for read pressure, then scale out, and shard only when volume forces it.

## Read replicas versus caching

| | Read replicas | Cache |
|---|---|---|
| What it holds | Full database copy kept in sync by replication | Hot subset, temporary copy |
| Consistency | Eventual, managed by the database | Whatever your invalidation logic achieves |
| App changes | Mostly none (route reads to replica) | App manages population and invalidation |
| Shines at | Read-heavy workloads, geographic distribution | Lowest latency on frequently hit items |

## Ongoing maintenance

- Archive old data so the working set stays small.
- Review indexes as query patterns shift; drop unused ones.
- Schedule recurring slow-query analysis and optimization.

## Pitfalls

- Adding a cache before measuring a bottleneck.
- Caching volatile, money-relevant data.
- Write-behind on data that must never be lost.
- Assuming a single global consistency level for every data type.
- Jumping to sharding when a bigger instance or a replica would do.

## Practice drills

- Pick a read-heavy endpoint, measure p50/p95 latency, add cache-aside with a TTL, and measure again; document the stale-data window you accepted.
- For an app you know, label each entity with strong, eventual or session consistency and justify each label in one sentence.
