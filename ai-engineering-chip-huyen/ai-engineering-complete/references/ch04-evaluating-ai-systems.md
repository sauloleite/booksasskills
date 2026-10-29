---
name: ai-eng-ch04-evaluating-ai-systems
description: Use when defining evaluation criteria for an LLM application, choosing between foundation models, deciding API vs self-hosting, interpreting public benchmarks or leaderboards, checking for data contamination, or designing an evaluation pipeline (rubrics, eval sets, sample sizes, slicing). Based on Chapter 4 of Chip Huyen's "AI Engineering".
---

# Chapter 4: Evaluating AI Systems (AI Engineering, Chip Huyen)

Three jobs: deciding what to measure, picking a model, and building an evaluation pipeline that keeps steering development after launch. Methods from the previous chapter (exact match, functional correctness, similarity, AI as a judge, perplexity) are assumed; here the question is which method serves which criterion.

## When to use this skill

- A team is about to build an LLM feature and has not written down how success will be judged.
- Someone asks "which model should we use?" or "is model X better than Y for us?"
- A team is weighing a commercial model API against hosting an open weight model.
- A benchmark score or leaderboard rank is being used as the main argument for a model.
- You need to detect or measure hallucination, toxicity, instruction adherence, or persona consistency.
- You must decide how big an evaluation set should be, or whether a measured improvement is real.
- An evaluation pipeline exists but its results are noisy, untrusted, or disconnected from business outcomes.

## Core mental models

**Evaluation-driven development.** By analogy with test-driven development, define how the application will be judged before building it. A deployed system whose quality nobody can measure is arguably worse than one never shipped: it costs money to run and is risky to remove. The applications that dominate production (recommenders, fraud detection, coding, classification-like tasks) are the ones with measurable outcomes. The author sees evaluation as the largest bottleneck to AI adoption; better pipelines unlock use cases that are currently too hard to judge. Caveat: only building what is easy to measure is like searching for lost keys under the streetlight.

**Four buckets of criteria.** For any application, sort requirements into:
1. Domain-specific capability (does the model know the domain: code, law, Latin, math).
2. Generation capability (is open-ended output faithful, relevant, coherent, safe).
3. Instruction-following capability (does it obey format, length, content, style, persona constraints).
4. Cost and latency (can you afford it and will users wait for it).

**Close-ended vs open-ended measurement.** Domain knowledge and reasoning are usually measured with close-ended tasks (multiple choice, classification) because they are cheap to verify, reproducible, and have a known random baseline (25% with four options). But choosing the right option is a discrimination skill, not a generation skill, so multiple-choice scores say little about summarization, translation or writing quality. Multiple-choice results are also fragile: trivial formatting changes (an extra space, a "Choices:" label) can flip answers.

**Correct is not the same as efficient or readable.** Functional correctness is the default for code, but generated code or SQL that is slow, memory hungry, or unreadable may still be unusable. Efficiency can be measured exactly (runtime, memory, compared with a reference solution, as BIRD-SQL does); readability usually needs a subjective judge.

**Old NLG metrics, new priorities.** Fluency and coherence mattered when models wrote awkward text; strong models have mostly solved them, though they remain useful for weak models, creative writing and low-resource languages (measure with an AI judge or perplexity). The pressing generative concerns now are factual consistency and safety. Other app-specific qualities (controversiality, friendliness, conciseness) can be measured with the same techniques.

**Local vs global factual consistency.** Local: is the output supported by a supplied context (summaries, policy-bound support bots, data analysis, RAG answers)? Global: is it true against open world knowledge (general chatbots, fact-checking, market research)? Local checks are far easier. For global checks, the hard part is deciding what counts as fact and which sources to trust; beware treating "no evidence found" as "evidence of absence." Models judging evidence tend to weight topical relevance over credibility signals that humans value.

**Instruction following is entangled.** A failure can mean the model lacks the skill (cannot write a given verse form) or misunderstood the instruction, and a bad prompt can masquerade as a bad model. Two reference designs: IFEval checks automatically verifiable constraints (keywords, word counts, bullet counts, JSON, language) and scores the fraction satisfied; INFOBench extends to content, linguistic and style constraints, decomposing each instruction into yes/no criteria and scoring the fraction of criteria met. Strong LLM judges answered those yes/no checks better than crowdworkers, though worse than experts.

**Roleplay is instruction following with two axes.** Judge style (does it sound like the character) and knowledge (does it know what the character knows, and not what it would not know). The negative-knowledge check matters, for example game characters must not leak spoilers.

**Pareto thinking for cost and latency.** Quality, cost and latency trade off. Identify which objectives are non-negotiable, filter on them first, then optimize the rest. Latency has several metrics (time to first token, time per output token, time between tokens, total time per query) and depends on prompt and output length, not only the model. Users always say they want lower latency, but it is often an annoyance rather than a deal breaker.

**Cost curves differ by hosting mode.** API pricing is per token and roughly flat with scale. Self-hosting is mostly fixed compute, so per-token cost drops as utilization rises; teams therefore pick the biggest model that fits their GPU memory (common sizes: 16, 24, 48, 80 GB). Re-evaluate build vs buy at each scale step.

**Hard vs soft attributes.** Hard attributes cannot or will not be changed (license, training data, model size, privacy policy, control requirements). Soft attributes can be improved (accuracy, toxicity, factual consistency). The same attribute can be either: latency is soft if you serve the model, hard if someone else does. Estimating how much a soft attribute can improve is genuinely uncertain: task decomposition can lift a weak result dramatically, while some models never become usable.

**Best model vs best model for you.** Leaderboards answer the first question; your own pipeline answers the second. Provider updates can help one application and hurt another.

**Data contamination.** A model evaluated on data it trained on scores higher than it deserves. It is mostly accidental (web scrapes include published benchmarks; train and test drawn from the same source) and sometimes deliberate for good reasons (training on benchmark data after model selection to improve the released model). A benchmark loses value once public, which is why benchmarks saturate and get replaced.

## Decision frameworks

### Which evaluation method for which criterion

| Criterion | First choice | Alternatives / notes |
|---|---|---|
| Domain knowledge, reasoning | Close-ended benchmark, accuracy | Point-weighted scoring for hard or multi-answer items; F1, precision, recall for classification |
| Code / SQL | Functional correctness (execution) | Add runtime and memory vs reference; AI judge for readability |
| Fluency, coherence | AI judge | Perplexity via logprobs |
| Local factual consistency | AI judge given context and output | Entailment classifier (premise, hypothesis to entail/contradict/neutral); cheap and specialized |
| Global factual consistency | Search-augmented verification (decompose into atomic claims, make each self-contained, query search, judge each) | Self-consistency sampling (generate N extra answers, measure agreement); accurate but costly |
| Safety, toxicity, bias | Small specialized moderation/toxicity classifier | General AI judge or provider moderation endpoint; slower and pricier |
| Format constraints | Programmatic checks (regex, JSON parse, counts) | |
| Content / style constraints | Yes/no criteria per instruction, scored by AI judge or human | |
| Roleplay | Heuristics where possible (e.g. response length for a terse persona) | AI judge on style and knowledge |
| Relevance to query | Semantic similarity | AI judge |
| Classifier confidence | Logprobs over the label set | Flat distribution means low confidence |

### Model API vs self-hosting (seven axes)

| Axis | Leans API when... | Leans self-host when... |
|---|---|---|
| Data privacy | Policy allows external processing (some firms trust big clouds but not startups) | Data cannot leave the org or the country; fear of provider training on your data, plus memorization risk |
| Data lineage / copyright | You want contractual indemnity from a provider | You need inspectable training data (fully open models), knowing such inspection is hard in practice |
| Performance | You need frontier capability (best models tend to stay closed, since providers keep their best behind APIs and open models lack user feedback) | A smaller open model is good enough |
| Functionality | You want scaling, function calling, structured output, guardrails out of the box | You need logprobs, intermediate outputs, or finetuning types the provider does not offer |
| Cost | Usage is modest; engineering talent is scarce | API bills dominate at scale and you can staff serving, optimization, guardrails |
| Control and transparency | Rate limits, silent model updates, and provider risk are acceptable | You must freeze versions, avoid over-cautious refusals, or survive provider bans, exits, or policy changes |
| On-device | Never | Offline or on-device privacy is required |

Also consider: the same model behaves slightly differently across API providers, so retest when switching; prefer models behind a widely mimicked standard API to make swapping cheap; favor models with large communities because quirks will already be documented; privately deployed commercial models count as self-hosted for this analysis.

### License questions for any open weight model

- Is commercial use allowed?
- Are there usage caps or thresholds (e.g. a monthly active user limit requiring a special license)?
- May outputs be used to train or distill other models? Check the full lineage: a model trained on another model's outputs inherits that model's terms.
- Terminology: "open weight" means weights only; "open model" means data too. Most so-called open source models are open weight.

### Reading a leaderboard

- Which benchmarks are included, and do they cover your capability? A leaderboard without coding benchmarks says little about code generation.
- Are benchmarks highly correlated? Redundant benchmarks amplify the same bias (reasoning-heavy suites move together; truthfulness tracks them only moderately).
- How are scores aggregated? Plain averaging treats unequal-difficulty scores as equal and weights all tasks equally; mean win rate (fraction of head-to-head wins across scenarios) is one alternative.
- Were expensive benchmarks dropped for compute reasons?
- How recent are they? Saturated benchmarks no longer separate models.

### Sample size for comparing two systems

Rough guide for 95% confidence that one system beats another: a 30% score gap needs about 10 examples, 10% about 100, 3% about 1,000, 1% about 10,000. Each 3x shrink in the gap needs roughly 10x more data. For reference, typical benchmark sizes cluster around 1,000 examples; 300 is a commonly cited floor, with 1,000+ preferred, especially for synthetic data.

## Step-by-step playbooks

### A. Model selection workflow

1. **Filter on hard attributes.** Apply license, privacy, residency, hosting mode, size, and control requirements. Decide API vs self-host using the seven axes.
2. **Shortlist with public data.** Build a private leaderboard: collect recent, reliable benchmarks matching your capabilities, gather or run scores (evaluation harnesses help; full suites can be very expensive), normalize differing metrics, weight by importance, and balance against cost and latency. Goal is a short list, not a winner.
3. **Experiment with your own pipeline.** Run the shortlist on your own prompts, data and metrics. Map each candidate on cost vs performance, first finding the best achievable quality, then the cheapest model that meets thresholds.
4. **Monitor in production.** Detect failures, collect user feedback, and loop back. Steps are iterative; e.g. open models may fail step 3, forcing a switch to APIs.

Repeat selection at each adaptation stage. For prompting, start with the strongest model to test feasibility, then try smaller ones. For finetuning, start small to debug code, then scale to the largest that fits your hardware.

### B. Defining a criteria sheet

For each criterion record: metric, benchmark or dataset (public or internal), hard requirement, and ideal target. Include rows for cost per token, throughput scale (tokens per minute the provider must support), latency percentiles (e.g. P90 time to first token and total query time), overall quality, task capability, and factual consistency on an internal hallucination set.

### C. Building an evaluation pipeline (open-ended tasks)

1. **Evaluate every component.** Score intermediate outputs separately from end-to-end results so failures can be localized. Example: in a document-parsing-then-extraction flow, measure text extraction by similarity to ground truth and the extraction step by accuracy given clean text. Evaluate per turn (quality of each output) and per task (did the user's goal get done, in how many turns). Task-level matters more to users but task boundaries in conversations can be fuzzy.
2. **Write the evaluation guideline.** The most important step. Define what the system must do and must not do, including out-of-scope inputs, how to detect them, and how to respond. Explore real queries, generate several responses each, label good vs bad, and extract criteria (teams typically use two or three, such as relevance, grounding, safety). Remember a correct answer can still be a bad one if unhelpful.
3. **Build rubrics with examples.** Pick a scale per criterion (binary, three-way entail/neutral/contradict, 1 to 5, 0 to 1). Write anchored examples for each score. Have humans apply the rubric; if they disagree or struggle, revise until unambiguous. The rubric doubles later as an annotation guide for finetuning data.
4. **Tie metrics to business metrics.** Map metric levels to outcomes (e.g. grounding score X lets you automate Y% of tickets) and set a usefulness threshold below which the product is not worth shipping. Know the business target first (stickiness, engagement, automation rate) and watch for engagement goals that reward harmful or addictive behavior.
5. **Select methods per criterion.** Mix cheap and expensive scorers: a cheap classifier on all traffic plus a strong judge on a small sample. Use logprobs when available. Prefer automatic metrics but keep human review in production (some teams manually review hundreds of conversations daily) as a north-star signal. Plan production-time evaluation, where references are missing but user feedback exists.
6. **Annotate evaluation data.** Prefer real production data and natural labels; otherwise human or AI labeling against the rubric. Cover each component and each criterion, at turn and task level.
7. **Slice the data.** Keep multiple eval sets: one matching production distribution, slices by user tier, channel, input length or topic, a known-hard set, a user-error set (typos, malformed input), and an out-of-scope set. Slicing exposes bias against subgroups, aids debugging, reveals improvement areas, and guards against Simpson's paradox (a model can win every subgroup yet lose in aggregate due to group-size imbalance). If you care about it, give it a test set.
8. **Size the sets.** Bootstrap: resample the eval set with replacement many times and rescore; wide swings mean you need more data. Use the sample size guide above for comparisons.
9. **Evaluate the evaluator.** See checklist below.
10. **Iterate with tracking.** Criteria, rubrics and examples will evolve, but keep enough stability that results stay comparable over time. Log every variable: eval data version, rubric, judge prompt, judge model, sampling settings.

### D. Designing a hallucination benchmark

1. Inspect outputs to find which query types trigger hallucination (commonly niche knowledge and questions presupposing something nonexistent, such as asking what a person said on a topic they never addressed).
2. Overweight those query types in the eval set.
3. Choose local or global checking and pick a method from the table above.
4. Report grounding scores per slice, not only overall.

### E. Handling contamination

1. Detect: n-gram overlap against training data (e.g. a 13-token match flags an example as dirty; accurate but needs training data access and is expensive) or unusually low perplexity on eval items (cheap, less precise).
2. If you train models, remove benchmarks you care about before training, and report the contaminated fraction plus scores on both full and clean subsets.
3. As a consumer, treat public scores as filters, prefer benchmarks with private held-out splits, watch for statistical outliers, and confirm on your own private data.

## Checklists

**Before building**
- [ ] Criteria written for all four buckets
- [ ] Each criterion has metric, method, data source, hard threshold, ideal target
- [ ] Must-have vs nice-to-have latency distinguished
- [ ] Usefulness threshold and business mapping agreed

**Evaluating the evaluation pipeline**
- [ ] Right signal: do better responses score higher, and do better scores move business outcomes?
- [ ] Reliability: same inputs give same scores across runs; low variance across bootstrapped or alternate eval sets; fixed configs (judge temperature 0)
- [ ] Metric correlation checked: drop perfectly correlated duplicates; investigate uncorrelated pairs (real insight or broken metric)
- [ ] Added cost and latency of evaluation measured (skipping evaluation to save latency is a risky bet)

**Eval dataset coverage**
- [ ] Production-like set
- [ ] Slices by user segment, channel, input type
- [ ] Known-failure set
- [ ] User-mistake set
- [ ] Out-of-scope set
- [ ] Per-component and per-task labels

**Switching models or providers**
- [ ] Rerun full private eval, even for the "same" model on a new provider
- [ ] Recheck license and output usage terms
- [ ] Confirm required features (logprobs, function calling, structured output, finetuning)
- [ ] Verify scale limits and SLA

## Pitfalls and anti-patterns

- Shipping without any way to know whether the system works.
- Picking the top leaderboard model without checking benchmark fit or contamination.
- Using multiple-choice scores to infer generation quality.
- Blaming the model when the prompt is the problem, or vice versa.
- Evaluating only end-to-end output, leaving failures impossible to localize.
- Judging chat systems only per turn, ignoring whether tasks finish and how many turns they take.
- Vague rubrics that make AI judges and annotators inconsistent.
- Defining only desired behavior and never specifying out-of-scope handling.
- Small eval sets that cannot detect the score differences being claimed.
- Changing the eval pipeline so often that results are not comparable, or not logging judge prompts and settings.
- Assuming a provider's model is frozen; silent updates can break prompts, which also rules out some regulated uses.
- Overvaluing latency improvements users would not actually notice, or chasing engagement metrics that reward harmful content.
- Taking anecdotes about model regressions as universal; the same update can help one app and hurt another.

## Key terms

- **Evaluation-driven development:** fix success criteria before building.
- **Functional correctness:** output judged by whether it executes or behaves as required.
- **Local / global factual consistency:** support by given context vs by world knowledge.
- **Textual entailment (NLI):** classify a hypothesis vs a premise as entailment, contradiction, or neutral.
- **Self-verification:** sample extra responses and treat disagreement as a hallucination signal.
- **Knowledge-augmented verification:** decompose into claims and check each against search results.
- **IFEval / INFOBench:** instruction-following benchmarks (automatic format checks vs yes/no criteria per instruction).
- **Pareto optimization:** balancing several objectives with no single best point.
- **TTFT, time per output token, time per query:** latency metrics.
- **Hard / soft attributes:** fixed constraints vs improvable properties.
- **Open weight vs open model:** weights only vs weights plus training data.
- **Inference service / model API:** the serving system and its interface.
- **Logprobs:** token log probabilities, useful for confidence, classification and perplexity.
- **Evaluation harness:** tool to run many benchmarks on a model.
- **Mean win rate:** leaderboard aggregation by average head-to-head win fraction.
- **Benchmark saturation:** models max out a benchmark so it stops discriminating.
- **Data contamination:** evaluation data present in training data.
- **Slice-based evaluation:** scoring subsets separately.
- **Simpson's paradox:** aggregate ranking reverses subgroup rankings.
- **Bootstrapping:** resampling with replacement to estimate result stability.
- **Usefulness threshold:** minimum score at which the application delivers value.

## Source map

- Evaluation Criteria
  - Evaluation-driven development (sidebar)
  - Domain-Specific Capability
  - Generation Capability
    - Factual consistency
    - Safety
  - Instruction-Following Capability
    - Instruction-following criteria
    - Roleplaying
  - Cost and Latency
- Model Selection
  - Model Selection Workflow
  - Model Build Versus Buy
    - Open source, open weight, and model licenses
    - Open source models versus model APIs (data privacy; data lineage and copyright; performance; functionality; API cost versus engineering cost; control, access, and transparency; on-device deployment)
  - Navigate Public Benchmarks
    - Benchmark selection and aggregation
    - Public leaderboards
    - Custom leaderboards with public benchmarks (sidebar: are a provider's models getting worse?)
    - Data contamination with public benchmarks (how it happens; handling it)
- Design Your Evaluation Pipeline
  - Step 1. Evaluate All Components in a System
  - Step 2. Create an Evaluation Guideline (define criteria; scoring rubrics with examples; tie evaluation metrics to business metrics)
  - Step 3. Define Evaluation Methods and Data (select methods; annotate data; evaluate your evaluation pipeline; iterate)
- Summary
