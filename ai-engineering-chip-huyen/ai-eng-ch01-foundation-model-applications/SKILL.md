---
name: ai-eng-ch01-foundation-model-applications
description: Use when scoping or planning an LLM/foundation-model product: deciding whether and why to build, buy vs build, picking a use-case pattern, defining AI vs human roles, setting success metrics and usefulness thresholds, planning milestones and maintenance, assessing defensibility, or explaining the AI engineering stack vs ML engineering. Based on Chapter 1 of Chip Huyen's "AI Engineering".
---

# Chapter 1: Building Applications on Foundation Models (AI Engineering, Chip Huyen)

This skill condenses the opening chapter of the book into guidance an agent can apply when an engineer is at the very start of an AI project: understanding what foundation models are, deciding whether an application is worth building, framing how it should be built, and knowing which parts of classic ML practice still apply. Later chapters go deep on each topic; this one is the map.

## When to use this skill

Apply it when the user:

- Asks "should we build this with an LLM?" or "is this a good AI use case?"
- Needs to justify an AI initiative (threat, opportunity, exploration) or choose buy vs build.
- Is designing how much autonomy the AI gets and where humans stay in the loop.
- Needs success criteria: business metrics, quality, latency (TTFT, TPOT), cost per request.
- Has a promising demo and wants a realistic plan to production.
- Worries about a product being made obsolete by the next model release or copied by a large incumbent.
- Wants to understand the layers of an AI stack, or how an AI engineer's job differs from an ML engineer's or a full-stack engineer's.
- Is confused about terminology: tokens, masked vs autoregressive models, self-supervision, foundation model, pre-training vs post-training vs finetuning, prompt engineering vs "training".

## Core mental models

**Scale is the defining force.** Bigger models do more tasks, which expands demand; but only a handful of well-funded organizations can afford to train them, which produced the model-as-a-service pattern. Net effect: demand for AI apps went up while the barrier to building them went down. That combination is why AI engineering exists as a discipline.

**A language model is a probabilistic completion engine.** It encodes how likely each token is given a context. The basic unit is the token (a character, word, or word fragment). For GPT-4-class tokenizers, one token is roughly three quarters of a word, so 100 tokens is about 75 words. The vocabulary (all tokens a model knows) is fixed by the model developer, e.g. about 32k for Mixtral 8x7B and about 100k for GPT-4. Tokens beat characters (they carry meaning) and beat whole words (smaller vocabulary, graceful handling of unseen words). Non-English text often costs more tokens per character.

**Two families of language model.**
- Masked (e.g. BERT): fills blanks using context on both sides. Suited to classification, sentiment, and tasks needing whole-context understanding.
- Autoregressive (also called causal): predicts the next token from preceding ones only, so it can generate indefinitely. This is the default for generation and what "language model" means in the rest of the book.

**Many tasks reduce to completion.** Translation, summarization, coding, and classification can all be phrased as "complete this text". The catch: outputs are predictions, not guarantees, and a raw completion model may continue your text (e.g. add another question) rather than answer it. Turning a completer into an assistant is the job of post-training.

**Self-supervision is what unlocked scale.** Supervised learning needs costly human labels (labeling a million images at a few cents each already costs tens of thousands of dollars; expert labels such as medical imaging cost far more). In language modeling, every text sequence supplies its own labels: each prefix is an input and the next token is the target. Start and end-of-sequence markers matter; the end marker is how a model learns when to stop. Self-supervision infers labels from data; unsupervised learning needs no labels at all. Do not conflate them.

**Size is relative.** Parameter count is the usual size measure, and what counts as "large" keeps shifting (117M was large in 2018; around 100B is large at the time of writing). Larger models need more data to reach their potential; training a big model on a small dataset wastes compute that a smaller model would use better.

**Foundation model = general-purpose, often multimodal, built upon.** Extending language models to images, audio, video and more produced large multimodal models (LMMs). The term "foundation" signals both centrality and that others build on top. Two shifts follow: from modality-siloed research (NLP vs vision vs speech) to unified models, and from task-specific models to general-purpose ones. Self-supervision extends to multimodal data too (CLIP learned from about 400M naturally co-occurring image-text pairs). CLIP is an embedding model, not generative; embeddings are vectors meant to capture meaning and serve as backbones for generative multimodal systems.

**Three ways to adapt a model to your task.** Prompt engineering (instructions plus examples), retrieval-augmented generation (pull relevant data, e.g. customer reviews, into the context), and finetuning (further training on curated examples). Adapting a strong existing model is typically orders of magnitude cheaper than building from scratch (think a handful of examples and a weekend vs a million examples and half a year). Task-specific models still win on size, speed and cost in some cases.

**Why AI engineering took off now.** Three reinforcing factors: general-purpose capability (many more tasks become automatable, especially anything involving communication), surging investment (costs for some use cases fell around 100x in a year), and a very low entry barrier (API access, natural-language programming, AI-written code).

**Adaptation is split by whether weights change.** Prompt-based techniques leave weights untouched: fast, data-light, and they let you try many models cheaply, but may fall short for complex or strict-performance tasks. Finetuning changes weights: more data and complexity, but can improve quality, latency and cost, and is needed for genuinely new tasks.

**Training vocabulary.** Pre-training trains from random initialization (the overwhelming majority of compute, risky, few practice it). Finetuning continues training from existing weights. Post-training is conceptually the same as finetuning; the label usually signals that the model developer did it (e.g. instruction tuning before release), whereas finetuning is what application developers do. Quantization changes weights but is not training. Putting examples or documents into the context is prompt engineering, not training or finetuning, regardless of colloquial usage.

## Decision frameworks

### Why build at all (rank the motivation)

| Motivation | Signal | Implication |
|---|---|---|
| Existential threat | Competitors using AI could make you obsolete (common in document processing, financial analysis, insurance, data processing, advertising, design) | Top priority; strongly favor in-house capability rather than outsourcing to a potential competitor |
| Profit and productivity opportunity | AI can cut acquisition cost, lift retention, speed sales, research, internal comms | Most common case; seriously evaluate buying existing tools first |
| Exploratory, fear of being left behind | Unclear fit, but transformative tech | Reasonable as bounded R&D if affordable; small startups may not afford it |

If the user only wants to learn, skip planning and build: building is the best teacher. If it is a business bet, plan first, because a cool demo is easy and a profitable product is hard.

### Role of AI in the product

| Dimension | Option A | Option B | Design consequence |
|---|---|---|---|
| Criticality | Critical (app fails without AI, like face unlock) | Complementary (app works without it, like smart compose) | Critical demands much higher accuracy and reliability; users forgive mistakes in complementary features |
| Trigger | Reactive (answers a user request) | Proactive (surfaces itself when useful) | Reactive usually needs low latency; proactive can be precomputed but needs a higher quality bar because unrequested low-quality output feels intrusive |
| Update cadence | Dynamic (continually updated per user, e.g. per-user finetuning or memory) | Static (shared model updated periodically) | Dynamic needs personalization infrastructure and feedback pipelines |

### Role of humans (autonomy ladder)

Pick a rung and define the promotion criteria up front:
1. AI drafts suggestions that humans may use.
2. AI handles simple requests directly, routes complex ones to humans.
3. AI handles everything without human involvement.

Pair this with a crawl-walk-run rollout: humans mandatory; then AI interacts directly with internal staff; then broader automation including external users. Promote on evidence, e.g. when human agents accept AI suggestions for a request class nearly verbatim at a very high rate (the book's example is around 95%), let customers talk to the AI directly for that class.

### Internal vs external, open vs closed outputs

Enterprises deploy internal-facing apps (knowledge management) faster than external ones (customer chatbots) because privacy, compliance and catastrophic-failure risks are lower, and the team builds expertise along the way. Likewise, close-ended tasks (classification) are easier to evaluate, so their risk is easier to estimate. When risk tolerance is low, recommend starting internal and close-ended.

### Defensibility

Three possible moats: technology, data, distribution. With shared foundation models, technology rarely differentiates; distribution tends to favor incumbents. Data is the realistic moat for newcomers: get to market early, collect usage data, and run a data flywheel (even when data cannot train models directly, usage reveals behavior and product gaps). Two red-flag tests:
- **Subsumption test:** does the product exist only because today's model is weak at something (e.g. parsing PDFs)? If the next model fixes it, the product dies. Mitigation: target a segment the model provider will not serve, such as on-prem users of open models.
- **Feature test:** could a big platform replicate this as a feature with a small team in weeks? If yes, find an overlooked wedge and grow from it (many successful companies started as "just a feature").

### Choosing an adaptation technique (first pass)

| Situation | Start with |
|---|---|
| Exploring, little data, need speed | Prompt engineering across several models |
| Model lacks your private or fresh knowledge | RAG |
| Strict quality, latency or cost targets, or a task the model never saw | Finetuning |
| Huge volume, narrow fixed task | Consider a small task-specific model |

Data need roughly orders as: prompting < finetuning < training from scratch.

### Where AI tends to help (use-case patterns)

Eight recurring categories, each with consumer and enterprise variants: coding; image and video production; writing; education; conversational bots; information aggregation; data organization; workflow automation (including agents). Apps often span several. Practical heuristics drawn from the evidence in the chapter:
- Writing and creative work suit AI because errors are cheap to ignore and probabilistic variety is a feature.
- Coding gains are large for documentation (about 2x) and code generation and refactoring (roughly 25 to 50 percent), and small for highly complex tasks; practitioners report frontend outperforming backend.
- AI narrows quality gaps between workers (largest gains for weaker writers; one controlled study saw about 40 percent faster and 18 percent better output).
- Summarization and structured extraction (receipts, IDs, contracts, meeting notes into action items) are high-value enterprise wins.
- A task is "exposed" to AI if AI can cut its completion time by at least half; occupations heavy in translation, writing, tax prep and web design are highly exposed, physical trades are not. Use this lens to spot candidates.
- Agents (models that plan and use tools) unlock automation like booking or refunds but need tool access and permissions.

## Step-by-step playbooks

### Playbook A: Scoping a new AI application

1. **State the reason.** Classify as threat, opportunity, or exploration. If exploration, set a time and budget box.
2. **Buy vs build.** List existing vendor or open-source options. Build in-house when AI is existential or a core differentiator; otherwise default to buying.
3. **Define the AI's role.** Critical or complementary, reactive or proactive, dynamic or static. Derive accuracy, latency and quality bars from these.
4. **Define the human's role.** Choose the starting autonomy rung and write explicit promotion criteria (acceptance rate, error rate, escalation rate).
5. **Check defensibility** (if selling it): run the subsumption and feature tests; identify the data flywheel.
6. **Set success metrics** (Playbook B).
7. **Evaluate off-the-shelf models** against those metrics before committing. Measure the baseline gap (e.g. model already automates 30 percent of tickets against a 60 percent goal).
8. **Re-decide.** If the cost to reach the usefulness threshold exceeds the expected return, stop or rescope. Goals legitimately change after evaluation.
9. **Plan milestones for the last mile** (Playbook C) and maintenance (Playbook D).

### Playbook B: Setting expectations and metrics

1. Start with business impact. For a support bot: share of messages automated, extra throughput, response time reduction, labor saved.
2. Add guardrail metrics so volume gains do not mask unhappiness: customer satisfaction and feedback.
3. Define a usefulness threshold below which the product does not ship, covering:
   - Quality of responses.
   - Latency: time to first token (TTFT), time per output token (TPOT), total latency. Benchmark against the current process, not an abstract ideal (if humans answer in a median of an hour, minutes may be fine).
   - Cost per inference request.
   - Other: interpretability, fairness.
4. Map business metrics to model metrics and back, so model work is tied to outcomes.

### Playbook C: From demo to product

1. Expect a fast start: a compelling demo may take days. Do not extrapolate that pace.
2. Budget for the long tail: early teams report reaching roughly 80 percent of target experience in a month, then needing several more months to pass 95 percent, with most effort on product rough edges and hallucinations.
3. Break the plan into milestones defined by metric thresholds, not features.
4. Track progress per percentage point near the top; each increment is slower than the last.
5. Build evaluation and versioning early so iteration is measurable.

### Playbook D: Planning for maintenance in a fast-moving field

1. Assume models, prices and context limits will change on a months timescale; schedule periodic cost-benefit reviews of each technology choice.
2. Keep the model layer swappable (providers are converging on similar APIs), but budget for re-tuning prompts, data and workflows per model, since each has quirks.
3. Maintain versioned prompts and an evaluation suite so a model swap is a test run, not a gamble.
4. Watch vendor risk: in-house hosting that looked cheaper can flip when API prices halve; a third-party provider can fold.
5. Watch regulatory and supply risk: data protection rules, export controls on compute, GPU availability.
6. Assess IP risk: if outputs come from a model trained on others' data, clarify ownership; IP-heavy businesses may need legal review before adoption.

### Playbook E: Organizing the work (AI-first workflow)

1. Start at the application layer: prompts, context, interface, evaluation.
2. Ship a product prototype first, gather user feedback, iterate quickly.
3. Invest in data and model work (finetuning, dataset engineering, inference optimization) only once the product shows promise.
4. Drop to infrastructure (serving, compute, monitoring) as scale demands.
5. Keep AI engineers involved in product decisions; the old split between model builders and product builders no longer fits.

## Checklists

**Pre-build go/no-go**
- [ ] Motivation classified (threat / opportunity / exploration)
- [ ] Buy options surveyed
- [ ] AI criticality, trigger, update cadence decided
- [ ] Human-in-the-loop level and promotion criteria written
- [ ] Defensibility assessed (subsumption, feature, data moat)
- [ ] Business metrics and usefulness threshold defined (quality, TTFT, TPOT, total latency, cost per request, fairness)
- [ ] Off-the-shelf baseline measured
- [ ] ROI still positive after baseline evaluation
- [ ] Last-mile time budgeted
- [ ] Maintenance, vendor, regulatory and IP risks reviewed

**Stack responsibilities to staff**
- Application layer: evaluation, prompt engineering and context construction (including memory for long tasks), AI interface, user feedback capture.
- Model layer: modeling and training/finetuning, dataset engineering (deduplication, tokenization, context retrieval, quality control, removing sensitive and toxic data), inference optimization (quantization, distillation, parallelism).
- Infrastructure layer: serving, data and compute management, monitoring.

**Interface options to consider:** standalone web, desktop or mobile app; browser extension; bot inside chat platforms; plug-in via a host product's API; voice; embodied (AR/VR). Remember chat feedback is easy for users to give but hard to extract.

**Enduring ML principles to keep applying:** tie work to business problems; map business to model metrics; run systematic experiments (now over models, prompts, retrieval methods, sampling parameters instead of just hyperparameters); optimize speed and cost; close the loop with production feedback.

## Pitfalls and anti-patterns

- **Demo euphoria:** treating a weekend prototype as evidence the product is close.
- **Building for hype:** chasing AI without a threat or opportunity case, or conversely waiting so long you get disrupted.
- **Wrapper fragility:** a product whose only value is a temporary model weakness.
- **Feature-sized startup:** something an incumbent can clone quickly, with no data flywheel.
- **Proactive spam:** pushing low-quality unsolicited outputs; proactive needs a higher bar.
- **Volume as success:** counting automated messages while ignoring satisfaction.
- **Unfair benchmark comparisons:** comparing models evaluated with different prompting setups (e.g. many-shot chain-of-thought for one, few-shot for another). The same model can swing several points on a benchmark with prompting alone; always compare under identical prompts.
- **Assuming ground truth exists:** open-ended outputs have many valid answers, so exact-match evaluation breaks; plan evaluation as a first-class effort.
- **Mislabeling work:** calling context stuffing "training" or "finetuning" leads to wrong cost and data expectations.
- **Locking into one vendor or build choice** without periodic re-evaluation.
- **Ignoring latency physics:** autoregressive decoding is sequential (e.g. 10 ms per token means about one second per 100 tokens), so web-style 100 ms targets are hard; design UX around streaming or precomputation.
- **Underestimating compute scale:** teams comfortable with a few GPUs may lack skills for large clusters.
- **Undervaluing ML knowledge:** not strictly required to build, but it widens options and is key to debugging misbehaving models.
- **Ignoring abuse vectors:** generated content can be used for spam, fake reviews and content farms; consider misuse in design.

## Key terms

- **Token / tokenization / vocabulary:** units a model reads and writes; the process of splitting text into them; the full set the model knows.
- **Masked LM:** predicts missing tokens using both sides of context.
- **Autoregressive (causal) LM:** predicts next token from prior tokens; generative.
- **Generative model:** produces open-ended outputs from a finite vocabulary.
- **Self-supervision:** labels derived from the input itself. **Supervision:** human-provided labels. **Unsupervised:** no labels.
- **BOS/EOS:** sequence start and end markers.
- **Parameter (weight):** learned variable; count is the size measure.
- **Foundation model:** large, general-purpose LLM or LMM others build upon.
- **LMM:** large (generative) multimodal model.
- **Embedding:** vector representing meaning; CLIP produces joint text-image embeddings.
- **Natural language supervision:** using co-occurring text as labels for other modalities.
- **Prompt engineering:** steering behavior via input only. **Context construction:** supplying needed information, tools, memory.
- **RAG:** retrieving external data into the prompt.
- **Pre-training / post-training / finetuning:** from scratch / after pre-training by model developer / after by application developer.
- **Inference:** computing an output from an input. **Inference optimization:** making it faster and cheaper.
- **Dataset engineering:** curating, generating, annotating data for training or adaptation.
- **TTFT / TPOT:** time to first token / time per output token.
- **Human-in-the-loop:** humans participate in AI decisions. **Crawl-walk-run:** staged autonomy rollout.
- **Usefulness threshold:** minimum performance for a product to be worth shipping.
- **Data flywheel:** usage data improving the product, attracting more usage.
- **Agent:** AI that plans and uses tools.
- **Exposure (occupational):** share of tasks AI can speed up by 50 percent or more.
- **MMLU:** popular multitask knowledge benchmark.
- **AI engineering:** building applications on top of existing foundation models; less model building, more adaptation and evaluation, closer to full-stack work.

## Source map

Chapter 1, "Introduction to Building AI Applications with Foundation Models":
- The Rise of AI Engineering
  - From Language Models to Large Language Models (Language models; Self-supervision)
  - From Large Language Models to Foundation Models
  - From Foundation Models to AI Engineering (sidebar: Why the Term "AI Engineering?")
- Foundation Model Use Cases
  - Coding; Image and Video Production; Writing; Education; Conversational Bots; Information Aggregation; Data Organization; Workflow Automation
- Planning AI Applications
  - Use Case Evaluation (The role of AI and humans in the application; AI product defensibility)
  - Setting Expectations
  - Milestone Planning
  - Maintenance
- The AI Engineering Stack
  - Three Layers of the AI Stack
  - AI Engineering Versus ML Engineering (Model development: Modeling and training, sidebar on training vs pre-training vs finetuning vs post-training, Dataset engineering, Inference optimization; Application development: Evaluation, Prompt engineering and context construction, AI interface)
  - AI Engineering Versus Full-Stack Engineering
- Summary
