---
name: fse-ch04-modeling
description: Guidance for software modeling and diagramming as a communication tool, based on Chapter 4 of Schutta and Vega's "Fundamentals of Software Engineering". Covers why and when to diagram, choosing among context, component, class, sequence, deployment, security, data and workshop-style models, formality versus audience, keeping diagrams simple and accurate, color and templates, and tool choice including diagrams as code. Use when a developer asks which diagram to draw, explains a system to a given audience, reviews a diagram, picks a modeling tool, or documents an unfamiliar codebase.
---

# Software Modeling (FSE Chapter 4)

Purpose: help a developer use diagrams as a deliberate communication device rather than as ceremony. A diagram earns its place only when it helps a specific audience understand intent, boundaries, behavior or risk. Code remains the authoritative design; diagrams add context around it, and they are only as valuable as they are accurate. The agent's job is to pick the right model for the moment, pitch its formality at the audience, keep it legible, and keep it from rotting.

## Key decision rules

1. **Code is the source of truth.** Software is cheap to change compared to buildings, so up-front blueprints matter less. Treat diagrams as supplements; when they disagree with code, the code wins.
2. **Stale is worse than missing.** An inaccurate diagram misleads onboarding, debugging and reviews. Either keep it current (ideally generated from code in the pipeline) or label it as a dated sketch and let it expire.
3. **Choose by the situation, not by habit.** Ask: what is the goal, how complex and risky is the problem, is it novel for this team, what is the budget, how business-critical is it. Higher risk and novelty justify more and more formal modeling.
4. **Formality shrinks the audience.** Formal notation (UML, Z) is precise but readable by fewer people. Default to informal box-and-line diagrams that borrow a few UML shapes; go formal only when the whole audience reads that notation.
5. **Match diagram type to question and reader:**
   - Scope and boundaries for leaders and product people: context diagram.
   - Runtime building blocks, interfaces and flows for engineers and ops: component diagram.
   - Type relationships for engineers: class diagram, extracted from code on demand.
   - One significant interaction or pattern, for devs, ops and QA: sequence diagram.
   - Nodes, networks, protocols, versions, scale and uptime: deployment diagram (label it logical or physical).
   - Trust zones, protocols, PII and regulation: security diagram.
   - Entities and relationships, conceptual to logical to physical: data model.
   - Shared understanding of a domain or process: event storming, value stream mapping, user story mapping. Business continuity: disaster recovery model.
6. **Sketch to think.** An hour or two drawing a design can save days of rework. Sketches can be thrown away; redrawing the same sketch again and again signals it deserves a proper tool and a shared home.
7. **One idea per diagram.** Never cram the whole system into one view. Split at logical seams and link diagrams to each other; an overview is fine but should not be the only model. Test: would it be legible printed?
8. **Context limits what reviewers can judge.** A reviewer without domain knowledge can only check the obvious. Supply the narrative and domain context, or pick a reviewer who has it.
9. **Color never carries meaning alone.** Always include a legend, assume grayscale printing and color blind readers, and add a second cue (shape, line style, label).
10. **Standards, but not dogma.** Org templates give consistency; skip any required diagram that adds nothing (for example, use case diagrams on a story-based project) and say why.
11. **The message beats the tool.** Prefer whatever everyone can access; paper and whiteboards are legitimate. Version control every diagram. Review AI-extracted diagrams for hallucinated elements. Avoid model-to-code generation except where a domain truly requires it.

## Default workflow

1. Identify the audience and the one question the diagram must answer.
2. Pick the diagram type and formality from rule 5 and the situation questions in rule 3.
3. Draft quickly (whiteboard, text-based tool, or extraction from code), showing only the elements involved.
4. Add title, scope statement, legend, and a "logical vs physical" or "current vs proposed" label as relevant.
5. Run the review checklist in the practices reference (legibility, color, accuracy, audience fit).
6. Decide its lifespan: throwaway, maintained by hand, or generated in CI. Store and version it accordingly.

## References

- [references/diagram-catalog.md](references/diagram-catalog.md): read when choosing which diagram to create, judging formality for an audience, or explaining why and when modeling pays off; includes a selection matrix and workshop techniques.
- [references/modeling-practices-and-tools.md](references/modeling-practices-and-tools.md): read when drawing, reviewing or cleaning up a diagram, setting team diagram standards, choosing a tool, deciding on diagrams as code, or planning practice exercises.
- [references/source-map.md](references/source-map.md): read to locate which reference covers a given chapter section.

## Scripts

None. The chapter offers qualitative guidance without thresholds or calculations, so no script would add real value.
