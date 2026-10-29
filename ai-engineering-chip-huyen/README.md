# AI Engineering (Chip Huyen, O'Reilly 2025) as agent skills

Original syntheses of each chapter, written as Claude Agent Skills. No book text, tables or figures are reproduced; each skill ends with a source map of section headings to locate the discussion in the book.

| Skill | Chapter |
|---|---|
| [`ai-engineering-complete`](ai-engineering-complete/SKILL.md) | Whole book: lifecycle, cross-chapter decisions, routing to chapter references |
| [`ai-eng-ch01-foundation-model-applications`](ai-eng-ch01-foundation-model-applications/SKILL.md) | 1. Introduction to Building AI Applications with Foundation Models |
| [`ai-eng-ch02-understanding-foundation-models`](ai-eng-ch02-understanding-foundation-models/SKILL.md) | 2. Understanding Foundation Models |
| [`ai-eng-ch03-evaluation-methodology`](ai-eng-ch03-evaluation-methodology/SKILL.md) | 3. Evaluation Methodology |
| [`ai-eng-ch04-evaluating-ai-systems`](ai-eng-ch04-evaluating-ai-systems/SKILL.md) | 4. Evaluate AI Systems |
| [`ai-eng-ch05-prompt-engineering`](ai-eng-ch05-prompt-engineering/SKILL.md) | 5. Prompt Engineering |
| [`ai-eng-ch06-rag-and-agents`](ai-eng-ch06-rag-and-agents/SKILL.md) | 6. RAG and Agents |
| [`ai-eng-ch07-finetuning`](ai-eng-ch07-finetuning/SKILL.md) | 7. Finetuning |
| [`ai-eng-ch08-dataset-engineering`](ai-eng-ch08-dataset-engineering/SKILL.md) | 8. Dataset Engineering |
| [`ai-eng-ch09-inference-optimization`](ai-eng-ch09-inference-optimization/SKILL.md) | 9. Inference Optimization |
| [`ai-eng-ch10-architecture-and-user-feedback`](ai-eng-ch10-architecture-and-user-feedback/SKILL.md) | 10. AI Engineering Architecture and User Feedback |

## Structure

Every skill follows progressive disclosure:

- `SKILL.md`: short router (key decision rules, default workflow, links). Loaded only when the skill triggers.
- `references/*.md`: one file per topic, read only when the task needs it. `references/source-map.md` maps each book section to the file that covers it.
- `scripts/*.py`: standard-library calculators (memory, KV cache, latency and cost, pass@k, retrieval metrics, sample size, dedup, and more). Run with `--help`.

`ai-engineering-complete` bundles all chapter references (prefixed `chNN-`) and scripts, plus a cross-chapter `lifecycle-playbook.md`. After editing any chapter skill, refresh it with:

```
python3 tools/build_complete.py
```

## Install

Copy any skill folder into `~/.claude/skills/` (Claude Code) or upload it as a skill in Claude.
