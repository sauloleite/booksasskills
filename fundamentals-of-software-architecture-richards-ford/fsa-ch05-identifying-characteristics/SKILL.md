---
name: fsa-ch05-identifying-characteristics
description: Guides identification of architecture characteristics ("-ilities") from domain concerns, requirements and implicit domain knowledge; decomposing composite goals like agility; telling scalability from elasticity; deciding architecture versus design; and pruning to a short prioritized list via a worksheet and top-three selection. Based on Chapter 5 of Richards and Ford's "Fundamentals of Software Architecture" (2nd ed.). Use when gathering non-functional requirements, translating business goals into -ilities, running an architecture kata, or running a stakeholder prioritization session.
---

# Identifying Architecture Characteristics

## Purpose

Help an agent turn a business problem into a small, justified set of driving architecture characteristics. The work has three moves: elicit candidates from three sources, translate and decompose business language into measurable characteristics, then cut the list down and let stakeholders pick what matters most. The output feeds trade-off analysis, style selection and decision records.

## Key decision rules (apply even without opening references)

1. **Mine three sources**: stakeholder domain concerns, requirements artifacts, and the architect's implicit domain knowledge. Always add a pass for what an industry veteran would assume unstated (for example data integrity in medical device software).
2. **Translate, do not echo**: stakeholders speak in outcomes (acquisitions, time to market, user satisfaction, competitive advantage, tight budget). Map each to candidate -ilities, then ask which outranks which.
3. **Decompose composites**: a goal without a direct measure (agility, "on time every day") is a composite. List its measurable parts. Never equate a composite with one part or with one business concern.
4. **Run failure questions** on any single obvious characteristic: fast but down? volume grows? crash midway? fast but wrong? provable later? Each relevant answer adds a characteristic (availability, scalability, reliability, recoverability, auditability).
5. **Decode numbers**: user counts imply scalability; real usage rhythm (mealtimes, deadlines, on-sale moments) implies elasticity, even when unstated. Keep the two separate.
6. **Define performance against scale**: a baseline at no particular load plus an acceptable level at a stated user count.
7. **Implicit is not automatically architectural**: availability, stability, security are always present; promote one only if it shapes structure and is critical to success. Delegating payments to a processor plus routine hygiene keeps security in design.
8. **Guard against brittleness**: integration points threaten reliability, but prefer degrading gracefully over failing when a non-essential dependency is down.
9. **Architecture or design?** For each characteristic ask: reasons to avoid the structural option (performance, coupling)? does either option hurt other characteristics? what is the total cost of supporting everything in architecture versus design? Decide with the implementation team, never alone (Ivory Tower antipattern).
10. **Keep the list short**: each characteristic adds complexity; a generic architecture that supports everything is an antipattern. Overspecifying is as harmful as underspecifying.
11. **Cap and prioritize**: around seven driving slots (six or eight fine); overflow goes to "others considered"; stakeholders pick an unordered top three. Do not chase a full ranking.
12. **Eliminate one**: ask which characteristic you would drop first. Explicit ones are usually the first cut; implicit ones tend to support overall success. A dropped characteristic may move into design rather than vanish.
13. **No perfect answer**: aim for the least bad set of trade-offs; the mistakes to avoid are the expensive ones.

## Default workflow

1. Gather the problem statement, users, requirements and additional context (kata format works well).
2. Elicit candidates from all three sources; translate business concerns.
3. Decompose composites with failure questions; decode numbers into scalability, elasticity and performance-at-scale.
4. Walk every requirement and context item: tag as none, design concern, or architectural characteristic.
5. Check each candidate for overspecification, fragility, and whether design alone suffices.
6. Fill a capped worksheet; move overflow to others considered; pull implicit items in only when they need special structure.
7. Run the elimination exercise; get stakeholders to pick an unordered top three.
8. Hand off: driving list, top three, others considered with reasons, and objective definitions for each driver.

## References

- [references/elicitation-and-translation.md](references/elicitation-and-translation.md): read when extracting characteristics from business goals or requirements, decomposing a composite goal, separating explicit from implicit, or distinguishing scalability, elasticity and performance.
- [references/katas-and-requirement-walkthrough.md](references/katas-and-requirement-walkthrough.md): read when running or simulating an architecture kata, doing a requirement-by-requirement analysis, or deciding whether a characteristic belongs in architecture or design.
- [references/limiting-and-prioritizing.md](references/limiting-and-prioritizing.md): read when the candidate list is too long, when facilitating a stakeholder prioritization session with the worksheet, or when choosing the top three.
- [references/source-map.md](references/source-map.md): read to locate which reference covers a given chapter section.

## Scripts

None. The chapter's guidance is qualitative and facilitation-based; no calculation warrants a script.
