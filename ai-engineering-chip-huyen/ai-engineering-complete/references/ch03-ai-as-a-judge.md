# AI as a Judge: Design, Limits, and Choice of Judge Model

## Contents
- What an AI judge is
- Why teams adopt AI judges
- Three judging modes
- Writing the judge prompt and choosing a scale
- Limitation 1: inconsistency
- Limitation 2: criteria ambiguity and judge drift
- Limitation 3: cost and latency
- Limitation 4: biases
- Limitation 5: privacy and IP
- Which model should judge
- Specialized judges
- Playbook: from zero to a trusted judge
- Worked example: diagnosing a score jump
- Glossary

## What an AI judge is

An AI judge (LLM as a judge) is a model used to grade AI outputs. The unit to reason about is the whole configuration: model version, prompt and sampling parameters. Change any part and you have a new judge whose scores are not comparable to the old one, which is why judging counts as subjective evaluation.

Model-based evaluation is an old idea that became practical around GPT-3 (2020). By 2023 to 2024 it was arguably the most common production evaluation method (one platform reported 58% of its 2023 evaluations used AI judges), and it also draws strong skepticism.

## Why teams adopt AI judges

- Fast, easy and cheap relative to human raters.
- Reference-free, so usable on live traffic.
- Any criterion expressible in language: correctness, repetition, toxicity, hallucination, persona fit, perceived trustworthiness of an image.
- Reported human agreement can be high: on MT-Bench a GPT-4 judge agreed with humans 85% of the time, above the 81% human-human agreement; AlpacaEval judges correlated about 0.98 with a human-voted arena leaderboard.
- Judges can explain verdicts, which aids auditing.
- For some criteria they are the only automatic option, and an imperfect judge can still steer early development.

Caution: published agreement figures are specific to their benchmark, model and prompt; they do not transfer to your criterion automatically.

## Three judging modes

| Mode | Inputs | Output | Typical uses |
|---|---|---|---|
| Pointwise | question, answer (plus context) | label or score | monitoring, guardrails |
| Reference comparison | question, reference, answer | equivalent or not | replacing similarity metrics when paraphrase is common |
| Pairwise | question, answer A, answer B | which is better | model ranking, preference data for alignment, best-of-n at inference |

## Writing the judge prompt and choosing a scale

Treat the judge prompt as an application prompt. It must state:
1. **The task**: what is judged, from which inputs.
2. **The criteria**: concrete rules for high and low scores, including contradictions with the reference, partial answers and irrelevant extras. More detail generally helps.
3. **The scoring system**.

Then add an example per score level with a short reason, request a rationale with the score, and use low-temperature sampling.

Scale reliability, best first:
1. **Classification labels** (pass/fail; relevant/partial/irrelevant). Models handle text categories better than numbers.
2. **Small discrete scales**, typically 1 to 5 (classification with numeric names).
3. **Wider discrete ranges**: reliability drops as the range widens.
4. **Continuous scores**: least reliable from a generative judge; leave to specialized scorers.

If stakeholders want a percentage, compute the share of items labeled pass rather than asking the judge for one. Do not adopt a tool's built-in criterion ("relevance", "faithfulness", "groundedness") without reading its prompt; tools ship different prompts and scales under the same name, and defaults change across versions.

## Limitation 1: inconsistency

The same judge can score the same input differently across runs or after small prompt edits.

Mitigations and costs:
- Fix sampling settings (low temperature, seed where supported).
- Add graded examples: in one study this lifted a judge's self-consistency from about 65% to 77.5%, while the longer prompts roughly quadrupled spend.
- Judge several times and aggregate, multiplying cost.

Consistency is not accuracy: a judge can repeat the same mistake every time. Validate against human labels.

## Limitation 2: criteria ambiguity and judge drift

Judge metrics are not standardized. Three open source tools each offered "faithfulness" with different instructions and outputs: a 1 to 5 scale, a 0/1 verdict per statement, and YES/NO that passes if any part of the context supports the claim. A 3, a 1 and a NO for the same pair cannot be reconciled. Even trained scorers can have odd ranges (BLEURT spans roughly -2.5 to 1.0), making thresholds arbitrary.

Drift: the application should change while its yardstick stays fixed, but judges are applications too and get iterated. A coherence score rising from 90% to 92% might reflect the app, or a revised judge prompt, a typo fix that made it lenient, or a silent provider model update. The risk peaks when another team owns the judge.

Rules:
- Do not trust a judge whose model and prompt you cannot inspect.
- Version the configuration and store its identifier with every score.
- When the judge must change, re-score a frozen baseline with old and new judges and report the offset.
- Never mix scores for "the same" criterion from different tools.

## Limitation 3: cost and latency

Many teams use judges as production guardrails, showing users only approved responses.

Cost: using the same model to generate and judge doubles calls; three criteria (say quality, factual consistency, toxicity) make four calls per request. Evaluation can outspend generation. Levers: cheaper or smaller judges; spot-checking a sample (bigger samples, more confidence, more cost; tune empirically by risk); merging criteria into one call only if validation shows no loss. Even so, judges cost far less than human raters.

Latency: an in-path judge reduces risk but adds delay, possibly a nonstarter under strict budgets. Alternatives: asynchronous judging with after-the-fact remediation, or a fast small judge in-path and a strong one offline.

## Limitation 4: biases

| Bias | Effect | Reported magnitude | Mitigation |
|---|---|---|---|
| Self-bias | Model favors its own outputs | One study: about +10% win rate for GPT-4 on itself, +25% for Claude-v1 | Never let a candidate judge a head-to-head it is in; use a third party or panel |
| First-position bias | Favors the first option | Common; humans show the reverse (recency) | Judge both orders; treat order-flipping verdicts as ties |
| Verbosity bias | Favors longer answers | Judges preferred ~100-word answers with errors over correct ~50-word ones; at a 2x length gap in creative tasks the longer one nearly always won | Instruct to ignore length; include short correct top-score examples; control for length in analysis |

Newer, stronger judges showed less verbosity bias than predecessors, so some biases may shrink, but test rather than assume. Humans also prefer longer answers, far less strongly.

## Limitation 5: privacy and IP

A proprietary judge means sending your data to its provider, and undisclosed training data leaves commercial safety uncertain. Check data agreements before piping production traffic out.

Overall stance from the chapter: judge adoption will keep growing, but judges must be supplemented by exact evaluation, human evaluation, or both.

## Which model should judge

| Judge vs generator | Rationale | Watch out for |
|---|---|---|
| Stronger | Better verdicts and can guide the weaker model. Fits when the generator is picked for cost or speed: a cheap in-house generator with a strong model grading 1% of traffic, or a fast generator with a slow strong model reviewing in the background and replacing bad answers | The strongest model has no stronger judge, and another method is needed to know which is strongest |
| Weaker | Judging can be easier than generating (critiquing a song vs writing one). Common: strong generator, cheap background judge | Validate on your criterion; general-purpose experiments found stronger judges track humans better |
| Same (self-evaluation, self-critique, self-ask) | Sanity check (if a model rejects its own answer, distrust it); critique-and-revise can improve outputs | Self-bias; unfit for cross-model comparison |
| Small specialized | Trained for one judgment with fixed criteria and scale; can beat large generalists there cheaply | Narrow; fails silently out of scope |

Default: baseline with the strongest general judge you can afford, collect human-labeled disagreements, then try cheaper or specialized judges and keep them only if agreement holds.

## Specialized judges

- **Reward models**: (prompt, response) to score; long used in RLHF. Google's Cappy (about 360M parameters) outputs a 0 to 1 correctness score.
- **Reference-based judges**: BLEURT scores (candidate, reference) similarity; Prometheus takes (prompt, response, reference, rubric) and outputs 1 to 5, treating the reference as a 5.
- **Preference models**: (prompt, A, B) to the preferred response, often with a rationale (PandaLM, JudgeLM). Valuable because human preference data is costly and needed for both alignment and comparative evaluation.

## Playbook: from zero to a trusted judge

1. Name the criterion precisely and collect pass/fail examples from real outputs.
2. Draft the prompt (task, criteria, scale, per-level examples, rationale); choose labels or 1 to 5.
3. Hand-label a representative set (a few hundred items is a practical start; use domain experts when correctness matters).
4. Measure agreement (accuracy, Cohen's kappa, or rank correlation); fix criteria based on disagreements.
5. Probe biases: swap orders, pair short-correct with long-wrong answers, check self-judging gaps.
6. Freeze and version: model id, prompt hash, temperature, examples.
7. Deploy as offline-only, sampled async monitoring, or in-path guardrail; set the sampling rate from risk and budget.
8. Re-check agreement periodically and whenever the judge or traffic changes.

## Worked example: diagnosing a score jump

Invented case: groundedness rose from 84% to 91% after a release. Judge identifiers show the provider alias now resolves to a newer model. Re-scoring last month's stored outputs with the new judge gives 89%, so 5 of the 7 points came from the judge. Pin an explicit model version, report a true gain of about 2 points, and make the pipeline fail loudly when judge identity changes.

## Glossary

- **Judge configuration**: the model, prompt and sampling settings that define a judge.
- **Spot-checking**: judging a sample of outputs rather than all of them.
- **Self-ask**: prompting a model to assess and then revise its own answer.
- **Recency bias**: the human tendency to prefer the last option seen.
