# Attention, KV Cache, Kernels and Compilers

## Contents
- Why attention is a bottleneck
- Sizing the KV cache
- Redesigning attention (training-time)
- Managing the KV cache (serving-time)
- Attention kernels
- Kernel techniques
- Compilers and lowering
- Case study: stacking optimizations
- Decision guide
- Worked examples
- Pitfalls

## Why attention is a bottleneck

Each new token needs the key and value vectors of all earlier tokens. Rather than recompute them, the server stores and reuses them in the **KV cache**, computing K and V only for the newest token each step. Prefill fills the initial cache. Training needs no cache, because the whole sequence is known and processed in one pass.

Two growth laws: attention compute over a generation grows quadratically with length, and KV cache memory grows linearly with both sequence length and batch size.

Consequences:

- The cache competes with weights for HBM, capping batch size and context.
- Reading it each decode step adds bandwidth load and latency.
- It can exceed the weights: a Google analysis of a 500B+ multi-head-attention model at batch 512 and 2,048-token context found a 3 TB cache, three times the weights.

This compute and memory cost is a main reason long context is hard. Fixes fall into three buckets: redesign attention, manage the cache, write faster kernels.

## Sizing the KV cache

Unoptimized multi-head attention:

**KV bytes = 2 x B x S x L x H x M**

(2 for key and value; B batch; S sequence length including generated tokens; L layers; H model dimension; M bytes per value, 2 for FP16/BF16, 1 for 8-bit.)

With GQA or MQA, replace H with KV heads x head dimension. With 32 query heads and 8 KV heads the cache shrinks 4x; with one KV head (MQA), 32x.

Planning rules:

- HBM budget = weights + KV cache at peak batch and context + activations and framework overhead.
- Max concurrent sequences = (HBM - weights - overhead) / KV bytes per sequence.
- Decode bytes per step = weights + KV read for the batch; at large batch and long context the cache can dominate traffic.

## Redesigning attention (training-time)

These change the architecture, so they need training or finetuning, or choosing a model that already has them.

- **Local windowed attention**: attend only to a fixed window of recent tokens. Cache and compute scale with the window: 32k-token sequences with a 4k window shrink both about 8x.
- **Interleaved local and global attention**: local layers capture nearby context, global layers keep document-wide information.
- **Multi-query attention (MQA)**: all query heads share one KV set.
- **Grouped-query attention (GQA)**: query heads in groups share a KV set per group; a tunable middle ground.
- **Cross-layer attention**: adjacent layers share K and V; three layers sharing cuts the cache 3x.

Character.AI reports conversations averaging about 180 messages, making KV cache their main throughput limit. Combining MQA, interleaved local/global attention and cross-layer sharing cut their cache over 20x, and memory stopped limiting large batches.

## Managing the KV cache (serving-time)

- **PagedAttention** (vLLM): stores the cache in non-contiguous fixed-size blocks, like virtual-memory pages, cutting fragmentation and allowing blocks to be shared across sequences. A key reason vLLM spread quickly.
- **KV cache quantization**: store K and V at lower precision.
- **Adaptive KV compression**: keep full detail only where it matters.
- **Selective KV cache**: keep entries for a subset of past tokens.

The last three are potentially lossy; check long-context quality.

## Attention kernels

Leave the math and storage alone and compute attention faster on the specific chip. **FlashAttention** fuses several transformer operations into one kernel that keeps intermediates in on-chip memory instead of round-tripping to HBM. Kernels are hardware-specific: FlashAttention first targeted A100-class GPUs, and H100s needed FlashAttention-3. Confirm your framework ships the version that matches your GPUs.

## Kernel techniques

A **kernel** is a routine tuned for one accelerator, used for repeated parallel operations: matrix multiplication, attention, convolution (common in image generators). Writing one needs detailed knowledge of the memory hierarchy (registers, shared memory, caches, global memory) and is usually done in CUDA, Triton or ROCm, which give fine control over threads and memory but are harder than Python. Once the domain of specialists at chip vendors and framework teams, kernel work now attracts many AI engineers. Companies often guard their kernels as trade secrets, since faster kernels mean cheaper serving.

| Technique | Idea | Portability |
|---|---|---|
| Vectorization | Handle several contiguous elements per instruction, reducing I/O | Broad |
| Parallelization | Split arrays into independent chunks across cores or threads | Broad |
| Loop tiling | Reorder loop data access to fit the chip's memory layout and caches | Hardware-specific; CPU tilings can be poor on GPU |
| Operator fusion | Run several operators in one pass so data is read and written once | Needs knowledge of the model's operators; most engineer-intensive |

## Compilers and lowering

Running a model script on a chip requires translating its operations into that chip's instructions: **lowering**, performed by a **compiler**, which swaps in specialized kernels where it can.

- Standalone: Apache TVM, MLIR.
- Integrated: torch.compile, XLA/OpenXLA (from TensorFlow), the TensorRT compiler for NVIDIA GPUs.
- Proprietary in-house compilers at AI companies.

Stance: always use available compilation and fused kernels; write custom kernels only for proven hot spots and only if you can maintain them across hardware generations.

## Case study: stacking optimizations

The PyTorch team sped up Llama-7B on one A100 80 GB by applying, in order: torch.compile, INT8 weights, INT4 weights, speculative decoding. Each step added throughput and the gains compounded. Quality impact was not reported, so measure it yourself before copying the stack.

## Decision guide

| Symptom | First move | Next |
|---|---|---|
| OOM or tiny batch at long context | Paged KV cache server; cap context per request | KV quantization; a GQA/MQA model |
| Decode slows as conversations grow | KV quantization or selective/compressed cache | Model with local/global or cross-layer attention |
| Slow prefill on long prompts | FlashAttention-class kernels via the framework | Prompt caching, tensor parallelism |
| Training a long-context model | Build in GQA/MQA, local windows, cross-layer sharing | Long-context quality evals |
| New GPU generation | Confirm kernel and compiler support | Re-benchmark; old tuning may not carry over |

## Worked examples

**GQA at long context.** 32 layers, 8 KV heads, head dim 128, FP16. Per token: 2 x 32 x 8 x 128 x 2 = 131,072 bytes. Batch 16 at 8,192 tokens: about 17.2 GB. With full multi-head attention (32 KV heads): about 68.7 GB, over four times the roughly 16 GB of FP16 weights for an 8B model.

**Capacity.** 80 GB GPU, 16 GB weights, 8 GB reserved overhead: 56 GB free. At about 1.07 GB per 8,192-token sequence, about 52 sequences fit; an 8-bit cache doubles that to about 104.

## Pitfalls

- Planning memory for weights only.
- Expecting attention redesigns to be switchable at serving time.
- Lossy KV compression without long-context checks.
- Custom kernels before compilers and stock fused kernels.
- Assuming kernels tuned for one GPU generation are optimal on the next.
