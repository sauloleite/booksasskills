# Fine-Tuning Decisions: When, Which Method, Which Model Size

## Contents
- Parametric learning in one paragraph
- Go / no-go checklist
- The method menu (SFT, vision, DPO, RFT/RLVR)
- Fine-tuning large foundation models: costs and payoffs
- The case for small models
- Picking a model size and staying current
- Decision walkthroughs
- Pitfalls

## Parametric learning in one paragraph

Parametric learning updates the model's weights so that the improvement lives inside the model rather than in the prompt. It becomes attractive when nonparametric methods have proven the value of the examples but carrying those examples and insights in every prompt costs too many tokens and too much latency. The chapter treats it as a later step: start nonparametric, measure, and consider weights only when example volume is large. Training from scratch (pretraining on trillions of tokens) is out of scope for nearly every team; the realistic options are adapting an existing open-weight or hosted model.

## Go / no-go checklist

Lean toward fine-tuning when several of these hold:
- **Narrow domain matters.** The model must use internal jargon, a strict style guide, or handle sensitive material with very few errors, and off-the-shelf models stumble.
- **Rigid format or tone.** Every output must follow a fixed template (financial disclosures, legal disclaimers) and prompt engineering to enforce it has become elaborate and fragile.
- **Tool calls must be exact.** The agent calls high-consequence functions (dosage calculators, trading APIs) and miscalls or mishandled edge cases are unacceptable.
- **Data and budget exist.** A curated set in the hundreds or thousands, GPU time, and (for reinforcement fine-tuning) domain experts to grade outputs.
- **Retraining cadence is sustainable.** You can run versioning, scheduled retrains and compatibility checks. If the domain moves fast, upkeep may eat the gains.

Hold off when any of these hold:
- **Prototyping or low traffic.** Prompting and nonparametric learning iterate with zero retraining cost. Wait until the use case and data pipelines are stable.
- **Upstream models move faster than you.** A new provider base model may beat your tuned older model and erase months of work. Weigh your investment against the release pace.
- **Resource limits.** Scarce GPUs, costly annotation, or strict inference speed targets. Retrieval-augmented generation and other nonparametric approaches deliver much of the benefit with far lower upfront and ongoing cost.

The overriding rule: fine-tune only when performance needs, data availability and operational capacity line up, and always keep a plan for retraining or migrating when the next base model ships. Before any tuning, check whether an existing instruction-tuned open model (with a suitable license) plus prompt engineering or nonparametric learning already meets the bar. If uncertain, do not fine-tune; there is usually a cheaper, higher-leverage product improvement available.

## The method menu

| Lever | Training signal | Use it for |
|---|---|---|
| Supervised fine-tuning (SFT) | Curated prompt and ideal-response pairs | Classification, structured output, fixing instruction-following errors, function calling |
| Vision fine-tuning | Image and label pairs | Image classification, more reliable multimodal instruction following |
| Direct preference optimization (DPO) | Per prompt, a preferred and a rejected response | Tone, style, what a summary should emphasize |
| Reinforcement fine-tuning (RFT) | Candidate outputs scored by expert graders, policy-gradient update | Complex reasoning, high-stakes domains such as legal or medical |

RLVR (reinforcement learning with verifiable rewards) is the generalization of RFT to any grader you can build; details in the SFT, DPO and RLVR playbook.

Quick selector:
- You can write the correct answer: SFT.
- You cannot write the perfect answer, but can say which of two is better: DPO.
- You can score an answer automatically or with a scalable grader: RLVR.
- The input is images: vision fine-tuning.

## Fine-tuning large foundation models: costs and payoffs

Most teams start with frontier general models (GPT-class, Claude, Gemini) because they perform well everywhere, and their vendors already invest heavily in post-training. Tuning them aligns their broad knowledge with your context: a finance-tuned model parses domain terms and also follows your house reporting conventions; a support-tuned model keeps every reply inside corporate guidelines.

Costs to price in before committing:
- Compute: billions of parameters mean heavy GPU demand, long runs and significant cloud spend.
- Repeat cost: each retrain for new data or drift multiplies that spend.
- Latency: real-time serving can get slower.
- Infrastructure: without an in-house ML platform the barriers may be prohibitive.
- Data: often thousands of representative examples; curation and labeling are slow and can inject bias.
- Governance: without disciplined data governance and a real hold-out test set, you risk overfitting to stale or unrepresentative examples and losing generalization and fairness.

When it is worth it: accuracy-critical, nuance-heavy applications (diagnostic support in healthcare, legal analysis, complex technical support) where a tuned large model often beats smaller specialists, and where the organization can fund it. The author stresses this applies to only a small number of use cases. The chapter's examples are an introduction meant to help you judge whether deeper investment is warranted, not a full training curriculum.

## The case for small models

Small models, tuned to one well-bounded task, can match or even beat large models on that task because all their capacity goes to it. Their advantages:
- **Cost and latency:** fit where compute is tight or response time is critical.
- **Faster experiments:** short training runs allow rapid iteration over configurations, suiting agile teams and limited hardware.
- **Interpretability:** fewer layers and parameters make behavior easier to analyze, debug and validate, which matters in finance, healthcare and regulated settings (for example, a small medical image classifier is easier to audit).
- **Edge and real-time deployment:** embedded devices, mobile apps, IoT networks.
- **Frequent retraining:** cheap enough to refresh often for fast-moving data such as social sentiment, fraud patterns or personalized recommendations.
- **Federated and privacy-preserving setups:** can be tuned on edge devices across decentralized data.
- **Access:** many strong open models (Llama, Phi families) are free to modify.
- **Sustainability:** much lower energy for training and inference; fits green-AI goals.
- **Data efficiency:** with high accuracy demands but limited data, a focused small model can perform well without overfitting (for example, domain sentiment over financial reports).

Evidence of the trend cited in the chapter (early 2025): open-weight models in the 70B class exceeded 66% mean MMLU on Stanford HELM; some compact models crossed roughly 64%; a 3.8B Phi-3-mini matched the 60% MMLU of the 540B PaLM, a 142x size reduction in about two years. Mobile-focused evaluation showed sub-9B models doing well on edge tasks, with more variance as size drops.

## Picking a model size and staying current

Size tiers the chapter recommends:

| Parameters | Sweet spot |
|---|---|
| Under 8B | On-device or lowest-cost inference |
| 8B to 70B | General reasoning at moderate cost |
| Frontier proprietary | Highest-stakes accuracy |

Decide using deployment constraints (latency, hardware, budget) and task difficulty together.

The leading small-model family changes within months, so do not hard-code a favorite. Re-check periodically against third-party leaderboards: Stanford HELM (MMLU, GPQA, IFEval), Papers With Code (aggregated benchmarks and artifacts), Hugging Face evaluation results (GSM8K, HumanEval and others), and the BIG-Bench Hard leaderboard. Always confirm on your own eval set; public benchmarks only shortlist candidates.

## Decision walkthroughs

**A. Insurance claims agent, 300 labeled examples, weekly policy changes.** Domain is narrow, but data is thin and the domain moves weekly. Verdict: no fine-tune yet. Use dynamic exemplars plus an insight list, and revisit when examples reach the thousands and policy churn slows.

**B. High-volume internal agent, 40k calls/day, recurring argument mis-parsing on five tools.** Prompts are already long, failures are concentrated and measurable, traffic justifies per-call savings. Verdict: SFT for function calling on a mid-size open model, after confirming built-in function calling plus schema validation still falls short.

**C. Help-desk replies that are correct but too long and cold.** Correctness is fine; style is the gap; graders can easily pick the better of two replies. Verdict: DPO on a small model.

**D. Code-fix agent with a unit-test suite.** Tests give an automatic pass/fail reward. Verdict: RLVR candidate once SFT on known-good fixes plateaus.

## Pitfalls

- Fine-tuning to fix a problem that a better prompt, schema validation or retrieval would solve.
- Tuning before the use case is stable, then retraining every sprint.
- No migration plan, so the team is stuck on an old base model when better ones ship.
- No hold-out set, so overfitting to stale examples goes unnoticed.
- Choosing a model from a leaderboard snapshot without re-checking or testing on your own data.
