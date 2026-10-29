---
name: fsa-ch14-service-based-style
description: Applies the service-based architecture style (coarse-grained domain services, optional shared database) from Chapter 14 of Richards and Ford's "Fundamentals of Software Architecture" (2nd ed.). Use when evaluating whether a system should be service-based versus monolithic or microservices, designing domain services, UIs, gateways or database topology, managing shared-database schema change, governing service count and coupling, aligning teams, or planning a stepping-stone migration toward microservices.
---

# Service-Based Architecture Style (FSA Chapter 14)

## Purpose

Service-based architecture is a pragmatic distributed style: a small set of separately deployed, coarse-grained domain services, usually reached from one or more UIs and often backed by a shared relational database. It gives much of the deployability, testability and fault isolation of distributed systems at a fraction of the cost and complexity of microservices or event-driven designs, while keeping ACID transactions inside each service. Use this skill to decide whether the style fits, shape its topology, control database change, govern it over time, and use it as an intermediate step toward finer granularity.

## Key decision rules

1. **Service count ceiling.** With one shared database keep domain services to about 12 or fewer. More strains testing, deployment, monitoring, connections and schema coordination.
2. **Coarse by design.** Each service owns a full domain or subdomain and exposes an API facade that orchestrates the request internally (in-process calls), not by calling sibling services.
3. **ACID inside, not across.** Keep a business workflow within one service so commit and rollback work. If a workflow must span services, expect compensating updates and question the boundaries.
4. **Granularity cost.** A change anywhere in a domain service means retesting and redeploying the whole service. Extract a slice only when its change rate or scaling need clearly differs.
5. **Minimize service-to-service calls.** Domains should couple mainly through the database. Do cross-domain orchestration in the UI or API gateway. Frequent inter-service calls mean wrong boundaries or wrong style.
6. **Split data only when it is truly private.** Give a service its own database only if no other service needs that data; share data rather than add runtime calls.
7. **Never one entity library for all tables.** Partition the database logically and ship one entity library per partition, as fine-grained as still makes coherent data domains. Lock the common partition's library to the database team.
8. **Scale selectively.** Default to one instance per service; add instances (behind a load balancer) only for throughput or failover.
9. **Federate UI and data for isolation.** Separate UIs and databases by audience or security zone; each federated UI-plus-database group becomes its own quantum.
10. **Align teams by domain.** Cross-functional domain teams fit; layer-based teams (UI, backend, DBA) fight the style.
11. **Use it as a stepping stone.** Move to service-based first, then break down only volatile or high-scale domains. Not everything needs to become a microservice.

Qualitative profile: strong on agility, testability, deployability, fault tolerance, availability, simplicity, cost and transactional integrity; only moderate on scalability and weak on elasticity, because each instance replicates a lot of functionality. Never present star ratings; describe these qualitatively.

## Default workflow

1. **Frame the need.** List driving characteristics. If extreme elasticity or very high system-wide scalability dominates, note the style's limits early.
2. **Identify domains.** Aim for roughly 4 to 12 coarse domain services. Merge or rethink if analysis produces many more.
3. **Design each service.** Choose layered or subdomain-partitioned internals; define the API facade and the transaction boundary for each workflow.
4. **Choose UI and gateway topology.** Single UI, UIs per audience, or per service; add a gateway for external exposure, cross-cutting concerns or load balancing.
5. **Choose data topology.** Shared, grouped or per-service databases; set up logical partitions and matching entity libraries.
6. **Count quanta.** Determine which parts can differ in characteristics (security zones, scaling).
7. **Set governance.** Fitness checks for change locality, inter-service call volume, service count and library dependencies.
8. **Align teams.** Map stream-aligned teams to domains; plan how enabling, platform and complicated-subsystem teams engage.
9. **Plan evolution.** Mark volatile domains as candidates for later decomposition.
10. **Record decisions** with the trade-offs above (consistency vs. change scope, cost vs. elasticity).

## References

- [references/topology-and-service-design.md](references/topology-and-service-design.md): read when laying out services, choosing internal service design, reasoning about ACID vs. compensating updates, picking UI variants, adding a gateway, or deploying to cloud.
- [references/data-topologies.md](references/data-topologies.md): read when choosing database topology, assessing schema-change impact, or fixing a shared entity library antipattern.
- [references/risks-governance-and-teams.md](references/risks-governance-and-teams.md): read when reviewing an existing service-based system for risk, writing fitness functions, or mapping teams and Team Topologies onto the services.
- [references/characteristics-fit-and-migration.md](references/characteristics-fit-and-migration.md): read when deciding whether the style fits, explaining its strengths and weaknesses, counting quanta, studying the worked recycling example, or planning a stepping-stone migration.
- [references/source-map.md](references/source-map.md): read to locate which reference covers a given chapter section.

## Scripts

None. The chapter offers heuristics (a service-count ceiling, change-locality and coupling signals) rather than calculations; the sketches in the governance reference show how to turn them into checks.
