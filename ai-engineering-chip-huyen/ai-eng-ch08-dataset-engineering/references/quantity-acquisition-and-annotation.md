# Data Quantity, Acquisition and Annotation

## Contents
- Sizing: the factors that set how much data you need
- Technique choice by data volume, and ossification
- The pilot experiment and how to read it
- Subset scaling curves
- Task count as a quantity dimension
- Staged finetuning to stretch scarce data
- Budget math
- Acquisition sources in order of preference
- Mix-and-match pipeline (worked example)
- Finding public datasets safely
- Annotation guidelines
- Glossary

## Sizing: the factors that set how much data you need

There is no universal number: reported runs range from one example to millions, and even millions are tiny next to pre-training (Llama 3 saw 16T tokens). Beyond quality and diversity, three factors move the requirement:
1. **Technique.** Full finetuning can give the best results, but its data needs exceed PEFT's by orders of magnitude.
2. **Task complexity.** Review sentiment needs far less than QA over financial filings.
3. **Base model distance.** Stronger base models start closer to the target and need fewer examples, the reverse of pre-training, where larger models are data-hungrier. In OpenAI's SNLI experiment, advanced models finetuned clearly better at 100 examples, but all five converged at 550,000.

## Technique choice by data volume, and ossification

| You have | Default |
|---|---|
| A few hundred to a few thousand pairs | PEFT on the strongest base model you can afford |
| Tens of thousands to millions of pairs | Consider full finetuning, possibly of a smaller model |
| Millions of pairs | Also evaluate training from scratch |

Why the last row: pre-training can ossify weights so they adapt poorly to a large finetuning set, and smaller models suffer more from this. Finetuning is usually more efficient than training from scratch, but with abundant data, measure rather than assume.

## The pilot experiment and how to read it

Before a large effort, finetune on about 50 carefully made examples.
- Target reached: done. Clear improvement: more data will likely help; fit a scaling curve.
- No improvement: a bigger set rarely rescues it, but first check learning rate and other hyperparameters, data quality and prompts. Most setups show a visible gain at 50 to 100 good examples, so a flat result often signals a bug.

## Subset scaling curves

Finetune on nested fractions of the current data (for example 25%, 50%, 100%) and plot the metric against size.
- Steep slope: doubling the data should pay off substantially.
- Flat slope: doubling buys little; spend on quality, diversity or a different technique.

Expect diminishing returns as the normal shape. Illustration: the first 1,000 examples add ten accuracy points, the next 1,000 add five. When projecting, fit a curve that bends (for example log-linear in size) rather than a straight line.

Worked projection: at 2K examples the metric is 61, at 4K it is 66, at 8K it is 69. Gains per doubling are 5 then 3. A further doubling to 16K is likely worth 1 to 2 points; if annotation costs $3 per example, that is $24K for under two points, so diversity or guideline fixes may be the better spend.

## Task count as a quantity dimension

Quantity is not just row count. In Flan scaling experiments, raising the number of distinct finetuning tasks from 9 to 282 produced large gains, and gains kept trickling in up to 1,836 tasks. Track diversity in task type, topic and output format as you grow the set; ten thousand rows of one task is a different asset from ten thousand rows across forty tasks.

## Staged finetuning to stretch scarce data

Lower-quality or less-relevant data can reduce how much premium data you need, by training in two stages:

| Pattern | Stage 1 | Stage 2 | Example |
|---|---|---|---|
| Self-supervised then supervised | raw domain documents | the few labeled pairs | legal QA with many statutes, few QA pairs |
| Adjacent task then target | related labeled task | target task | tweet sentiment, then product-review sentiment |
| Synthetic then real | large AI-generated set | small real set | medical report classification under privacy limits |

Warning for the third pattern: two separate jobs and the handoff between them are easy to mishandle. Done poorly, it spends more compute to reach a worse model than finetuning once on good data. Other ways to cut labeling demand include weak supervision, semi-supervision and active learning.

## Budget math

Money caps volume: $10,000 at $2 per example buys at most 5,000 examples, and every dollar on labels is one not spent on compute. Write the split down before collecting.

## Acquisition sources in order of preference

Goal: enough data of the needed quality and diversity, collected lawfully and with respect for privacy.

1. **Your own application.** Usually the most valuable source: only it matches your target distribution. Includes user content, usage-generated system data and feedback. A working data flywheel is a durable advantage.
2. **Existing datasets, open or proprietary.** Check marketplaces before creating anything. Often no single set fits, and you will combine several.
3. **Human annotation.** Targets exactly the behaviors you want, at the cost of guidelines, money and consistency risk.
4. **Synthesis.** Fills coverage gaps and privacy-constrained areas (see the synthesis reference).

## Mix-and-match pipeline (worked example)

Illustrative build of an (instruction, response) set for a contract-review assistant:
1. Find a promising open set of 20,000 legal QA pairs; confirm license and sub-source licenses.
2. Drop weak or off-task instructions: 16,000 remain.
3. Among those, flag 5,000 with good instructions but poor responses. 11,000 are fully good.
4. Paralegals rewrite the 5,000 responses: 16,000 good pairs.
5. Coverage review shows indemnity clauses are thin. Write 40 instruction templates for that gap and have an LLM expand them to 1,200 instructions (30 per template, deliberately modest to keep diversity).
6. Paralegals answer or verify the 1,200: final set of 17,200.

Expect hidden detours: guideline revisions and re-annotation, a second team to fact-check, or more templates with fewer generations each when diversity collapses.

## Finding public datasets safely

Where to look: Hugging Face, Kaggle, Google Dataset Search, government portals (data.gov, data.gov.in), ICPSR, UCI and OpenML, the Open Data Network, AWS Open Data, framework datasets (TensorFlow Datasets), Stanford SNAP for graphs, and evaluation harnesses (lm-evaluation-harness: 400+ benchmarks averaging 2,000+ examples, enough for PEFT).

Rules:
- Use public data, never trust it. Inspect and validate it like raw data.
- Read the license, then trace provenance. A dataset licensed for commercial use can still include a portion taken from a source that forbids it.
- If you train on benchmark data, remove it from your own evaluation, or your scores are contaminated.

## Annotation guidelines

Writing the guideline is often harder than annotating (LinkedIn called it one of its hardest pipeline steps). It must say what a good response looks like and why, whether correct-but-unhelpful is acceptable, what separates adjacent scores (with paired borderline examples), and how to handle ambiguous inputs. The same guideline serves human and AI annotators and doubles as the evaluation guideline, so evaluation items can also seed synthesis. Do not abandon careful annotation midway hoping the model infers intent; that is too risky for most applications.

## Glossary

- **Ossification**: pre-trained weights resisting adaptation to large finetuning sets; worse for small models.
- **Data flywheel**: loop where product usage yields training data that improves the product.
