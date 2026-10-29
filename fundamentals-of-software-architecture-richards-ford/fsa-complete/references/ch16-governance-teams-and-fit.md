## Contents
- Governance fitness functions
- Team topology alignment
- Characteristic profile (qualitative)
- Partitioning and architecture quanta
- When to choose the style: use cases
- Fit test and anti-signals
- Self-review questions

# Governance, Teams and Style Fit

## Governance fitness functions

The style has many moving parts, so continuous automated governance is not optional. Recommended fitness functions:

1. **Memory consumption.** Each processing-unit instance periodically publishes its current memory use, tagged only with the unit name (all instances of a unit hold the same replicated data, so one figure per unit name is representative). A second fitness function records instance counts per unit. Multiply to get total memory per unit across the cluster. Alert as per-instance memory nears the container limit.
2. **Synchronization time (cache to database).** Each unit emits the request ID and timestamp of a cache update; each data writer emits the same request ID and a timestamp after the database commit. A fitness function joins on request ID and subtracts. Report per unit (atomic) or as a system average (holistic). Watch the trend after architecture changes and compare against the business's freshness target.
3. **Data-pump bottlenecks.** Pumps are the backpressure point, because database writes are slower than cache writes. Track queue depth per pump queue, or aggregated. Growing depth lengthens sync time and raises the odds of data loss and collisions, especially at peak concurrency.
4. **Database read frequency.** Count requests to data readers. Rising reads erode scalability, elasticity and responsiveness.
5. **The driving characteristics themselves.** Measure scalability, elasticity and responsiveness directly, since they are the reason the style was chosen.

Sketch of the sync-time join (original, illustrative):

```python
def sync_times(cache_events, commit_events):
    """cache_events/commit_events: iterables of (request_id, unit, ts_ms)."""
    started = {rid: (unit, ts) for rid, unit, ts in cache_events}
    for rid, _writer, committed in commit_events:
        if rid in started:
            unit, ts = started[rid]
            yield unit, committed - ts

def summarize(pairs):
    by_unit = {}
    for unit, ms in pairs:
        by_unit.setdefault(unit, []).append(ms)
    return {u: sum(v) / len(v) for u, v in by_unit.items()}
```

Also alert on request IDs that never get a commit event: those are candidate lost updates.

## Team topology alignment

The style is technically partitioned (a single domain spans units, pumps, readers, writers, contracts, orchestrators and the database). It works best with teams organized around those technical areas (functionality, pumps, readers/writers, database), though cross-functional domain teams with specialists can still succeed.

| Team type | Fit | Why |
|---|---|---|
| Stream-aligned | Weakens as system grows | One domain change can touch units, pumps, readers, writers, cache contracts, orchestrators and the database, often shared with other teams. |
| Enabling | Good | Pumps, readers, writers and middleware are shared or cross-cutting; a team dedicated to, say, a writer and its pump can experiment and optimize independently of feature teams. |
| Complicated-subsystem | Good | The data grid and pumps can get very complex. Resolving collisions and asynchronous sync errors in writers is exactly the kind of work domain teams should be shielded from. |
| Platform | Good | Treat pumps and virtualized middleware as platform, exposed through common tools, services and APIs. |

## Characteristic profile (qualitative)

Strengths, all at the top of what any style offers:
- **Elasticity, scalability, performance.** These are the reasons to choose it. In-memory data and no database in the request path let it handle very large concurrent user counts (the authors speak of millions).
- The authors call it the only style that maximizes responsiveness, scalability and elasticity together.

Weaknesses:
- **Simplicity.** Very low. Caching plus an eventually consistent system of record means many interacting parts. Take particular care to prevent data loss on crash.
- **Testability.** The weakest point. Reproducing hundreds of thousands of concurrent users is costly and hard, so much high-volume testing ends up happening in production under real peaks, which puts normal operations at risk.
- **Cost.** Relatively high: overall complexity, caching-product licenses, and the compute needed for elastic headroom whether in cloud or on-prem.

Treat it as a specialized style: reach for it only when those three driving characteristics must be maximized.

## Partitioning and architecture quanta

- **Partitioning:** classified as technical. Separately deployed units hint at domain partitioning, but each domain is realized as several technical component types.
- **Quanta:** the number varies. The database is excluded from the quantum calculation because units do not talk to it synchronously. Quanta are therefore drawn around the user interfaces and the units they talk to. Units that communicate synchronously with each other, directly or via the processing grid, belong to the same quantum.

## When to choose the style: use cases

The authors cite two signals: sharp spikes in user or request volume, and throughput beyond about 10,000 concurrent users.

**Concert ticketing.** Traffic idles until a popular show goes on sale, then jumps from hundreds to many thousands of users within moments, and inventory sells out in minutes. A fixed and finite seat pool must be updated continuously under heavy contention; synchronous database transactions at that rate are impractical. Fit: the deployment manager spins up many units as load surges, and ideally pre-starts them just before the sale opens. Design note: the seat count is a contended counter, so evaluate a distributed cache or key routing for it (see the caching guidance).

**Online auctions.** Like ticketing, demand is unpredictable: nobody knows how many bidders will join or how many bids each price will draw. Units can be spun up as an auction heats up and removed as it ends. Dedicating a unit to each auction keeps bidding data consistent (it avoids cross-instance collisions on the same item). Asynchronous pumps forward bids to history, analytics and auditing with little latency impact on bidding.

Other domains with the same shape (invented examples for pattern matching): flash sales, limited product drops, game launch logins, exam registration windows, live-event voting.

## Fit test and anti-signals

Strong fit when most of these hold:
- Concurrency is extreme or highly variable, and elasticity is a top-three characteristic.
- Working data per unit is modest and mostly hot.
- The business accepts eventual consistency in the system of record.
- Budget and skills exist for caching products, messaging and production-grade load governance.

Anti-signals (prefer another style):
- Most requests need archived or cold data from the database.
- Units restart or redeploy constantly, causing frequent cold loads.
- Cache data per unit would be very large.
- Downstream consumers need near-real-time database freshness.
- Team is small, budget is tight, or the load is steady and moderate (a simpler style meets it).
- Strong transactional consistency is required across most data.

## Self-review questions (original)

1. Which named caches in the design are contended counters, and what cache model does each use?
2. If every instance of the busiest unit restarted at once, how long would the cold load take, and what would users see?
3. What is the peak-hour collision share for the most frequently updated cache, using measured RL?
4. Which team owns the pumps and writers, and is that team shielded from feature churn?
5. What staleness can the reporting and downstream consumers of the database tolerate, and which fitness function proves it?
6. Could a simpler style meet the load if it is steady rather than spiky?
