# Model Merging and Multi-Task Finetuning

## Contents
- What merging is for
- Multi-task strategies compared
- On-device deployment and federated learning
- Merging versus ensembling
- Approach 1: summing (linear combination, task arithmetic, SLERP, pruning)
- Approach 2: layer stacking
- Approach 3: concatenation
- Merge playbook
- Glossary

## What merging is for

Finetuning customizes one model; merging builds one from several. You may finetune constituents before merging and optionally finetune the result. Without that last step, merging needs no GPU, which suits developers with little compute.

The goal is one model worth more than its constituents used separately, through:
- **Quality**: two models strong on different parts of a task combine into one stronger on the whole (one covers some questions, another a different overlapping set; the merge covers more).
- **Footprint**: two task models become one multi-task model with fewer parameters, especially natural for adapters on a shared base.

Many techniques are experimental and may age quickly, so think in the three approaches below rather than specific recipes. Merged models have often sat near the top of the Hugging Face Open LLM Leaderboard, as ensembles once did on older leaderboards.

## Multi-task strategies compared

| Strategy | How | Strength | Weakness |
|---|---|---|---|
| Simultaneous | One mixed dataset, one run | One model, no forgetting | Several skills at once usually need more data and training |
| Sequential | Task A, then B, then C | Each step is single-task | Catastrophic forgetting of earlier tasks |
| Parallel then merge | One finetune or adapter per task from the same base, then merge | Each task learned well; no sequential forgetting | Interference; merge quality must be verified |

Default with separate per-task data and modest compute: parallel finetunes on a shared base, then merge.

## On-device deployment and federated learning

Phones, laptops, cars, watches and warehouse robots have little memory, so one merged multi-task model beats shipping several. On-device inference matters when data must stay local, when connectivity is poor, and when you want inference cost on users' hardware instead of your data center.

Merging also implements federated learning: copies of one model learn separately from device data and are later merged into a new base, usually by averaging.

## Merging versus ensembling

| | Ensembling | Merging |
|---|---|---|
| Combines | Outputs (vote or learned combiner) | Parameters |
| Constituents | Kept intact | Fused |
| Inference cost | One call per constituent | One call |

Use ensembling when quality outweighs serving cost; merging when one cheap model is the goal.

## Approach 1: summing

Add constituent weights. Rescale first if one model's values are on a very different scale.

### Linear combination

Average or weighted average: merged = (wA x A + wB x B) / (wA + wB). Surprisingly effective, studied since the early 1990s, and standard in federated learning.
- Whole-model averaging: model soups averaged several finetuned models and improved accuracy at no inference cost.
- Component averaging, most commonly of adapters.
- Works best when constituents share a base. Then reason with **task vectors** (finetuned minus base; with LoRA, the adapter itself).
- **Task arithmetic**: add vectors to combine skills; subtract one to remove a capability, such as an invasive skill like face recognition or a pre-training bias. Confirm removals with targeted tests.
- Mismatched sizes can be handled by projecting layers into a shared dimension.
- Aligning parameters before averaging (optimal-transport fusion, Git Re-Basin, task-subspace matching) is sound in principle but hard, so naive averaging stays more common.

### SLERP

Treat each vector as a point on a sphere, trace the shortest surface path between them (like a great-circle flight route) and pick a point on it. Factor t in [0, 1]: below 0.5 leans to the first vector, 0.5 is the midpoint. Tools implement the math. SLERP takes exactly two inputs; for more, chain it (A with B, then with C), noting that order and factors change the result.

### Pruning redundant task-specific parameters

Most finetuning changes are tiny and contribute little. TIES-Merging showed most of a task vector can be reset to the base values with little loss; keeping about the top 20% of changes matched keeping all. The assumption is that the parameters that moved most matter most.

Redundant deltas are harmless alone but interfere once merged. TIES (trim, elect sign, merge) and DARE (drop and rescale) prune first and markedly improve merged quality. More constituents means pruning matters more. Pruning sparsifies task vectors, not the final model: it is for quality, not size or latency.

## Approach 2: layer stacking

Assemble a model by piling up layers drawn from different sources, for example layer 1 from model X and layer 2 from model Y. Practitioners call this passthrough merging or frankenmerging. The result may have a novel architecture or size, and unlike summing it usually needs further finetuning.

- **Frankenmerge**: Goliath-120B was assembled from Xwin and Euryale, both Llama 2-70B finetunes, using 72 of each one's 80 layers.
- **Sparse upcycling to MoE**: copy selected layers of a pretrained dense model several times, add a router that sends each input to the best copy, and keep training experts and router. This has beaten MoE models trained from scratch. The chapter also cites Together AI's Mixture-of-Agents, combining six weaker open models to rival GPT-4o on some benchmarks (it chains whole models, so it is closer to orchestration than weight merging).
- **Depthwise upscaling**: grow a bigger model cheaply, for instance after moving from 40 GB to 80 GB GPUs. SOLAR 10.7B came from a 32-layer 7B model: duplicate it, sum 16 selected layer pairs and stack the rest (32 x 2 minus 16 = 48 layers), then keep training. The number of summed layers sets the target size.

Approaches can be mixed: sum some layers, stack others.

## Approach 3: concatenation

Join parameters side by side; two LoRA adapters of rank r1 and r2 become one of rank r1 + r2. It might score slightly higher but saves no memory versus serving them separately, and the gain rarely justifies the parameters. Generally avoid.

## Merge playbook

1. Fix the goal: quality on one task, one model for several tasks, or a smaller deployment.
2. Prefer constituents from the same base, ideally LoRA adapters.
3. Compute task vectors.
4. With three or more constituents, prune deltas (TIES or DARE style).
5. Combine: two and smooth, SLERP with t swept over 0.3, 0.5, 0.7; several, weighted linear combination tuned on validation data; removing a behavior, subtract its vector; more capacity, stacking or upscaling plus training.
6. Rescale if magnitudes differ; optionally finetune the merged model briefly.
7. Evaluate every constituent task and general ability against the best single constituent and an ensemble baseline.

Example: three adapters on one 8B base (SQL, ticket triage, summarization) for a device that keeps one model resident. Prune each to its largest 20% of deltas, merge with weights 0.4/0.3/0.3, evaluate all three. If SQL drops too far, raise its weight or keep SQL as a separate adapter and merge only the other two.

Watch for: sequential finetuning without forgetting safeguards, unpruned many-way merges, unscaled sums, untrained stacked models, and trusting a leaderboard recipe without testing your own tasks.

## Glossary

- **Task vector (delta parameters)**: finetuned weights minus base weights.
- **Model soup**: average of several finetuned models' weights.
- **TIES / DARE**: merge methods that prune small or redundant deltas first.
- **Sparse upcycling**: dense model to MoE by copying layers and adding a router.
- **Depthwise scaling**: deepening a model by duplicating it and summing some layer pairs.
- **Catastrophic forgetting**: losing earlier skills when trained on new data.
