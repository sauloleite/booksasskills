# Public benchmarks, leaderboards, and data contamination

## Contents
- What public benchmarks are for
- Evaluation harnesses
- Benchmark selection and aggregation
- How public leaderboards are built and where they fall short
- Benchmark correlation
- Aggregation methods
- Building a custom leaderboard from public benchmarks
- Interpreting "the model got worse" reports
- Data contamination: how it happens
- Detecting and handling contamination
- Leaderboard review checklist
- Worked example
- Pitfalls
- Glossary

## What public benchmarks are for

Public benchmarks weed out weak models but do not find the best one for you: they rarely match your needs and are likely contaminated. Use them to shortlist, then decide with your own pipeline.

## Evaluation harnesses

Thousands of benchmarks exist (one suite bundles over two hundred) and saturation keeps spawning more. Harnesses run hundreds of them from one tool; use one when a shortlisted model lacks a score you need. Budget for it: a full holistic suite over about 30 models cost an estimated 80 to 100 thousand dollars (API fees plus about 19,500 GPU hours), growing with models and benchmarks.

## Benchmark selection and aggregation

Two questions define a leaderboard: which benchmarks, and how to combine them. If A beats B on coding but loses on toxicity, or wins one coding benchmark and loses another, the ranking depends on choices you must make explicitly.

## How public leaderboards are built and where they fall short

- **Compute limits coverage**, so expensive benchmarks get dropped (a retrieval benchmark omitted from one lite suite; a code benchmark skipped because it needs many sampled completions).
- **Small, shifting sets.** A major open leaderboard went from four benchmarks to six, then swapped all of them within a year as they saturated (toward competition math, a harder knowledge test, graduate-level Q&A, multistep reasoning, instruction following).
- **Opaque, divergent choices.** Two prominent leaderboards of the same period shared only two benchmarks; why law and medicine but no general science, or math but no code, was rarely explained. Transparency has since improved.
- **Common shape:** a few benchmarks spanning reasoning, factual consistency, math and science; rarely summarization, tool use, toxicity or retrieval.
- **Implication:** a top-ranked model will likely, not reliably, suit you; a board without code benchmarks says little about code.

## Benchmark correlation

- Perfectly correlated benchmarks are redundant; strongly correlated ones amplify the same bias.
- On one six-benchmark board, three reasoning-heavy benchmarks correlated at about 0.87 to 0.90, while truthfulness correlated only 0.42 to 0.55 with the others: better reasoning does not buy truthfulness.
- Compute the correlation matrix across candidates before trusting an average.

## Aggregation methods

| Method | How it works | Weakness |
|---|---|---|
| Plain average | Mean of raw scores | Treats scores of unequal difficulty as equal (80% on a hard truthfulness test is not 80% on easy math) and weights all tasks equally |
| Mean win rate | For each scenario, the fraction of other models this model beats; averaged across scenarios | Depends on which models are in the pool |
| Weighted, normalized score | Normalize each benchmark (different metrics such as accuracy, F1, BLEU), then weight by importance to you | Requires you to state weights explicitly, which is the point |

## Building a custom leaderboard from public benchmarks

1. List needed capabilities from the criteria sheet.
2. Collect recent benchmarks for each (code for a coding agent, creative writing for a writing assistant).
3. Vet reliability: anyone can publish one, and many miss what their name claims. Read items.
4. Gather scores, checking how they were produced; run missing ones with a harness.
5. Drop or down-weight near-duplicates by correlation.
6. Normalize metrics and weight by importance.
7. Combine with cost and latency into a shortlist; move it to private evaluation.

## Interpreting "the model got worse" reports

Users often report regressions after updates, and a 2023 study measured large shifts for two flagship models over three months. Either evaluation is hard even for providers, or (more plausibly) an update raised the average while hurting specific uses. Either way, the best overall model is not necessarily best for you. Anecdotes are not laws: one version migration cut a company's intent-classification accuracy by about 10% while improving another's support bot. Pin versions and rerun private evaluation on every update.

## Data contamination: how it happens

Contamination (leakage, training on the test set) means the model saw evaluation data in training, so scores overstate ability. A satirical paper trained a one-million-parameter model only on benchmark data and beat far larger models on them.

Routes:

- **Accidental web scraping:** benchmarks published before a model's training cut-off are probably in its training data. This is a major reason benchmarks saturate quickly; a benchmark starts losing value once it becomes public.
- **Shared sources:** training and evaluation drawn from the same material (practice problems from the same textbooks in both).
- **Deliberate, with good intent:** select the best checkpoint using held-out benchmarks, then train further on that high-quality benchmark data before release. The released model is better for users but can no longer be fairly scored on those benchmarks.
- **Deliberate, to inflate scores:** exists, but less common than the accidental kinds.

Consequence: a high bar-exam score may reflect exposure to bar-exam questions, not legal competence.

## Detecting and handling contamination

| Detector | How | Pros | Cons |
|---|---|---|---|
| N-gram overlap | Flag an eval example as dirty if a long token span (13 tokens is a common choice) also appears in training data | More accurate | Needs the training data; comparing every example against the full corpus is slow and expensive |
| Perplexity | Unusually low perplexity on eval items suggests the model has seen them | Cheap; needs only the model | Less accurate; needs logprob access |

Handling, by role:

- **Model developers:** strip the benchmarks you care about from training data before training. When reporting a score, state what fraction of the benchmark appeared in training and give scores on both the full set and the clean subset. Many skip this because it is laborious. A well-known early analysis found 13 benchmarks with at least 40% of items present in training data.
- **Why not remove everything:** most practitioners do not control foundation model training data; benchmark data can genuinely improve models; and new benchmarks created after training will always be contaminated by later models.
- **Leaderboard hosts:** plot score spreads (standard deviations) to spot outliers; benchmark creators should keep a private held-out split with an automatic scoring service.
- **Consumers:** use public scores only as a filter, prefer benchmarks with private splits, distrust sudden outliers, and confirm on private data the model cannot have seen.

## Leaderboard review checklist

- [ ] Does it include benchmarks for the capabilities I need?
- [ ] Are the benchmarks recent and unsaturated?
- [ ] Were important but expensive benchmarks omitted?
- [ ] Are several benchmarks highly correlated, double-counting one skill?
- [ ] How are scores aggregated, and does that weighting match my priorities?
- [ ] Is there evidence or disclosure about contamination?
- [ ] Do the scores come from a reliable, reproducible setup?

## Worked example

A team compares three open models for SQL generation. A general leaderboard ranks X first but has no code or SQL benchmark. Their custom board uses two recent text-to-SQL benchmarks (one with efficiency scoring), a low-weight reasoning benchmark, and an instruction-following benchmark for format; Y lacks a published SQL score, so they run it with a harness. The two SQL benchmarks correlate at 0.95, so they merge them. An n-gram check of their private SQL set against a public dump two candidates trained on flags 18% of items, so they report clean-subset scores: Y wins, and X's lead came mostly from dirty items.

## Pitfalls

- Choosing a leaderboard winner without checking capability fit or benchmark correlation.
- Ignoring contamination for benchmarks older than the model.

## Glossary

- **Saturation:** top models max out a benchmark so it no longer separates them.
- **Dirty example / clean subset:** eval items found in training data vs those with no detected overlap.
- **Private hold-out:** unreleased benchmark split scored by its owner.
