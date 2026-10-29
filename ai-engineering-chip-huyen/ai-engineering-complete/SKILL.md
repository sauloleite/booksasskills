---
name: ai-engineering-complete
description: Use for any end-to-end question about building LLM / foundation-model applications: scoping a use case, picking a model, evaluation, prompting, RAG, agents, finetuning, dataset work, inference cost and latency, production architecture and user feedback. Whole-book guide to Chip Huyen's "AI Engineering" that routes to ten chapter references for depth.
---

# AI Engineering, complete guide (Chip Huyen, O'Reilly 2025)

This skill condenses the whole book into one operating model for building applications on top of foundation models. It sits on top of ten chapter skills, bundled in `references/`. Use this file for orientation, cross-chapter decisions and the end-to-end lifecycle; open the matching reference when the task needs depth (formulas, full checklists, glossaries, source maps).

## When to use this skill

- Someone is starting or reviewing an LLM product and needs the full lifecycle, not one technique.
- A question cuts across chapters: "should we prompt, add RAG or finetune?", "why is quality dropping in production?", "how do we make this cheaper without breaking it?".
- You need to decide which chapter-level guidance applies before going deep.

## Reference map

| Need | Open |
|---|---|
| Is this a good use case, build vs buy, AI's role, moats, setting expectations, the AI stack | `references/ch01-foundation-model-applications.md` |
| Training data effects, transformer internals, model size and scaling, post-training (SFT, RLHF, DPO), sampling, structured output, hallucination causes | `references/ch02-understanding-foundation-models.md` |
| Perplexity and cross entropy, exact vs subjective evaluation, similarity metrics, embeddings, AI-as-a-judge, comparative ranking (Elo, Bradley-Terry) | `references/ch03-evaluation-methodology.md` |
| Evaluation criteria, factual consistency, instruction following, model selection, API vs self-hosting, benchmarks and contamination, designing an eval pipeline | `references/ch04-evaluating-ai-systems.md` |
| Prompt structure, in-context learning, system vs user prompt, decomposition, chain-of-thought, prompt tooling and versioning, prompt attacks and defenses | `references/ch05-prompt-engineering.md` |
| Retrieval (BM25, embeddings, hybrid, reranking, chunking), RAG evaluation, agents, tools, planning, reflection, agent failure modes, memory | `references/ch06-rag-and-agents.md` |
| When to finetune, memory math, numeric formats and quantization, PEFT and LoRA/QLoRA, multi-LoRA serving, model merging, hyperparameters | `references/ch07-finetuning.md` |
| Data quality, coverage and quantity, acquisition and annotation, synthetic data and its limits, distillation, deduplication, cleaning and formatting | `references/ch08-dataset-engineering.md` |
| Latency and throughput metrics, compute vs bandwidth bound, hardware, compression, speculative decoding, KV cache and attention optimizations, batching, prompt caching, parallelism | `references/ch09-inference-optimization.md` |
| Production architecture (context, guardrails, router, gateway, caches, agent loops), observability, drift, orchestration, user feedback design | `references/ch10-architecture-and-user-feedback.md` |

## The book's core thesis in seven ideas

1. **Scale created a new discipline.** Only a few labs can train frontier models, so most teams consume them as a service. AI engineering is the work of adapting and shipping those models, which means less modeling and much more evaluation, context construction and product work than classic ML engineering.
2. **Evaluation is the bottleneck and the backbone.** Open-ended outputs, black-box models and saturating benchmarks make evaluation hard, so it must be designed first (evaluation-driven development) and reused at every stage: model selection, prompting, RAG, finetuning, deployment and monitoring.
3. **Adapt with the cheapest lever that works.** Prompting changes no weights, RAG adds information, finetuning changes behavior. Climb the ladder only when systematic experiments show the lower rung is exhausted.
4. **Information problems and behavior problems need different fixes.** Missing, private or stale knowledge points to retrieval. Wrong format, style, safety or domain syntax points to finetuning. Many systems need both.
5. **Data is the durable moat.** Models and techniques commoditize quickly; application data, annotation guidelines and a user-feedback flywheel are what newcomers can actually defend.
6. **Production cost is dominated by inference.** Latency (TTFT, TPOT) and cost per request are product requirements, shaped by the prefill/decode split, memory bandwidth, the KV cache, batching and caching.
7. **Grow architecture incrementally and observe everything.** Start with query, model, response. Add context, guardrails, routing, caching and agentic write actions only as needs appear, with metrics, logs and traces from day one.

## End-to-end lifecycle playbook

### Phase 1: Scope (ch01, ch04)
1. Classify the motivation: existential threat, profit or productivity gain, or exploration. Existential use cases justify building in-house; others start from buy options.
2. Define AI's role: critical or complementary, reactive or proactive, static or dynamic. Define the human's role and plan a crawl, walk, run rollout where autonomy grows only with evidence (for example, acceptance rate of suggestions).
3. Tie success to business metrics plus guardrail metrics (satisfaction, safety). Set a usefulness threshold covering quality, latency targets, cost per request and fairness.
4. Check defensibility: is this a feature the next model release or a big platform will absorb? Where will proprietary data come from?
5. Expect the last mile to dominate. A demo reaching most of the target is fast; closing the final gap can take far longer.

### Phase 2: Evaluation design before building (ch03, ch04)
1. List likely failure modes and turn each into a criterion in four buckets: domain capability, generation quality (factual consistency, safety), instruction following, cost and latency. Give each a metric, a hard threshold and a target.
2. Prefer exact evaluation where an objective exists (unit tests, execution accuracy, pass@k, schema validity). Use similarity metrics only with complete, correct references. Use AI judges for subjective criteria, with a fixed model, a versioned prompt, a small labeled scale and examples per score.
3. Never rely on a judge alone: pair with exact checks and human review of samples; watch self, position and verbosity bias and judge drift.
4. Build several sliced eval sets (production-like, known-hard, user-error, out-of-scope). Size them to the gap you need to detect: roughly 10x more samples for a 3x smaller difference. Bootstrap to check stability.
5. Evaluate the evaluator: does the score track real quality, is it reproducible, what does it cost?

### Phase 3: Model selection (ch02, ch04)
1. Filter on hard constraints: license (commercial use, using outputs to train other models), privacy, data lineage, on-device needs, required features (logprobs, finetuning, tool calling).
2. Shortlist with public benchmarks and leaderboards, knowing they filter out bad models rather than find the best one, and may be contaminated.
3. Run your own eval on the shortlist. For prompting work start with the strongest affordable model; for finetuning, start small and scale up.
4. Weigh API vs self-hosting across privacy, performance, functionality, control and cost. API cost per token stays flat while self-hosting gets cheaper with volume, so revisit at each scale step.
5. Account for model properties: training-data coverage of your language and domain (under-represented languages cost more tokens and score lower), total vs active parameters in MoE models, and post-training choices that affect behavior.

### Phase 4: Prompting (ch02, ch05)
1. Treat prompts as experiments: version them, keep the eval set fixed, judge changes on the whole system.
2. Write clear instructions with a fallback for uncertainty, a persona when perspective matters, examples (more valuable in niche domains than general ones), explicit output format, and enough context.
3. Put critical information at the start or end of long prompts; test placement per model. Always inspect the final rendered prompt, because chat-template mismatches fail silently.
4. Decompose complex tasks into chains for debuggability and cheaper per-step models; give the model room to reason (chain-of-thought, self-critique) when quality matters more than latency.
5. Tune sampling deliberately: temperature, top-p, min-p, stop conditions. For structured output, escalate from prompting, to parsing and retries, to constrained decoding, to finetuning.
6. Secure the prompt layer: assume system prompts will leak; defend in layers against extraction, jailbreaks and indirect injection; measure violation rate together with false refusal rate.

### Phase 5: Context construction, RAG and agents (ch06)
1. Start retrieval with BM25 as a baseline; add embeddings for semantic matches; move to hybrid (cheap retriever plus reranker, or parallel retrievers fused with Reciprocal Rank Fusion).
2. Tune the four levers: chunking, reranking, query rewriting, contextual retrieval (metadata, generated chunk context).
3. Evaluate in layers: retrieval (context precision and recall, NDCG, MRR), embeddings, and end-to-end answers.
4. For agents, choose tools deliberately (knowledge, capability extension, write actions), separate planning from execution, validate plans before running them, add reflection, and require human approval for risky write actions. Remember that per-step errors compound across long tasks.
5. Track agent failures by type: invalid tool or parameters, goal failure, false completion claims, tool errors, inefficiency. Design memory in tiers (weights, context window, external store) with an eviction policy.

### Phase 6: Finetuning and data (ch07, ch08)
1. Finetune only after systematic prompting and RAG, and only for behavior gaps or to make a smaller model match a larger one.
2. Estimate memory first: inference needs weights plus roughly 20% overhead; training adds gradients and optimizer state, and activations can exceed weights. Use gradient checkpointing, accumulation, offloading or parallelism to fit.
3. Default to PEFT, usually LoRA (rank 4 to 64, apply across attention and feedforward); use QLoRA when memory is tight; serve variants as multi-LoRA adapters over one base model. Consider model merging to combine skills without retraining.
4. Curate data for quality, coverage and quantity. A small, consistent, well-aligned set often beats a large noisy one. Pilot with 50 to 100 examples and train on subsets to see the scaling curve.
5. Use synthetic data only with verification (execution, judges, back-translation, filters); mix in real data to avoid collapse; check licenses for distillation and track lineage.
6. Process in order: inspect by hand, deduplicate (before splitting), clean and filter (markup, PII, disallowed fields), then format to the exact chat template used at inference.

### Phase 7: Inference optimization (ch09)
1. Measure first: TTFT, TPOT, total latency as percentiles, throughput, cost per request, goodput against an SLO, and MFU/MBU instead of naive GPU utilization.
2. Identify the bottleneck: prefill is compute-bound, decode is memory-bandwidth-bound; the KV cache can outgrow the weights.
3. Apply levers by level. Model level: weight quantization (the most impactful), distillation, speculative decoding, attention and KV cache optimizations. Service level: continuous batching, prefill/decode disaggregation, prompt caching, batch APIs for offline work, replica and tensor parallelism.
4. Re-evaluate quality after any lossy change; even the same open model served by different providers can score differently.

### Phase 8: Production architecture, monitoring and feedback (ch10)
1. Add components in order of need: richer context, input guardrails (PII handling, malicious prompts), output guardrails (retry, parallel calls, block, human fallback), router and gateway (intent routing, fallback, access and cost control), caches (exact caching with exclusions; semantic caching only after measuring hit rate and error risk), then agent loops and write actions.
2. Observe with metrics tied to failure modes and business metrics, logs with IDs, and traces per step; track MTTD, MTTR and change failure rate; read real samples daily.
3. Watch for drift from silent prompt edits, changing user behavior and provider model updates behind unchanged names.
4. Delay orchestration frameworks until they earn their abstraction cost.
5. Design feedback capture: explicit ratings are sparse and biased; implicit signals (early stops, regenerations, edits, corrections, sharing, conversation length) are plentiful but noisy. Turn edits and comparisons into preference data, and guard against feedback loops and sycophancy.

## Cross-chapter decision map

| Symptom | Likely cause | First move | Then |
|---|---|---|---|
| Plausible but wrong facts | Missing context, or post-training mismatch | Ground with retrieval, allow "I don't know", ask for sources (ch02, ch06) | Factual-consistency evals (ch04) |
| Wrong format or style | Weak instructions or behavior gap | Explicit format, examples, constrained decoding (ch02, ch05) | Finetune for format (ch07) |
| Good demo, poor production quality | Eval set does not match traffic | Build production-like and hard slices (ch04) | Feedback-driven data flywheel (ch08, ch10) |
| Retrieval returns near misses | Chunking, lexical gaps, ranking | Hybrid retrieval, reranker, query rewriting (ch06) | Finetune embeddings (ch06) |
| Agent loops or fails silently | Planning errors, weak tools, compounding errors | Plan validation, reflection, tool ablation (ch06) | Stronger model, human approval (ch01, ch06) |
| Too slow | Long outputs, large prefill, no batching | Measure TTFT/TPOT, shorten outputs, prompt caching (ch09) | Quantize, speculative decoding, disaggregate (ch09) |
| Too expensive | Oversized model, repeated context | Route easy queries to smaller models (ch10), cache (ch09, ch10) | Distill or finetune a smaller model (ch07, ch08) |
| Quality shifted with no code change | Drift | Version prompts and pin model versions (ch05, ch10) | Continuous evaluation in production (ch04, ch10) |
| Security incident | Prompt injection, data leakage | Layered defenses, input/output guardrails (ch05, ch10) | Sandboxing and approval for write actions (ch06) |

## The adaptation ladder (summary)

| Rung | Changes | Best for | Cost and risk |
|---|---|---|---|
| Prompting | Nothing in the model | Most tasks; fast iteration | Fragile across models; leaks |
| RAG and tools | Context per query | Knowledge, freshness, private data, actions | Retrieval quality, latency, injection surface |
| PEFT finetuning | Small adapters | Format, style, domain syntax, smaller-model parity | Data, ML skill, maintenance, forgetting |
| Full finetuning | All weights | Large datasets, deep behavior change | Highest memory and data cost |
| Pre-training | Everything | Rarely justified for application teams | Prohibitive for most |

## Universal checklist

- [ ] Success defined in business terms with a usefulness threshold.
- [ ] Failure modes listed and each mapped to an evaluation method.
- [ ] Eval sets sliced, sized for the gap you care about, and versioned.
- [ ] Prompts versioned, separate from code, rendered prompt inspected.
- [ ] Simplest adaptation tried systematically before the next rung.
- [ ] Retrieval evaluated separately from generation.
- [ ] Write actions gated by approval and sandboxing.
- [ ] Data inspected by hand, deduplicated, licensed and formatted to the inference template.
- [ ] Latency measured as percentiles; cost per request known.
- [ ] Guardrails on inputs and outputs, with false refusals tracked.
- [ ] Metrics, logs and traces in place; drift sources monitored.
- [ ] Feedback captured and routed back into data and evals.

## Pitfalls that span the book

- Shipping on vibe checks instead of a reusable evaluation pipeline.
- Trusting public benchmarks or opaque AI judges as proof of fitness for your task.
- Declaring "prompting doesn't work" after unsystematic experiments, then finetuning prematurely.
- Treating long context windows as a replacement for retrieval.
- Optimizing averages instead of latency percentiles, or GPU utilization instead of goodput.
- Adding orchestration frameworks, semantic caches or agents before the need is proven.
- Letting raw user feedback train the system toward sycophancy or filter bubbles.

## Note on provenance

This skill and its references are original syntheses written for agent use. They do not reproduce the book's text, tables or figures. Each reference ends with a source map of the chapter's section headings so readers can find the original discussion in the book.
