## Contents

- Why migrations are never copy and paste
- Strategy factors
- Big bang versus phased
- Batch sizing
- ETL stages and their failure modes
- Synchronization during transition
- Schema version control
- How Flyway-style tools work
- Schema versioning rules
- Data transformations with schema changes
- Migration runbook
- Pitfalls
- Practice drills

# Data Migration and Schema Evolution

## Why migrations are never copy and paste

Moving data between systems (an engine upgrade, relational to NoSQL or back, a new external service, merging several sources) is a recurring job across a career. It looks like a copy; in reality it needs planning, execution and validation, or you risk loss and corruption.

## Strategy factors

Choose the migration approach from: data volume, system complexity, available downtime, risk tolerance, and business requirements.

## Big bang versus phased

| | Big bang | Phased |
|---|---|---|
| What moves | Everything in one cutover, usually in a downtime window | One segment at a time, each validated before the next |
| Pros | Simpler to orchestrate; no long dual-running period | Lower blast radius; lessons from early phases improve later ones |
| Cons | All-or-nothing risk | Takes longer; needs synchronization while systems coexist |

Guidance:

- First migration project, or high-stakes data: go phased.
- Segment along a natural boundary (department, region, customer tier, tenant) and start with the segment whose failure hurts least.
- Example (invented): moving a company directory, migrate the internal tools team first, then support staff, then sales, and payroll-relevant records last.

## Batch sizing

When code processes the data, work in batches so memory stays bounded. 1,000 to 10,000 records per batch is a reasonable starting range, but confirm with a proof-of-concept run on your hardware and data before committing to a number. The bundled `migration_batch_planner.py` script turns PoC measurements into batch counts, duration estimates and a window-fit check.

## ETL stages and their failure modes

| Stage | Job | What goes wrong |
|---|---|---|
| Extract | Read from the source | Rate limits; load on a live production source |
| Transform | Reshape to the target's format and rules | Data-quality problems invisible in the small PoC sample |
| Load | Write into the target | Constraint and validation failures |

Treat each stage as a separate component with its own boundary. Invest in error handling and logging from the start: for every rejected record you want what failed, when and why, so you can fix and rerun quickly. A dead-letter table of rejects with reasons is a cheap way to get this.

## Synchronization during transition

Phased migrations create a period where both systems are live: a new hire created mid-migration must exist in old and new stores. Tools:

- **Message queues** to propagate updates asynchronously
- **Change data capture (CDC)** to stream row-level changes from the source's log
- **Reconciliation jobs** that compare the systems and repair drift

## Schema version control

Schemas change constantly: tables appear, columns are added, dropped, renamed or retyped. A schema without version control has the same risks as code without it: lost history, overwritten teammates' work, and no rollback. Version the schema with the same discipline as the code, in the same repository.

Tools: Flyway, Liquibase, Rails migrations (and equivalents such as Alembic or EF Core migrations). They record which changes each environment has applied so dev, test and production stay aligned.

## How Flyway-style tools work

1. Keep a history table in the target database (Flyway's is `flyway_schema_history`).
2. Scan a migrations folder for files that follow a naming convention, such as `V7__add_status_to_orders.sql`.
3. Diff discovered scripts against the history table.
4. Apply the unapplied ones in version order and record each.

Migrations run sequentially: going from version 100 to 250 applies every step in between. That is a deliberate safety property, since each script builds on the exact prior state and failures are easy to localize. Squashing or shortcut paths exist for advanced cases, but sequential is the norm.

Migrations can be plain SQL or written in the application language (Flyway supports Java-based migrations), which helps when the transformation needs real parsing or business logic.

## Schema versioning rules

1. **Idempotent scripts:** safe to run twice (`CREATE TABLE IF NOT EXISTS`, guarded updates).
2. **Backward compatible when possible:** the old application version should still work against the new schema during rollout.
3. **Schema change and its data transformation ship together**, in the same versioned migration, so structure and data never diverge across environments.

## Data transformations with schema changes

Benefits of versioning them together:

- Structure and data stay consistent with each other.
- With transactional DDL, the change is atomic: schema and data both apply or neither does.
- The history table tells you which environments already ran it.

Example (invented): normalize a legacy `phone` text column into `phone_e164` for SMS delivery.

```python
def migrate(conn, to_e164, batch=5000):
    conn.execute("ALTER TABLE contacts ADD COLUMN IF NOT EXISTS phone_e164 TEXT")
    last_id = 0
    while True:
        rows = conn.fetch("SELECT id, phone FROM contacts WHERE id > %s "
                          "AND phone_e164 IS NULL ORDER BY id LIMIT %s",
                          (last_id, batch))
        if not rows:
            break
        for cid, raw in rows:
            try:
                value = to_e164(raw)            # business rule lives in app code
            except ValueError:
                log_reject("contacts", cid, raw)
                continue
            conn.execute("UPDATE contacts SET phone_e164 = %s WHERE id = %s",
                         (value, cid))
        last_id = rows[-1][0]
```

Note the `IS NULL` guard (idempotent rerun), keyset batching (bounded memory) and reject logging. Contracting the schema (dropping the old `phone` column) belongs in a later migration, after every reader has switched.

For heavy transformations:

- Run them as background jobs to limit production impact.
- Use dual writes (old and new shape) during the transition.
- Write the rollback plan before starting.

Expect dirty data: missing values, malformed formats and cases nobody imagined. Always trial on a small sample, validate thoroughly, then scale to the full set.

## Migration runbook

1. Inventory: volume, sources, consumers, downtime allowance, risk tolerance.
2. Choose big bang or phased; define segments and order.
3. PoC on a representative sample; measure throughput, pick batch size.
4. Build ETL with per-record error logging and a reject store.
5. Set up sync (queue, CDC) and reconciliation if systems coexist.
6. Version every schema and data change in the migration tool.
7. Dry run in staging with production-like data; compare counts and checksums.
8. Execute, validate each phase, keep the rollback path ready.
9. Retire the old path only after reconciliation is clean.

## Pitfalls

- Treating migration as a one-off script nobody versions.
- Testing transformations only on clean sample data.
- Loading whole tables into memory.
- Renaming or dropping a column in the same release that stops writing it.
- No reconciliation during dual running.

## Practice drills

- Build a tiny app with a migration tool, then evolve the schema three times (add a column, change a type, split a table) without losing data.
- Write a CSV-to-database loader that logs every rejected row with a reason, and run it on a deliberately messy file.
