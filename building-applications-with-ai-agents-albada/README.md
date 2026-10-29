# Building Applications with AI Agents (Michael Albada, O'Reilly 2025) as agent skills

Original syntheses written as Claude Agent Skills, at three granularities. No book text, code, tables or figures are reproduced; every skill includes a source map of section headings to locate the discussion in the book.

## Whole book

| Skill | Scope |
|---|---|
| [`baa-complete`](baa-complete/SKILL.md) | All 13 chapters: core rules, lifecycle, symptom-to-fix map, router to 58 references and 15 scripts |

## Themes

| Skill | Chapters | Scope |
|---|---|---|
| [`baa-theme-agent-design-foundations`](baa-theme-agent-design-foundations/SKILL.md) | 1, 2, 3 | Whether to build an agent, scoping, components, UX |
| [`baa-theme-tools-orchestration-multiagent`](baa-theme-tools-orchestration-multiagent/SKILL.md) | 4, 5, 8 | Tools, orchestration, multiagent coordination |
| [`baa-theme-memory-and-learning`](baa-theme-memory-and-learning/SKILL.md) | 6, 7 | Memory, knowledge, learning loops, fine-tuning |
| [`baa-theme-evaluation-and-operations`](baa-theme-evaluation-and-operations/SKILL.md) | 9, 10, 11 | Evals, monitoring, drift, rollouts, improvement |
| [`baa-theme-security-and-governance`](baa-theme-security-and-governance/SKILL.md) | 12, 13 | Security, autonomy, governance, compliance |

## Chapters

| Skill | Chapter |
|---|---|
| [`baa-ch01-introduction-to-agents`](baa-ch01-introduction-to-agents/SKILL.md) | Building Applications with AI Agents, Ch. 1: Introduction to Agents |
| [`baa-ch02-designing-agent-systems`](baa-ch02-designing-agent-systems/SKILL.md) | Designing Agent Systems (Albada, Chapter 2) |
| [`baa-ch03-ux-design-for-agentic-systems`](baa-ch03-ux-design-for-agentic-systems/SKILL.md) | UX Design for Agentic Systems (Albada, Ch. 3) |
| [`baa-ch04-tool-use`](baa-ch04-tool-use/SKILL.md) | Tool Use (Albada, Chapter 4) |
| [`baa-ch05-orchestration`](baa-ch05-orchestration/SKILL.md) | Orchestration (Albada, Ch. 5) |
| [`baa-ch06-knowledge-and-memory`](baa-ch06-knowledge-and-memory/SKILL.md) | Knowledge and Memory (Building Applications with AI Agents, Chapter 6) |
| [`baa-ch07-learning-in-agentic-systems`](baa-ch07-learning-in-agentic-systems/SKILL.md) | Learning in Agentic Systems (Albada, Chapter 7) |
| [`baa-ch08-from-one-agent-to-many`](baa-ch08-from-one-agent-to-many/SKILL.md) | From One Agent to Many (Albada, Chapter 8) |
| [`baa-ch09-validation-and-measurement`](baa-ch09-validation-and-measurement/SKILL.md) | Validation and Measurement for Agentic Systems |
| [`baa-ch10-monitoring-in-production`](baa-ch10-monitoring-in-production/SKILL.md) | Monitoring Agents in Production |
| [`baa-ch11-improvement-loops`](baa-ch11-improvement-loops/SKILL.md) | Improvement Loops (Building Applications with AI Agents, Chapter 11) |
| [`baa-ch12-protecting-agentic-systems`](baa-ch12-protecting-agentic-systems/SKILL.md) | Protecting Agentic Systems (Albada, Ch. 12) |
| [`baa-ch13-human-agent-collaboration`](baa-ch13-human-agent-collaboration/SKILL.md) | Human-Agent Collaboration (Albada, Chapter 13) |

## Structure

Every skill follows progressive disclosure: a short router `SKILL.md`, topic files in `references/` (each with a contents list) and standard-library `scripts/` (run with `--help`).

Theme and whole-book skills are generated from the chapter skills. After editing a chapter, refresh them with:

```
python3 tools/build_bundles.py
```

Install any skill by copying its folder into `~/.claude/skills/` (Claude Code) or uploading it in Claude. Install either the whole-book skill, the themes, or the chapters you need; installing all levels at once works but duplicates content.
