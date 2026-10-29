---
name: ai-eng-ch08-dataset-engineering
description: Guides building, sourcing, synthesizing, verifying and processing datasets for adapting foundation models (SFT, preference, reward-model, CoT, tool-use, long-context data). Use when deciding what data and how much is needed, choosing between app logs, public, annotated or synthetic data, writing annotation guidelines, generating or distilling data with LLMs, checking synthetic data, or inspecting, deduplicating, cleaning and formatting a training set. Based on Chapter 8 of Chip Huyen's "AI Engineering" (O'Reilly, 2025).
---

# Dataset Engineering (AI Engineering, Chapter 8)

Purpose: help an agent design and produce the dataset that gives the best finetuned model within budget. Application teams rarely change the model itself, so data is their main lever. The skill covers post-training data (instruction, preference, reward-model data) and borrows pre-training lessons where they transfer. Curation, synthesis and processing loop back on each other; expect to iterate.

## Key decision rules

Apply these even without opening a reference.

1. **Data shows the behavior.** Whatever examples demonstrate (verbosity, reasoning steps, tool calls, unsolicited advice) the model learns. Trace each unwanted behavior to the examples that teach it; remove them and add counter-examples.
2. **Format follows phase.** Self-supervised: raw sequences (counted in tokens). SFT: (instruction, response) (counted in examples). Preference: (instruction, winner, loser). Reward model: preference triplets or ((instruction, response), score).
3. **Three criteria, none substitutes for another:** quality, coverage, quantity.
4. **Quality = six checks:** relevant, aligned with task requirements (aligned beats merely correct), consistent across annotators, correctly formatted, sufficiently unique, compliant. Define each for the task before collecting.
5. **Small and curated beats big and noisy** (about 1K to 10K curated examples have beaten far larger noisy sets), but very small sets are less robust.
6. **Coverage = the diversity axes your users actually vary on** (task, topic, format, length, language, typos, turns). Mirror real usage; adding heterogeneous data blindly can hurt.
7. **Size by technique and base model.** Hundreds to a few thousand examples: PEFT on the strongest base model. Tens of thousands to millions: consider full finetuning, possibly of a smaller model. Millions: also test training from scratch (ossification). Stronger base models need fewer examples; with very large sets, base model differences shrink.
8. **Pilot with 50 to 100 good examples.** Clear gain: more data will help. No gain: check learning rate, data quality and prompts before blaming data size; a bigger set rarely rescues a flat pilot.
9. **Fit a scaling curve** on 25/50/100% subsets before buying more data; expect diminishing returns.
10. **Prefer your own application data** (it matches the target distribution); check existing datasets before creating any; never trust a public dataset or its top-level license without inspecting sub-sources.
11. **One annotation guideline** for training and evaluation. Never abandon it midway.
12. **Synthesize what you can verify.** Functional checks first (execution, tests, back-translation), then AI verifiers, factual-consistency filters, topic and anomaly filters, heuristics. Final test: does it improve the model?
13. **Synthetic data complements human data.** All-synthetic recursive training risks model collapse; always mix in real data (no proven safe ratio). Never retrain on self-generated outputs without a verification gate.
14. **Imitation is shallow.** Distilled students copy style more than capability; teaching answers the student cannot derive (from a teacher or a human) teaches hallucination. Check model licenses before training on outputs.
15. **Track lineage** of every generated example (generator, prompt, date); generator copyright problems and benchmark exposure transfer to you.
16. **Judge preference pairs twice with order swapped**; keep only consistent verdicts.
17. **Processing hygiene:** order steps by cost, trial-run scripts on a sample, never modify data in place, deduplicate before splitting, read raw examples by hand.
18. **Formatting must match exactly** at training and inference: the model's chat template, and the same prompt shape (a missing separator or a trailing space can break a finetuned model). Drop prompt-era task descriptions and few-shot demos; turn the demos into training rows.

## Default workflow

1. List behaviors to learn and unlearn; pick training phase, example format, single vs multi-turn.
2. Define the six quality checks and the coverage axes for this task; draft the annotation guideline.
3. Run a 50 to 100 example pilot; if it helps, fit a subset scaling curve and set the size and the data/compute budget split.
4. Acquire: app data, then existing datasets (license and provenance checks), then annotation, then targeted synthesis for coverage gaps.
5. Verify every synthetic or annotated batch; record lineage; keep a real-data anchor.
6. Process: inspect (run `inspect_jsonl.py`), measure agreement (`annotator_agreement.py`), deduplicate (`minhash_dedup.py`), clean and filter, format with the exact chat template.
7. Train, evaluate on uncontaminated data, trace failures back to examples, iterate.

## References

Read only the file that matches the current task.

- [references/curation-quality-and-coverage.md](references/curation-quality-and-coverage.md): read when choosing example formats, preparing CoT, tool-use or multi-turn data, defining quality criteria, or choosing diversity axes and data mix per phase.
- [references/quantity-acquisition-and-annotation.md](references/quantity-acquisition-and-annotation.md): read when sizing a dataset, interpreting a pilot or scaling curve, choosing PEFT vs full finetuning vs from scratch, planning staged finetuning, picking data sources, finding public datasets, or writing annotation guidelines.
- [references/data-synthesis-techniques.md](references/data-synthesis-techniques.md): read when generating or augmenting data (templates, perturbation, counterfactuals, simulation, self-play, paraphrase, translation, reverse instruction, long-context data, code pipelines, AI-judged preference pairs).
- [references/verification-limits-and-distillation.md](references/verification-limits-and-distillation.md): read when filtering synthetic or annotated data, assessing collapse, bias, imitation or lineage risks, or planning distillation or self-training.
- [references/data-processing.md](references/data-processing.md): read when inspecting a raw dataset, defining and running deduplication, cleaning PII and markup, pruning to budget, or formatting for a chat template and matching inference prompts.
- [references/source-map.md](references/source-map.md): read to find which reference covers a given chapter section.

## Scripts

All scripts use the Python 3 standard library only, are deterministic, and print `--help`.

- Run `python3 scripts/inspect_jsonl.py data.jsonl --key instruction --target response --reverse` to compute a dataset inspection report: row and parse-error counts, per-field missing/empty/type counts, character and word length percentiles with a histogram, exact duplicate rows, duplicate instructions, same instruction with different responses, and same response for different instructions. Add `--json` for machine-readable output.
- Run `python3 scripts/minhash_dedup.py data.jsonl --fields instruction response --threshold 0.8 --keep-out dedup.jsonl --clusters-out clusters.json` to find near-duplicate clusters with MinHash and LSH, confirm each candidate pair by exact shingle Jaccard, and write a deduplicated file that keeps the first row per cluster. Tune `--shingle`, `--num-perm` and `--bands`; the report prints the similarity at which LSH candidate recall rises steeply.
- Run `python3 scripts/annotator_agreement.py a.jsonl b.jsonl --weights quadratic` to compute observed agreement, chance agreement and Cohen's kappa (unweighted, linear or quadratic weighted for ordinal scores) between two annotators, with label distributions, a confusion matrix and the list of disagreeing items to resolve. Accepts JSONL or CSV with `id` and `label` columns, or plain text with one label per line.
