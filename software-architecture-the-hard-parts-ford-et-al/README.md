# Software Architecture: The Hard Parts (Neal Ford, Mark Richards, Pramod Sadalage, Zhamak Dehghani, O'Reilly) as agent skills

Original syntheses written as Claude Agent Skills, at three granularities. No book text, story dialogue, code, rating tables, figures or appendix lists are reproduced; every skill includes a source map to locate the discussion in the book.

## Whole book

| Skill | Scope |
|---|---|
| [`sahp-complete`](sahp-complete/SKILL.md) | All 15 chapters: core rules, map of the book, migration playbook, symptom-to-fix map, router to 48 references and 13 scripts |

## Themes

| Skill | Chapters | Scope |
|---|---|---|
| [`sahp-theme-tradeoff-analysis-and-coupling`](sahp-theme-tradeoff-analysis-and-coupling/SKILL.md) | 1, 2, 15 | Trade-off method, quanta, static and dynamic coupling |
| [`sahp-theme-modularity-and-decomposition`](sahp-theme-modularity-and-decomposition/SKILL.md) | 3, 4, 5 | Business case, decomposability, decomposition patterns |
| [`sahp-theme-data-decomposition-and-analytics`](sahp-theme-data-decomposition-and-analytics/SKILL.md) | 6, 14 | Splitting operational data, data mesh and data products |
| [`sahp-theme-granularity-and-reuse`](sahp-theme-granularity-and-reuse/SKILL.md) | 7, 8 | Service size drivers, code reuse techniques |
| [`sahp-theme-data-ownership-and-access`](sahp-theme-data-ownership-and-access/SKILL.md) | 9, 10 | Data ownership, eventual consistency, distributed reads |
| [`sahp-theme-workflows-sagas-contracts`](sahp-theme-workflows-sagas-contracts/SKILL.md) | 11, 12, 13 | Orchestration vs choreography, sagas, contracts |

## Chapters

| Skill | Chapter |
|---|---|
| [`sahp-ch01-no-best-practices`](sahp-ch01-no-best-practices/SKILL.md) | No Best Practices: Trade-offs, ADRs and Fitness Functions (SAHP Chapter 1) |
| [`sahp-ch02-discerning-coupling`](sahp-ch02-discerning-coupling/SKILL.md) | Discerning Coupling in Software Architecture |
| [`sahp-ch03-architectural-modularity`](sahp-ch03-architectural-modularity/SKILL.md) | Architectural Modularity (SAHP Chapter 3) |
| [`sahp-ch04-architectural-decomposition`](sahp-ch04-architectural-decomposition/SKILL.md) | Architectural decomposition (SAHP Chapter 4) |
| [`sahp-ch05-component-decomposition-patterns`](sahp-ch05-component-decomposition-patterns/SKILL.md) | SAHP Chapter 5: Component-Based Decomposition Patterns |
| [`sahp-ch06-pulling-apart-operational-data`](sahp-ch06-pulling-apart-operational-data/SKILL.md) | Pulling Apart Operational Data (SAHP Chapter 6) |
| [`sahp-ch07-service-granularity`](sahp-ch07-service-granularity/SKILL.md) | SAHP Chapter 7: Service Granularity |
| [`sahp-ch08-reuse-patterns`](sahp-ch08-reuse-patterns/SKILL.md) | SAHP Ch. 8: Reuse Patterns |
| [`sahp-ch09-data-ownership-and-transactions`](sahp-ch09-data-ownership-and-transactions/SKILL.md) | Data Ownership and Distributed Transactions (SAHP Chapter 9) |
| [`sahp-ch10-distributed-data-access`](sahp-ch10-distributed-data-access/SKILL.md) | Distributed Data Access (SAHP Chapter 10) |
| [`sahp-ch11-distributed-workflows`](sahp-ch11-distributed-workflows/SKILL.md) | Managing Distributed Workflows (SAHP Chapter 11) |
| [`sahp-ch12-transactional-sagas`](sahp-ch12-transactional-sagas/SKILL.md) | SAHP Chapter 12: Transactional Sagas |
| [`sahp-ch13-contracts`](sahp-ch13-contracts/SKILL.md) | Contracts in Distributed Architectures (SAHP Ch. 13) |
| [`sahp-ch14-analytical-data`](sahp-ch14-analytical-data/SKILL.md) | Managing Analytical Data (SAHP Chapter 14) |
| [`sahp-ch15-trade-off-analysis`](sahp-ch15-trade-off-analysis/SKILL.md) | SAHP Chapter 15: Building Custom Trade-Off Analyses |

## Structure

Every skill follows progressive disclosure: a short router `SKILL.md`, topic files in `references/` (each with a contents list) and standard-library `scripts/` (run with `--help`).

Theme and whole-book skills are generated from the chapter skills. After editing a chapter, refresh them with:

```
python3 tools/build_bundles.py
```

Install any skill by copying its folder into `~/.claude/skills/` (Claude Code) or uploading it in Claude. Pick one level (whole book, themes or chapters) to avoid duplicated content.
