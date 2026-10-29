---
name: fsa-ch25-negotiation-and-leadership
description: Applies Chapter 25 of Richards and Ford's "Fundamentals of Software Architecture" (2nd ed.) on negotiation and leadership. Covers negotiating with business stakeholders, peer architects and developers, the 4 Cs, essential vs accidental complexity, pragmatic yet visionary design, leading by example, and controlling meetings to stay with the team. Use when preparing for a contested decision, pushing back on an extreme requirement (e.g. five nines), resolving a disagreement, phrasing a request to developers, or auditing an architect's meeting load.
---

# Negotiation and Leadership Skills (FSA Chapter 25)

## Purpose

This skill helps an agent coach an architect through the people side of the role: getting contested decisions accepted by stakeholders, peers and developers, leading without relying on title, avoiding self-inflicted complexity, and protecting time to work alongside the team. The chapter's stance is that about half of architectural effectiveness is people skill, that almost every decision will be challenged, and that respect earned through collaboration is what makes future negotiations easy.

## Key decision rules (apply even without opening references)

**Negotiating with business stakeholders**
1. Treat buzzwords and exaggerations as signals of the real driving characteristic (urgency -> time to market, "fast" -> performance, "never down" -> availability).
2. Gather facts before negotiating (operating windows, volumes, incidents) and try to disprove your own position first.
3. Acknowledge the concern, then convert percentages into concrete downtime or latency per day and per year. Nines are abstract; minutes are not.
4. Divide and conquer: restrict demanding requirements to the parts of the system that truly need them.
5. Raise cost and time last, and qualify them with specifics. Opening with them sours the negotiation.

**Negotiating with other architects**
6. Prefer evidence over argument: run both options in a production-like environment and share results. Search results and chatbot output are not proof for a specific environment.
7. Do not overrule a peer by seniority. Stay calm and concise; if things get personal or heated, stop and resume later.

**Negotiating with developers**
8. Always justify decisions; never dictate from on high (Ivory Tower antipattern).
9. Put the reason before the demand, and phrase the demand as a neutral consequence of that reason rather than a personal order.
10. When a developer backs a rejected option, invite them to prove it meets the failed requirement. Either they gain buy-in by discovering the reason, or you gain a better solution.

**Leading**
11. Practice the 4 Cs: communication, collaboration, clear, concise (distinct from the C4 diagram model).
12. Remove accidental complexity (complexity you added) and keep only essential complexity (inherent in the problem). For every element, name the need it serves.
13. Be pragmatic yet visionary: weigh budget, time, team skill, trade-offs and technical limits. Find and fix the actual bottleneck before proposing strategic re-architecture.
14. Lead by example, not title. Offer suggestions as questions that leave the developer in control, not as directives; never belittle ideas in public; coach teammates who use condescending language.
15. For unwelcome work, use the person's name and ask for help as a favor rather than issuing a demand.
16. Respect cultural greeting norms and professional boundaries (handshake yes, hugs no). Become the go-to person: offer help unprompted, notice distress, run lunch-and-learns.

**Integrating with the team**
17. For meetings others call: ask why you are needed, read the agenda, attend only the relevant part, and go in place of developers or the tech lead.
18. For meetings you call: minimize them, replace announcements with written messages, keep an agenda, and schedule at the start of day, just after lunch, or end of day to protect developer flow.
19. Sit with the team or be visibly present; block daily time for questions and mentoring; adapt for remote teams.

## Default workflow

1. Identify the counterpart: business stakeholder, peer architect, or developer(s).
2. Collect signals and facts: buzzwords, business context, measurable data.
3. Pick the matching techniques (rules 1 to 10) and plan the opening sentence (acknowledge, then reason).
4. Quantify: run `scripts/availability_budget.py` for availability demands; scope the requirement to the parts that need it.
5. Prepare a demonstration if the dispute is technical.
6. Draft the wording: name, reason first, consequence or question instead of command; hold cost and time in reserve.
7. Afterwards, check the outcome for accidental complexity and record the agreed decision (for example in an ADR).
8. Periodically audit the architect's calendar and team presence (rules 17 to 19).

## References

- [references/negotiation-playbook.md](references/negotiation-playbook.md): read when preparing for any negotiation with stakeholders, other architects or developers; includes ordered techniques, invented examples, pitfalls and a pre-negotiation checklist.
- [references/leadership-principles.md](references/leadership-principles.md): read when reviewing a design for accidental complexity, balancing vision with practicality, rephrasing directives, framing requests as favors, or advising on greetings, boundaries and mentoring.
- [references/team-integration-and-meetings.md](references/team-integration-and-meetings.md): read when an architect is overloaded with meetings, disconnected from the team, protecting developer flow, or working with remote teams; includes a weekly calendar audit procedure.
- [references/source-map.md](references/source-map.md): read to see which reference covers each chapter section.

## Scripts

- Run `python3 scripts/availability_budget.py downtime 3n 4n 5n 99.95` to compute the allowed unplanned downtime per year, month, week and day for each availability target, so a stakeholder sees minutes instead of nines.
- Run `python3 scripts/availability_budget.py percent --per day --seconds 90` (or `--minutes`, `--hours`; `--per year|month|week|day`) to convert a tolerated downtime budget into the availability percentage it implies.
- Add `--json` before the subcommand for machine output; `--year-days` changes the year length (default 365.25). Published tables may differ by seconds due to rounding.
