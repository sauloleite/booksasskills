## Contents
- Database topology options
- Cloud, on-prem and hybrid deployment
- Risk 1: frequent database reads
- Risk 2: synchronization delay and data loss
- Risk 3: high data volumes
- Risk 4: data collisions (with estimation model and worked examples)
- Risk review checklist

# Data Topologies, Deployment and Data Risks

Most of what goes wrong in space-based systems is about data: caching, background synchronization and eventual consistency.

## Database topology options

Because units never talk to the database synchronously, the database is mostly decoupled from transaction processing. That gives wide freedom over database type and topology. Pick based on how the backing database will be used:

| Situation | Leaning |
|---|---|
| Reporting and analytics are central, done directly against the store | Single monolithic database |
| Analytics run through a data mesh | Domain-partitioned databases |
| Sync throughput and per-domain consistency matter, and data splits cleanly by domain | Domain-partitioned databases (a single database can slow synchronization and so lengthen inconsistency windows) |
| Downstream systems consume the database for further processing | Single monolithic database |

Ask first: who reads the database, and how fresh must it be for them?

## Cloud, on-prem and hybrid deployment

- Everything (units, middleware, pumps, readers, writers, database) can run in the cloud or on-prem.
- Distinctive option: split it. Run units and middleware in a managed elastic cloud, keep physical databases on-prem. Asynchronous pumps and eventual consistency make this cross-boundary synchronization workable. Transactions get cloud elasticity; data management, reporting and analytics stay in a controlled on-prem environment. The authors present this hybrid as something other styles cannot easily do.
- Cloud elasticity fits the style's shape well, hybrid or not.

When an organization has data residency or security constraints but needs burst capacity, raise the hybrid topology as a candidate.

## Risk 1: frequent database reads

The style's benefits depend on serving transactional data from cache. Database reads should only happen when retrieving archived data (old orders, past statements) or cold-starting a unit with no live peers.

Red flags that the style is a poor fit:
- Data volume is so large that most of it must be archived and fetched from the database on demand.
- Units crash or are redeployed so often that cold starts are routine.

Governance: track the rate of requests to data readers.

## Risk 2: synchronization delay and data loss

- The database is always eventually consistent with the caches. Under the high concurrency this style targets, pumps commonly back up, which can delay database updates substantially. This is a serious risk when downstream consumers need fresh data quickly.
- Messages can be lost in the pump. Standard mitigations:
  - persisted queues (stored on disk, not only memory);
  - client-acknowledge mode on the writer side: the broker keeps the message until the writer confirms it finished, and hides the in-flight message from other writers meanwhile.
- Trade-off: both mitigations slow throughput and widen the inconsistency window. Choose them knowingly.
- See also general asynchronous data-loss prevention guidance from the event-driven chapter.

## Risk 3: high data volumes

All transactional data lives in unit memory and is duplicated per instance. Keep volumes modest, especially as instance counts grow, and watch cache size closely; a unit that exhausts memory crashes. Governance: a memory fitness function (see the governance reference).

## Risk 4: data collisions

**Definition.** With replicated caches in active/active mode (several instances may update the same item concurrently), a collision happens when instance B updates an item while A's earlier update to that same item is still replicating. Each copy then gets overwritten with the other's stale value, and both end up wrong.

**When.** Collisions become likely when the update rate on shared data outpaces replication latency (RL).

**Invented walk-through.** A seat-pool counter reads 200 on instances A and B. A sells 4 seats and writes 196. Before that reaches B, B sells 3 and writes 197. Replication then sets B to 196 and A to 197. Both are wrong; the correct value is 193.

**Estimation model.** Expected collisions per unit time:

```
collisions = N * UR^2 / S * RL
```
- N: instances sharing the named cache (directly proportional).
- UR: update rate (squared, so it dominates).
- S: cache size in rows (the only inverse factor: smaller caches mean more collisions because updates concentrate on fewer keys).
- RL: replication latency (directly proportional).

**Units warning.** The chapter labels UR and RL in milliseconds, but its worked numbers only come out when UR is in updates per second and RL is converted to seconds; the result is then collisions per second (multiply by 3600 for per hour). The bundled script uses that consistent reading.

Useful derived form: collisions as a share of updates equals N * UR * RL / S. That makes sensitivity obvious.

**Sensitivity, using the chapter's base case** (20 updates/s, 5 instances, 50,000 rows, 100 ms RL gives 72,000 updates and about 14.4 collisions per hour, roughly 0.02%, judged acceptable for replication):
- Cut RL to 1 ms: about 0.1 collisions per hour.
- Cut instances to 2: about 5.8 per hour.
- Shrink cache to 10,000 rows: about 72 per hour (0.1%).

**Practical guidance.**
- RL must come from production measurement (network type and physical distance between units drive it). Vendors rarely publish it. Use 100 ms for planning if you have nothing better.
- Update rates are not flat across a day. Find the peak rate and compute minimum, normal and peak scenarios, not just an average.
- If the peak collision share is unacceptable for the data in question, options are: switch that cache to distributed, reduce instances sharing the cache, route updates for a key to a single instance (for example, one unit per auction), or tighten RL (co-locate units).

Run:
```
python3 scripts/collision_rate.py -n 5 -s 50000 --scenario min=5 --scenario normal=20 --scenario peak=80 --threshold-pct 0.05
```

## Risk review checklist

- [ ] Is every hot read path served from cache? What fraction of requests hits a data reader?
- [ ] How often do all instances of a named cache go down together (crash, redeploy)?
- [ ] Per-instance cache size and projected growth versus container memory?
- [ ] Peak update rate per named cache and computed collision share?
- [ ] Is RL measured in production, or assumed?
- [ ] Pump queues persisted? Writers using client acknowledgment? Cost accepted?
- [ ] Who consumes the database downstream, and what staleness can they tolerate?
- [ ] Database topology chosen against reporting, mesh, sync throughput and downstream needs?
