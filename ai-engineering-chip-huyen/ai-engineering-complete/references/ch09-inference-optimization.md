---
name: ai-eng-ch09-inference-optimization
description: Use when making an LLM application faster or cheaper: diagnosing latency/cost, choosing metrics (TTFT, TPOT, goodput, MFU, MBU), sizing KV cache and GPU memory, selecting accelerators, choosing online vs batch APIs, or applying quantization, speculative decoding, batching, prefill/decode split, prompt caching and parallelism. Based on Chapter 9 of Chip Huyen's "AI Engineering".
---

# Chapter 9: Inference Optimization (AI Engineering, Chip Huyen)

## When to use this skill

Apply this skill whenever an engineer's question is about speed, cost or capacity of running a foundation model rather than about output quality. Typical triggers:

- "Our chatbot feels slow" or "p99 latency spiked": decompose latency and find the bottleneck.
- "Inference is too expensive": compute cost per request, look for batching, caching, compression or batch APIs.
- "Which GPU should we buy or rent?" or "Will this model fit?": memory, bandwidth and FLOP/s sizing, KV cache math.
- Self-hosting an open model (vLLM, TensorRT-LLM, llama.cpp, TGI, SGLang): picking server-level features.
- Comparing inference providers or frameworks, or choosing online, batch or streaming endpoints.

Hosted-API users get most model- and server-level techniques from the provider; their levers are API mode, prompt caching, prompt/output length, model choice and correct measurement. The mental models below still help evaluate providers.

## Core mental models

**Three levels of optimization.** Gains come from the model (make it smaller or architecturally cheaper), the hardware (faster chips), and the service (how requests are scheduled onto hardware). Production systems combine several levels. Model-level changes can alter outputs; service-level changes should not.

**Inference server vs inference service.** The server hosts models and owns hardware; the service wraps it with request intake, routing and preprocessing. A hosted model API is an entire inference service you rent.

**Bottlenecks: compute-bound vs memory bandwidth-bound.** A workload is compute-bound when the arithmetic itself limits speed, and bandwidth-bound when moving data (weights, KV cache) between memory and compute units limits speed. Arithmetic intensity (operations per byte moved) decides which; a roofline plot from a profiler such as NVIDIA Nsight shows where a kernel sits. Fixes differ: compute-bound work benefits from more FLOP/s or more chips; bandwidth-bound work benefits from higher memory bandwidth and fewer bytes per parameter.

**Terminology trap.** "Memory-bound" means bandwidth-bound to systems engineers but often means capacity-bound (OOM) to ML engineers. Capacity problems can usually be worked around by splitting work (e.g., offloading part of a model to CPU RAM), which then turns into a bandwidth problem. Clarify which one is meant.

**Prefill vs decode.** Prefill processes all input tokens in parallel and is compute-bound; it determines time to first token and populates the KV cache. Decode emits one token per step and, because each step must stream the full weights from HBM to the cores while doing little arithmetic, it is bandwidth-bound and leaves FLOPs idle. Context length, output length and batching strategy shift the balance. Image diffusion models, by contrast, are typically compute-bound. Many current LLM and data workloads are bandwidth-bound.

**Output tokens dominate.** Output tokens are priced roughly 2 to 4 times input tokens across providers, and one measured output token can cost about as much latency as ~100 input tokens. Small improvements to decoding pay off disproportionately.

**Latency/throughput trade-off.** Batching and higher concurrency raise throughput (lower cost) while raising per-request latency. Reports from production teams show 2 to 3 times throughput gains are possible if you accept worse TTFT and TPOT. Lower latency usually costs more money.

**Utilization is a means, not the goal.** High utilization is meaningless if cost and latency both get worse; the real targets are speed and cost.

**Model quality can drift with optimization.** The same open model served by different providers can score differently on benchmarks because of quantization or other lossy shortcuts. Always re-evaluate quality after an optimization that touches the model.

## Metrics to measure (and how)

| Metric | What it captures | Notes |
|---|---|---|
| Latency | Request sent to full response | Total = TTFT + TPOT x output tokens |
| TTFT | Time to first token; driven by prefill and input length | Chat needs near-instant; long-doc summarization tolerates more |
| Time to publish | Time to first token the user actually sees | Matters for agents/CoT, where hidden planning and tool calls precede visible output |
| TPOT (also TBT, ITL) | Time between output tokens; driven by decode | For streamed reading, ~120 ms/token (6 to 8 tok/s) already outpaces fast readers |
| Throughput | Output tokens/s across all users (TPS); also tokens/s/user | Count input (prefill) and output (decode) throughput separately |
| RPS / RPM | Completed requests per second or minute | RPM is more natural for multi-second LLM calls; providers may throttle concurrency |
| Cost per request | Prefill cost + decode cost | Best cross-model comparison since tokenizers differ |
| Goodput | Requests per unit time that meet the latency SLO | Guards against chasing throughput at the expense of UX |
| MFU | Achieved FLOP/s (or tokens/s) vs theoretical peak | Higher in training than inference, higher in prefill than decode; >50% is good for training |
| MBU | Achieved memory bandwidth vs peak | Bandwidth used ~ params x bytes/param x tokens/s |

Measurement rules:

- Treat latency as a distribution. Report p50, p90, p95, p99, never only the mean; a single 3-second outlier among 100 ms requests can inflate the mean several-fold. Investigate outliers (network errors, extreme prompt lengths).
- Plot TTFT against input length to separate "long prompt" slowness from genuine service problems.
- Distinct TTFT/TPOT profiles with equal total latency feel different to users; decide the preferred profile with user studies. You can trade one for the other by shifting compute between prefill and decode.
- nvidia-smi "GPU utilization" only reports the fraction of time the GPU is busy, not how much of its capacity is used. Do not use it as an efficiency signal; use MFU and MBU.
- Compute-bound phases show high MFU and low MBU; bandwidth-bound phases the reverse. MBU tends to fall as concurrency rises because the workload shifts toward compute-bound.
- Chip vendors' peak FLOP/s may be measured under favorable conditions (e.g., sparsity), so real MFU against spec sheets can look low.

Worked cost example (illustrative numbers): a $4/hour instance decoding 400 tokens/s produces 1.44M tokens/hour, so about $2.78 per 1M output tokens; 1,000 requests averaging 500 output tokens cost about $1.39 to decode. If it prefills 200 requests/minute, prefill for 1,000 requests costs about $0.33. Total is roughly $1.72 per 1,000 requests.

Worked MBU example: an 8B model in INT8 (1 byte/param) decoding at 150 tokens/s moves about 8e9 x 1 x 150 = 1.2 TB/s; on a chip with ~3.35 TB/s peak that is ~36% MBU. Halving bytes per parameter halves bandwidth demand, which is why quantization helps decode so much.

Worked goodput example: SLO of TTFT <= 500 ms and TPOT <= 50 ms; the service completes 60 requests/minute but only 45 meet both limits, so goodput is 45 RPM.

## Hardware essentials (AI accelerators)

- CPUs: few strong cores, best for sequential, single-thread-heavy work. GPUs: thousands of small cores for parallel work; matrix multiplication (the bulk of neural network FLOPs) parallelizes well. Alternatives include AMD GPUs, Google TPUs, Intel Gaudi, Graphcore IPU, Groq LPU, Cerebras, plus inference-focused chips (AWS Inferentia, Meta MTIA, Apple Neural Engine) and edge chips (Edge TPU, Jetson).
- Inference can account for the large majority (up to ~90%) of ML cost for deployed systems, which is why inference-specific chips favor low precision and fast memory access over large memory capacity. Training needs more memory (backprop) and is harder at low precision.
- Compute units are specialized for scalars, vectors or tensors (e.g., tensor cores on modern GPUs, tensor-first TPUs). Efficient execution must respect a chip's memory layout and compute primitives.
- Three numbers to compare chips: FLOP/s (drops as precision rises; FP8 roughly doubles FP16 throughput on recent NVIDIA parts), memory size, and memory bandwidth. Then power: maximum power draw and TDP (max draw is roughly 1.1 to 1.5 times TDP). Power matters for on-prem cost, data center siting and environmental impact; electricity is a real constraint on scaling compute.
- Memory hierarchy, slow to fast: CPU DRAM (tens of GB/s, large), GPU HBM (hundreds of GB/s to >1.5 TB/s, tens of GB), on-chip SRAM caches (>10 TB/s, tens of MB). Much GPU optimization is about keeping hot data high in this hierarchy. Mainstream frameworks give little control over this, hence interest in CUDA, Triton and ROCm.

## Decision frameworks

**Online vs batch vs streaming**

| Situation | Choose |
|---|---|
| User is waiting (chat, coding assistant) | Online API |
| Long outputs where perceived wait matters | Online + streaming (but you cannot score the full response before display; plan for retroactive retraction) |
| No tight deadline: synthetic data, periodic reports, bulk document onboarding, re-processing data for a model migration, mass personalization, re-indexing a knowledge base | Batch API (providers have offered ~50% discounts with turnaround in hours) |
| You run the service and demand exceeds capacity | Expose separate online and batch endpoints so urgent traffic is served first |

Do not confuse this with traditional ML batch inference, which precomputes predictions for a finite input set before requests arrive. Open-ended prompts cannot be precomputed (though fixed parts such as system prompts can be cached).

**Selecting accelerators.** Ask: can it run the workload (memory size), how fast (FLOP/s and bandwidth), and at what cost (cloud hourly price, or purchase price plus power). Bandwidth-bound workloads (LLM decode, long context) favor high-bandwidth, high-memory chips; compute-bound workloads (prefill-heavy, diffusion) favor high FLOP/s.

**Matching technique to symptom**

| Symptom / goal | Primary levers |
|---|---|
| Model doesn't fit in memory | Weight quantization, tensor parallelism, pipeline parallelism, smaller or distilled model |
| Slow TPOT (decode) | Quantization (fewer bytes per step), speculative decoding, inference with reference, parallel decoding (Medusa, lookahead), prefill/decode disaggregation |
| Slow TTFT | Prompt caching, shorter prompts, more prefill instances, tensor parallelism, FlashAttention-class kernels |
| KV cache limits batch size or context | GQA/MQA, cross-layer attention, local+global attention (training-time), PagedAttention, KV cache quantization or compression |
| High cost, relaxed latency | Larger batches, batch API, cheaper hardware, quantization |
| High cost from repeated prefixes | Prompt (prefix/context) caching |
| Strict latency at high load | More replicas, tensor parallelism; avoid pipeline parallelism |
| Mixed request lengths waste batch slots | Continuous (in-flight) batching |

**Model-level technique selection**

| Technique | Quality risk | Effort | When to use |
|---|---|---|---|
| Weight-only quantization | Low to moderate; evaluate | Low | Default first step; near-universal benefit, but little room left below a few bits |
| Distillation | Moderate; task-dependent | High (training) | You need a much smaller model that matches the big one on your task |
| Pruning | Variable | High; needs architecture knowledge and sparse-friendly hardware | Rarely the first choice in practice despite strong research results |
| Speculative decoding | None (lossless) | Low to moderate | Decode-bound serving with spare FLOPs; structured outputs like code accept more drafts |
| Inference with reference | None | Low | Outputs copy large spans of input: RAG answers, code edits, multi-turn chat |
| Parallel decoding (Medusa, lookahead/Jacobi) | Low if verified | High | You control the model and can train extra heads or tune the decoder |
| Attention redesign (local window, MQA, GQA, cross-layer) | Changes model | Requires training or finetuning | Building or finetuning a model for long context or large batches |
| KV cache management | None to low | Usually via framework | Long contexts, large batches |
| Kernels and compilers | None | Use existing (torch.compile, TensorRT, XLA); custom is expert work | Always use available compiled kernels; write custom only for hot paths |

**Speculative decoding parameters.** Pick a draft model that ideally shares the target's tokenizer and vocabulary (a small same-family model or a custom-trained one). Larger K means fewer target verification passes but lower acceptance. If MFU is already saturated, the free FLOPs it relies on are gone, so gains shrink.

**Prefill-to-decode instance ratio (when disaggregating).** Long inputs and TTFT priority: roughly 2:1 to 4:1. Short inputs and TPOT priority: roughly 1:2 to 1:1. Tune from measured traffic.

**Parallelism choice**

| Strategy | What is split | Main benefit | Main cost |
|---|---|---|---|
| Replica (data) parallelism | Nothing; full copies | Easy; more concurrent requests; lower latency under load | More chips; bin-packing models of different sizes onto GPUs of different memory |
| Tensor (intra-operator) parallelism | Tensors within each operator across devices | Fits huge models and lowers latency | Inter-device communication overhead |
| Pipeline parallelism | Layers into sequential stages; micro-batches flow through | Fits huge models; good throughput (common in training) | Adds per-request latency; avoid for strict latency |
| Context parallelism | The input sequence (e.g., halves on different devices) | Long inputs | Niche, complex |
| Sequence parallelism | Different operators (attention vs feedforward) on different devices | Long inputs | Niche, complex |

## Step-by-step playbooks

**Playbook A: diagnose a slow or expensive LLM endpoint**
1. Define SLOs (e.g., p95 TTFT, p95 TPOT) and a cost target per request.
2. Instrument TTFT, TPOT, time to publish, total latency, input and output token counts, throughput, RPM, and cost per request. Collect percentiles.
3. Split latency: TTFT high means prefill problem (long prompts, queueing, no caching); TPOT high means decode problem (bandwidth, oversized batches, prefill interference). Large gap between TTFT and time to publish means hidden agent/CoT steps; reduce steps or stream intermediate status.
4. Check for prefix repetition (system prompt, shared documents, conversation history). If present, enable prompt caching.
5. Check output lengths; trimming verbose outputs is often the cheapest win given output-token pricing.
6. Move latency-insensitive jobs to a batch API or queue.
7. If self-hosting, measure MFU and MBU to confirm the bottleneck, then pick levers from the symptom table.
8. Change one thing at a time; re-measure goodput and run the quality eval suite after each model-level change.

**Playbook B: size memory for a self-hosted model**
1. Weights: parameters x bytes per parameter (FP16 = 2, INT8 = 1, INT4 = 0.5).
2. KV cache (no optimizations): 2 x batch x sequence length x layers x model dimension x bytes per value. Example: 32 layers, dimension 4,096, batch 16, 4,096-token sequences, FP16 gives about 34 GB, comparable to or larger than the weights of a 13B FP16 model. GQA/MQA divide this by the query-to-KV-head ratio.
3. Add headroom for activations and framework overhead.
4. If it doesn't fit: quantize weights, quantize KV cache, reduce max batch or context, use PagedAttention-based servers, or add tensor parallelism.
5. Estimate decode speed ceiling: peak bandwidth / (weight bytes + KV bytes read per step).

**Playbook C: stand up a self-hosted inference stack**
1. Use a mature framework (vLLM, TensorRT-LLM, llama.cpp or similar) to get continuous batching, PagedAttention, optimized attention kernels and speculative decoding without custom work.
2. Compile the model (torch.compile or vendor compiler) so operations lower to efficient kernels.
3. Quantize weights (INT8, then INT4 if quality holds). A public PyTorch case study on a 7B model stacked compile, INT8, INT4 and speculative decoding for large cumulative throughput gains, but quality impact was not reported, so evaluate yourself.
4. Enable prefix caching.
5. Configure batching: continuous batching for LLMs; if using dynamic batching, set both max batch size and max wait window.
6. Choose parallelism: replicas for scale and latency; tensor parallelism when the model doesn't fit or latency must drop; avoid pipeline parallelism for interactive traffic.
7. At larger scale, disaggregate prefill and decode onto separate instances connected by fast interconnect (e.g., NVLink).
8. Load-test with realistic length distributions; report goodput, not just throughput.

## Checklists

**Before optimizing**
- [ ] SLOs defined per use case (TTFT, TPOT, total latency) and a cost-per-request target.
- [ ] Percentile latency, token counts and cost per request instrumented.
- [ ] Bottleneck identified (compute vs bandwidth vs capacity; prefill vs decode).
- [ ] Quality eval suite ready to detect regressions from lossy changes.

**Hosted API users**
- [ ] Streaming enabled where users read output live, with a plan for post-hoc moderation.
- [ ] Non-urgent workloads routed to batch APIs.
- [ ] Prompts ordered so stable content (system prompt, shared docs, examples) forms a cacheable prefix; provider prompt caching enabled (at writing, providers discounted cached input 75% to 90% and cut TTFT up to ~75% on long prefixes); cache storage fees accounted for.
- [ ] Output length constrained.
- [ ] Concurrency kept under provider rate limits.

**Self-hosters**
- [ ] Continuous batching and paged KV cache on.
- [ ] Weights quantized and quality re-checked.
- [ ] Optimized attention kernels (FlashAttention-class) and compiler in use; kernels match the GPU generation.
- [ ] Speculative decoding or inference with reference evaluated for decode-heavy traffic.
- [ ] Parallelism strategy fits latency goals; replica placement treated as bin-packing.
- [ ] MFU/MBU tracked over time (not nvidia-smi utilization).

**Evaluating a provider or framework**
- [ ] Benchmarked on your own prompts with your own length distribution.
- [ ] Compared by cost per request and goodput, not raw tokens/s (tokenizers differ).
- [ ] Quality checked against a reference deployment, since providers may quantize.

## Pitfalls and anti-patterns

- Reporting mean latency only; it hides tails and is distorted by outliers.
- Measuring TTFT from the model's perspective in agentic flows while users wait for hidden steps.
- Trusting nvidia-smi utilization as proof of efficient GPU use.
- Chasing maximum throughput or utilization while goodput and user experience degrade.
- Comparing tokens/s across models with different tokenizers.
- Assuming optimizations are free of quality impact; quantization, pruning and some provider shortcuts change outputs.
- Static batching for interactive traffic (early requests wait for the batch to fill) or naive batching where short responses wait for long ones.
- Co-locating prefill and decode at high load, letting new prefills starve ongoing decodes and inflate TPOT.
- Pipeline parallelism for latency-critical serving.
- Ignoring KV cache growth: it grows linearly with sequence length and batch size and can exceed weight memory several-fold, capping batch size and context.
- Expecting speculative decoding to help when compute is already saturated, or using a draft model with a different tokenizer.
- Investing in pruning or custom kernels before exhausting quantization, batching, caching and off-the-shelf kernels; and assuming kernels carry over to new hardware (FlashAttention needed a new version for H100).
- Putting variable content (timestamps, user data) before stable content in prompts, which breaks prefix caching.
- Implementing a prompt cache from scratch without budgeting its memory and engineering cost.

## Key terms

- **Arithmetic intensity / roofline**: operations per byte moved; plotted to classify kernels as compute- or bandwidth-bound.
- **Prefill / decode**: parallel input processing (compute-bound) vs one-token-at-a-time generation (bandwidth-bound).
- **TTFT, TPOT, TBT, ITL, time to publish**: first-token latency, per-token latency and its variants, and first visible token latency.
- **Goodput**: completed requests per unit time that satisfy the SLO.
- **MFU / MBU**: model FLOP/s utilization and model bandwidth utilization.
- **HBM, SRAM, DRAM**: GPU high-bandwidth memory, on-chip cache memory, host memory.
- **TDP**: thermal design power, a proxy for typical power draw.
- **Quantization, distillation, pruning**: reduce precision, train a small mimic, remove or zero parameters.
- **Speculative decoding**: a draft model proposes K tokens; the target verifies them in parallel and keeps the longest agreed prefix plus one token of its own; lossless.
- **Inference with reference**: drafts copied from the input context instead of a draft model.
- **Parallel decoding**: predicting several future tokens at once, then verifying (lookahead/Jacobi iteration, Medusa heads with tree attention).
- **KV cache**: stored key/value vectors of prior tokens, inference-only; attention compute grows quadratically with length, cache size linearly.
- **Local windowed attention, MQA, GQA, cross-layer attention**: architectural ways to shrink attention cost and KV cache.
- **PagedAttention**: non-contiguous block allocation of KV cache to cut fragmentation (vLLM).
- **Kernel**: hardware-specific optimized routine; built with vectorization, parallelization, loop tiling, operator fusion.
- **Lowering / compiler**: translating model code to hardware instructions, substituting kernels (torch.compile, XLA/OpenXLA, TensorRT, TVM, MLIR).
- **Static, dynamic, continuous batching**: fixed-size batches; size-or-timeout batches; slots refilled as requests finish (Orca, in-flight batching).
- **Prefill/decode disaggregation**: running the two phases on separate instances.
- **Prompt cache (context or prefix cache)**: reuse of processed shared prompt prefixes.
- **Replica, tensor, pipeline, context, sequence parallelism**: ways to spread serving across devices.

## Source map

Chapter 9, "Inference Optimization":
- Understanding Inference Optimization
  - Inference Overview (Computational bottlenecks; Online and batch inference APIs)
  - Inference Performance Metrics (Latency, TTFT, and TPOT; Throughput and goodput; Utilization, MFU, and MBU)
  - AI Accelerators (What's an accelerator?; Computational capabilities; Memory size and bandwidth; Power consumption; Selecting accelerators sidebar)
- Inference Optimization
  - Model Optimization (Model compression; Overcoming the autoregressive decoding bottleneck: Speculative decoding, Inference with reference, Parallel decoding; Attention mechanism optimization: Redesigning the attention mechanism, Optimizing the KV cache size, Writing kernels for attention computation, Calculating the KV cache size sidebar; Kernels and compilers; PyTorch case study sidebar)
  - Inference Service Optimization (Batching; Decoupling prefill and decode; Prompt caching; Parallelism)
- Summary
