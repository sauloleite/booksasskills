---
name: fsa-theme-teams-and-leadership
description: Theme skill on the human and organizational side of architecture from Richards and Ford's "Fundamentals of Software Architecture" (2nd ed.) (chapters 24, 25 and 26). Use when deciding the right level of architect involvement for a team, spotting oversized teams, introducing checklists or library-approval principles, negotiating with stakeholders, peers and developers, leading without authority, managing meetings, or checking that implementation, infrastructure, data, practices, teams, integration, enterprise standards, business context and generative AI line up with the architecture.
---

# Teams, leadership and intersections (Fundamentals of Software Architecture, ch. 24 to 26)

An architecture only works when people and the surrounding ecosystem carry it out. This theme covers working with teams, negotiating and leading, and aligning everything around the design.

## Cross-chapter rules

1. **Size the constraints.** Too tight stifles developers, too loose forces them to make architectural decisions; define component responsibilities and leave internal design to the team.
2. **Adjust involvement.** Score familiarity, team size, experience, complexity and duration, and re-score as the project moves (`scripts/involvement_score.py`).
3. **Watch team-size warning signs.** Merge conflicts and coordination loss, silent disagreement, and unclear ownership.
4. **Use checklists sparingly** for error-prone, unordered work, and require technical plus business justification for new libraries.
5. **Negotiate with evidence.** Translate stakeholder buzzwords into characteristics, turn availability targets into concrete downtime (`scripts/availability_budget.py`), limit demanding requirements to where they matter, demonstrate rather than debate with peers, and give developers the reason before the decision.
6. **Lead by example.** Communicate clearly and concisely, avoid adding accidental complexity, be pragmatic yet visionary, protect developer focus from meetings, and stay present with the team.
7. **Align the intersections.** Implementation, infrastructure, data topology, engineering practices, team topology, integrations, enterprise standards, business context and generative AI must all support the chosen characteristics; "implementation detail" is a common failure point.

## Default workflow

1. Set your involvement level and team guardrails (ch24).
2. Prepare negotiations with facts and plan leadership habits (ch25).
3. Review each intersection against the architecture and add fitness functions where drift is likely (ch26).

<!-- BEGIN GENERATED: run tools/build_bundles.py to refresh -->

## References by chapter

Each link is one level deep; read only the files whose description matches the task.

### CH24: Making Teams Effective

- [ch24-checklists-for-teams.md](references/ch24-checklists-for-teams.md): read when drafting or reviewing a definition of done, test checklist or release checklist, or when checklists are being ignored.
- [ch24-collaboration-and-architect-personalities.md](references/ch24-collaboration-and-architect-personalities.md): read when the architect-team relationship is strained, when deciding what level of detail an architect should specify, or to diagnose control-freak or armchair behavior; includes diagnostic questions.
- [ch24-design-principles-guidance.md](references/ch24-design-principles-guidance.md): read when setting library or technology decision rights, handling a developer pushing a new technology, or generalizing tiered decision rights to other areas.
- [ch24-elastic-leadership-involvement.md](references/ch24-elastic-leadership-involvement.md): read when deciding how involved to be with a team or how many teams one architect can carry; includes invented scored examples and caveats.
- [ch24-team-warning-signs.md](references/ch24-team-warning-signs.md): read when a team seems too large, someone proposes adding headcount, meetings hide disagreement, or work is being dropped.

### CH25: Negotiation and Leadership Skills

- [ch25-leadership-principles.md](references/ch25-leadership-principles.md): read when reviewing a design for accidental complexity, balancing vision with practicality, rephrasing directives, framing requests as favors, or advising on greetings, boundaries and mentoring.
- [ch25-negotiation-playbook.md](references/ch25-negotiation-playbook.md): read when preparing for any negotiation with stakeholders, other architects or developers; includes ordered techniques, invented examples, pitfalls and a pre-negotiation checklist.
- [ch25-team-integration-and-meetings.md](references/ch25-team-integration-and-meetings.md): read when an architect is overloaded with meetings, disconnected from the team, protecting developer flow, or working with remote teams; includes a weekly calendar audit procedure.

### CH26: Architectural Intersections

- [ch26-data-topology-alignment.md](references/ch26-data-topology-alignment.md): read when choosing a database topology or database types, or when data shape or read/write balance seems to fight the style.
- [ch26-generative-ai-intersection.md](references/ch26-generative-ai-intersection.md): read when embedding an LLM into a system or when deciding how far to trust AI help on architecture decisions.
- [ch26-implementation-and-infrastructure-alignment.md](references/ch26-implementation-and-infrastructure-alignment.md): read for the nine-intersection audit table, code versus design conflicts, structural governance, constraint definition, and infrastructure or cloud deployment mismatches.
- [ch26-organizational-and-business-alignment.md](references/ch26-organizational-and-business-alignment.md): read when assessing engineering practices, fitness functions for agility, team structure, external integrations, enterprise standards, business direction, unknown unknowns or residuality theory.

Merged section maps: [source-maps.md](references/source-maps.md).

## Scripts

Python 3 standard library only; run any script with `--help` for its arguments.

| Script | Purpose |
|---|---|
| `scripts/involvement_score.py` (ch24) | Elastic-leadership involvement calculator (FSA Chapter 24 five-factor scale). |
| `scripts/availability_budget.py` (ch25) | Translate availability targets ("nines") into concrete downtime budgets, and back. |

<!-- END GENERATED -->
