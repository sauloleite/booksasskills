---
name: fsa-theme-decisions-risk-diagrams
description: Theme skill on documenting and de-risking architecture, from Richards and Ford's "Fundamentals of Software Architecture" (2nd ed.) (chapters 21, 22 and 23). Use when making and justifying architectural decisions, writing or linting ADRs and routing them for approval, avoiding decision antipatterns, scoring architecture risk (impact x likelihood), running risk storming sessions, planning mitigations, or diagramming architecture with consistent views, layers, notation and keys.
---

# Decisions, risk and diagrams (Fundamentals of Software Architecture, ch. 21 to 23)

Three ways an architecture becomes visible to others: recorded decisions, quantified risk, and clear diagrams.

## Cross-chapter rules

1. **Decide at the last responsible moment,** with business and technical justification, and avoid the cycle of avoiding decisions, re-debating them and losing them in email.
2. **One system of record.** Write ADRs with status, context, a "We will" decision, consequences, compliance and notes; link superseded records both ways; agree in advance what needs approval (`scripts/adr_check.py`).
3. **Use AI to surface trade-offs, not to decide.** Context-free best practices are not architecture decisions.
4. **Score risk consistently.** Impact times likelihood on 1 to 3 scales; unknown likelihood counts as high and unproven technology as maximum risk. Assess characteristics by domain area and show stakeholders the high cells with direction of change (`scripts/risk_storm.py`).
5. **Risk storm collaboratively.** Identify individually first, then discuss disagreements and lone findings, then negotiate mitigation cost with budget holders. Repeat regularly.
6. **Diagram for communication.** Show the whole before zooming in, keep early artifacts cheap, separate topology from implementation using layers, adopt a lightweight standard, title and label everything, and never rely on color alone.

## Default workflow

1. Record each significant decision as an ADR and route it for approval (ch21).
2. Run a risk assessment and risk storming on the top characteristics; plan mitigations (ch22).
3. Communicate the result with consistent, layered diagrams (ch23).

<!-- BEGIN GENERATED: run tools/build_bundles.py to refresh -->

## References by chapter

Each link is one level deep; read only the files whose description matches the task.

### CH21: Architectural Decisions

- [ch21-adr-practice-storage-and-ai.md](references/ch21-adr-practice-storage-and-ai.md): read when deciding where ADRs live, turning standards into ADRs, documenting an existing system, or using generative AI to assist a decision.
- [ch21-adr-structure-and-authoring.md](references/ch21-adr-structure-and-authoring.md): read when writing or reviewing an ADR, setting status and supersession links, defining approval criteria, or designing a compliance check; includes an invented full example and a checklist.
- [ch21-decision-antipatterns-and-significance.md](references/ch21-decision-antipatterns-and-significance.md): read when a team is stalling, re-debating or losing decisions, when choosing a business justification, or when judging whether something is architectural at all.

### CH22: Analyzing Architecture Risk

- [ch22-mitigation-patterns-and-case-study.md](references/ch22-mitigation-patterns-and-case-study.md): read when choosing mitigations for availability, elasticity, security or third-party risk, or when you need a worked end-to-end example.
- [ch22-risk-matrix-and-assessment.md](references/ch22-risk-matrix-and-assessment.md): read when scoring a single risk, building or presenting a criteria-by-context assessment, filtering it for stakeholders, or adding trend direction.
- [ch22-risk-storming-playbook.md](references/ch22-risk-storming-playbook.md): read when planning, facilitating or reviewing a risk-storming session, resolving disagreements, negotiating mitigation cost, setting cadence, or scoring user-story risk in grooming.

### CH23: Diagramming Architecture

- [ch23-standards-and-visual-guidelines.md](references/ch23-standards-and-visual-guidelines.md): read when choosing between UML, C4 and ArchiMate, setting an organizational standard, or drawing or reviewing a diagram against the titles, lines, shapes, labels, color and keys guidelines (contains the review checklist).
- [ch23-tools-fidelity-and-layers.md](references/ch23-tools-fidelity-and-layers.md): read when deciding how polished an artifact should be, diagnosing artifact attachment, choosing tool features, structuring layers, or mapping layers and stencils onto diagrams-as-code.
- [ch23-views-and-representational-consistency.md](references/ch23-views-and-representational-consistency.md): read when planning a multi-view explanation, a slide sequence, or a detail diagram that needs context; includes a worked zoom example and pre-presentation checklist.

Merged section maps: [source-maps.md](references/source-maps.md).

## Scripts

Python 3 standard library only; run any script with `--help` for its arguments.

| Script | Purpose |
|---|---|
| `scripts/adr_check.py` (ch21) | Structural checks for Architectural Decision Records (ADRs) and approval routing. |
| `scripts/risk_storm.py` (ch22) | Risk scoring, risk-storming aggregation and risk-assessment tables (FSA ch. 22). |

<!-- END GENERATED -->
