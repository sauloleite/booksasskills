# Exact Evaluation: Functional Correctness, Reference Similarity, Embeddings

## Contents
- Functional correctness
- pass@k and the unbiased estimator
- Reference data
- Exact match and its variants
- Lexical similarity
- Semantic similarity
- Choosing and checking an embedding model
- Multimodal joint embeddings
- Decision table
- Pitfalls
- Glossary

## Functional correctness

Judge the system by whether it does the intended job: does the generated site meet the spec, did the agent actually book the table. The chapter calls this the ultimate metric, while noting it is often hard to measure and to automate.

Where it automates well:
- **Code**: run generated code against test cases (scenario plus expected output), known as execution accuracy. HumanEval and MBPP (code) and Spider, BIRD-SQL and WikiSQL (text-to-SQL) score this way.
- **Games and simulations**: the bot's score is the metric.
- **Measurable objectives**: a workload scheduler judged by energy saved; a pricing agent by margin in a sandbox.

Edge case: when AI handles only part of a complex task, its contribution is hard to isolate (grading one chess move is harder than grading the game). Measure the end-to-end outcome when possible; otherwise define step-level checks with explicit expected states.

Test suite checklist:
- [ ] Several test cases per problem, including edge and adversarial inputs.
- [ ] Sandboxed execution with timeouts and resource limits.
- [ ] Syntax errors, runtime errors and wrong outputs all count as failures but are logged separately.
- [ ] Hidden tests that neither the model nor prompt authors see.

## pass@k and the unbiased estimator

Per problem, the model produces k candidates; the problem counts as solved if any candidate passes every test. pass@k is the share of problems solved. Example: 20 problems, 9 solved at k = 5, so pass@5 = 45%. More attempts, more chances: in expectation pass@1 <= pass@5 <= pass@10. Always state k.

Drawing exactly k samples gives a noisy estimate. The standard approach (from the paper introducing HumanEval) samples n >= k per problem, counts c passing, and computes 1 - C(n - c, k) / C(n, k), averaged over problems. If n - c < k the value is 1; if c = 0 it is 0; pass@1 reduces to c / n. Use `scripts/pass_at_k.py`.

Reading it: pass@1 reflects single-shot use; large-k pass rates matter only if you can generate many candidates and verify them automatically. A big gap between pass@1 and pass@10 means the model can find correct solutions but samples them unreliably, so sampling settings or test-time selection may pay off.

## Reference data

Each item is (input, one or more references). Other names for a reference: ground truth, canonical response. Metrics needing references are reference-based; others are reference-free.

- Reference-based evaluation scales only as fast as references can be produced.
- Human references make human performance the yardstick, at high cost; AI-drafted references with human review are cheaper because reviewing beats authoring.
- References are often incomplete: a captioning model was penalized on public benchmarks for correct captions the references lacked.
- References can be wrong: organizers of a translation-metrics shared task found many poor reference translations, one reason reference-free metrics have rivaled reference-based ones in agreement with humans.

Rule: audit a sample of references and collect several per input for open-ended tasks.

Comparing a response with a reference can be done by an evaluator (human or AI judge) or by hand-designed metrics: exact match (binary), lexical similarity and semantic similarity (graded). Hand-designed metrics stay popular because they are deterministic and cheap.

## Exact match and its variants

Fits short, closed answers: arithmetic, trivia, factual or account lookups, fill-in-the-blank.
- **Normalized match**: lowercase, strip punctuation, canonicalize numbers and dates first.
- **Containment**: accept outputs containing the reference. Risk: the output can contain it and still be wrong. Invented example: a company was founded in July 1998; "March 3, 1998" contains "1998" and passes. Use only when extra content cannot change correctness.
- **Extract-then-match**: request a structured answer field, parse, then match. Usually the most robust.

Beyond simple tasks exact match fails: even a short phrase has many valid translations, and the count grows with length.

## Lexical similarity

Overlap at the token level (decide whether inflections and contractions count as one token).
- **Token overlap**: share of reference tokens found in the output. Invented example: reference "the dog chased the red ball", output "the dog caught the red ball", 5 of 6 tokens shared.
- **Edit distance (fuzzy matching)**: minimum insertions, deletions and substitutions to turn one string into the other; some libraries count an adjacent transposition as one edit, others as two.
- **n-gram metrics**: overlap of contiguous token sequences, capturing some order. BLEU, ROUGE, METEOR++, TER and CIDEr differ in precision vs recall emphasis, brevity handling and synonym support. WMT, COCO Captions and GEMv2 still use them; fewer foundation model benchmarks do.

Failure modes: paraphrases are penalized unless references are comprehensive; overlap is not correctness (on HumanEval, correct and incorrect solutions had similar BLEU); a single "not" barely moves the score. Use lexical metrics when references are plentiful and form matters (terminology compliance, templated output), or as a cheap regression tripwire.

## Semantic similarity

Scores closeness of meaning: embed both texts and take cosine similarity, A·B / (||A|| ||B||), ranging -1 to 1. Works for any modality with an embedder; for text it is semantic textual similarity. Metrics include BERTScore (BERT embeddings) and MoverScore.

Trade-offs: needs less exhaustive references than lexical metrics; only as good as the embedding model; costs compute; exact given embeddings but subjective in embedder choice, so pin and version it. Cosine is not a calibrated probability: set pass thresholds on labeled pairs from your domain.

The same similarity machinery also powers retrieval, ranking, clustering, anomaly detection and deduplication.

## Choosing and checking an embedding model

- Vectors typically have about 100 to 10,000 dimensions, still a compression of the raw data.
- Dedicated embedding models usually beat vectors extracted from a generative model's internal layers.
- Check **neighborhood sanity**: build a few dozen (anchor, similar, unrelated) triplets from your domain and verify the ordering.
- Check **downstream utility** on the actual task (retrieval for RAG, classification accuracy, clustering, recommendation). MTEB gives a shortlist, not a verdict.
- Check cost and latency at your volume.
- Embeddings exist for products, images, queries, graphs and users, not just text.

## Multimodal joint embeddings

Joint spaces let different modalities be compared directly: CLIP (text and image), ULIP (adds 3D point clouds), ImageBind (six modalities including audio). CLIP-style training encodes each (image, text) pair separately, projects both into one space, and pulls matching pairs together while pushing mismatches apart. A photo of someone fishing should land near "an angler" and far from an unrelated caption. This enables text-to-image search and checking whether a generated image matches its prompt.

## Decision table

| Task signal | Method | Setting to decide |
|---|---|---|
| Executable or measurable outcome | Functional correctness, pass@k | k, n, test coverage |
| Single short answer | Normalized exact match | Normalization rules |
| Short answer inside prose | Extract-then-match | Parser robustness |
| Rich references, form matters | BLEU / ROUGE / edit distance | Metric variant, n |
| References, free wording | Embedding cosine / BERTScore | Embedder, threshold |
| No references | AI judge | n/a |

## Pitfalls

- Reporting pass@k without k, or from exactly k noisy samples.
- Containment matching where extra details can be wrong.
- Reading high BLEU as high quality; trusting unaudited references.
- Changing the embedding model and comparing scores across the change.
- Borrowing a cosine threshold from another domain.

## Glossary

- **Execution accuracy**: functional correctness for code, judged by running it.
- **Reference-free metric**: needs only input and output, no ground truth.
- **Fuzzy matching**: approximate string matching via edit distance.
- **Joint embedding space**: one vector space shared by several modalities.
