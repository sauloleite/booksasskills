---
name: fsa-ch24-making-teams-effective
description: Applies Chapter 24 of Richards and Ford's "Fundamentals of Software Architecture" (2nd ed.) on how architects make development teams effective: bidirectional collaboration, constraints as a right-sized "room", control-freak vs armchair vs effective architects, five-factor elastic leadership scoring, team-size warning signs (process loss, pluralistic ignorance, diffusion of responsibility), checklists, and library decision rights. Use when calibrating architect involvement, diagnosing team dysfunction, drafting team checklists, or setting who decides on libraries and frameworks.
---

# Making Teams Effective (FSA Chapter 24)

## Purpose

This skill helps an agent advise an architect on the people side of architecture: leading the team through implementation rather than handing off diagrams. The chapter's central model is that the architect builds a "room" of constraints for developers. Too small and the team is stifled; too large and developers end up doing the architect's job. Everything else (calibrated involvement, warning signs, checklists, principle-based guidance) is a tool for sizing that room correctly and keeping the team healthy.

## Key decision rules (apply even without opening references)

1. **Collaborate both ways.** One-way handoff from architect to developers fails: decisions get lost going down and implementation changes never come back up. Put architect and developers on one virtual team.
2. **Size the room.** Over-constraining (banning needed libraries, dictating naming, method length, pseudocode) drives people away; under-constraining forces endless spikes and design debates.
3. **Architect defines components, developers design their insides.** The architect names a logical component, its responsibility, its core operations and its collaborators. Internal data structures, caching and patterns belong to developers.
4. **Watch for armchair drift:** no time for the team, shallow domain or technology knowledge, little hands-on coding, ignoring implementation consequences (complexity, maintenance, testing). Cure: get closer to the code and the business problem.
5. **Score involvement on five factors:** team familiarity, team size, overall experience, project complexity, project duration. Each from -20 (less) to +20 (more). New, large, junior, complex and long push toward more involvement.
6. **Duration is counterintuitive:** short projects need less architect involvement (urgency is built in); long ones need more (to keep pace and tackle the hardest work first).
7. **Rescore throughout the project and weight factors** when some matter more. The number is a guide, not a verdict.
8. **Team size thresholds:** the book calls 5 or fewer small and more than 12 big.
9. **Three signs a team is too big:** process loss (merge conflicts, collisions), pluralistic ignorance (private doubt, public agreement), diffusion of responsibility (dropped tasks, unclear ownership).
10. **Before adding a person, find a parallel workstream.** If none exists, warn the project manager that the addition will likely hurt.
11. **Facilitate dissent:** invite the quiet skeptic and support them for speaking, even if they turn out wrong.
12. **Checklists only for unordered, error-prone work.** Dependent sequences are procedures, not checklists; routine reliable tasks need none. Keep lists short, include the obvious, automate and remove items, avoid checklist sprawl.
13. **Grow checklists from failures:** QA defects feed the testing checklist; failed builds or deployments feed the release checklist after root-cause analysis.
14. **Make checklists stick** through shared reasoning, team co-authorship, and, if needed, announced verification with occasional spot checks (Hawthorne effect).
15. **Library requests answer two questions:** does it overlap existing functionality, and what is the technical and business justification?
16. **Decision rights by invasiveness:** special-purpose libraries, team decides; general-purpose, team recommends and architect approves; frameworks, architect only.
17. **Ask for the business case** to defuse technology crusades; it converts conflict into self-assessment.
18. **This is the architect's job,** not only the project or development manager's.

## Default workflow

1. Identify the symptom: frustration and attrition (room too small), confusion and churn (room too large), or dysfunction (size signals).
2. Ask the architect what they decide versus what developers decide; check against rule 3.
3. Score involvement (rules 5 to 7), or run the script; pick a stance (facilitator, mentor, close guide).
4. Check the three warning signs; if present, propose parallel workstreams, explicit owners, or a team split.
5. Publish decision-rights tiers for recurring choices (libraries first), with what a recommendation must include.
6. Introduce at most a few checklists (code completion, testing, release), co-authored, short, with an automation pass.
7. Set a date to rescore involvement and revisit checklists.

## References

- [references/collaboration-and-architect-personalities.md](references/collaboration-and-architect-personalities.md): read when the architect-team relationship is strained, when deciding what level of detail an architect should specify, or to diagnose control-freak or armchair behavior; includes diagnostic questions.
- [references/elastic-leadership-involvement.md](references/elastic-leadership-involvement.md): read when deciding how involved to be with a team or how many teams one architect can carry; includes invented scored examples and caveats.
- [references/team-warning-signs.md](references/team-warning-signs.md): read when a team seems too large, someone proposes adding headcount, meetings hide disagreement, or work is being dropped.
- [references/checklists-for-teams.md](references/checklists-for-teams.md): read when drafting or reviewing a definition of done, test checklist or release checklist, or when checklists are being ignored.
- [references/design-principles-guidance.md](references/design-principles-guidance.md): read when setting library or technology decision rights, handling a developer pushing a new technology, or generalizing tiered decision rights to other areas.
- [references/source-map.md](references/source-map.md): read to see which reference covers each chapter section.

## Scripts

- Run `python3 scripts/involvement_score.py --familiarity more --team-size 4 --experience less --complexity less --duration-months 2` to compute the five-factor involvement total (here -60, hands-off facilitator) and a recommended stance. Factors take `more`, `less`, `neutral` or a number in [-20, 20]; `--team-size` and `--duration-months` derive ratings by documented interpolation; `--weights experience=2` reweights factors; `--json` gives machine output. With `--team-size` it also prints the pairwise communication-channel count n(n-1)/2.
