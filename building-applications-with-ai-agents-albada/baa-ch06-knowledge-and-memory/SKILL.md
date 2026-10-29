---
name: baa-ch06-knowledge-and-memory
description: Guides the design of agent knowledge and memory, based on Chapter 6 of Michael Albada's "Building Applications with AI Agents" (O'Reilly, 2025). Covers context-window budgeting, rolling FIFO windows, BM25 keyword memory, vector-store semantic memory, RAG, semantic experience memory, GraphRAG and knowledge-graph construction, long context vs retrieval, dynamic graphs, and self-notes. Use when choosing or debugging an agent's memory or retrieval layer, deciding whether GraphRAG is worth it, planning a context budget, or hardening a knowledge graph.
---

# Knowledge and Memory (Building Applications with AI Agents, Chapter 6)

Purpose: help an engineer pick, build and operate the layers that put the right facts and history into each model call. Knowledge means external, verifiable content (policies, specs, catalogs, logs) usually delivered by RAG; memory means the agent's own trail (past turns, tool outputs, state). Memory is the store; context engineering decides what from the store enters a given call. The chapter orders techniques from cheap to costly, and its central message is to climb that ladder only when the lower rung fails.

## Key decision rules

**Start simple**
- A rolling context window, possibly plus keyword search, is sufficient for many agents. Escalate on observed failure, not by default.
- Budget rule: everything the task needs, nothing extra. Rough conversions: 1 token is about 0.75 words or 4 characters.
- FIFO eviction drops content by age, not importance; long prompts and wordy replies speed it up. Pin goals and constraints outside the rolling region.
- Models can miss details in long prompts: flag the most relevant material and place it near the end, next to the question.
- Persist agent state with checkpoints keyed by session; an orchestration graph invoked without persisted state forgets between calls. Make each memory operation its own node and order reads before, writes after, the model call.

**Keyword vs semantic**
- BM25 over an inverted index is fast and precise for exact terms (names, codes, IDs). Use the same text analysis at index and query time; trim top-K hits before injecting.
- Add embeddings and a vector store (FAISS, Annoy and similar) when paraphrase, synonyms or concept-level matches are missed. Chunk with overlap and attach source metadata to every chunk.

**RAG and experience memory**
- RAG is most valuable for domain or company knowledge and policies the model has never seen. Debug retrieval and generation separately.
- Semantic experience memory fixes blank-slate sessions and long-task drift: embed each input, search past interactions, reserve a fixed slice of the window for top matches, give the remainder to system message, latest input and recent turns, then write the new exchange back.

**GraphRAG**
- Move to GraphRAG when answers must connect facts across documents, summarize themes across a corpus, or the data is large, messy or narrative. It costs more and is harder, yet often wins once vector retrieval plateaus.
- Use global search for corpus-wide themes, local search for entity-specific questions.
- Build in eight steps: collect, preprocess, extract entities, extract relations, design ontology, populate, integrate and validate (entity resolution), maintain. Extract (subject, predicate, object) triples with a foundation model; spot-check them.
- Load idempotently (`MERGE`, staged node then relationship scripts, incremental loads). Bound hop depth in traversals.
- Prototyping a graph is easy; production readiness is a large project.

**Long context vs retrieval**
- 1M-token windows allow retrieval-free designs, but cost, latency and needle-finding reliability suffer. Hybrid (long context plus selective retrieval) is the consensus; prefer retrieval for fact-seeking, enterprise, freshness-critical or precision-ranking needs.

**Dynamic knowledge graphs**
- Worth it for real-time domains (news, monitoring, medicine, finance). Risks: error propagation, compute cost, privacy compliance, overreliance. Counter each with automated validation, scalable distributed infrastructure, encryption plus access control plus anonymization, and human review of consequential decisions.

**Self-notes**
- For long or multi-part inputs, have the model annotate the context before seeing the question, then answer with notes interleaved (Lanchantin et al., 2023).

## Default workflow

1. Classify what the agent needs: external knowledge, conversational continuity, cross-session personalization, relational reasoning.
2. Plan the window with `scripts/context_budget.py`: reply reserve, system prompt, pinned facts, memory slice, recent turns.
3. Ship the rolling window with pinned facts; log what gets evicted.
4. Add BM25, then embeddings, then RAG, then experience memory, each justified by a failure class you observed.
5. Pilot GraphRAG via a CLI on a corpus sample if multi-document or thematic questions fail; harden with ontology, entity resolution and idempotent loads.
6. Reassess long context vs retrieval on cost and accuracy; make the graph dynamic only if freshness demands it, with the four mitigations in place.

## References

- [references/context-and-keyword-memory.md](references/context-and-keyword-memory.md): read when separating knowledge from memory, structuring memory as orchestration nodes, sizing or trimming the context window, or setting up BM25 keyword memory.
- [references/semantic-memory-and-rag.md](references/semantic-memory-and-rag.md): read when adding embeddings and a vector store, building a RAG pipeline, designing semantic experience memory, or applying self-notes.
- [references/graphrag-and-knowledge-graphs.md](references/graphrag-and-knowledge-graphs.md): read when deciding whether GraphRAG is justified, choosing tooling, building or loading a knowledge graph, or writing multihop queries.
- [references/long-context-and-dynamic-graphs.md](references/long-context-and-dynamic-graphs.md): read when weighing long context against retrieval, considering a continuously updated graph, or choosing the overall memory architecture (escalation ladder and worked example).
- [references/source-map.md](references/source-map.md): read to find which file covers a given chapter section.

## Scripts

- `scripts/context_budget.py`: run to compute how a context window splits across reply reserve, system prompt, pinned facts, a reserved memory slice, and FIFO recent turns, and which memory hits and turns get dropped. Sizes take tokens, `w` (words) or `c` (characters).

```
python3 scripts/context_budget.py --context-length 8000 --output-reserve 1000 \
  --system 600 --user 300w --pinned 200 --memory-share 0.25 \
  --memory-hits 700 800 600 --turns 900 1200 1500 4000c 800 [--reclaim] [--json]
```

Memory hits are listed best first; turns oldest first. `--reclaim` gives unused memory reservation to the turn window.
