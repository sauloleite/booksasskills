# PEFT, LoRA and QLoRA

## Contents
- Full, partial and parameter-efficient finetuning
- The PEFT landscape: adapters and soft prompts
- LoRA mechanics in brief
- Why low-rank updates work
- Configuring LoRA: targets, rank, alpha
- Serving LoRA: merged versus separate adapters
- LoRA's drawbacks
- Quantized LoRA (QLoRA)
- Method selection table
- Worked examples
- Glossary

## Full, partial and parameter-efficient finetuning

**Full finetuning** trains every parameter, like pre-training but from trained rather than random weights. Its memory cost and appetite for annotated data put it out of reach for most teams at foundation-model scale.

**Partial finetuning** freezes most layers and trains the rest, usually those nearest the output because they are the most task-specific. Freezing nine of ten layers cuts trainable parameters to 10%. It is parameter-inefficient: on BERT-large and GLUE about a quarter of parameters had to train to approach full-finetune quality.

**PEFT** targets near full-finetune quality with orders of magnitude fewer trainable parameters; there is no formal threshold. It began with Houlsby et al. (2019), who inserted two small adapter modules per BERT block, froze everything else, and came within 0.4% of full finetuning on GLUE while training about 3% of parameters. The price was extra inference latency, since adapters are additional layers.

PEFT is also sample-efficient: where full finetuning can require from tens of thousands up to millions of examples for a clear gain, some PEFT methods do well with a few thousand.

## The PEFT landscape: adapters and soft prompts

**Adapter-based (additive) methods** add trainable modules beside frozen weights: LoRA (by far the most used), BitFit (contemporary with LoRA), IA3 (efficient mixed-task batching, attractive for multi-task finetuning, reported to beat LoRA and sometimes full finetuning), and LongLoRA (LoRA plus attention changes for longer context).

**Soft-prompt methods** prepend trainable continuous vectors to the input instead of changing the architecture. Unlike hard prompts they are not readable and are trained by backpropagation. Variants differ mostly in insertion point: prompt tuning at the embedded input only, prefix tuning at every layer, P-Tuning a related variant. PEFT libraries implement them all. They suit teams wanting more control than prompting without weight finetuning.

An October 2024 count of open issues in the Hugging Face PEFT repository showed LoRA far ahead, with soft prompts small but growing.

## LoRA mechanics in brief

For W (n x m) pick rank r and train A (n x r) and B (r x m); the adapted weight is W + (alpha / r) x AB. AB has W's shape, so it can be folded into W after training, which is why merged LoRA adds no inference latency, unlike the original adapters. Parameters per matrix: r x (n + m) instead of n x m. A 4096 x 4096 matrix (16.8M weights) at rank 8 trains 65,536. On GPT-3, LoRA matched or beat full finetuning on several tasks with about 4.7M trainable parameters (0.0027%). Low-rank factorization is lossy; higher rank keeps more expressiveness.

## Why low-rank updates work

Why should adapting a model need so few parameters and examples when building it needed billions of both? The intrinsic-dimension argument (Aghajanyan et al. 2020, among others): pre-training implicitly pushes models toward low intrinsic dimension, and larger models end up lower. Pre-training acts as compression for downstream tasks, so the better trained the model, the smaller the update needed.

Low-rank pre-training has worked at small scale (SqueezeNet matched AlexNet with about 50 times fewer parameters; ReLoRA up to 1.3B transformers; GaLore matching full rank at 1B, promising at 7B). If the compression argument holds, some full-rank pre-training is still needed before low-rank updates suffice; how much remains open.

Practical consequence: LoRA works best on strong, well-pretrained bases.

## Configuring LoRA: targets, rank, alpha

**Targets.** Mostly used on transformers (some CNN work exists). Typical candidates are the attention projections (query, key, value, output), applied uniformly across layers. What is available depends on the architecture, so read the model's paper for its weight layout.

Evidence for spending a fixed budget:
- GPT-3 175B with an 18M budget (0.01% of the model) could afford rank 8 on one matrix type, rank 4 on two, or rank 2 on all four. Rank 2 on all four scored best on WikiSQL and MultiNLI.
- Limited to two attention matrices, query and value are usually best.
- Adding the feedforward matrices tends to help more: Databricks got its biggest gain from LoRA on all feedforward layers. Other work finds feedforward and attention LoRA complementary, with attention LoRA more efficient when memory is tight.

Heuristic: cover more matrix types at low rank before raising rank on a few.

**Rank.** Roughly 4 to 64 suffices for many cases. The LoRA authors saw no gain from higher rank, Databricks saw quality flatten, and higher rank can overfit; yet one practitioner found r = 256 best on his tasks. Some hosted services cap rank (one at 32), likely for hardware reasons, not quality.

**Alpha.** Scales the adapter through alpha / r. Ratios alpha:r between 1:8 and 8:1 are common; smaller r tends to want relatively larger alpha. Sweep (r, alpha) jointly.

Starting grid: all attention projections (add MLP if memory allows); r in {8, 16, 32}; alpha in {r/2, r, 2r}; select on validation metrics.

## Serving LoRA: merged versus separate adapters

| Option | How | Latency | Best for |
|---|---|---|---|
| Merge | Compute W + (alpha/r)AB offline, serve the result | None added | One finetuned model |
| Keep separate | Serve W once; apply A, B per request | Some, reducible with optimized kernels | Many variants on one base |

Storage for 100 customer variants of one 4096 x 4096 matrix at rank 8: merged is 100 full copies (about 1.68B parameters); separate is one base plus 100 small pairs (about 23.3M). Switching customers loads a small adapter instead of full weights. Apple served several iPhone features from one roughly 3B on-device base with per-feature LoRA adapters, quantizing base and adapters to fit. Adapters are shareable: search Hugging Face (tags adapter, peft, LoRA) or AdapterHub before training.

## LoRA's drawbacks

- It usually does not reach full finetuning's best quality.
- Applying it means modifying model code, which needs architectural understanding. Hugging Face PEFT, Axolotl, unsloth and LitGPT handle popular models; obscure ones may need custom work.

## Quantized LoRA (QLoRA)

Shrinking the adapter is the wrong lever. A 13B base at 16-bit is 26 GB; a low-rank adapter on a couple of attention matrices is single-digit megabytes, and even GPT-3 175B (350 GB) gets a rank-2, four-matrix adapter under 40 MB. Quantize the base instead.

QLoRA (Dettmers et al., 2023) stores frozen weights in 4-bit NF4 (levels placed for roughly normal, zero-centered weights), dequantizes to BF16 for forward and backward computation, and uses paged optimizers that spill to CPU memory under pressure, especially with long sequences. It made finetuning a 65B model on one 48 GB GPU possible. Its Guanaco models (7B to 65B) were competitive in May 2023: by GPT-4's judgment the 65B ranked below GPT-4 but was often preferred to ChatGPT.

Limitation: NF4 conversion is costly, so steps can be slower than LoRA. Other quantized LoRA work: QA-LoRA, ModuLoRA, IR-QLoRA.

## Method selection table

| Situation | Choose |
|---|---|
| First project, modest GPU | LoRA |
| LoRA on a 16-bit base does not fit | QLoRA, accept slower steps |
| Few hundred examples | PEFT; full may not beat LoRA |
| Large high-quality data and LoRA plateaued | Full finetuning |
| Many per-customer or per-feature variants | LoRA with multi-LoRA serving |
| Multi-task with mixed batches | Consider IA3 |
| Longer context | LongLoRA or long-context finetuning; test short inputs |
| More than prompting, no weight training | Soft prompts |

## Worked examples

**Budget allocation.** 32 layers, hidden 4096, grouped-query attention (key/value width 1024), FFN width 14,336. Rank 16 on q and v: 32 x 16 x (8192 + 5120), about 6.8M. Rank 16 on all seven projections: about 41.9M (84 MB in BF16), about 0.5% of an 8B model. Check with `scripts/lora_params.py`.

**Multi-tenant SaaS.** 200 customers on one 8B base. Full finetunes: 200 x 16 GB. LoRA at about 80 MB each: 16 GB of base plus 16 GB of adapters, loaded per request.

**70B on one 80 GB GPU.** A 16-bit base alone is 140 GB, so plain LoRA fails. NF4 base is about 35 GB, leaving room for adapters, their states and checkpointed activations: choose QLoRA.

## Glossary

- **Additive method**: PEFT that adds modules rather than editing existing weights.
- **Soft prompt**: trainable continuous vectors fed with the input.
- **Intrinsic dimension**: size of the smallest subspace where useful updates exist.
- **Multi-LoRA serving**: one resident base, many swappable adapters.
- **NF4 / paged optimizer**: 4-bit normal-aware format / optimizer state that spills to CPU.
