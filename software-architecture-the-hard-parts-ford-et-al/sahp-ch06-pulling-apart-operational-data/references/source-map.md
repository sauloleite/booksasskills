# Source Map: Chapter 6, Pulling Apart Operational Data

| Chapter section | Covered in |
|---|---|
| Chapter opening story (data team resists the split) | [decomposition-drivers.md](decomposition-drivers.md) (Building the justification) |
| Chapter introduction (why data is harder to split; code-to-data analogy) | [decomposition-drivers.md](decomposition-drivers.md) |
| Data Decomposition Drivers | [decomposition-drivers.md](decomposition-drivers.md) |
| Data Disintegrators | [decomposition-drivers.md](decomposition-drivers.md) |
| Change Control (bounded context, contract abstraction) | [decomposition-drivers.md](decomposition-drivers.md) |
| Connection Management (quotas, even versus variable distribution) | [decomposition-drivers.md](decomposition-drivers.md), script `connection_budget.py` |
| Scalability | [decomposition-drivers.md](decomposition-drivers.md), script `connection_budget.py` |
| Fault Tolerance | [decomposition-drivers.md](decomposition-drivers.md) |
| Architectural Quantum | [decomposition-drivers.md](decomposition-drivers.md) |
| Database Type Optimization | [decomposition-drivers.md](decomposition-drivers.md), [database-type-selection.md](database-type-selection.md) |
| Data Integrators | [decomposition-drivers.md](decomposition-drivers.md) |
| Data Relationships | [decomposition-drivers.md](decomposition-drivers.md) |
| Database Transactions | [decomposition-drivers.md](decomposition-drivers.md) |
| Sysops Squad Saga: Justifying Database Decomposition | [decomposition-drivers.md](decomposition-drivers.md) (Building the justification) |
| Decomposing Monolithic Data (data domains, soccer-ball view, cutting views) | [five-step-decomposition.md](five-step-decomposition.md), script `data_domain_check.py` |
| Step 1: Analyze Database and Create Data Domains | [five-step-decomposition.md](five-step-decomposition.md) |
| Step 2: Assign Tables To Data Domains (schemas, synonyms) | [five-step-decomposition.md](five-step-decomposition.md) |
| Data Domain vs. Database Schema (sidebar) | [five-step-decomposition.md](five-step-decomposition.md) |
| Step 3: Separate Database Connections To Data Domains (data sovereignty) | [five-step-decomposition.md](five-step-decomposition.md), script `data_domain_check.py --access` |
| Don't Reach Into Other Databases (sidebar) | [five-step-decomposition.md](five-step-decomposition.md) |
| Step 4: Move Schemas To Separate Database Servers | [five-step-decomposition.md](five-step-decomposition.md) |
| Step 5: Switch over to independent database servers | [five-step-decomposition.md](five-step-decomposition.md) |
| Selecting a Database Type (evaluation characteristics) | [database-type-selection.md](database-type-selection.md) |
| Relational Databases | [database-type-selection.md](database-type-selection.md) |
| Aggregate Orientation (sidebar) | [database-type-selection.md](database-type-selection.md) |
| Key-Value Databases | [database-type-selection.md](database-type-selection.md) |
| Sharding in Databases (sidebar) | [database-type-selection.md](database-type-selection.md) |
| Document Databases | [database-type-selection.md](database-type-selection.md) |
| Schema-less Databases (sidebar) | [database-type-selection.md](database-type-selection.md) |
| Column Family Databases | [database-type-selection.md](database-type-selection.md) |
| Graph databases | [database-type-selection.md](database-type-selection.md) |
| Changing Relationship Types (sidebar) | [database-type-selection.md](database-type-selection.md) |
| NewSQL Databases | [database-type-selection.md](database-type-selection.md) |
| Cloud Native Databases | [database-type-selection.md](database-type-selection.md) |
| Time series Databases (and product summary) | [database-type-selection.md](database-type-selection.md) |
| Sysops Squad Saga: Polyglot Databases (business justification, embed versus reference aggregates) | [database-type-selection.md](database-type-selection.md) (Justifying a new database type; Aggregate design) |
