---
name: ai-eng-ch04-evaluating-ai-systems
description: Guides evaluation of LLM applications and model choice, based on Chapter 4 of Chip Huyen's "AI Engineering". Covers evaluation criteria (domain skill, generation quality, factual consistency, safety, instruction following, roleplay, cost and latency), model selection, API vs self-hosting, licenses, public benchmarks and leaderboards, data contamination, and evaluation pipeline design. Use when defining success criteria, picking or switching models, reading leaderboards, sizing an eval set, checking if a score gain is real, or detecting benchmark leakage.
---

# Evaluating AI Systems (AI Engineering, Chapter 4)

This skill turns evaluation methods (exact match, functional correctness, similarity, AI judges, perplexity) into decisions for a real application: what to measure, which model to use and how to host it, how far to trust public benchmarks, and how to build an evaluation pipeline that keeps steering development after launch. Core stance: decide how success is judged before building, treat public benchmarks as a filter rather than a verdict, and make your own pipeline the final authority.

## Key decision rules

Apply these even without opening the references.

1. **Evaluation-driven development.** Write criteria before building. A deployed system nobody can evaluate is worse than none: it costs money and is hard to remove.
2. **Four criteria buckets.** Cover domain capability, generation quality, instruction following, and cost and latency for every application.
3. **Multiple choice measures knowledge and reasoning, not generation.** Never infer summarization or writing quality from MCQ scores. Keep option formatting identical across models; tiny changes flip answers.
4. **Correct is not enough for code.** Add runtime and memory against a reference solution, and a judge for readability.
5. **Factual consistency: local before global.** Checking against supplied context is far easier than checking against world knowledge. Never treat "no evidence found" as proof.
6. **Build hallucination sets from failure types.** Overweight niche-knowledge and false-premise queries rather than sampling traffic at random.
7. **Cheap scorer on everything, expensive judge on a sample.** Small toxicity or NLI classifiers on all traffic; a strong AI judge on about 1%; humans on a daily sample.
8. **Instruction failures are entangled.** A bad output may be a weak model or a weak prompt; test both before concluding. Build your own instruction checks from your real constraints.
9. **Personas need style and negative-knowledge checks.** The character must not know or leak what it should not.
10. **Pareto filter.** Name non-negotiable objectives, filter on them, then optimize the rest. Separate must-have latency from nice-to-have.
11. **Hosting economics.** API cost per token is flat with scale; self-hosting cost is mostly fixed, so it gets cheaper per token as utilization rises. Re-decide at each scale step.
12. **Hard attributes first.** Filter on what you cannot change (license, privacy, residency, control), then shortlist, then test privately, then monitor. Latency is soft if you serve the model, hard if a vendor does.
13. **Check license terms and lineage.** Commercial use, user-count caps, and whether outputs may train other models, including terms inherited from any model whose outputs trained this one.
14. **Leaderboards: check coverage, correlation, aggregation, freshness.** Correlated benchmarks double-count a skill; plain averages treat unequal difficulties as equal.
15. **Assume public benchmarks are contaminated.** Use them to shortlist; decide on private data. Report clean-subset scores when you can detect overlap.
16. **Evaluate components, turns and tasks separately.** End-to-end scores alone cannot locate failures; task completion and turn count matter most to users.
17. **The guideline is the most important step.** Define what the system must not do, write rubrics with anchored examples, validate them on people, and map metric levels to business outcomes with a usefulness threshold.
18. **Size the eval set.** Rough rule for 95% confidence: 30-point gap needs about 10 examples, 10 points about 100, 3 points about 1,000, 1 point about 10,000. Aim for at least 300, preferably 1,000 or more. Bootstrap to check stability.
19. **Slice.** Keep a production-like set plus slices, known-hard, user-error and out-of-scope sets. Compare per slice to avoid Simpson's paradox.
20. **Evaluate the evaluator and version everything.** Check signal, reproducibility (judge temperature 0), metric correlation, and added cost and latency. Log data, rubric, judge model, prompt and sampling settings.

## Default workflow

1. Write the criteria sheet: for each criterion record metric, data source, hard requirement, ideal target (cost, throughput, latency percentiles, quality, task capability, factual consistency).
2. Filter models on hard attributes and decide API vs self-hosting along the seven axes.
3. Build a custom leaderboard from recent, relevant, decorrelated public benchmarks to get a shortlist; discount contaminated results.
4. Write the evaluation guideline: scope and out-of-scope handling, two or three criteria, rubrics with examples, business mapping.
5. Pick a method per criterion, assemble and slice annotated data, and size it with `scripts/eval_sample_size.py`.
6. Run shortlisted models through the pipeline; choose the cheapest model that clears every threshold.
7. Validate the pipeline itself, version it, and keep monitoring in production with user feedback and human review.

## References

- [references/evaluation-criteria.md](references/evaluation-criteria.md): read when defining what to measure, choosing metrics for domain skill, generation quality, instruction following or personas, or setting cost and latency requirements.
- [references/factual-consistency-and-safety.md](references/factual-consistency-and-safety.md): read when measuring hallucination or grounding (including RAG answers), building a hallucination test set, or choosing toxicity and bias detectors.
- [references/model-selection-and-hosting.md](references/model-selection-and-hosting.md): read when picking or switching models, reviewing open model licenses, or deciding between a model API and self-hosting.
- [references/public-benchmarks-and-contamination.md](references/public-benchmarks-and-contamination.md): read when interpreting leaderboards, building a custom leaderboard, judging reports that a model got worse, or detecting and handling data contamination.
- [references/evaluation-pipeline.md](references/evaluation-pipeline.md): read when designing or auditing an evaluation pipeline: component and task evaluation, guidelines and rubrics, business mapping, method mix, annotation, slicing, set size, evaluator validation, iteration.
- [references/source-map.md](references/source-map.md): read to find which reference covers a given chapter section.

## Scripts

Both use only the Python 3 standard library, are deterministic, and print `--help`.

- Run `python3 scripts/eval_sample_size.py size --gap 0.03 --baseline 0.80` to compute how many examples are needed to detect a 3-point gap (rule-of-thumb figure plus a two-proportion estimate).
- Run `python3 scripts/eval_sample_size.py bootstrap scores_a.txt` to compute a bootstrap confidence interval and standard error for one system's per-example scores (one number per line). Add `--compare scores_b.txt` (same examples, same order) to compute a paired interval for B minus A and a verdict on whether B is really better.
- Run `python3 scripts/ngram_contamination.py bench.txt corpus.txt --n 13 --clean-out clean.txt` to compute which benchmark examples (one per line, or `--jsonl --field text`) share 13-token spans with a corpus, the dirty percentage, and a clean subset file for side-by-side scoring.
