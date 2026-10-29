# Communicating Architecture: Diagrams and ADRs

## Contents
- Diagrams: audience first
- Choosing a diagram
- Why record decisions
- ADR structure
- Status lifecycle
- Writing guidance
- Storage and tooling
- Example ADR (invented)
- Pitfalls

## Diagrams: audience first

Architecture is ultimately communication, and models are one of its main channels. The same picture cannot serve everyone: a diagram a developer finds ideal will confuse a VP of engineering. Before drawing, decide who it is for:
- a developer (components, interfaces, sequence of calls);
- a fellow architect (quality attributes, deployment, integration points, risks);
- a business partner (context: users, external systems, value flow);
- yourself (a scratch model to decompose a problem or explore an option; may never be shared).

## Choosing a diagram

Diagrams can establish context, explain or manage complexity, and surface quality attributes. Options include component, deployment, sequence and context diagrams; the C4 model offers zoom levels (context, container, component, code) that map well to audiences.

Decision rule: draw a diagram only if it helps tell the story for that audience at that moment; otherwise skip it. Choosing the right picture at the right time is a skill to practice.

Quick mapping:

| Need | Diagram |
|------|---------|
| Explain scope and neighbors to executives | System context |
| Show what runs where, scaling units, regions | Deployment or C4 container |
| Debug or design an interaction across services | Sequence |
| Agree module boundaries inside one deployable | Component |

## Why record decisions

Projects involve countless decisions, small (a variable name) and large (a cloud provider). Big forks get decided under time pressure with partial information, then the team moves on, and the reasoning evaporates. The second law of software architecture in Richards and Ford's framing: the why matters more than the how. Future maintainers, and you a few weeks later, need the reasoning. Architectural decision records (introduced by Michael Nygard) turn that knowledge into a sequential, readable log of how the system reached its current state. They should be short, but long enough to explain the reasoning.

## ADR structure

| Section | What goes in it |
|---------|-----------------|
| Title | Three-digit sequence number plus a descriptive name (for example `012. Use event streaming for order updates`). Numbers make the history sortable. |
| Status | Request for comment, Proposed, Accepted, or Superseded (organizations may vary). |
| Context | Constraints and circumstances behind the decision: forces, quality attributes at stake, mandated vendors or policies. Be generous here. |
| Options | Every alternative considered, and why any were dropped early. |
| Decision | What was chosen and why; which options were rejected and why. Prefer too much detail over too little. |
| Consequences | Positive and negative effects, new risks, follow-up work. Again, err toward detail. |
| Governance | How compliance will be checked: which fitness functions, reviews or alerts enforce it. |
| Notes | Metadata: authors, approvers, relevant dates (accepted, superseded), links. |

## Status lifecycle

- **Request for comment**: circulating so teammates and affected parties can comment.
- **Proposed**: drafted and awaiting approval.
- **Accepted**: reviewed and adopted.
- **Superseded**: replaced by a later ADR. ADRs are immutable; you do not rewrite an accepted ADR when you change your mind. You write a new one, and the only edit to the old one is a pointer to its replacement.

## Writing guidance

- Write for a reader on day one of the project. Do not omit "obvious" context; it will not be obvious to a newcomer later.
- Attach diagrams and supporting material when they help.
- Plain text (Markdown or AsciiDoc) is the common choice; it diffs well and is searchable.
- When in doubt, keep the process simple.
- Real ADR examples are scarce since companies rarely publish them; public architecture-kata submissions on GitHub (from O'Reilly's Architectural Katas events) include full ADR sets worth studying.

## Storage and tooling

- Keep ADRs in version control next to the code (for example `docs/adr/`) or in a wiki; either way, make them **searchable**, because nobody remembers which ADR covered that odd networking choice.
- Light tooling is enough. This skill's `scripts/adr_tool.py` creates the next numbered file, marks a superseded ADR, lints structure and status, and prints an index.

## Example ADR (invented)

```markdown
# 007. Package pricing rules as a versioned library, not a service

## Status
Accepted

## Context
Four services compute prices. Rules change about twice a year.
Top attributes: performance (p95 under 50 ms), availability.
A remote call adds a failure mode on the checkout path.

## Options
1. Central pricing service (rejected: new network dependency on checkout).
2. Shared library pinned per service (chosen).
3. Copy logic into each service (rejected: drift, quadruple fixes).

## Decision
Option 2. Low volatility makes slow rollout acceptable.

## Consequences
+ No network hop; simple in-process tests.
- Version skew between services; upgrades need four deploys.

## Governance
CI check fails if a service is more than one minor version behind.

## Notes
Authors: R. Lima. Accepted 2026-03-02. Revisit if rules change monthly.
```

## Pitfalls
- No ADRs at all, so the same debates recur every year.
- Editing accepted ADRs in place, erasing the history.
- Decision without options or consequences (a press release, not a record).
- Governance left empty, so the decision silently erodes.
- One diagram reused for every audience.
