---
name: fsa-ch01-introduction
description: Frames software architecture as four interlocking dimensions (characteristics, logical components, style, decisions) analyzed in that order, applies three laws (trade-offs everywhere, rationale over mechanism, decisions on a spectrum) and the eight expectations of an architect. Based on Chapter 1 of Richards and Ford's "Fundamentals of Software Architecture" (2nd ed.). Use when scoping an architecture effort, separating architectural from technical decisions, challenging "no trade-off" claims, checking decision compliance or vitality, or coaching someone growing into the architect role.
---

# FSA Chapter 1: Introduction to Software Architecture

## Purpose

This skill gives an agent the foundational lens of the book: what counts as "architecture", the universal rules that govern every architectural judgment, and what an architect is accountable for beyond drawing boxes. Apply it at the start of any architecture conversation to frame the problem correctly (context first, analysis order, decision scope), and whenever a user claims a universal best practice, proposes a one-time standard, or makes a choice without recording why.

## Key decision rules (apply without opening references)

1. **Context first.** Every architecture is a product of the economics, tooling and practices of its time and place. Before recommending anything, ask what constraints (cost, licensing, ops maturity, team skills, regulation) shape this system. A style that is obviously right today may have been unaffordable a decade ago, and vice versa.
2. **Four dimensions, fixed analysis order.** Architecture = structure plus (a) architecture characteristics ("-ilities", the success criteria), (b) logical components (the behavior: domains, entities, workflows), (c) an architecture style chosen as the starting point, and (d) architecture decisions (the construction rules). Analyze characteristics and components first; only then pick a style; then codify decisions. Never start with a style.
3. **Pick the style that offers the easiest path** to the identified characteristics and components, not the most fashionable one.
4. **Law of trade-offs.** No architectural choice is free; each one gains some qualities at the expense of others. If an option appears to have no downside, assume the downside has not been found yet and keep looking.
5. **Trade-off analysis is never finished.** Reject attempts to settle styles, communication patterns or shared-code policies once for all projects. Re-evaluate per situation; defaults that work in one context fail badly in another (for example, mandating choreography everywhere).
6. **Rationale outweighs mechanism.** How a system works can be reverse-engineered from code; why it was built that way cannot. Always capture the alternatives considered and the trade-offs accepted.
7. **Decisions sit on a spectrum.** Reframe either/or debates as "where between the extremes, and why there".
8. **Guide, do not specify.** An architectural decision constrains a category (e.g., "use a reactive web framework"); picking the concrete product is a technical decision teams should own. Override only when a specific technology is required to protect a critical characteristic (scalability, performance, availability).
9. **A decision without enforcement is a suggestion.** Plan how each decision will be verified (reviews, automated fitness functions); unchecked violations silently erode the characteristics the decision protected.
10. **Watch vitality and structural decay.** Reassess architectures roughly every three years against business and technology change. Include test and release pipelines: fast coding with slow testing or releasing yields no real agility.
11. **Breadth over depth** when advising on technology: knowing the trade-offs of many options beats deep mastery of one.
12. **Expect challenge.** Broad decisions (e.g., making each database private to its owning application) raise costs for others and will be contested; prepare the business justification and negotiation path up front.

## Default workflow

1. Establish context: business domain vocabulary, goals, constraints, era-specific economics.
2. Identify the required architecture characteristics and the logical components.
3. Select a starting style that most easily satisfies both; note what it sacrifices.
4. For each significant choice: list options as points on a spectrum, surface the hidden trade-off, record the "why".
5. Classify each choice as architectural (guide) or technical (delegate); justify any exceptions.
6. Define how compliance will be checked and when the architecture will be re-assessed.
7. Map stakeholders who lose something from each decision and plan the negotiation.

## References

- [references/architecture-definition-and-context.md](references/architecture-definition-and-context.md): read when scoping an architecture, explaining what "architecture" includes, ordering the analysis, or arguing that context determines the right answer; also covers the book's three-part structure.
- [references/laws-and-trade-off-analysis.md](references/laws-and-trade-off-analysis.md): read when evaluating options, challenging "best practice" or "no downside" claims, writing decision rationale, or resisting one-size-fits-all standards.
- [references/architect-expectations-playbook.md](references/architect-expectations-playbook.md): read when separating architectural from technical decisions, planning compliance or vitality reviews, assessing an architect's skills, or handling stakeholder pushback and politics.
- [references/source-map.md](references/source-map.md): read to see which reference covers each chapter section.

## Scripts

None. The chapter is conceptual and offers no calculation or structural check that a script would make more reliable.
