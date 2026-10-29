# Memory Math, Numeric Formats and Quantization

## Contents
- Core takeaways
- Why training needs more memory than inference
- Inference and training formulas
- Activations and gradient checkpointing
- Ways to make a job fit
- Numeric formats: range versus precision
- Choosing and loading a format
- Quantization: what and when
- Inference quantization
- Training quantization and mixed precision
- Worked estimates
- Glossary

## Core takeaways

1. Memory is the binding constraint, for serving and even more for training.
2. Three numbers drive the footprint: total parameters, trainable parameters, bytes per value.
3. Fewer trainable parameters means less memory: the motivation for PEFT.
4. Fewer bits per value is the simplest general lever: 13B parameters are 52 GB in FP32, 26 GB in 16-bit.
5. Serving uses as few bits as quality allows (16, 8, even 4). Training is precision-sensitive and usually runs in mixed precision.

## Why training needs more memory than inference

Inference runs the forward pass only. Training adds a backward pass: compute the loss against ground truth, compute one gradient per trainable parameter (how much the loss moves when that parameter moves), and let the optimizer convert gradients into updates. So every trainable parameter carries a gradient plus optimizer state; frozen ones carry neither.

| Optimizer | State values | Values incl. gradient |
|---|---|---|
| Plain SGD | 0 | 1 |
| Momentum | 1 | 2 |
| Adam (dominant for transformers) | 2 | 3 |

## Inference and training formulas

**Inference.** Weights take N x M (N parameters, M bytes each). Activations and attention key-value vectors grow linearly with sequence length and batch size; a workable default is 20% of weight memory, so total is about **N x M x 1.2**. Raise the allowance for long contexts or big batches. Examples: 13B at 2 bytes is 26 GB of weights, about 31.2 GB to serve; 70B at 2 bytes is 140 GB for weights alone.

**Training** = weights + activations + gradients + optimizer states. With Adam and 2-byte values, gradients plus states cost **trainable x 3 x 2 bytes**:
- all 13B parameters trainable: 78 GB on top of 26 GB of weights;
- 1B trainable: 6 GB;
- full finetune of 7B in 16-bit: 14 + 42 = 56 GB before activations. Consumer GPUs have 12 to 24 GB, high-end cards up to 48 GB.

The 2-byte assumption is a simplification. Many mixed-precision setups keep optimizer states and a master weight copy in FP32, which can double or triple these figures.

## Activations and gradient checkpointing

The formulas assume activations are smaller than weights. During training that often fails: activations stored for the backward pass can dwarf the weights, growing with scale, sequence length and batch (measured on Megatron models by Korthikanti et al.). Gradient checkpointing (activation recomputation) drops activations and recomputes them when needed, saving memory at the cost of slower training.

## Ways to make a job fit

- **Shrink the footprint:** fewer trainable parameters (partial finetuning, PEFT); fewer bits (quantization, QLoRA); smaller micro-batches with gradient accumulation; gradient checkpointing.
- **Use memory better:** offload excess to CPU (popularized by DeepSpeed; QLoRA's paged optimizers are a variant); shard across GPUs or machines with DeepSpeed, PyTorch Distributed or ColossalAI.

## Numeric formats: range versus precision

| Format | Bits | Notes |
|---|---|---|
| FP64 | 64 | Default in NumPy and pandas; rarely used in neural nets |
| FP32 | 32 | Former default for training and serving |
| TF32 | 19 | NVIDIA format named for FP32 compatibility |
| FP16 | 16 | More precision bits, narrow range |
| BF16 | 16 | Designed by Google for TPUs; FP32's range, less precision |
| FP8, FP4 | 8, 4 | Minifloats; 4 bits is the smallest IEEE-consistent float |
| INT8, INT4 | 8, 4 | Integer (fixed-point); growing for serving |

A float has a sign bit, exponent bits for range and significand bits for precision. Lower precision perturbs values slightly; out-of-range values become infinity or garbage.

FP16 versus BF16 is the case to remember. A value near 70,000 overflows FP16 (max about 65,504) but survives in BF16; just above 1,024, BF16's worst-case rounding error is about 0.4% versus 0.05% for FP16. Choose by which failure hurts more: overflow or rounding.

## Choosing and loading a format

- **Load weights in their release format.** Reading BF16 weights as FP16 visibly hurts quality; many teams did this with Llama 2 (and again with Llama 3.1) and blamed the model.
- Choose by the workload's value range, its sensitivity to small numeric changes, and native hardware support.

## Quantization: what and when

Strictly, quantization means converting to integers; in practice it covers any precision reduction, as here. It is cheap, very effective, easy, and general across tasks and architectures (10B parameters: 40 GB in 32-bit, 20 GB in 16-bit).

- **What:** whatever dominates memory without hurting quality too much. Weights are quantized more often than activations because the quality impact is smaller and steadier.
- **When:** after training (PTQ, by far the most common, and what application developers use) or during training.

## Inference quantization

- Serving moved from FP32 to 16-bit in the late 2010s, then to 8-bit (LLM.int8()) and 4-bit (QLoRA's work).
- Mixed-precision serving keeps sensitive values high: Apple's on-device models averaged 3.5 bits by mixing 2- and 4-bit weights; NVIDIA Blackwell added 4-bit float inference.
- Below 8 bits you either keep floats (FP8, FP4) or, more commonly, use INT8 or INT4.
- The floor is 1 bit. BinaryConnect, Xnor-Net and BitNet tried it; BitNet b1.58 (1.58 bits per parameter) matched 16-bit Llama 2 up to 3.9B parameters.
- Lower precision also allows bigger batches and faster arithmetic, but format conversion overhead means latency does not always drop. Many tiny rounding errors can add up to a large quality loss.
- PTQ takes a few lines in PyTorch, TensorFlow or Hugging Face transformers; TensorFlow Lite and PyTorch Mobile offer it for devices, some of which run only quantized models.

Default: train high, quantize for serving, evaluate the quantized artifact you ship.

## Training quantization and mixed precision

Two goals: (1) a model that stays good in low precision when served, since PTQ can degrade it; (2) cheaper, faster training.

| Technique | Goal 1 | Goal 2 | Notes |
|---|---|---|---|
| Quantization-aware training (QAT) | Yes | No | Simulates low precision while computing in high; can slow training |
| Training directly in low precision | Yes | Yes | Hard because backprop is precision-sensitive; Character.AI reported full INT8 training, removing the train/serve mismatch |
| Mixed precision | Partly | Yes | High-precision master weights with low-precision gradients and activations, or sensitive parts kept high (LLM-QAT kept embeddings at 16-bit, weights and activations at 4-bit) |
| Automatic mixed precision (AMP) | | Yes | Framework picks precision per operation |
| Phase-split precision | | Yes | Pretrain high, finetune lower; common when a well-resourced lab releases a model others adapt |

Why training is fragile at low precision: rounding errors compound over many update steps, and the loss needs precise computation because small errors there can point updates the wrong way.

## Worked estimates

Reproduce with `scripts/finetune_memory.py` (activation column is a lower bound for training).

| Scenario | Weights | Grad + Adam | Activations (20%) | Total |
|---|---|---|---|---|
| Serve 8B, BF16 | 16 GB | none | 3.2 GB | ~19.2 GB, fits 24 GB |
| Serve 8B, INT4 | 4 GB | none | 0.8 GB | ~4.8 GB |
| Full finetune 8B, 2-byte | 16 GB | 48 GB | 3.2 GB+ | ~67 GB, needs 80 GB or sharding |
| LoRA 8B, 40M trainable | 16 GB | 0.24 GB (+0.08 adapter) | 3.2 GB+ | ~19.5 GB |
| QLoRA 8B, 40M trainable | 4 GB | 0.24 GB (+0.08 adapter) | 0.8 GB+ | ~5.1 GB |

Common mistakes: sizing training from inference numbers, forgetting optimizer states, assuming training activations are small, and using QAT expecting faster training.

## Glossary

- **Optimizer state**: values an optimizer keeps per parameter between steps (Adam: two moment estimates).
- **Gradient checkpointing**: recomputing activations in the backward pass instead of storing them.
- **Exponent / significand bits**: a float's range / precision bits.
- **PTQ / QAT**: quantize after training / simulate low precision during training.
- **CPU offloading**: moving tensors from GPU to CPU memory to fit a job.
