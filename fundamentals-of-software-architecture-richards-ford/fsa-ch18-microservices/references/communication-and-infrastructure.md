## Contents

- API layer
- Operational reuse: sidecar, service mesh, service discovery
- Frontends
- Communication style
- Choreography vs orchestration
- Pitfalls
- Glossary

# Communication and Shared Infrastructure

## API layer

Usually called an API gateway; sits between consumers (UIs, external systems) and services. It can be a plain reverse proxy or a richer gateway hosting cross-cutting features (security, naming, discovery).

Rule: the gateway holds routing and cross-cutting concerns (security, monitoring, logging) only. No mediation, orchestration or business rules. Mediators belong to technically partitioned styles; putting workflow logic in the gateway pulls business behavior out of its bounded context.

Review check: if a gateway configuration contains conditionals on business data, sequencing of domain calls, or result aggregation with business meaning, move that logic into a domain service or a dedicated orchestration service.

## Operational reuse: sidecar, service mesh, service discovery

Microservices separates two kinds of reuse that classic SOA merged:

- **Domain reuse:** avoided; duplicate instead.
- **Operational reuse:** welcome, because concerns like monitoring, logging and circuit breaking benefit from uniformity.

The problem without a mechanism: if each team builds monitoring its own way, nobody can guarantee coverage, and upgrading the monitoring tool becomes a multi-team project of unknown length.

**Sidecar pattern.** Each service runs alongside a component that handles operational concerns. A shared infrastructure or platform team can own it, so upgrading the logging or monitoring tool means updating the sidecar once and every service picks it up.

**Service mesh.** Sidecars connect through a service plane (integration software, Istio being a typical product) to form a mesh. The mesh acts as a single control console for operational settings across all services, such as monitoring levels and logging, and gives a holistic operational view with each service as a node.

**Service discovery.** Automatic detection and location of service instances on the network. Requests go through the discovery mechanism, which can watch request volume and frequency and launch more instances for scale or elasticity. It is often part of the mesh (so present in every service) and often hosted in the API layer so callers have one consistent entry point.

Placement guide:

| Concern | Put it in |
|---|---|
| Authentication, rate limiting, request routing | API layer |
| Logging, metrics, tracing, circuit breaker, retries | Sidecar, controlled via mesh |
| Instance lookup and elastic scaling | Service discovery (mesh and/or API layer) |
| Business rules, workflow sequencing | Domain service or orchestration service |

## Frontends

The original vision placed the UI inside each bounded context, but web application partitioning and other constraints make that hard. Two practical options:

- **Monolithic frontend:** one UI (web, mobile or desktop) calling through the API layer. Simpler; the UI becomes a shared deployment unit across domains.
- **Micro-frontends:** UI components map to backend services, giving matching granularity and isolation from screen to data. Better independence; more integration work in the UI shell. Mezzalira's "Building Micro-Frontends" is the recommended deep dive.

Choose micro-frontends when domain teams must ship UI changes independently; choose a single frontend when UI consistency and simplicity outweigh team autonomy.

## Communication style

First decision per interaction: synchronous (caller waits) or asynchronous (events and messages, as in event-driven architecture).

Services typically interoperate in a protocol-aware, heterogeneous way:

- **Protocol-aware:** with no central integration hub, every service must know (or discover) how to call each peer; organizations standardize the calling conventions (a given REST level, specific queues).
- **Heterogeneous:** each service may use a different stack; polyglot is fully supported.
- **Interoperability:** services do call each other over the network to collaborate, even though transactional calls are discouraged.

Enforced heterogeneity anecdote, distilled: one early adopter required every team to use a different stack, making accidental class sharing impossible. The lesson is not "maximize variety" but "right-size technology to each narrow problem"; a small team should not be forced onto a heavyweight relational database it does not need. This runs counter to typical enterprise standardization and is only viable because the style is so decoupled.

## Choreography vs orchestration

Microservices has no global mediator. Two coordination options:

**Choreography.** No central coordinator; services call each other or exchange events as needed (for example, a wish-list service fetching demographic details from another service before answering). Fits the bounded-context philosophy and performs better (fewer bottlenecks, less coupling).

**Orchestration.** A dedicated, localized mediator service whose only job is coordinating calls for a workflow (for example, a customer-report service gathering data from several others).

| Factor | Choreography | Orchestration service |
|---|---|---|
| Decoupling | Maximal | Couples participants to the orchestrator |
| Error handling and coordination | Harder, spread across services | Centralized, easier to reason about |
| Performance | Better, no central hop | Extra hop, potential bottleneck |
| Fit | Simple flows, independent steps | Complex, multi-step business processes |

**Front Controller risk.** In a complex choreographed flow, the first service called often ends up coordinating many others on top of its own domain work. That double role adds complexity. If you see it, either move coordination into an explicit orchestration service or simplify the flow.

Domain workflows are frequently coupled by nature; the architect's job is to choose the representation of that coupling that best serves both domain and architecture goals.

## Pitfalls

- Business logic creeping into the gateway.
- Each team hand-rolling operational tooling instead of a shared sidecar.
- Accidental front controllers in choreographed workflows.
- Treating heterogeneity as a goal rather than a permission.
- Synchronous chains that recreate a distributed monolith; prefer async where the caller does not need the answer.

## Glossary

- **Service plane:** integration software that links sidecars into a mesh.
- **Front Controller:** a choreographed service that has drifted into mediating a whole workflow.
- **Orchestration service:** a localized mediator dedicated to one workflow.
