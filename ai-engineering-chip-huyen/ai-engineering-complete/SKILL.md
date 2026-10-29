---
name: ai-engineering-complete
description: Whole-book guide to Chip Huyen's "AI Engineering" for building LLM / foundation-model applications end to end. Use when a task spans several stages (scoping, model selection, evaluation, prompting, RAG, agents, finetuning, dataset work, inference cost and latency, production architecture, user feedback) or when it is unclear which technique applies. Routes to per-topic references from all ten chapters and bundles 24 calculation scripts.
---

# AI Engineering, complete (Chip Huyen, O'Reilly 2025)

Operating model for building applications on top of foundation models, condensed from the whole book. This file holds the cross-chapter rules and a router; depth lives in `references/` (one file per topic, prefixed by chapter) and calculations in `scripts/`. Open only what the task needs.

## Core rules (apply without opening references)

1. **Evaluation first.** Define failure modes, criteria, thresholds and eval sets before building; reuse that pipeline at every stage. Never ship on vibe checks or on public leaderboards alone.
2. **Cheapest adequate lever.** Prompting, then RAG and tools, then PEFT finetuning, then full finetuning. Climb only after systematic experiments show the rung below is exhausted.
3. **Diagnose the gap type.** Missing, private or stale information calls for retrieval; wrong format, style, safety or domain syntax calls for finetuning. Many systems need both.
4. **Exact beats subjective.** Use unit tests, execution, schema checks and pass@k wherever an objective exists; AI judges only with a pinned model and prompt, plus human spot checks.
5. **Strongest model for feasibility, smallest model that passes for production.** Revisit API vs self-hosting at each scale step.
6. **Data is the moat.** Invest in annotation guidelines, curation (quality over quantity), verification of synthetic data and a user-feedback flywheel.
7. **Latency and cost are requirements.** Measure TTFT, TPOT, percentiles and cost per request; find whether you are compute- or bandwidth-bound before optimizing.
8. **Grow architecture incrementally.** Query to model to response first; then context, guardrails, router and gateway, caches, agent loops and write actions, with metrics, logs and traces from day one.
9. **Gate side effects.** Write actions need human approval for risky steps, sandboxing and layered prompt-injection defenses; track false refusals alongside violations.
10. **Watch for drift.** Version prompts, pin model versions, and keep evaluating in production.

## Lifecycle at a glance

| Phase | Core question | Read |
|---|---|---|
| 1. Scope | Should we build this, with what role for AI and humans, judged by which business metric? | ch01-*, lifecycle-playbook |
| 2. Evaluation design | What will fail, how will we detect it, how much data do we need? | ch03-*, ch04-* |
| 3. Model selection | Which models pass hard constraints and our own evals; API or self-host? | ch02-*, ch04-model-selection-and-hosting |
| 4. Prompting | Is the prompt clear, versioned, robust and defended? | ch05-* |
| 5. Context, RAG, agents | Does the model get the right information and tools, safely? | ch06-* |
| 6. Finetuning and data | Is there a behavior gap that only weights can fix, and the data to fix it? | ch07-*, ch08-* |
| 7. Inference optimization | Where is the bottleneck, and which lever moves it without hurting quality? | ch09-* |
| 8. Production and feedback | Which components, which signals, which feedback loop? | ch10-* |

For the detailed phase playbooks, a symptom-to-fix map across chapters, the adaptation ladder and a universal checklist, read [references/lifecycle-playbook.md](references/lifecycle-playbook.md).

## Default workflow

1. Place the task in a lifecycle phase (table above). If it spans phases, start with [references/lifecycle-playbook.md](references/lifecycle-playbook.md).
2. Apply the core rules; open only the one or two references listed below whose "read when" matches.
3. When numbers are involved (memory, cost, latency, sample sizes, retrieval or eval metrics), run the matching script instead of estimating by hand.
4. State assumptions and which rule or reference drove each recommendation.

<!-- BEGIN GENERATED: run tools/build_complete.py to refresh -->

## References by chapter

Each link is one level deep; read only the files whose description matches the task.

### CH01: Introduction to Building AI Applications with Foundation Models

- [ch01-ai-engineering-stack.md](references/ch01-ai-engineering-stack.md): read when staffing a team, planning a platform, choosing prompting vs finetuning, explaining AI vs ML vs full-stack engineering, interface options, or why evaluation is harder.
- [ch01-expectations-milestones-maintenance.md](references/ch01-expectations-milestones-maintenance.md): read when writing success metrics, usefulness thresholds, a milestone plan, last-mile estimates, or a maintenance and risk register.
- [ch01-foundation-models-and-adaptation.md](references/ch01-foundation-models-and-adaptation.md): read when explaining tokens, masked vs autoregressive models, self-supervision, model size and data, foundation and multimodal models, the three adaptation levers, or why AI engineering grew so fast.
- [ch01-use-case-evaluation.md](references/ch01-use-case-evaluation.md): read when deciding whether to build, buy vs build, the AI's and humans' roles, Crawl-Walk-Run promotion criteria, or defensibility. Includes a decision record template.
- [ch01-use-case-patterns.md](references/ch01-use-case-patterns.md): read when brainstorming or ranking ideas, applying the exposure lens, or needing evidence for a category (coding, image and video, writing, education, bots, aggregation, data organization, workflow automation).

### CH02: Understanding Foundation Models

- [ch02-inconsistency-and-hallucination.md](references/ch02-inconsistency-and-hallucination.md): read when outputs vary between runs, flip on small input changes, or contain fabricated facts.
- [ch02-model-architecture-and-scale.md](references/ch02-model-architecture-and-scale.md): read for transformer internals, prefill vs decode, SSM/Mamba/RWKV alternatives, parameter and MoE reasoning, FLOPs and cost math, Chinchilla limits, inverse scaling, and scaling bottlenecks.
- [ch02-post-training.md](references/ch02-post-training.md): read when explaining base vs SFT vs preference-tuned behavior, designing demonstration or comparison data, or using a reward model.
- [ch02-sampling-and-test-time-compute.md](references/ch02-sampling-and-test-time-compute.md): read when choosing temperature, top-k, top-p, min-p, stop conditions or logprob use, or designing best-of-N, beam search, voting and verifier selection.
- [ch02-structured-outputs.md](references/ch02-structured-outputs.md): read when outputs must be valid JSON, YAML, SQL, regex or fixed labels, or when JSON mode or constrained decoding is failing.
- [ch02-training-data.md](references/ch02-training-data.md): read when judging whether a model covers a language, domain or data format, or deciding between specialized model, finetune and translation bridge.

### CH03: Evaluation Methodology

- [ch03-ai-as-a-judge.md](references/ch03-ai-as-a-judge.md): read when writing a judge prompt, choosing a scoring format or judge model, diagnosing judge inconsistency, drift or bias, budgeting judge cost and latency, or considering reward, reference-based or preference models.
- [ch03-comparative-evaluation.md](references/ch03-comparative-evaluation.md): read when ranking models from pairwise votes, choosing Elo vs Bradley-Terry vs TrueSkill, judging a public arena, designing an internal leaderboard, or translating win rates into a switch decision.
- [ch03-evaluation-landscape.md](references/ch03-evaluation-landscape.md): read when framing an evaluation plan, explaining why foundation models are hard to evaluate, separating exact from subjective methods, or walking the method selection ladder with a worked plan.
- [ch03-exact-evaluation.md](references/ch03-exact-evaluation.md): read when building functional-correctness tests or pass@k, choosing among exact match, edit distance, n-gram metrics and embedding similarity, auditing references, or selecting an embedding model.
- [ch03-language-modeling-metrics.md](references/ch03-language-modeling-metrics.md): read when computing or interpreting entropy, cross entropy, BPC, BPB or perplexity, comparing models across tokenizers, or using perplexity for contamination, deduplication or anomaly detection.

### CH04: Evaluate AI Systems

- [ch04-evaluation-criteria.md](references/ch04-evaluation-criteria.md): read when defining what to measure, choosing metrics for domain skill, generation quality, instruction following or personas, or setting cost and latency requirements.
- [ch04-evaluation-pipeline.md](references/ch04-evaluation-pipeline.md): read when designing or auditing an evaluation pipeline: component and task evaluation, guidelines and rubrics, business mapping, method mix, annotation, slicing, set size, evaluator validation, iteration.
- [ch04-factual-consistency-and-safety.md](references/ch04-factual-consistency-and-safety.md): read when measuring hallucination or grounding (including RAG answers), building a hallucination test set, or choosing toxicity and bias detectors.
- [ch04-model-selection-and-hosting.md](references/ch04-model-selection-and-hosting.md): read when picking or switching models, reviewing open model licenses, or deciding between a model API and self-hosting.
- [ch04-public-benchmarks-and-contamination.md](references/ch04-public-benchmarks-and-contamination.md): read when interpreting leaderboards, building a custom leaderboard, judging reports that a model got worse, or detecting and handling data contamination.

### CH05: Prompt Engineering

- [ch05-prompt-anatomy-and-context.md](references/ch05-prompt-anatomy-and-context.md): read when choosing zero vs few-shot, splitting system and user prompts, debugging chat templates, or designing long-context and NIAH tests.
- [ch05-prompt-attacks.md](references/ch05-prompt-attacks.md): read when threat-modeling an LLM feature, assessing prompt extraction, jailbreak, indirect injection, training-data extraction or copyright risk.
- [ch05-prompt-defenses.md](references/ch05-prompt-defenses.md): read when choosing and layering defenses, planning red teaming, or setting up violation and false refusal measurement.
- [ch05-prompt-tooling-and-versioning.md](references/ch05-prompt-tooling-and-versioning.md): read when evaluating prompt optimizers or structured-output libraries, budgeting their API calls, or designing prompt storage, metadata and a versioned catalog.
- [ch05-writing-effective-prompts.md](references/ch05-writing-effective-prompts.md): read when drafting or revising a prompt, enforcing output formats, restricting a model to its context, decomposing a task, or adding CoT or self-critique.

### CH06: RAG and Agents

- [ch06-agent-evaluation.md](references/ch06-agent-evaluation.md): read when testing or debugging an agent: failure taxonomy, planning-dataset metrics, tool testing, efficiency baselines, benchmarks.
- [ch06-agents-tools-and-planning.md](references/ch06-agents-tools-and-planning.md): read when designing an agent: tool categories and write-action safety, plan generation and validation, function calling, plan granularity, control flows, ReAct/Reflexion, and tool selection.
- [ch06-memory.md](references/ch06-memory.md): read when designing short-term and long-term memory, context budgets, eviction or summarization, or contradiction handling.
- [ch06-retrieval-foundations.md](references/ch06-retrieval-foundations.md): read when deciding RAG vs long context, choosing term, embedding or hybrid retrieval, picking an ANN index, setting up retrieval evaluation, or applying RRF.
- [ch06-retrieval-optimization-and-multimodal.md](references/ch06-retrieval-optimization-and-multimodal.md): read when tuning chunking, reranking, query rewriting or chunk enrichment, assessing a vector database product, or building RAG over images or SQL tables.

### CH07: Finetuning

- [ch07-deciding-to-finetune.md](references/ch07-deciding-to-finetune.md): read when deciding whether to finetune at all, choosing between finetuning and RAG, or planning the prompt-to-finetune ladder.
- [ch07-finetuning-tactics.md](references/ch07-finetuning-tactics.md): read when picking the base model, development path, framework or API, setting hyperparameters, reading loss curves, or running the pre-launch and pre-ship checklists.
- [ch07-memory-and-precision.md](references/ch07-memory-and-precision.md): read when sizing GPUs, explaining why training needs more memory, choosing FP32/BF16/FP16/INT8/INT4, or deciding between PTQ, QAT and mixed precision.
- [ch07-model-merging.md](references/ch07-model-merging.md): read when combining models or adapters, doing multi-task finetuning, deploying on device, or choosing among linear, SLERP, TIES/DARE, layer stacking and concatenation.
- [ch07-peft-and-lora.md](references/ch07-peft-and-lora.md): read when choosing among full, partial, adapter and soft-prompt methods, configuring LoRA targets, rank and alpha, serving many adapters, or using QLoRA.

### CH08: Dataset Engineering

- [ch08-curation-quality-and-coverage.md](references/ch08-curation-quality-and-coverage.md): read when choosing example formats, preparing CoT, tool-use or multi-turn data, defining quality criteria, or choosing diversity axes and data mix per phase.
- [ch08-data-processing.md](references/ch08-data-processing.md): read when inspecting a raw dataset, defining and running deduplication, cleaning PII and markup, pruning to budget, or formatting for a chat template and matching inference prompts.
- [ch08-data-synthesis-techniques.md](references/ch08-data-synthesis-techniques.md): read when generating or augmenting data (templates, perturbation, counterfactuals, simulation, self-play, paraphrase, translation, reverse instruction, long-context data, code pipelines, AI-judged preference pairs).
- [ch08-quantity-acquisition-and-annotation.md](references/ch08-quantity-acquisition-and-annotation.md): read when sizing a dataset, interpreting a pilot or scaling curve, choosing PEFT vs full finetuning vs from scratch, planning staged finetuning, picking data sources, finding public datasets, or writing annotation guidelines.
- [ch08-verification-limits-and-distillation.md](references/ch08-verification-limits-and-distillation.md): read when filtering synthetic or annotated data, assessing collapse, bias, imitation or lineage risks, or planning distillation or self-training.

### CH09: Inference Optimization

- [ch09-attention-kv-cache-and-kernels.md](references/ch09-attention-kv-cache-and-kernels.md): read when the KV cache limits batch or context, when selecting attention variants (GQA, MQA, local, cross-layer), PagedAttention or KV compression, or when working with kernels and compilers.
- [ch09-bottlenecks-and-hardware.md](references/ch09-bottlenecks-and-hardware.md): read when deciding whether a workload is compute- or bandwidth-bound, comparing or buying accelerators, or reasoning about memory hierarchy, power and TDP.
- [ch09-metrics-and-measurement.md](references/ch09-metrics-and-measurement.md): read when defining SLOs, building dashboards, computing cost per request, goodput, MFU or MBU, or interpreting utilization numbers.
- [ch09-model-compression-and-decoding.md](references/ch09-model-compression-and-decoding.md): read when choosing among quantization, distillation and pruning, or tuning speculative decoding, inference with reference, or parallel decoding (Lookahead, Medusa).
- [ch09-service-level-optimization.md](references/ch09-service-level-optimization.md): read when choosing online, batch or streaming APIs, configuring batching, splitting prefill and decode, setting up prompt caching, or picking a parallelism strategy and GPU placement.

### CH10: AI Engineering Architecture and User Feedback

- [ch10-agents-and-orchestration.md](references/ch10-agents-and-orchestration.md): read when adding agent loops or write actions, choosing or avoiding an orchestration framework, or cutting pipeline latency with parallelism.
- [ch10-context-and-guardrails.md](references/ch10-context-and-guardrails.md): read when deciding on context construction, PII masking, input or output guardrail policies, retries, human handoff, or streaming versus safety.
- [ch10-conversational-feedback-signals.md](references/ch10-conversational-feedback-signals.md): read when extracting explicit or implicit feedback from conversations, building a complaint taxonomy, or interpreting ambiguous user actions.
- [ch10-feedback-design-and-limitations.md](references/ch10-feedback-design-and-limitations.md): read when designing feedback UI and timing, handling consent and visibility, or preparing feedback for training while controlling bias, degenerate loops, and sycophancy.
- [ch10-observability.md](references/ch10-observability.md): read when defining production metrics, logging and tracing, incident debugging, or drift detection.
- [ch10-routing-gateway-and-caching.md](references/ch10-routing-gateway-and-caching.md): read when adding routers, a model gateway, or an exact or semantic cache, or when checking cacheability and cross-user leak risk.

Merged section maps for all chapters: [source-maps.md](references/source-maps.md).

## Scripts

Python 3 standard library only; run any script with `--help` for its arguments and an example.

| Script | Purpose |
|---|---|
| `scripts/usefulness_check.py` (ch01) | Estimate latency and cost per request and check them against usefulness thresholds. |
| `scripts/sampling_demo.py` (ch02) | Show how temperature, top-k, top-p and min-p reshape a next-token distribution. |
| `scripts/scaling_calculator.py` (ch02) | Back-of-envelope scaling calculator for foundation model training and serving. |
| `scripts/lm_metrics.py` (ch03) | Cross entropy, perplexity, bits-per-character and bits-per-byte from token logprobs. |
| `scripts/pass_at_k.py` (ch03) | Unbiased pass@k estimator for functional-correctness evaluation. |
| `scripts/rank_matches.py` (ch03) | Rank models from pairwise matches with Elo and Bradley-Terry, and score each |
| `scripts/eval_sample_size.py` (ch04) | Size an evaluation set and check how stable its score is. |
| `scripts/ngram_contamination.py` (ch04) | Flag benchmark examples whose word n-grams also appear in a training corpus. |
| `scripts/prompt_catalog_lint.py` (ch05) | Lint a JSON prompt catalog for the metadata a production prompt needs. |
| `scripts/safety_metrics.py` (ch05) | Compute violation rate and false refusal rate from labeled red-team results. |
| `scripts/agent_compound_success.py` (ch06) | Estimate how per-step accuracy compounds over a multi-step agent task. |
| `scripts/retrieval_metrics.py` (ch06) | Compute retrieval quality metrics for a RAG retriever. |
| `scripts/rrf_fuse.py` (ch06) | Merge several ranked retrieval lists with Reciprocal Rank Fusion (RRF). |
| `scripts/finetune_memory.py` (ch07) | Back-of-the-envelope GPU memory estimator for serving and finetuning an LLM. |
| `scripts/lora_params.py` (ch07) | Count LoRA trainable parameters for a transformer and size adapter storage. |
| `scripts/annotator_agreement.py` (ch08) | Inter-annotator agreement (Cohen's kappa) between two label files. |
| `scripts/inspect_jsonl.py` (ch08) | Inspection report for a JSONL training dataset (first step of data processing). |
| `scripts/minhash_dedup.py` (ch08) | Near-duplicate detection for a JSONL dataset with MinHash + LSH banding (stdlib only). |
| `scripts/kv_cache_size.py` (ch09) | Estimate KV cache memory for transformer inference, and how many sequences fit. |
| `scripts/latency_report.py` (ch09) | Percentile latency report and goodput against an SLO, from a CSV of request timings. |
| `scripts/mfu_mbu.py` (ch09) | Compute model FLOP/s utilization (MFU) and model bandwidth utilization (MBU). |
| `scripts/request_latency_cost.py` (ch09) | Estimate per-request latency and cost for an LLM call (hosted API or self-hosted). |
| `scripts/cache_savings.py` (ch10) | Estimate whether a system cache (exact or semantic) pays off. |
| `scripts/implicit_feedback.py` (ch10) | Aggregate implicit conversational feedback signals from a JSONL log. |

<!-- END GENERATED -->

## Provenance

Original synthesis for agent use; it does not reproduce the book's text, tables or figures. `references/source-maps.md` maps each chapter section to the file that covers it, so readers can find the original discussion in the book. The chapter-level skills in the sibling `ai-eng-ch*` folders hold the same references and scripts; this folder is regenerated from them.
