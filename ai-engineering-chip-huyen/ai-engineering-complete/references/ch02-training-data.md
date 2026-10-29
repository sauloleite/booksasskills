# Training Data: Coverage, Languages, Domains

## Contents
- Core principle and where data comes from
- Quality versus quantity
- Multilingual coverage: the gap and its symptoms
- Translation bridges and language-specific models
- Domain coverage and domain-specific models
- Inferring coverage when nobody publishes it
- Decision playbook
- Worked example
- Pitfalls and glossary

## Core principle and where data comes from

Model differences trace back to training data, architecture and size, and post-training. Data is the easiest of these to reason about when predicting weakness: if a task, language or format was rare on the public web, expect the model to be weak until proven otherwise.

- Builders mostly use what is available. Common Crawl (a nonprofit crawl capturing a few billion pages per month in 2022 and 2023) and C4, Google's cleaned subset, dominate.
- The crawl holds plenty of untrustworthy content (clickbait, propaganda, conspiracies, bigotry); several of its most frequent news sites rate poorly for trustworthiness.
- Most models that disclose sources (GPT-3, Gemini) use Common Crawl variants; many labs no longer disclose, so assume opaque provenance.
- Cheap filters reward popularity, not quality (GPT-2 used Reddit links with three or more upvotes).
- Result: strong performance on what the crawl over-represents, not necessarily on your task. Curate data for your language, domain or task, either training from scratch or, more often, finetuning a general model.

## Quality versus quantity

More data costs more compute and does not guarantee better results. A 1.3B coding model trained on about 7B tokens of high-quality code beat far larger models on several coding benchmarks. Aim for quantity, quality and diversity together.

## Multilingual coverage: the gap and its symptoms

English is about 46% of Common Crawl, roughly eight times Russian (about 6%). Only around a dozen languages pass 1%; those below are generally low-resource.

Diagnostic: divide a language's share of world population by its share of the crawl. A value near 1 is proportional; English sits well below 1. Punjabi exceeds 200, Swahili and Urdu exceed 100, and Kannada, Telugu, Gujarati, Marathi and Bengali range from about 35 to 65 despite huge speaker counts.

Symptoms to expect:
1. **Lower quality.** GPT-4 scored clearly worse on translated MMLU in Telugu than in English, solved Project Euler problems over three times as often in English as in Armenian or Farsi, and solved none in Burmese or Amharic. The weakest MMLU languages are among the least represented, though language structure and culture also make some languages harder.
2. **Different safety behavior.** ChatGPT-3.5 refused six of seven English requests for false claims about China but complied every time in both Chinese scripts. The cause is unknown.
3. **More tokens.** On MASSIVE, median length was about 7 tokens in English, 32 in Hindi and 72 in Burmese for equivalent text.
4. **Higher latency and cost**, proportional to tokens: Burmese costs about ten times English for the same meaning.

## Translation bridges and language-specific models

Translating to English and back is common but weak: the model must still understand the source language, and translation drops meaning (Vietnamese pronouns encode speaker relationships that collapse to "I" and "you"). Use only as a verified stopgap.

Language-specific models exist, most actively for Chinese (ChatGLM, YAYI, Llama-Chinese) and also French (CroissantLLM), Vietnamese (PhoGPT) and Arabic (Jais). Check before building.

## Domain coverage and domain-specific models

General models handle everyday questions in coding, law, science, business and sports because those topics are on the web. A domain breakdown of C4 only shows what is present, not what is missing.

They are unlikely to handle tasks whose data never reached the web: drug discovery (protein, DNA, RNA data, costly and specially formatted) and cancer screening (X-ray and fMRI scans, restricted by privacy). These need curated datasets: AlphaFold learned from roughly 100,000 known proteins with their structures, BioNeMo targets biomolecular drug discovery, and Med-PaLM 2 pairs an LLM with medical data. Biomedicine leads, but architectural sketches or factory plans could likewise justify specialized models.

## Inferring coverage when nobody publishes it

- Text: domain keyword heuristics give a rough mix.
- Vision: distribution analyses are rare (images are hard to categorize, and published analyses focus on resolution or length). Infer coverage from per-category benchmarks: CLIP and OpenCLIP score alike on ImageNet but diverge sharply on cars, traffic signs and bird species. A few categories say little about the rest of the visual world.

## Decision playbook

1. Build a small set of real queries in the target language or domain, plus English equivalents.
2. Measure the quality gap.
3. Count tokens with the provider's tokenizer and project cost and latency.
4. Run safety probes in the target language.
5. Prefer, in order: an existing specialized model, a finetune on curated data, a translation bridge (only if the source is well understood and nothing meaning-bearing is lost).
6. For proprietary formats, plan for a specialized model or heavy adaptation from the start.

## Worked example

A support bot serves Hindi and English equally. Sampled Hindi messages average 4.5 times the tokens of their English translations, so Hindi traffic costs about 4.5 times more and generates more slowly. Tests also show a 15-point accuracy gap and weaker refusals. A translation bridge cuts cost but strips honorifics that set tone, so the team finetunes on curated Hindi data and re-runs safety probes.

## Pitfalls and glossary

Pitfalls: budgeting with English token counts; using English benchmarks as a proxy; assuming safety tuning is language-independent; expecting general models to read proprietary formats; assuming more data always helps.

- **Low-resource language**: little available training data, roughly under 1% of Common Crawl.
- **Under-representation ratio**: population share over crawl share; far above 1 signals weakness.
- **Translation bridge**: answering through an English pivot.
