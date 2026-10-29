---
name: ai-eng-ch06-rag-and-agents
description: Use when designing, debugging or evaluating context construction for LLM apps: RAG vs long context, term vs embedding vs hybrid retrieval, vector indexes, chunking, reranking, query rewriting, contextual retrieval, multimodal/tabular RAG, agent tools, planning, function calling, reflection, agent failure evaluation, and memory management. Based on Chapter 6 of Chip Huyen's "AI Engineering".
---

# Chapter 6: RAG and Agents (AI Engineering, Chip Huyen)

Operational guide for building the per-query context that a foundation model needs, either by retrieving it (RAG) or by letting the model act through tools (agents), plus the memory layer that keeps both within context limits.

## When to use this skill

- Deciding whether a knowledge base needs RAG or can simply be placed in the prompt.
- Choosing between BM25/keyword search, embedding search, or a hybrid, and picking a vector index or vector database.
- Tuning retrieval quality: chunk size and overlap, rerankers, query rewriting, chunk enrichment.
- Answering questions over images, audio or SQL tables rather than plain text.
- Designing an agent: which tools to expose, how to plan, how to validate plans, where to put humans in the loop.
- Diagnosing agent failures (wrong tool, bad arguments, false "done", slowness, cost blowups).
- Designing short-term and long-term memory for chat assistants and long-running agents.

## Core mental models

**Instructions vs context.** Instructions are shared across all queries; context is specific to each query. Missing context is a primary cause of hallucination. Building context is the foundation-model equivalent of feature engineering in classical ML.

**RAG = retriever + generator.** The retriever has two jobs: indexing (preparing data so it can be found fast) and querying (fetching what is relevant). How you index is dictated by how you will query. The retriever's quality largely determines the system's quality. Retriever and generator are usually off-the-shelf and trained separately, although end-to-end finetuning of the whole pipeline can give large gains.

**Long context does not kill RAG.** Two reasons: data grows faster than context windows (applications tend to fill whatever limit they get), and models do not use long context uniformly well; more tokens add cost, latency and the risk of attending to the wrong part. RAG feeds only the most relevant slice. Practical exception: Anthropic has suggested that knowledge bases under roughly 200k tokens can be put directly into a Claude prompt.

**Retrieval is ranking.** Every retriever scores documents for relevance to a query; algorithms differ in how the score is computed. ("Document" and "chunk" are used interchangeably.)

**Term-based (lexical) retrieval.** Scores by term overlap. TF (how often a term appears in a doc) times IDF (log of total docs over docs containing the term, so rare terms weigh more). BM25 refines TF-IDF by normalizing for document length and remains a strong, hard-to-beat baseline. Elasticsearch implements this with an inverted index (term to list of documents plus frequencies). Tokenization choices matter: naive word splitting breaks multiword terms, so common n-grams can be treated as single terms; lowercasing, punctuation removal and stop-word removal are usually handled by the tool. Plain n-gram overlap scoring works only when queries and documents have similar lengths.

**Embedding-based (semantic) retrieval.** Embed chunks at index time into a vector database; at query time embed the query with the same model and fetch the k nearest vectors. It captures meaning (avoids "transformer" returning electrical devices) but can blur exact tokens such as error codes or product names. It is only as good as the embedding model.

**Sparse vs dense is a misleading split.** SPLADE uses sparse embeddings yet behaves like dense retrieval, so "term-based vs embedding-based" is the more useful categorization.

**Vector search = nearest-neighbor search.** Exact k-NN (score everything, sort, return top k) is precise but only viable for small corpora. Large corpora use approximate nearest neighbor (ANN) indexes that organize vectors into buckets, trees or graphs, often with quantization or sparsification:
- LSH: hash similar vectors into the same bucket; cheap to build, slower and less accurate to query.
- HNSW: multi-layer proximity graph traversed at query time; accurate and fast queries, expensive to build and memory hungry.
- Product quantization: split vectors into subvectors and compare compressed codes.
- IVF: k-means clusters (typically sized so each holds about 100 to 10,000 vectors), search only the clusters nearest the query. IVF plus PQ is the core of FAISS.
- Annoy: forest of random-split binary trees.
- Others: ScaNN, SPTAG, FLANN. Any database that stores vectors and searches them counts as a vector database; traditional databases are adding this.

**Index/query trade-off.** A richer index gives more accurate retrieval but takes longer to build and more memory. Benchmark ANN options on recall, queries per second, build time and index size.

**Agent = environment + actions.** An agent perceives and acts on an environment; its tools define its action set. Environment constrains which tools make sense, and the tool inventory constrains which environments the agent can operate in. The model is the planner: it interprets the task and feedback, sequences actions, and decides when the goal is reached. RAG is a special case of an agent whose tools are retrievers and SQL executors.

**Why agents need stronger models.** Errors compound across steps (about 95% per-step accuracy falls to roughly 60% over 10 steps and well under 1% over 100), and tool access raises the stakes of each mistake. The payoff is saved human time.

**Three tool categories.**
1. Knowledge augmentation: retrievers, SQL, internal APIs (people search, inventory, Slack, email), and web access (search, news, GitHub, social APIs), which keeps a model from going stale but exposes it to low-quality or hostile content.
2. Capability extension: calculators, calendars, time zone and unit converters, translators, code interpreters, and modality bridges (text-to-image, captioning, transcription, OCR, LaTeX, chart rendering). Cheaper than training the model to do these things; tool-augmented agents (e.g., Chameleon with 13 tools) beat the bare model on benchmarks like ScienceQA and TabMWP.
3. Write actions: anything that changes state (send email, modify a table, transfer money). Most powerful, most dangerous.

**Planning is search.** A task is a goal plus constraints. Planning means exploring possible action paths, predicting each path's outcome, and choosing the best, including concluding no path exists. Whether autoregressive LLMs can truly plan is debated; they can effectively backtrack by revising or restarting, and they plan better when they can predict the outcome state of actions (world-model framing) or are paired with search and state-tracking tools. FM planners are prompted or finetuned; RL planners are trained with RL, which is costlier; the two approaches may converge.

**Plan, validate, execute, reflect.** Decouple plan generation from execution so bad plans never run. Reflection is optional for operation but close to mandatory for success.

**Memory hierarchy.** Internal knowledge (weights; changes only by retraining), short-term memory (the context window; fast, small, per task), long-term memory (external stores accessed by retrieval; persistent, deletable without touching the model). Place information by frequency of need: always-needed in weights via finetuning, rarely needed in long-term storage, immediately relevant in context.

## Decision frameworks

### RAG or long context?
| Situation | Lean toward |
|---|---|
| Corpus small and stable (well under the model's effective context; ~200k tokens for Claude per Anthropic) | Put it all in the prompt |
| Corpus large, growing, or per-user | RAG |
| Cost or latency per query is tight | RAG (fewer input tokens) |
| Answers depend on a few precise facts buried in large data | RAG plus reranking |

### Term-based vs embedding-based vs hybrid
| Criterion | Term-based (BM25, Elasticsearch) | Embedding-based |
|---|---|---|
| Index and query speed | Much faster | Embedding generation plus ANN search add latency |
| Out-of-box quality | Strong, few knobs | Depends on embedding model |
| Improvement headroom | Limited | High: finetune embedder, retriever, or jointly with generator |
| Exact identifiers, codes, names | Good | Can lose them |
| Natural-language or paraphrased queries | Weak (term ambiguity) | Good |
| Cost | Cheap | Embedding, storage and search can be a large share of spend (one fifth to one half of model API spend is not unusual), worse when data churns and must be re-embedded |

Rule: start with BM25 as the baseline. Add embeddings when semantic matching measurably helps. Production systems usually go hybrid, either:
- **Sequential**: cheap broad retriever fetches candidates, a precise but costly step (exact k-NN, cross-encoder) reranks them. Example: keyword filter on an entity, then semantic search on the remainder of the question.
- **Parallel ensemble**: run several retrievers and merge rankings with Reciprocal Rank Fusion: score(D) = sum over retrievers of 1 / (k + rank_i(D)), with k commonly 60.

Remember generation usually dominates RAG latency, so embedding/search latency may be acceptable, but still measure its UX impact.

### Choosing an ANN index
- Need high recall and fast queries, can afford build time and RAM: HNSW.
- Need fast cheap builds, frequent rebuilds, tolerate lower accuracy: LSH or tree methods.
- Huge corpus, memory bound: IVF with product quantization.
- Rebuilding often because data changes: weight build time heavily.

### Chunking choices
| Lever | Smaller | Larger |
|---|---|---|
| Diversity of info in context | More chunks fit | Fewer chunks fit |
| Risk of losing context spread across a doc | Higher | Lower |
| Index size, embedding cost, search space | Grows (halving size doubles vectors) | Shrinks |

Constraints: chunk must fit both the generator's context and the embedding model's input limit. Token-based chunking aligns with the generator's tokenizer but forces reindexing when you switch models. No universal best size or overlap: tune empirically.

### Tool inventory size
More tools increase capability but make selection harder and inflate the prompt with tool descriptions. Literature ranges from 5 tools (Toolformer) to 13 (Chameleon) to over 1,600 APIs (Gorilla). Decide by experiment, not intuition (see playbook below). Different tasks need different tools, and different models prefer different tools.

### Plan representation
| Plan written as | Pros | Cons |
|---|---|---|
| Exact function names and args | Directly executable | Brittle to tool renames; prompts, examples and finetunes must be redone; hard to reuse across products |
| Natural-language steps | Robust to API changes, closer to model's training distribution, fewer hallucinations | Needs a translator to executable calls (simpler task, a weaker model can do it) |
| Hierarchical (high-level then detailed per stage) | Balances "detailed plans are hard to generate, vague plans are hard to execute" | More components |

### Control flows
Sequential (B depends on A), parallel (independent subtasks, cuts perceived latency), conditional (branch on a prior result), loop (repeat until a condition). Non-sequential flows are harder to generate and translate because the model, not exact code, decides the conditions. When picking a framework, check which flows it supports.

### Level of automation per action
For each tool, decide explicitly: agent may plan it, agent may execute it, or human must approve/execute it. Humans can supply a high-level plan, validate plans, or run risky steps (database updates, merges, payments). Treat an unreliable model like a new intern: no production delete rights.

### Memory placement and eviction
- Reserve a fixed share of context for retrieved long-term memory (e.g., 30%), leaving the rest for short-term; overflow beyond that threshold moves to long-term storage.
- Eviction options, in increasing sophistication: FIFO / keep last N messages or tokens (simple, but can drop the opening messages that define the task); summarization plus named-entity tracking; summary merged with key details the summary missed (classifier picks which sentences from memory and summary to keep); reflection after each step deciding whether new information is inserted, merged, or replaces outdated/contradicting entries. Usage-based eviction (least frequently used) is hard because you must know what the model actually used.
- Contradictions: keep newest, ask a model to adjudicate, or keep both for multiple perspectives; choose per use case.

## Step-by-step playbooks

### Build a text RAG pipeline
1. Inventory sources (internal docs, chat history, web) and estimate size and change rate.
2. Chunk: start recursive (section, then paragraph, then sentence) or format-aware (code splitters, one chunk per Q&A pair, language-specific splitting). Add small overlap at boundaries (e.g., about 20 characters on a 2,048-character chunk) so split facts survive.
3. Enrich chunks (contextual retrieval): attach title, summary, tags, extracted entities and exact identifiers, and the questions each chunk answers. Optionally have a model write a short (about 50 to 100 token) note situating each chunk within its source document and prepend it before indexing.
4. Index with BM25 first; add an embedding index if semantic queries matter; combine via sequential reranking or RRF.
5. At query time, rewrite the query into a standalone form using conversation history; resolve references (who "his wife" is) via lookups, and have the rewriter declare the query unanswerable rather than invent entities.
6. Retrieve k candidates (k depends on use case, model, query), rerank (by a stronger model, or by recency for news, email, markets), then trim to fit context. Put the most important material at the start or end of the context, though inclusion matters more than exact order.
7. Assemble the final prompt with light post-processing and generate.
8. Evaluate (next playbook) and iterate on chunking, enrichment and retriever choice.

### Evaluate a RAG system
1. Build an eval set of queries with documents labeled relevant or not (humans or AI judges).
2. Measure context precision (share of retrieved docs that are relevant) and context recall (share of relevant docs that were retrieved). Recall needs every document labeled per query, so many production tools only report precision.
3. If order matters, add ranking metrics: NDCG, MAP, MRR.
4. For semantic retrieval, evaluate embeddings separately (similar docs should be closer; task benchmarks like MTEB). Use BEIR for retrieval benchmarking and ANN-Benchmarks for index trade-offs.
5. Evaluate end-to-end answer quality; a retriever is good only if final answers are good.
6. Track latency and cost at query time and the cost of re-embedding as data changes.

### RAG over non-text data
- **Images/other media**: retrieve by metadata (captions, titles, tags), or by content using a joint text-image embedding model such as CLIP: embed all texts and images into one vector store, embed the query, return nearest items of any modality.
- **Tables**: text-to-SQL from the query plus schemas, execute the SQL, generate the answer from results. If schemas do not all fit in context, add a step that predicts which tables are relevant. Text-to-SQL can be the main generator or a specialized model.

### Design an agent
1. Define the environment and the task (goal plus constraints, including deadlines).
2. Choose tools across the three categories; mark each as read-only or write; set its automation level.
3. Write tool documentation carefully: entry point name, parameters, what it does. Prefer small simple functions; split complex ones.
4. Add an intent classifier up front to route queries (billing vs password reset) and reject out-of-scope requests instead of burning compute on impossible plans.
5. Generate a plan (whole task or just the next subtask). Optionally generate several in parallel and let an evaluator choose (costs more, saves latency).
6. Validate before executing: heuristics (no unknown tools, max step count) and/or an AI judge. Regenerate if invalid.
7. Execute via function calling. Per query, restrict the allowed tool subset and set tool mode (required, none, auto). APIs may guarantee valid function names but not correct argument values, so log and inspect every call's arguments.
8. Reflect after each step and at the end: is the request feasible, is the plan sensible, is the step on track, is the goal truly met? Use ReAct-style interleaving (thought, action, observation, repeat until finish) or Reflexion-style separation (evaluator scores outcome, self-reflection explains failure, then a new trajectory). Reflection can be self-critique or a separate scorer/agent.
9. Add memory for overflow, persistence and structured state (spreadsheets for leads, queues for pending actions).

### Improve planning quality
In roughly increasing cost: better system prompt with more examples; clearer tool and parameter descriptions; simpler or split tools; a stronger model; finetuning a planner. Use natural-language or hierarchical plans if tools change often.

### Curate the tool inventory
1. Compare agent performance across different tool sets.
2. Ablate: remove a tool; if performance holds, drop it.
3. Find tools the agent keeps misusing; if prompting and finetuning do not fix it, redesign or swap the tool.
4. Plot tool-call frequency distributions per model and task.
5. Study tool transitions (after X, how often Y); frequently chained tools are candidates to merge into one composite tool. Agents can also keep a skill library of self-written, proven programs for reuse (Voyager-style).
6. Re-check how easily the framework accepts new tools; needs will change.

### Evaluate an agent
1. List failure modes and measure the frequency of each.
2. Build a planning dataset of (task, tool inventory) pairs; sample K plans per task.
3. Report: share of valid plans; average plans needed to get a valid one; share of valid tool calls; rates of invalid tools, invalid parameters, and wrong parameter values.
4. Check goal failures: plan does not solve the task or violates constraints (wrong destination, over budget, too late to matter).
5. Check reflection failures: agent claims success on incomplete work (e.g., places 40 of 50 people and declares done).
6. Test each tool independently; print every call and output; benchmark any plan-to-command translator.
7. Detect missing tools by examining domains with high failure rates and asking domain experts which tools they would use.
8. Measure efficiency: steps per task, cost per task, time per action, outlier slow or expensive actions. Compare with a baseline (another agent or a human), remembering that efficient-for-human and efficient-for-AI differ (an agent can fetch 100 pages in parallel).
9. Use public harnesses where relevant: Berkeley Function Calling Leaderboard, AgentOps, TravelPlanner.

## Checklists

**Retrieval solution evaluation**
- [ ] Supported retrieval types; hybrid search available?
- [ ] Supported embedding models and ANN algorithms
- [ ] Scales for your data volume and traffic pattern
- [ ] Indexing time; bulk add/delete limits
- [ ] Query latency per retrieval mode
- [ ] Pricing basis (stored vectors/documents vs query volume)
- [ ] Enterprise needs: access control, compliance, data/control plane separation

**RAG readiness**
- [ ] BM25 baseline measured; chunk size within embedder and generator limits
- [ ] Exact identifiers preserved; multi-turn queries rewritten
- [ ] Retrieval metrics and end-to-end quality tracked; re-embedding cost estimated

**Agent safety and readiness**
- [ ] Each tool tagged read or write, with automation level and approval rules
- [ ] Code execution sandboxed against injection; web sources chosen with care
- [ ] Plans validated before execution; step cap set
- [ ] Out-of-scope intent class exists
- [ ] Every tool call's arguments and output logged
- [ ] Time constraints included in success criteria
- [ ] Budget alerts for runaway loops

## Pitfalls and anti-patterns

- Assuming a bigger context window makes retrieval unnecessary, or that stuffing everything in improves answers.
- Skipping a BM25 baseline; semantic search often struggles to beat it convincingly.
- Pure embedding search on data full of codes, SKUs or names.
- Chunks with no overlap that split key facts, or chunks so small that a topic's later sections are never retrieved.
- Chunking by one model's tokenizer and forgetting it forces a reindex on model swap.
- Retrieving with the raw follow-up query ("How about Emily?") instead of a rewritten standalone query; rewriters that hallucinate identities.
- Underestimating vector DB and re-embedding costs.
- Letting a model plan and execute in one pass with no validation, so a long useless plan burns hours of API spend.
- Overloading the agent with tools "just in case"; keeping tools the model consistently misuses.
- Hard-coding exact function names in plans and few-shot examples when the API surface is still changing.
- Trusting function-calling APIs to produce correct argument values.
- Giving write access (payments, deletes, merges) without human approval or strong security.
- Believing an agent's own declaration that it finished.
- Heavy few-shot ReAct/Reflexion prompts that eat context and inflate latency without measuring the gain.
- FIFO truncation that discards the opening message containing the user's goal.

## Key terms

- **Indexing / querying**: preparing data for retrieval / fetching relevant data.
- **TF-IDF, BM25**: term-frequency relevance scoring; BM25 adds length normalization.
- **Inverted index**: term to documents map.
- **k-NN / ANN**: exact / approximate nearest-neighbor search (LSH, HNSW, PQ, IVF, Annoy).
- **Hybrid search, reranking, RRF**: combining retrievers, re-scoring candidates, fusing rankings by summed 1/(k + rank).
- **Context precision / recall**: relevance share of retrieved / coverage of relevant; NDCG, MAP, MRR add rank awareness.
- **Query rewriting / contextual retrieval**: self-contained queries / enriched chunks.
- **Text-to-SQL**: semantic parsing of a question into executable SQL.
- **Tool inventory; read vs write actions**: available actions; perceiving vs changing the environment.
- **Function calling**: model emits tool name plus arguments for the app to run.
- **Control flow**: sequential, parallel, conditional, loop.
- **ReAct / Reflexion**: interleaved thought-action-observation / evaluator plus self-reflection driving retries.
- **Tool transition / skill library**: tool Y-after-X statistics / stored reusable agent-made tools.
- **Internal, short-term, long-term memory**: weights, context, external store.

## Source map

Chapter 6, "RAG and Agents":
- RAG
  - RAG Architecture
  - Retrieval Algorithms (sidebar: Sparse Versus Dense Retrieval; Term-based retrieval; Embedding-based retrieval; Comparing retrieval algorithms; Combining retrieval algorithms)
  - Retrieval Optimization (Chunking strategy; Reranking; Query rewriting; Contextual retrieval; sidebar: Evaluating Retrieval Solutions)
  - RAG Beyond Texts (Multimodal RAG; RAG with tabular data)
- Agents
  - Agent Overview
  - Tools (Knowledge augmentation; Capability extension; Write actions)
  - Planning (Planning overview; Foundation models as planners; sidebar: FM Versus RL Planners; Plan generation; Function calling; Planning granularity; Complex plans; Reflection and error correction; Tool selection)
  - Agent Failure Modes and Evaluation (Planning failures; Tool failures; Efficiency)
- Memory
- Summary
