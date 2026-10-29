---
name: baa-theme-memory-and-learning
description: Theme skill on how agents remember and improve, from Michael Albada's "Building Applications with AI Agents" (chapters 6 and 7). Use when designing context windows and memory stores, choosing keyword, vector, RAG, experience memory or GraphRAG, building knowledge graphs, weighing long context against retrieval, or adding learning loops (dynamic few-shot, Reflexion, experiential rules, SFT, DPO, RLVR).
---

# Memory, knowledge and learning (Building Applications with AI Agents, ch. 6 and 7)

Memory decides what the agent can draw on; learning decides how it gets better over time. Both follow the same principle: start with the cheapest reversible option and escalate only on observed failure.

## Cross-chapter rules

1. **Separate knowledge from memory.** Knowledge is external, verifiable fact (usually retrieved); memory is the agent's own history and state. Context engineering chooses what of either enters each call.
2. **Budget the context window.** Include what the task needs and nothing more, put the most relevant material near the end, and remember that age-based eviction drops important content. Plan allocations with `scripts/context_budget.py`.
3. **Escalate memory only on failure.** Rolling window plus keyword search, then BM25, semantic vectors, RAG, experience memory, GraphRAG and finally dynamic graphs.
4. **Use GraphRAG for connected questions.** Multi-document reasoning, corpus-level themes and messy narrative data; expect higher cost and a hard path from prototype to production.
5. **Learning is optional and costs upkeep.** Add a loop only when a measurable gain justifies its design, evaluation and monitoring.
6. **Nonparametric first.** Fixed examples, then retrieved successful cases, then Reflexion after failures, then a maintained list of experiential rules. Each needs a quality signal per attempt.
7. **Fine-tune only when performance need, data and operations line up.** Match method to signal: SFT for gold answers, DPO for preferences, RLVR for verifiable rewards. Validate datasets with `scripts/validate_finetune_jsonl.py`; when in doubt, wait.
8. **Combine speeds.** Keep in-context adaptation running and periodically move stable, high-volume patterns into weights.

## Default workflow

1. Map information needs to knowledge vs memory and set the context budget (ch06).
2. Start with the simplest retrieval that passes evals; record failures that justify the next rung (ch06).
3. Add nonparametric learning with an explicit quality signal (ch07).
4. Consider fine-tuning only after prompts, tools and retrieval plateau, with a migration plan (ch07).

<!-- BEGIN GENERATED: run tools/build_bundles.py to refresh -->

## References by chapter

Each link is one level deep; read only the files whose description matches the task.

### CH06: Knowledge and Memory

- [ch06-context-and-keyword-memory.md](references/ch06-context-and-keyword-memory.md): read when separating knowledge from memory, structuring memory as orchestration nodes, sizing or trimming the context window, or setting up BM25 keyword memory.
- [ch06-graphrag-and-knowledge-graphs.md](references/ch06-graphrag-and-knowledge-graphs.md): read when deciding whether GraphRAG is justified, choosing tooling, building or loading a knowledge graph, or writing multihop queries.
- [ch06-long-context-and-dynamic-graphs.md](references/ch06-long-context-and-dynamic-graphs.md): read when weighing long context against retrieval, considering a continuously updated graph, or choosing the overall memory architecture (escalation ladder and worked example).
- [ch06-semantic-memory-and-rag.md](references/ch06-semantic-memory-and-rag.md): read when adding embeddings and a vector store, building a RAG pipeline, designing semantic experience memory, or applying self-notes.

### CH07: Learning in Agentic Systems

- [ch07-fine-tuning-decisions.md](references/ch07-fine-tuning-decisions.md): read when deciding whether to fine-tune, which method to use, or whether a small or large model fits; includes decision walkthroughs.
- [ch07-nonparametric-learning.md](references/ch07-nonparametric-learning.md): read when designing exemplar banks, Reflexion loops or insight lists, or choosing between them; includes a worked example and pitfalls.
- [ch07-sft-dpo-rlvr-playbook.md](references/ch07-sft-dpo-rlvr-playbook.md): read when building tool-calling SFT data, configuring LoRA/SFT or DPO runs, designing RLVR graders, or combining both learning families.

Merged section maps: [source-maps.md](references/source-maps.md).

## Scripts

Python 3 standard library only; run any script with `--help` for its arguments.

| Script | Purpose |
|---|---|
| `scripts/context_budget.py` (ch06) | Plan a per-call context-window budget for an agent with layered memory. |
| `scripts/validate_finetune_jsonl.py` (ch07) | Validate a fine-tuning JSONL file for agent SFT (chat + tool calls) or DPO. |

<!-- END GENERATED -->
