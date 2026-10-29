# Data Processing: Inspect, Deduplicate, Clean, Format

## Contents
- Operating rules for processing pipelines
- Inspect: statistics, slices, annotators, manual reading
- Deduplicate: why, what counts, how
- Clean and filter
- Prune when data exceeds budget
- Format: templates, slimmer instructions, inference parity
- End-to-end processing checklist
- Glossary

Treat these steps as a menu. Model papers that disclose dataset details (Llama 3, Nemotron, Self-Instruct) are rich sources of processing tricks.

## Operating rules for processing pipelines

Each step can take hours or days at scale.
1. **Order steps by cost.** If cleaning one example is costlier than deduplicating, dedupe first so you clean less. If dedup is the expensive step, run cheap quality filters first so dedup sees fewer rows.
2. **Trial-run every script** on a small sample and inspect outputs before running on everything.
3. **Never modify data in place.** Keep the original: other teams or applications may need different processing, and a buggy script can corrupt data irrecoverably. Write each stage to a new versioned location.

## Inspect: statistics, slices, annotators, manual reading

Start every raw dataset by documenting its history: origin, every transformation already applied, and prior uses (including whether it fed any benchmark you plan to use).

**Distributions to plot**
- Token frequency (what is common), input lengths, response lengths.
- Special tokens present, and whether they collide with your model's template tokens.
- Topic and language distributions, and their relevance to the task.

**Creative statistics.** Invent statistics that expose differences. Microsoft researchers compared GPT-3 and GPT-4 generations on the same instructions by counting which verbs paired with which object nouns, plus response lengths; GPT-4 showed more varied pairings and longer answers. Such statistics evaluate models as well as data.

**Slice everything** by source, time and annotator. Look for question patterns with systematically longer, shorter, higher- or lower-scored answers; explain outliers before deciding their fate; check each annotator's score distribution (some skew short or high) and decide whether to recalibrate or drop their work.

**Agreement.** When items have multiple annotations, compute inter-annotator disagreement (for categorical labels, Cohen's kappa for two annotators). Review conflicting items, resolve them, and feed recurring conflict patterns back into the guideline.

**Read the data.** Tools do not replace reading rows; the author reports fifteen minutes of looking routinely saves hours. Annotate a handful yourself and compare with the given labels, fact-check responses, and look for same query with different responses or same response for different queries.

## Deduplicate: why, what counts, how

**Why it matters**
- Duplicates skew the distribution into spurious rules (three copies of "red pencil, $20" vs one "green pencil, $1" can teach that red means pricey) and leak across train/test splits.
- Repeating 0.1% of data 100 times dropped an 800M model to roughly 400M-model quality although 90% of tokens stayed unique (Hernandez et al., 2022); other studies agree. At best, duplicates waste compute.

**Kinds of duplication in document data**
- Whole-document: a document appears more than once.
- Intra-document: a paragraph repeats inside one document.
- Cross-document: the same passage (a popular quote, a boilerplate disclaimer) recurs across documents.

**Define "duplicate" before running anything**
- Granularity: document, paragraph, sentence or token span.
- Strictness: exact match, or a threshold such as 80% overlap.
- Order: are two lists with the same items in different order duplicates?

**Methods**

| Method | How | Trade-off |
|---|---|---|
| Pairwise comparison | similarity of every pair via exact, n-gram, fuzzy or embedding similarity | most flexible, quadratic cost; fine for thousands, painful for millions |
| Hashing | bucket items (MinHash with LSH, Bloom filters) and compare only within buckets | near-linear; tune shingle size, permutations and bands to your threshold |
| Dimensionality reduction | project to low-dimensional vectors, then compare, often with ANN indexes from vector search | good for semantic near-duplicates; needs embeddings |

Off-the-shelf options include datasketch, Dedupe, TheFuzz, TextDistance, dupeGuru, deduplicate-text-datasets, and lazyNLP (Bloom filter based).

**Rules**
- Deduplicate before the train/test split, and also check train against every evaluation benchmark you will report.
- Keep a mapping from removed IDs to the kept representative, so decisions are auditable.
- For instruction data, check duplicates on the instruction alone, on the response alone and on the pair; each reveals a different problem (conflicting labels, templated answers, true repeats).

## Clean and filter

1. **Strip formatting noise.** Scraped data is full of HTML; unless you want the model to emit HTML, remove it. Databricks reported a 20% accuracy gain and 60% shorter inputs after removing stray Markdown and HTML tokens.
2. **Enforce compliance.** Remove PII, sensitive material, copyrighted content and toxic content (detectors from evaluation work apply). Drop every field you are not allowed to use, such as name, zip code or gender.
3. **Remove low-quality items** with the verification methods (judges, classifiers, heuristics).
4. **Mine heuristics by reading.** Low-quality signals can be non-obvious: Kern et al. (2024) found labels from the second half of an annotation session were worse, probably from fatigue. Other candidates to test: annotation time far below median, copy-pasted responses, sudden style shifts by one annotator.

## Prune when data exceeds budget

If data still exceeds compute, select with active learning (examples the model learns most from), importance sampling (examples most important to the task) or data-pruning metrics (Sorscher et al., 2022). All depend on a good per-example value estimate; validate the subset against a random subset of equal size.

## Format: templates, slimmer instructions, inference parity

**Tokenizer and chat template.** Each model expects its own tokenizer and exact chat template. A wrong template yields strange, hard-to-diagnose bugs. Render a few examples through the real template and read the token stream.

**Instruction shape.** SFT data is (instruction, response), where the instruction may split into system prompt and user prompt.

**Moving from prompting to finetuning.** With enough data, drop the task description and few-shot demos from instructions and turn each demo into a training row. Illustration: a ticket-routing prompt with three demos becomes rows like `printer jammed again => IT`, and the deployed prompt shrinks to `{TICKET} =>`, cutting input tokens and latency.

**Experiment with formats.** Different finetuning formats change results; test a few (separator choice, with or without a brief system line).

**Inference parity.** At serving time, reproduce the training format exactly. With training inputs like `refund not received =>`, all of these can break behavior:
- missing separator: `refund not received`
- extra prefix: `Ticket: refund not received =>`
- trailing whitespace after the separator

Put the formatter in shared code used by both the training pipeline and the serving path.

**Tool use.** Keep any multi-message format (addressed messages, end-of-turn tokens) identical between training and serving.

## End-to-end processing checklist

- [ ] Raw data preserved read-only; each stage writes a new version; scripts trial-run
- [ ] Provenance documented; distributions plotted overall and per source, time, annotator
- [ ] Agreement measured, conflicts resolved, guideline updated; a few dozen rows read by hand
- [ ] Duplicate definition written; dedup before split; train vs eval overlap checked
- [ ] Markup, PII, disallowed fields, toxic and copyrighted content removed; types verified
- [ ] Rendered through the exact chat template; serving uses the same formatter

## Glossary

- **Inter-annotator agreement**: how much independent annotators agree on the same items; kappa corrects for chance.
- **MinHash / LSH**: compact signatures approximating Jaccard similarity, bucketed so only likely matches are compared.
- **Bloom filter**: probabilistic set membership used for fast exact or n-gram overlap detection.
- **Data pruning**: dropping low-value examples to save compute without losing quality.
