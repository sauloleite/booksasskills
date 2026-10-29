---
name: fsa-ch18-microservices
description: Applies the microservices architecture style as described in Chapter 18 of Richards and Ford's "Fundamentals of Software Architecture" (2nd ed.). Covers bounded-context boundaries, service granularity, data isolation and database topologies, API layer limits, sidecars and service mesh, choreography vs orchestration, sagas, governance of coupling, team topologies, and fit. Use when deciding whether microservices suits a system, sizing or splitting services, choosing a data topology, reviewing a microservices design for risks, or setting up coupling governance.
---

# Microservices Architecture (FSA Chapter 18)

## Purpose

Help an architect decide whether microservices fits a problem and, if it does, shape it well: draw service boundaries around bounded contexts, size services by behavior rather than by line count, keep data owned per context, keep business logic out of shared infrastructure, coordinate workflows deliberately, and govern coupling so the system does not decay into a distributed ball of mud. The chapter treats microservices as the extreme of domain partitioning: it buys independent deployability, fault isolation, scalability, elasticity and evolvability, and pays for them with network latency, coordination complexity and data headaches.

## Key decision rules (apply even without opening references)

1. **Decoupling beats reuse here.** The style's primary goal is decoupling, so prefer duplicating code (for example an address class) inside each bounded context over sharing it. Shared custom libraries leak a context across boundaries.
2. **Size by behavior, not by "micro".** Fowler called the name "a label, not a description". Too-small services (the Grains of Sand antipattern) must chat to do anything useful.
3. **Find boundaries with three tests:** functional cohesion (one significant behavior), transactional cohesion (entities that must commit together belong together), and communication cost (if a cluster of services talks constantly, merge it). Expect to iterate; the first cut is rarely right.
4. **Avoid cross-service transactions.** Needing one is a symptom that services are too fine-grained; regroup instead. Use a saga with compensation only as a considered exception (for example two parts needing very different characteristics). If distributed transactions dominate the design, microservices is the wrong style.
5. **Data topology: database-per-service is the default.** A single shared monolithic database is not an option, nor are domain-level databases. A small cluster of services (roughly five to six at most) may share a schema as a deliberately broader bounded context, at the cost of coordinated schema change.
6. **Beware the Entity Trap.** Do not make one service per table or entity. Decide per fact which context is the source of truth and whether others query it or hold replicated or cached copies.
7. **API layer = routing plus cross-cutting concerns only.** No orchestration, mediation or business rules in the gateway.
8. **Separate operational reuse from domain reuse.** Couple operational concerns (logging, monitoring, circuit breaking) through sidecars wired into a service mesh; keep domain code unshared.
9. **Choreography by default, orchestration for complex workflows.** Choreography preserves decoupling and performs better; orchestration localizes coordination and error handling in one dedicated service. Watch for a choreographed service quietly turning into a front controller.
10. **Govern both static coupling (libraries, contracts) and dynamic coupling (runtime calls).** Use SBOMs and dependency tooling for the first; logs or a call registry fed into fitness functions for the second.
11. **Align teams to domains.** Technically partitioned teams (UI, backend, DBA) fight this style; stream-aligned teams whose streams cross many contexts signal misaligned boundaries or the wrong style.
12. **Serverless is a deployment model of microservices,** not a separate style; containers on Kubernetes are an equally valid deployment.
13. **Good fit:** systems with high functional and data modularity, where parts can fail, change and be tested independently. **Poor fit:** tightly coupled workflows, transaction-heavy domains, latency-critical request paths.

## Default workflow

1. Confirm fit: check functional and data modularity, need for independent scaling or fault isolation, DevOps and automation maturity, and team alignment by domain.
2. Draft bounded contexts from the domain; apply the three boundary tests; list the transactions each context needs.
3. Choose a data topology per context (own database by default; justify any shared schema and keep the sharer count small).
4. Decide communication per interaction: sync or async; choreography or an orchestrator service; saga only where justified.
5. Define the API layer, sidecar contents, mesh and service discovery; pick the frontend approach (single UI or micro-frontends).
6. Set governance: static and dynamic coupling metrics as fitness functions; run the audit script on the call map.
7. Review against the common risks and iterate on granularity.

## References

- [references/boundaries-granularity-and-transactions.md](references/boundaries-granularity-and-transactions.md): read when drawing or reviewing service boundaries, resolving granularity disputes, or deciding whether a saga is justified.
- [references/data-topologies.md](references/data-topologies.md): read when choosing where data lives, handling shared tables, or arguing against a shared database.
- [references/communication-and-infrastructure.md](references/communication-and-infrastructure.md): read when designing the API layer, sidecars, service mesh, discovery, frontends, protocols, or choreography vs orchestration.
- [references/risks-governance-teams-and-fit.md](references/risks-governance-teams-and-fit.md): read when assessing fit, reviewing a design for common risks, setting up coupling governance, mapping team topologies, or deploying to cloud or serverless.
- [references/source-map.md](references/source-map.md): read to locate which reference covers a given chapter section.

## Scripts

- `scripts/coupling_audit.py`: run `python3 scripts/coupling_audit.py services.json` to compute per-service fan-out and fan-in, mutual call pairs and cycles, database sharer counts against the five-to-six guideline, and custom libraries shared across services. Run `python3 scripts/coupling_audit.py --help` for the input format and threshold flags. Use it as a governance fitness function over a call map built from logs or a service registry; exit code 1 means at least one finding exceeded a threshold.
