---
name: fsa-ch02-architectural-thinking
description: Applies the architectural-thinking mindset from Chapter 2 of Richards and Ford's "Fundamentals of Software Architecture" (2nd ed.). Covers placing a decision on the architecture-versus-design spectrum, two-sided trade-off analysis, translating business drivers into architecture characteristics, building technical breadth (knowledge pyramid, daily learning habit, personal technology radar), and staying hands-on without becoming a bottleneck. Use when deciding who owns a decision, comparing options, planning an architect's learning, or advising a developer moving into architecture.
---

# Architectural Thinking (FSA Chapter 2)

## Purpose

Help an agent reason like a software architect rather than like a feature developer. Chapter 2 frames architectural thinking as four habits: telling structural decisions apart from cosmetic ones, valuing breadth of technical knowledge over depth, analyzing both the upside and the downside of every option against the business context, and keeping coding skills alive without sitting on the team's critical path. Use the rules below directly; open a reference file when the task needs the full procedure, worked example, or checklist.

## Key decision rules

1. **Architecture vs design is a spectrum, not a binary.** Place a decision using three lenses: how strategic it is, how much effort it takes to build or reverse, and how heavy its trade-offs are. More of each pushes it toward architecture and toward the architect's ownership.
2. **Strategic signals:** weeks of planning rather than minutes, many stakeholders rather than one or two people, and an expected lifespan of years rather than a quick tactical step that is independent of other choices.
3. **Effort signal:** follow Fowler's framing that architecture is "the stuff that's hard to change". Cost to reverse matters as much as cost to build.
4. **Every option has costs.** Never present an option with benefits only. If you cannot name the downsides, the analysis is not done. Most architecture questions honestly resolve to a context-dependent answer; always spell out which factors it depends on.
5. **Context decides, not search engines or LLMs.** Answers hinge on deployment environment, business drivers, culture, budget, deadlines, team skills and more. Ask for these before recommending; never return a generic "best" choice.
6. **Pick the least-bad option.** Frame the final choice as a priority question between competing qualities (for example, extensibility versus security), and tie it back to a named business driver.
7. **Translate business goals into architecture characteristics** (scalability, performance, availability, and so on). This needs domain knowledge and working relationships with business stakeholders.
8. **Breadth beats depth for architects.** Knowing that five candidate solutions exist is more valuable than mastering one. Let some expertise fade deliberately; keep only what you actively maintain.
9. **Watch for two breadth dysfunctions:** trying to stay expert in everything (burnout, mastery of nothing) and stale expertise (old knowledge mistaken for current). Also watch for the Frozen Caveman: a past incident turned into a fixed fear applied to every new design. Keep risk assessment realistic.
10. **Architects must code, but off the critical path.** Avoid the Bottleneck Trap: delegate framework and critical-path code to the team and take a small business feature one to three iterations out.
11. **When team coding is impossible,** stay hands-on through production-quality proofs of concept, technical debt, bug fixes, automation (including fitness functions), and code reviews.

## Default workflow

1. **Classify the decision.** Score it on strategic weight, effort to change, and trade-off significance. Say whether it is architecture, design, or in between, and who should own it.
2. **Gather context.** Ask for business drivers, constraints, team skills, budget, timeline and environment. Name the architecture characteristics those drivers imply.
3. **Enumerate options widely.** Use breadth: list realistic alternatives, including ones the user did not mention.
4. **Analyze both sides of each option.** Build an advantages and disadvantages list per option; check security, contracts, coupling, extensibility, operability and scaling. Mark trade-offs that depend on a specific technology.
5. **Resolve with a priority question.** State which quality wins and why, given the drivers. Present the result as the least-bad fit for this context, not a universal answer.
6. **Validate cheaply when uncertain.** Recommend a production-quality proof of concept to compare finalists on real characteristics and effort.
7. **Close the loop on people.** If the user is an architect, check that they are not owning critical-path code and suggest a hands-on outlet; if they want to grow, suggest the daily learning habit and a personal radar.

## References

- [references/architecture-vs-design.md](references/architecture-vs-design.md): read when deciding whether a choice is architectural or design-level, who should own it, or how much rigor it deserves.
- [references/trade-off-analysis.md](references/trade-off-analysis.md): read when comparing options, writing a recommendation, translating business drivers into characteristics, or needing the worked messaging example (shared topic versus per-consumer queues).
- [references/technical-breadth-and-radar.md](references/technical-breadth-and-radar.md): read when planning learning, advising a developer becoming an architect, building a personal technology radar, or spotting Frozen Caveman reasoning.
- [references/hands-on-coding-balance.md](references/hands-on-coding-balance.md): read when an architect asks how much to code, what to code, or how to stay technical without slowing the team.
- [references/source-map.md](references/source-map.md): read to see which reference file covers each chapter section.

## Scripts

None. The chapter offers qualitative judgment frameworks rather than calculations, so no script is provided.
