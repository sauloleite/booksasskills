# Centralized Analytics Patterns: Warehouse and Lake

## Contents
- Why analytical data is a separate concern
- Data Warehouse: mechanics
- Star schema in brief
- Data Warehouse: failure modes and strengths
- Data Lake: mechanics
- Data Lake: failure modes and strengths
- The shared flaw: technical partitioning
- Diagnostic checklist for existing pipelines
- Choosing between centralized patterns and mesh

## Why analytical data is a separate concern

Operational data is shaped around transactions: small, frequent reads and writes, normalized to protect integrity. Analytical data is shaped around questions: large scans, history, aggregation, joins across domains. Running heavy aggregations directly on transactional relational stores competes with live load, and the schemas rarely fit both uses. Every approach in this chapter is an answer to "where and in what shape should the analytical copy live, and who owns it?"

Historical context matters for the argument: once client/server systems moved data onto shared network databases, organizations could finally reuse history for analysis, and the first answer was a centralized warehouse. The approaches then evolved in step with architecture styles.

## Data Warehouse: mechanics

Assumes operational data sits in relational databases reachable over the network. The pipeline:

1. **Extract** from many operational sources, because querying every database live for reports is impractical.
2. **Transform** into one analytical schema, usually dimensional (star), denormalized for speed and simpler queries.
3. **Load** on a recurring schedule, through database replication or dedicated translation tooling.
4. **Analyze** inside the warehouse, which has its own large storage and compute so analytical load stays off operational systems.
5. **Consume** through data analysts who build BI reports and dashboards, usually with a SQL-like query interface. Part of the reason for the transform step is to make complex aggregations easier to express.

## Star schema in brief

- **Facts**: measurable quantities (durations, amounts, counts, rates).
- **Dimensions**: descriptive context for facts (who, where, which category, which product).
- Deliberately denormalized: fewer joins, faster aggregation, support for multidimensional cubes.
- In practice these schemas grow very complex, and they erase domain boundaries; queries must reconstruct the domain view.

Invented example: a ride-hailing company's warehouse has a `trip_fact` table (fare, distance, wait minutes) and dimensions for driver, city, vehicle class and date. The dispatch team renames a status code and splits "vehicle class" into two fields; the nightly ETL silently drops rows until someone notices revenue dashboards dipped.

## Data Warehouse: failure modes and strengths

| Failure mode | What actually happens |
|---|---|
| Integration brittleness | Domain schemas track domain semantics, so any domain change forces schema changes, which force import logic changes in the transform step. |
| Domain knowledge split | Operational teams know the business rules; analysts know analytics techniques. Both are needed for a correct report, so every data change needs coordination among architects, developers, DBAs and data scientists. |
| Complexity | A second schema plus ongoing ingest and transform machinery, maintained as a separate program of work yet tightly coupled to every operational domain. |
| Weak return on effort | Historically huge on-premises infrastructure and maintenance cost, while consumers kept asking for reports the schema could not answer. Many warehouses failed on this alone. |
| Synchronization bottleneck | All independent data streams converge in one place, an organizational and operational choke point; sync jobs often hurt the very operational systems they were meant to be decoupled from. |
| Contract brittleness | Pipelines that both ingest and transform embed analytical contract assumptions; operational and analytical contracts differ, and the transform layer is where they collide. |

Genuine strengths: one consolidated place for analytical data, and a dedicated silo that isolates analytical compute from operational workloads. The pattern fits monolithic or shared-database systems far better than distributed ones.

## Data Lake: mechanics

A reaction to the warehouse, keeping centralization and pipelines but flipping the order: load first, transform later and only when someone needs it. The reasoning: up-front schemas often did not fit the questions actually asked, and many ML models prefer data close to its raw form.

1. **Extract** from many sources, with little or no reshaping; some light structuring may still happen (for example, sources dropping columnar snapshot files).
2. **Load** regular dumps into the lake, commonly in cloud storage.
3. **Consume** through data scientists and other analytical users who discover data and perform their own joins, aggregations and transformations per question.

## Data Lake: failure modes and strengths

- **Discovery of the right assets is hard.** Domain relationships evaporate as data lands in an unstructured store, so domain experts still have to be pulled in to build correct analyses.
- **PII and combinable data.** Privacy regulation increasingly covers data that can be combined to identify someone, not just obvious identifiers. Raw dumps make that recombination easy. Only domain experts reliably know what is sensitive, so they end up re-auditing lake contents.
- **Still technically partitioned.** Ingest, transform, load and serve remain separate technical stages, and data is still treated as an entity apart from its domain.
- **Pipelines remain brittle.** Less transformation does not mean none; cleansing and reshaping still occur and still couple to upstream schemas.
- **Quality pushed downstream.** Integrity checks and quality work move into downstream lake pipelines, which can recreate warehouse-style bottlenecks.
- **Staleness or breakage.** Batch, technically partitioned flows force an unpleasant choice when upstream systems change: ignore the change and serve stale data, or let coupled pipelines fail.

Genuine strengths: less rigid structure than a warehouse, far less up-front transformation, raw data that suits ML, and a better (though imperfect) fit for distributed architectures. The costs are ad hoc transformation work for each consumer and frequent confusion about how data sets relate.

## The shared flaw: technical partitioning

Both patterns separate data from the domain that gives it meaning. Modern architectures (microservices especially) encapsulate domain knowledge, including data, inside domain boundaries. When analytical data is then pulled into a technically partitioned central store, semantic coupling that was artificially cut must be managed across teams, and the more it is cut, the harder it is to manage. What is needed is a design that keeps domain-level partitioning while still cleanly separating analytical from operational data: that is the motivation for Data Mesh.

## Diagnostic checklist for existing pipelines

Ask these when reviewing a warehouse or lake in a distributed system:

- When a service team changes its schema, who finds out, and how quickly? (Brittleness)
- Can a consumer join two data sets correctly without asking the owning teams? (Discovery)
- Is there a list of fields that are sensitive alone or in combination, and who maintains it? (PII)
- Do sync or extract jobs read from live operational databases at peak times? (Bottleneck leak)
- Where are data quality checks run, and who is paged when they fail? (Downstream quality)
- What is the maximum acceptable lag, and what happens when a source is late? (Staleness)
- Does a central data team gate every new analytical use case? (Organizational bottleneck)

Three or more worrying answers in a domain-partitioned system is a strong signal to evaluate a mesh-style redesign, at least for the domains that change most often.

## Choosing between centralized patterns and mesh

- Monolith or single shared database, stable schemas, mainly fixed BI reports: a warehouse can still be reasonable.
- Many raw sources, exploratory data science, modest PII exposure, a capable central data team: a lake can work, but budget for discovery and governance tooling.
- Microservices with isolated data, frequent domain change, PII sensitivity, and many analytical consumers: favor Data Mesh (see also data-mesh-and-dpq-design.md).
