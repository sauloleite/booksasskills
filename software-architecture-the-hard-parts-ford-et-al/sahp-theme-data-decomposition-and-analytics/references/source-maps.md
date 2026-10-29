# Source maps: book sections to reference files

File names below are the chapter-prefixed names used in this folder.

## Source Map: Chapter 6, Pulling Apart Operational Data

| Chapter section | Covered in |
|---|---|
| Chapter opening story (data team resists the split) | [ch06-decomposition-drivers.md](ch06-decomposition-drivers.md) (Building the justification) |
| Chapter introduction (why data is harder to split; code-to-data analogy) | [ch06-decomposition-drivers.md](ch06-decomposition-drivers.md) |
| Data Decomposition Drivers | [ch06-decomposition-drivers.md](ch06-decomposition-drivers.md) |
| Data Disintegrators | [ch06-decomposition-drivers.md](ch06-decomposition-drivers.md) |
| Change Control (bounded context, contract abstraction) | [ch06-decomposition-drivers.md](ch06-decomposition-drivers.md) |
| Connection Management (quotas, even versus variable distribution) | [ch06-decomposition-drivers.md](ch06-decomposition-drivers.md), script `connection_budget.py` |
| Scalability | [ch06-decomposition-drivers.md](ch06-decomposition-drivers.md), script `connection_budget.py` |
| Fault Tolerance | [ch06-decomposition-drivers.md](ch06-decomposition-drivers.md) |
| Architectural Quantum | [ch06-decomposition-drivers.md](ch06-decomposition-drivers.md) |
| Database Type Optimization | [ch06-decomposition-drivers.md](ch06-decomposition-drivers.md), [ch06-database-type-selection.md](ch06-database-type-selection.md) |
| Data Integrators | [ch06-decomposition-drivers.md](ch06-decomposition-drivers.md) |
| Data Relationships | [ch06-decomposition-drivers.md](ch06-decomposition-drivers.md) |
| Database Transactions | [ch06-decomposition-drivers.md](ch06-decomposition-drivers.md) |
| Sysops Squad Saga: Justifying Database Decomposition | [ch06-decomposition-drivers.md](ch06-decomposition-drivers.md) (Building the justification) |
| Decomposing Monolithic Data (data domains, soccer-ball view, cutting views) | [ch06-five-step-decomposition.md](ch06-five-step-decomposition.md), script `data_domain_check.py` |
| Step 1: Analyze Database and Create Data Domains | [ch06-five-step-decomposition.md](ch06-five-step-decomposition.md) |
| Step 2: Assign Tables To Data Domains (schemas, synonyms) | [ch06-five-step-decomposition.md](ch06-five-step-decomposition.md) |
| Data Domain vs. Database Schema (sidebar) | [ch06-five-step-decomposition.md](ch06-five-step-decomposition.md) |
| Step 3: Separate Database Connections To Data Domains (data sovereignty) | [ch06-five-step-decomposition.md](ch06-five-step-decomposition.md), script `data_domain_check.py --access` |
| Don't Reach Into Other Databases (sidebar) | [ch06-five-step-decomposition.md](ch06-five-step-decomposition.md) |
| Step 4: Move Schemas To Separate Database Servers | [ch06-five-step-decomposition.md](ch06-five-step-decomposition.md) |
| Step 5: Switch over to independent database servers | [ch06-five-step-decomposition.md](ch06-five-step-decomposition.md) |
| Selecting a Database Type (evaluation characteristics) | [ch06-database-type-selection.md](ch06-database-type-selection.md) |
| Relational Databases | [ch06-database-type-selection.md](ch06-database-type-selection.md) |
| Aggregate Orientation (sidebar) | [ch06-database-type-selection.md](ch06-database-type-selection.md) |
| Key-Value Databases | [ch06-database-type-selection.md](ch06-database-type-selection.md) |
| Sharding in Databases (sidebar) | [ch06-database-type-selection.md](ch06-database-type-selection.md) |
| Document Databases | [ch06-database-type-selection.md](ch06-database-type-selection.md) |
| Schema-less Databases (sidebar) | [ch06-database-type-selection.md](ch06-database-type-selection.md) |
| Column Family Databases | [ch06-database-type-selection.md](ch06-database-type-selection.md) |
| Graph databases | [ch06-database-type-selection.md](ch06-database-type-selection.md) |
| Changing Relationship Types (sidebar) | [ch06-database-type-selection.md](ch06-database-type-selection.md) |
| NewSQL Databases | [ch06-database-type-selection.md](ch06-database-type-selection.md) |
| Cloud Native Databases | [ch06-database-type-selection.md](ch06-database-type-selection.md) |
| Time series Databases (and product summary) | [ch06-database-type-selection.md](ch06-database-type-selection.md) |
| Sysops Squad Saga: Polyglot Databases (business justification, embed versus reference aggregates) | [ch06-database-type-selection.md](ch06-database-type-selection.md) (Justifying a new database type; Aggregate design) |

## Source Map: Chapter 14, Managing Analytical Data

| Chapter section | Covered in |
|---|---|
| Chapter introduction (operational vs analytical data) | ch14-centralized-analytics-patterns.md |
| Previous Approaches | ch14-centralized-analytics-patterns.md |
| The Data Warehouse | ch14-centralized-analytics-patterns.md |
| The Star Schema (sidebar) | ch14-centralized-analytics-patterns.md |
| The Data Lake | ch14-centralized-analytics-patterns.md |
| The Data Mesh | ch14-data-mesh-and-dpq-design.md |
| Definition of Data Mesh | ch14-data-mesh-and-dpq-design.md |
| Data Product Quantum | ch14-data-mesh-and-dpq-design.md |
| Data Mesh, Coupling, and Architecture Quantum | ch14-data-mesh-and-dpq-design.md |
| When to Use Data Mesh | ch14-data-mesh-and-dpq-design.md |
| Sysops Squad Saga: Data Mesh | ch14-dpq-worked-example-and-fitness-functions.md |
