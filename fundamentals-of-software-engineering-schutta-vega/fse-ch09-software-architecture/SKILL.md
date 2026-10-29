---
name: fse-ch09-software-architecture
description: Architecture guidance for engineers growing into design decisions, based on Chapter 9 of Schutta and Vega's "Fundamentals of Software Engineering". Covers trade-off analysis, architecture vs design (strategic vs tactical), quality attributes, stakeholder alignment, monolithic vs distributed styles, evolutionary architecture, hypothesis-driven development, fitness functions, diagrams, ADRs and katas. Use when someone asks which architecture, style or datastore to pick, compares options, writes or lints an ADR, defines fitness functions, or practices architecture.
---

# FSE Ch. 9: Software Architecture

This skill helps an agent coach a developer through architectural work: framing the problem with the right questions, ranking quality attributes, comparing options by explicit trade-offs, choosing a style, keeping the architecture healthy with fitness functions, and recording decisions in ADRs that a newcomer can follow. It distills Chapter 9 of Schutta and Vega's "Fundamentals of Software Engineering", whose central message is that architecture has no right answers, only trade-offs judged against the system's context. The chapter is an on-ramp; for style-by-style depth it points to dedicated architecture books.

## Key decision rules

Apply these even without opening a reference.

**Framing**
1. Treat as architecture anything that is costly to reverse later, plus the quality attributes beyond features. Spend rigor proportional to the cost of change.
2. Never open with a style or product name. First gather context: users and concurrency, geography, availability and latency targets, spike triggers, usage hours, integrations and constraints, contracted clouds, current vs ideal deployment, data and retention, laws, security, privacy, cost, carbon footprint, competitors. If answers are missing, state assumptions explicitly.
3. "It depends" is acceptable only when followed by the factors it depends on.

**Trade-offs**
4. Aim for the least-bad option, not a perfect one. Weight each option's ratings by your ranked attributes; do not just add up stars.
5. Every new network hop is a new failure mode. If you choose a runtime service over a build-time library, design the fallback (cached answer, default, alternative path). Volatile logic that must be current for every caller favors a service; stable logic favors a library (simpler tests, but slow rollout and version drift).
6. Decide within the deadline; chasing academic perfection sinks projects.

**Architecture vs design**
7. Place each decision on the tactical-to-strategic spectrum using three tests: time horizon, who must be involved (one or two developers vs many roles up to the CTO), and cost of change (IDE refactor vs breaking consumers). Middle-ground decisions are made jointly by architects and developers.
8. Label tactical stopgaps as temporary and note the strategic fix; stopgaps routinely outlive their plan.

**Quality attributes**
9. With stakeholders, say "quality attributes", not "nonfunctional requirements"; frame benefits in their terms and examples.
10. Identify attributes from signal phrases (bursts, never-twice, 24x7, regulated data) and from implied, unstated needs (abuse, bots, scale-down cost).
11. Rank a short list (numbered list, table or mind map), share it with stakeholders, iterate. Name the tensions explicitly (security vs usability, elasticity vs cost). Champion simplicity.
12. When a proposal meets resistance, use indirection: reframe as additive or a pilot, anchor on a felt problem, recruit a respected ally; influence often lies off the org chart.

**Styles**
13. Choose a style only after ranking attributes. Monolithic: layered, microkernel, pipeline (big ball of mud is the failure mode). Distributed: service-oriented, microservices, event-driven, space-based.
14. Pick microservices when elasticity and scalability are top-ranked; otherwise prefer something simpler. They cost network latency, complexity, money, observability effort and harder debugging. A disciplined modular monolith is maintainable; bad modularity, not single deployment, is what hurts.

**Evolution and governance**
15. Design expecting change; architectural work may span iterations. Validate changes with hypothesis-driven development: change, expected outcome, metric and threshold chosen in advance.
16. Architectures decay without active effort. Turn each top attribute into a fitness function (latency budget, complexity cap, load-scaling curve, dependency rule), automate it in CI/CD where possible, and review the set periodically.

**Communication**
17. Pick each diagram for one audience and draw it only if it helps tell the story.
18. Record significant decisions as ADRs: three-digit sequential ID and descriptive title; Status, Context, Options, Decision, Consequences, Governance, Notes. Err toward more context. Accepted ADRs are immutable: supersede, do not edit. Keep them in plain text, searchable, written for a first-day reader.

## Default workflow

1. Classify the request: tactical design question or strategic architecture question (rule 7). For tactical ones, answer directly.
2. Gather or assume context with the discovery questions.
3. Extract, rank and put in tension the top 3 to 7 quality attributes; confirm with the user.
4. Generate at least two options (always include a simpler one) and compare them in a weighted trade-off table, including failure modes and fallbacks.
5. Recommend, stating what is sacrificed and why.
6. Propose fitness functions for the top attributes and, if the change is uncertain, a hypothesis with a metric.
7. Draft an ADR (use the script), plus one audience-specific diagram if it helps.
8. Note stakeholder framing: who must agree, which attributes need selling, any indirection strategy.

## References

- [references/architecture-thinking-and-trade-offs.md](references/architecture-thinking-and-trade-offs.md): read when scoping a new system, running a trade-off analysis (library vs service worked example), or deciding whether something is architecture or design.
- [references/quality-attributes-and-styles.md](references/quality-attributes-and-styles.md): read when extracting and ranking quality attributes from requirements, persuading stakeholders, or choosing between monolithic and distributed styles.
- [references/evolutionary-architecture-and-fitness-functions.md](references/evolutionary-architecture-and-fitness-functions.md): read when working in Agile teams, writing a hypothesis for an architectural change, or designing and maintaining fitness functions (includes sample checks).
- [references/adrs-and-architecture-diagrams.md](references/adrs-and-architecture-diagrams.md): read when writing or reviewing an ADR, managing ADR status, or choosing a diagram for an audience.
- [references/practice-with-architectural-katas.md](references/practice-with-architectural-katas.md): read when the user wants to practice architecture, run a kata session or interview, or asks for further reading.
- [references/source-map.md](references/source-map.md): read to find which file covers a given chapter section.

## Scripts

`scripts/adr_tool.py` (Python 3 stdlib). Run it to create numbered ADRs, mark superseded ones, check ADR structure, and list ADRs.

- Run `python3 scripts/adr_tool.py new --dir docs/adr --title "Adopt event streaming for orders" --authors "Ana" --date 2026-10-29` to create the next `NNN-slug.md` from the template (default status Proposed).
- Run `python3 scripts/adr_tool.py new --dir docs/adr --title "..." --supersedes 3` to create a replacement and set ADR 003's status to "Superseded by NNN". Do this only once the replacement is agreed.
- Run `python3 scripts/adr_tool.py lint --dir docs/adr` to check ID/title consistency, duplicates and gaps, missing or placeholder sections, valid status, supersede targets, and Governance on accepted ADRs. Exits 1 on any ERROR.
- Run `python3 scripts/adr_tool.py index --dir docs/adr` to print a Markdown table of ID, title and status.
