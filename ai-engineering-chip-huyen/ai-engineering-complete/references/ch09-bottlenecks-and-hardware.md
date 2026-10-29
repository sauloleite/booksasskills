# Bottlenecks and AI Accelerators

## Contents
- Where optimization happens
- Compute-bound vs bandwidth-bound
- The "memory-bound" ambiguity
- Prefill and decode as two workloads
- Accelerators: what they are and who makes them
- The spec numbers that matter
- Memory hierarchy
- Power and energy
- Selecting accelerators
- Worked examples
- Pitfalls

## Where optimization happens

| Layer | What you change | Effect on outputs |
|---|---|---|
| Model | Size, precision, architecture, decoding procedure | May change outputs (some decoding tricks are lossless) |
| Hardware | Chip and memory system | None |
| Service | Scheduling, batching, caching, placement, parallelism | Should not change outputs |

The **inference server** holds models and hardware and executes requests; the **inference service** wraps it with request intake, routing and preprocessing. A commercial model API is a whole service you rent, so most techniques here are the provider's job, but knowing them lets you judge providers and explain observed latency and cost.

## Compute-bound vs bandwidth-bound

- **Compute-bound**: time is set by the arithmetic required. More FLOP/s or more chips helps.
- **Memory bandwidth-bound**: time is set by data movement between memory and compute (weights streamed from HBM, data copied from host RAM). Faster memory or fewer bytes helps.

The test is **arithmetic intensity** (operations per byte moved). The **roofline model** (Williams et al., 2009) plots attainable performance against intensity: the slanted segment is the bandwidth ceiling, the flat segment the compute ceiling. Profilers such as NVIDIA Nsight draw it for your kernels, so check instead of guessing.

Typical cases at the time of writing: diffusion image generation is usually compute-bound; autoregressive LLM generation is usually bandwidth-bound; many AI and data workloads overall are bandwidth-bound because of transformer design and current accelerators. Re-check on new hardware and software.

## The "memory-bound" ambiguity

Systems and GPU engineers (and the Roofline paper) use "memory-bound" to mean bandwidth-bound; many ML engineers use it to mean capacity-bound, i.e. OOM. Ask which one a report means. The capacity case usually reduces to bandwidth anyway: an oversized model can be split between GPU and CPU memory, and the cost is transfer time. With a fast enough link, capacity would barely matter.

## Prefill and decode as two workloads

| Phase | Work | Bottleneck | Drives |
|---|---|---|---|
| Prefill | All prompt tokens in parallel; fills the KV cache | Compute | TTFT |
| Decode | One token per step | Bandwidth: each step pulls all weights from HBM yet does little math, leaving FLOPs idle | TPOT |

Implications used throughout the skill:

- The phases want different resources, so large deployments run them on separate machines.
- Idle decode FLOPs are what speculative and parallel decoding exploit.
- Fewer bytes per parameter speed up decode directly, which is why weight quantization works so well.
- Prompt length adds prefill, output length adds decode, and batching raises intensity because one weight read serves many sequences. Long context tends toward bandwidth limits, which attention and KV cache techniques can relieve.

## Accelerators: what they are and who makes them

An accelerator is a chip specialized for a workload class. CPUs have a few strong cores (around 64 at the high end of consumer parts) suited to sequential logic, OS work and I/O. GPUs have thousands of small cores for work that splits into independent pieces; matrix multiplication, which makes up more than 90% of a network's floating point work by common estimates, parallelizes extremely well.

NVIDIA dominates, with alternatives from AMD, Google (TPU), Intel (Habana Gaudi), Graphcore (IPU), Groq (LPU), Cerebras and others. A strong trend is **inference-specialized silicon**: inference can cost more than training for widely used systems (one survey: up to 90% of deployed ML cost). Training needs much more memory for backpropagation, is harder at low precision and prioritizes throughput; inference prioritizes latency. So inference chips (Apple Neural Engine, AWS Inferentia, Meta MTIA, edge parts like Google Edge TPU and NVIDIA Jetson Xavier) favor low precision and fast memory access over capacity. Some chips target a single architecture such as the transformer.

Compute units specialize in scalars, vectors or tensors. GPUs added tensor cores to their vector units; TPUs are tensor-first. Efficient execution must respect each chip's memory layout and primitives, which is why kernels are per-architecture.

## The spec numbers that matter

Compare chips on **FLOP/s, memory size, memory bandwidth**, then power.

- **FLOP/s**: peak operations per second, rarely reached in practice (actual/peak is a utilization metric). Lower precision yields more operations, though not exactly 2x per halving. On recent NVIDIA data-center parts, FP8 tensor throughput is about double FP16/BF16, which is about double TF32 (a 19-bit format). Spec sheets quoted "with sparsity" reflect favorable conditions, which the author calls peak FLOP/s hacking, and make your MFU look low.
- **Memory**: many parallel cores must be fed constantly, so GPU memory needs far more bandwidth and less latency than system RAM, part of why it costs more. CPUs use planar DDR SDRAM; high-end GPUs use stacked HBM; cheaper GPUs may use GDDR.

## Memory hierarchy

Orders of magnitude only:

| Level | Bandwidth | Size | Role |
|---|---|---|---|
| Host DRAM | Tens of GB/s (~25 to 50) | 16 to 64 GB laptops, 1 TB+ workstations | Overflow; slow path |
| GPU HBM | Hundreds of GB/s up to 1.5 TB/s and beyond on newer parts | ~24 to 80 GB | Weights, KV cache, activations |
| On-chip SRAM (L1/L2, sometimes L3, registers, shared memory) | Over 10 TB/s | Tens of MB (about 40 MB or less) | Hot data for the current operation |

Much GPU optimization is keeping data high in this hierarchy. PyTorch and TensorFlow expose little control over it, hence interest in CUDA, Triton and ROCm.

## Power and energy

Transistor switching consumes energy and produces heat that cooling must remove. An A100 has about 54 billion transistors, an H100 about 80 billion. An H100 at full load for a year uses roughly 7,000 kWh, versus roughly 10,000 kWh for an average US household per year. Electricity limits compute scaling; data-center siting trades cheap remote power against network latency that hurts inference.

Spec sheets list **maximum power draw** (peak at full load) and **TDP** (heat to dissipate under typical load, a proxy for expected draw). Max draw is often about 1.1 to 1.5 times TDP. Cloud users do not pay for cooling directly, but power matters for on-prem cost and sustainability.

## Selecting accelerators

1. **Characterize the workload.** Long prompts with short answers, embeddings and diffusion lean compute-bound; long generations, chat and long context lean bandwidth-bound. Confirm with roofline or MFU/MBU.
2. **Can it run?** Memory must hold weights at the chosen precision, KV cache at target batch and context, and overhead.
3. **How fast?** Compute-bound: FLOP/s at the precision you will run. Bandwidth-bound: memory bandwidth; decode ceiling is roughly bandwidth / bytes read per step.
4. **At what cost?** Cloud pricing is usage-based and similar across providers; owned hardware is purchase price plus ongoing power.
5. Choose the cheapest option that meets SLOs, not the highest peak specs or utilization.

## Worked examples

**Decode ceiling.** A 13B FP16 model is about 26 GB. On a 2 TB/s GPU at batch 1, the best case is about 2,000 / 26 = 77 tokens/s before KV reads and overhead. INT8 halves the bytes and raises the ceiling to about 154 tokens/s. A chip with double the FLOP/s but equal bandwidth would barely help.

**Two cards.** Card A has 2x the FLOP/s of card B with equal bandwidth and memory; B costs half as much. A decode-dominated chat service at small batch gets similar TPOT on B for half the price. A classifier sending 8,000-token prompts and reading back 5 tokens is prefill-bound and may justify A.

## Pitfalls

- Optimizing before measuring which bound applies.
- Misreading "memory-bound" (bandwidth vs OOM).
- Comparing chips on FLOP/s quoted with sparsity or at an unused precision.
- Sizing memory for weights only.
- Choosing hardware for peak utilization rather than cost at the required latency.
