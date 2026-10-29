# Source maps: book sections to reference files

File names below are the chapter-prefixed names used in this folder.

## Source Map: Chapter 1, Introduction

| Chapter section | Reference file |
|---|---|
| Introduction (chapter opening, context) | ch01-architecture-definition-and-context.md |
| Defining Software Architecture | ch01-architecture-definition-and-context.md |
| Laws of Software Architecture | ch01-laws-and-trade-off-analysis.md |
| Expectations of an Architect | ch01-architect-expectations-playbook.md |
| Make Architecture Decisions | ch01-architect-expectations-playbook.md |
| Continually Analyze the Architecture | ch01-architect-expectations-playbook.md |
| Keep Current with Latest Trends | ch01-architect-expectations-playbook.md |
| Ensure Compliance with Decisions | ch01-architect-expectations-playbook.md |
| Understand Diverse Technologies | ch01-architect-expectations-playbook.md |
| Know the Business Domain | ch01-architect-expectations-playbook.md |
| Possess Interpersonal Skills | ch01-architect-expectations-playbook.md |
| Understand and Navigate Politics | ch01-architect-expectations-playbook.md |
| Roadmap | ch01-architecture-definition-and-context.md |

## Source Map: Chapter 2, Architectural Thinking

| Chapter section | Covered in |
|---|---|
| Architectural Thinking (chapter introduction) | ../SKILL.md (Purpose) |
| Architecture Versus Design | ch02-architecture-vs-design.md |
| Strategic Versus Tactical Decisions | ch02-architecture-vs-design.md |
| Level of Effort | ch02-architecture-vs-design.md |
| The Significance of Trade-Offs | ch02-architecture-vs-design.md |
| Technical Breadth | ch02-technical-breadth-and-radar.md |
| Frozen Caveman Antipattern (sidebar) | ch02-technical-breadth-and-radar.md |
| The 20-Minute Rule | ch02-technical-breadth-and-radar.md |
| Developing a Personal Radar | ch02-technical-breadth-and-radar.md |
| The Thoughtworks Technology Radar | ch02-technical-breadth-and-radar.md |
| Parts (quadrants and rings) | ch02-technical-breadth-and-radar.md |
| Analyzing Trade-Offs | ch02-trade-off-analysis.md |
| Understanding Business Drivers | ch02-trade-off-analysis.md |
| Balancing Architecture and Hands-On Coding | ch02-hands-on-coding-balance.md |
| There's More to Architectural Thinking | ch02-hands-on-coding-balance.md (closing note) |

## Source map: Chapter 3, Modularity

| Chapter section | Covered in |
|---|---|
| Chapter introduction (modularity as an implicit characteristic, entropy) | ch03-modularity-granularity-and-packaging.md |
| Modularity Versus Granularity | ch03-modularity-granularity-and-packaging.md |
| Defining Modularity | ch03-modularity-granularity-and-packaging.md |
| Sidebar: Modular Reuse Before Classes | ch03-modularity-granularity-and-packaging.md |
| Sidebar: A Language with No Name Conflicts: Java 1.0 | ch03-modularity-granularity-and-packaging.md |
| Measuring Modularity | ch03-cohesion-and-lcom.md, ch03-coupling-metrics-and-main-sequence.md, ch03-connascence.md |
| Cohesion | ch03-cohesion-and-lcom.md |
| Coupling | ch03-coupling-metrics-and-main-sequence.md |
| Sidebar: Why Such Similar Names for Coupling Metrics? | ch03-coupling-metrics-and-main-sequence.md |
| Core Metrics (Abstractness, Instability) | ch03-coupling-metrics-and-main-sequence.md |
| Distance from the Main Sequence | ch03-coupling-metrics-and-main-sequence.md |
| Sidebar: The Limitations of Metrics | ch03-coupling-metrics-and-main-sequence.md |
| Connascence | ch03-connascence.md |
| Static connascence | ch03-connascence.md |
| Dynamic connascence | ch03-connascence.md |
| Connascence properties (Strength, Locality, Degree) | ch03-connascence.md |
| From Modules to Components | ch03-modularity-granularity-and-packaging.md |

Calculations from Cohesion (LCOM) and Core Metrics / Distance from the Main Sequence are implemented in scripts/modularity_metrics.py.

## Source Map: Chapter 4, Architectural Characteristics Defined

| Chapter section | Covered in |
|---|---|
| Chapter introduction (structural design, domain vs. characteristics) | ch04-qualifying-characteristics.md |
| The Longevity of the Term "Non-Functional Requirements" (sidebar) | ch04-qualifying-characteristics.md |
| Architectural Characteristics and System Design | ch04-qualifying-characteristics.md |
| Nondomain design consideration | ch04-qualifying-characteristics.md |
| Influences some structural aspect of the design | ch04-qualifying-characteristics.md |
| Critical or important to application success | ch04-qualifying-characteristics.md, ch04-trade-offs-least-worst.md |
| Implicit versus explicit characteristics | ch04-qualifying-characteristics.md |
| Architectural Characteristics (Partially) Listed | ch04-characteristics-catalog.md |
| Operational Architectural Characteristics | ch04-characteristics-catalog.md |
| Structural Architectural Characteristics | ch04-characteristics-catalog.md |
| Cloud Characteristics | ch04-characteristics-catalog.md |
| Cross-Cutting Architectural Characteristics | ch04-characteristics-catalog.md |
| ISO definitions and functional suitability | ch04-characteristics-catalog.md |
| The Many Ambiguities in Software Architecture (sidebar) | ch04-characteristics-catalog.md |
| Trade-Offs and Least Worst Architecture | ch04-trade-offs-least-worst.md |

## Source Map: Chapter 5 Headings to Reference Files

| Chapter section | Covered in |
|---|---|
| Chapter introduction (three sources of characteristics, implicit domain knowledge) | ch05-elicitation-and-translation.md |
| Extracting Architectural Characteristics from Domain Concerns | ch05-elicitation-and-translation.md |
| Composite Architectural Characteristics | ch05-elicitation-and-translation.md |
| Extracting Architectural Characteristics | ch05-elicitation-and-translation.md |
| The Origin of Architecture Katas (sidebar) | ch05-katas-and-requirement-walkthrough.md |
| Working with Katas | ch05-katas-and-requirement-walkthrough.md |
| Kata: Silicon Sandwiches | ch05-katas-and-requirement-walkthrough.md |
| Explicit Characteristics | ch05-elicitation-and-translation.md, ch05-katas-and-requirement-walkthrough.md |
| Implicit Characteristics | ch05-elicitation-and-translation.md, ch05-katas-and-requirement-walkthrough.md |
| Design Versus Architecture and Trade-Offs (sidebar) | ch05-katas-and-requirement-walkthrough.md |
| Limiting and Prioritizing Architectural Characteristics | ch05-limiting-and-prioritizing.md |
| Case Study: The Vasa (sidebar) | ch05-limiting-and-prioritizing.md |
| Architectural characteristics worksheet (figure and session) | ch05-limiting-and-prioritizing.md |

## Source Map: Chapter 6, Measuring and Governing Architecture Characteristics

| Chapter section | Covered in |
|---|---|
| Chapter introduction | [ch06-defining-and-measuring-characteristics.md](ch06-defining-and-measuring-characteristics.md) |
| Measuring Architecture Characteristics (They aren't physics; Wildly varying definitions; Too composite) | [ch06-defining-and-measuring-characteristics.md](ch06-defining-and-measuring-characteristics.md) |
| Operational Measures | [ch06-defining-and-measuring-characteristics.md](ch06-defining-and-measuring-characteristics.md) |
| The Many Flavors of Performance (sidebar) | [ch06-defining-and-measuring-characteristics.md](ch06-defining-and-measuring-characteristics.md) |
| Structural Measures | [ch06-structural-metrics-and-complexity.md](ch06-structural-metrics-and-complexity.md) |
| Cyclomatic Complexity (sidebar) | [ch06-structural-metrics-and-complexity.md](ch06-structural-metrics-and-complexity.md) |
| What's a Good Value for Cyclomatic Complexity? (sidebar) | [ch06-structural-metrics-and-complexity.md](ch06-structural-metrics-and-complexity.md) |
| Process Measures | [ch06-defining-and-measuring-characteristics.md](ch06-defining-and-measuring-characteristics.md) |
| Governance and Fitness Functions | [ch06-fitness-functions-and-governance.md](ch06-fitness-functions-and-governance.md) |
| Governing Architecture Characteristics | [ch06-fitness-functions-and-governance.md](ch06-fitness-functions-and-governance.md) |
| Fitness Functions | [ch06-fitness-functions-and-governance.md](ch06-fitness-functions-and-governance.md) |
| Cyclic dependencies | [ch06-fitness-functions-and-governance.md](ch06-fitness-functions-and-governance.md), script `dependency_fitness.py` |
| Distance from the Main Sequence fitness function | [ch06-fitness-functions-and-governance.md](ch06-fitness-functions-and-governance.md), script `dependency_fitness.py` |
| ArchUnit / NetArchTest layer governance, metric gaming, Chaos Monkey and Simian Army, checklist perspective (unheaded continuation) | [ch06-fitness-functions-and-governance.md](ch06-fitness-functions-and-governance.md) |

## Source map: Chapter 7 sections to reference files

| Chapter section | Covered in |
|---|---|
| Chapter introduction (why scope matters, limits of structural measures) | ch07-architecture-quantum-and-coupling.md |
| Architectural Quanta and Granularity | ch07-architecture-quantum-and-coupling.md |
| Plurals for Latin-Derived Technical Terms (sidebar) | ch07-architecture-quantum-and-coupling.md |
| Domain-Driven Design's Bounded Context (sidebar) | ch07-architecture-quantum-and-coupling.md |
| Coupling types: semantic, implementation, static, dynamic | ch07-architecture-quantum-and-coupling.md |
| Low external implementation static coupling, brittleness | ch07-architecture-quantum-and-coupling.md |
| Synchronous Communication | ch07-communication-and-dynamic-coupling.md |
| The Impact of Scoping | ch07-scoping-decision-playbook.md |
| Scoping and Architectural Style | ch07-scoping-decision-playbook.md |
| Kata: Going Green | ch07-scoping-decision-playbook.md |
| Scoping and the Cloud | ch07-scoping-decision-playbook.md |

## Source Map: Chapter 8, Component-Based Thinking

Chapter section headings mapped to the reference file that covers each.

| Chapter section | Covered in |
|---|---|
| Chapter introduction (component-based thinking, logical components as building blocks) | ch08-logical-architecture-and-identification.md |
| Defining Logical Components | ch08-logical-architecture-and-identification.md |
| Logical Versus Physical Architecture | ch08-logical-architecture-and-identification.md |
| Creating a Logical Architecture | ch08-logical-architecture-and-identification.md |
| Identifying Core Components | ch08-logical-architecture-and-identification.md |
| The Workflow approach | ch08-logical-architecture-and-identification.md |
| The Actor/Action approach | ch08-logical-architecture-and-identification.md |
| The Entity Trap | ch08-logical-architecture-and-identification.md |
| Assigning User Stories to Components | ch08-logical-architecture-and-identification.md |
| Analyzing Roles and Responsibilities | ch08-refining-components.md |
| Analyzing Architectural Characteristics | ch08-refining-components.md |
| Restructuring Components | ch08-refining-components.md |
| Component Coupling | ch08-component-coupling.md |
| Static Coupling | ch08-component-coupling.md |
| Temporal Coupling | ch08-component-coupling.md |
| The Law of Demeter | ch08-component-coupling.md |
| Case Study: Going, Going, Gone: Discovering Components | ch08-refining-components.md |

## Source Map: Chapter 9, Foundations

Chapter section headings mapped to the reference file that covers each.

| Chapter heading | Reference file |
|---|---|
| Part II intro (Architecture Styles) | ch09-styles-and-lineage.md |
| Styles Versus Patterns | ch09-styles-and-lineage.md |
| Where Do Architectural Styles Come From? (sidebar) | ch09-styles-and-lineage.md |
| Fundamental Patterns | ch09-styles-and-lineage.md |
| Big Ball of Mud | ch09-styles-and-lineage.md |
| Unitary Architecture | ch09-styles-and-lineage.md |
| Client/Server | ch09-styles-and-lineage.md |
| Desktop and database server | ch09-styles-and-lineage.md |
| Browser and web server | ch09-styles-and-lineage.md |
| Single-page JavaScript applications | ch09-styles-and-lineage.md |
| Three-tier | ch09-styles-and-lineage.md |
| Three-Tier Architectures, Language Design, and Long-Term Implications (sidebar) | ch09-styles-and-lineage.md |
| Architecture Partitioning | ch09-top-level-partitioning.md |
| Conway's Law (sidebar) | ch09-top-level-partitioning.md |
| Kata: Silicon Sandwiches, Partitioning | ch09-top-level-partitioning.md |
| Domain partitioning | ch09-top-level-partitioning.md |
| Technical partitioning | ch09-top-level-partitioning.md |
| Monolithic Versus Distributed Architectures | ch09-distributed-fallacies.md |
| Fallacy #1: The Network Is Reliable | ch09-distributed-fallacies.md |
| Fallacy #2: Latency Is Zero | ch09-distributed-fallacies.md (numbers: scripts/call_chain_budget.py) |
| Fallacy #3: Bandwidth Is Infinite | ch09-distributed-fallacies.md (numbers: scripts/call_chain_budget.py) |
| Fallacy #4: The Network Is Secure | ch09-distributed-fallacies.md |
| Fallacy #5: The Topology Never Changes | ch09-distributed-fallacies.md |
| Fallacy #6: There Is Only One Administrator | ch09-distributed-fallacies.md |
| Fallacy #7: Transport Cost Is Zero | ch09-distributed-fallacies.md |
| Fallacy #8: The Network Is Homogeneous | ch09-distributed-fallacies.md |
| The Other Fallacies | ch09-distributed-fallacies.md |
| Fallacy #9. Versioning is easy | ch09-distributed-fallacies.md |
| Fallacy #10. Compensating updates always work | ch09-distributed-fallacies.md |
| Fallacy #11. Observability is optional | ch09-distributed-fallacies.md |
| Team Topologies and Architecture | ch09-team-topologies.md |
| Stream-aligned, Enabling, Complicated-subsystem, Platform teams | ch09-team-topologies.md |
| On to Specific Styles | ch09-team-topologies.md |

## Source Map: Chapter 10, Layered Architecture Style

| Chapter section | Covered in |
|---|---|
| Chapter introduction (antipatterns of implied/accidental architecture) | ch10-layer-design-and-isolation.md (Pitfalls), SKILL.md |
| Topology | ch10-layer-design-and-isolation.md |
| Style Specifics | ch10-layer-design-and-isolation.md |
| Layers of Isolation | ch10-layer-design-and-isolation.md |
| Adding Layers | ch10-layer-design-and-isolation.md |
| (Architecture Sinkhole antipattern, within Adding Layers) | ch10-layer-design-and-isolation.md, scripts/layer_rules_check.py |
| Data Topologies | ch10-operations-governance-and-teams.md |
| Cloud Considerations | ch10-operations-governance-and-teams.md |
| Common Risks | ch10-operations-governance-and-teams.md |
| Governance | ch10-operations-governance-and-teams.md, scripts/layer_rules_check.py |
| Team Topology Considerations | ch10-operations-governance-and-teams.md |
| Style Characteristics | ch10-style-fit-and-tradeoffs.md |
| When to Use | ch10-style-fit-and-tradeoffs.md |
| When Not to Use | ch10-style-fit-and-tradeoffs.md |
| Examples and Use Cases | ch10-style-fit-and-tradeoffs.md |

## Source Map: Chapter 11, The Modular Monolith Architecture Style

| Chapter section | Covered in |
|---|---|
| (Chapter introduction) | [ch11-fit-teams-and-example.md](ch11-fit-teams-and-example.md) (classification), SKILL.md |
| Topology | [ch11-structure-and-communication.md](ch11-structure-and-communication.md) |
| Style Specifics | [ch11-structure-and-communication.md](ch11-structure-and-communication.md) |
| Monolithic Structure | [ch11-structure-and-communication.md](ch11-structure-and-communication.md) |
| Modular Structure | [ch11-structure-and-communication.md](ch11-structure-and-communication.md) |
| Module Communication | [ch11-structure-and-communication.md](ch11-structure-and-communication.md) |
| Peer-to-peer approach | [ch11-structure-and-communication.md](ch11-structure-and-communication.md) |
| Mediator approach | [ch11-structure-and-communication.md](ch11-structure-and-communication.md) |
| Data Topologies | [ch11-structure-and-communication.md](ch11-structure-and-communication.md) |
| Cloud Considerations | [ch11-structure-and-communication.md](ch11-structure-and-communication.md) |
| Common Risks | [ch11-risks-and-governance.md](ch11-risks-and-governance.md) |
| Governance | [ch11-risks-and-governance.md](ch11-risks-and-governance.md), scripts/check_module_boundaries.py |
| Team Topology Considerations | [ch11-fit-teams-and-example.md](ch11-fit-teams-and-example.md) |
| Style Characteristics | [ch11-fit-teams-and-example.md](ch11-fit-teams-and-example.md) (qualitative only) |
| When to Use | [ch11-fit-teams-and-example.md](ch11-fit-teams-and-example.md) |
| When Not to Use | [ch11-fit-teams-and-example.md](ch11-fit-teams-and-example.md) |
| Examples and Use Cases | [ch11-fit-teams-and-example.md](ch11-fit-teams-and-example.md) |

## Source Map: Chapter 12, Pipeline Architecture Style

| Chapter section | Covered in |
|---|---|
| (Chapter introduction) | ch12-topology-filters-and-pipes.md |
| Topology | ch12-topology-filters-and-pipes.md |
| Style Specifics | ch12-topology-filters-and-pipes.md |
| Filters | ch12-topology-filters-and-pipes.md |
| Pipes | ch12-topology-filters-and-pipes.md |
| Data Topologies | ch12-topology-filters-and-pipes.md |
| Cloud Considerations | ch12-topology-filters-and-pipes.md |
| Common Risks | ch12-risks-governance-and-teams.md |
| Governance | ch12-risks-governance-and-teams.md |
| Team Topology Considerations | ch12-risks-governance-and-teams.md |
| Style Characteristics | ch12-fit-tradeoffs-and-examples.md |
| When to Use | ch12-fit-tradeoffs-and-examples.md |
| When Not to Use | ch12-fit-tradeoffs-and-examples.md |
| Examples and Use Cases | ch12-fit-tradeoffs-and-examples.md |

## Source Map: Chapter 13, Microkernel Architecture Style

| Chapter section | Reference file |
|---|---|
| Introduction (product and customization fit) | ch13-fit-tradeoffs-and-use-cases.md |
| Topology | ch13-core-plugin-design.md |
| Style Specifics | ch13-core-plugin-design.md |
| Core System | ch13-core-plugin-design.md |
| Plug-In Components | ch13-core-plugin-design.md |
| The Spectrum of "Microkern-ality" | ch13-fit-tradeoffs-and-use-cases.md |
| Registry | ch13-core-plugin-design.md |
| Contracts | ch13-core-plugin-design.md |
| Data Topologies | ch13-core-plugin-design.md |
| Cloud Considerations | ch13-fit-tradeoffs-and-use-cases.md |
| Common Risks | ch13-risks-governance-teams.md |
| Volatile Core | ch13-risks-governance-teams.md |
| Plug-In Dependencies | ch13-risks-governance-teams.md |
| Governance | ch13-risks-governance-teams.md |
| Team Topology Considerations | ch13-risks-governance-teams.md |
| Architecture Characteristics Ratings | ch13-fit-tradeoffs-and-use-cases.md |
| Examples and Use Cases | ch13-fit-tradeoffs-and-use-cases.md |

## Source Map: Chapter 14, Service-Based Architecture Style

| Chapter section | Reference file |
|---|---|
| (Chapter introduction) | ch14-characteristics-fit-and-migration.md |
| Topology | ch14-topology-and-service-design.md |
| Style Specifics | ch14-topology-and-service-design.md |
| Service Design and Granularity | ch14-topology-and-service-design.md |
| User Interface Options | ch14-topology-and-service-design.md |
| API Gateway Options | ch14-topology-and-service-design.md |
| Data Topologies | ch14-data-topologies.md |
| Cloud Considerations | ch14-topology-and-service-design.md |
| Common Risks | ch14-risks-governance-and-teams.md |
| Governance | ch14-risks-governance-and-teams.md |
| Team Topology Considerations | ch14-risks-governance-and-teams.md |
| Style Characteristics | ch14-characteristics-fit-and-migration.md |
| Examples and Use Cases | ch14-characteristics-fit-and-migration.md |

## Source Map: Chapter 15 "Event-Driven Architecture Style"

| Chapter section | Covered in |
|---|---|
| Introduction (request-based vs event-based model) | ch15-topology-and-event-semantics.md |
| Topology | ch15-topology-and-event-semantics.md |
| Style Specifics | (container section) |
| Events Versus Messages | ch15-topology-and-event-semantics.md |
| Derived Events | ch15-topology-and-event-semantics.md |
| Triggering Extensible Events | ch15-topology-and-event-semantics.md |
| Asynchronous Capabilities | ch15-topology-and-event-semantics.md |
| Broadcast Capabilities | ch15-topology-and-event-semantics.md |
| Event Payload | ch15-event-payload-and-granularity.md |
| Data-based event payloads | ch15-event-payload-and-granularity.md |
| Key-based event payload | ch15-event-payload-and-granularity.md |
| Trade-off summary | ch15-event-payload-and-granularity.md |
| Anemic events | ch15-event-payload-and-granularity.md |
| The Swarm of Gnats Antipattern | ch15-event-payload-and-granularity.md |
| Error Handling | ch15-async-reliability-patterns.md |
| Preventing Data Loss | ch15-async-reliability-patterns.md |
| Request-Reply Processing | ch15-async-reliability-patterns.md |
| Mediated Event-Driven Architecture | ch15-mediator-and-data-topologies.md |
| Data Topologies | ch15-mediator-and-data-topologies.md |
| Monolithic Database Topology | ch15-mediator-and-data-topologies.md |
| Domain Database Topology | ch15-mediator-and-data-topologies.md |
| Dedicated Data Topology | ch15-mediator-and-data-topologies.md |
| Cloud Considerations | ch15-style-fit-risks-and-governance.md |
| Common Risks | ch15-style-fit-risks-and-governance.md |
| Governance | ch15-style-fit-risks-and-governance.md |
| Team Topology Considerations | ch15-style-fit-risks-and-governance.md |
| Style Characteristics | ch15-style-fit-risks-and-governance.md |
| Choosing Between Request-Based and Event-Based Models | ch15-style-fit-risks-and-governance.md |
| Examples and Use Cases | ch15-style-fit-risks-and-governance.md |

## Source Map: Chapter 16 Section Headings

| Chapter section | Covered in |
|---|---|
| (Chapter introduction) | ch16-topology-and-components.md |
| Topology | ch16-topology-and-components.md |
| Style Specifics | ch16-topology-and-components.md |
| Processing Unit | ch16-topology-and-components.md |
| Virtualized Middleware | ch16-topology-and-components.md |
| Messaging Grid | ch16-topology-and-components.md |
| Data Grid | ch16-topology-and-components.md |
| Replicated and distributed caching | ch16-caching-models.md |
| Near-cache considerations | ch16-caching-models.md |
| Processing Grid | ch16-topology-and-components.md |
| Deployment Manager | ch16-topology-and-components.md |
| Data Pumps | ch16-topology-and-components.md |
| Data Writers | ch16-topology-and-components.md |
| Data Readers | ch16-topology-and-components.md |
| Data Topologies | ch16-data-risks-and-collisions.md |
| Cloud Considerations | ch16-data-risks-and-collisions.md |
| Common Risks | ch16-data-risks-and-collisions.md |
| Frequent Reads from the Database | ch16-data-risks-and-collisions.md |
| Data Synchronization and Consistency | ch16-data-risks-and-collisions.md |
| High Data Volumes | ch16-data-risks-and-collisions.md |
| Data Collisions | ch16-data-risks-and-collisions.md, scripts/collision_rate.py |
| Governance | ch16-governance-teams-and-fit.md |
| Team Topology Considerations | ch16-governance-teams-and-fit.md |
| Style Characteristics | ch16-governance-teams-and-fit.md |
| Examples and Use Cases | ch16-governance-teams-and-fit.md |
| Concert Ticketing System | ch16-governance-teams-and-fit.md |
| Online Auction System | ch16-governance-teams-and-fit.md |

## Source Map: Chapter 17 sections to reference files

| Chapter section | Reference file |
|---|---|
| Chapter introduction | ch17-taxonomy-and-orchestration.md (historical context); SKILL.md |
| Topology | ch17-taxonomy-and-orchestration.md |
| Style Specifics | ch17-taxonomy-and-orchestration.md (historical context) |
| Why So Many Service Names? (sidebar) | ch17-taxonomy-and-orchestration.md |
| Taxonomy | ch17-taxonomy-and-orchestration.md |
| Business services | ch17-taxonomy-and-orchestration.md |
| Enterprise services | ch17-taxonomy-and-orchestration.md |
| Application services | ch17-taxonomy-and-orchestration.md |
| Infrastructure services | ch17-taxonomy-and-orchestration.md |
| Orchestration engine and message bus | ch17-taxonomy-and-orchestration.md |
| Message flow | ch17-taxonomy-and-orchestration.md |
| Reuse...and Coupling | ch17-reuse-coupling-and-characteristics.md |
| Data Topologies | ch17-taxonomy-and-orchestration.md |
| Really? Declarative Transactions?!? (sidebar) | ch17-taxonomy-and-orchestration.md |
| Cloud Considerations | ch17-modern-esb-integration-and-governance.md |
| Common Risks | ch17-modern-esb-integration-and-governance.md |
| Governance | ch17-modern-esb-integration-and-governance.md (plus scripts/integration_flow_guard.py) |
| Team Topology Considerations | ch17-reuse-coupling-and-characteristics.md |
| Style Characteristics | ch17-reuse-coupling-and-characteristics.md |
| Examples and Use Cases | ch17-modern-esb-integration-and-governance.md (where the style still fits); ch17-reuse-coupling-and-characteristics.md (change variability) |

## Source Map: Chapter 18, Microservices Architecture

| Chapter section | Reference file |
|---|---|
| Introduction (origins, DDD, bounded context, share nothing) | ch18-boundaries-granularity-and-transactions.md |
| Topology | ch18-boundaries-granularity-and-transactions.md |
| Style Specifics: Bounded Context | ch18-boundaries-granularity-and-transactions.md |
| Style Specifics: Granularity | ch18-boundaries-granularity-and-transactions.md |
| Style Specifics: Data Isolation | ch18-data-topologies.md |
| Style Specifics: API Layer | ch18-communication-and-infrastructure.md |
| Style Specifics: Operational Reuse (sidecar, service mesh, service discovery) | ch18-communication-and-infrastructure.md |
| Style Specifics: Frontends | ch18-communication-and-infrastructure.md |
| Style Specifics: Communication (incl. Enforced Heterogeneity sidebar) | ch18-communication-and-infrastructure.md |
| Style Specifics: Choreography and Orchestration | ch18-communication-and-infrastructure.md |
| Style Specifics: Transactions and Sagas | ch18-boundaries-granularity-and-transactions.md |
| Data Topologies | ch18-data-topologies.md |
| Cloud Considerations | ch18-risks-governance-teams-and-fit.md |
| Common Risks | ch18-risks-governance-teams-and-fit.md |
| Governance | ch18-risks-governance-teams-and-fit.md (checks automated in scripts/coupling_audit.py) |
| Team Topology Considerations | ch18-risks-governance-teams-and-fit.md |
| Style Characteristics | ch18-risks-governance-teams-and-fit.md |
| Examples and Use Cases | ch18-risks-governance-teams-and-fit.md |

## Source Map: Chapter 19 sections to reference files

| Chapter section | Covered in |
|---|---|
| Chapter introduction ("It depends") | SKILL.md (purpose) |
| Shifting "Fashion" in Architecture | ch19-trends-and-prerequisites.md |
| Decision Criteria (prerequisite factors) | ch19-trends-and-prerequisites.md |
| Decision Criteria: domain/architecture isomorphism | ch19-style-determinations.md |
| Decision Criteria: monolith vs distributed, data location, sync vs async | ch19-style-determinations.md |
| Decision Criteria: outputs of the design process | ch19-style-determinations.md |
| Monolith Case Study: Silicon Sandwiches | ch19-case-studies.md |
| Modular Monolith | ch19-case-studies.md |
| Microkernel | ch19-case-studies.md |
| Distributed Case Study: Going, Going, Gone | ch19-case-studies.md |

## Source Map: Chapter 20, Architectural Patterns

| Chapter section | Covered in |
|---|---|
| Introduction (styles vs patterns, best practices, patterns vs solutions) | ch20-patterns-vs-styles-and-reuse.md |
| Reuse | ch20-patterns-vs-styles-and-reuse.md |
| Separating Domain and Operational Coupling | ch20-patterns-vs-styles-and-reuse.md |
| Hexagonal architecture | ch20-patterns-vs-styles-and-reuse.md |
| Service Mesh | ch20-patterns-vs-styles-and-reuse.md |
| Orthogonal Coupling (sidebar) | ch20-patterns-vs-styles-and-reuse.md |
| Communication | ch20-communication-patterns.md |
| Orchestration Versus Choreography | ch20-communication-patterns.md |
| CQRS | ch20-communication-patterns.md |
| Infrastructure | ch20-broker-infrastructure-patterns.md |
| Broker-Domain Pattern (Single-Broker and Domain-Broker) | ch20-broker-infrastructure-patterns.md |

## Source Map: Chapter 21, Architectural Decisions

| Chapter section | Covered in |
|---|---|
| Chapter introduction (what an architectural decision is) | ch21-decision-antipatterns-and-significance.md |
| Architectural Decision Antipatterns | ch21-decision-antipatterns-and-significance.md |
| The Covering Your Assets Antipattern | ch21-decision-antipatterns-and-significance.md |
| Groundhog Day Antipattern | ch21-decision-antipatterns-and-significance.md |
| Email-Driven Architecture Antipattern | ch21-decision-antipatterns-and-significance.md |
| Architectural Significance | ch21-decision-antipatterns-and-significance.md |
| Architectural Decision Records | ch21-adr-structure-and-authoring.md |
| Basic Structure | ch21-adr-structure-and-authoring.md |
| Title | ch21-adr-structure-and-authoring.md |
| Status | ch21-adr-structure-and-authoring.md |
| ADRs and Request for Comments (RFC) (sidebar) | ch21-adr-structure-and-authoring.md |
| Context | ch21-adr-structure-and-authoring.md |
| Decision | ch21-adr-structure-and-authoring.md |
| Consequences | ch21-adr-structure-and-authoring.md |
| Compliance | ch21-adr-structure-and-authoring.md |
| Notes | ch21-adr-structure-and-authoring.md |
| Example | ch21-adr-structure-and-authoring.md |
| Storing ADRs | ch21-adr-practice-storage-and-ai.md |
| ADRs as Documentation | ch21-adr-practice-storage-and-ai.md |
| Using ADRs for Standards | ch21-adr-practice-storage-and-ai.md |
| Using ADRs with Existing Systems | ch21-adr-practice-storage-and-ai.md |
| Leveraging Generative AI and LLMs in Architectural Decisions | ch21-adr-practice-storage-and-ai.md |

Structural checks of ADR files (sections, status, supersession links, hedged decisions) and approval routing are automated in `scripts/adr_check.py`.

## Source Map: Chapter 22, Analyzing Architecture Risk

| Chapter section | Covered in |
|---|---|
| Chapter introduction (operational vs structural risk) | ch22-risk-matrix-and-assessment.md |
| Risk Matrix | ch22-risk-matrix-and-assessment.md |
| Risk Assessments | ch22-risk-matrix-and-assessment.md |
| Risk Storming | ch22-risk-storming-playbook.md |
| Phase 1: Identification | ch22-risk-storming-playbook.md |
| Phase 2: Consensus | ch22-risk-storming-playbook.md |
| Phase 3: Risk Mitigation | ch22-risk-storming-playbook.md |
| User-Story Risk Analysis | ch22-risk-storming-playbook.md |
| Risk-Storming Use Case | ch22-mitigation-patterns-and-case-study.md |
| Availability | ch22-mitigation-patterns-and-case-study.md |
| Elasticity | ch22-mitigation-patterns-and-case-study.md |
| Security | ch22-mitigation-patterns-and-case-study.md |
| Summary (cadence of risk storming) | ch22-risk-storming-playbook.md |

Scoring, phase-1 aggregation, assessment totals with direction and high-only filtering, and availability-to-downtime conversion are automated in `scripts/risk_storm.py`.

## Source Map: Chapter 23, Diagramming Architecture

| Chapter section | Covered in |
|---|---|
| Chapter introduction (communication, multiple views) | ch23-views-and-representational-consistency.md |
| Representational consistency | ch23-views-and-representational-consistency.md |
| Diagramming | ch23-views-and-representational-consistency.md |
| Tools | ch23-tools-fidelity-and-layers.md |
| Irrational Artifact Attachment (sidebar) | ch23-tools-fidelity-and-layers.md |
| Layers, Stencils/templates, Magnets | ch23-tools-fidelity-and-layers.md |
| Use Layers Semantically, Not Decoratively (sidebar) | ch23-tools-fidelity-and-layers.md |
| Diagramming Standards: UML, C4, and ArchiMate | ch23-standards-and-visual-guidelines.md |
| UML | ch23-standards-and-visual-guidelines.md |
| C4 | ch23-standards-and-visual-guidelines.md |
| ArchiMate | ch23-standards-and-visual-guidelines.md |
| Diagram Guidelines | ch23-standards-and-visual-guidelines.md |
| Titles | ch23-standards-and-visual-guidelines.md |
| Lines | ch23-standards-and-visual-guidelines.md |
| Shapes | ch23-standards-and-visual-guidelines.md |
| Labels | ch23-standards-and-visual-guidelines.md |
| Color | ch23-standards-and-visual-guidelines.md |
| Keys | ch23-standards-and-visual-guidelines.md |
| Summary (standards with exceptions) | ch23-standards-and-visual-guidelines.md |
| Summary (lightweight tools, CASE history, objectivity) | ch23-tools-fidelity-and-layers.md |

## Source Map: Chapter 24, Making Teams Effective

| Chapter section | Covered in |
|---|---|
| Chapter introduction | ch24-collaboration-and-architect-personalities.md |
| Collaboration | ch24-collaboration-and-architect-personalities.md |
| Constraints and Boundaries | ch24-collaboration-and-architect-personalities.md |
| Architect Personalities | ch24-collaboration-and-architect-personalities.md |
| The Control-Freak Architect | ch24-collaboration-and-architect-personalities.md |
| The Armchair Architect | ch24-collaboration-and-architect-personalities.md |
| The Effective Architect | ch24-collaboration-and-architect-personalities.md |
| How Much Involvement? | ch24-elastic-leadership-involvement.md |
| Team Warning Signs | ch24-team-warning-signs.md |
| Process Loss | ch24-team-warning-signs.md |
| Pluralistic Ignorance | ch24-team-warning-signs.md |
| Diffusion of responsibility (unheaded part of Team Warning Signs) | ch24-team-warning-signs.md |
| Leveraging Checklists | ch24-checklists-for-teams.md |
| The Hawthorne Effect (sidebar) | ch24-checklists-for-teams.md |
| Developer Code-Completion Checklist | ch24-checklists-for-teams.md |
| Unit and Functional Testing Checklist | ch24-checklists-for-teams.md |
| Software-Release Checklist | ch24-checklists-for-teams.md |
| Providing Guidance | ch24-design-principles-guidance.md |
| The Impact of Business Justifications (sidebar) | ch24-design-principles-guidance.md |
| Summary | ch24-design-principles-guidance.md |

The five-factor involvement scale is automated in `scripts/involvement_score.py`.

## Source Map: Chapter 25, Negotiation and Leadership Skills

| Chapter section | Covered in |
|---|---|
| Chapter introduction (negotiation and leadership as hard skills, further reading) | ch25-negotiation-playbook.md |
| Negotiation and Facilitation | ch25-negotiation-playbook.md |
| Negotiating with Business Stakeholders | ch25-negotiation-playbook.md |
| Negotiating with Other Architects | ch25-negotiation-playbook.md |
| Negotiating with Developers | ch25-negotiation-playbook.md |
| The Software Architect as a Leader | ch25-leadership-principles.md |
| The 4 Cs of Architecture | ch25-leadership-principles.md |
| Be Pragmatic, Yet Visionary | ch25-leadership-principles.md |
| Leading Teams by Example | ch25-leadership-principles.md |
| Integrating with the Development Team | ch25-team-integration-and-meetings.md |
| Developer Flow State (sidebar) | ch25-team-integration-and-meetings.md |
| Summary | ch25-team-integration-and-meetings.md |

The availability-to-downtime conversion used in stakeholder negotiation is automated in `scripts/availability_budget.py`.

## Source Map: Chapter 26, Architectural Intersections

| Chapter section | Covered in |
|---|---|
| Chapter introduction (the nine intersections) | ch26-implementation-and-infrastructure-alignment.md |
| Architecture and Implementation | ch26-implementation-and-infrastructure-alignment.md |
| Operational Concerns | ch26-implementation-and-infrastructure-alignment.md |
| Structural Integrity | ch26-implementation-and-infrastructure-alignment.md |
| Architectural Constraints | ch26-implementation-and-infrastructure-alignment.md |
| Architecture and Infrastructure | ch26-implementation-and-infrastructure-alignment.md |
| History: How Pets.com Gave Us Elastic Scale (sidebar) | ch26-implementation-and-infrastructure-alignment.md |
| Architecture and Data Topologies | ch26-data-topology-alignment.md |
| Database Topology | ch26-data-topology-alignment.md |
| Architectural Characteristics | ch26-data-topology-alignment.md |
| Data Structure | ch26-data-topology-alignment.md |
| Read/Write Priority | ch26-data-topology-alignment.md |
| Architecture and Engineering Practices | ch26-organizational-and-business-alignment.md |
| Architecture and Team Topologies | ch26-organizational-and-business-alignment.md |
| Architecture and Systems Integration | ch26-organizational-and-business-alignment.md |
| Architecture and the Enterprise | ch26-organizational-and-business-alignment.md |
| Architecture and the Business Environment | ch26-organizational-and-business-alignment.md |
| Architecture and Generative AI | ch26-generative-ai-intersection.md |
| Incorporating Generative AI into Architecture | ch26-generative-ai-intersection.md |
| Generative AI as an Architect Assistant | ch26-generative-ai-intersection.md |
| Summary | SKILL.md (purpose) |

No scripts: the chapter offers alignment criteria rather than calculations.

## Source Map: Chapter 27, The Laws of Software Architecture, Revisited

| Chapter section | Covered in |
|---|---|
| Chapter introduction (the three laws restated) | SKILL.md; ch27-why-and-spectrum-thinking.md |
| First Law: Everything in Software Architecture Is a Trade-Off | ch27-trade-off-analysis-method.md |
| Shared Library Versus Shared Service | ch27-trade-off-analysis-method.md |
| Synchronous Versus Asynchronous Messaging | ch27-trade-off-analysis-method.md |
| First Corollary: Missing Trade-Offs | ch27-hidden-trade-offs-and-reuse.md |
| Why We Can't Have Nice Things (sidebar) | ch27-hidden-trade-offs-and-reuse.md |
| Second Corollary: You Can't Do It Just Once | ch27-hidden-trade-offs-and-reuse.md |
| Second Law: Why Is More Important Than How | ch27-why-and-spectrum-thinking.md |
| Out of Context Antipattern | ch27-trade-off-analysis-method.md |
| The Spectrum Between Extremes | ch27-why-and-spectrum-thinking.md |
| Parting Words of Advice | ch27-why-and-spectrum-thinking.md |

Weighted and unweighted factor tallies, and detection of a winner flip caused by weighting, are automated in `scripts/tradeoff_matrix.py`.
