---
name: fse-theme-design-and-architecture
description: Theme skill on designing software from Schutta and Vega's "Fundamentals of Software Engineering" (chapters 4, 7, 8 and 9). Use when choosing and drawing diagrams, designing usable and accessible user interfaces, picking data formats, databases, consistency and caching strategies, tuning queries or planning data migrations, and when making architecture decisions: trade-offs, quality attributes, styles, fitness functions and ADRs.
---

# Design and architecture (Fundamentals of Software Engineering, ch. 4, 7, 8, 9)

Design decisions at every scale, from a dialog box to a database to the overall architecture, share one discipline: understand the context, make trade-offs explicit, and communicate them clearly.

## Cross-chapter rules

1. **No best answer, only trade-offs.** Name the factors behind "it depends", weight options by priority, and accept the least-bad choice for the current context.
2. **Ask before designing.** Users, scale, availability, latency, data retention, regulation, security, cost; identify quality attributes, including implied ones, and rank a short list.
3. **Diagrams communicate, not decorate.** Pick the view for the audience and question, keep notation simple, split large views, keep them accurate (or generated) and give color a legend.
4. **Code is the final design.** Prefer sketches for thinking and generated diagrams for accuracy over heavy up-front models.
5. **You are not the user.** Do quick research, design accessibility and internationalization in from the start, prevent errors, write helpful error messages, support undo, and make destructive actions deliberately harder. Check color contrast with `scripts/contrast_check.py`.
6. **Fit data choices to the workload.** Choose formats, databases and persistence abstractions by need, set consistency per data type by the cost of being wrong, cache only for measured bottlenecks, and scale in steps.
7. **Measure before tuning queries,** and migrate data in phased, verified batches (`scripts/migration_batch_planner.py`) with versioned schema changes.
8. **Architecture evolves.** Prefer incremental change with hypotheses and thresholds, guard key qualities with automated fitness functions, and choose distributed styles only when their benefits rank highest.
9. **Record the why.** Numbered, immutable ADRs linked to governance (`scripts/adr_tool.py`).

## Default workflow

1. Gather context and rank quality attributes (ch09).
2. Sketch and validate the design with the right diagrams (ch04).
3. Decide data storage, consistency, caching and migration approach (ch08).
4. Design the interface for real users and accessibility (ch07).
5. Record decisions in ADRs and add fitness functions (ch09).

<!-- BEGIN GENERATED: run tools/build_bundles.py to refresh -->

## References by chapter

Each link is one level deep; read only the files whose description matches the task.

### CH04: Modeling

- [ch04-diagram-catalog.md](references/ch04-diagram-catalog.md): read when choosing which diagram to create, judging formality for an audience, or explaining why and when modeling pays off; includes a selection matrix and workshop techniques.
- [ch04-modeling-practices-and-tools.md](references/ch04-modeling-practices-and-tools.md): read when drawing, reviewing or cleaning up a diagram, setting team diagram standards, choosing a tool, deciding on diagrams as code, or planning practice exercises.

### CH07: User Interface Design

- [ch07-accessibility-and-globalization.md](references/ch07-accessibility-and-globalization.md): read when planning or reviewing accessibility, localization, internationalization, RTL support or cultural fit.
- [ch07-discoverability-errors-and-destructive-actions.md](references/ch07-discoverability-errors-and-destructive-actions.md): read when deciding what to expose or hide, designing shortcuts, writing error messages, building delete or other irreversible flows, or setting practice exercises.
- [ch07-usability-qualities-and-prioritization.md](references/ch07-usability-qualities-and-prioritization.md): read when auditing usability or deciding which qualities to optimize for a product's usage pattern; includes the efficiency multiplier example.
- [ch07-user-research-and-defaults.md](references/ch07-user-research-and-defaults.md): read when gathering user requirements, considering secondary users, or choosing, persisting and instrumenting defaults.
- [ch07-visual-design-principles.md](references/ch07-visual-design-principles.md): read when laying out or critiquing a screen's visual hierarchy, grouping, alignment and consistency.

### CH08: Working with Data

- [ch08-consistency-caching-and-growth.md](references/ch08-consistency-caching-and-growth.md): read when choosing consistency models, reasoning about CAP, designing or rejecting a cache, or planning scaling (replicas, sharding) and growth reviews.
- [ch08-data-types-and-formats.md](references/ch08-data-types-and-formats.md): read when deciding structured versus unstructured handling, choosing JSON, XML, CSV or YAML, or handling binary data, timestamps or datasets too large for memory.
- [ch08-database-selection-and-persistence.md](references/ch08-database-selection-and-persistence.md): read when picking a database family, choosing between raw SQL, a repository and an ORM, or setting up connection pools and transaction boundaries.
- [ch08-migration-and-schema-evolution.md](references/ch08-migration-and-schema-evolution.md): read when planning a data migration, ETL or dual-running sync, or adding versioned schema and data migrations.
- [ch08-query-performance.md](references/ch08-query-performance.md): read when a query or endpoint is slow, when designing indexes or pagination, reading EXPLAIN output, sizing a pool from metrics, or trading ORM readability for SQL speed.

### CH09: Software Architecture

- [ch09-adrs-and-architecture-diagrams.md](references/ch09-adrs-and-architecture-diagrams.md): read when writing or reviewing an ADR, managing ADR status, or choosing a diagram for an audience.
- [ch09-architecture-thinking-and-trade-offs.md](references/ch09-architecture-thinking-and-trade-offs.md): read when scoping a new system, running a trade-off analysis (library vs service worked example), or deciding whether something is architecture or design.
- [ch09-evolutionary-architecture-and-fitness-functions.md](references/ch09-evolutionary-architecture-and-fitness-functions.md): read when working in Agile teams, writing a hypothesis for an architectural change, or designing and maintaining fitness functions (includes sample checks).
- [ch09-practice-with-architectural-katas.md](references/ch09-practice-with-architectural-katas.md): read when the user wants to practice architecture, run a kata session or interview, or asks for further reading.
- [ch09-quality-attributes-and-styles.md](references/ch09-quality-attributes-and-styles.md): read when extracting and ranking quality attributes from requirements, persuading stakeholders, or choosing between monolithic and distributed styles.

Merged section maps: [source-maps.md](references/source-maps.md).

## Scripts

Python 3 standard library only; run any script with `--help` for its arguments.

| Script | Purpose |
|---|---|
| `scripts/contrast_check.py` (ch07) | WCAG 2.x color contrast checker for foreground/background pairs. |
| `scripts/migration_batch_planner.py` (ch08) | Plan batches and timing for a big bang or phased data migration. |
| `scripts/adr_tool.py` (ch09) | Create and lint Architectural Decision Records (ADRs) kept as Markdown files. |

<!-- END GENERATED -->
