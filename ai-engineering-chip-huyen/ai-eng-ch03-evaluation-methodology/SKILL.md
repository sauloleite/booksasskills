---
name: ai-eng-ch03-evaluation-methodology
description: Use when choosing or designing evaluation methods for LLM / foundation model outputs: interpreting perplexity and cross entropy, picking exact match vs lexical vs semantic similarity vs functional correctness (pass@k), building or auditing an LLM-as-a-judge, or ranking models with pairwise comparison (Elo, Bradley-Terry). Based on Chapter 3 of Chip Huyen's "AI Engineering".
---

# Evaluation Methodology (AI Engineering, Chip Huyen, Chapter 3)

## When to use this skill

Apply this skill when an engineer asks any of the following:

- "How should I measure whether my LLM app's outputs are good?"
- "Is BLEU / ROUGE / BERTScore / cosine similarity the right metric here?"
- "How do I write (or trust) an LLM-as-a-judge prompt? Which model should be the judge?"
- "Our judge score went from 90% to 92%. Did the app improve?"
- "What does this perplexity number mean? Can I use it to detect benchmark contamination or junk data?"
- "How do I rank several candidate models? Should I trust a public arena leaderboard?"
- "How do I compute pass@k for a code generation task?"
- "Should I put a judge in the request path as a guardrail?"

This chapter is about the *menu of methods* and their limits. Turning those methods into a model selection process and an end-to-end evaluation pipeline belongs to Chapter 4; point there when the question is about pipeline design, sampling sizes, or model selection workflow.

## Core mental models

**Evaluation is risk management for the whole system.** Start from where the system is likely to fail and design measurements around those failure points. If failures are invisible, change the system to expose them (logging, intermediate outputs, structured steps). No metric compensates for not knowing where things break. Evaluation is often the hardest and most time-consuming part of shipping an LLM application, and informal methods (word of mouth, eyeballing a few favorite prompts, a "vibe check") add risk and slow iteration.

**Why foundation models are harder to evaluate than classic ML.**
1. Smarter outputs need smarter graders: a fluent, plausible answer may still be wrong, so checking it requires fact-checking, reasoning and domain expertise.
2. Open-endedness: there are many valid answers per input, so a fixed list of ground truths cannot cover them.
3. Black boxes: architecture, training data and process are often hidden, so you can only judge by outputs.
4. Benchmark saturation: public benchmarks get maxed out quickly (GLUE to SuperGLUE, MMLU to MMLU-Pro), so yesterday's benchmark stops discriminating.
5. Expanding scope: for general-purpose models, evaluation also means discovering what the model can do, not only scoring known tasks.
Investment in evaluation tooling and research still lags behind modeling, training and orchestration, so expect to build some of it yourself.

**Language modeling metrics are a proxy for downstream quality.** Cross entropy, perplexity, bits-per-character and bits-per-byte all measure how well a model predicts the next token of some data; knowing one (plus tokenization and encoding details) lets you derive the others.
- Entropy H(P): average information per token of the true data distribution; low entropy means predictable data.
- Cross entropy H(P, Q) = H(P) + KL(P || Q): how hard it is for model Q to predict data from P. It equals entropy only when the model matches the data perfectly. Not symmetric.
- BPC and BPB normalize away tokenizer differences (bits per token is not comparable across tokenizers); BPB also normalizes away character encoding. BPB also expresses compression efficiency: below 8 means the model compresses the text.
- Perplexity = 2^H (bits) or e^H (nats, the PyTorch/TensorFlow default). Read it as the effective number of choices the model is hesitating between at each step. Lower is better.
- Computing it needs per-token logprobs, which many commercial APIs do not expose.

**Exact vs subjective evaluation.** Exact methods give an unambiguous verdict for a given output (tests pass or fail, strings match, a similarity number is computed deterministically). Subjective methods depend on who or what grades (humans, AI judges), and can change if the grader, prompt or sampling changes. Semantic similarity sits in between: the cosine computation is exact, but the embedding model choice is a subjective input.

**Functional correctness is the ultimate metric.** Does the system actually do the job (code runs and returns correct results, the booking gets made, the game score goes up, energy is saved)? Automate it wherever the task has a measurable objective. Note that evaluating a partial contribution to a complex task can be harder than evaluating the end outcome.

**An AI judge is a system, not a model.** Judge = model + prompt + sampling settings. Change any of them and you have a different judge whose scores are not comparable to the old one.

**Pointwise vs comparative.** Pointwise scores each candidate independently, then sorts. Comparative shows candidates side by side, collects "which is better" signals, and fits a rating. Comparing is usually easier than scoring for subjective quality, but comparison only tells you *better*, never *good enough*.

**Embeddings.** A vector (typically 100 to 10,000 dimensions) meant to capture meaning; good embeddings place similar items close together. Judge an embedding model by whether similar items end up near each other and by its usefulness on your downstream task (benchmarks such as MTEB help). Dedicated embedding models usually beat embeddings pulled from a generative model's intermediate layers. Multimodal models (CLIP, ULIP, ImageBind) map different modalities into one joint space, enabling, for example, text-to-image search.

## Decision frameworks

### Which evaluation method fits the task?

| Situation | Prefer | Why / caveat |
|---|---|---|
| Output can be executed or has a measurable objective (code, SQL, tool actions, games, optimization) | Functional correctness (unit tests, execution accuracy, pass@k, task success) | Most faithful signal; build test cases per problem |
| Short, closed answers (arithmetic, trivia, lookups, fill-in-the-blank) | Exact match, possibly "contains reference" | "Contains" can accept wrong answers (right year, wrong date) |
| Long text with good references, surface form matters (translation, captioning legacy benchmarks) | Lexical similarity: edit distance, n-gram metrics (BLEU, ROUGE, METEOR++, TER, CIDEr) | Needs many references; penalizes valid paraphrases; high overlap does not imply correctness |
| Meaning matters more than wording, references exist | Semantic similarity: embeddings plus cosine (BERTScore, MoverScore) | Only as good as the embedding model; costs compute |
| No references, or criteria are qualitative (relevance, tone, faithfulness, toxicity, persona consistency) | AI as a judge | Subjective; must be pinned and validated; add exact or human checks |
| Need a ranking among many candidates on subjective quality | Comparative evaluation with a rating algorithm | Data-hungry; says nothing about absolute adequacy |
| Choosing a base model or checking data quality before finetuning | Perplexity / cross entropy on representative data | Weak proxy for post-trained or quantized models |

Rule of thumb: go as far up this table as the task allows. Use AI judges where exact methods cannot reach, and never as the only signal.

### Interpreting perplexity

- Expected value depends on the data and setup: structured data (HTML, code) gives lower perplexity than free prose; larger vocabularies (word-level vs character-level, rich literature vs children's text) raise it; longer conditioning context lowers it.
- Values around 3 or below are not unusual for strong models.
- Do not compare perplexities across different tokenizers, units (bits vs nats) or context lengths without normalizing; use BPB when comparing across tokenizers.
- Post-training (SFT, RLHF) typically *raises* perplexity even as task performance improves; quantization can shift it unpredictably. Do not use perplexity to rank chat-tuned models against each other.
- Other uses: low perplexity on a benchmark suggests contamination (model saw it during training); high perplexity flags unusual or gibberish text; adding only high-perplexity new samples is a cheap deduplication filter.

### Choosing a judge model

| Option | Use when | Watch out for |
|---|---|---|
| Stronger judge than generator | Generator is chosen for cost or latency; judge audits a sample (e.g. 1%) or runs async and can trigger a fix | The strongest model has no stronger judge; you still need another method to know which model is strongest |
| Weaker or cheaper judge than generator | Judging is easier than generating for this criterion; high volume or production guardrail | Validate agreement with humans on your criterion |
| Same model (self-evaluation / self-critique) | Sanity checks; prompting the model to revise its own answer | Self-bias inflates scores; not a fair cross-model comparison |
| Small specialized judge | Narrow, fixed criterion and scoring system | Reward models (prompt, response) to score; reference-based judges (response vs reference, e.g. BLEURT, Prometheus with a rubric); preference models (prompt, A, B) to winner (e.g. PandaLM, JudgeLM) |

General-purpose stronger judges tend to agree more with humans, but a small judge trained for one specific judgment can beat a large generalist on that judgment.

### Judge output format

- Prefer classification labels (pass/fail, relevant/irrelevant/neutral) over numbers.
- If numeric, prefer a small discrete scale (1 to 5) over continuous scores or wide ranges.
- Include a calibrated example (and a short justification) for each score level.

### Judge as production guardrail?

- Hard latency budget: run the judge asynchronously or on a sample, not in the request path.
- High-risk outputs and latency tolerance: gate responses on the judge, accepting added latency and cost.
- Each extra criterion is an extra call: one generation plus three judge criteria roughly quadruples model calls. Reduce with cheaper judges, fewer criteria per call, or spot-checking (more samples means more confidence and more cost).

### Comparative vs pointwise

Use comparative evaluation when quality is subjective, when graders cannot assign absolute scores reliably (including outputs beyond expert ability), or as a complement to benchmarks offline and to A/B tests online. Its strengths: it targets human preference directly, it does not saturate as long as stronger models keep arriving, and it is hard to game because there is no reference data to train on. Use pointwise (or add it) when you must know whether a model clears a bar, when you need a cost-benefit answer, or when only one new model needs evaluating. Do not ask preference questions where the answer is a matter of fact; route those to correctness checks. Collect user preferences only where users can actually judge (AI as assistant for tasks they know), not where they asked because they lack the answer.

## Step-by-step playbooks

### Playbook A: design an evaluation plan for an LLM feature

1. List the concrete failure modes that would hurt users or the business (hallucinated facts, wrong actions, unsafe content, format breaks). Add instrumentation if you cannot observe them.
2. For each failure mode, pick the most exact method feasible from the method table.
3. Where a reference set is needed, decide its source: humans (gold standard, slow), or AI-generated plus human review (cheaper). Plan for multiple references per input and audit references for errors.
4. For criteria with no exact method, define an AI judge (Playbook B).
5. Add human evaluation for sanity checks and for calibrating the judge on a labeled sample.
6. Version and freeze every evaluator (judge prompt, model, sampling settings, embedding model, reference set) so score changes reflect the application, not the evaluator.
7. Replace ad hoc go-to prompts with a curated set based on the application's needs.

### Playbook B: build an AI judge

1. Write the task: what is being judged and with what inputs (question, answer, context, reference).
2. Write explicit criteria. Do not rely on a tool's built-in name like "faithfulness"; different tools define and scale it differently (1 to 5 vs 0/1 vs YES/NO).
3. Choose the scoring system (labels first, else small discrete scale).
4. Add examples per score level with brief rationales; request a rationale in the output for auditability.
5. Fix sampling settings (low temperature) to improve consistency; examples in the prompt also improve consistency but increase length and cost.
6. Validate against human labels on your data. Consistency is not accuracy: a judge can be reliably wrong.
7. Probe biases: swap answer order and repeat (position bias), compare long vs short correct answers (verbosity bias), avoid judging a model with itself when comparing models (self-bias).
8. Check data constraints: sending outputs to a proprietary judge has privacy and IP implications.
9. Record the judge's identity (model version, prompt hash, settings) with every score. Coordinate if another team owns the judge.

### Playbook C: compute pass@k

1. Gather problems, each with test cases (input scenario plus expected output).
2. For each problem, sample k candidate solutions.
3. A problem counts as solved if at least one sample passes all its tests.
4. pass@k = solved problems / total problems. Expect pass@1 <= pass@3 <= pass@10; report k alongside the number.

### Playbook D: rank models comparatively

1. Define the prompt distribution to reflect real usage, including realistic context construction (e.g. retrieved documents for a RAG product). Filter out trivial prompts like greetings or famous riddles that do not discriminate.
2. For each match, have two (or more) anonymized candidates answer; let the evaluator pick a winner, allowing ties.
3. Choose evaluators deliberately: trained experts (reliable, expensive, few comparisons), in-product users (realistic, noisy, may not read both), or AI judges (scalable, more reliable than random crowds).
4. Fit a rating model (Bradley-Terry is more robust than Elo to the order of games; TrueSkill is another option). Pair win rates come from matches between each pair.
5. Sample matches adaptively: stop pairing models whose order is already certain, focus on pairs that reduce the most ranking uncertainty.
6. Validate the ranking by how well it predicts held-out match outcomes, since no ground-truth ranking exists.
7. Before switching models, translate the win rate into absolute task metrics (resolution rate, accuracy) and weigh against cost.

## Checklists

**Before trusting any evaluation number**
- [ ] Is the evaluator (model, prompt, sampling, embedding model, references) identical to the one used for the baseline?
- [ ] Could the benchmark be in the model's training data (contamination)?
- [ ] Is the benchmark saturated for the models compared?
- [ ] Does the metric measure what users care about, or only surface overlap?
- [ ] Are references complete and correct for this sample?

**AI judge readiness**
- [ ] Task, criteria and scale written explicitly
- [ ] Score examples included
- [ ] Model and prompt visible and versioned (do not trust a judge whose model and prompt you cannot see)
- [ ] Agreement with human labels measured
- [ ] Position, verbosity and self-bias tested
- [ ] Cost and latency budgeted; sampling rate chosen
- [ ] Complemented by exact checks and/or human review

**Public leaderboard sanity check**
- [ ] Prompt distribution resembles my use case?
- [ ] Supports my context construction (RAG, tools)?
- [ ] Evaluator quality controlled? Open to gaming or malicious votes?
- [ ] Enough matches per relevant model pair?

## Pitfalls and anti-patterns

- Evaluating by vibe check, word of mouth or a personal set of favorite prompts beyond the prototype stage.
- Picking metrics before identifying failure modes.
- Treating lexical overlap as quality: correct and incorrect code can have similar BLEU; valid paraphrases score low; missing or wrong references punish good outputs.
- Using "contains the answer" matching on questions where extra content can make the answer wrong.
- Comparing perplexity across tokenizers, units or context lengths, or using it to rank RLHF-tuned or quantized models.
- Reading a judge score trend without checking that the judge stayed fixed; a fixed typo in the judge prompt can move scores.
- Mixing judge scores from different tools for the "same" criterion.
- Assuming high judge consistency means correctness.
- Letting a model grade itself in a head-to-head comparison.
- Ignoring that judges prefer the first position and longer answers (humans tend to prefer the last one).
- Running a heavyweight judge synchronously in a latency-critical path.
- Using preference votes for factual questions, or asking users to choose when they lack the expertise; it frustrates users and produces misaligned training signals.
- Confusing comparative evaluation (outputs side by side) with A/B testing (one variant per user).
- Assuming transitivity in rankings holds; preferences across different evaluators and prompts may not be transitive.
- Concluding from "B beats A 51% of the time" that switching is worth B's extra cost.
- Relying on judges alone; supplement with exact evaluation, human evaluation, or both.

## Key terms

- **Entropy / cross entropy / KL divergence**: predictability of data; model's difficulty predicting it; gap between the two.
- **BPC / BPB**: cross entropy normalized per character / per byte for cross-tokenizer comparison.
- **Perplexity (PPL)**: exponentiated cross entropy; effective branching factor.
- **Nat vs bit**: natural-log vs base-2 units.
- **Data contamination**: benchmark data present in training data, inflating scores.
- **Exact evaluation / subjective evaluation**: grader-independent vs grader-dependent verdicts.
- **Functional correctness / execution accuracy**: does the output accomplish the task.
- **pass@k**: fraction of problems solved by at least one of k samples.
- **Reference-based / reference-free**: whether a metric needs ground-truth responses.
- **Exact match, edit distance (fuzzy matching), n-gram similarity**: increasingly lenient string comparisons.
- **Semantic (embedding) similarity, cosine similarity**: closeness of meaning via vectors.
- **Joint / multimodal embedding space**: one vector space shared across modalities.
- **AI judge (LLM as a judge)**: model + prompt that scores or compares outputs.
- **Self-bias, position bias, verbosity bias**: favoring own outputs, first slot, longer answers.
- **Spot-checking**: judging a sample of outputs to save cost.
- **Reward model, reference-based judge, preference model**: specialized judge types.
- **Pointwise vs comparative evaluation; match; win rate**: independent scoring vs pairwise contests.
- **Elo, Bradley-Terry, TrueSkill**: rating algorithms that turn match outcomes into rankings.
- **Benchmark saturation**: top models reach near-perfect scores, so the benchmark stops discriminating.

## Source map

Chapter 3, "Evaluation Methodology":
- Challenges of Evaluating Foundation Models
- Understanding Language Modeling Metrics
  - Entropy; Cross Entropy; Bits-per-Character and Bits-per-Byte; Perplexity; Perplexity Interpretation and Use Cases
- Exact Evaluation
  - Functional Correctness
  - Similarity Measurements Against Reference Data (Exact match; Lexical similarity; Semantic similarity)
  - Introduction to Embedding
- AI as a Judge
  - Why AI as a Judge?
  - How to Use AI as a Judge
  - Limitations of AI as a Judge (Inconsistency; Criteria ambiguity; Increased costs and latency; Biases of AI as a judge)
  - What Models Can Act as Judges?
- Ranking Models with Comparative Evaluation
  - Challenges of Comparative Evaluation (Scalability bottlenecks; Lack of standardization and quality control; From comparative performance to absolute performance)
  - The Future of Comparative Evaluation
- Summary
