---
name: fse-ch08-working-with-data
description: Data-handling judgment for developers growing into engineers, based on Chapter 8 of Schutta and Vega's "Fundamentals of Software Engineering" (O'Reilly, 2025). Covers data shapes and formats, database family selection, persistence abstractions, pooling and transactions, consistency models and CAP, caching strategies, scaling, query and index tuning, EXPLAIN, observability, migrations and schema versioning. Use when choosing a format or database, designing persistence, diagnosing slow queries, adding a cache, or planning a migration or schema change.
---

# Working with Data

Data outlives the code around it, and most production surprises (slow pages, painful migrations, inconsistent reads) are data problems that looked fine in development. This skill gives an agent the chapter's decision criteria for helping a developer pick representations and stores, choose a persistence abstraction, keep queries fast, decide on consistency and caching, plan for growth, and evolve schemas and move data safely. It favors informed, reversible choices for current requirements over speculative architecture.

## Key decision rules

1. **Decide for today, keep it changeable.** There is rarely a perfect data choice, only an appropriate one. Pick from current requirements, keep the design reasonably flexible, and avoid overengineering for imagined scale. Outgrowing a database is a success problem.
2. **Format by five questions:** consumer (human or machine), size/speed needs, compatibility, structural complexity, validation needs. Defaults: JSON for APIs, YAML for human-edited config, XML when schema validation or namespaces matter, CSV for flat exports (configure quoting, encoding and blanks explicitly).
3. **Unstructured input:** keep the raw artifact and store extracted structured metadata beside it; query the metadata.
4. **Time:** store UTC, exchange ISO 8601 with offsets, use the platform's modern date/time library, show zones in UIs.
5. **Database by workload shape**, scored on relationships, read/write mix, query shape, growth and consistency need: relational for clear relationships, joins and transactions; document for variable or fast-changing record shapes; key-value for key-only access at maximum speed (cache, session); graph for dense relationships and traversals; vector for similarity search and RAG. Never by trend.
6. **Abstraction level by team and need.** Raw SQL gives control, the repository pattern isolates and makes tests easy, and an ORM gives speed of development at the cost of opacity. Higher is not automatically better. Default hybrid: ORM for routine work, SQL for measured hot paths. Team skills count.
7. **Pool connections; the app owns transaction boundaries.** Group every multi-step write that must be consistent into one short transaction.
8. **Consistency per data type, by business impact of being wrong:** strong for money, stock, auth; eventual for feeds, logs, recommendations; session for carts, preferences, drafts. CAP: under a partition choose CP (refuse) or AP (serve stale).
9. **Cache only after the four questions:** change rate, cost of stale data, query cost, measured bottleneck. Cache-aside with TTL for read-heavy data; write-through when cache must match DB; write-behind only where losing some writes is acceptable. Do not cache rapidly changing, money-relevant values.
10. **Scale in order:** vertical first, read replicas for read-heavy load, horizontal next, sharding last. Review growth indicators monthly with DBAs and ops.
11. **Query hygiene is mandatory:** explicit columns, bounded results, parameterized SQL (no concatenation, ever), indexes on filter/join/sort columns but not low-cardinality ones, keyset pagination on big tables. Verify with EXPLAIN / EXPLAIN ANALYZE and compare plans across environments when prod diverges.
12. **Observe from the app side too:** pool pending/active/idle metrics, query timings, traces that expose dominant spans and N+1 patterns.
13. **Migrate in phases when unsure,** least critical segment first, in PoC-sized batches (1,000 to 10,000 records as a starting range), with per-record error logging, sync (queues, CDC) and reconciliation while systems coexist.
14. **Version the schema like code** (Flyway, Liquibase, Rails migrations): sequential, idempotent, backward compatible where possible, with the data transformation in the same migration. Trial transformations on a small sample first and expect dirty data.

## Default workflow

1. Clarify the data: shape, volume now and in a year, consumers, consistency cost of errors.
2. Choose format and store using rules 2 to 5; record the reasoning and the trigger that would make you revisit it.
3. Choose abstraction level and set up pooling and transaction boundaries (rules 6 and 7).
4. Write queries with rule 11 hygiene; test with production-like volumes.
5. Add observability before tuning; tune with EXPLAIN; add caching or scaling only for measured problems (rules 9, 10, 12).
6. For any schema change or data move, follow rules 13 and 14 and the migration runbook.

## References

- [references/data-types-and-formats.md](references/data-types-and-formats.md): read when deciding structured versus unstructured handling, choosing JSON, XML, CSV or YAML, or handling binary data, timestamps or datasets too large for memory.
- [references/database-selection-and-persistence.md](references/database-selection-and-persistence.md): read when picking a database family, choosing between raw SQL, a repository and an ORM, or setting up connection pools and transaction boundaries.
- [references/consistency-caching-and-growth.md](references/consistency-caching-and-growth.md): read when choosing consistency models, reasoning about CAP, designing or rejecting a cache, or planning scaling (replicas, sharding) and growth reviews.
- [references/query-performance.md](references/query-performance.md): read when a query or endpoint is slow, when designing indexes or pagination, reading EXPLAIN output, sizing a pool from metrics, or trading ORM readability for SQL speed.
- [references/migration-and-schema-evolution.md](references/migration-and-schema-evolution.md): read when planning a data migration, ETL or dual-running sync, or adding versioned schema and data migrations.
- [references/source-map.md](references/source-map.md): chapter section to reference file mapping.

## Scripts

Python 3 stdlib only; `--help` documents every flag.

- Run `python3 scripts/migration_batch_planner.py --segment tools=12000 --segment sales=480000 --poc-records 20000 --poc-seconds 50 --batch-size 5000 --window-hours 4` to compute batches per phase, estimated and cumulative hours (PoC throughput times a safety factor), and how many downtime windows are needed, with warnings when a phase exceeds one window or the batch size is outside the usual range. Add `--record-bytes 2048 --memory-mb 64` to check that one batch fits a memory budget; `--json` for machine output.

## Further reading

- Kleppmann and Riccomini, Designing Data-Intensive Applications (2nd ed.)
- Perkins et al., Seven Databases in Seven Weeks
- Ambler and Sadalage, Refactoring Databases
- Reis and Housley, Fundamentals of Data Engineering
- Sadalage and Fowler, NoSQL Distilled
