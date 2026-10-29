# Topology and Event Semantics (choreographed EDA)

## Contents
- Request-based versus event-based thinking
- The four topology parts and how a flow runs
- Broker layout
- Events versus messages (with a classification test)
- Derived events, extensible events, poison events
- Asynchronous capabilities: responsiveness vs performance, quantum detangling
- Broadcast and semantic decoupling
- Worked example: designing a choreographed flow
- Glossary

## Request-based versus event-based thinking

Two mental models compete when designing a system:

- **Request model.** Something (UI, API layer, orchestration service, integration hub) receives a request and routes it, deterministically and synchronously, to processors that read or update data. Example: "show my last six months of orders". The caller wants data in a known context.
- **Event model.** Something has happened in the world and the system must react. Example: a bid lands on an auction item; the system must compare it with concurrent bids and pick the current leader. Nobody is asking for data; a fact has occurred.

Ask of each business interaction: "is this a question or command with a known path, or a fact the business must react to?" The answer drives the style choice (see the style-fit reference for the full decision rule).

The authors treat EDA as a full architecture style, not merely a pattern: whole systems can be built from it alone, though it also embeds inside microservices or space-based systems as a hybrid.

## The four topology parts

1. **Initiating event**: the trigger that starts an entire flow. Can be trivial (a bid) or rich (an employee marriage that ripples through a benefits system).
2. **Event broker**: hosts the event channels. The initiating event goes into a channel there.
3. **Event processor** (commonly just "service"): exactly one processor accepts the initiating event, does one specific task, then announces what it did.
4. **Derived event**: the announcement. Other processors subscribe, do their own task, and announce in turn. The flow ends only when every processor is idle and no derived events remain.

Mental model: a relay race. Once a processor hands the baton on (publishes its derived event), it is finished with that flow and free for other work. Each processor scales on its own according to its load or backlog.

### Broker layout
- Brokers are usually **federated**: several clustered instances, one per domain, each holding every channel used by that domain's flows.
- Because choreographed EDA is fire-and-forget broadcast, channels are publish/subscribe: topics, AMQP topic exchanges, or streams.

## Events versus messages

Treat these as different things, not synonyms. Four tests:

| Test | Event | Message |
|---|---|---|
| Tense / intent | Reports a past fact ("order placed") | Asks for something to be done or answered ("apply payment", "give shipping options") |
| Reply expected | Usually none | Usually yes |
| Audience | Many receivers (one-to-many, pub/sub) | One receiver type (point-to-point) |
| Physical channel | Topic, stream, notification service | Queue or messaging service |

Key rule: **broadcasting a command does not make it an event.** A teacher telling a whole class to open their books is still a command. Likewise, a directed instruction that others happen to overhear is still a message. Classify by intent first, audience second.

Practical classification drill an agent can run on proposed channel names:
- Imperative verb at the front (`ship_order`, `calculate_tax`) = message. Belongs on a queue, likely in a mediated flow or request-reply.
- Past-participle fact (`order_shipped`, `tax_calculated`) = event. Belongs on a topic.
- If a "fact" name actually encodes what the receiver must do (`inventory_needs_decrement`), it is a disguised command; rename it to the fact or move it to a queue.

Choreographed EDA mostly uses events. Messages appear when a processor needs data from another (request-reply) and throughout the mediator topology, which drives order with commands.

## Derived events

- Derived events are essential, not incidental. One processor may emit several, one per meaningful outcome.
- Example shape: a card charge fans out to a fraud check (outcomes: fraud found / clean) and a credit check (outcomes: within limit, near limit, limit exceeded). Each outcome is its own derived event because different downstream processors care about different outcomes (notification, decline, a marketing processor that offers a higher limit).
- An outcome event may carry useful extra data (for example, remaining credit) for consumers that might care.
- Balance this against flooding the system with tiny events (Swarm of Gnats; see the payload reference).

### Extensible derived events (the "always advertise" rule)
- Every processor should publish what it did, even when nobody currently listens.
- An event with no subscribers is an **extensibility hook**, not waste. On a broker it simply evaporates; on a stream it is ignored.
- Payoff: when the business later wants, say, analytics on every customer email sent, a new processor subscribes to the existing "email sent" event. No existing processor changes.

### Poison events
- A poison event is a derived event that circulates forever: A reacts to B's event and emits something B reacts to, which emits something A reacts to, and so on.
- These arise easily in choreography. Classic setup: inventory adjusts stock, warehouse reorders, replenishment event comes back to inventory. If inventory then emitted another "inventory adjusted" that warehouse also consumed, you would have a loop.
- Guard: for any processor that consumes an event downstream of its own output, make sure that handler does not emit an event that re-enters the same chain. Map event-type cycles explicitly (the bundled script does this).

## Asynchronous capabilities

EDA relies on asynchrony both for fire-and-forget and for request-reply.

### Responsiveness is not performance
- **Responsiveness**: how soon the user hears back.
- **Performance**: how long the end-to-end work takes.
- Making a slow (multi-second) validation asynchronous cuts the user-perceived wait to an acknowledgment time of a few tens of milliseconds, while total processing time barely changes. That is a responsiveness gain only.
- Optimizing the slow service itself (parallel validators, caching) while keeping a synchronous call is a performance gain.
- Price of async: the user gets an acknowledgment and a promise, not a guarantee. You need a way to report later failures (for example, notify a registered user that their post was rejected and how to fix it). Where no such channel exists (anonymous users, or a stock purchase with no later notification path), the error-handling problem becomes serious; see the reliability reference.
- Decision question: "does the user need anything back besides an acknowledgment?" If not, do not make them wait.

### Detangling architecture quanta
- Two independently deployable systems joined by a synchronous call become one quantum (they share availability, responsiveness and scalability). The book names this antipattern Dynamic Quantum Entanglement.
- Symptoms: caller blocked while callee is down; caller slowed when callee is slow; caller cannot scale unless callee also scales.
- Fix: replace the call with an async send, and return any confirmation (such as an ID) on a separate async channel. The caller keeps accepting work while the callee is down, trusting confirmations to arrive later. Result: two quanta, each with its own characteristics.

## Broadcast and semantic decoupling

- A publisher does not know who (if anyone) consumes its event or what they do with it.
- This underpins eventual consistency and complex event processing. Example: a market price tick consumed by analytics, buy logic and sell logic, none of which the price publisher knows about.
- **Semantic decoupling**: the producer has no dependency on the actions consumers take.

## Worked example (invented): hotel booking choreography

Initiating event: guest submits a booking.
- Reservation processor stores the hold, returns a booking reference to the guest, emits `booking_held`.
- Payment, Loyalty-points and Housekeeping-forecast processors each subscribe to `booking_held` and run in parallel.
- Payment emits `deposit_captured` or `deposit_declined` (two outcome events, not one event with a status flag).
- Notification listens to `deposit_declined` (ask for another card) and to `booking_confirmed`.
- Loyalty emits `points_accrued` that no one consumes yet: an extensible hook for a future marketing feature.
- Loop check: Housekeeping emits `forecast_updated`; ensure Reservation never reacts to it with something Housekeeping consumes.

## Glossary
- **Federated broker**: per-domain clustered broker instances.
- **Derived event**: any event produced by a processor in response to another event.
- **Extensible event**: a derived event with zero current subscribers, kept as a hook.
- **Poison event**: a derived event that loops endlessly between processors.
- **Semantic decoupling**: producer independent of consumers' behavior.
- **Architecture quantum**: independently deployable unit with high functional cohesion, bound together by synchronous coupling; characteristics are scoped to it.
