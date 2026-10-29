# Model Compression and Faster Decoding

## Contents
- Why model-level changes need care
- Compression: quantization, distillation, pruning
- Choosing a compression approach
- The autoregressive decoding bottleneck
- Speculative decoding
- Inference with reference
- Parallel decoding
- Choosing a decoding accelerator
- Worked examples
- Pitfalls

## Why model-level changes need care

Model-level techniques change the model or how it emits tokens, so they can change outputs. The same open model served by different providers has scored differently on benchmarks (Cerebras published such a comparison), plausibly due to lossy shortcuts. Treat each model-level change as a release and run quality evals before and after.

Transformer LLMs are costly at inference for three reasons: **size** (fix with compression, this file), **autoregressive decoding** (fix with speculative, reference-based or parallel decoding, this file) and **attention** (see the attention and kernels reference).

## Compression: quantization, distillation, pruning

**Quantization** lowers numeric precision. Going from 32-bit to 16-bit halves memory; 8-bit and 4-bit halve it again. In practice, weight-only quantization dominates: simple, usually effective without extra work, and especially strong for bandwidth-bound decode since fewer bytes per step means more tokens per second. Its ceiling is near: you cannot go below one bit per value.

**Distillation** trains a small student to imitate a large teacher; for a specific task the student can behave comparably at a fraction of the size. Cost: a training project with data and task-specific validation.

**Pruning** means either removing whole units (architecture and parameter count shrink) or zeroing the least useful weights (parameter count stays, non-zero count drops, so the model becomes sparse). A pruned model can be used directly or finetuned to recover quality, and pruning can reveal smaller architectures worth training from scratch. Research results are strong (lottery-ticket work removed over 90% of non-zero weights in some networks without accuracy loss), yet practice lags because pruning needs deep knowledge of the architecture, usually yields smaller gains than alternatives, and many chips cannot exploit sparsity.

## Choosing a compression approach

| Situation | Choice |
|---|---|
| Want a quick, low-effort win on any model | Weight-only quantization: 8-bit first, then 4-bit if evals hold |
| Model does not fit the target hardware | Quantize first; then a distilled or smaller model, or tensor parallelism |
| Narrow task, budget for training | Distillation |
| Architecture expertise plus sparse-friendly hardware, other levers exhausted | Pruning |
| Quality must not move | Skip lossy compression; use lossless decoding and service-level levers |

## The autoregressive decoding bottleneck

Generation is sequential (100 ms per token means 10 s for 100 tokens) and expensive: output tokens cost about 2 to 4x input tokens across providers, and Anyscale measured one output token weighing on latency like about 100 input tokens. A small gain in decode speed noticeably improves experience. The methods below reflect a fast-moving area; future architectures may remove the bottleneck.

## Speculative decoding

Also called speculative sampling. A cheap **draft** (proposal) model guesses ahead and the **target** model, whose quality you want, checks the guesses.

1. Draft proposes K tokens.
2. Target scores all K positions in one parallel pass.
3. Keep the longest left-to-right run the target agrees with (j tokens).
4. Target appends one token of its own; repeat.

Each loop yields 1 to K + 1 tokens, and the output matches the target model's, so it is lossless.

Why it wins despite rejections:

- Verification is parallel and prefill-like, far cheaper than sequential generation.
- Many tokens are easy, so a weak drafter often gets them right.
- Decode leaves compute idle, so verification is nearly free. If MFU is already saturated (very large batches), that slack is gone and gains shrink.

Tuning:

- Acceptance depends on domain; structured text like code accepts more than free prose.
- Larger K means fewer target passes when guesses land but lower acceptance of long runs. Tune K on your traffic.
- The drafter can be any architecture but should ideally share the target's vocabulary and tokenizer: a small same-family model or a custom-trained one. DeepMind's 4B drafter for Chinchilla-70B ran about 8x faster per token (1.8 ms vs 14.1 ms) and cut response latency by more than half with no quality loss; T5-XXL saw similar gains.
- Implementation is cheap (about 50 lines of PyTorch) and already built into vLLM, TensorRT-LLM and llama.cpp, so usually you enable and tune rather than build.

## Inference with reference

Answers often copy spans of their input: quoting a retrieved document, re-emitting code with a small fix, repeating earlier turns. Inference with reference proposes draft tokens taken from the input instead of from a draft model, then verifies them with the target as above.

- No extra model to host or train.
- The core problem is picking which context span to propose at each step; the simplest method finds a span matching the latest output tokens and proposes what follows it.
- Only helps with heavy input/output overlap: RAG, code editing, multi-turn chat. Yang et al. (2023) reported about 2x faster generation in such settings.
- Lossless, since the target verifies everything.

## Parallel decoding

These methods try to break the sequential dependency by producing positions t+1 through t+k at once. It can work because context often constrains tokens a few positions ahead even when the very next one is uncertain.

- **Lookahead decoding** (same decoder) uses the Jacobi method, an iterative solver that updates many parts of a solution independently: guess K future tokens in parallel, check them against the context, regenerate only the failing ones, and iterate until all pass. The family is called Jacobi decoding.
- **Medusa** attaches several small heads to a frozen base model; head k learns to predict the token k+1 positions beyond the base model's next token. Each head proposes several candidates, arranged in a tree and verified with tree-structured attention to pick the best consistent path. NVIDIA reported up to 1.9x faster Llama 3.1 generation on HGX H200.

Verification and integration are essential because tokens are not produced in order. The idea is appealing but unintuitive, and Medusa is hard to implement since it requires training heads.

## Choosing a decoding accelerator

| Situation | Best fit |
|---|---|
| Outputs copy large spans of the prompt | Inference with reference |
| Decode-bound serving, idle compute, same-tokenizer small model available | Speculative decoding |
| Structured outputs (code, JSON) | Speculative decoding, expect high acceptance |
| You own the model and can train add-on heads | Medusa |
| No extra model or training allowed | Lookahead/Jacobi, inference with reference |
| Compute already saturated at large batch | Little gain from any; use service-level levers |

## Worked examples

**Speculative back-of-envelope.** Assume each draft token is accepted independently with probability 0.7 and K = 4. Expected tokens per target pass = (1 - 0.7^5) / (1 - 0.7), about 2.77. If a target pass costs 20 ms and drafting 4 tokens costs 6 ms, each loop yields 2.77 tokens in 26 ms, about 9.4 ms per token versus 20 ms: roughly 2.1x. At acceptance 0.3, expected tokens fall to about 1.42 and per-token time to about 18 ms, almost no gain. Measure acceptance on real traffic first.

**Quantization and fit.** A 70B model in FP16 needs about 140 GB of weights, over one 80 GB GPU. INT8: about 70 GB, fitting with little KV room. INT4: about 35 GB, leaving space for a large cache. Each halving also roughly halves bytes streamed per decode step.

## Pitfalls

- Shipping quantized or pruned models without quality evals.
- Expecting pruning gains on hardware that ignores sparsity.
- Draft model with a different tokenizer, or K picked without measuring acceptance.
- Speculative decoding on compute-saturated servers.
- Inference with reference for open-ended generation with little prompt overlap.
- Underestimating the work of training Medusa heads.
