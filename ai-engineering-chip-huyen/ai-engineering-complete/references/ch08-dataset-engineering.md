---
name: ai-eng-ch08-dataset-engineering
description: Use when building or auditing a finetuning dataset (SFT, preference, reward model, tool use, CoT, long context), deciding how much data is needed, sourcing or annotating data, generating and verifying synthetic data, distilling a model, or deduplicating, cleaning and formatting training data. Based on Chapter 8 of Chip Huyen's "AI Engineering".
---

# Chapter 8: Dataset Engineering (AI Engineering, Chip Huyen)

Operational guidance for designing, acquiring, synthesizing, verifying and processing the data used to adapt foundation models. The focus is post-training (finetuning) data, since that is what application teams usually control, with lessons borrowed from pre-training where they transfer.

## When to use this skill

- An engineer wants to finetune and asks "what data do I need, in what format, and how much?"
- A team must choose between public datasets, purchased data, human annotation, application logs, or synthetic generation.
- Someone is writing annotation guidelines or seeing inconsistent labels.
- A pipeline generates instruction, preference, tool-use or code data with an LLM and needs quality controls.
- A model behaves badly (verbose, preachy, hallucinating) and the root cause may be in the training examples.
- The plan involves distillation from a stronger (or weaker) model, or training on a model's own outputs.
- Raw data needs inspection, deduplication, cleaning, PII removal, filtering or chat-template formatting.
- A finetuned model misbehaves at inference and prompt/training format mismatch is suspected.

## Core mental models

**Data-centric vs model-centric.** You can improve a system by changing the model (architecture, size, training technique) or by changing the data while holding the model fixed. Most application teams cannot change the model much, so data becomes their main lever and differentiator. Real progress usually needs both, but data work is where application developers get the most return.

**Data teaches behavior, both ways.** The dataset is a specification by example. Whatever the examples show (style, verbosity, reasoning steps, tool calls, refusals), the model learns. Curation therefore includes removing examples that demonstrate unwanted behavior (for instance, unrequested rewrites appended to fact-checks) and adding counter-examples that show the desired behavior.

**Format follows the training phase.**

| Goal | Example shape |
|---|---|
| Continued pre-training / self-supervised | raw token sequences (documents) |
| Instruction finetuning (SFT) | (instruction, response) |
| Preference finetuning (DPO, RLHF) | (instruction, preferred response, rejected response) |
| Reward model | preference triplets, or ((instruction, response), score) |

Pre-training quantity is counted in tokens; SFT quantity in examples.

**The three curation criteria: quality, coverage, quantity.** Think of them as ingredient freshness, ingredient mix, and ingredient amount. All three matter; a weakness in one is not fixed by excess in another.

**Quality has six practical dimensions** (for finetuning data):
1. Relevant to the target task and time period.
2. Aligned with task requirements (factual where facts matter, creative where creativity matters, concise if the product wants brevity, includes justifications if the task requires them). "Aligned" beats "correct": a technically correct answer can still be the wrong target.
3. Consistent across examples and across annotators (same score means same quality).
4. Correctly formatted (no stray HTML, trailing whitespace, inconsistent casing or number formats, mistyped columns).
5. Sufficiently unique (duplicates bias the model and leak into test sets; tolerance depends on the use case).
6. Compliant with laws and internal policy (PII, licensing, copyright).

Evidence summarized in the chapter: small curated sets (around 1K to 10K examples, as in LIMA and Yi) can beat much larger noisy sets, though very small sets yield less robust models. Human labels are themselves error-prone on nuanced policies, which pushed teams such as Llama 3's toward AI-assisted annotation.

**Coverage means diversity along the axes your users actually vary on.** Axes include task type, topic/domain, instruction length and detail, output format (JSON, yes/no, open-ended), response length, language and culture, typos and register, number of turns, context length, and ratio of human to synthetic data. Which axes matter is application-specific: a translator needs topic and style diversity but not language diversity; a global shopping assistant needs linguistic and cultural diversity more than domain diversity. Adding heterogeneous data is not automatically good; it can hurt. Experiments show that quality plus diversity together beat either alone at equal size, and that increasing the number of distinct tasks gives large gains before plateauing.

**Data mix differs per phase.** In Llama 3, code plus math made up close to half of pre-training and SFT data (far above their share of the web), because high-quality code and math disproportionately boost reasoning; annealing on such data late in pre-training helped benchmarks. Preference data, by contrast, was dominated by general content to mirror real user preferences.

**Quantity is situational.** Needs range from a handful of examples to millions. Drivers besides quality and diversity:
- Finetuning technique: full finetuning needs orders of magnitude more data than PEFT (LoRA etc.).
- Task complexity: binary sentiment needs far less than financial-filing QA.
- Base model strength: the closer the base model already is, the fewer examples needed. Stronger models win clearly with ~100 examples; with hundreds of thousands, model differences largely vanish.
- Budget: annotation cost per example caps dataset size, and data and compute spend trade off against each other.

**Ossification.** With very large datasets, finetuning a pre-trained model can underperform training from scratch because pre-trained weights adapt poorly; smaller models are more affected. If you have millions of examples, evaluate from-scratch training as an option.

**Augmentation vs synthesis.** Augmentation derives new examples from real ones (flip, paraphrase, swap). Synthesis creates data that imitates real data without being real. Both are often called "synthetic data."

**Synthetic data is a complement, not a replacement.** Mixing human and AI data usually gives the best value.

## Decision frameworks

### How much data and which technique

| Situation | Recommendation |
|---|---|
| Hundreds to a few thousand examples | PEFT (e.g., LoRA) on a stronger base model |
| Tens of thousands to millions of examples | Consider full finetuning, possibly on a smaller model |
| Millions of examples, small model | Also test training from scratch (ossification risk) |
| Unknown whether finetuning helps | Pilot with ~50 to 100 well-crafted examples first |
| Pilot shows clear gains | More data will likely help; measure the scaling curve |
| Pilot shows no gain | Check hyperparameters, data quality and prompts before concluding; if truly flat, a bigger set rarely rescues it |

### Estimating marginal value of more data
Train on nested subsets (e.g., 25%, 50%, 100%) and plot performance vs size. Steep slope: doubling data should pay off. Flat slope: more data buys little; invest in quality, diversity or a different approach. Expect diminishing returns as a default.

### Reducing the need for scarce high-quality data (staged finetuning)
- Lots of unlabeled domain text, few labeled pairs: self-supervised finetune on the documents, then SFT on pairs.
- Lots of adjacent-task labels: finetune on the related task first, then on the target task.
- Sensitive domain with little real data: finetune on synthetic data, then on real data. Warning: this two-stage handoff is easy to get wrong and can cost more compute for a worse model than SFT on good data alone.

### Choosing a data source

| Source | Strength | Watch out for |
|---|---|---|
| Your own application (user content, usage logs, feedback) | Matches the real distribution; enables a data flywheel | Privacy, consent, feedback design |
| Public datasets (Hugging Face, Kaggle, Google Dataset Search, government portals, academic repositories, cloud open data, eval harness benchmarks) | Cheap, fast start | License (including sub-sources), provenance, unverified quality, benchmark contamination |
| Purchased / proprietary | Specialized coverage | Cost, license scope |
| Human annotation | Can target exact behaviors | Cost, inconsistency, fatigue, guideline effort |
| Synthetic (rule-based, simulation, AI) | Scale, coverage of rare cases, privacy | Verification burden, collapse, lineage |

In practice, combine channels: start from a found dataset, filter, repair, then fill coverage gaps with targeted synthesis plus human review.

### When to synthesize, and with which method

| Need | Good fit |
|---|---|
| Structured documents or grammar-bound data (invoices, transactions, forms, equations, regex) | Rule/template generation with fakers |
| Robustness and invariances | Transformations and perturbation (crops, noise, word swaps, random token replacement) |
| Bias mitigation | Counterfactual swaps (gender, names, roles) |
| Rare, dangerous or expensive real-world events | Simulation (driving, robotics, finance shocks, manufacturing defects, climate) |
| Tool use / agent trajectories | Simulate action sequences, execute, keep the most efficient successful one; AI-simulated APIs when real calls are slow or costly |
| Multi-party behavior (negotiation, support) | Self-play / role-play between model instances |
| More phrasings of existing queries | AI paraphrasing |
| Low-resource languages or programming languages | AI translation verified by back-translation |
| Long, high-quality responses | Reverse instruction (generate prompts for existing human-written content) |
| Longer context window | Chunk long docs, generate QA per chunk, train with the full doc as context |
| Preference pairs | AI judge with position-swap consistency check |
| Privacy-restricted domains | Fully synthetic records |
| Cheaper/faster model | Distillation from a teacher |

### Is it really distillation?
Distillation means the teacher's quality is the student's ceiling. Training on synthetic data can also produce a student that surpasses the generator (bootstrapping via reverse instruction; a large base model finetuned on data from a smaller generator). Self-generated data only helps if it is verified first; unfiltered self-training can stall or degrade.

## Step-by-step playbooks

### A. Design a finetuning dataset from scratch
1. Write down the behaviors the model must learn and unlearn; trace current failures to specific example patterns.
2. Choose the training phase and example format (see table above). Decide single-turn, multi-turn, or both: single-turn is easy to get; multi-turn teaches clarifying questions and incorporating corrections but needs designed scenarios.
3. For each of the six quality dimensions, define what it concretely means for this task.
4. List the coverage axes that matter for your users and set target proportions, ideally mirroring real traffic; for large efforts, test candidate mixes on small models and extrapolate.
5. Write annotation guidelines: what good looks like, why, whether correct-but-unhelpful is acceptable, and what separates adjacent scores. Reuse them for evaluation data (they are the same guidelines).
6. Run a 50 to 100 example pilot, then a subset-scaling experiment to size the full effort against the budget.
7. Acquire, synthesize, verify and process (playbooks below); iterate, since curation, generation and processing loop back on each other.

### B. Build an (instruction, response) set by mixing channels (illustrative)
1. Find a candidate public set; check license and provenance.
2. Drop poor instructions.
3. Separate good instructions with poor responses; have humans rewrite those responses.
4. Identify thin topics; write a few instruction templates per gap and have an LLM expand them, keeping per-template counts modest to preserve diversity.
5. Human-annotate or verify the generated items.
6. Expect detours: revising guidelines and re-annotating, adding fact-checkers, adding templates.

### C. Synthesize instruction data with an LLM
1. Seed: a topic/subtopic tree, keyword list, instruction-type list, or a small set of curated seed examples (each can itself be AI-generated).
2. Generate N instructions per leaf or per template; generate one or more responses per instruction (AI or human for either side).
3. For long-form targets, prefer reverse instruction to avoid hallucinated long responses.
4. For code, follow a verify-and-repair loop: generate diverse problem statements; generate solutions per language, with good-practice rules and step-by-step reasoning in the prompt; run parsers and linters; run AI-generated unit tests; on failure, feed the problem, faulty code and error output back for revision; keep only passing samples; translate to other languages and re-test; generate explanations/docs and keep only those whose back-translated code matches the original.
5. To bootstrap without new human labels: train a weak model on seeds, use it to write instructions for high-quality existing text, finetune on that, repeat.
6. Verify (playbook D) before anything enters the training set.

### D. Verify data (synthetic or real)
1. Prefer data you can check functionally (execution, tests, back-translation, exact answers). That is why code is the most common synthetic domain.
2. Otherwise use AI verifiers: a 1 to 5 score, a good/bad classifier, or a judge given explicit quality requirements.
3. Check factual consistency with hallucination/inconsistency detectors when facts matter.
4. Use creative discriminators: if a detector easily separates synthetic from real, the synthetic data is not realistic enough; a quality classifier trained on a target bar (e.g., acceptance-worthy papers) can filter rejects.
5. Run topic classification to drop off-task items and anomaly detection to flag outliers.
6. Apply heuristics: drop empty or too-short items, truncate or drop overlong ones, filter by keyword, author, date, source or metadata, drop repetitive items, same-instruction-different-response conflicts, and outputs that just echo inputs.
7. For AI-judged preference pairs, ask twice with the order swapped and keep only consistent verdicts (counters first-position bias).
8. Final test: does training on it improve the model on your evaluation?

### E. Process a raw dataset
Operational rules first: order the steps by cost (deduplicate before expensive cleaning, or filter before expensive dedup, whichever saves more); trial-run every script on a sample; never modify data in place, keep the original for other uses and as protection against buggy scripts.

1. **Inspect.** Record provenance, prior processing and prior uses. Plot token, input-length and response-length distributions; check special tokens, topics and languages and their relevance. Slice by source, time and annotator; look for annotators skewing short or high, question types with odd lengths or scores, and outliers. Compute inter-annotator disagreement and resolve conflicts. Then read examples by hand: annotate a few yourself and compare, fact-check, look for same-query-different-answer and same-answer-different-query pairs. Fifteen minutes of reading routinely saves hours. Creative statistics (e.g., verb/object pair distributions) also compare models.
2. **Deduplicate.** Decide granularity (document, paragraph, sentence, token), match strictness (exact vs partial overlap threshold), and whether order matters. Look for whole-document, intra-document and cross-document duplicates. Methods: pairwise similarity (exact, n-gram, fuzzy, embedding; costly at scale), hashing (MinHash, Bloom filters) to compare only within buckets, or dimensionality reduction plus approximate nearest neighbors. Libraries exist (e.g., datasketch, Dedupe, TheFuzz). Dedupe before splitting train/test.
3. **Clean and filter.** Strip markup you do not want learned (one reported case: removing stray Markdown/HTML gave about 20% accuracy gain and 60% shorter inputs). Remove non-compliant content: PII, sensitive or copyrighted material, toxicity, and disallowed fields (name, zip code, gender). Remove low-quality items using verification methods and heuristics discovered by reading the data (e.g., labels from late in an annotation session tend to be worse due to fatigue). If you still have more than you can afford to train on, prune with active learning, importance sampling or data-pruning metrics.
4. **Format.** Apply the target model's tokenizer and exact chat template; template errors cause strange bugs. SFT data is (instruction, response), with instruction possibly split into system and user prompts. When moving from prompting to finetuning, drop task descriptions and few-shot examples from the instruction (turn the few-shot examples into training rows); the model learns the task from data, which also shortens inference prompts and cuts cost. Experiment with alternative formats. At inference, reproduce the training prompt format exactly: missing delimiters, extra prefixes or a stray trailing space can all break behavior. For tool use, consider a multi-message format with headers naming source and destination and explicit turn-termination tokens.

## Checklists

**Before collecting data**
- [ ] Target behaviors and anti-behaviors listed
- [ ] Phase and example format chosen; single vs multi-turn decided
- [ ] Six quality dimensions defined for this task
- [ ] Coverage axes and target mix defined from real usage
- [ ] Annotation guideline drafted and shared with eval
- [ ] Budget split between data and compute

**Before training on a dataset**
- [ ] Licenses checked for the dataset and its sub-sources; distillation allowed by the teacher model's terms
- [ ] Provenance documented (including which models generated what)
- [ ] Distributions plotted and sliced; outliers explained
- [ ] Inter-annotator agreement measured; conflicts resolved
- [ ] Deduplicated, and train/test overlap checked against eval benchmarks
- [ ] PII and policy-violating content removed
- [ ] Markup noise stripped; types and number formats correct
- [ ] Synthetic portion verified and mixed with real data
- [ ] Chat template matches the base model; inference prompt matches training format
- [ ] Original raw data preserved

**Special behaviors**
- [ ] CoT: responses contain the reasoning steps, not only the final answer
- [ ] Tool use: trajectories reflect efficient machine actions (APIs), not human UI habits; observed rather than recalled when human-sourced
- [ ] Long context: examples actually require the extended context

## Pitfalls and anti-patterns

- Chasing volume over quality; noisy data at scale often loses to a curated small set.
- Adding heterogeneous data blindly; it can lower performance.
- Abandoning annotation guidelines midway and hoping the model infers intent.
- Trusting public datasets or licenses without inspection.
- Concluding "finetuning doesn't work" from a tiny pilot without checking learning rate, data quality and prompts.
- Asking experts to describe their workflow instead of observing it; they omit steps.
- Copying human tool-use habits that are inefficient for an agent.
- Training a student on teacher answers it cannot actually derive, which teaches it to fabricate solution-shaped text. The same applies when human labelers use knowledge the model lacks.
- Superficial imitation: distilled models copy style but lag on factuality and out-of-distribution generalization; reasoning gains mostly need a better base model.
- Recursive training on purely synthetic data (model collapse): rare events vanish as common outputs dominate. Mix in real data; no established safe ratio exists, and successes with very high synthetic fractions were shown for single iterations only.
- Bias amplification through feedback loops when model outputs re-enter training.
- Lost lineage: a generator model's copyright issues or benchmark exposure silently transfer to your model and contaminate your evals.
- Too many generations per template, collapsing diversity.
- AI judges' position bias in preference data.
- Duplicates skewing spurious correlations (a few repeated rows can teach a false rule) and leaking into test sets; heavy repetition of a tiny slice can degrade a model to the quality of one half its size.
- Editing data in place; skipping trial runs.
- Mismatched chat templates or inference prompts that deviate by even one character from training format.
- Distilling from models whose license forbids training on their outputs.

## Key terms

- **Data-centric AI**: improving systems by improving data with the model held fixed.
- **Data flywheel**: loop where product usage generates data that improves the product.
- **Coverage / diversity**: how well data spans the variation in real usage.
- **Data mix**: proportions of domains/tasks in a training phase.
- **Annealing**: late-stage training with decaying learning rate on a shifting, higher-quality mix.
- **Ossification**: pre-trained weights resisting adaptation to large finetuning sets.
- **PEFT / LoRA**: parameter-efficient finetuning; needs less data than full finetuning.
- **Augmentation**: new data derived from real data. **Synthesis**: artificial data mimicking real data.
- **Procedural generation**: algorithmic data creation (rules, templates).
- **Perturbation**: adding noise to inputs for robustness.
- **Sim2Real**: transferring simulation-trained behavior to the real world.
- **Self-play**: model instances interacting to generate experience.
- **Back-translation**: translate output back to the source and compare to verify fidelity.
- **Reverse instruction**: generating prompts for existing high-quality content.
- **AI verifier**: judge or scorer filtering generated data.
- **Model collapse**: degradation from recursive training on generated data.
- **Data lineage**: traceable origin of each example.
- **Distillation**: training a student to imitate a teacher.
- **Inter-annotator disagreement**: divergence between annotators on the same item.
- **MinHash / Bloom filter**: hashing tools for scalable near-duplicate detection.
- **Active learning / importance sampling / data pruning**: selecting the most useful subset when data exceeds budget.
- **Chat template**: model-specific token structure for roles and turns.

## Source map

- Chapter 8 introduction; sidebar "A Data-Centric View of AI"
- Data Curation
  - Data Quality
  - Data Coverage
  - Data Quantity
  - Data Acquisition and Annotation (sidebar: Resources for Publicly Available Datasets)
- Data Augmentation and Synthesis
  - Why Data Synthesis
  - Traditional Data Synthesis Techniques (Rule-based data synthesis; Simulation)
  - AI-Powered Data Synthesis (Instruction data synthesis; Data verification; Limitations to AI-generated data: Quality control, Superficial imitation, Potential model collapse, Obscure data lineage)
  - Model Distillation
- Data Processing
  - Inspect Data
  - Deduplicate Data
  - Clean and Filter Data
  - Format Data
- Summary
