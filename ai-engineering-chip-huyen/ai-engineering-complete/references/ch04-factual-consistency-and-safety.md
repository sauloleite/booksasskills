# Factual consistency (hallucination) and safety evaluation

## Contents
- Local vs global factual consistency
- Why global checks are hard
- Method menu for factual consistency
- Choosing a factual consistency method
- Designing a hallucination evaluation set
- Factual consistency in RAG
- Safety: harm categories
- Safety: method menu
- Worked example
- Pitfalls
- Glossary

## Local vs global factual consistency

| Setting | Checked against | Typical applications | Difficulty |
|---|---|---|---|
| Local | A supplied context (document, policy, retrieved passages, data table) | Summaries, policy-bound support bots, data analysis, RAG answers | Easier: the evidence is in hand |
| Global | Open-world knowledge | General assistants, fact-checking, market research | Harder: you must find and vet evidence first |

Under local checking, an output that contradicts the world but agrees with the supplied context counts as consistent. Decide which setting your product needs before choosing a metric; most narrow-scope business apps need local checking.

## Why global checks are hard

- The hardest step is deciding what the facts are; many claims are opinions or depend on which sources you trust, and the web is full of false marketing, invented statistics and slanted posts.
- **Absence-of-evidence trap:** failing to find support for a link between X and Y is not proof that no link exists. A verifier should label such claims "unverified", not "true".
- Research on what evidence models find persuasive suggests they lean on how topically relevant a page is and mostly ignore credibility cues people rely on, such as citations or a neutral tone. Do not assume an AI verifier weighs sources the way an expert would.

## Method menu for factual consistency

1. **AI judge with context.** Ask whether the output makes claims the source does not support. Strong general models beat older metrics here; a finetuned truthfulness judge matched human labels 90 to 96% of the time. Cheapest to set up; quality depends on the rubric.
2. **Self-verification (SelfCheckGPT).** Sample N extra responses; disagreement with the original suggests hallucination. No reference needed, but N extra generations per check.
3. **Knowledge-augmented verification (SAFE).** Split the response into atomic claims, rewrite each to stand alone (resolve pronouns), issue search queries per claim, judge each claim against results. Suits global checks of long answers; expensive and bounded by search quality.
4. **Textual entailment (NLI) classifier.** Context is the premise, output or claim the hypothesis; classes are entailment (consistent), contradiction (inconsistent), neutral (undetermined). Small models (one has about 184M parameters, trained on about 764k pairs) are cheap enough for all traffic.
5. **Benchmarks.** TruthfulQA: 817 misconception-based questions in 38 categories (health, law, finance, politics); human experts score about 94%. Use it to compare models, not to certify your app.

## Choosing a factual consistency method

| Situation | Default | Upgrade when needed |
|---|---|---|
| Context available, high volume | NLI classifier per claim | AI judge on a sample |
| Context available, low volume or nuanced | AI judge with a strict rubric | Decompose into claims first |
| No context, long-form answers | Search-augmented claim checking | Human review for high-stakes slices |
| No context, no search allowed | Self-consistency sampling | Restrict scope to supply context |
| Comparing base models | Truthfulness benchmark plus your own set | |

Scoring scale options: binary (consistent or not) or three-way (entail, neutral, contradict, often mapped to 1, 0, -1). Three-way keeps "unsupported" separate from "wrong", which matters for RAG debugging.

## Designing a hallucination evaluation set

1. Read many outputs and catalogue which query types trigger hallucination. Two recurrent types:
   - **Niche knowledge:** obscure entities or rare topics (a small town's bylaw versus a famous national law).
   - **False premises:** questions assuming something that never happened (what a person said on a topic they never addressed); models tend to invent rather than reject the premise.
2. Overweight those types; random traffic under-represents them.
3. Attach context to local items; pick a method and scale from the table above.
4. Report per query type and slice, and add every new production hallucination to the set.

## Factual consistency in RAG

For retrieval-augmented systems the core check is local consistency with the retrieved context. Score retrieval separately from grounding to tell missing context from an ignored one.

## Safety: harm categories

Taxonomies differ across providers (content moderation endpoints, guard models), but most cover:

1. Inappropriate language (profanity, explicit content).
2. Harmful instructions or encouragement (crime how-tos, self-destructive behaviour).
3. Hate speech and discrimination.
4. Violence (threats, graphic detail).
5. Stereotypes (for example defaulting to one gender for a profession).
6. Political or religious bias. Studies have placed different foundation models at different points on political and economic axes depending on their training, so test for one-sided output on contested topics.

Factual inconsistency can cause harm too; it is tracked separately only because of its size.

## Safety: method menu

- **General AI judge** prompted with your taxonomy: flexible, slower, costlier.
- **Provider moderation tools** that some vendors expose.
- **Specialized toxicity and hate-speech classifiers** built for human-written text (including language-specific ones): far smaller, faster and cheaper; the default for all traffic.
- **Benchmarks:** RealToxicityPrompts (about 100k naturally occurring prompt prefixes likely to elicit toxic continuations) and BOLD (bias in open-ended generation).

Default pattern: specialized classifier on every output, general judge on flagged or sampled outputs, humans on the judge's borderline cases.

## Worked example

An insurance support bot answers from policy documents.

- Setting: local. Each answer is split into claims; an NLI model checks every claim against the retrieved clauses on all traffic.
- Any "contradiction" blocks the reply; "neutral" claims go to an AI judge with a rubric that defines what counts as an acceptable inference.
- Hallucination set: 40% questions about rarely used riders, 30% false-premise questions (coverage for a product the insurer does not sell), 30% ordinary questions.
- Safety: a small toxicity classifier on all outputs; a judge on the 2% sample plus anything flagged.
- Reported: grounding rate per slice, false-premise rejection rate, toxicity flag rate.

## Pitfalls

- Running global fact-checking when the product only needs context grounding.
- Building a hallucination set from random traffic, which hides the hard cases.
- Merging "unsupported" and "contradicted" into one label.

## Glossary

- **Self-verification:** disagreement among resampled answers as a hallucination signal.
- **False-premise query:** a question presupposing something untrue.
- **Absence-of-evidence fallacy:** reading a failed search as proof that no link exists.
