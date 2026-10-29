---
name: ai-eng-ch07-finetuning
description: Use when deciding whether to finetune, prompt, or add RAG; estimating GPU memory for inference or training; picking precision/quantization; choosing PEFT, LoRA or QLoRA settings; serving many adapters; merging models or doing multi-task finetuning; or setting learning rate, batch size, epochs. Based on Chapter 7 of Chip Huyen's "AI Engineering".
---

# Chapter 7: Finetuning (AI Engineering, Chip Huyen)

## When to use this skill

Apply this skill when an engineer:
- Asks "should we finetune?" or "finetune or RAG?" for an LLM application.
- Needs a back-of-envelope estimate of the GPU memory a model needs to serve or to train.
- Is choosing a numeric format (FP32, FP16, BF16, INT8, INT4) or a quantization approach (PTQ, QAT, mixed precision).
- Is choosing between full, partial, adapter-based or soft-prompt finetuning, or configuring LoRA (target matrices, rank r, alpha) or QLoRA.
- Must serve many customer- or task-specific finetuned variants cheaply.
- Wants to combine models (merging, task arithmetic, frankenmerging, upscaling) or train one model on several tasks.
- Is setting up a finetuning run: base model, method, framework/API, and hyperparameters.

Data acquisition and synthesis for finetuning (instruction data, distillation datasets) belong to Chapter 8; inference optimization and KV cache to Chapter 9; evaluation pipelines to Chapters 3 and 4.

## Core mental models

**Finetuning is transfer learning by weight updates.** Prompting adapts behavior through context; finetuning changes weights. Its value comes from sample efficiency: a strong base model already holds most of what is needed, so a few hundred to a few thousand good examples can achieve what would take millions from scratch. Treat finetuning as unlocking and shaping latent capability, not as installing new knowledge.

**Any training after pre-training is finetuning.** Variants the application developer may use:
- *Continued pre-training* (self-supervised on cheap, raw in-domain text) before spending on labeled data.
- *Supervised finetuning (SFT)* on (input, output) pairs; can be next-token or *infilling* (fill-in-the-middle, useful for editing and code repair, possible even on autoregressive models).
- *Preference finetuning* on (prompt, preferred, rejected) triples via RL or similar.
- *Long-context finetuning*: changes positional handling; harder, and may degrade short-input quality.
Prefer starting from an already post-trained (instruct) model: the closer the starting point to your task, the less adaptation work.

**Form versus facts.** Finetuning mainly fixes behavior (format, style, relevance, safety, rare syntaxes). RAG mainly fixes information gaps (private, missing or stale facts). Finetuning on poor data can make hallucination worse.

**Specialization has a cost.** Gains on the target task can come with regressions on other tasks (sometimes called an alignment tax). Any finetuned model must be re-evaluated on all traffic types it will see.

**Memory is the central bottleneck.** Training needs far more memory than inference because every trainable parameter carries a gradient plus optimizer state, and activations must be kept for the backward pass. Most finetuning innovations (PEFT, quantized training, offloading) exist to shrink this footprint.

**Backpropagation in one paragraph.** Forward pass computes outputs; loss measures error against ground truth; gradients (one per trainable parameter) attribute the error; the optimizer (Adam dominates for transformers) turns gradients into updates. Frozen parameters need no gradients or optimizer state.

**Numeric formats trade range against precision.** Floats split bits between exponent (range) and significand (precision). BF16 and FP16 are both 16 bits, but BF16 keeps FP32's range with less precision, so large values that overflow FP16 survive in BF16. TF32 actually uses 19 bits. Integer formats (INT8, INT4) are increasingly common for serving.

**Intrinsic dimension explains PEFT.** Pre-training compresses what a model needs into a low-dimensional subspace, and larger, better-trained models end up with lower intrinsic dimension. That is why small low-rank updates and small datasets suffice for finetuning, and why full-rank pre-training is still likely needed before low-rank methods work (low-rank pre-training such as ReLoRA and GaLore works only at modest scales so far).

**LoRA mechanics.** For a weight matrix W (n x m), learn two small matrices A (n x r) and B (r x m). The effective weight becomes W plus (alpha / r) times AB. Only A and B train; W stays frozen. Because AB has W's shape, it can be folded into W after training, so unlike classic adapter layers it adds no inference latency when merged.

**Merging versus ensembling.** Ensembling keeps models intact and combines their outputs (better quality, multiplied inference cost). Merging combines parameters into one model (one inference call, often smaller footprint).

## Decision frameworks

### Should we finetune at all?

| Signal | Lean toward finetuning | Lean away |
|---|---|---|
| Prompt work done | Systematic, versioned prompts with representative examples and clear metrics still fall short | Prompt experiments were ad hoc, examples unrepresentative, metrics vague |
| Failure type | Behavioral: wrong format, irrelevant detail level, unsafe output, rare DSL or uncommon SQL dialect | Informational: missing private data, outdated facts |
| Model size goal | Want a small model to match a big one on a narrow task (cost, latency, self-hosting) | One general model must handle diverse prompts |
| Examples needed | More demonstrations than fit in context | A handful of examples works and prompt caching covers cost |
| Bias | Base model shows systematic bias that curated data can counter | n/a |
| Team and ops | ML training skills, hosting capability, budget for monitoring and retraining | No one can debug training, choose LRs, or operate a self-hosted model |
| Model churn | Task is stable and the gain is large | New base models may overtake your finetune before it pays off |

Do not accept "general models are bad at our domain" without testing: strong general models have repeatedly beaten purpose-built domain models (the chapter's BloombergGPT versus GPT-4 case study). Separate "we need to finetune" from "we want to learn finetuning".

### Finetuning versus RAG

- Outputs factually wrong, missing or stale: RAG first.
- Outputs correct but wrong shape, style, detail level, or invalid syntax: finetuning.
- Both problems: start with RAG (no data curation, no model hosting), using simple term-based retrieval such as BM25 before vector search.
- RAG on the base model often beats a finetuned model, and RAG plus a finetuned model helps only some of the time compared with RAG alone. Measure the combination; do not assume additivity.
- Complexity placement: advanced retrieval adds inference-time components; finetuning adds development-time work but leaves the inference pipeline unchanged.

### Multi-task needs

| Situation | Option |
|---|---|
| Finetuning for task X hurt tasks Y and Z | Finetune on a mix covering all tasks |
| One model cannot do all tasks well | Separate models (or adapters) per task, routed |
| Separate models are costly to serve | Merge them, or use multi-LoRA serving |
| Learning tasks one after another | Avoid naive sequential finetuning (catastrophic forgetting); prefer parallel per-task finetunes then merge |
| Joint training on all tasks | Works, but usually needs more data and compute |

### Choosing a finetuning method

- First finetune ever, or limited GPU: LoRA (or QLoRA if memory is tight).
- Only a few hundred examples: PEFT; full finetuning may not beat LoRA here.
- Thousands to millions of examples and a quality ceiling with LoRA: consider full finetuning.
- Many variants on one base (per customer, per feature): adapters, served from one shared base.
- Want more control than prompting but no weight training: soft prompts (prompt tuning, prefix tuning, P-Tuning), which differ mainly in where the trainable tokens are injected.
- Partial finetuning (train only the last layers) is memory-cheap but parameter-inefficient: it needs a large share of parameters to approach full-finetune quality.
- Need longer context: long-context finetuning or LongLoRA; check short-input regressions.
- Multi-task with mixed batches: IA3 is designed for it.

### Choosing precision

- Load a model in the format it was released in. Loading BF16 weights as FP16 visibly degrades quality.
- Serving: PTQ to 16, 8 or 4 bits is standard and cheap; quantize weights before activations (more stable).
- Model degrades after PTQ: QAT (simulates low precision during training; improves low-precision quality but does not speed training).
- Cut training cost: mixed precision via AMP (master weights high precision, gradients and activations lower); keep sensitive parts like embeddings higher precision.
- Pick a format by value range, sensitivity to small errors, and hardware support. Lower precision usually speeds compute and allows bigger batches, but conversions can add overhead, and out-of-range values become infinity or garbage.

### Serving LoRA

| Need | Approach |
|---|---|
| One finetuned model, lowest latency | Merge AB into W before serving |
| Many adapters on one base | Keep W, A, B separate; load adapters per request; accept small latency overhead (optimizable) |

### Choosing a merge approach

| Approach | What it does | Use when | Watch out |
|---|---|---|---|
| Linear combination (average, weighted average, model soups) | Weighted sum of parameters or adapters | Models share a base; combine task vectors | Rescale if magnitudes differ; alignment methods exist but are hard |
| Task arithmetic | Add or subtract task vectors (finetuned minus base) | Add skills, or remove unwanted ones (biases, invasive capabilities) | Verify removals with evals |
| SLERP | Interpolate along the sphere between two vectors with factor t in [0, 1] | Smooth blend of two models | Only two at a time; chain for more |
| Pruning then merging (TIES, DARE) | Zero out small, redundant task-vector deltas before summing | Merging several models; more models means more interference | Pruning improves merge quality, not model size |
| Layer stacking (passthrough, frankenmerging) | Take layers from different models and stack | New architectures, MoE via sparse upcycling, depthwise upscaling | Usually requires further training |
| Concatenation | Join parameters (two LoRAs give rank r1 + r2) | Rarely | No memory saving versus separate models; generally not recommended |

## Step-by-step playbooks

### 1. Adaptation ladder (from prompt to finetune)
0. Define evaluation criteria and build the eval pipeline first; run it at every step.
1. Prompt only, with systematic prompt versioning.
2. Add few-shot examples (typically 1 to 50).
3. If failures are informational, add retrieval, starting with term-based search.
4. Branch on remaining failures: informational leads to better retrieval (embeddings, hybrid); behavioral (irrelevant, malformed, unsafe) leads to finetuning.
5. Try RAG plus finetuning together, and keep it only if evals show a gain.
Paths vary per application; let failure analysis pick the next rung.

### 2. Memory estimate (back of the envelope)
Let N = parameter count, M = bytes per value.
1. Weights: N x M. (Examples: 13B at 2 bytes is 26 GB; 70B at 2 bytes is 140 GB.)
2. Inference total: about N x M x 1.2 (activations plus KV cache assumed about 20 percent; raise for long context or large batch).
3. Training adds, per trainable parameter: 1 gradient plus optimizer state (SGD 0, momentum 1, Adam 2 values). With Adam at 2 bytes: trainable params x 3 x 2 bytes.
4. Example: full finetune of 7B in 16-bit with Adam: 14 GB weights + 42 GB grads/states = 56 GB before activations, beyond consumer GPUs (12 to 24 GB, up to 48 GB high end).
5. Activations during training can exceed weight memory. Mitigate with gradient checkpointing (recompute instead of store; slower).
6. If still too large: fewer trainable params (PEFT), fewer bits (quantization, QLoRA), smaller batch with gradient accumulation, CPU offloading (DeepSpeed-style), or multi-GPU frameworks (DeepSpeed, PyTorch Distributed, ColossalAI).

### 3. Configure LoRA
1. Confirm the framework supports LoRA for your architecture (popular models are covered by PEFT, Axolotl, unsloth, LitGPT; obscure ones may need code changes and architecture knowledge).
2. Choose targets. Under a tight budget, spreading low rank over more matrices beat high rank on one; if limited to two attention matrices, use query and value. Adding feedforward (MLP) matrices often gives the largest gains when memory permits.
3. Choose rank: start in the 4 to 64 range; raising r often does not help and can overfit, though some tasks benefit from very high rank (e.g., 256). Some hosted APIs cap rank (e.g., 32).
4. Choose alpha: alpha:r ratios between 1:8 and 8:1 are common; small r tends to pair with larger alpha. Sweep (r, alpha).
5. Short on memory: quantize the frozen base rather than shrinking the adapter (adapters are megabytes versus gigabytes of base weights). QLoRA stores base weights in 4-bit NF4, dequantizes to BF16 for compute, and pages optimizer state to CPU; it can fit a 65B model on one 48 GB GPU but trains slower due to (de)quantization.
6. Decide serving mode (merged versus separate adapters). Check public adapter hubs before training your own.

### 4. Plan a finetuning project
1. Base model: during feasibility, use the strongest model you can afford; if it fails, weaker ones will too. Reuse what prompt experiments taught you about model behavior.
2. Pick a path:
   - Progression: validate code on the cheapest model; validate data on a mid-size model (loss should fall as data grows); push the best model; then train across sizes to map price versus performance.
   - Distillation: finetune the strongest affordable model on a small set; use it to generate more data; train a cheaper model on that data.
3. Method: LoRA first, full finetuning later if justified by data volume and quality ceiling.
4. Framework: hosted finetuning API for speed (limited base models and knobs) versus open frameworks (LLaMA-Factory, unsloth, PEFT, Axolotl, LitGPT) or the model's own training code for control (you provision compute; adapters fit on mid-tier GPUs).
5. Plan serving and maintenance: who hosts, how monitored, and what improvement threshold triggers switching to a newer base model.

### 5. Tune hyperparameters from loss curves
- Learning rate: search roughly 1e-7 to 1e-3; a common start is the end-of-pretraining LR times 0.1 to 1. Jumpy loss means too high; flat, slow loss means too low; raise it as far as stability allows. Use a schedule (larger early, smaller late).
- Batch size: below about 8 tends to be unstable; larger is faster and steadier but memory-bound. Use gradient accumulation to emulate larger batches.
- Epochs: millions of examples, 1 to 2; thousands, possibly 4 to 10. Train and validation loss both falling: more epochs or data. Train falling, validation rising: overfitting, cut epochs.
- Prompt loss weight: for instruction data, weight response tokens more than prompt tokens; around 10 percent prompt weight is a common default (0 means learn only from responses).

### 6. Multi-task via merging
1. Finetune one adapter or model per task in parallel from the same base.
2. Compute task vectors (finetuned minus base, or the LoRA weights).
3. Prune redundant deltas (TIES or DARE style), especially for three or more models.
4. Sum (linear or SLERP) with tuned weights or interpolation factors.
5. Optionally finetune the merged model briefly. Merging without further training needs no GPU.
6. Evaluate every constituent task on the merged model.

## Checklists

**Before approving a finetuning project**
- [ ] Eval pipeline and metrics exist and were used for prompt experiments.
- [ ] Prompt experiments were systematic (clear instructions, realistic examples, versioning).
- [ ] Failure analysis shows behavioral rather than informational failures.
- [ ] RAG (at least BM25) tried if any failures are factual.
- [ ] Training data source and quality plan exist (see Chapter 8).
- [ ] Someone can debug training (optimizer, LR, over/underfitting).
- [ ] Hosting and inference plan decided (API versus self-host).
- [ ] Budget and policy for monitoring, retraining, and base-model upgrades.
- [ ] Regression suite covers all task types the model will receive.

**Before launching a training run**
- [ ] Memory estimate done (weights, grads, optimizer, activations) and fits hardware.
- [ ] Model loaded in its intended dtype.
- [ ] Code validated on the cheapest model; checkpoint paths exist and are writable.
- [ ] LR, batch size (or accumulation), epochs, prompt loss weight set with rationale.
- [ ] Train and validation loss both tracked.
- [ ] LoRA targets, r, alpha recorded for reproducibility.

**Before shipping**
- [ ] Finetuned model beats the prompt-only and RAG baselines on target metrics.
- [ ] No unacceptable regressions on non-target tasks.
- [ ] Hallucination rate checked (bad data can raise it).
- [ ] Quantized serving version evaluated, not just the training-precision version.
- [ ] Serving mode chosen (merged LoRA versus multi-adapter).

## Pitfalls and anti-patterns

- Finetuning as the first move, or after shallow, unsystematic prompting.
- Using finetuning to inject fresh or private facts that retrieval would serve better.
- Finetuning on one query type and silently degrading others.
- Sequential task-by-task finetuning that triggers catastrophic forgetting.
- Assuming domain-specific models beat strong general models without benchmarking.
- Ignoring the treadmill: a newer base model may outperform your finetune, and switching has costs.
- Loading weights in the wrong dtype (BF16 as FP16) and blaming the model.
- Estimating training memory from inference memory; forgetting gradients, optimizer states and activations.
- Assuming lower precision always lowers latency (conversion overhead can cancel gains).
- Trying to save memory by shrinking LoRA parameters instead of quantizing the base.
- Cranking LoRA rank up by default; it often adds nothing and can overfit.
- Merging many finetunes without pruning redundant deltas (interference).
- Concatenating adapters expecting savings.
- Stacked-layer merges shipped without further training.
- Tiny batches without gradient accumulation, giving unstable updates.
- Reading only training loss; overfitting shows up in validation loss.
- Hosted finetuning APIs when you need knobs or base models they do not expose.

## Key terms

- **Transfer learning**: reusing knowledge from one task to learn another faster. Feature-based transfer (using embeddings in another model) is the alternative to finetuning.
- **Sample efficiency**: quality reached per training example.
- **Continued pre-training**: self-supervised finetuning on raw domain text.
- **Infilling finetuning**: training to fill gaps using both left and right context.
- **Trainable versus frozen parameters**: updated versus fixed during finetuning.
- **Gradient / optimizer state**: per-parameter error signal / extra values the optimizer keeps (Adam keeps two).
- **Gradient checkpointing (activation recomputation)**: trade compute for activation memory.
- **Gradient accumulation**: sum gradients over several batches before updating.
- **FP32 / FP16 / BF16 / TF32 / INT8 / INT4 / FP8 / FP4**: numeric formats; BF16 favors range, FP16 favors precision.
- **Quantization**: converting values to fewer bits (strictly, to integers; loosely, any precision reduction).
- **PTQ / QAT**: quantize after training / simulate low precision during training.
- **Mixed precision, AMP**: different precisions for different values; framework automation of that choice.
- **Full / partial finetuning**: update all / a subset of existing weights.
- **PEFT**: near full-finetune quality with orders of magnitude fewer trainable parameters.
- **Adapter (additive) methods**: add trainable modules (Houlsby adapters, LoRA, BitFit, IA3, LongLoRA).
- **Soft prompts**: trainable continuous token vectors (prompt tuning, prefix tuning, P-Tuning), unlike readable hard prompts.
- **LoRA rank r / alpha**: inner dimension of the low-rank factors / scale of their contribution (alpha / r).
- **QLoRA, NF4, paged optimizers**: 4-bit-base LoRA; normal-distribution-aware 4-bit format; CPU-GPU paging of optimizer state.
- **Multi-LoRA serving**: one shared base with swappable adapters.
- **Model merging / ensembling**: combine parameters / combine outputs.
- **Task vector (delta parameters), task arithmetic**: finetuned minus base; add or subtract to combine or remove skills.
- **SLERP**: spherical interpolation between two vectors.
- **TIES, DARE**: prune-then-merge methods.
- **Frankenmerging (passthrough)**: layer stacking across models.
- **Sparse upcycling**: building an MoE by duplicating layers of a dense model and adding a router.
- **Depthwise scaling**: upscaling depth by duplicating a model and summing some layers (e.g., 32 layers to 48).
- **Federated learning**: devices train copies locally; copies are merged.
- **Catastrophic forgetting**: losing old skills when trained on new ones.
- **Prompt loss weight**: how much prompt tokens count in the loss relative to response tokens.

## Source map

Chapter 7, "Finetuning":
- Finetuning Overview
- When to Finetune
  - Reasons to Finetune
  - Reasons Not to Finetune
  - Finetuning Domain-Specific Tasks (sidebar)
  - Finetuning and RAG
- Memory Bottlenecks
  - Key Takeaways for Understanding Memory Bottlenecks (sidebar)
  - Backpropagation and Trainable Parameters
  - Memory Math (Memory needed for inference; Memory needed for training)
  - Numerical Representations
  - Quantization (Quantization Versus Reduced Precision sidebar; Inference quantization; Training quantization)
- Finetuning Techniques
  - Parameter-Efficient Finetuning (PEFT techniques; LoRA: Why does LoRA work?, LoRA configurations, Serving LoRA adapters, Quantized LoRA)
  - Model Merging and Multi-Task Finetuning (Summing: Linear combination, SLERP, Pruning redundant task-specific parameters; Layer stacking; Concatenation)
  - Finetuning Tactics (Finetuning frameworks and base models: Base models, Finetuning methods, Finetuning frameworks; Finetuning hyperparameters: Learning rate, Batch size, Number of epochs, Prompt loss weight)
- Summary
