# Reuse, Coupling, Characteristics and Teams

## Contents
- Reuse is implemented through coupling
- The canonical entity trap
- Technical partitioning taken to the extreme
- Team topology: a communication antipattern
- Characteristics profile (qualitative)
- Diagnostic checklist for an existing system
- Review questions

## Reuse is implemented through coupling

Architects in this style were told to hunt for reuse aggressively. The classic move: notice that every division of an insurer (auto, home, life, disability, and so on) has its own notion of Customer, extract all of it into one canonical Customer service, and point every division at it. The reuse goal is met on paper.

The hidden price, discovered slowly:
- Reuse and coupling are the same mechanism. Every consumer of the shared service is now coupled to it.
- Any change to the shared service ripples to all consumers, so even small changes become risky.
- Risky changes demand coordinated deployments, whole-system testing and other drags on engineering speed.

Decision rule: treat every proposed shared component as a coupling decision first and a reuse win second. Ask how often it will change, how many consumers it will have, and whether those consumers change for the same reasons.

## The canonical entity trap

A single enterprise-wide entity must carry the union of everything every context needs. Auto insurance needs driver's license data (a property of the person, not the car), so the shared Customer gains license fields the disability division never uses, yet the disability team must still understand and carry that complexity. Multiply by every division.

Domain-driven design's preference for separate, context-specific models over holistic reuse grew partly from pain with exactly this kind of architecture. Default recommendation: let each bounded context own its own model of the entity, and integrate via identifiers and translation rather than a shared canonical schema.

## Technical partitioning taken to the extreme

Among general-purpose styles, none pushed technical partitioning further than this one. It is coherent from a separation-of-concerns and reuse standpoint, and a practical nightmare.

Why: a typical work item is domain-shaped, such as "add a delivery instruction field to checkout". The domain concept (checkout) is pulverized across layers, so the task can touch dozens of services in several tiers plus the shared schema. Worse, if the existing enterprise services have the wrong transactional granularity for the new need, developers must either redesign them or create a near-duplicate service with different transactional behavior, which defeats the reuse that justified the design.

Change variability: on a good day a change stays inside the enterprise layer; on a bad day (an unanticipated kind of change) it spans four or five layers with tightly coupled edits in each. Because the scope of any change is so unpredictable, every request needs deep analysis, and teams come to dread the word "change".

## Team topology: a communication antipattern

Team topologies were not a design concern when the style was popular. Its strict taxonomy mirrors a strict separation of people: business-service authors rarely talked with enterprise-service builders; they communicated through contracts, interfaces and enterprise ticketing systems, with a different team per integration layer. The result is slow feature delivery, and this anti-example helped motivate modern team-topology thinking (stream-aligned teams owning a domain end to end).

Warning signs in a modern org: features need tickets to three or more teams; a central integration team approves every workflow change; teams are named after technical layers rather than business capabilities.

## Characteristics profile (qualitative)

Many characteristics now considered essential were not goals in that era; agile practices had not reached the large enterprises using the style.

- Partitioning: technical, to an extreme.
- Architecture quanta: one, even though the system is distributed. Two reasons: the shared database or few databases couple many concerns, and, more importantly, the orchestrator is a giant coupling point; no part can have characteristics different from the mediator coordinating everything. The style thus combines the drawbacks of monoliths and of distributed systems.
- Deployability and testability: very poor, both because the style hinders them and because nobody aimed for them.
- Elasticity and scalability: achievable, with effort; vendors invested heavily (for example, session replication across application servers).
- Performance: weak, since every business request is spread over many hops and layers.
- Simplicity and cost: inverted from what you want; it is complex and expensive.
- Evolvability and agility: poor; change scope is unpredictable and cross-layer.

Lessons the style taught the field: technical partitioning has real-world limits, and distributed transactions are far harder in production than on paper. The backlash against it led directly to domain-partitioned styles such as microservices.

## Diagnostic checklist for an existing system

Flag drift toward this style when several hold:
- Services are grouped by technical layer and owned by layer-specific teams.
- A shared canonical model is mandated across many contexts.
- A central bus or workflow engine holds business logic and transaction boundaries.
- Near-duplicate services exist that differ mainly in transactional behavior.
- Typical stories require multi-team, multi-layer coordinated releases.
- One shared database underlies many "independent" services.

## Review questions

1. For a proposed shared "Product" service used by six teams, what change frequency and consumer diversity would make it a net loss?
2. Why does a central orchestrator collapse a distributed system to one quantum, and what would have to change to get two?
3. A story touches business, enterprise and application layers plus the schema; how would you restructure ownership so it touches one team?
