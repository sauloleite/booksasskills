# What Architecture Is, and Why Context Decides

Covers: the chapter opening (audience, why the role matters, context), the four-dimension definition, and the roadmap of the book.

## Who this framing serves

The book addresses three kinds of readers, and an agent should recognize each:

- **Developers aiming for the next career step** who want to see how large parts of systems fit together.
- **Managers** who want to understand why some architectures succeed.
- **Accidental architects**: people who already make architecture decisions (as defined below) without holding the title. When a user describes choosing styles, data ownership or integration rules, treat them as an architect regardless of job title, and apply the full discipline.

## Why the role resists automation

The authors position architecture as work centered on trade-off judgment inside complex, shifting contexts, often with incomplete information. Generative tools can produce candidate designs, but weighing competing characteristics against a specific organization's constraints remains a human responsibility. Agent implication: when assisting, present options with explicit trade-offs and leave the weighing transparent; do not hand down a single "correct" architecture as if context were irrelevant.

## Context determines the right answer

Architectures only make sense against the conditions that produced them.

- In the late twentieth century, operating systems, application servers and databases were costly commercial products, so a dominant design goal was to share infrastructure as efficiently as possible.
- A design in which every service owns isolated machinery and a private database would have required dozens of paid OS, app-server and database licenses around the early 2000s, making it economically absurd then.
- Open source software and DevOps engineering practices removed those cost barriers, which is what made such distributed styles feasible.

**Checklist: context questions before recommending anything**

- What does infrastructure, licensing and operations actually cost here?
- How mature are deployment automation and operational practices?
- What did the original architects optimize for, and does that constraint still hold?
- Which past assumptions (scarcity of hardware, licensing, team size) have changed?

Use the answers to explain both why a legacy design looked the way it did and whether its reasons still apply.

## The four-dimension definition

Architecture is the system's **structure** combined with four dimensions. Analyze them in this order:

| Order | Dimension | What it captures | Key question |
|---|---|---|---|
| 1 | Architecture characteristics | The "-ilities": capabilities and success criteria the system must support | What must this system be good at to succeed? |
| 2 | Logical components | The behavior: domains, entities and workflows the system implements | What does the system do, and how is that behavior partitioned? |
| 3 | Architecture style | The named topology used as a starting point | Which style gives the easiest path to (1) and (2)? |
| 4 | Architecture decisions | Rules that constrain construction: what teams may and may not do | Which constraints keep the implementation aligned with (1)? |

Notes for applying it:

- Characteristics and logical components are the two structural analyses; each needs its own techniques. Their outputs are what make style selection possible.
- The style is scaffolding, not a goal. It reflects the general philosophy of the implementation.
- Decisions are expressed as rules. Example of the shape: "in a layered design, only the domain and service layers may touch the database; the UI layer may not." Such a rule both directs teams and limits them.
- Architecture is broader than boxes and lines: principles, characteristics and decisions are part of it.

**Worked example (invented).** A team asks, "Should our claims platform use event-driven microservices?"

1. Redirect to characteristics first: the business needs auditability, burst scalability during storms, and moderate cost.
2. Identify logical components: intake, assessment, payment, fraud review, notifications.
3. Only now compare styles: a modular monolith may satisfy auditability and cost with less operational load; event-driven pieces may be justified only around the bursty intake workflow.
4. Record decisions as rules: "payment owns its data; other components request payment status through its API."

## Roadmap of the book (for routing)

The book is organized in three parts, which mirrors the definition above:

- **Part I, Foundations**: how to analyze architecture characteristics and logical components; these outputs feed style selection.
- **Part II, Architecture Styles**: a catalog of named topologies, comparing structure, communication, data topology, team alignment and physical deployment.
- **Part III, Techniques and Soft Skills**: decision recording, risk, diagramming, negotiation, leadership. The authors stress that these people-centered skills are frequently the hardest for new architects, because the path into the role usually rewards technical rather than interpersonal strength.

Agent implication: if a user's question is about style selection but they have not established characteristics, step back to Part I thinking first; if the problem is adoption or pushback, treat it as a Part III problem rather than a technical one.

## Short glossary

- **Accidental architect**: someone making architecture-level decisions without the title.
- **Architecture characteristics**: non-domain qualities ("-ilities") that define success, such as scalability, availability, performance.
- **Logical components**: building blocks of behavior, typically aligned to domains and workflows.
- **Architecture style**: a named, reusable topology chosen as the implementation's starting point.
- **Architecture decision**: a constraint on how the system is built, with recorded justification.
