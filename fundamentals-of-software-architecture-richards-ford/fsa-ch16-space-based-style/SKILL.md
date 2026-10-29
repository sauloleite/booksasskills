---
name: fsa-ch16-space-based-style
description: Guidance for evaluating, designing and governing space-based architectures (processing units, replicated in-memory data grids, data pumps, readers and writers, elastic deployment), based on Chapter 16 of Richards and Ford's "Fundamentals of Software Architecture". Use when a system faces extreme or spiky concurrency, when choosing replicated versus distributed caching, estimating data-collision risk, planning cache-to-database sync, defining fitness functions for memory and sync time, aligning teams, or deciding whether the style is worth its cost and complexity.
---

# Space-Based Architecture Style (FSA Chapter 16)

Space-based architecture removes the database from the synchronous request path. Each processing unit serves requests from an in-memory data grid that replicates to peer instances; changes reach the database later through asynchronous data pumps and data writers; data readers reload caches only when no live copy exists. A deployment manager adds and removes instances with load. The result maximizes elasticity, scalability and responsiveness at the price of complexity, testability and cost. This skill helps an agent decide whether the style fits, shape its data and caching design, quantify its risks and govern it.

## Key decision rules

1. **Choose it for load shape, not fashion.** Signals: sharp unpredictable spikes, or sustained concurrency above roughly 10,000 users, where the database would be the final bottleneck. Steady moderate load almost always has a simpler answer.
2. **It is a specialized style.** It is the one style that maximizes responsiveness, scalability and elasticity together; simplicity and testability are its weakest areas and cost is high. Name these trade-offs explicitly in any recommendation.
3. **Keep the database out of the hot path.** Database reads should occur only for archived data or a cold start (all instances of a named cache down or redeployed together). If most data must come from the archive, or units restart often, the style does not fit.
4. **Replicated cache is the default.** It is fastest and has no single point of failure. Move a cache to a distributed model when it exceeds about 100 MB per instance, is updated at a high rate, or holds contended values that must be correct (inventory, seats).
5. **Choose the cache model per processing unit.** Mixing models is expected; forcing one model everywhere is a compromise.
6. **Avoid near-caches here.** Unsynchronized front caches give different instances different hit rates, so responsiveness becomes uneven.
7. **Quantify collision risk before trusting active/active replication.** Collisions per second = N x UR^2 / S x RL (UR per second, RL in seconds); as a share of updates, N x UR x RL / S. Use measured production RL, or 100 ms for planning, and evaluate minimum, normal and peak rates.
8. **Pumps are always asynchronous; the database is always eventually consistent.** The instance that updated its cache owns sending the change. Use persisted queues and client-acknowledge writers to prevent loss, accepting slower sync.
9. **Prefer a data abstraction layer.** Readers and writers translate between cache contracts and database schema so database changes do not ripple into units. Send only changed fields plus key and action in pump contracts.
10. **Writer granularity is a trade-off.** One writer per domain means fewer components; one writer per pump aligns unit, pump and writer for better scalability and agility.
11. **Orchestrate with small orchestrator units**, one per major workflow, rather than a single central engine. Synchronously linked units share an architecture quantum; the database does not count toward quanta.
12. **Govern continuously** with fitness functions for per-unit memory (times instance count), cache-to-database sync time, pump queue depth, reader request frequency, and the driving characteristics themselves.
13. **Database topology follows its consumers.** Heavy direct reporting or downstream consumers favor one database; data mesh analytics or clean domain partitions with sync-throughput pressure favor domain databases. A cloud-processing, on-prem-data hybrid is a distinctive option.
14. **Teams:** the style is technically partitioned. Enabling, complicated-subsystem and platform teams fit well (pumps, writers, data grid, collisions); stream-aligned teams struggle as the system grows.

## Default workflow

1. Characterize load: peak concurrency, spike pattern, predictability (pre-start instances for scheduled spikes).
2. Run the fit test and anti-signals; if the fit is weak, recommend a simpler style and stop.
3. Decompose into processing units by functional area; list named caches per unit, with size, peak update rate and correctness sensitivity.
4. Pick a cache model per cache; run the collision script for replicated caches with contended keys.
5. Design pumps (contracts, actions, granularity), writers, readers, the reverse-pump cold-start path, and the abstraction layer.
6. Choose database topology and deployment (cloud, on-prem, hybrid).
7. Define fitness functions and thresholds; assign team ownership of technical areas.
8. Record decisions and trade-offs (cache model, writer granularity, sync tolerances) in ADRs, and walk the risk checklist.

## References

- [references/topology-and-components.md](references/topology-and-components.md): read when explaining or designing the parts (processing units, messaging grid, data grid replication mechanics, processing grid, deployment manager, pumps, writers, readers, abstraction layer).
- [references/caching-models.md](references/caching-models.md): read when choosing replicated, distributed or near-cache for a unit, or sizing cache memory.
- [references/data-risks-and-collisions.md](references/data-risks-and-collisions.md): read when assessing data risks, computing collision rates, picking a database topology, or proposing a hybrid cloud deployment.
- [references/governance-teams-and-fit.md](references/governance-teams-and-fit.md): read when defining fitness functions, aligning teams, describing the style's strengths and weaknesses, quanta, or judging fit against use cases.
- [references/source-map.md](references/source-map.md): read to trace a chapter section to the file that covers it.

## Scripts

Run `python3 scripts/collision_rate.py -n <instances> -s <cache_rows> --rate <updates_per_sec> [--rl-ms 100]` to compute expected collisions per hour and collision share for one replicated cache.

Run `python3 scripts/collision_rate.py -n 5 -s 50000 --scenario min=5 --scenario normal=20 --scenario peak=80 --threshold-pct 0.05` to compare minimum, normal and peak rates and flag scenarios above an acceptable collision percentage. Use `--help` for all options.
