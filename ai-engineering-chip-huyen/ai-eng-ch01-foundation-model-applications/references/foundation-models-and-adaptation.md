# Foundation Models, Adaptation, and Why AI Engineering Exists

Covers the chapter's opening arc: language models, tokens, self-supervision, model size, the move to multimodal foundation models, the three adaptation techniques, and the three forces behind the rise of AI engineering. Use it to correct terminology, set realistic expectations about what a model is, and frame build-vs-adapt conversations.

## Contents
- The scale thesis
- Language models as completion engines
- Tokens: practical arithmetic and gotchas
- Masked vs autoregressive models
- Self-supervision and why it unlocked scale
- Model size and data needs
- From LLMs to foundation models
- Adapting a general model: prompting, RAG, finetuning
- Why AI engineering took off: three forces
- Choosing the name "AI engineering"
- Worked examples
- Pitfalls
- Glossary

## The scale thesis

The organizing idea is that scale changed everything after 2020, with two effects:

1. **Capability expansion.** Bigger models handle more kinds of tasks, so more applications become feasible and demand rises.
2. **Concentration of model building.** Only a few actors (big tech, some governments, heavily funded startups) can pay for frontier training. They sell access as a service, so everyone else builds without the training bill.

Higher demand plus a lower barrier is the causal story for AI engineering. Applying ML in products is old (recommendations, fraud, churn); what is new is the scale and availability of general models, bringing new possibilities and failure modes while many productionization principles carry over.

## Language models as completion engines

A language model stores statistics about which token is likely in a given context (an idea as old as frequency-based codebreaking and Shannon's entropy work). Treat it as something that continues text:

- **Many tasks reduce to completion.** Translation, summarization, code, math and classification can be phrased as a prefix to continue; a spam classifier can be a prompt ending in an "Answer:" slot.
- **Completion is not conversation.** A raw completer may answer a question with another question; assistant behavior comes from post-training.
- **Outputs are probabilistic predictions**, not guarantees. That property makes models creative and frustrating; design assuming some outputs are wrong.

## Tokens: practical arithmetic and gotchas

- A token may be a character, a word, or a fragment such as a suffix. The vocabulary is the fixed token set chosen by the model developer (about 32k for Mixtral 8x7B, about 100k for GPT-4), so token counts do not transfer between models.
- Rule of thumb for GPT-4-class tokenizers: one token is about 0.75 of an English word, so tokens is roughly words / 0.75. Use it for quick latency and cost estimates.
- Contractions and rare words split into several tokens; in non-English text one Unicode character can take several tokens, raising cost and latency.

Why tokens: fragments carry meaning (stem plus suffix), the vocabulary stays smaller than a word list, and invented words still decompose into known pieces.

## Masked vs autoregressive models

| | Masked (e.g. BERT) | Autoregressive / causal |
|---|---|---|
| Predicts | Missing tokens anywhere | Next token only |
| Context used | Both sides of the gap | Only preceding tokens |
| Typical use | Classification, sentiment, tasks needing whole-context understanding (e.g. spotting a bug requires code before and after it) | Text generation; can keep producing tokens indefinitely |
| Popularity today | Niche for non-generative tasks | Dominant; "language model" in the book means this type |

Decision hint: if the task is a fixed-label judgment on a whole input and volume or cost matters, a masked or small task-specific encoder can still be the right tool. For anything generative, use an autoregressive model.

## Self-supervision and why it unlocked scale

Supervised learning needs labeled examples (fraud or not; one of a thousand ImageNet classes), and labels are the bottleneck:

- Cost scales with volume and redundancy: at a few cents per image, a million images costs tens of thousands of dollars; double annotation doubles it; moving toward a million classes pushes it into the tens of millions.
- Cost scales with expertise: everyday objects are cheap, rare-language translations pricier, expert medical reads extremely expensive. Per-label prices also fall with volume (vendor tiers can differ fourfold).

In language modeling the text supplies its own targets: each prefix is an input and the following token its label, so one sentence yields one training pair per token plus one for the end marker. Start and end markers let the model handle many sequences; the end marker teaches it when to stop.

Keep three terms distinct: **supervised** (human labels), **self-supervised** (labels derived from the data), **unsupervised** (no labels). Because raw text is everywhere, self-supervision made huge datasets, and hence LLMs, possible.

## Model size and data needs

- Size is measured in parameters ("weights" now loosely covers all of them); more usually, not always, means more capacity.
- "Large" moves: about 117M parameters was large in 2018 and small a year later; around 100B was large when the book was written.
- Bigger models need more data to reach their potential. Training a big model on a small dataset wastes compute; a smaller model would do as well or better. The goal is maximizing performance, not matching a small model with fewer examples.

## From LLMs to foundation models

Two shifts define a foundation model:

1. **Modality unification.** Research used to be siloed (NLP, vision, speech). A generative multimodal model (LMM) predicts the next token conditioned on text plus image or other tokens. The book's "foundation model" covers LLMs and LMMs.
2. **Task generality.** A sentiment model could not translate; a foundation model does many tasks acceptably out of the box and can be tuned for one.

Self-supervision extends to multimodal data: CLIP learned from about 400M web image-caption pairs (roughly 400x ImageNet, no manual labels), a variant called natural language supervision, and was the first model to generalize across many image classification tasks without extra training. CLIP is an embedding model, not a generator; such joint embeddings are backbones for generative multimodal systems (Flamingo, LLaVA, Gemini).

## Adapting a general model: prompting, RAG, finetuning

Running example: a retailer's product descriptions come out accurate but off-brand or full of generic marketing filler. Three levers:

| Lever | What changes | Example move | Typical data need |
|---|---|---|---|
| Prompt engineering | Only the input | Detailed instructions plus sample descriptions in the brand voice | A handful of examples |
| RAG | Input filled from a data source at request time | Pull relevant customer reviews into the context | A searchable corpus |
| Finetuning | The weights | Further train on curated strong descriptions | Many curated examples |

Adapting a strong model is dramatically cheaper than building one (roughly ten examples and a weekend versus a million examples and half a year). Counterweight: task-specific models can be much smaller, hence faster and cheaper per call. Build vs adapt is a case-by-case buy-or-build call.

## Why AI engineering took off: three forces

1. **General-purpose capability.** Models do old tasks better and new tasks at all. Since they write roughly at human level, anything involving communication (most work) can be partly automated: emails, support replies, contract explanations, marketing images and video, synthetic data, code.
2. **Investment surge.** After ChatGPT, venture and enterprise spending jumped as cheaper, faster builds improved ROI. One practitioner saw his AI costs fall about 100x in a year (2022 to 2023); forecasts put 2025 AI investment near $100B in the US and $200B globally; AI mentions in S&P 500 earnings calls tripled in a year (stock gains correlated, causation unclear).
3. **Low entry barrier.** Model-as-a-service puts a strong model behind one API call with no hosting; AI writes code for non-engineers; models are programmed in plain language.

Momentum signals: four open source tools (AutoGPT, Stable Diffusion web UI, LangChain, Ollama) out-starred Bitcoin on GitHub in about two years. As an OpenAI executive argued, the biggest opportunity for most people is adapting existing models, not training new ones.

## Choosing the name "AI engineering"

The author rejected "ML engineering" (foundation model work differs materially, though ML engineering can be the umbrella) and Ops-suffixed names (the core activity is engineering model behavior, not only operating it); a small practitioner survey favored "AI engineering".

## Worked examples

**Correcting terminology.** A stakeholder says "we trained the model on our policy PDFs" when they pasted the PDFs into the prompt. That is prompt engineering (context), not training: no weights changed, no training data pipeline exists, and swapping the model will not carry the "training" over. Their cost and data plans should reflect that.

**Picking a lever.** A legal team wants answers grounded in this week's contract amendments. The knowledge is private and changes weekly, so RAG is the first move; finetuning would bake in stale facts and require retraining each week.

## Pitfalls

- Treating a completion as a fact, or expecting a base model to converse rather than continue.
- Reusing token estimates across models or languages.
- Calling self-supervision "unsupervised", or context stuffing "training".
- Training an oversized model on a small dataset when a smaller one would match it.
- Assuming a general model always wins; at high volume on a narrow task a small model can be cheaper and faster.

## Glossary

- **Generative model:** produces open-ended outputs from a finite vocabulary.
- **BOS / EOS:** special tokens marking sequence start and end.
- **Natural language supervision:** using text that accompanies another modality (captions) as its labels.
- **LMM:** large multimodal model, generative over several modalities.
- **Embedding model:** outputs meaning-bearing vectors rather than generated content.
