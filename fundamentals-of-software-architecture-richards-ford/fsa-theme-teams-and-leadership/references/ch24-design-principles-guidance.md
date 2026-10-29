# Providing Guidance Through Design Principles

## Idea

Communicating design principles is another way to build the constraint room and one of the keys to a successful team. Principles tell developers which decisions they may make alone, which need the architect, and what evidence to bring. The chapter's running example is the layered stack: the set of third-party libraries an application is built from.

## Two questions for any proposed library

Before adopting a library, the developer answers:

1. **Overlap:** does this library duplicate functionality already in the system or in a library already in use? Skipping this check is how large projects accumulate duplicate capabilities.
2. **Justification:** why is it needed? Ask for both a technical and a business justification. Requiring the business case also trains developers to think in business terms.

## Sidebar lesson: the power of asking for a business justification

Paraphrased story: on a large Java project, one developer pushed hard to introduce Scala, so disruptively that two key colleagues planned to leave. The lead architect agreed to support Scala on one condition: a business justification covering retraining and rewrite costs. The developer happily went off to write it and returned the next day changed. They had plenty of technical arguments but could find no business value to offset the added cost, budget and schedule impact, and they recognized they had been disrupting the team. They became one of the most constructive members, and the two colleagues stayed.

Lessons for an agent:
- When a team member is fixated on a technology, do not argue technical merits; ask for the business case (cost, timeline, risk, value delivered).
- The request is not a trap. It turns a conflict into a self-assessment and builds business awareness.

## Decision-rights by library category

Communicate principles visually: a simple graphic showing which categories of decision belong to whom. The categories are examples; define more as needed.

| Category | What it is | Who decides |
|---|---|---|
| Special purpose | Narrow utilities for a specific need, where custom code is not warranted (PDF rendering, barcode scanning, image resizing) | Developers decide on their own |
| General purpose | Convenience wrappers over the language's standard API (for example, Apache Commons or Guava in Java) | Developers analyze overlap, write the justification, and recommend; the architect approves |
| Framework | Pervasive libraries that shape a whole application layer and are hard to remove (persistence, inversion of control, web frameworks) | Architect only; developers do not even do the analysis |

Why this ordering: the more invasive and harder to reverse a library is, the more it shapes the architecture, so decision rights move up. Narrow, easily replaced libraries cost little to get wrong.

## Generalizing the pattern beyond libraries

The same three-tier decision-rights structure works for other recurring questions. Invented examples:

| Domain | Team decides | Team recommends, architect approves | Architect decides |
|---|---|---|---|
| Data stores | Index changes, query tuning | New table or collection in an owned store | New database technology, shared data between services |
| Integration | Payload field additions (backward compatible) | New endpoint on an existing service | New communication protocol or broker |
| Infrastructure | Instance sizing within quota | New managed service already on the approved list | New cloud provider or region strategy |

How to roll out:
1. List the recurring decisions the team asks about.
2. Classify each by invasiveness and reversibility.
3. Assign each to a tier and publish a one-page graphic.
4. For the middle tier, define what a recommendation must contain (overlap analysis, technical and business justification).
5. Revisit tiers as the involvement score changes: a senior, settled team can take on more of the middle tier.

## Chapter summary and stance

- Making teams effective is hard and depends on experience and people skills, but three simple tools reliably help: elastic leadership (calibrated involvement), checklists, and guidance through design principles.
- The authors firmly reject the view that this belongs only to development or project managers. The architect leads the team technically through implementation, and a close working relationship lets the architect see team dynamics and adjust them.

## Review questions (original)

1. A developer asks to add a JSON schema validation library. Which tier is it, and what should the request include?
2. A team wants to replace the ORM. Who should do the analysis?
3. What would you ask a developer who insists a new language will make the team faster?
