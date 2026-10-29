# Verifying Data, Limits of AI-Generated Data, and Distillation

## Contents
- Principle: synthesize what you can verify
- Verification toolbox, strongest first
- Heuristic filters
- The final test
- Limitation 1: quality control
- Limitation 2: superficial imitation
- Limitation 3: model collapse and bias amplification
- Limitation 4: obscured lineage
- Model distillation
- When synthetic training is not distillation
- Training on self-generated data
- Verification and provenance checklist
- Glossary

## Principle: synthesize what you can verify

Teams synthesize the data they can verify, which is why code is the most common synthetic domain: it executes. Most of Llama 3's synthetic data was code, checked by execution or back-translation. Plan synthesis backward from the verifier. These checks apply to any training data.

## Verification toolbox, strongest first

1. **Functional correctness.** Execute, test, compare to a known answer, or round-trip (back-translation). Prefer this whenever an oracle exists.
2. **AI verifiers.** A general judge or specialized scorer. Framings, simplest first: score 1 to 5; classify good vs bad; give the model the explicit quality requirements and ask whether the example meets each one. The requirement-list framing is easiest to audit.
3. **Factual consistency checks.** If facts matter, run hallucination or inconsistency detectors and drop examples likely to contain fabrications.
4. **Discriminators.** If synthetic data should mimic real data, train a detector to separate them; easy separation means the synthetic data is not realistic enough. If it should meet a quality bar, train a classifier for that bar (for example, would a generated paper be accepted at a top venue) and drop clear rejects.
5. **Topic classification.** Label each example's topic and drop off-task ones.
6. **Anomaly detection.** When data should follow a common pattern, outliers are often low quality; review or drop them.

Worked example, 20,000 synthetic support dialogues: rules drop dialogues under 3 turns; a requirement-list judge keeps only those citing policy and never over-promising refunds; a topic classifier drops unsupported intents; a real-vs-synthetic detector near AUC 1.0 means the generator needs more variation (typos, partial info); a 200-item human spot check per batch estimates residual error.

## Heuristic filters

Cheap and effective; derive more by reading data.
- Remove empty or too-short items; truncate or drop overlong items.
- Filter by keyword, author or user, creation date, metadata or source.
- Self-Instruct's filters: drop repeated items, instructions outside a length band, one instruction paired with conflicting responses, and outputs that just echo the input.

## The final test

Evaluation of generated data is still hard. The decisive check is downstream: does adding it improve the model on your evaluation set? Synthetic data has passed that test for many published models, but run it for yours with an ablation (with vs without the synthetic slice).

## Limitation 1: quality control

Generated data can be poor, and teams avoid what they cannot verify; reliable data-evaluation metrics are the bottleneck.

## Limitation 2: superficial imitation

Imitation models can match a teacher's style while lagging on factual accuracy and on tasks outside the training distribution ("The False Promise of Imitating Proprietary LLMs"). Worse, imitation can teach hallucination: if the teacher can solve hard math and the student cannot, training on the teacher's solutions teaches the student to emit solution-shaped text it cannot back up. The same happens with humans: when a labeler answers using knowledge the model lacks, the label teaches the model to make things up. The cited authors conclude that real reasoning gains come mainly from better base models.

Guards: filter teacher outputs to problems the student can plausibly solve (or put the needed facts in context), and evaluate students on factuality and out-of-distribution sets, not only style-sensitive judges.

## Limitation 3: model collapse and bias amplification

**Model collapse.** Training recursively on generated data can cause irreversible degradation, shown for VAEs, Gaussian mixture models and LLMs, in both pre-training and post-training. Likely mechanism: generators over-produce probable outcomes and under-produce improbable ones (no-cancer cases over cancer cases), so each generation thins the tails until rare events vanish.

What is known: collapse looks inevitable with fully synthetic training and avoidable when real data is mixed in (Gerstgrasser et al.; Bertrand et al.; Dohmatob et al.), yet no study gives a safe ratio. Large synthetic shares have worked (synthetic math nearly matched real data for Llama 2-7B with no saturation near a million samples; Nemotron-4 340B-Instruct used 98% synthetic post-training data), but only for a single iteration.

**Bias amplification.** When a model's outputs re-enter its training data, its existing biases can grow over iterations. The loop is more stable when outputs faithfully reflect the original training distribution. Watch this whenever production outputs feed back into training (including flywheels built on accepted suggestions).

Guards: keep a real-data anchor, protect rare classes, track rare-class recall across iterations, and tag every row's origin.

## Limitation 4: obscured lineage

Generated data hides its origins, and generators can regurgitate their training data. If generator X saw infringing material, your model may inherit the infringement; if X saw benchmark B, your score on B may be contamination. Record per example the generator and version, prompt template, seed source and date, and prefer evaluation sets built after choosing the generator.

## Model distillation

Distillation trains a small student to mimic a large teacher; generated data is the method itself.
- Classic goal is cheaper deployment: DistilBERT is 40% smaller than BERT, keeps 97% of its language understanding and is 60% faster.
- The student can start from random weights (DistilBERT) or from an existing pre-trained checkpoint (Alpaca: Llama-7B on text-davinci-003 outputs, at about 4% of the teacher's size).
- Synthetic instructions pair naturally with LoRA: BuzzFeed's LoRA-tuned Flan-T5 cut inference cost 80%, with quality unreported. Always pair cost wins with a quality evaluation.
- **License check first**: many model terms forbid training other (especially competing) models on their outputs.

## When synthetic training is not distillation

Distillation assumes the teacher's quality is the student's ceiling. Synthetic data can also produce a student stronger than the data generator:
- Bootstrapping with reverse instruction (a weak model labeling human-written text) improves beyond its starting point.
- NVIDIA pre-trained a 340B base model and finetuned it on Mixtral-8x7B-Instruct outputs for both instruction and preference data (a mixture-of-experts model with far fewer total parameters). The resulting Nemotron-4-340B-Instruct beat the generator on many tasks. Parameter counts of MoE and dense models are not directly comparable, but the generator was still the smaller model.

Decision rule: if your plan relies on the student exceeding the generator, you are not distilling; you need a strong base model and a filtering mechanism that selects data better than the generator's average output.

## Training on self-generated data

Llama 3 found that data from a more capable model helps substantially, but training indiscriminately on a model's own outputs does not help and can hurt. With verification in place and only verified samples kept, they kept improving the model on its own generations. Rule: never feed self-generated data back without a verification gate.

## Verification and provenance checklist

- [ ] Verifier chosen before generating; functional checks wherever an oracle exists
- [ ] Judge prompts list explicit requirements; preference judgments order-swapped
- [ ] Real data mixed in; origin, generator, prompt and date recorded per row
- [ ] Generator license allows training on outputs; eval sets checked for generator exposure
- [ ] Ablation shows the synthetic slice helps

## Glossary

- **Superficial imitation**: student copies teacher style but not capability.
- **Model collapse**: degradation from recursive training on generated data, losing rare events first.
- **Data feedback loop**: model outputs re-entering training data, amplifying bias.
- **Data lineage**: traceable origin of each example, including which models produced it.
