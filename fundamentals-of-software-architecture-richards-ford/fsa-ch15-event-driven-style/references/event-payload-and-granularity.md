# Event Payload Design and Event Granularity

## Contents
- Two payload families
- Data-based payloads: gains and costs
- Stamp coupling and bandwidth math
- Key-based payloads: gains and costs
- Per-event decision procedure
- Anemic events and the payload spectrum
- Swarm of Gnats: granularity of the events themselves
- Review checklist and invented examples

## Two payload families

The payload is whatever data an event carries. Two poles:
- **Data-based**: everything a consumer could need travels in the event.
- **Key-based**: only a context identifier (order ID, customer ID); consumers look the rest up.

It is a per-event decision, not a system-wide one. Different event types in one system can and should use different payload styles.

## Data-based payloads

Gains:
- Consumers do not hit the database, which helps performance, responsiveness and scalability.
- The producer cannot know who listens or what they need; shipping everything guarantees each consumer has enough.
- Works where consumers cannot reach the owning database at all (strict bounded contexts, domain or per-service data topologies).

Costs:
1. **Multiple systems of record.** The database and in-flight events both hold the order. If the customer corrects the order (wrong quantity, wrong address) right after submitting, stale events still in flight carry old values. Event timing is hard to control, so the stale data might even be applied after the fresh data, overwriting the correction.
2. **Contract management.** A large payload needs a contract. Choices: JSON vs XML; strict (schema, GraphQL spec, class definition) vs loose (plain name-value pairs). Every choice creates static coupling between producer and all consumers.
3. **Versioning.** Strict contracts can carry a version (for example, a vendor MIME type in headers) for backward compatibility, but every consumer must apply the same versioning logic, which demands strong governance. A consumer that ignores the version breaks when the schema changes. Communicating versions and deprecations is hard when you do not even know all consumers. Net effect: data-based payloads are somewhat fragile.
4. **Stamp coupling** (below).

## Stamp coupling and bandwidth

Stamp coupling: many consumers share one big structure but each uses a different small slice. Changing any field (say, removing an address line) can force retest and redeploy of a consumer that never read it. Contract versioning defers this but does not remove it: once a version is retired or a breaking change lands, the consumer must be touched.

Bandwidth is the overlooked cost (it is one of the fallacies of distributed computing that bandwidth is unlimited; in the cloud it is often what you pay for). Calculation:

```
bandwidth_per_second = events_per_second * payload_size
```

Illustration with numbers of my own choosing (decimal units, 1 KB = 1,000 bytes): 800 events/s with a 300 KB payload is 240,000 KB/s (240 MB/s) to each subscribing consumer. If a consumer needs only two fields totalling 40 bytes, the same rate costs 32,000 bytes/s (32 KB/s). The ratio equals payload size over needed bytes, here 7,500x. Multiply by the number of subscribers for broker egress.

Consumer-driven contracts (each consumer gets a contract with only its fields) normally cure stamp coupling, but they fit poorly with broadcast because the producer does not know its consumers. This pushes many architects toward key-based payloads.

## Key-based payloads

Shape: a tiny loose JSON object, for example `{"invoice_id": "INV-77"}`.

Costs:
- Every subscriber queries the database, all at about the same moment because they run in parallel. This hurts responsiveness, performance and scalability and can swamp the database.
- If the needed data sits inside another processor's bounded context, the consumer cannot simply query it (and may resort to synchronous calls, which EDA should avoid).

Gains:
- One system of record, so mid-flow changes are handled cleanly; consumers read current data.
- The contract is trivial and rarely changes, so it is usually loose and schema-less; versioning and deprecation problems mostly disappear.
- No stamp coupling, minimal bandwidth, faster through the network and broker.

## Per-event decision procedure

The core tension: **scale and performance (favor data-based)** versus **contract stability, bandwidth and integrity (favor key-based)**. For each event type:

1. Will the underlying entity change while the flow is in progress? Yes leans key-based.
2. Is extreme throughput or latency critical for this flow? Yes leans data-based.
3. Can every likely consumer reach the owning data store without synchronous calls? No leans data-based.
4. How large is the full entity relative to what typical consumers use? A big gap leans key-based (or a trimmed payload).
5. How often does the entity's shape change? Often leans key-based.
6. Do consumers need to know *what changed* or *prior values*? Then pure key-based is insufficient (anemic); add a delta.

Record the choice per event type in an ADR or event catalog, with the deciding factor.

## Anemic events and the payload spectrum

An anemic event lacks the context consumers need to decide or act. Example: `profile_updated` carrying only a customer ID. Consumers cannot tell which fields changed, cannot tell whether they need to act at all, and cannot see old values (the database holds only the current state, so a lookup does not help).

Think of payloads as a spectrum:
- Key-only at one end: fine for creates and deletes, weak for updates.
- Full entity at the other end: stamp coupling and bandwidth costs.
- The middle, often the right answer for updates: key plus the changed fields with before and after values.

## Swarm of Gnats

Anemic events concern payload size. Swarm of Gnats concerns **how many** derived events a processor fires and how fine-grained they are.

Two failure directions:
- **Too coarse**: one `check_completed` event with an outcome flag inside. Every subscriber must open the payload to see if it applies, wasting processing and bandwidth (for example, card-locking and customer-alert processors both parsing every clean result). Fix: one event per distinct outcome (`fraud_detected`, `fraud_cleared`), so the event type itself routes the work.
- **Too fine** (the antipattern): one user action that changes three profile fields emits three separate events. The system fills with near-duplicate events about one action, downstream processors spawn their own small events in turn, and nobody can follow the flows anymore. Fix: emit one event for the whole action containing before and after values for every changed field.

Heuristic from the chapter: **design derived events around the outcome or state change of the processing, not around individual field changes or individual steps.** Split by outcome when consumers differ by outcome; merge when it is a single business action.

## Review checklist
- Each event type has an explicit payload style and a stated reason.
- No update event is key-only unless every consumer truly needs only "something changed".
- Payload sizes and rates are known; bandwidth per consumer is estimated.
- Unused fields per consumer are tracked (feeds stamp-coupling governance).
- Outcome events are split by outcome; single user actions produce one event.
- Versioning approach is uniform across all consumers of strict contracts.

## Invented examples
- **Shipment label printed**: created once, never edited, consumers own their data: key-based is fine.
- **Price tick**: very high rate, consumers need the price itself, value is immutable: data-based with a small payload.
- **Address change**: key plus old and new address; not full customer record.
