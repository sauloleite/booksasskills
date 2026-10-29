# Evaluation Landscape: Why Foundation Models Are Hard to Evaluate, and How to Pick a Method

## Contents
- Framing: evaluation as risk management
- The five difficulties specific to foundation models
- The investment gap
- Exact vs subjective evaluation
- Method selection ladder
- Worked example: planning evaluation for a support assistant
- Glossary

## Framing: evaluation as risk management

Evaluation serves two goals: limit the damage a system can do and reveal what else it could do. Consequences:

- Start from where the system is likely to break, then design measurements for each failure. Metrics chosen before failure modes are known tend to measure what is easy, not what matters.
- If a failure is not observable, the fix is architectural first: log intermediate steps, split a monolithic prompt into checkable stages, store retrieved context next to the answer.
- No volume of metrics or tooling rescues a team that does not know where its system fails.
- Public incidents (a chatbot encouraging self-harm, fabricated citations filed in court, an airline held liable for its bot's wrong policy) show quality-control risk rising with adoption. Evaluation can absorb most of a project's effort, sometimes more budget than generation itself.

The default failure is informal evaluation: reputation ("people say model X is good"), eyeballing, or a private list of favorite prompts curated from taste rather than product needs. Tolerable when starting a prototype; inadequate for iteration, because you cannot tell whether a change helped.

## The five difficulties specific to foundation models

1. **Grader capability.** The better the model, the more skill it takes to catch its errors. A fluent summary may require reading the source, fact-checking and domain knowledge. Evaluation time per item grows with task sophistication; "sounds right" is no longer evidence.
2. **Open-endedness.** Classifiers pick from fixed labels; generative outputs admit many valid answers, so any finite reference list is incomplete.
3. **Opacity.** Architecture, training data and process are often undisclosed (or the team cannot use them), so only outputs can be judged and the test set must do all the work.
4. **Benchmark saturation.** A benchmark stops discriminating once top models max it out, now within a year or two (GLUE to SuperGLUE, NaturalInstructions to Super-NaturalInstructions, MMLU to MMLU-Pro). Assume every public benchmark has a shelf life.
5. **Expanding scope.** For general-purpose models, evaluation also means discovering unplanned capabilities and limits, possibly beyond human level.

## The investment gap

Papers and open source repositories on LLM evaluation multiplied quickly in 2023 and 2024, yet evaluation tooling remains thin next to tooling for modeling, training and orchestration, and experimental results are rarely fed back into better evaluations. In practice: budget time to build your own harness, datasets and judges; expect non-standard definitions in tools; version evaluation code and data as first-class artifacts.

## Exact vs subjective evaluation

| Property | Exact | Subjective |
|---|---|---|
| Verdict for a fixed output | Deterministic | Depends on the grader |
| Repeatability | Same every run | Varies across runs, graders, prompts |
| Examples | Unit tests, string match, BLEU, cosine score | Human ratings, AI judges |
| Made more reliable by | n/a | Detailed rubrics, fixed graders, calibrated examples |

Semantic similarity is a boundary case: cosine over two given embeddings is exact, but the embedding model is a subjective choice, so treat it as part of the metric definition.

Scope note: the chapter focuses on automatic evaluation of open-ended outputs. Close-ended components (intent routers, scorers) use standard classification metrics. Human evaluation stays necessary for many applications and always helps as a sanity check, but it is slow and costly, so automate and use humans to anchor and audit.

## Method selection ladder

Work down and stop at the first rung the task genuinely supports. Lower rungs are more flexible and more fragile.

1. **Functional correctness**: output can be executed or its effect measured.
2. **Exact match**: the correct answer is short and unambiguous.
3. **Lexical similarity**: rich references exist and surface form matters.
4. **Semantic similarity**: references exist but wording varies freely.
5. **AI judge**: no references, or the quality is qualitative (tone, relevance, faithfulness to context, persona fit, safety).
6. **Comparative ranking**: you must order candidates on subjective quality and absolute scores are unreliable.
7. **Human evaluation**: always present for calibration; primary when stakes are high and automation is untrusted.

Perplexity and related metrics sit outside the ladder: they measure the model's fit to a data distribution (useful for base model selection, data quality and contamination checks), not the quality of one response.

Combination rules:
- Never let a subjective method be the only signal; pair AI judges with exact checks, human review, or both.
- When one requirement has exact and subjective facets (valid JSON and helpful), measure each facet with the most exact method available instead of asking a judge about everything.

## Worked example: planning evaluation for a support assistant

Invented scenario: an assistant answers billing questions from retrieved policy documents and can issue refunds through a tool.

1. Failure modes: wrong refund amount; refund issued against policy; answer contradicts retrieved policy; rude tone; leaking another customer's data.
2. Visibility: log retrieved documents, tool call arguments and the final message separately.
3. Methods:
   - Refund amount and eligibility: functional tests over account states with expected tool calls.
   - Balance and date lookups: exact match after format normalization.
   - Consistency with policy: AI judge comparing answer to retrieved context, pass/fail with rationale.
   - Tone: AI judge on a 1 to 5 scale with an example per level, spot-checked on sampled traffic.
   - Data leakage: deterministic pattern checks plus human review of flagged cases.
4. Calibration: humans label a few hundred items for the judge criteria; measure agreement first.
5. Versioning: freeze judge model, prompt and sampling settings; record them with each score.

## Glossary

- **Saturation**: strong models reach near-perfect scores, so the benchmark stops separating them.
- **Exact / subjective evaluation**: grading whose verdict does or does not depend on the grader.
- **Vibe check**: impression-based assessment; acceptable only at the very start.
