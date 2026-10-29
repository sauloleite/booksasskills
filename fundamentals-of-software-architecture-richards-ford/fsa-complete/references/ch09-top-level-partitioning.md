# Top-Level Partitioning and Conway's Law

## Contents
- Why top-level partitioning matters
- Technical partitioning
- Domain partitioning
- Decision guide
- Conway's Law and the Inverse Conway Maneuver
- Kata recap: Silicon Sandwiches
- Invented worked example
- Pitfalls

## Why top-level partitioning matters

Components are generic containers, so they can be grouped in any way. Every grouping is a trade-off (the book's first law: everything in software architecture involves trade-offs). The grouping at the **top level** matters most, because it fixes the basic style and how code is organized, and it determines whether the architect starts component identification from technical roles or from business domains. Make this decision early and deliberately; it is among the first an architect faces.

Two families:

- **Technical partitioning**: top-level components are technical capabilities (presentation, business rules, services, persistence). Example style: layered monolith.
- **Domain partitioning**: top-level components are business domains or workflows. Example styles: modular monolith (one deployable, one database, popularized by Simon Brown), microservices.

Nesting is normal in both. A domain component can contain its own layers; a technical layer contains many subcomponents. Classification is by the top level only.

## Technical partitioning

Strengths:

- Code of one kind lives in one place, so it is easy to find all persistence or all presentation code.
- Separation of technical concerns limits ripple: if a layer depends only on its neighbors, a persistence change touches only adjacent layers.
- Familiar. It maps to Model-View-Controller, so many organizations adopt it by default.
- Isolates cross-cutting variation (for example customization) in dedicated partitions.

Weaknesses:

- Real workflows cut across every layer, so a single business change touches many partitions; the domain is spread thinly over all of them.
- Global coupling: shared partitions (common code, customization layers) affect every consumer when they change.
- Domain concepts may be duplicated across technical partitions.
- Tends toward one shared database spanning all domains, which is hard to untangle if the system later needs to become distributed.
- Encourages organizing people by skill (UI team, backend team, DBAs), which by Conway's Law reinforces the layering and slows cross-layer work.

## Domain partitioning

Strengths:

- Mirrors how the business operates rather than an implementation detail.
- Matches the axis along which most change requests arrive (a feature in one workflow).
- Supports cross-functional teams that own a domain end to end.
- Message flow follows the problem domain.
- Aligns with modular monolith and microservices; migrating components and their data to a distributed style later is comparatively easy.

Weakness:

- Cross-cutting variation (customization, shared policies) ends up repeated inside several domain components.

## Decision guide

Neither family is correct in general. Observed industry direction over recent years favors domain partitioning in both monoliths and distributed systems. Use these signals:

| Signal | Leans toward |
|---|---|
| Most change requests are "add or alter a business capability" | Domain |
| Teams are, or should become, cross-functional and product aligned | Domain |
| A future move to distributed deployment is plausible | Domain |
| Data will need to be split per domain later | Domain |
| Dominant variability is a cross-cutting technical concern that must stay in one place | Technical |
| Small, simple app with a stable workflow set and a skill-organized team | Technical can be fine |
| Team needs a familiar, low-ceremony default for a short-lived system | Technical can be fine |

Whichever is chosen, record the cost being accepted: scattered workflows (technical) or scattered cross-cutting variation (domain).

## Conway's Law and the Inverse Conway Maneuver

Conway's observation (late 1960s): a system's design tends to replicate the communication structure of the organization building it. Consequences:

- Skill-based departments (frontend, backend, DBA) naturally produce technically partitioned systems. That split of people is somewhat artificial and can block collaboration on shared business concerns.
- The **Inverse Conway Maneuver** (named by Jonny Leroy of Thoughtworks) flips the causality: shape teams to match the desired architecture, evolving both together. The broader practice is now usually discussed under the name team topologies.

Agent guidance: when proposing a partitioning, always ask how teams are organized. If the target is domain partitioning but teams are organized by skill, flag the mismatch and suggest team changes alongside the code changes; otherwise expect the code to drift back.

## Kata recap: Silicon Sandwiches

The kata is a sandwich-shop ordering system with chain-wide behavior plus per-location customization. The chapter compares two designs:

- **Domain-partitioned**: top-level components per workflow (purchasing, promotions, order preparation, inventory, recipes, delivery, location), each holding subcomponents for both shared and local variations.
- **Technically partitioned**: top-level components for shared versus local customization, with a few workflow components (purchase, delivery) remaining.

The verdict is "it depends": domain partitioning keeps workflows cohesive but repeats customization code; the customization-split design isolates customization but couples everything to the shared and local partitions, duplicates domain concepts across them, and invites a single database mixing customization and domain data.

## Invented worked example

A clinic scheduling product must support per-hospital rules (opening hours, booking limits). Proposal A: top-level `Scheduling`, `Billing`, `Patients`, `Notifications`, each with a `rules` subpackage. Proposal B: top-level `CoreRules`, `HospitalOverrides`, `Api`, `Persistence`.

Analysis:

1. Recent backlog: 80 percent of tickets are "change how booking works" or "change how billing works". That favors A.
2. The company plans to scale scheduling independently next year. A lets `Scheduling` and its tables move out with little untangling; B would need its shared schema split first.
3. Risk under A: each domain reimplements override lookup. Mitigation: a small shared library or an override service with a narrow contract, governed by a fitness function that forbids domain packages from importing each other.
4. Decision: A, with the duplication risk recorded in the ADR.

## Pitfalls

- Treating the layered default as a neutral choice. It is a decision with costs; make it explicitly.
- Classifying by nested structure instead of the top level.
- Choosing domain partitioning in code while keeping skill-based teams and one shared database, then wondering why boundaries erode.
- Reaching for distributed deployment to "get" domain boundaries; a modular monolith delivers the boundaries without the network costs.
