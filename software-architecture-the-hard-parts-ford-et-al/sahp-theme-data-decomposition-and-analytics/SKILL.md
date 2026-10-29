---
name: sahp-theme-data-decomposition-and-analytics
description: Theme skill on splitting operational data and designing analytical data from "Software Architecture: The Hard Parts" (Ford, Richards, Sadalage, Dehghani) (chapters 6 and 14). Use when deciding whether and how to split a shared database, identifying data domains and cross-domain dependencies, managing connection budgets, choosing database types per domain, or choosing between data warehouse, data lake and data mesh with data product quanta.
---

# Data decomposition and analytical data (Software Architecture: The Hard Parts, ch. 6 and 14)

Operational and analytical data have different purposes and shapes. This theme covers splitting the operational database safely and giving analytics a design of its own.

## Cross-chapter rules

1. **Weigh reasons to split against reasons to keep together.** Change control, connections, scalability, fault tolerance, quantum boundaries and database fit argue for splitting; data relationships and transactions argue against.
2. **Split by data domain, not by table.** Assign tables and their dependent artifacts to domains, break cross-domain links, and merge domains that are too entangled (`scripts/data_domain_check.py`).
3. **Follow a staged migration.** Domains, then schemas per domain, then services restricted to their own schema, then separate servers, then cut over.
4. **Govern connections.** Demand is pool size times instances; set quotas, measure waits, and rebalance (`scripts/connection_budget.py`).
5. **Pick database types per domain** with a business case and an ADR; remember aggregate boundaries are costly to change.
6. **Keep analytics separate from operations.** Warehouses and lakes centralize data away from its domain and recreate coupling; data mesh gives each domain a data product owned by its team.
7. **Data product quanta stay asynchronous.** They run beside their service, sync with eventual consistency, expose loose contracts to consumers and are governed by policies run in a platform sidecar. Guard completeness with fitness functions (`scripts/daily_completeness_check.py`).

## Default workflow

1. Decide whether the database must split (ch06).
2. Map domains and dependencies, then migrate in stages (ch06).
3. Design analytical data as domain-owned data products (ch14).

<!-- BEGIN GENERATED: run tools/build_bundles.py to refresh -->

## References by chapter

Each link is one level deep; read only the files whose description matches the task.

### CH06: Pulling Apart Operational Data

- [ch06-database-type-selection.md](references/ch06-database-type-selection.md): read when choosing a database type for a domain, comparing relational, key-value, document, column family, graph, NewSQL, cloud native or time-series stores, or designing aggregates.
- [ch06-decomposition-drivers.md](references/ch06-decomposition-drivers.md): read when deciding whether to split, weighing a specific disintegrator or integrator, doing connection or quota math, or building evidence for a skeptical data team.
- [ch06-five-step-decomposition.md](references/ch06-five-step-decomposition.md): read when defining data domains, cutting cross-domain views and FKs, using synonyms, isolating connections, or planning server migration and cutover.

### CH14: Managing Analytical Data

- [ch14-centralized-analytics-patterns.md](references/ch14-centralized-analytics-patterns.md): read when evaluating or migrating away from a data warehouse or data lake, explaining star schemas, or diagnosing brittleness, PII and staleness in existing pipelines.
- [ch14-data-mesh-and-dpq-design.md](references/ch14-data-mesh-and-dpq-design.md): read when designing a Data Mesh, choosing DPQ types, setting coupling and communication rules, defining governance, or deciding whether mesh fits.
- [ch14-dpq-worked-example-and-fitness-functions.md](references/ch14-dpq-worked-example-and-fitness-functions.md): read when building an aggregate or ML-oriented DPQ, writing its ADR, or defining completeness and contract fitness functions.

Merged section maps: [source-maps.md](references/source-maps.md).

## Scripts

Python 3 standard library only; run any script with `--help` for its arguments.

| Script | Purpose |
|---|---|
| `scripts/connection_budget.py` (ch06) | Check and rebalance per-service connection quotas against a shared database. |
| `scripts/data_domain_check.py` (ch06) | Report cross-domain database dependencies that must be broken before a split. |
| `scripts/daily_completeness_check.py` (ch14) | Daily completeness fitness function for a data product feed. |

<!-- END GENERATED -->
