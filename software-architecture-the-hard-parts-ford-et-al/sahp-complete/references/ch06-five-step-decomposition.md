# Five-Step Decomposition of a Monolithic Database

## Contents
- Data domains
- Visualizing domains and cross-domain dependencies
- Step 1: analyze the database and identify data domains
- Step 2: assign tables to domain schemas
- Step 3: separate database connections per domain
- Step 4: relocate each schema onto its own server
- Step 5: switch over to the independent servers
- After the split
- Checklists per step
- Glossary
- Pitfalls

## Data domains

A data domain is a cluster of database artifacts (tables, views, foreign keys, triggers, procedures) that belong to one business area and are normally used together inside a narrow functional scope. It is the unit that moves; individual tables are too fine-grained to migrate safely one at a time.

**Data domain versus schema.** A data domain is an architectural idea; a schema is the database construct that holds a domain's objects. The mapping is usually one-to-one, but one domain may span several schemas, especially after merging domains whose tables are too intertwined to separate. In practice the two words are used interchangeably.

**Rule:** the bounded-context rule applies at domain level. A service talks to exactly one data domain. Anything it needs from another domain comes through that domain's owning service.

Invented assignment for a library-management system:

| Table | Domain |
|---|---|
| member, member_address | Membership |
| book, author, book_author, copy | Catalog |
| loan, reservation, overdue_notice | Circulation |
| fine, payment | Billing |

## Visualizing domains and cross-domain dependencies

Picture the database as a soccer ball: each white patch is a domain holding its tables and their internal links. Draw links within a patch as solid lines (they survive) and links between patches as dashed lines (they must be cut). The dashed lines are the work list: cross-domain foreign keys, views joining tables from two domains, triggers updating another domain's table, and procedures or functions touching foreign tables. The script `data_domain_check.py` produces this list from a table-to-domain mapping and a dependency inventory.

Database teams should use the refactoring patterns from Ambler and Sadalage's "Refactoring Databases" to remove these links safely and incrementally (for example, drop foreign key, introduce transition periods, replace views).

**Example of cutting a view (invented).** A Billing view joins `fine` with `member` to show the member's name next to each fine. Once Membership is its own domain, rewrite the view to use only Billing tables (keep `member_id`, drop the name). The Billing service then calls the Membership service for names. Every such cut moves an integration point from SQL into the application layer, with the latency and consistency cost that implies.

## Step 1: analyze the database and identify data domains

Starting state: every service can read and write every table (the shared database integration style from Hohpe and Woolf's "Enterprise Integration Patterns"). This is the tight coupling that makes change control painful.

Actions:
- Inventory tables and every coupling artifact (FKs, views, triggers, procedures, functions, synonyms).
- Group tables by business area and co-usage. Usage logs, query plans and the service-to-table access matrix help.
- Name candidate domains and record ambiguous tables.

## Step 2: assign tables to domain schemas

Create one schema per domain and move each table into its schema. In SQL Server style this is a schema transfer statement; in Oracle a schema is effectively a user.

```sql
-- invented: move the fine table into the billing schema
ALTER SCHEMA billing TRANSFER legacy.fine;
```

If tables in different domains are too tightly coupled to separate, merge those domains into a broader bounded context that several services share (merging and shared ownership are treated in later chapters).

**Synonyms as a transition aid.** A synonym is an alias, similar to a symbolic link, for an object in another schema or server. Creating one in the consuming schema lets a cross-domain query refer to a local-looking name:

```sql
CREATE SYNONYM circulation.member FOR membership.member;
-- circulation queries now join circulation.member
```

Trade-off: a synonym still needs read or write privileges on the target and does not actually remove the cross-schema query; it just hides it. Its value is that every cross-domain reference becomes an explicit, searchable object, which simplifies dependency analysis and later removal. Treat synonyms as scaffolding to be dismantled in Step 3, not as an end state.

## Step 3: separate database connections per domain

Refactor each service's connection configuration so it connects only to its own domain's schema, with read and write rights limited to that schema. All cross-schema access must now be resolved in services: where a service used to join another domain's table, it calls the owning service instead. Remove every synonym created in Step 2.

This is the hardest step, because every hidden cross-domain query surfaces as a code change.

**Key guideline:** never reach into another domain's database; go through the service that owns it.

Completing Step 3 yields **data sovereignty per service**: each service owns its data. It is the ideal end state for distributed architectures, with clear costs:

| Benefits | Costs |
|---|---|
| Schema changes stay inside the owning domain | Bulk access to another domain's data becomes slow (remote calls instead of joins) |
| Each service can pick the database type and technology that fits | Referential integrity is no longer enforced by the database, so data quality can degrade |
| | Any procedure or function touching other domains' tables must be rewritten in the service layer |

## Step 4: relocate each schema onto its own server

Separate schemas on one server still form a single architecture quantum: a server crash, a noisy neighbor or a capacity limit hits all domains. Moving domains to their own servers is what delivers the scalability, fault tolerance and performance benefits.

Two migration options:

| Option | Sequence | Pros | Cons |
|---|---|---|---|
| Backup and restore | Back up each domain schema, stand up a server per domain, restore, repoint services, drop schemas from the old server | Simple, low tooling effort | Usually needs downtime |
| Replication | Stand up a server per domain, replicate schemas, repoint services, drop schemas from the old server | Avoids downtime | More setup work and more coordination |

Choose replication when the domain cannot tolerate an outage window; choose backup and restore when a maintenance window is acceptable and the team wants the simplest route.

## Step 5: switch over to the independent servers

When replication has fully caught up, switch each service's connection to the new server, then remove the old connections and delete the domain's schema from the original server. Each domain and its services now deploy and operate independently.

## After the split

With domains on independent servers, teams can:
- Tune each server separately for availability and scalability.
- Re-evaluate the best database type per domain and introduce polyglot persistence where justified (see the database type selection reference).

## Checklists per step

Step 1
- [ ] Complete artifact inventory, including triggers and procedures
- [ ] Service-to-table access matrix (read versus write)
- [ ] Candidate domains named; ambiguous tables listed

Step 2
- [ ] One schema per domain, every table placed
- [ ] Domains merged where coupling is too strong to cut
- [ ] Each remaining cross-domain reference made explicit (synonym or ticket)

Step 3
- [ ] Each service has credentials for one schema only
- [ ] All cross-domain joins replaced by service calls or local copies
- [ ] All synonyms dropped; cross-domain procedures moved to services
- [ ] Integrity checks that FKs used to provide now implemented in services

Step 4
- [ ] Migration option chosen per domain (downtime tolerance)
- [ ] New servers sized from the measured per-domain connection and load profile

Step 5
- [ ] Replication lag zero before cutover
- [ ] Old connections removed, old schemas deleted
- [ ] Per-server tuning and database type review scheduled

## Glossary

- **Cross-domain dependency:** any FK, view, trigger, function, procedure or synonym linking objects in two different data domains.
- **Data sovereignty per service:** each service is the sole owner (writer) of its data; others access it only through the service.
- **Shared database integration:** many applications or services integrating by reading and writing the same tables.
- **Synonym:** a database alias for an object in another schema or server.

## Pitfalls

- Jumping to separate servers before connections are isolated: the hidden cross-schema queries will break on cutover.
- Leaving synonyms in place permanently and calling the job done.
- Cutting every FK by default instead of merging domains whose integrity rules are essential.
- Forgetting that stored procedures and triggers are code; they must be found and moved.
- Excluding DBAs from the plan; the process depends on them executing the refactorings.
