# Data Augmentation and Synthesis Techniques

## Contents
- Augmentation vs synthesis
- Five reasons to synthesize
- Traditional techniques: rules and templates
- Traditional techniques: transformations, perturbation, counterfactuals
- Traditional techniques: simulation
- AI-powered simulation: APIs and self-play
- Paraphrasing and translation
- Where synthetic data goes: pre-training vs post-training
- Preference data with AI judges
- Instruction data synthesis
- Reverse instruction and bootstrapping
- Long-context data
- Case study: a verified code-data pipeline
- Choosing a method
- Glossary

## Augmentation vs synthesis

Augmentation derives new examples from real ones (a flipped cat photo is still a cat). Synthesis manufactures examples that imitate real data without being real (simulated mouse trajectories that resemble a bot). Because both aim to automate data creation, people use the terms loosely; below, "synthesis" covers both. Synthetic data reduces, but does not remove, the need for human data. Mixed human and AI data usually gives the best value.

Fake-data tools (Faker, Chance) long predate LLMs in software testing; modern models extend generation to clinical notes, contracts, financial statements and media.

## Five reasons to synthesize

| Reason | What it buys | Examples |
|---|---|---|
| Quantity | Scale where real data is scarce or dangerous | rare weather, deep-sea data, car accidents |
| Coverage | Targeted traits and behaviors | extreme lengths; toxic or detoxified text; adversarial examples; rare classes; deliberately inconsistent summaries for an inconsistency detector (TrueTeacher) |
| Quality | Sometimes beats human data | agent-efficient tool traces; harder math problems; preference ratings more consistent than humans, who vary by person and mood |
| Privacy | The only option when real records are off-limits | synthetic patient records; synthetic insurance claims |
| Distillation | A cheaper, faster imitator of a stronger model | student trained on teacher outputs |

Anthropic's model-written evaluations (154 behaviors) came close to, sometimes beat, human-written datasets. AI-content detectors require synthetic data by definition.

## Traditional techniques: rules and templates

Also called procedural generation (as in games that build levels, maps and worlds algorithmically). Define a template with typed slots and fill them with a random generator.
- Good for structured documents: invoices, resumes, tax forms, bank statements, agendas, catalogs, contracts, config files.
- Good for grammar-bound data: regular expressions, math equations. AlphaGeometry reached Olympiad level using 100 million synthetic examples.
- Common feasibility path for sensitive domains: fraud models are prototyped on template-generated transactions before getting access to real ones.

## Traditional techniques: transformations, perturbation, counterfactuals

- **Label-preserving transforms.** Images: rotate, crop, scale, erase (AlexNet). Text: swap in near-synonyms from a thesaurus or embedding neighbors if meaning and sentiment survive.
- **Counterfactual swaps for bias.** Generate twins with swapped pronouns, titles, family roles or culturally marked names to break spurious associations.
- **Perturbation.** Add noise to create examples and harden the model. Tiny changes fool models (a one-pixel attack misclassified about 68% of CIFAR-10 and 16% of ImageNet test images), a real security risk. Training on perturbed data improves robustness and sometimes accuracy (ImageNet-C/P use 15 corruptions; BERT randomized 1.5% of tokens for a small gain).
- **Sophisticated visual augmentation.** Snap generated variants of characters across skin tones, body types, hair, clothing and expressions to cover under-represented cases.

## Traditional techniques: simulation

Simulate when reality is costly or dangerous: a horse on a highway for self-driving (CARLA, Waymo SimulationCity), or robot trajectories where only successful simulated pours become training data.
- Asymmetry: simulated success does not guarantee real success, but simulated failure predicts real failure. Sim2Real closes the gap.
- Tool use: simulate several action sequences per query, execute, verify outcomes, and keep the most efficient success as the label.
- Rare events: IPOs and bankruptcies, manufacturing defects, extreme weather.

## AI-powered simulation: APIs and self-play

- **Simulated APIs.** A model can predict a call's result without executing it (StableToolBench), useful when real calls are slow or expensive.
- **Self-play.** Model instances play each other: OpenAI's Dota 2 bot accumulated about 180 years of games per day; AlphaGo used millions of self-played Go games. For general agents: negotiators with different strategies, or one instance as a frustrated customer and another as support.

## Paraphrasing and translation

- **Paraphrase** existing queries to multiply phrasings. MetaMath rewrote about 15,000 MATH and GSM-8K problems into nearly 400,000 and outperformed larger models on related benchmarks.
- **Translate** from high-resource into low-resource languages (for example Quechua or Lao) to train small specialist models.
- **Verify with back-translation**: translate X into Y, have a different model translate Y back to X', compare X' to X. Large divergence flags a bad translation.
- **Code translation** spreads an SFT set across programming languages (Llama 3 did this). Code back-translation verifies generated explanations and docs: generate docs from code, regenerate code from the docs, keep the docs only if the regenerated code matches the original.

## Where synthetic data goes: pre-training vs post-training

Synthesis concentrates in post-training: pre-training aims to add knowledge, which models reformat more easily than create, while post-training data is the most labor-intensive to produce. Web corpora already contain AI text anyway, and synthetic pre-training corpora exist (Cosmopedia, 25B tokens).

## Preference data with AI judges

Using a judge to choose between responses is straightforward; the main risk is judge bias, especially preferring whichever response comes first. Mitigation used by NVIDIA: ask twice with order swapped, and keep the (prompt, winner, loser) triplet only if the same response wins both times.

## Instruction data synthesis

Either side of a pair can come from AI or humans: AI instructions with human responses, or human instructions with AI responses.
- **Instruction generation**: start from a list of topics, keywords or instruction types (or templates), and generate a fixed number per item. The list and templates can themselves be AI-generated.
- **Response generation**: one or several responses per instruction (several lets you rank and keep the best or build preference pairs).

Patterns: a topic tree (UltraChat: 30 topics, 30 to 50 subtopics each, dialogues per subtopic) or seed expansion (Alpaca: 175 seed pairs grown to 52,000 with text-davinci-003).

Keep per-template or per-leaf counts modest; too many generations from one prompt converge to near-duplicates.

## Reverse instruction and bootstrapping

Long responses are where models hallucinate most. Reverse instruction flips the job: take high-quality human long-form content (stories, books, Wikipedia) and have a model write the prompt that would elicit it, so only the cheap side is synthetic.

Bootstrapping loop (instruction backtranslation, Li et al. 2023):
1. Train a weak model on a few seed pairs.
2. Use it to write instructions for unlabeled high-quality text.
3. Finetune on the new pairs.
4. Repeat until the target is reached.

In principle this allows continual self-improvement without new human labels; whether it keeps working in practice is unproven.

## Long-context data

To extend a model from, say, 8K to 128K tokens:
1. Split long documents into chunks that fit the current window.
2. Generate several QA pairs per chunk.
3. Train with the full document (longer than the old window, within the new one) as context for each pair.

The answer depends on a local chunk, but the model must find it in the long context. Check that examples genuinely need the extended context.

## Case study: a verified code-data pipeline

Llama 3's synthetic data was mostly code because code is checkable. Combined with translation and back-translation, this workflow yielded over 2.7 million SFT examples for Llama 3.1:
1. Generate diverse problem statements.
2. Generate solutions per language; good-practice rules and CoT in the prompt helped.
3. Parse and lint; then run model-generated unit tests.
4. On failure, re-prompt with problem, faulty code and tool feedback (about 20% of solutions were fixed this way).
5. Translate passing code to other languages; drop translations that fail tests.
6. Generate explanations and docs; drop those failing back-translation.

Only fully passing examples are kept. Reuse this shape wherever an executable oracle exists (SQL against a fixture DB, regex against test strings, math checkers).

## Choosing a method

| Need | Method |
|---|---|
| Structured or grammar-bound records | templates plus fakers |
| Invariance and robustness | transforms, perturbation |
| Fairness gaps | counterfactual swaps |
| Rare or hazardous events | simulation |
| Efficient agent trajectories | simulate, execute, keep the best path; simulated APIs |
| Multi-party behavior | self-play / role-play |
| More phrasings | paraphrase |
| Low-resource language | translate plus back-translation check |
| Long, high-quality answers | reverse instruction |
| Longer context window | chunk-QA with full-document context |
| Preference pairs | AI judge with order-swap consistency |
| Privacy-restricted domain | fully synthetic records |

Whatever the method, verify before training (see the verification reference).

## Glossary

- **Sim2Real**: transferring simulation-trained behavior to the physical world.
- **Reverse instruction**: writing prompts for existing human content.
- **First-position bias**: a judge's tendency to favor the first option shown.
