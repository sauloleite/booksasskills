# Fundamentals of Software Architecture, 2nd ed. (Mark Richards and Neal Ford, O'Reilly) as agent skills

Original syntheses written as Claude Agent Skills, at three granularities. No book text, code, tables, rating matrices, figures or discussion questions are reproduced; every skill includes a source map of section headings to locate the discussion in the book.

## Whole book

| Skill | Scope |
|---|---|
| [`fsa-complete`](fsa-complete/SKILL.md) | All 27 chapters: core rules, map of the book, end-to-end workflow, symptom-to-fix map, router to 94 references and 18 scripts |

## Themes

| Skill | Chapters | Scope |
|---|---|---|
| [`fsa-theme-architectural-thinking`](fsa-theme-architectural-thinking/SKILL.md) | 1, 2, 3, 8, 27 | Trade-off thinking, modularity, components, the laws |
| [`fsa-theme-architecture-characteristics`](fsa-theme-architecture-characteristics/SKILL.md) | 4 to 7 | Defining, identifying, measuring, governing and scoping characteristics |
| [`fsa-theme-style-foundations-and-selection`](fsa-theme-style-foundations-and-selection/SKILL.md) | 9, 19, 20 | Style fundamentals, fallacies, choosing a style, cross-style patterns |
| [`fsa-theme-monolithic-styles`](fsa-theme-monolithic-styles/SKILL.md) | 10 to 13 | Layered, modular monolith, pipeline, microkernel |
| [`fsa-theme-distributed-styles`](fsa-theme-distributed-styles/SKILL.md) | 14 to 18 | Service-based, event-driven, space-based, SOA, microservices |
| [`fsa-theme-decisions-risk-diagrams`](fsa-theme-decisions-risk-diagrams/SKILL.md) | 21 to 23 | ADRs, risk assessment and storming, diagramming |
| [`fsa-theme-teams-and-leadership`](fsa-theme-teams-and-leadership/SKILL.md) | 24 to 26 | Team effectiveness, negotiation, leadership, ecosystem alignment |

## Chapters

| Skill | Chapter |
|---|---|
| [`fsa-ch01-introduction`](fsa-ch01-introduction/SKILL.md) | FSA Chapter 1: Introduction to Software Architecture |
| [`fsa-ch02-architectural-thinking`](fsa-ch02-architectural-thinking/SKILL.md) | Architectural Thinking (FSA Chapter 2) |
| [`fsa-ch03-modularity`](fsa-ch03-modularity/SKILL.md) | FSA Ch. 3: Modularity |
| [`fsa-ch04-characteristics-defined`](fsa-ch04-characteristics-defined/SKILL.md) | Architecture Characteristics Defined (FSA Chapter 4) |
| [`fsa-ch05-identifying-characteristics`](fsa-ch05-identifying-characteristics/SKILL.md) | Identifying Architecture Characteristics |
| [`fsa-ch06-measuring-and-governing`](fsa-ch06-measuring-and-governing/SKILL.md) | Measuring and Governing Architecture Characteristics (FSA Chapter 6) |
| [`fsa-ch07-scope-of-characteristics`](fsa-ch07-scope-of-characteristics/SKILL.md) | Scope of Architecture Characteristics (architecture quantum) |
| [`fsa-ch08-component-based-thinking`](fsa-ch08-component-based-thinking/SKILL.md) | Component-Based Thinking (FSA Chapter 8) |
| [`fsa-ch09-style-foundations`](fsa-ch09-style-foundations/SKILL.md) | Architecture Style Foundations (FSA Chapter 9) |
| [`fsa-ch10-layered-style`](fsa-ch10-layered-style/SKILL.md) | Layered Architecture Style (FSA Chapter 10) |
| [`fsa-ch11-modular-monolith`](fsa-ch11-modular-monolith/SKILL.md) | Modular Monolith (FSA Chapter 11) |
| [`fsa-ch12-pipeline-style`](fsa-ch12-pipeline-style/SKILL.md) | Pipeline (Pipes and Filters) Architecture Style |
| [`fsa-ch13-microkernel-style`](fsa-ch13-microkernel-style/SKILL.md) | Microkernel (Plug-in) Architecture Style |
| [`fsa-ch14-service-based-style`](fsa-ch14-service-based-style/SKILL.md) | Service-Based Architecture Style (FSA Chapter 14) |
| [`fsa-ch15-event-driven-style`](fsa-ch15-event-driven-style/SKILL.md) | Event-Driven Architecture Style (FSA Chapter 15) |
| [`fsa-ch16-space-based-style`](fsa-ch16-space-based-style/SKILL.md) | Space-Based Architecture Style (FSA Chapter 16) |
| [`fsa-ch17-orchestration-driven-soa`](fsa-ch17-orchestration-driven-soa/SKILL.md) | Orchestration-Driven SOA (FSA Chapter 17) |
| [`fsa-ch18-microservices`](fsa-ch18-microservices/SKILL.md) | Microservices Architecture (FSA Chapter 18) |
| [`fsa-ch19-choosing-a-style`](fsa-ch19-choosing-a-style/SKILL.md) | Choosing an Architecture Style (FSA Chapter 19) |
| [`fsa-ch20-architectural-patterns`](fsa-ch20-architectural-patterns/SKILL.md) | Architectural Patterns (FSA Chapter 20) |
| [`fsa-ch21-architectural-decisions`](fsa-ch21-architectural-decisions/SKILL.md) | Architectural Decisions (FSA Chapter 21) |
| [`fsa-ch22-analyzing-risk`](fsa-ch22-analyzing-risk/SKILL.md) | Analyzing Architecture Risk (FSA Chapter 22) |
| [`fsa-ch23-diagramming`](fsa-ch23-diagramming/SKILL.md) | Diagramming Architecture (FSA Chapter 23) |
| [`fsa-ch24-making-teams-effective`](fsa-ch24-making-teams-effective/SKILL.md) | Making Teams Effective (FSA Chapter 24) |
| [`fsa-ch25-negotiation-and-leadership`](fsa-ch25-negotiation-and-leadership/SKILL.md) | Negotiation and Leadership Skills (FSA Chapter 25) |
| [`fsa-ch26-architectural-intersections`](fsa-ch26-architectural-intersections/SKILL.md) | Architectural Intersections (FSA Chapter 26) |
| [`fsa-ch27-laws-revisited`](fsa-ch27-laws-revisited/SKILL.md) | The Laws of Software Architecture, Revisited (FSA Chapter 27) |

## Structure

Every skill follows progressive disclosure: a short router `SKILL.md`, topic files in `references/` (each with a contents list) and standard-library `scripts/` (run with `--help`).

Theme and whole-book skills are generated from the chapter skills. After editing a chapter, refresh them with:

```
python3 tools/build_bundles.py
```

Install any skill by copying its folder into `~/.claude/skills/` (Claude Code) or uploading it in Claude. Pick one level (whole book, themes or chapters) to avoid duplicated content.
