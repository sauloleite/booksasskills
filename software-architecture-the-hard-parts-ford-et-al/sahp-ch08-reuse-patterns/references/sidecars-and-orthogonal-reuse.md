# Sidecars, service mesh and orthogonal reuse

## Contents
- Duplicate or couple? It depends on the style
- The operational coupling problem
- Lineage: hexagonal architecture
- Sidecar and service mesh mechanics
- Orthogonal coupling and orthogonal reuse
- What belongs in the sidecar
- Ownership and governance
- Strengths, weaknesses and fit
- Worked example and checklist

## Duplicate or couple?

Microservices prize decoupling, so they tolerate duplication. Two services that both deal with a customer each keep their own internal model and exchange loosely structured data (for example JSON name/value pairs), so either can change its internals or even its technology stack without breaking the other. Duplication has real costs (synchronization effort, meanings drifting apart), but in microservices the cost of coupling is usually worse. The same question in a service-based architecture, with fewer, larger services sharing a database, often resolves the other way: couple. The correct answer depends on the architecture style.

## The operational coupling problem

Some capabilities actually benefit from being identical everywhere: monitoring, logging, authentication and authorization, circuit breakers, service discovery. Leaving each team to implement them independently produces chaos:
- Operations cannot verify that every service actually emits the agreed telemetry.
- Organization-wide upgrades of a tool (a new monitoring agent version) require coordinating every team.

## Lineage: hexagonal architecture

The sidecar idea descends from Alistair Cockburn's hexagonal architecture (ports and adapters): domain logic at the center, technical integrations attached through adapters at the edge. One difference from microservices thinking: hexagonal architecture treats the database as just another pluggable adapter, whereas domain-driven design and microservices keep schema and transactional boundaries inside the service with the domain logic.

## Sidecar and service mesh mechanics

1. Split each service into its domain part and its operational part.
2. Move the operational part into a separate component deployed alongside every service: the sidecar (named after a motorcycle sidecar).
3. If every service is guaranteed to carry the sidecar, the sidecars present a uniform operational interface and can be linked through a control or service plane.
4. The interconnected sidecars form the service mesh, giving architects and operators one place for dashboards, traffic and scale controls, and policy.
5. Use fitness functions to verify that every service actually includes the sidecar; the mesh's value depends on that guarantee.

**Polyglot governance.** Microservices let teams pick platforms per service, which complicates enterprise-wide standards. The mesh gives governance a consistent lever across heterogeneous stacks. Without it, adopting a single monitoring product would mean building and maintaining a sidecar for every platform in use.

## Orthogonal coupling and orthogonal reuse

Two parts are orthogonally coupled when they serve independent purposes yet must meet to form a working system: monitoring is unrelated to, say, a checkout flow, but checkout cannot ship without it. Microservices are partitioned by domain; operational concerns slice across all those partitions at right angles. A sidecar is an *orthogonal reuse pattern*: it reuses something along a seam perpendicular to the main partitioning, isolating the cross-cutting concern in one consistent layer. Recognizing orthogonal coupling lets you choose intersection points that entangle the concerns least.

The architectural analogue in design-pattern terms is the Decorator: behavior is layered onto every service without changing the service's own connections. The same approach can carry cross-cutting concerns other than operational ones (the book returns to this for contracts and data).

## What belongs in the sidecar

**Yes:** plumbing with no domain responsibility, such as logging, monitoring, service discovery, authentication, authorization, circuit breaking.

**No (by default):** domain classes such as Customer or Address. Putting them in the sidecar makes them technically available everywhere but re-creates exactly the coupling microservices avoid: change the class and every consumer must move. If a shared domain shape is truly needed, treat it as an explicit trade-off decision and manage it with contracts. Neither answer is unambiguously right, so it is an architect's call.

**Maybe:** technical utilities (say, a format converter). Weigh how many teams need it against the size and overhead added to every service, including those that never use it. A workable threshold: fewer than about half the teams using it means it stays out (ship it as a library) and gets reassessed later.

**Size warning.** Every addition grows the sidecar, and a sidecar can become large and complex. Guard against it becoming the biggest component in the system.

**Dual implementations.** If a shared library also logs and the service logs too, you get duplicate entries. Deciding that the sidecar owns logging resolves who writes what.

## Ownership and governance

Options: shared responsibility across service teams, a central infrastructure or platform team, or a mix. As team count grows, a dedicated team that owns the sidecar, treats service teams as customers, and runs a pipeline that tests the sidecar once bound into each service via fitness functions scales better than shared ownership. Service teams request additions; the owning team applies the inclusion criteria above.

## Strengths, weaknesses and fit

Strengths: a uniform, isolated way to handle unavoidable cross-cutting coupling; consistent infrastructure control across services; flexible ownership models.

Weaknesses: a sidecar implementation per platform is required; the sidecar tends to accumulate features and complexity.

Fit: spreading a cross-cutting concern consistently across many distributed services, independent of how they talk to each other.

## Worked example (invented)

A media company runs 24 services in Go, Kotlin and Node. Security wants mTLS and audit logs everywhere; SRE wants uniform latency metrics.
- Adopt a mesh sidecar providing mTLS, authn/authz, metrics, tracing, structured logging and retries.
- Platform team owns it; a deployment check fails any pod without the sidecar.
- Request: add an image-thumbnailing helper used by 4 services. Under half the teams, domain-adjacent, sizable: rejected, published as a library.
- Request: add a shared `Subscriber` model. Domain coupling: rejected; teams exchange subscriber data through a versioned contract instead.

## Checklist

- [ ] Is the concern operational with no domain behavior?
- [ ] Do enough teams need it to justify the overhead on everyone?
- [ ] Is there a fitness function proving every service has the sidecar?
- [ ] Is ownership explicit, with criteria for additions?
- [ ] Is the sidecar's size and complexity being watched?
- [ ] Are libraries and services prevented from duplicating what the sidecar now does?
