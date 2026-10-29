# Data Topology Alignment

## Contents
- Why this intersection is easy to miss
- Topology must fit the style
- Match database strengths to architecture strengths
- Match the database type to the shape of the data
- Match the database type to the read/write balance
- Decision procedure
- Worked example

## Why this intersection is easy to miss

Teams choose a style carefully, then default to whatever database they already run. A wrong database type or topology can neutralize the very characteristics the style was chosen for. General tendencies:
- A single shared (monolithic) database gives strong consistency and easy transactions but limits scalability and fault tolerance.
- Distributed database topologies help scalability and change isolation but cost data integrity, consistency and often performance.

## Topology must fit the style

Three basic physical topologies:

| Topology | Typical fit |
|---|---|
| Monolithic (one shared database) | Monolithic styles, simple or cost-constrained systems |
| Domain-based (one database per domain, shared by that domain's services) | Service-based architecture and other coarse-grained distributed styles |
| Database per service | Microservices, where each service owns its data to keep a tight bounded context |

Rules:
- Microservices without database-per-service loses change control, and suffers in fault tolerance, scalability, elasticity, maintainability, testability and deployability.
- Service-based architecture is tolerant: it can work with a monolithic or domain-split database, so topology there is a softer decision.

## Match database strengths to architecture strengths

Each database type, like each architecture style, has things it excels at and things it does poorly. Pick a type whose strengths amplify the style's strengths. The companion book (Software Architecture: The Hard Parts) compares relational, key-value, document, columnar, graph and NewSQL databases.

Qualitative guidance:
- Styles whose standout traits are scalability and elasticity (microservices, event-driven, space-based) pair well with key-value and columnar stores, which share those traits.
- Relational databases bring strong consistency and rich querying but are harder to scale out; use them where consistency and relationships dominate.
- Do not pair a style chosen for extreme elasticity with a database that becomes the bottleneck under that elasticity.

## Match the database type to the shape of the data

- Hierarchical, interdependent relationships: relational.
- Self-contained payloads such as JSON events or request bodies: document.
- Lookups by identifier with no relational needs: key-value. Forcing key/value pairs into relational tables wastes effort in both the database and the code.
- Data within one system is often mixed. Prefer polyglot persistence (several database types, each matched to its data) whenever it is practical.

## Match the database type to the read/write balance

| Dominant workload | Better fit |
|---|---|
| Heavy writes, occasional reads | Columnar |
| Heavy reads | Key-value, document or graph |
| Reads and writes roughly balanced | Relational or NewSQL |

Getting this wrong mainly shows up as poor performance.

## Decision procedure

1. Identify the architecture style and its top characteristics.
2. Choose the topology the style expects (shared, domain, per service). Flag any deviation as an ADR with its consequences.
3. For each data set, classify its structure (relational, document, key-value, graph-like).
4. For each data set, classify its workload (write-heavy, read-heavy, balanced).
5. Pick the type that fits structure and workload and does not weaken the style's top characteristics.
6. If the answers differ across data sets, use polyglot persistence and accept the operational cost explicitly.

## Worked example

An IoT telemetry platform uses event-driven architecture for scale and elasticity. Sensor readings arrive constantly and are rarely read individually: columnar store. Device metadata (owner, site, firmware) is relational and changes rarely: relational database. Live dashboards read the latest reading per device very frequently: key-value cache keyed by device ID. A single relational database for all three would have capped ingest throughput and undercut the elasticity that motivated the style.
