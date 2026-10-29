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
