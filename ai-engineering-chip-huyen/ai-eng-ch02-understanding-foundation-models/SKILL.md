---
name: ai-eng-ch02-understanding-foundation-models
description: Use when choosing or sizing a foundation model, judging language/domain data coverage, transformer internals and alternatives, scaling laws and compute cost, SFT vs preference finetuning (RLHF, DPO, reward models), sampling (temperature, top-k, top-p), best-of-N, structured outputs, inconsistency or hallucination. Based on Chapter 2 of Chip Huyen's "AI Engineering".
---

# Understanding Foundation Models (AI Engineering, Chip Huyen, Chapter 2)

This skill condenses how model-builder decisions (data, architecture, size, post-training, sampling) show up as behaviors an application engineer must handle. The engineer rarely trains a foundation model; the point is to predict a model's strengths and failure modes from how it was built, and to use the levers that remain under the engineer's control at inference time, above all sampling.

## When to use this skill

- Picking a model for a non-English language, a specialized domain, or a cost-constrained deployment.
- Estimating memory, cost, or latency from parameter counts, token counts, or FLOPs.
- Explaining why a model behaves like a text completer instead of an assistant, or why it refuses too much or too little.
- Tuning temperature, top-k, top-p, max tokens, stop sequences, or seeds.
- Improving quality by generating several candidates and selecting one (best-of-N, voting, verifiers).
- Getting reliable JSON, YAML, SQL, regex, or class labels from a model.
- Diagnosing inconsistent answers or hallucinations and choosing mitigations.

## Core mental models

**A model reflects its data distribution.** Whatever is scarce in the training corpus will be weak in the model. Web crawls (Common Crawl and filtered derivatives such as C4) dominate public training sets because they are available, not because they are good. They contain lots of low-trust content, and many labs no longer disclose their sources. Default assumption: the model is strong on what the web over-represents and weak on what it under-represents.

**Language skew.** English is close to half of Common Crawl; many widely spoken languages (Punjabi, Swahili, Urdu, Telugu, Bengali, and others) have a share far below their share of world population. Practical consequences:
- Lower accuracy on benchmarks and reasoning in under-represented languages (structure and culture also contribute, not just data volume).
- Safety behavior can differ by language (a model may refuse in English and comply in another language).
- Tokenizers are less efficient for some scripts, so the same meaning can cost several times more tokens (up to roughly 10x for languages like Burmese versus English). Cost and latency scale with tokens.
- Translate-to-English pipelines need a model that understands the source language well enough, and translation drops information (for example, relational pronouns that English flattens).

**Domain coverage.** General models handle everyday questions in many fields because those fields appear on the web. Tasks whose data is proprietary, private, or in special formats (protein or genomic sequences, medical imaging, factory plans) are poorly served; domain-specific models (AlphaFold, BioNeMo, Med-PaLM 2 are examples) come from curated data. Specialized models can be trained from scratch or finetuned from a general model. For vision models, infer domain coverage from benchmark results, since domain distribution analyses are rare.

**Quality can beat quantity.** A small model trained on a modest volume of high-quality, task-focused data can outperform much larger models on that task (a 1.3B coding model trained on about 7B curated tokens is the canonical example). Quantity, quality, and diversity all matter.

**Transformer essentials.**
- It replaced RNN seq2seq, which compressed the whole input into one final hidden state and processed tokens strictly in sequence. Attention lets each output step look back at every prior token, and input tokens can be processed in parallel.
- Inference has two phases: prefill (parallel processing of the prompt, producing key and value vectors) and decode (one token at a time, inherently sequential). Many serving optimizations target one phase or the other.
- Attention uses a query (what the current step is looking for), keys (an index for each prior token), and values (the content of each prior token). Scores come from scaled dot products of query and keys, passed through softmax, then used to weight values. Attention is multi-headed: the hidden dimension is split across heads, and head outputs are concatenated and projected.
- Every prior token needs stored key and value vectors, so memory grows with context length. This is a core reason long context is hard and why KV cache management matters.
- A transformer block holds an attention module (query, key, value, output projection matrices) and an MLP/feedforward module (linear layers with simple nonlinearities like ReLU or GELU). Before the blocks sits an embedding module (token and position embeddings; the number of positions naively caps context length, though extension techniques exist). After them sits the output (unembedding) layer that maps to token probabilities.
- Size is driven by hidden dimension, number of blocks (layers), feedforward dimension, and vocabulary size. Longer context raises memory footprint but not parameter count.

**Architectures beyond the transformer.** The transformer has been unusually durable since 2017 and is heavily optimized for current hardware, so a challenger must win at real scale on real hardware. Candidates: RWKV (parallelizable RNN, no hard context limit in theory, but that does not guarantee good long-context quality) and state space models (S4, H3, Mamba with linear scaling in sequence length, and Jamba, a hybrid transformer-Mamba MoE). If the architecture shifts, adaptation techniques may change but the engineering fundamentals will not.

**Three numbers describe scale.** Parameters (capacity to learn), training tokens (how much it learned), and training FLOPs (cost). Newer generations often beat older models several times their size (Llama 3 8B outperforming Llama 2 70B on MMLU). Training tokens equal dataset tokens times epochs. Dataset size is best measured in tokens, not samples, though token counts depend on the tokenizer.

**Sparsity and MoE.** Total parameters can mislead. In a mixture-of-experts model only some experts run per token, so cost and speed track active parameters (Mixtral 8x7B: about 46.7B total, about 12.9B active per token). Memory still has to hold all the weights.

**Compute-optimal scaling (Chinchilla).** For a fixed compute budget, train on roughly 20 tokens per parameter and scale model and data together. This assumes data is cheap relative to compute, and was derived for dense models on mostly human data. Production priorities differ: smaller models that are cheaper to serve can be the better choice even when "undertrained" by Chinchilla standards (inference-aware variants of the law exist). Each extra point of quality costs disproportionately more, yet small loss improvements can be very noticeable downstream.

**Scaling bottlenecks.** Two hard limits: data and electricity. Training sets are growing faster than new human text, web content is increasingly AI-generated, and sites are restricting crawlers (a large share of C4 is now restricted). Proprietary data becomes a competitive moat. Anything published online may end up in training data, which enables deliberate data injection by bad actors, and machine unlearning remains unsolved. Data centers' share of global electricity is projected to rise sharply, constraining growth.

**Pre-training vs post-training.** Pre-training (self-supervised next-token prediction) builds capability and optimizes token-level quality; it yields a completer that may be toxic or wrong. Post-training optimizes whole-response quality for users, uses a tiny fraction of compute (about 2% for InstructGPT), and mostly unlocks abilities that already exist. Two stages:
1. Supervised finetuning (SFT) on demonstration data, (prompt, response) pairs, also called behavior cloning. Demonstrations need skilled labelers and must span the task types you want; they are expensive (minutes to half an hour per pair). Cheaper routes include volunteer crowds (with demographic bias), heuristic mining of dialogue-shaped web text, and synthetic data.
2. Preference finetuning: RLHF (train a reward model, then optimize the policy against it, typically with PPO), DPO (simpler, no separate RL loop), or RLAIF. The goal of encoding "human preference" assumes a universal preference exists; controversial topics guarantee upsetting someone, while over-censoring makes the product dull.

"Instruction finetuning" is ambiguous (SFT only, or SFT plus preference tuning); clarify it when it comes up.

**Reward models.** Direct scores from labelers are noisy (pointwise evaluation). Pairwise comparison is easier and cheaper than writing responses (a few dollars per comparison versus tens of dollars per written response), but still slow, and agreement between labelers is only around 73%. Ranking k responses yields all pairwise comparisons. The reward model is trained to maximize the score gap between winner and loser (a log-sigmoid of the difference). Starting it from a strong base model helps, though weaker judges can still score stronger generators. A reward model alone, without RL, is useful at inference for picking the best of several samples.

**Sampling.** The model outputs logits (one per vocabulary token); softmax turns them into probabilities; a decoding rule picks the token. Greedy decoding suits classification but makes generation bland. Logprobs (log-scale probabilities) avoid underflow and are valuable for classification, evaluation, and debugging, but many providers expose them only partially or not at all.

## Decision frameworks

**Sampling parameters by goal**

| Goal | Settings to start from |
|---|---|
| Deterministic-looking extraction, classification, grading | Temperature 0 (argmax), fixed seed, cache repeated queries |
| Balanced creative writing | Temperature around 0.7, top-p 0.9 to 0.95; tune empirically |
| Brainstorming, diverse candidates for selection | Higher temperature, vary settings across samples |
| Constrained vocabulary per step | Top-k (roughly 50 to 500) to cut softmax cost; top-p adapts the candidate pool to context; min-p sets a floor probability |

Lower temperature sharpens the distribution toward the top logit (more consistent, more boring); higher temperature flattens it (more creative, less coherent). Providers usually cap temperature at 2.

**Choosing a structured output technique** (ordered from light touch to heavy treatment)

| Technique | Use when | Cost and caveats |
|---|---|---|
| Prompting with format instructions | Model already mostly complies | No guarantee; a few percent invalid may be unacceptable |
| Prompting plus an AI validator/corrector | Validity matters, budget allows | At least two calls per output; adds cost and latency |
| Post-processing (defensive parsers, fixers for recurring errors) | Errors are small and repetitive | Cheap and surprisingly effective; fails on badly broken output |
| Test time compute (regenerate until valid) | Validity is checkable and failures are occasional | Multiplies cost |
| Constrained sampling (grammar masks logits; guidance, outlines, instructor, llama.cpp, provider JSON modes) | Need format guarantees for a supported grammar | Needs a grammar per format and logit access; can add latency; JSON mode guarantees syntax, not content |
| Finetuning on format examples, or adding a classifier head | Format must be reliable across many calls, or labels must be from a fixed set | Most general and reliable; classifier head guarantees valid classes |

Consider YAML over JSON when output tokens are costly; it is less verbose.

**Selecting among multiple samples**

| Task shape | Selector |
|---|---|
| Exact answer (math, multiple choice) | Majority vote (self-consistency) |
| Open-ended quality | Reward model or verifier score |
| No scorer available | Highest average logprob (normalize by length so short outputs are not favored) |
| Verifiable output (SQL, code, schema) | Generate until it validates |
| Latency-critical | Run in parallel, return the first valid completion |
| User-facing creative choice | Show several options and let the user pick |

**Model size and family heuristics**

- Within a family, more parameters usually means better quality; across generations, check recent benchmarks before assuming a bigger older model wins.
- For an MoE model, estimate cost and speed from active parameters and memory from total parameters.
- A large model trained on too little data can lose to a smaller, well-trained one.
- Bigger is occasionally worse (inverse scaling): tasks relying on memorization or strong priors, and more alignment training can amplify stated opinions or self-preservation talk. These effects are mostly small-scale.

**Language or domain gaps: build, adapt, or bridge**

- Check whether a language-specific or domain-specific model exists (many exist for Chinese, French, Vietnamese, Arabic, biomedicine).
- If not, finetune a general model on curated in-language or in-domain data.
- Translate-to-English only as a stopgap, after verifying the model reads the source language well and that nothing meaning-bearing is lost.

## Step-by-step playbooks

**Back-of-envelope sizing and cost**
1. Inference memory floor for weights: parameters times bytes per parameter (7B at 16-bit is at least 14 GB; real usage is higher because of KV cache and activations).
2. Training compute: get the FLOPs figure. Divide by (number of GPUs times per-GPU FLOP/s times seconds) and by expected utilization. Around 50% utilization is acceptable; above 70% is excellent.
3. Cost: GPU-hours times hourly rate. Worked logic: a GPT-3-scale run (about 3.14e23 FLOPs) on 256 H100s takes most of a year even at peak, and millions of dollars at realistic utilization.
4. Keep units straight: FLOPs counts operations; FLOP/s is throughput. "FLOPS" is ambiguous; some labs use FLOP/s-days.
5. For token cost in non-English languages, measure actual token counts with the provider's tokenizer on representative text before budgeting.

**Evaluating a model for a non-English or specialized use case**
1. Build a small test set in the target language/domain, mirroring real queries.
2. Compare quality against the same set in English to quantify the gap.
3. Measure tokens per request in each language to project cost and latency.
4. Test safety behavior in the target language separately; do not assume English refusals transfer.
5. Decide among native, finetuned, or translation-bridge options using the framework above.

**Reading a model's alignment from its provenance**
1. Determine which stages it went through: base (pre-trained only), SFT, preference finetuned (RLHF/DPO/RLAIF).
2. A base model completes text: expect continuations, not answers. Use completion-style prompts or pick an instruct/chat variant.
3. A preference-tuned model is more usable but may have shifted refusal patterns and, per InstructGPT, possibly more hallucination than SFT alone, even though people prefer it overall.

**Using test time compute**
1. Confirm a selection mechanism exists (scorer, validator, vote, or user choice).
2. Diversify candidates by varying temperature, top-p, or prompts.
3. Start with small N (2 to 5); cost scales roughly linearly with N, although a shared prompt prefill can be reused.
4. Use beam search when you control decoding and want to prune weak partial candidates early.
5. Monitor for diminishing or negative returns: with very large N, a verifier can be fooled by adversarial candidates (OpenAI saw a peak near 400 samples), while other work reports log-linear gains up to thousands. Production systems do not sample at that scale.
6. Remember that verifiers can be worth a very large effective model-size increase (roughly 30x in OpenAI's math experiments), and test time compute can beat parameter scaling.
7. For brittle models (those that flip on small input changes), retries help a lot, but swapping in a more robust model is the better fix.

**Mitigating inconsistency**
1. Same input, different output: cache answers; pin temperature, top-p, top-k; fix the seed.
2. Accept that hardware differences can still change outputs; with hosted APIs you cannot control this.
3. Slightly different input, very different output: pinning settings will not help; invest in prompt design and memory/context systems, and evaluate robustness with perturbed inputs.

**Mitigating hallucination**
1. Ground the model with provided context (retrieval) rather than relying on parametric knowledge.
2. Ask for concise answers; fewer generated tokens means fewer chances to fabricate.
3. Allow and encourage "I don't know" in the instructions.
4. Ask the model to cite the sources behind each claim, then verify them.
5. Watch for snowballing: an early wrong statement gets treated as fact and then defended. Restart generation or check intermediate claims rather than letting the model continue from an error.
6. Route factual, high-stakes outputs through detection and evaluation (covered in the evaluation chapters).

## Checklists

**Before committing to a model**
- [ ] Training data likely covers my language and domain? Evidence from benchmarks in that slice?
- [ ] Token efficiency measured for my languages?
- [ ] Total vs active parameters understood; memory fits target hardware?
- [ ] Context length sufficient, and quality at long context tested (not just the advertised limit)?
- [ ] Base vs instruct/chat variant chosen deliberately?
- [ ] Logprobs available if I need classification confidence or scoring?
- [ ] Data terms and provenance acceptable for my use (licensing, opt-outs)?

**Before shipping generation settings**
- [ ] Temperature, top-p/top-k chosen per task, not left at defaults by accident.
- [ ] Max tokens high enough to avoid truncating structured output, low enough to bound cost and latency.
- [ ] Stop sequences set and tested so they cannot cut a JSON object short.
- [ ] Seed fixed and responses cached where repeatability matters.
- [ ] Structured output validated by a parser on every call, with a fallback path.

## Pitfalls and anti-patterns

- Assuming parameter count alone predicts quality; ignoring training tokens, data quality, and model generation.
- Treating an MoE's total parameters as its per-token cost, or its active parameters as its memory needs.
- Assuming English benchmark scores transfer to other languages, or that English safety behavior does.
- Budgeting multilingual workloads with English token counts.
- Relying on translate-in, translate-out without checking what the translation loses.
- Expecting a base model to follow instructions.
- Believing temperature 0 plus a seed guarantees identical outputs across infrastructure.
- Trusting JSON mode to produce correct content; it only enforces syntax, and truncation can still break parsing.
- Setting an aggressive max-token limit or stop word on a structured format.
- Scaling up N in best-of-N without a reliable selector, or without accounting for linear cost growth.
- Picking by raw summed logprob, which favors short outputs; use the average.
- Investing heavily in constrained sampling for formats a modestly finetuned model would learn reliably (some argue that effort is better spent on instruction following).
- Letting a model continue reasoning from its own unverified earlier claims (self-delusion).
- Assuming more alignment training is monotonically better or that RLHF reduces hallucination.
- Publishing internal material on the web on the assumption it will not reach future training sets.

## Key terms

- **Common Crawl / C4**: large web crawl and its filtered subset, used by most disclosed foundation models.
- **Low-resource language**: a language with little available training data.
- **Seq2seq**: RNN encoder-decoder architecture preceding the transformer.
- **Attention (Q, K, V)**: mechanism weighting prior tokens' values by query-key similarity.
- **Prefill / decode**: parallel prompt processing vs sequential token generation.
- **KV cache**: stored key and value vectors for prior tokens; grows with context.
- **Transformer block**: attention module plus MLP module; count equals layers.
- **Unembedding layer (model head)**: maps final vectors to token logits.
- **SSM, S4, H3, Mamba, Jamba, RWKV**: alternatives or hybrids targeting efficient long sequences.
- **MoE**: model split into experts, only some active per token.
- **Sparse model**: many zero-valued parameters, cheaper to store and compute.
- **Training tokens**: dataset tokens times epochs.
- **FLOPs vs FLOP/s**: operation count vs hardware throughput.
- **Utilization**: fraction of peak compute actually achieved.
- **Chinchilla scaling law**: compute-optimal ratio of about 20 training tokens per parameter.
- **Scaling extrapolation (hyperparameter transfer)**: predicting large-model hyperparameters from small-model studies; hampered by interacting hyperparameters and emergent abilities.
- **Emergent abilities**: capabilities that appear only at scale.
- **Inverse scaling**: tasks where larger models do worse.
- **Model collapse concern**: degradation from recursively training on AI-generated data.
- **SFT / demonstration data / behavior cloning**: finetuning on (prompt, response) pairs.
- **Preference finetuning (RLHF, DPO, RLAIF)**: aligning outputs to preferences.
- **Reward model / comparison data**: scorer trained on (prompt, winner, loser) triples.
- **PPO**: RL algorithm commonly used in RLHF.
- **Logits, softmax, logprobs**: raw scores, normalized probabilities, log probabilities.
- **Greedy, temperature, top-k, top-p (nucleus), min-p**: decoding controls.
- **Stopping condition**: max tokens or stop tokens ending generation.
- **Test time compute**: spending more inference compute (multiple samples, beam search) for better outputs.
- **Best-of-N, self-consistency, verifier**: sample-and-select strategies.
- **Robustness**: stability of outputs under small input changes.
- **Semantic parsing**: converting language into structured forms such as SQL.
- **Constrained sampling**: masking logits to tokens a grammar allows.
- **Feature-based transfer (classifier head)**: adding a task head to a base model.
- **Inconsistency**: divergent outputs for identical or near-identical inputs.
- **Hallucination**: ungrounded output; explained by self-delusion (snowballing) and by mismatch between labeler and model knowledge during SFT.

## Source map

Chapter 2, "Understanding Foundation Models":
- Training Data
  - Multilingual Models
  - Domain-Specific Models
- Modeling
  - Model Architecture (Transformer architecture; Attention mechanism; Transformer block; Other model architectures)
  - Model Size (Inverse Scaling sidebar; Scaling law: Building compute-optimal models; Scaling extrapolation; Scaling bottlenecks)
- Post-Training
  - Supervised Finetuning
  - Preference Finetuning (Reward model; Finetuning using the reward model)
- Sampling
  - Sampling Fundamentals
  - Sampling Strategies (Temperature; Top-k; Top-p; Stopping condition)
  - Test Time Compute
  - Structured Outputs (Prompting; Post-processing; Constrained sampling; Finetuning)
  - The Probabilistic Nature of AI (Inconsistency; Hallucination)
- Summary
