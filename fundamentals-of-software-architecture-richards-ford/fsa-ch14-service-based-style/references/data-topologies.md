# Data Topologies and Shared Entity Libraries

## Contents
- Database topology options
- Rule for splitting the database
- Why shared-database schema change is risky
- Antipattern: one shared entity library
- Pattern: logical partitions with matching libraries
- Handling the common partition
- Change-impact checklist
- Worked example

## Database topology options

Service-based architecture is unusual among distributed styles in that a single shared database is a legitimate, well-supported choice. The options form a spectrum:

| Topology | Coupling | Typical reason to choose |
|---|---|---|
| One shared database | Highest; all services in one quantum | Cross-domain joins, reporting, ACID simplicity |
| Several databases, each shared by a group of services | Medium | Separate security zones, separate user populations, partial independence |
| One database per domain service | Lowest; similar to microservices | Strong independence for domains whose data no one else needs |

## Rule for splitting the database

Only give a service (or group) its own database when no other service needs that data. If a split forces services to call each other to fetch data they previously read directly, you have traded a schema-coupling problem for a runtime-coupling problem. In this style, sharing data is generally preferred over adding service-to-service calls.

## Why shared-database schema change is risky

A careless change to a table in the shared database can ripple into every service. Schema change therefore becomes costly and needs coordination, effort and care. The mitigation is not to avoid the shared database but to control how its schema is represented in code.

## Antipattern: one shared entity library

Services usually access tables through **entity objects** (classes mirroring table schemas), sometimes with SQL, packaged as a shared binary (a JAR, DLL, wheel, npm package and so on).

Putting every entity for every table into one library is the weakest way to build the style:

- Any table change alters the library.
- Every service consumes the library, so every service must be rebuilt, retested and redeployed, even services that never touch the changed table.
- Versioning the library softens this, but nobody can easily tell which services are really affected without tedious manual analysis.

Flag this whenever you see a single `entities` or `model` package imported by all services.

## Pattern: logical partitions with matching libraries

1. Partition the database **logically** into data domains (for example: common, customer, invoicing, order, tracking). Physical separation is not required.
2. Create one shared entity library per logical partition.
3. Each service depends only on the libraries for partitions it actually uses.
4. A change to a table in, say, the invoicing partition modifies only the invoicing library. Only services depending on that library are retested and redeployed.

Guidance: make the logical partitions as fine-grained as you can while each one still represents a coherent data domain. Finer partitions mean smaller change impact; partitions that no longer map to a real domain create confusion.

## Handling the common partition

Most systems end up with a partition of tables every service uses (reference data, users, configuration). Changes there still touch all services. Mitigations:

- Lock the common entity library in version control so only the database team can change it.
- Treat any change to it as a coordinated, all-services event with explicit review.

This makes the cost of touching shared tables visible and deliberate.

## Change-impact checklist

When a schema change is proposed, the agent should answer:

1. Which logical partition owns the table?
2. Which entity library maps that partition?
3. Which services declare a dependency on that library? (Those, and only those, need retest and redeploy.)
4. Is the table in the common partition? If yes, route to the database team and plan an all-services release.
5. Does a single library cover everything? If yes, record the antipattern and propose partitioning.

## Worked example

A logistics platform has six domain services and one database. Today a single `core-entities` library holds 140 entity classes. Adding a column to `shipment_label` forces all six services through release.

Refactor: define partitions `common`, `booking`, `shipment`, `billing`, `fleet`. Split the library into five. After the split, the `shipment_label` change touches `shipment-entities`, used by Shipping and Tracking only. Four services are untouched. The `common-entities` library is placed under database-team ownership.
