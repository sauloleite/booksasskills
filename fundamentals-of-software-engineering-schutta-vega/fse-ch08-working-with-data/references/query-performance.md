## Contents

- Mindset
- Query hygiene: projection and limits
- Prepared statements
- Index management
- Large result sets and pagination
- Execution plans (EXPLAIN)
- Monitoring and observability
- Balancing readability against performance
- Slow-query playbook
- Practice drills

# Query Performance

## Mindset

Working is not the same as fast. Once a query returns the right rows, the next question is how to make it cheaper. A good query versus a careless one can be the difference between seconds and milliseconds, and slowness frustrates users regardless of UI polish.

## Query hygiene: projection and limits

Two silent costs hide in innocent queries:

1. `SELECT *` drags every column over the wire and into memory, including wide text and blobs you never read.
2. Unbounded result sets load thousands of rows at once.

Fix: name the columns the caller needs (often a slim summary DTO instead of the full entity) and bound the result with `LIMIT` or pagination (20 to 50 rows per page is typical for UIs). Explicit column lists also document the data contract of that code path. On large tables this alone can yield order-of-magnitude gains.

## Prepared statements

Building SQL by string concatenation forces a fresh parse and plan on every call and opens the door to SQL injection. Parameterized (prepared) statements:

- Let the database parse and plan once and reuse the plan with new parameter values; for hot queries this plan reuse can cut execution time by roughly 20% to 50%.
- Escape parameters automatically, defeating injection without hand-rolled sanitizing.

```python
# Wrong: injection risk and no plan reuse
cur.execute(f"SELECT id FROM users WHERE email = '{email}'")
# Right
cur.execute("SELECT id FROM users WHERE email = %s", (email,))
```

Rule: no user-supplied value is ever concatenated into SQL. Treat any exception as a code-review blocker.

## Index management

An index is a lookup structure from column values to row locations, turning a full table scan into a direct seek, like a book's back-of-book index. Illustrative magnitude: an email lookup on an unindexed table taking around 2 seconds can drop to a few milliseconds once indexed (hundreds of times faster).

Indexes cost storage and slow every insert, update and delete, because each index must be maintained.

Index candidates:

- Columns in frequent `WHERE` filters
- Join keys
- `ORDER BY` and `GROUP BY` columns
- Composite indexes for queries that filter on several columns together (order columns to match the query's filters)

Avoid indexing low-cardinality columns (booleans, small status enums) on their own; the index rarely beats a scan. Revisit indexes as query patterns change.

```sql
CREATE INDEX idx_orders_customer_created ON orders (customer_id, created_at);
-- serves: WHERE customer_id = ? ORDER BY created_at DESC
```

## Large result sets and pagination

Development databases hide volume problems; production tables do not. Paginate any list that can grow.

Offset pagination (`LIMIT n OFFSET k`) plus a `COUNT(*)` for the total is the common first version. Two problems at scale:

- The database must walk and throw away the first k rows, so deep pages get slower and slower.
- The total count re-scans every matching row on each request.

Alternatives:

| Technique | How | Use when |
|---|---|---|
| Keyset (seek) pagination | `WHERE id > :last_seen_id ORDER BY id LIMIT n` | Large tables, sequential browsing, infinite feeds |
| Cached counts | Store the total and refresh periodically | Totals change slowly |
| Estimated counts | Use planner statistics or approximate counters | Huge tables where "about 1.2M results" is fine |
| Count-free UI | Infinite scroll or "next" only | Users do not need page numbers |

```sql
SELECT id, title, unit_price FROM items
WHERE category = $1 AND id > $2
ORDER BY id
LIMIT 50;
```

## Execution plans (EXPLAIN)

The query planner (optimizer) compiles SQL into an execution plan. It weighs indexes, table statistics and alternative strategies.

- **Rule-based** optimizers apply fixed rules (for example, always use an available index).
- **Cost-based** optimizers enumerate candidate plans and pick the cheapest estimate. Almost every modern engine is cost-based.

Engine notes:

- **PostgreSQL:** builds scan options for each table, chooses indexes and compares join orders; for queries with many joins it switches to a genetic optimizer that finds a good-enough plan quickly.
- **MySQL:** cost-based, particularly strong on read paths; weighs access methods, join types and join order.
- **Oracle:** very sophisticated, with adaptive plans that can change mid-execution from runtime statistics.

Usage: `EXPLAIN <query>` shows the planned approach; `EXPLAIN ANALYZE` (PostgreSQL, MySQL) actually runs it and shows real timings and row counts next to estimates. Syntax and output vary by engine. Run `ANALYZE` variants on writes only inside a transaction you roll back.

What a plan shows: table access order, join algorithm (nested loop, merge, hash), index usage per table, scan type (sequential or index), estimated or actual cost, estimated versus actual rows.

Red flags:

- Sequential scan on a large table where a selective filter should use an index
- A join algorithm that does not suit the row counts (for example, nested loop over two big inputs)
- An index that exists but is not used, or is missing
- Very high cost or row estimates
- Estimated rows far from actual rows (stale statistics, skewed data)

**Cross-environment comparison:** when something is fast in staging and slow in production after a deploy, diff the plans between environments. Missing indexes, stale statistics and different data distributions show up immediately; this often finds the root cause faster than other debugging.

## Monitoring and observability

EXPLAIN shows ideal-conditions behavior; production behavior under load needs observability, meaning you can infer internal state from what the system emits. Database-side tools (slow-query log, `pg_stat_statements`) are only half the view; add the application's perspective.

The three pillars:

- **Logs:** events and errors, correlated with metrics and traces.
- **Metrics:** pool usage (active, idle, pending), query and transaction durations, error rates.
- **Traces:** one request's path across components and services, with database calls as spans.

Diagnostic questions and the signal that answers each:

| Question | Signal | Likely action |
|---|---|---|
| Is the pool a bottleneck? | High pending count; active pinned at max | Grow the pool, or find leaks and long transactions |
| Is the pool oversized? | Active persistently low, idle persistently high | Shrink it; free memory and DB resources |
| Why is this request slow? | Trace where one DB span dominates (say 90% of time) | EXPLAIN that query |
| Is there an N+1? | Trace with dozens of tiny sequential queries in one operation | Fix ORM fetching (join fetch, batch load) |
| Is a query degrading? | Query-time metrics trending up versus deploys or data growth | Optimize before it becomes an incident |
| How do DB errors hurt users? | DB errors (constraint violations, deadlocks, connectivity) correlated with failed requests | Prioritize by user impact |

In Spring Boot, Actuator plus Micrometer instrument the DataSource (HikariCP by default) and expose these pool metrics with little configuration; equivalents exist in most stacks (OpenTelemetry instrumentation, framework metrics).

## Balancing readability against performance

Typical tension: a derived ORM query plus in-memory stream filtering is pleasant to read but drags extra rows and columns into the app; a hand-written SQL join with the filter in `WHERE` and only the needed columns is faster but tied to the schema and harder to maintain.

Decide with five factors: data scale, performance requirement, maintenance burden, team SQL fluency, future flexibility.

Default: use the ORM for most operations and drop to SQL on the measured hot paths. Push filtering, sorting and aggregation into the database whenever the dataset is not trivially small.

## Slow-query playbook

1. Reproduce and measure (trace or timing, with production-like data).
2. Confirm the culprit span or query in traces.
3. Run EXPLAIN, then EXPLAIN ANALYZE in a safe environment.
4. Fix in order: projection and limits, parameterization, missing index, query rewrite, pagination strategy, caching.
5. Re-measure and compare the plan before and after.
6. Add a metric or alert so regressions surface early.

## Practice drills

- Find a slow query in a current project, capture its plan, add or adjust an index or rewrite it, and record before/after timings and plans.
- Convert an offset-paginated endpoint to keyset pagination and benchmark page 1 versus page 1,000.
