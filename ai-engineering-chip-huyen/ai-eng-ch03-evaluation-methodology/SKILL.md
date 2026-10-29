---
name: ai-eng-ch03-evaluation-methodology
description: Chooses, designs and audits methods for evaluating open-ended foundation model outputs, based on Chapter 3 of Chip Huyen's "AI Engineering". Covers perplexity, cross entropy and bits-per-byte; functional correctness and pass@k; exact match, lexical and embedding similarity; LLM-as-a-judge design, biases and judge choice; pairwise ranking with Elo or Bradley-Terry. Use when picking a metric, building or debugging an AI judge, interpreting a score change, checking contamination, or ranking models.
---

# Evaluation Methodology (AI Engineering, Chapter 3)

This skill helps an agent pick and defend the right way to measure open-ended model outputs. It covers the method menu (language modeling metrics, exact evaluation, AI judges, comparative ranking), how each works, and where each breaks. Turning these methods into a model selection process and a full evaluation pipeline is Chapter 4's territory; this skill is about choosing and trusting the individual instruments.

## Key decision rules

Apply these even without opening a reference.

1. **Failure modes first.** List where the system can fail, then pick metrics. If a failure is invisible, change the system (log intermediate steps, split stages) before adding metrics.
2. **Climb the exactness ladder.** Prefer, in order: functional correctness, exact match, lexical similarity, semantic similarity, AI judge, comparative ranking. Stop at the most exact method the task supports. Keep humans in the loop for calibration.
3. **Functional correctness is the ultimate metric** whenever the outcome can be executed or measured (code, SQL, tool actions, games, optimization targets).
4. **Report pass@k with k**, estimated from n >= k samples per problem with the unbiased formula, not from exactly k draws.
5. **Containment matching can accept wrong answers** (right year, wrong date). Prefer extract-then-match.
6. **High lexical overlap is not correctness.** Correct and incorrect code can score alike on BLEU; valid paraphrases score low; references can be missing or wrong. Audit references.
7. **Semantic similarity is only as good as its embedding model.** Pin the model; set cosine thresholds on your own labeled pairs.
8. **Perplexity rules:** lower is better; compare across tokenizers only via bits-per-byte; check units (PyTorch/TensorFlow use nats, so exponentiate with e); match context lengths. Do not rank post-trained (SFT/RLHF) or quantized models by perplexity, since post-training usually raises it. Suspiciously low perplexity on a benchmark signals contamination; high perplexity flags junk or novel data.
9. **An AI judge is model + prompt + sampling settings.** Change any one and scores are no longer comparable. Version all three and store them with every score.
10. **Never trust a judge whose model and prompt you cannot see**, and never mix "the same" criterion (faithfulness, relevance) across tools: their prompts and scales differ.
11. **Judge output format:** classification labels beat numbers; small discrete scales (1 to 5) beat wide or continuous ones; give an example per score level and ask for a rationale.
12. **Consistency is not accuracy.** Validate the judge against human labels on your data.
13. **Probe judge biases:** self-bias (do not let a candidate grade itself in a head-to-head), first-position bias (swap order and aggregate), verbosity bias (test short-correct vs long-wrong).
14. **Budget judge cost and latency.** Each criterion is another call; one generation plus three criteria is four calls. Use cheaper judges or spot-checking; keep heavy judges out of latency-critical paths.
15. **Judge strength:** a stronger judge auditing a cheap generator on a sample is the common pattern; weaker or specialized judges are fine once validated; self-evaluation is for sanity checks and self-revision, not for comparisons.
16. **AI judges supplement, never replace,** exact and human evaluation.
17. **Comparative evaluation answers "which is better", never "is it good enough".** Convert win rates into absolute task metrics and cost before switching models.
18. **Do not ask for preference on factual questions** or from users who could not have produced the answer themselves.
19. **Prefer Bradley-Terry to Elo for batch rankings** (Elo depends on match order). Validate a ranking by its accuracy on held-out matches; there is no ground-truth ranking.
20. **Discount public leaderboards** whose prompts, evaluators or context construction (RAG, tools) differ from yours.

## Default workflow

1. Write the failure-mode list and the quality dimensions users care about.
2. For each dimension, choose the most exact feasible method (rule 2) and decide the reference source (human, AI-drafted plus human review).
3. For residual qualitative criteria, build an AI judge: explicit task, criteria, scale, per-level examples; validate on 100 or more human-labeled items; run bias probes.
4. Freeze and version every evaluator (judge config, embedding model, reference set, test suite).
5. If the decision is a model choice among several candidates, add comparative evaluation on realistic prompts, then confirm the winner with absolute metrics and cost.
6. Re-check judge agreement and benchmark contamination whenever models, judges or traffic change.

## References

Read only the file that matches the question.

- [references/evaluation-landscape.md](references/evaluation-landscape.md): read when framing an evaluation plan, explaining why foundation models are hard to evaluate, separating exact from subjective methods, or walking the method selection ladder with a worked plan.
- [references/language-modeling-metrics.md](references/language-modeling-metrics.md): read when computing or interpreting entropy, cross entropy, BPC, BPB or perplexity, comparing models across tokenizers, or using perplexity for contamination, deduplication or anomaly detection.
- [references/exact-evaluation.md](references/exact-evaluation.md): read when building functional-correctness tests or pass@k, choosing among exact match, edit distance, n-gram metrics and embedding similarity, auditing references, or selecting an embedding model.
- [references/ai-as-a-judge.md](references/ai-as-a-judge.md): read when writing a judge prompt, choosing a scoring format or judge model, diagnosing judge inconsistency, drift or bias, budgeting judge cost and latency, or considering reward, reference-based or preference models.
- [references/comparative-evaluation.md](references/comparative-evaluation.md): read when ranking models from pairwise votes, choosing Elo vs Bradley-Terry vs TrueSkill, judging a public arena, designing an internal leaderboard, or translating win rates into a switch decision.
- [references/source-map.md](references/source-map.md): read when you need to locate which chapter section a topic comes from.

## Scripts

All are Python 3 standard library, deterministic, with `--help`.

- Run `python3 scripts/pass_at_k.py --n 10 --c 3 -k 1 5 10` to compute the unbiased pass@k for one problem, or `python3 scripts/pass_at_k.py --csv results.csv -k 1 10` (columns `n,c`) to compute benchmark-level pass@k averaged over problems.
- Run `python3 scripts/lm_metrics.py --file logprobs.txt --text-file scored.txt` to compute cross entropy (nats and bits), perplexity, bits-per-character and bits-per-byte from per-token logprobs (natural log; add `--base2` for log2 inputs). Logprobs can also be passed inline: `python3 scripts/lm_metrics.py -0.4 -1.2 -0.05`.
- Run `python3 scripts/rank_matches.py matches.csv` (columns `model_a,model_b,winner`, winner may be `tie`) to compute Elo and Bradley-Terry ratings and compare their accuracy at predicting held-out matches. Add `--shuffle-seed 1` to show Elo's sensitivity to match order.
