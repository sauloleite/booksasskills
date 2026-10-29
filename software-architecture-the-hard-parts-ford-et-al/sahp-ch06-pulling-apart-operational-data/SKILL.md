---
name: sahp-ch06-pulling-apart-operational-data
description: Decides whether and how to split a monolithic operational database by weighing six data disintegrators against two integrators, then executes a five-step data-domain migration (schemas, connection isolation, separate servers) and picks a database type per domain. Based on Chapter 6 of Ford, Richards, Sadalage and Dehghani's "Software Architecture: The Hard Parts". Use when justifying a database split, mapping tables to data domains, finding cross-domain foreign keys or views, sizing connection quotas, planning schema migration, or choosing relational versus NoSQL, NewSQL, cloud or time-series stores.
---

# Pulling Apart Operational Data (SAHP Chapter 6)

Purpose: help an agent treat database decomposition as a deliberate trade-off rather than an automatic consequence of splitting services. Data is the riskiest asset to restructure and hides its seams inside foreign keys, views and procedures, so the agent first justifies the split with named drivers, then migrates incrementally through data domains, and finally chooses the best-fitting database type per domain.

## Key decision rules (apply without opening references)

1. **Not every distributed architecture must split its data.** Microservices expect per-service data ownership; service-based architecture can share one database. Split only when drivers justify it.
2. **Balance six disintegrators against two integrators.** Disintegrators: change control, connection management, scalability, fault tolerance, architectural quantum, database type optimization. Integrators: data relationships (FKs, views, triggers, procedures, logical links) and database transactions (atomic multi-table writes). For each candidate split, state which force matters more to the business; the answer sets both whether to split and how coarse the result is.
3. **Breaking schema changes drive change control.** Drops, renames and type changes break every consumer; additions usually do not. The worst risk is the forgotten consumer that fails in production. Bounded contexts confine the blast radius.
4. **Ownership means writing.** A service owns data it writes; others ask it through a contract that may differ from the schema, so schema changes stay local while the contract evolves on its own schedule.
5. **Do the connection arithmetic.** Each service instance has its own pool: demand = sum(pool x instances). Look for connection waits first when a shared database shows timeouts or tripped circuit breakers.
6. **Govern connections with quotas.** Start with an even split, measure per-service peak usage and waits with fitness functions, keep quotas in external configuration, and shift spare connections to waiting services. Quotas summing to the database maximum become invalid once services scale out.
7. **A shared database is one failure domain and one quantum.** It is a single point of failure, and services needing different operational characteristics cannot form separate quanta until their data is split.
8. **Migrate by data domains, not tables.** A data domain groups tables plus their coupling artifacts used together in one functional scope. Cross-domain dependencies must be removed; intra-domain ones may stay. If two domains are too entangled, merge them into a broader context rather than cutting essential integrity.
9. **A service talks to exactly one data domain.** Never reach into another domain's tables; call the owning service. Synonyms are temporary scaffolding that make cross-schema references explicit, not a solution.
10. **Follow the five steps in order:** (1) analyze and identify domains, (2) move tables into per-domain schemas, (3) restrict each service's connection to its own schema and move all cross-domain access into services (hardest step), (4) move schemas to separate servers via backup and restore (simpler, needs downtime) or replication (no downtime, more work), (5) switch connections, then drop old connections and schemas.
11. **Data sovereignty per service has costs:** slow bulk access across domains, no database-enforced referential integrity, and procedures touching other domains must move to code.
12. **Choose the database type per domain on seven characteristics:** learning curve, modeling ease, scalability, availability/partition tolerance, consistency, ecosystem, read/write priority. Products in one family differ (consistency, quorum behavior), so verify per product.
13. **Aggregate boundaries are the expensive NoSQL decision.** Embed children when parents are few and reads or rendering dominate; reference them when they are shared or updated independently. Schema-less stores still have an implicit schema to version.
14. **Justify a new database type in business terms** (change turnaround, cost) with the data team as co-owner, and record it in an ADR.

## Default workflow

1. Clarify the architecture style and whether per-service data ownership is actually required.
2. Gather evidence per disintegrator: change frequency and consumer counts per table, connection waits and projected pool demand, load and capacity, outage history, characteristic differences between service groups, data that fits another engine poorly.
3. Gather evidence per integrator: relationship artifacts and atomic-write requirements.
4. Decide split or not and target granularity; write the reasoning down.
5. Map tables (and artifacts) to candidate domains; run `data_domain_check.py` to list cross-domain dependencies, merge candidates and services touching several domains.
6. Plan the five steps with the DBAs, choosing backup and restore or replication per domain.
7. Run `connection_budget.py` for current and projected instance counts to size each new database and quotas on anything still shared.
8. For each domain, evaluate database types on the seven characteristics; design aggregates if NoSQL is chosen.
9. Output: decision record (drivers, integrators, verdict), domain map, break list, migration plan, quota plan, database type choices with trade-offs.

## References

- [references/decomposition-drivers.md](references/decomposition-drivers.md): read when deciding whether to split, weighing a specific disintegrator or integrator, doing connection or quota math, or building evidence for a skeptical data team.
- [references/five-step-decomposition.md](references/five-step-decomposition.md): read when defining data domains, cutting cross-domain views and FKs, using synonyms, isolating connections, or planning server migration and cutover.
- [references/database-type-selection.md](references/database-type-selection.md): read when choosing a database type for a domain, comparing relational, key-value, document, column family, graph, NewSQL, cloud native or time-series stores, or designing aggregates.
- [references/source-map.md](references/source-map.md): read to find which file covers a given chapter section.

## Scripts

Python 3 standard library only; each supports `--help` and `--json`.

- Run `python3 scripts/data_domain_check.py domains.txt deps.txt --access access.txt --merge-threshold 3` to compute the cross-domain dependencies to break before splitting. `domains.txt`: `object, domain` lines (tables, optionally views or procedures). `deps.txt`: `kind, name, table1 table2 ...` with kind in fk, view, trigger, proc, function, synonym (fk lists child then parent). Optional `access.txt`: `service, table, r|w|rw`. Reports unassigned tables, each cross-domain artifact with its foreign tables, per-pair coupling counts with merge candidates, services touching several domains, and domains written by several services. Exits 1 if anything must be broken.
- Run `python3 scripts/connection_budget.py services.csv --db-max 300 --headroom 2` to compute per-service buffer, quota and peak demand at the given instance counts against the database limit, and a rebalancing proposal moving spare connections to services with waits. CSV header: `service,quota,max_used,instances[,waits]`. Add `--even` to start from an even split. Exits 1 if scaled demand exceeds the limit or a service stays short.
