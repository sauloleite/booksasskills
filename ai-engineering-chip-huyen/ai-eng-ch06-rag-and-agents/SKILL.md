---
name: ai-eng-ch06-rag-and-agents
description: Guides per-query context construction for LLM apps, based on Chapter 6 of Chip Huyen's "AI Engineering" (O'Reilly, 2025). Covers RAG vs long context, BM25 vs embedding vs hybrid retrieval, ANN indexes, chunking, reranking, query rewriting, contextual retrieval, multimodal and text-to-SQL RAG, agent tools, planning, function calling, reflection, agent failure evaluation, and memory. Use when designing, debugging or evaluating a RAG pipeline, an agent, or an assistant's memory, or when computing retrieval metrics, RRF fusion or multi-step agent success.
---

# RAG and Agents (AI Engineering, Chapter 6)

Purpose: help build and evaluate the context a foundation model gets for each query. Instructions are shared across queries; context is per query, and missing context is a main driver of hallucination. Two patterns supply it: RAG (retrieve from external memory) and agents (act through tools, of which retrieval is one). A memory layer keeps both within the context limit. This file holds the rules to apply by default; the reference files hold the depth.

## Key decision rules

**RAG vs long context**
- Long windows do not retire RAG: data keeps growing past any limit, and models use long context unevenly while paying for every token. Retrieve only the relevant slice.
- Exception: Anthropic says a knowledge base under about 200k tokens (roughly 500 pages) can go directly into a Claude prompt. Otherwise default to RAG.

**Retrieval**
- The retriever is the main quality lever. Every retriever ranks by a relevance score; choose how the score is computed.
- Start with BM25 (or Elasticsearch) as the baseline: fast, cheap, strong out of the box, hard to beat, but few knobs.
- Add embedding retrieval when paraphrased or natural queries matter; it has more headroom via finetuning but blurs exact identifiers (error codes, SKUs) and costs embedding, storage and search. Vector DB spend can reach one fifth to one half of model API spend; re-embedding on data change multiplies it.
- Production default is hybrid: cheap candidate retrieval then a precise reranker, or parallel retrievers merged with Reciprocal Rank Fusion, score = sum of 1/(k + rank), k = 60.
- Index richness trades build time and memory for query accuracy: HNSW (accurate, fast queries, costly build), LSH (cheap build, weaker queries), IVF+PQ (memory-bound scale; about 100 to 10,000 vectors per cluster). Compare on recall, QPS, build time, index size.
- Prefer "term-based vs embedding-based" over "sparse vs dense" (SPLADE is sparse but behaves like dense).

**Retrieval optimization**
- Chunk recursively (section, paragraph, sentence) or by format; add small overlap (about 20 chars per 2,048-char chunk); never exceed the embedder's or generator's limit. Token-based chunking forces reindexing on model swap. Smaller chunks give variety but strand information and double index cost per halving. No universal size: tune.
- Rerank to fit context or save tokens; weight recency for time-sensitive data. For context, inclusion matters more than exact order, but put the strongest evidence at the start or end.
- Rewrite follow-up turns into standalone queries; resolve references by lookup; return "unresolvable" rather than invent an entity.
- Enrich chunks: metadata, extracted identifiers (keeps codes searchable after embedding), questions each chunk answers, and a 50 to 100 token note situating the chunk in its document.
- Tables: text-to-SQL, execute, generate; add a table-selection step if schemas do not fit. Images: metadata retrieval or a joint embedding model such as CLIP.

**Evaluate RAG on three levels**: retrieval (context precision, context recall; NDCG/MAP/MRR when order matters), embeddings (MTEB), and final answers. Recall needs every document labeled per query, so production often reports precision only.

**Agents**
- Agent = environment + action set (tools). Success depends on the tool inventory and the planner.
- Errors compound: 95% per step is about 60% over 10 steps and 0.6% over 100. Use the strongest model you can for planning, shorten plans, and add checks.
- Tool categories: knowledge augmentation (retrievers, SQL, internal APIs, web; vet web sources), capability extension (calculator, code interpreter with sandboxing, modality converters), write actions (state changes; highest value and risk).
- Decouple planning from execution: generate, validate (unknown tools, step cap, AI judge), then execute. Reflect before, during and after; reflection is optional to run but necessary to succeed.
- Classify intent first, with an out-of-scope class. Set an automation level per action; risky writes need human approval.
- Prefer natural-language or hierarchical plans when tools change; a weaker model can translate steps to calls.
- Function-calling APIs may guarantee valid tool names, never correct argument values: log and inspect every call.
- Pick tools by experiment: compare tool sets, ablate, replace tools the model keeps misusing, study call distributions and tool transitions.
- Improve planning in this order: better prompt and examples, better tool descriptions, simpler tools, stronger model, finetuning.

**Agent evaluation**: list failure modes and measure each one's frequency. Planning (invalid tool, invalid params, wrong values, goal or constraint violated, deadline missed, false "done"), tool (wrong output, translation error, missing tool), efficiency (steps, cost, time per action vs a baseline).

**Memory**: weights for what every task needs, long-term store for rarely needed items, context for the immediate task. Reserve a share of context for retrieved memory (e.g. 30%) and move overflow out. FIFO can drop the goal-setting opening; prefer summarization with entity tracking, or reflection-driven insert/merge/replace. Choose a contradiction policy per use case.

## Default workflow

1. Size the knowledge: fits comfortably in context, or needs RAG? Is a tool or action needed beyond retrieval?
2. RAG: chunk, enrich, index BM25 first, add embeddings and fuse or rerank only if measured gains justify cost.
3. Add query rewriting for multi-turn, reranking to fit context, and text-to-SQL or multimodal retrieval as data demands.
4. Evaluate retrieval (run the metrics script), embeddings, and end-to-end answers; track latency and re-embedding cost.
5. Agents: define environment, task constraints and tool inventory with read/write tags and automation levels; add intent routing; plan, validate, execute, reflect.
6. Evaluate agents with a planning dataset and the failure taxonomy; check compounding with the success script.
7. Add memory with a context budget, eviction strategy and contradiction policy.

## References

- [references/retrieval-foundations.md](references/retrieval-foundations.md): read when deciding RAG vs long context, choosing term, embedding or hybrid retrieval, picking an ANN index, setting up retrieval evaluation, or applying RRF.
- [references/retrieval-optimization-and-multimodal.md](references/retrieval-optimization-and-multimodal.md): read when tuning chunking, reranking, query rewriting or chunk enrichment, assessing a vector database product, or building RAG over images or SQL tables.
- [references/agents-tools-and-planning.md](references/agents-tools-and-planning.md): read when designing an agent: tool categories and write-action safety, plan generation and validation, function calling, plan granularity, control flows, ReAct/Reflexion, and tool selection.
- [references/agent-evaluation.md](references/agent-evaluation.md): read when testing or debugging an agent: failure taxonomy, planning-dataset metrics, tool testing, efficiency baselines, benchmarks.
- [references/memory.md](references/memory.md): read when designing short-term and long-term memory, context budgets, eviction or summarization, or contradiction handling.
- [references/source-map.md](references/source-map.md): read to find which file covers a given chapter section.

## Scripts

All are Python 3 standard library, deterministic, with `--help`.

- Run `python3 scripts/retrieval_metrics.py results.json -k 5` to compute precision@k, recall@k, MRR, MAP and NDCG from ranked results and relevance labels (binary list or graded dict). Add `--json` for machine output.
- Run `python3 scripts/rrf_fuse.py lists.json --top 10` to fuse several retrievers' ranked lists with Reciprocal Rank Fusion (`-k` sets the constant, default 60).
- Run `python3 scripts/agent_compound_success.py --p 0.95 --steps 10 100` to compute end-to-end agent success from per-step accuracy; `--mode solve --target 0.9 --steps 20` gives the per-step accuracy required, and `--mode max-steps --p 0.99 --target 0.8` gives the longest viable plan.
