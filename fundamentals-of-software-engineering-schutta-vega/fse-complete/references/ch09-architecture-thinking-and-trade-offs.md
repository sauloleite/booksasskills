# Architectural Thinking and Trade-Off Analysis

## Contents
- What counts as architecture
- Discovery questions before any design
- Trade-off analysis method
- Worked example: shared logic as a library or a service
- The accidental architect
- Architecture versus design
- Pitfalls
- Glossary

## What counts as architecture

The chapter frames architecture through three overlapping ideas:

1. **The big-picture structure**, borrowed from building construction: the parts that are expensive to rework once the foundation is laid (in software: deployment topology, datastore, integration style, language and framework platform, public contracts).
2. **The decisions that are costly to reverse later.** Software is easier to refactor than concrete, yet some choices (for example committing to many small services on a particular stack and then reconsidering half a year in) consume months to undo.
3. **The questions search engines cannot settle.** An error message has a findable fix; "which datastore suits this particular app" does not, because the answer depends on context no one else has.

So architecture is decision-making about hard-to-change things, grounded in trade-off analysis and the quality attributes (the "-ilities") that the system needs beyond its features. Good choices do not predict the future, but they keep likely future changes cheap.

## Discovery questions before any design

Before proposing structure, explore the problem space. Ask about:

| Area | Questions |
|------|-----------|
| Load | Total users? Concurrent users? What triggers spikes? When is it used (office hours, 24x7, seasonal)? |
| Geography | Where are users? One region or worldwide? |
| Availability and speed | Availability target? Acceptable response time per feature? |
| Environment | Which clouds are already contracted? Ideal deployment target versus current one? |
| Integration and constraints | What does it talk to? What is fixed (vendors, platforms, skills)? |
| Data | What is stored? Retention period? |
| Risk and rules | Applicable laws and regulations? Security policies? Privacy concerns? |
| Business | What do competitors offer that must be matched or beaten? |
| Cost and sustainability | Running cost and how to lower it? Carbon footprint and how to lower it? |

Agent behavior: when a user asks "what architecture should I use?", do not answer with a style name first. Ask the handful of these questions that matter, or state explicit assumptions for each and flag them as assumptions.

Invented illustration: an expense-approval tool for 800 staff in Portugal. Design-changing questions: EU hosting (GDPR), receipt volume and size (storage cost), retention of financial records, expansion to other countries (multi-region, multi-currency), and whether receipt OCR is in scope.

## Trade-off analysis method

Core stance: there is no correct architecture, only trade-offs, and often the goal is the least-bad option rather than the best one. "It depends" is a legitimate first answer, but it must be followed by **what** it depends on.

Procedure:
1. List the candidate options (at least two, including "do the simpler thing").
2. Identify the quality attributes that matter most for this system and rank them (see the quality-attributes reference).
3. Score each option per attribute. Do not just total the stars: weight by your ranking, because a style that looks mediocre overall may win on the two attributes you care about.
4. For each option, name the new failure modes it introduces and how they would be handled.
5. Decide within the deadline. Chasing a theoretically perfect architecture is a known way projects fail; pick the best achievable option and record the reasoning (ADR).

## Worked example: shared logic as a library or a service

Several modules need the same logic. Extracting it is sensible; the architectural question is how callers get it.

| Factor | Runtime dependency (remote service) | Build-time dependency (packaged library) |
|--------|-------------------------------------|------------------------------------------|
| Volatility | Fits logic that changes often | Fits stable logic |
| Freshness | Every caller sees the new version at once on deploy | Each consumer upgrades on its own schedule; version drift across the org is likely |
| Failure modes | New out-of-process call: timeouts, outages, latency; may need geo-distribution | No network hop, so that class of errors disappears |
| Testing | Harder (needs stubs, contract tests) | Simpler, runs in-process |
| Rollout of fixes | Central and immediate | Slow; requires each team to rebuild and redeploy |

Deciding questions: how volatile is it, and how much does it matter that every caller runs the latest rules? If you choose the service, design the fallback: a cached last-good answer, a safe default, or an alternative path.

Practice case: a tax calculator that depends on delivery address. Rules change often and stale rules cause legal risk, which pushes toward a service. But if the service is unreachable, checkout must not stop. A defensible answer: a service plus a locally cached rule set with a staleness limit, a clear policy for what happens when the cache is too old (for example accept the order and reconcile later), and alerting. Whatever you recommend, state the trade-off you accepted.

## The accidental architect

Many engineers do architecture without the title, because architects are scarce and stretched across many projects. If you are effectively the architect:
- Deliberately step back from the ticket to look at the whole system.
- Seek feedback from teammates and people elsewhere in the organization rather than deciding alone.
- Treat delegated architectural tasks as a growth path toward the role.

## Architecture versus design

The line is blurry, and the two constrain each other (the Twin Peaks idea: existing design limits architectural options; architecture limits design choices). Most decisions sit on a spectrum. Three tests place a decision on that spectrum:

| Test | Leans design (tactical) | Leans architecture (strategic) |
|------|-------------------------|--------------------------------|
| Time horizon | Fixes today's acute problem, possibly a stopgap | Serves long-term direction, may cost time now or require backing up |
| Who decides | One or two developers | Many roles, long discussions, possibly the CTO |
| Cost of change | Mechanical, IDE-assisted (rename or extract a method) | Breaks consumers or needs migration (renaming a public API, splitting a monolith into services) |

Why the distinction matters: it tells you who should own the decision and how much rigor (analysis, ADR, review) it deserves. Decisions in the middle of the spectrum should be made jointly by architects and developers.

Warning: tactical fixes ("duct tape") tend to outlive their intended lifetime. When taking one, write down that it is temporary and what the strategic fix would be. Investing time in the strategic path often saves time overall.

## Pitfalls
- Answering with a favorite style or tool before understanding load, data, constraints and regulations.
- Treating "it depends" as the end of the conversation instead of naming the factors.
- Comparing options by total score without weighting by priority.
- Adding a network call without designing for its failure.
- Spending strategic-level process on tactical choices, or making strategic choices casually in a pull request.

## Glossary
- **Twin Peaks**: the mutual, chicken-and-egg influence between architecture and design.
- **Least-worst option**: the realistic target when every option has costs.
