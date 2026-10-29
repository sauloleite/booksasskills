# Taxonomy, Orchestration Engine, Message Flow and Data

## Contents
- Historical context: why the style made sense
- The word "service" is overloaded
- The four-layer service taxonomy
- Orchestration engine and message bus
- Message flow
- Data topology and declarative transactions
- Glossary
- Worked example: tracing one request

## Historical context: why the style made sense

Orchestration-driven SOA emerged in the late 1990s. Read it as a rational answer to that era's constraints, not as stupidity:

- Companies were growing fast and merging, so they inherited duplicated and inconsistent versions of core entities (customer, policy, account) and duplicated workflows.
- Compute was scarce and commercial: operating systems were licensed per machine, database licensing was convoluted, and vendors of application servers and databases fought over features such as connection pooling.
- Distributed computing had just become feasible and was needed for scale.
- With every resource expensive, "reuse everything you can" became the governing philosophy, and the organizational wish to remove duplication reinforced it.
- Open source operating systems were not yet trusted, so a style with many small, independently deployed units (microservices) would have been unaffordable.

The lesson for today: when you evaluate a style, reconstruct the forces of the era (licensing, hardware cost, team practices) that made it attractive, and check whether those forces still hold in your context. A style survives only as long as its motivating constraints do.

## The word "service" is overloaded

Three styles in the book use "service": orchestration-driven SOA, service-based architecture, and microservices. A SOA enterprise service differs from a microservice in granularity, ownership, data, deployment and coupling. The term suffers from semantic diffusion. When a stakeholder says "service", pin down which style's meaning is intended before reasoning about granularity, data ownership or deployment.

## The four-layer service taxonomy

The style organizes services by technical role, with a dedicated team or role per layer, so that every layer pursues maximal abstraction and reuse. Real implementations vary in the exact layers, and some layers may live inside an application server; the common idea is a strict classification of services by responsibility.

| Layer | Granularity | What it holds | Typical owner |
|---|---|---|---|
| Business services | Very coarse | Entry points for business processes; signatures only (input, output, schema), no code | Business users or analysts |
| Enterprise services | Fine | Atomic, shared building blocks around domain operations and transactional entities | Shared enterprise development team |
| Application services | Any, single use | One-off functionality one application needs, not worth making reusable | The single application team |
| Infrastructure services | Concrete | Operational concerns: monitoring, logging, authentication, authorization | Shared infrastructure team close to operations |

Business service granularity test (the era's heuristic): ask "Are we in the business of X?". "Place order" or "execute trade" pass. "Create customer" fails, because the company creates customers only as a step toward its real business, so it belongs in the enterprise layer.

Enterprise service goal: perfectly encapsulated building blocks that can be freely composed into any workflow, so a piece of workflow never has to be written twice. Why it fails in practice:
- The ideal level of abstraction balancing all competing forces is elusive and probably unreachable.
- Software components are not like construction materials that stay valid for decades; markets, technology and practices keep changing, so the "stable reusable asset" decays.

Application services exist precisely because not everything deserves enterprise reuse (for example, geolocation needed by one app).

Infrastructure services follow directly from technical partitioning: cross-cutting operational concerns become their own layer.

## Orchestration engine and message bus

The engine is the heart of the style. Responsibilities:
- Composes business services from enterprise services (defines the mapping).
- Coordinates transactions and decides where transaction boundaries sit.
- Transforms messages between formats and contracts.
- Acts as an integration hub joining custom code, packaged software and legacy systems.

These capabilities are what an enterprise service bus (ESB) packages. Guidance:
- Building a whole architecture around an ESB is generally a bad idea.
- In integration-heavy environments that genuinely need both a hub and an orchestrator, using an ESB that already bundles both is sensible.
- Develop the skill of separating a tool's real uses from vendor hype, in both directions.

Organizational consequence (Conway's Law): because everything flows through the bus, the integration architects who own it accumulate political power and turn into a bureaucratic bottleneck.

Why delegating transactions to the engine disappoints: wrapping a handful of services in a distributed transaction works, but as entities take part in more and more workflows, finding correct transaction boundaries gets harder and complexity climbs. Transactional enterprise building blocks proved very difficult to deliver.

## Message flow

Every request, including calls that are internal to a workflow, passes through the engine, which holds the architecture's logic. A business service invokes the bus; the bus runs the workflow, calling enterprise services in order; enterprise services may call application services, again through the bus. The bus is both integration hub and orchestrator for all traffic. Consequences: extra network hops on every step, a single choke point for change and performance, and workflow logic that lives outside the domain code.

## Data topology and declarative transactions

- Despite being distributed, the style usually relies on one or a few shared relational databases, the norm for late-1990s distributed systems.
- Transactionality was moved out of the database and into the bus or application server, which offered declarative, per-entity transaction settings, so transactional behavior could be configured independently of the database and of how an entity was being reused.
- Architects of the era treated data as foreign territory: an integration point, not part of the problem domain.

Declarative transactional scope (configured in XML on entity components such as EntityBeans, adjusted per workflow) largely failed for two reasons:
1. If a developer cannot know an entity's transactional behavior until runtime, entities and their dependencies become much more complex, and teams end up cloning near-identical entities that differ only in transactional scope.
2. However sophisticated the bus, failure modes produce edge cases it cannot resolve, leaving inconsistent data that humans must repair by hand.

General principle: some multifaceted concerns, transactions above all, cannot be cleanly abstracted away; the abstraction leaks too much to be reliable. Be skeptical of any tool or platform promising to make distributed transactions transparent.

## Glossary

- Taxonomy (of services): classification of services into layers by technical responsibility.
- Canonical entity service: a single shared service holding the enterprise-wide definition of an entity (for example, Customer).
- Orchestration engine / message bus / ESB: central mediator that sequences calls, transforms messages, manages transactions, and integrates heterogeneous systems.
- Semantic diffusion: a term's meaning blurring as it is applied to more and more things.

## Worked example: tracing one request

A lender's "Approve loan" business service is defined by analysts as a signature. The bus maps it to enterprise services "Create applicant", "Score credit" and "Price loan". "Score credit" calls an application service that wraps one bureau's API; every call is logged through infrastructure services. Each hop crosses the bus. Now product asks to add a co-applicant. The change touches the business signature, the bus workflow and transaction boundary, the applicant entity used by other workflows, the shared database schema, and possibly the pricing service. Four teams, four tickets, one coordinated release. That is the style's change profile in miniature.
