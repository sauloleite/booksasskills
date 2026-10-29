# Diagram Catalog: Why Model and Which Diagram to Draw

## Contents
- Why software teams model at all
- The blueprint analogy and where it breaks
- When diagrams pay off
- Diagram lifespan
- Situation questions for choosing diagrams
- Formal versus informal notation
- Selection matrix
- Diagram types in detail
- Workshop and specialty models
- Worked example
- Glossary

## Why software teams model at all

Modeling means building simplified representations of a system so people can reason about its structure, behavior and purpose, and so they can talk about it. A good model mirrors the problem domain closely enough to generate insight during design and development. Models serve many consumers: end users, testers, other developers, security reviewers, budget holders, project managers, architects, and very often only the author. The central skill is not drawing; it is knowing which picture a given reader needs at a given moment.

Software has borrowed vocabulary and methods from older fields (architecture, quality assurance, even library science), and modeling fashions have come in waves, from UML in the 1990s to the C4 model today. Treat any single fashion with skepticism and pick what serves the current communication need.

## The blueprint analogy and where it breaks

In construction, full plans precede work because physical change is costly: you cannot try out a structural wall in production. Plans prove code compliance, route utilities, let the owner approve the design, and later verify the result. Software differs because changing code usually costs hours, not demolition (though refactoring is often pricier than people expect). That malleability makes exhaustive up-front diagrams less critical.

Diagrams also never compile. Following Jack Reeves's "Code as Design" argument, programming is itself design work, and source code is the most faithful expression of that design. So an agent should never let diagram production block or substitute for working code.

## When diagrams pay off

Use a diagram when it does one of these jobs:

- **Provides context** that code alone hides: who calls whom, where the edges are.
- **Manages complexity** by decomposing a problem into parts you can reason about separately.
- **Predicts quality attributes** (scalability, availability, security and the other nonfunctional "abilities") and lets you design for them before building.
- **Plans a design.** Cheap sketching before coding can avert days of wrong-direction work.
- **Supports software archaeology**: learning a legacy or unfamiliar system.
- **Speeds onboarding and knowledge transfer** to new teammates.
- **Guides debugging and test design** by making system boundaries and core responsibilities explicit.
- **Satisfies process requirements** where an SDLC mandates artifacts. This can help (forces thinking) or hurt (forces busywork).

Every benefit above except planning depends on the diagram being accurate. A clear, current diagram is an asset; an outdated one can do active harm by teaching people a system that no longer exists.

## Diagram lifespan

Diagrams sit on a spectrum from a whiteboard sketch erased within the hour to a formal model maintained in a tool. It is acceptable for a diagram to expire once it stops being useful. Decision rule:

| Signal | Action |
|---|---|
| Used once to think or align in a meeting | Photograph or discard |
| You keep redrawing the same picture | Formalize it in a tool, store it centrally, share it |
| Large and referenced daily by the team | Print it big (plotter) and post it; tangible copies get attention |
| Derivable from code | Generate it on demand or in CI rather than maintaining by hand |

## Situation questions for choosing diagrams

The honest answer to "which diagrams do we need" is that it depends. Ask:

1. What exactly are we trying to accomplish (align on scope, design an interaction, validate uptime, onboard someone)?
2. How complicated is the problem?
3. How risky is the application if it fails?
4. Has this team built something like it before, or is it novel?
5. What budget and time are available?
6. How critical is the system to the business?

More complexity, risk, novelty and criticality justify more diagrams, more rigor, and longer-lived models. A low-risk, familiar, low-budget project may need one sketch.

## Formal versus informal notation

- **Formal** models use defined notation (UML, or a mathematical specification language such as Z). Precision rises, but the pool of readers who can decode it shrinks. Even if you are fluent, ask how many people in the organization are.
- **Informal** box-and-line diagrams reach broader audiences, including nontechnical people.

UML emerged in the mid-1990s to unify competing notations, became an OMG standard in 1997, and an ISO/IEC standard (19501) in 2005. Despite that pedigree, most engineers prefer informal diagrams that borrow selected UML elements. Subtle notation details (such as filled versus hollow diamonds for composition versus aggregation) are lost on most readers. Default to simple; use what works for your readers.

## Selection matrix

| Diagram | Answers | Typical audience | When in project | Durability |
|---|---|---|---|---|
| Context | What is in and out of scope; what external actors exchange | Architects, leadership, PMs, product owners | Early | Stable; high level |
| Component | What runtime parts exist and how they interact | Devs, architects, production support, DevOps | Throughout | Medium |
| Class | How types relate (inheritance, composition, cardinality) | Engineers, architects | Early, refined throughout | Rots fast; extract from code |
| Sequence | How one significant flow unfolds over time | Devs, architects, DevOps, QA | Throughout | Rots if detailed; extractable |
| Deployment | Where software runs, on what, connected how | Architects, devs, DevOps, infra, security, middleware | Early (validate quality attributes) | Medium; follows infra |
| Security | Trust zones, protocols, PII handling | Devs, architects, security | Throughout | Medium |
| Data model | Entities and relationships at chosen granularity | Customers to DBAs | Very early, refined throughout | Evolves with domain |

## Diagram types in detail

### Context diagram
The most zoomed-out view: one box for the system, surrounded by the people and systems it exchanges information with. Arrows can be annotated with the logical data involved and, where useful, its volume and frequency. Use it at kickoff to agree on boundaries, especially what is explicitly out of scope. Keep internals out entirely.

### Component diagram
Shows the main runtime elements, the interfaces between them, and how information moves. Originally a design-time statement of intended interactions, it doubles as the best narrative for a technical audience and is a staple of onboarding. Large systems need several component diagrams split at logical seams rather than one wall chart.

### Class diagram
Shows classes, inheritance, composition, optional cardinality, and methods only where they clarify. Because it drifts from code quickly, prefer extracting it from source when needed instead of hand-maintaining it. For big codebases, slice by domain or module so each view is digestible. Useful early to sketch the overall shape, then refined.

### Sequence diagram
Depicts the ordered messages within a single flow, including only the participants involved. Never attempt to document every flow; choose the architecturally significant or most interesting ones, or use it to show a pattern or the canonical way to use a library. Showing parameters and return types helps developers but accelerates staleness. Can be extracted from running or static code, handy when entering a new codebase. QA uses these to decide what to test. Usually authored by developers or solution architects.

### Deployment diagram
A runtime view of hardware or infrastructure nodes, the software on each, the connections, protocols, cardinality and optionally component versions. Always label it as **logical** (a cluster drawn as one box) or **physical** (the actual count of load balancers or servers). Draw it early to test quality attributes: a 24/7 system deploys very differently from one with relaxed uptime needs; the diagram helps check scaling, business continuity and cost. Most organizations offer a constrained, Lego-like kit of approved platforms and reference architectures. Model with what is actually permitted: no Azure-specific icons in an AWS shop, no unapproved database engine when a corporate standard exists.

### Security diagram
A specialization of the deployment or technology view focused on protection mechanisms: which parts sit inside the secure zone versus outside the firewall, and which protocols (for example HTTPS, LDAP) cross each boundary. Used throughout a project both to set a pattern and to verify that security needs are met. Explicitly consider personally identifiable information and applicable regulations.

### Data model
Entities and their relationships at three levels of increasing concreteness:
- **Conceptual**: very high level, not normalized, understandable by customers.
- **Logical**: business terms, usually normalized.
- **Physical**: implementation details including data types, for DBAs and developers.

Created very early to illustrate the domain and refined for the life of the project. Audience ranges from customers to information architects, DBAs, developers and support.

## Workshop and specialty models

Often the act of building these together is the payoff: teams discover they never shared an understanding of the problem.

- **Event storming**: a collaborative workshop (in person or remote) where business and technical people map domain events, the commands that trigger them, and the actors issuing those commands, with sticky-note colors per category. Lightweight and adaptable.
- **Value stream mapping**: models the current process and a target future state to expose friction and bottlenecks.
- **User story mapping**: lays out the user experience as high-level activities across the top with steps and details beneath, built jointly with sketches and sticky notes.
- **Disaster recovery models**: detail runtime entities and their hardware to define business continuity requirements. Weigh how many people an outage affects and what downtime costs. Importance grows as production release approaches.

## Worked example

A developer joins a team building a parcel-tracking service and is asked to "document the architecture" for three groups.

- Steering committee: one context diagram showing the tracking service, carriers' feeds, the customer mobile app, and the billing system, with a note that returns processing is out of scope. No technology names.
- New engineers: two component diagrams (ingestion side, customer-facing side) that reference each other, plus one sequence diagram for the "carrier scan event updates customer" flow, generated from tracing data where possible.
- Ops and security review: a physical deployment diagram labeled with node counts for the 24/7 ingestion tier, and a security overlay showing the public API outside the firewall, TLS on every edge, and where customer addresses (PII) are stored.

Nothing else is drawn until someone needs it.

## Glossary

- **Cardinality**: how many instances on one side of a relationship correspond to the other (one to many, and so on).
- **Normalization**: structuring data to cut redundancy and protect integrity.
- **Quality attributes**: nonfunctional requirements such as availability, scalability, security, cost.
- **Software archaeology**: reconstructing understanding of an existing, often poorly documented system.
- **C4 model**: a layered approach (context, containers, components, code) to architecture diagrams.

See also: modeling-practices-and-tools.md for drawing and review practices.
