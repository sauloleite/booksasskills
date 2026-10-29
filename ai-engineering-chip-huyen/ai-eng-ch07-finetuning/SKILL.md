---
name: ai-eng-ch07-finetuning
description: Decision rules and playbooks for adapting LLMs by finetuning, based on Chapter 7 of Chip Huyen's "AI Engineering". Covers finetune vs prompt vs RAG, GPU memory math for serving and training, numeric formats and quantization, PEFT, LoRA and QLoRA configuration and serving, model merging and multi-task finetuning, and finetuning hyperparameters. Use when deciding whether to finetune, sizing hardware, choosing LoRA rank/targets, serving many adapters, merging models, or debugging learning rate, batch size and epochs.
---

# Finetuning (AI Engineering, Chapter 7)

## Purpose

Help an engineer decide whether finetuning is warranted, pick the cheapest method that will work, size the hardware, configure and run the job, and serve or combine the results. The chapter's stance: finetuning is a late, deliberate step after disciplined prompting and (for factual gaps) retrieval; memory is its central constraint; and LoRA-style PEFT is the default technique. Data acquisition for finetuning, inference optimization and evaluation design belong to other chapters.

## Key decision rules

Apply these even without opening a reference.

**Whether to finetune**
1. Build the evaluation pipeline first and prompt systematically (clear instructions, realistic examples, versioned prompts, defined metrics). Many "prompting failed" claims come from sloppy prompt experiments.
2. Diagnose failures. Missing, private or stale facts point to RAG. Correct but irrelevant, malformed or unsafe outputs point to finetuning. In short: RAG for facts, finetuning for form.
3. If both kinds of failure exist, do RAG first, starting with term-based retrieval (BM25) before vector search.
4. Do not assume RAG plus finetuning beats RAG alone; in the cited study it helped only 43% of the time. Measure it.
5. Do not accept "general models are bad at our domain" without benchmarking a strong general model; a finance-specific 50B model lost to a general model released the same month.
6. Count the full cost: data, training skill, hosting, monitoring, and a policy for when a newer base model makes your finetune obsolete.
7. Expect regressions on tasks you did not train on. Fix by training on a mix of all query types, using per-task models, or merging.
8. Finetuning on low-quality data can increase hallucinations.

**Memory and precision**
9. Inference memory is about N x bytes x 1.2 (20% for activations and KV cache; more for long context or large batches).
10. Training adds, per trainable parameter, one gradient plus optimizer state (SGD 0, momentum 1, Adam 2). Adam at 2 bytes: trainable x 6 bytes. A 7B full finetune in 16-bit is about 56 GB before activations.
11. Training activations can exceed the weights; use gradient checkpointing to trade compute for memory.
12. Load a model in the dtype it was released in (BF16 read as FP16 degrades quality).
13. Quantize weights before activations. Serve at the lowest precision that holds quality and evaluate the quantized artifact. QAT improves low-precision quality but does not make training faster.

**Method and configuration**
14. Start with LoRA; move to full finetuning only with thousands-plus examples and a LoRA plateau. With a few hundred examples, full finetuning may not beat LoRA.
15. Partial finetuning saves memory but needs many trainable parameters (about 25% on BERT-large) to approach full quality.
16. Under a fixed trainable budget, cover more matrix types at low rank rather than one at high rank. If only two attention matrices, use query and value; adding the MLP matrices often gives the largest gain.
17. Rank 4 to 64 is usually enough; higher rank often adds nothing and can overfit. Keep alpha:r between 1:8 and 8:1, larger alpha for smaller r. Sweep both.
18. Short on memory: quantize the frozen base (QLoRA, NF4) rather than shrinking the adapter. QLoRA trades slower steps for memory.
19. One model: merge LoRA into the base for zero latency overhead. Many variants: keep adapters separate on one shared base.

**Merging**
20. For multi-task, avoid naive sequential finetuning (catastrophic forgetting); finetune per task in parallel from the same base and merge.
21. Prune redundant task-vector deltas (TIES, DARE) before merging, especially with three or more models. SLERP merges two at a time. Layer-stacked merges need further training. Avoid concatenation.

**Tactics**
22. Feasibility: use the strongest model you can afford. Then follow the progression path (cheap model for code, mid model for data, best model for quality, all sizes for the frontier) or the distillation path.
23. Learning rate: search 1e-7 to 1e-3, start near the end-of-pretraining LR times 0.1 to 1, lower it if loss swings, raise it if loss creeps. Batch size below about 8 is unstable; use gradient accumulation. Epochs: 1 to 2 for millions of examples, 4 to 10 for thousands; stop when validation loss rises. Prompt loss weight defaults to about 10%.

## Default workflow

1. Define metrics and build the evaluation pipeline.
2. Prompt systematically, then add 1 to 50 examples.
3. Add term-based RAG if failures are informational.
4. Classify remaining failures: informational leads to better retrieval, behavioral leads to finetuning.
5. Estimate memory with `scripts/finetune_memory.py`; pick full, LoRA or QLoRA to fit the hardware.
6. Choose base model, method, framework; size the LoRA with `scripts/lora_params.py`.
7. Debug on the cheapest model, then tune LR, batch, epochs from train and validation loss.
8. Evaluate against prompt-only and RAG baselines and on all traffic types; evaluate the quantized serving artifact.
9. Decide serving mode (merged vs multi-adapter) and, for several tasks, whether to merge.
10. Set a policy for re-evaluating when new base models ship.

## References

- [references/deciding-to-finetune.md](references/deciding-to-finetune.md): read when deciding whether to finetune at all, choosing between finetuning and RAG, or planning the prompt-to-finetune ladder.
- [references/memory-and-precision.md](references/memory-and-precision.md): read when sizing GPUs, explaining why training needs more memory, choosing FP32/BF16/FP16/INT8/INT4, or deciding between PTQ, QAT and mixed precision.
- [references/peft-and-lora.md](references/peft-and-lora.md): read when choosing among full, partial, adapter and soft-prompt methods, configuring LoRA targets, rank and alpha, serving many adapters, or using QLoRA.
- [references/model-merging.md](references/model-merging.md): read when combining models or adapters, doing multi-task finetuning, deploying on device, or choosing among linear, SLERP, TIES/DARE, layer stacking and concatenation.
- [references/finetuning-tactics.md](references/finetuning-tactics.md): read when picking the base model, development path, framework or API, setting hyperparameters, reading loss curves, or running the pre-launch and pre-ship checklists.
- [references/source-map.md](references/source-map.md): read to find which reference covers a given chapter section.

## Scripts

Both scripts use only the Python 3 standard library and print plain text. Run them from this skill's directory.

Run `finetune_memory.py` to compute GPU memory for inference, full, partial, LoRA or QLoRA training (weights, activations, gradients, optimizer states), optionally checking the fit against a GPU:

```
python3 scripts/finetune_memory.py --params 7B --gpu-gb 24
python3 scripts/finetune_memory.py --params 13B --mode full --optimizer adam --activation-factor 0
python3 scripts/finetune_memory.py --params 65B --mode qlora --trainable-fraction 0.005 --gpu-gb 48
```

Default mode `compare` prints inference, full, LoRA and QLoRA side by side. Useful flags: `--weight-format`, `--state-format`, `--trainable-params`, `--master-format fp32` (mixed-precision master copy).

Run `lora_params.py` to compute LoRA trainable parameters and adapter size from model dimensions, the largest rank within a parameter budget, and storage for N variants merged versus base plus adapters:

```
python3 scripts/lora_params.py --hidden 12288 --layers 96 --rank 2 --targets q,k,v,o --total-params 175B
python3 scripts/lora_params.py --hidden 4096 --layers 32 --rank 16 --targets q,k,v,o,gate,up,down --kv-dim 1024 --ffn-dim 14336 --total-params 8B --adapters 100
```

Treat outputs as back-of-the-envelope estimates; activation memory during training is a floor unless gradient checkpointing is on.
