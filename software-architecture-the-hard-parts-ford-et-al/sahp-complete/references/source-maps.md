# Source maps: book sections to reference files

File names below are the chapter-prefixed names used in this folder.

## Source Map: Chapter 1, What Happens When There Are No "Best Practices"?

| Chapter section | Covered in |
|---|---|
| Chapter introduction (no silver bullets, least worst) | [ch01-trade-off-mindset-and-decision-records.md](ch01-trade-off-mindset-and-decision-records.md) |
| Why "The Hard Parts"? | [ch01-trade-off-mindset-and-decision-records.md](ch01-trade-off-mindset-and-decision-records.md) |
| Giving Timeless Advice About Software Architecture | [ch01-trade-off-mindset-and-decision-records.md](ch01-trade-off-mindset-and-decision-records.md) |
| The Importance of Data in Architecture (operational vs analytical data) | [ch01-data-vocabulary-and-running-example.md](ch01-data-vocabulary-and-running-example.md) |
| Architecture Decision Records | [ch01-trade-off-mindset-and-decision-records.md](ch01-trade-off-mindset-and-decision-records.md) |
| Architecture Fitness Functions | [ch01-fitness-functions-governance.md](ch01-fitness-functions-governance.md) |
| Using Fitness Functions | [ch01-fitness-functions-governance.md](ch01-fitness-functions-governance.md) |
| The Equifax Data Breach (sidebar) | [ch01-fitness-functions-governance.md](ch01-fitness-functions-governance.md) |
| Architecture versus Design: Keeping Definitions Simple | [ch01-trade-off-mindset-and-decision-records.md](ch01-trade-off-mindset-and-decision-records.md) (why over how), [ch01-data-vocabulary-and-running-example.md](ch01-data-vocabulary-and-running-example.md) (definitions) |
| Introducing the Sysops Squad Saga | [ch01-data-vocabulary-and-running-example.md](ch01-data-vocabulary-and-running-example.md) |
| Non-Ticketing Workflow | [ch01-data-vocabulary-and-running-example.md](ch01-data-vocabulary-and-running-example.md) |
| Ticketing Workflow | [ch01-data-vocabulary-and-running-example.md](ch01-data-vocabulary-and-running-example.md) |
| A Bad Scenario | [ch01-data-vocabulary-and-running-example.md](ch01-data-vocabulary-and-running-example.md) |
| Sysops Squad Architectural Components | [ch01-data-vocabulary-and-running-example.md](ch01-data-vocabulary-and-running-example.md) |
| Sysops Squad Data Model | [ch01-data-vocabulary-and-running-example.md](ch01-data-vocabulary-and-running-example.md) |

## Source Map: Chapter 2, Discerning Coupling in Software Architecture

| Chapter section | Covered in |
|---|---|
| Part I. Pulling Things Apart (part opener: static vs dynamic coupling) | ch02-trade-off-analysis-framing.md |
| Chapter 2 opening (story setup, coupling definition, trade-off method, service size question) | ch02-trade-off-analysis-framing.md |
| Architecture (Quantum \| Quanta) | ch02-architecture-quantum-static-coupling.md |
| Independently Deployable | ch02-architecture-quantum-static-coupling.md |
| High Functional Cohesion | ch02-architecture-quantum-static-coupling.md |
| High Static Coupling | ch02-architecture-quantum-static-coupling.md |
| Sidebar: Service-Based Architecture | ch02-architecture-quantum-static-coupling.md |
| Dynamic Quantum Coupling | ch02-dynamic-coupling-dimensions.md |
| Communication | ch02-dynamic-coupling-dimensions.md |
| Consistency | ch02-dynamic-coupling-dimensions.md |
| Coordination | ch02-dynamic-coupling-dimensions.md |
| Sysops Squad Saga: Understanding Quanta | ch02-architecture-quantum-static-coupling.md (bootstrap test, quantum vs bounded context, static quantum diagram); ch02-dynamic-coupling-dimensions.md (runtime entanglement, elasticity) |

Script support: `scripts/quantum_coupling.py` implements the static quantum count, the per-call dynamic coordinates and runtime fusion by synchronous calls.

## Source Map: Chapter 3, Architectural Modularity

| Chapter section | Covered in |
|---|---|
| Chapter opening (story setup, business and technical change, capacity analogy, agility) | [ch03-modularity-drivers-and-business-case.md](ch03-modularity-drivers-and-business-case.md) |
| Modularity Drivers | [ch03-modularity-drivers-and-business-case.md](ch03-modularity-drivers-and-business-case.md) |
| Maintainability | [ch03-change-characteristics.md](ch03-change-characteristics.md) |
| Testability | [ch03-change-characteristics.md](ch03-change-characteristics.md) |
| Deployability | [ch03-change-characteristics.md](ch03-change-characteristics.md) |
| Scalability | [ch03-operational-characteristics.md](ch03-operational-characteristics.md) |
| Availability/Fault Tolerance | [ch03-operational-characteristics.md](ch03-operational-characteristics.md) |
| Sysops Squad Saga: Creating a Business Case | [ch03-modularity-drivers-and-business-case.md](ch03-modularity-drivers-and-business-case.md) |

The maintainability-level formula, change and test scope, lockstep deployment, and synchronous failure spread are also computed by `scripts/modularity_impact.py`.

## Source map: Chapter 4, Architectural Decomposition

| Chapter section | Covered in |
|---|---|
| Chapter opening (story: Elephant Migration AntiPattern) | ch04-decomposition-approaches.md |
| Chapter introduction and decision tree (Figure 4-1) | ch04-decomposition-approaches.md |
| Is the Code Base Decomposable? | ch04-decomposability-assessment.md |
| Afferent and Efferent Coupling | ch04-decomposability-assessment.md |
| Abstractness, Instability, and Distance from the Main Sequence | ch04-decomposability-assessment.md |
| Distance from the Main Sequence | ch04-decomposability-assessment.md |
| Component-Based Decomposition | ch04-decomposition-approaches.md |
| Tactical Forking | ch04-decomposition-approaches.md |
| Trade-offs | ch04-decomposition-approaches.md |
| Sysops Squad Saga: Choosing A Decomposition Approach | ch04-decomposition-approaches.md (story summary, decision record template) |

Metric calculations are also implemented in `../scripts/decomposability_metrics.py`.

## Source Map: Chapter 5, Component-Based Decomposition Patterns

Where each part of the chapter is covered. Pattern names are kept so readers can find them in the book; the chapter's fitness-function headings are described here in paraphrase rather than by their exact titles.

| Part of the chapter | Covered in |
|---|---|
| Chapter introduction (pattern roadmap and three-part pattern structure) | ch05-component-inventory-and-sizing.md |
| Architecture Stories (sidebar) | ch05-component-inventory-and-sizing.md |
| Identify and Size Components Pattern, description | ch05-component-inventory-and-sizing.md |
| Identify and Size: governance checks (inventory changes, share of codebase, distance from mean size) | ch05-fitness-functions-catalog.md |
| Identify and Size: story section | ch05-component-inventory-and-sizing.md (one-line summary) |
| Gather Common Domain Components Pattern, description | ch05-common-domain-and-flattening.md (Part A) |
| Gather Common Domain: governance checks (repeated leaf names, duplicated code) | ch05-fitness-functions-catalog.md |
| Gather Common Domain: story section | ch05-common-domain-and-flattening.md (coupling checklist summary) |
| Flatten Components Pattern, description | ch05-common-domain-and-flattening.md (Part B) |
| Flatten Components: governance check (no code in non-leaf namespaces) | ch05-fitness-functions-catalog.md |
| Flatten Components: story section | ch05-common-domain-and-flattening.md (worked example summary) |
| Determine Component Dependencies Pattern, description | ch05-dependencies-domains-and-domain-services.md |
| Determine Dependencies: governance checks (dependency ceiling, forbidden component links) | ch05-fitness-functions-catalog.md |
| Determine Dependencies: story section | ch05-dependencies-domains-and-domain-services.md (filtering shared components) |
| Create Component Domains Pattern, description | ch05-dependencies-domains-and-domain-services.md |
| Create Component Domains: governance check (allowed domains under the root) | ch05-fitness-functions-catalog.md |
| Create Component Domains: story section | ch05-dependencies-domains-and-domain-services.md (procedure and business validation) |
| Create Domain Services Pattern, description | ch05-dependencies-domains-and-domain-services.md |
| Create Domain Services: governance check (shared namespace prefix per service) | ch05-fitness-functions-catalog.md |
| Create Domain Services: story section | ch05-dependencies-domains-and-domain-services.md (sequencing rules) |
| Summary | SKILL.md (workflow) and ch05-dependencies-domains-and-domain-services.md |

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

## Source Map: Chapter 7, Service Granularity

| Chapter section | Covered in |
|---|---|
| Opening story (team debates how small services should be) | ch07-balancing-and-trade-off-negotiation.md (Why balance, not rules) |
| Modularity versus granularity; size metrics | ch07-sizing-metrics-and-disintegrators.md |
| Granularity Disintegrators | ch07-sizing-metrics-and-disintegrators.md |
| Service Scope and Function | ch07-sizing-metrics-and-disintegrators.md |
| Code Volatility | ch07-sizing-metrics-and-disintegrators.md |
| Scalability and Throughput | ch07-sizing-metrics-and-disintegrators.md |
| Fault Tolerance | ch07-sizing-metrics-and-disintegrators.md (plus leftover-cohesion and naming test) |
| Security | ch07-sizing-metrics-and-disintegrators.md |
| Extensibility | ch07-sizing-metrics-and-disintegrators.md |
| Granularity Integrators | ch07-granularity-integrators.md |
| Database Transactions | ch07-granularity-integrators.md |
| Workflow and Choreography | ch07-granularity-integrators.md |
| Shared Code | ch07-granularity-integrators.md |
| Data Relationships | ch07-granularity-integrators.md; scripts/granularity_drivers.py datamap |
| Finding The Right Balance | ch07-balancing-and-trade-off-negotiation.md; scripts/granularity_drivers.py assess |
| Sysops Squad Saga: Ticket Assignment Granularity | ch07-balancing-and-trade-off-negotiation.md (Lessons from the case studies, Worked example A) |
| Sysops Squad Saga: Customer Registration Granularity | ch07-balancing-and-trade-off-negotiation.md (Lessons from the case studies; Design versus architecture; Worked example B) |

## Source map: Chapter 8, Reuse Patterns

| Chapter section | Covered in |
|---|---|
| Part II introduction (Putting Things Back Together) | SKILL.md (purpose) |
| Chapter opening story (single versus multiple shared libraries, library versus service) | ch08-replication-and-shared-libraries.md, ch08-shared-services.md |
| Chapter introduction (reuse in distributed systems, share nothing, WET versus DRY) | ch08-replication-and-shared-libraries.md (Context) |
| Code Replication | ch08-replication-and-shared-libraries.md |
| Code Replication: When To Use | ch08-replication-and-shared-libraries.md |
| Shared Library | ch08-replication-and-shared-libraries.md |
| Dependency Management and Change Control | ch08-replication-and-shared-libraries.md |
| Versioning Strategies | ch08-replication-and-shared-libraries.md |
| Shared Library: When To Use | ch08-replication-and-shared-libraries.md |
| Shared Service | ch08-shared-services.md |
| Change Risk | ch08-shared-services.md |
| Performance | ch08-shared-services.md |
| Scalability | ch08-shared-services.md |
| Fault Tolerance | ch08-shared-services.md |
| Shared Service: When To Use | ch08-shared-services.md |
| Sidecars and Service Mesh | ch08-sidecars-and-orthogonal-reuse.md |
| Sidebar: Orthogonal Coupling | ch08-sidecars-and-orthogonal-reuse.md |
| Sidecars and Service Mesh: When To Use | ch08-sidecars-and-orthogonal-reuse.md |
| Sysops Squad Saga: Common Infrastructure Logic | ch08-sidecars-and-orthogonal-reuse.md (what belongs in the sidecar, ownership) |
| Code Reuse: When Does It Add Value? | ch08-reuse-value-and-platforms.md |
| Sidebar: Reuse | ch08-reuse-value-and-platforms.md (abstraction versus rate of change) |
| Reuse via Platforms | ch08-reuse-value-and-platforms.md |
| Sysops Squad Saga: Shared Domain Functionality | ch08-shared-services.md (worked example) |

The four techniques are compared side by side in ch08-reuse-value-and-platforms.md. No scripts: the chapter has no calculations.

## Source Map: Chapter 9 Sections to Reference Files

| Chapter section | Covered in |
|---|---|
| Chapter opening (Sysops Squad story, intro) | ch09-data-ownership-scenarios.md (section 8) |
| Assigning Data Ownership | ch09-data-ownership-scenarios.md (sections 1, 2) |
| Single Ownership Scenario | ch09-data-ownership-scenarios.md (section 3) |
| Common Ownership Scenario | ch09-data-ownership-scenarios.md (section 4) |
| Joint Ownership Scenario | ch09-data-ownership-scenarios.md (section 5) |
| Table Split Technique | ch09-data-ownership-scenarios.md (5.1) |
| Data Domain Technique | ch09-data-ownership-scenarios.md (5.2) |
| Delegate Technique | ch09-data-ownership-scenarios.md (5.3) |
| Service Consolidation Technique | ch09-data-ownership-scenarios.md (5.4) |
| Data Ownership Summary | ch09-data-ownership-scenarios.md (sections 6, 7) |
| Distributed Transactions | ch09-acid-vs-base-distributed-transactions.md |
| Eventual Consistency Patterns | ch09-eventual-consistency-patterns.md (section 1) |
| Background Synchronization Pattern | ch09-eventual-consistency-patterns.md (section 2) |
| Orchestrated Request-Based Pattern | ch09-eventual-consistency-patterns.md (section 3) |
| Event-Based Pattern | ch09-eventual-consistency-patterns.md (section 4) |
| Sysops Squad Saga: Data Ownership For Ticket Processing | ch09-data-ownership-scenarios.md (sections 6, 8) |

Selection guidance and error-handling playbooks (ch09-eventual-consistency-patterns.md sections 5 to 8) and the script `scripts/data_ownership.py` synthesize material across sections.

## Source Map: Chapter 10, Distributed Data Access

| Chapter section | Covered in |
|---|---|
| Chapter opening (story setup and Wishlist/Catalog framing) | ch10-data-access-patterns.md (The problem shape); ch10-choosing-and-recording.md (What the chapter story illustrates) |
| Inter-service Communication Pattern | ch10-data-access-patterns.md |
| Column Schema Replication Pattern | ch10-data-access-patterns.md |
| Replicated Caching Pattern | ch10-replicated-caching.md |
| Data Domain Pattern | ch10-data-access-patterns.md |
| Sysops Squad Saga: Data Access For Ticket Assignment | ch10-choosing-and-recording.md; ch10-replicated-caching.md (sizing) |

## Source Map: Chapter 11, Managing Distributed Workflows

| Chapter section | Covered in |
|---|---|
| Chapter introduction (coordination as a dynamic coupling dimension; orchestration vs choreography topology) | ch11-orchestration-vs-choreography.md, SKILL.md |
| Orchestration Communication Style | ch11-orchestration-vs-choreography.md |
| Choreography Communication Style | ch11-orchestration-vs-choreography.md, ch11-semantic-vs-implementation-coupling.md |
| (Semantic coupling and technical vs domain partitioning, within Choreography) | ch11-semantic-vs-implementation-coupling.md |
| Workflow State Management | ch11-choreography-workflow-state.md |
| Trade-Offs Between Orchestration and Choreography | ch11-orchestration-vs-choreography.md |
| State Owner and Coupling | ch11-orchestration-vs-choreography.md, ch11-choreography-workflow-state.md |
| Sysops Squad Saga: Managing Workflows (scenario-driven comparison and ADR) | ch11-orchestration-vs-choreography.md (Scenario-driven comparison and ADR) |

## Source Map: Chapter 12, Transactional Sagas

| Chapter section | Reference file |
|---|---|
| Chapter opening (saga origins, Sysops Squad framing) | ch12-saga-pattern-catalog.md |
| Transactional Saga Patterns | ch12-saga-pattern-catalog.md |
| Epic Saga(sao) | ch12-saga-pattern-catalog.md; ch12-compensation-vs-state-management.md |
| Phone Tag Saga(sac) Pattern | ch12-saga-pattern-catalog.md |
| Fairy Tale Saga(seo) Pattern | ch12-saga-pattern-catalog.md |
| Time Travel Saga(sec) Pattern | ch12-saga-pattern-catalog.md |
| Fantasy Fiction Saga(aao) Pattern | ch12-saga-pattern-catalog.md |
| Horror Story(aac) Pattern | ch12-saga-pattern-catalog.md |
| Parallel Saga(aeo) Pattern | ch12-saga-pattern-catalog.md |
| Anthology Saga(aec) Pattern | ch12-saga-pattern-catalog.md |
| State Management and Eventual Consistency | ch12-compensation-vs-state-management.md |
| Saga State Machines | ch12-saga-state-machines-and-tooling.md |
| Techniques For Managing Sagas | ch12-saga-state-machines-and-tooling.md |
| What Next? | ch12-saga-pattern-catalog.md (selection playbook) |
| Sysops Squad Saga: Atomic Transactions and Compensating Updates | ch12-compensation-vs-state-management.md |

Story note: the chapter's narrative shows a team discovering that a ticket-completion workflow designed as an atomic, orchestrated saga leaks side effects, can fail during compensation, and blocks the field expert on a survey step; it ends by steering toward state-managed eventual consistency. The references use invented examples instead.

## Source Map: Chapter 13 "Contracts"

| Chapter section | Covered in |
|---|---|
| Chapter introduction (contracts as a cross-cutting force; broad definition) | ch13-strict-vs-loose-contracts.md (Broad definition of a contract) |
| Strict versus Loose Contracts | ch13-strict-vs-loose-contracts.md (The strictness spectrum; Need-to-know contracts and GraphQL/REST) |
| Trade-offs Between Strict versus Loose Contracts | ch13-strict-vs-loose-contracts.md (Choosing strictness per edge) |
| Strict Contracts | ch13-strict-vs-loose-contracts.md (What strict contracts give and cost; Versioning policy checklist) |
| Loose Contracts | ch13-strict-vs-loose-contracts.md (What loose contracts give and cost) |
| Contracts in microservices | ch13-consumer-driven-contracts.md (The three decisions) |
| Coupling Levels | ch13-consumer-driven-contracts.md (Coupling levels for shared domain data) |
| Consumer-driven Contracts | ch13-consumer-driven-contracts.md (Push versus pull; Strengths and weaknesses; Readiness checklist) |
| Stamp Coupling | ch13-stamp-coupling.md (What stamp coupling is; Industry documents) |
| Over-coupling via Stamp Coupling | ch13-stamp-coupling.md (Accidental stamp coupling) |
| Bandwidth | ch13-stamp-coupling.md (Bandwidth: the cost model); scripts/contract_usage.py |
| Stamp Coupling for Workflow Management | ch13-stamp-coupling.md (Stamp coupling for workflow management; Strengths and weaknesses) |
| Sysops Squad Saga: Managing Ticketing Contracts | ch13-strict-vs-loose-contracts.md (Worked example: one workflow, mixed strictness). The story shows strictness chosen per collaborator in one workflow, with a loose contract for an app-store mobile client. |

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

## Source Map: Chapter 15, Build Your Own Trade-Off Analysis

| Chapter section | Reference file |
|---|---|
| Chapter opening (Sysops Squad retrospective) | ch15-communicating-and-staying-objective.md |
| Introduction and the three-step process | ch15-three-step-analysis-process.md |
| Finding Entangled Dimensions | ch15-three-step-analysis-process.md |
| Coupling | ch15-three-step-analysis-process.md |
| Analyze Coupling Points | ch15-three-step-analysis-process.md |
| Assess Trade-Offs | ch15-three-step-analysis-process.md |
| Trade-Off Techniques | ch15-trade-off-techniques.md |
| Qualitative versus Quantative Analysis | ch15-trade-off-techniques.md |
| MECE Lists | ch15-trade-off-techniques.md |
| The "Out of Context" Trap | ch15-trade-off-techniques.md |
| Model Relevant Domain Cases | ch15-trade-off-techniques.md |
| Prefer Bottom Line over Overwhelming Evidence | ch15-communicating-and-staying-objective.md |
| Avoiding Snake Oil and Evangelism | ch15-communicating-and-staying-objective.md |
| Sysops Squad Saga: Epilog | ch15-communicating-and-staying-objective.md |
