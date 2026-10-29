---
name: fsa-ch23-diagramming
description: Applies Chapter 23 of Richards and Ford's "Fundamentals of Software Architecture" (2nd ed.) on diagramming architecture. Covers representational consistency across views, the Irrational Artifact Attachment antipattern, low- versus high-fidelity artifacts, tool features and semantic layers, UML, C4 and ArchiMate, and guidelines for titles, lines, shapes, labels, color and keys. Use when drawing, generating (Mermaid, PlantUML, Structurizr) or reviewing an architecture diagram, choosing a notation standard, or planning how to present an architecture to stakeholders.
---

# Diagramming Architecture (FSA Chapter 23)

## Purpose

This skill helps an agent create, critique and present architecture diagrams the way the chapter recommends. Its premise is that diagrams are a core communication tool: an architecture that cannot win funding from managers or buy-in from developers never gets built, and a clear topology picture builds the shared understanding that wins both. The guidance centers on four themes: always establish context before zooming in, match artifact fidelity to design maturity, pick and apply a notation pragmatically, and follow a small set of visual rules that prevent misreading.

## Key decision rules (apply even without opening references)

1. **Representational consistency.** Before switching to a detail view, show where that part sits in the whole system and how it connects. Order: full topology, then the boundary of the region, then its internals.
2. **Fidelity follows maturity.** Use throwaway sketches (cards, whiteboard, tablet) while the design is still changing; invest in polished diagrams only once the team has iterated enough.
3. **Watch for Irrational Artifact Attachment.** Attachment to an artifact grows with the time spent making it. If someone defends a design because the drawing is finished, treat that as a warning sign. Keep objectivity above affection for a diagram.
4. **Learn one tool deeply**, and require layers, stencils/templates, connector magnets, basic drawing primitives and broad export.
5. **Use layers semantically.** Base layer: architectural topology in architectural terms ("synchronous", "asynchronous"), no protocol or product names. Next layer: implementation specifics. Further optional overlays: bounded contexts, transaction scope, ownership, quanta.
6. **Build shared stencils** for patterns common in the organization so diagrams stay consistent and quick to produce.
7. **Notation choice.** UML: keep class and sequence diagrams, skip the rest. C4 (Context, Container, Component, Class): good default if an organization wants one standard. ArchiMate: lightweight enterprise modeling across business domains.
8. **Standards with escape hatches.** Adopt a standard, but allow reasonable exceptions when it cannot express the design; mark deviations in the key.
9. **Titles and labels on everything** unless the item is truly well known to the audience; label strictly wherever ambiguity is possible.
10. **Lines:** visible thickness, arrowheads for direction, consistent arrowhead semantics. Solid means synchronous, dotted means asynchronous (the one widely shared convention).
11. **Shapes:** no universal vocabulary exists, so define one and stay consistent (for example 3D box for deployables, rectangle for containers, cylinder for databases).
12. **Color:** use it to separate or group artifacts, but never as the sole carrier of a critical difference; repeat the meaning with an icon, pattern or shape for colorblind viewers.
13. **Keys:** add one whenever any symbol could be misread. A diagram that invites misreading does more damage than having no diagram.
14. **Prefer lightweight over CASE-style modeling.** Leave out detail that is noise for the question the diagram answers.

## Default workflow

1. Identify the audience and the question the diagram must answer (funding, build guidance, operations handoff, review).
2. Decide fidelity from design maturity (rule 2). If still exploring, sketch two or more alternatives cheaply.
3. Choose notation: the organization's standard if one exists, otherwise C4 for system views or an informal style with a key.
4. Draw the base topology layer in architectural terms. Add implementation and overlay layers (or separate views) only as the audience needs them.
5. Apply the visual rules (9 to 13); run the review checklist in the standards reference.
6. When presenting multiple views, sequence them per rule 1 and keep names and positions stable across views.
7. Before polishing, have the design challenged; resist defending it on the basis of effort spent.

## References

- [references/views-and-representational-consistency.md](references/views-and-representational-consistency.md): read when planning a multi-view explanation, a slide sequence, or a detail diagram that needs context; includes a worked zoom example and pre-presentation checklist.
- [references/tools-fidelity-and-layers.md](references/tools-fidelity-and-layers.md): read when deciding how polished an artifact should be, diagnosing artifact attachment, choosing tool features, structuring layers, or mapping layers and stencils onto diagrams-as-code.
- [references/standards-and-visual-guidelines.md](references/standards-and-visual-guidelines.md): read when choosing between UML, C4 and ArchiMate, setting an organizational standard, or drawing or reviewing a diagram against the titles, lines, shapes, labels, color and keys guidelines (contains the review checklist).
- [references/source-map.md](references/source-map.md): read to trace a chapter section to the reference that covers it.

## Scripts

None. The chapter offers qualitative guidance rather than calculations; use the review checklist in the standards reference instead.
