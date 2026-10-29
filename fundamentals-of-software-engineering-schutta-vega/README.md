# Fundamentals of Software Engineering (Nathaniel Schutta and Dan Vega, O'Reilly 2025) as agent skills

Original syntheses written as Claude Agent Skills, at three granularities. No book text, code, tables or figures are reproduced; every skill includes a source map of section headings to locate the discussion in the book.

## Whole book

| Skill | Scope |
|---|---|
| [`fse-complete`](fse-complete/SKILL.md) | All 15 chapters: core rules, map of the book, task playbooks, symptom-to-fix map, router to 64 references and 10 scripts |

## Themes

| Skill | Chapters | Scope |
|---|---|---|
| [`fse-theme-code-craft`](fse-theme-code-craft/SKILL.md) | 2, 3, 6 | Reading, writing and safely changing code |
| [`fse-theme-testing-and-delivery`](fse-theme-testing-and-delivery/SKILL.md) | 5, 10 | Automated testing, production readiness, pipelines, rollout |
| [`fse-theme-design-and-architecture`](fse-theme-design-and-architecture/SKILL.md) | 4, 7, 8, 9 | Modeling, UI, data, architecture and ADRs |
| [`fse-theme-productivity-learning-ai`](fse-theme-productivity-learning-ai/SKILL.md) | 11, 12, 15 | Tooling, automation, learning, AI-assisted coding |
| [`fse-theme-career-and-collaboration`](fse-theme-career-and-collaboration/SKILL.md) | 1, 13, 14 | Engineering mindset, soft skills, career management |

## Chapters

| Skill | Chapter |
|---|---|
| [`fse-ch01-programmer-to-engineer`](fse-ch01-programmer-to-engineer/SKILL.md) | FSE Ch. 1: From Programmer to Engineer |
| [`fse-ch02-reading-code`](fse-ch02-reading-code/SKILL.md) | Reading Code (FSE Chapter 2) |
| [`fse-ch03-writing-code`](fse-ch03-writing-code/SKILL.md) | Writing Code (FSE Chapter 3) |
| [`fse-ch04-modeling`](fse-ch04-modeling/SKILL.md) | Software Modeling (FSE Chapter 4) |
| [`fse-ch05-automated-testing`](fse-ch05-automated-testing/SKILL.md) | Automated Testing (FSE Chapter 5) |
| [`fse-ch06-exploring-unfamiliar-systems`](fse-ch06-exploring-unfamiliar-systems/SKILL.md) | Exploring and Modifying Unfamiliar Systems |
| [`fse-ch07-user-interface-design`](fse-ch07-user-interface-design/SKILL.md) | User Interface Design (Schutta and Vega, Ch. 7) |
| [`fse-ch08-working-with-data`](fse-ch08-working-with-data/SKILL.md) | Working with Data |
| [`fse-ch09-software-architecture`](fse-ch09-software-architecture/SKILL.md) | FSE Ch. 9: Software Architecture |
| [`fse-ch10-to-production`](fse-ch10-to-production/SKILL.md) | To Production |
| [`fse-ch11-powering-up-productivity`](fse-ch11-powering-up-productivity/SKILL.md) | Powering Up Productivity (FSE Chapter 11) |
| [`fse-ch12-learning-to-learn`](fse-ch12-learning-to-learn/SKILL.md) | Learning to Learn (Fundamentals of Software Engineering, Chapter 12) |
| [`fse-ch13-soft-skills`](fse-ch13-soft-skills/SKILL.md) | Soft Skills for Software Engineers (FSE Chapter 13) |
| [`fse-ch14-career-management`](fse-ch14-career-management/SKILL.md) | Career Management (FSE Chapter 14) |
| [`fse-ch15-ai-powered-software-engineer`](fse-ch15-ai-powered-software-engineer/SKILL.md) | The AI-Powered Software Engineer |

## Structure

Every skill follows progressive disclosure: a short router `SKILL.md`, topic files in `references/` (each with a contents list) and standard-library `scripts/` (run with `--help`).

Theme and whole-book skills are generated from the chapter skills. After editing a chapter, refresh them with:

```
python3 tools/build_bundles.py
```

Install any skill by copying its folder into `~/.claude/skills/` (Claude Code) or uploading it in Claude. Pick one level (whole book, themes or chapters) to avoid duplicated content.
