# Characteristics, Quanta, Fit and Migration

## Contents
- Qualitative characteristic profile
- Architecture quanta in this style
- When to choose it
- Worked example: device recycling system
- Stepping-stone migration
- Review questions

## Qualitative characteristic profile

The style is **domain partitioned**: top-level structure follows business domains, not technical layers. A change to one domain normally touches only that service plus its UI and data.

Relative to other distributed styles:

**Strong (but not best in class)**
- Agility, testability and deployability: domain-scoped services change, test and release independently, with less risk than a monolith. Together these shorten time to market.
- Fault tolerance and availability: services are self-contained and rarely call each other (they share code and data instead), so one failing service does not take others down.
- Simplicity and cost: among the cheapest and least complex distributed styles to build and operate.
- Transactional integrity: the best ACID support of any distributed style, because the transaction boundary is a whole domain service, giving familiar commit and rollback.
- Domain-driven design fit: one domain maps cleanly to one deployable.

**Middling to weak**
- Scalability: workable, but each instance replicates a large amount of functionality.
- Elasticity: weaker still, for the same reason; scaling out quickly is costly in machine resources.

General trade-off to communicate: paying more in cost and complexity (microservices, event-driven, space-based) buys more scalability, elasticity and fault tolerance. Many organizations do not need that extra capability, or cannot justify its price. Recommending a heavyweight style for modest needs is like buying a race car for a traffic-jammed commute.

Typical scaling stance: one instance per service by default; scale only the services with real throughput or failover needs. Single-instance services keep in-memory caching and connection pooling simple.

The style also gives good modularity without forcing hard decisions about fine granularity and service choreography versus orchestration.

## Architecture quanta in this style

Quantum count is one or more. Rules of thumb:

- If every service shares one database (or one UI), the whole system is a single quantum.
- Federating the UI and the database creates separate quanta.
- Services that share a database stay in the same quantum even if they have separate UIs.

Use this to answer "can these parts have different characteristics?": only parts in different quanta can truly differ in scalability, availability or security posture.

## When to choose it

Choose or recommend service-based when most of these hold:

- Business application with a clear set of domains (roughly 4 to 12).
- Strong need for ACID consistency within a domain workflow.
- Team wants distribution benefits (independent deploys, fault isolation) without microservices operational cost.
- Teams are, or can be, organized by domain.
- Elasticity needs are modest or limited to a few services.

Look elsewhere when:

- Extreme or bursty elasticity across the whole system is required.
- Domain analysis yields far more than about 12 services.
- Workflows inherently cross many domains with heavy service-to-service traffic.

## Worked example: device recycling system

The book's running case (a company buying back used electronics) maps to services: quoting, receiving, assessment, accounting, item status, recycling, reporting. Design choices worth reusing:

- **Scale selectively.** Only the public-facing quoting and status services get multiple instances; internal services run one instance each.
- **UIs by audience.** A customer-facing UI, plus separate internal UIs for receiving and for recycling and accounting. This isolates faults, scales the public side, and means external users have no network route to internal functions.
- **Databases by security zone.** One database for customer-facing operations, one for internal operations, in separate network zones. A firewall permits internal services to read and update customer-facing data, but not the reverse. Database-level mirroring or synchronization is an alternative. The result is two quanta: customer-facing and internal operations.
- **Volatility isolation.** Assessment logic changes constantly as new devices arrive; in its own service those changes stay contained.

Invented analogue: an insurance broker could split a public quote-and-status quantum (scaled, internet-facing) from an internal underwriting, billing and reporting quantum (single instances, private network), with one-way access from internal to public data.

## Stepping-stone migration

Service-based is a good intermediate target when moving from a monolith toward a finer-grained distributed style, or when building a new distributed system. The guiding idea: not every part of a system needs to be microservices.

Playbook:

1. Decompose into domain services first.
2. Observe each domain for change frequency, scaling needs and fault isolation needs.
3. Break down only the domains that justify it. In the recycling case, assessment (high churn) splits into per-device-type services; recycling and accounting stay coarse.
4. Leave stable domains as domain services indefinitely.

Skipping this step tends to turn every function into a microservice whether or not it needs to be one.

## Review questions

1. Which two signals tell you the domain boundaries in a service-based design are wrong?
2. Why does a shared database not prevent this style from delivering independent deployability?
3. How many quanta does a system have if two services share a database but have separate UIs?
4. What would make you extract part of a domain service into finer services?
5. Why is elasticity weaker here than scalability, and when does that matter?
