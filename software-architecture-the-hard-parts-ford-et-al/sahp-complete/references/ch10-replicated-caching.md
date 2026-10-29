# Replicated In-Memory Caching for Data Access

## Contents
- Why caching counts as a data access pattern
- Three caching models compared
- How the pattern works
- Strengths
- The four limiting trade-offs
- Sizing procedure and examples
- Setup checklist
- Pitfalls

## Why caching counts as a data access pattern

Caching is usually framed as a speed trick (in-memory reads take nanoseconds versus milliseconds for a database). Here it doubles as a sharing mechanism: the data a reader needs is already present inside the reader process, so no request to the owner happens at read time.

## Three caching models compared

| Model | Where data lives | Shares across services? | Verdict for data access |
|---|---|---|---|
| Single in-memory | Private cache inside each service | No, caches never sync | Useless for sharing; only speeds up a service's own reads |
| Distributed | External cache server reached over a protocol | Yes | Poor fit: see below |
| Replicated | A copy inside every participating service, synced by the product | Yes | The intended model |

Why a distributed cache does not fix the problem:
- Availability: the reader now depends on the cache cluster instead of the owner, so fault tolerance does not improve.
- Ownership: any connected service can write to the shared cache, which breaks the owner's exclusive write right and can let cache and owner database diverge. Strict governance can contain this but it remains a risk.
- Latency: every read is still a network hop, slower than a local replica.

## How the pattern works

- The owner populates and is the sole writer of the cache.
- Each reader holds a read-only replica in its own memory.
- When the owner changes an entry, the product propagates the change asynchronously, behind the scenes, to every replica.
- Instances find each other through network broadcast and lookup.
- Not every caching product supports replication; verify with the vendor. Products known to support it include Hazelcast, Apache Ignite and Oracle Coherence.

## Strengths

- Fastest possible access to non-owned data (local memory, no explicit inter-service call).
- Fault tolerance: once a reader's replica is populated, the owner can go down and come back without affecting it; the caches reconnect on their own.
- Independent scaling of reader and owner.
- Data stays consistent (sync is handled by the product) and ownership is preserved (single writer).
- Note: the reader may need to combine cached fields with its own rows in application code, since there is no SQL join.

## The four limiting trade-offs

1. **Startup dependency.** The very first reader instance needs the owner running to load the cache; if the owner is absent, that instance waits. Later reader instances can copy the cache from a sibling reader, so they do not need the owner. After loading, the owner's availability no longer matters. Mitigate with startup ordering, readiness probes, or alerting when the first instance is blocked.
2. **Data volume.** Every instance holds the full cache. Total memory equals cache size times the number of instances holding it (owner and reader instances alike). Feasibility falls off quickly above roughly 500 MB per cache, especially with many instances. Example: 500 MB across 5 instances is 2.5 GB.
3. **Update rate.** If data changes faster than replication can propagate (the limit depends on data size and replication latency), replicas fall out of sync. Good for slow-changing reference data like descriptions or skill profiles; poor for volatile values like stock counts or live positions.
4. **Configuration in cloud and containers.** Peers discover each other via TCP/IP broadcast and lookup. A wide address range makes socket handshakes slow, and dynamic, uncontrolled IPs in cloud and container platforms make discovery awkward. Expect work on discovery plugins, network policies, firewalls and cross-zone traffic.

Also weigh, from the worked story: licensing cost for a commercial product and the team's lack of experience with the technique.

## Sizing procedure and examples

1. Cache only the fields the reader needs, not whole rows.
2. Estimate bytes per entry (fields plus key plus product overhead; pad generously).
3. Multiply by entry count for cache size.
4. Use the maximum expected instance count at peak for every service that holds the cache, owner included.
5. Total memory = cache size x total instances. Compare cache size against about 500 MB and total memory against available heap per pod.

Invented examples:
- Pricing tiers: 40,000 entries x 800 bytes = 32 MB; owner 2 instances, three reader services at 6 instances each, so 20 instances and 640 MB in total. Fine per instance, but check total cluster memory.
- Customer profiles for a recommender: 12 million entries x 2 KB = about 24 GB. Over the threshold by far; use a data domain, column replication or remote calls instead.
- In the chapter's story, a small expert-profile dataset (around a megabyte) across a handful of instances was trivially affordable.

Run `scripts/replicated_cache_sizing.py` to do this arithmetic and flag the threshold.

## Setup checklist

- Product supports replicated mode, and its license cost is acceptable.
- Owner is configured as the only writer; readers open the cache read-only.
- Discovery works in the target network (zones, firewalls, container networking).
- First-instance startup behavior defined and tested (owner down at boot).
- Change rate measured against replication latency.
- Proof of concept done if the team is new to the product.

## Pitfalls

- Using a distributed cache and calling it replicated.
- Counting only reader instances in memory math.
- Caching volatile data and then debugging stale reads.
- Letting readers write to their replica.
