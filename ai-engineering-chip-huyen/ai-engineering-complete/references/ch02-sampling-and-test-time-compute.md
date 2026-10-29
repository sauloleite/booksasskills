# Sampling and Test Time Compute

## Contents
- Why sampling matters
- From logits to a token
- Temperature
- Logprobs
- Top-k, top-p, min-p
- Stopping conditions
- Settings by task
- Test time compute
- Selecting the best output
- How far it scales; robustness
- Worked examples
- Pitfalls and glossary

## Why sampling matters

Sampling turns probabilities into output. It explains much puzzling behavior (inconsistency, some hallucination) and is among the cheapest quality levers, since it needs no retraining. Custom strategies usually need logit access.

## From logits to a token

A language model emits one logit per vocabulary entry. Logits can be negative and do not sum to one; softmax converts them to probabilities. Greedy decoding (always the top token) suits classification but makes open text bland. Sampling picks each token in proportion to its probability, yet common continuations still dominate and vivid low-probability phrasings rarely surface.

## Temperature

Logits are divided by T before softmax. T below 1 sharpens toward the top token (consistent, dull); above 1 flattens (creative, less coherent).

- Anchor: logits 1 and 2 give 0.27 and 0.73 at T = 1, and 0.12 and 0.88 at T = 0.5. Below about 0.1 the top token nearly always wins.
- T = 0 means argmax in practice (division by zero is skipped along with softmax).
- Providers usually allow 0 to 2; self-hosted models accept any non-negative T.
- About 0.7 is a common creative default; tune empirically.

## Logprobs

Log-scale probabilities avoid underflow with vocabularies around 100,000. Use them for classification confidence, evaluation and debugging (a near-uniform distribution means the model learned little). Availability is limited, partly because they ease model copying: at the time of writing OpenAI returned only the top 20 and stopped scoring arbitrary text in September 2023, and Anthropic returned none.

## Top-k, top-p, min-p

- **Top-k** keeps the k largest logits before softmax, avoiding two full passes over the vocabulary. k of 50 to 500; smaller k means more predictable text.
- **Top-p (nucleus)** keeps the smallest set of most likely tokens whose cumulative probability reaches p (typically 0.9 to 0.95). It adapts to context (a yes/no question needs two candidates, an open question many). It need not save compute, and theory gives it little support, but it works well in practice.
- **Min-p** drops tokens below a minimum probability. Some implementations scale the floor by the top token's probability; the demo script supports both.

## Stopping conditions

Long outputs cost time and money (billing is per output token) and can annoy users. Max-token limits are simple but can cut mid-sentence; stop tokens such as end-of-sequence end naturally. For structured output, early stopping can drop closing brackets and break parsing, so leave headroom.

## Settings by task

These are starting points to validate on your own data, not fixed rules.

| Task | Start with |
|---|---|
| Classification, extraction, grading | T = 0, fixed seed, cache |
| Factual Q&A | Low T, top-p about 0.9 |
| Creative writing | T about 0.7, top-p 0.9 to 0.95 |
| Candidates for later selection | Higher T, vary settings per sample |
| Short constrained answers | Top-p or min-p, or constrained decoding |

## Test time compute

Generate several responses per query and keep the best. Best of N samples independently; beam search keeps the most promising partial sequences at each step and prunes the rest (requires decoding control). Diversify candidates by varying temperature, top-p or the prompt. Cost scales roughly linearly with N, though shared input can be processed once. "Test time" is research jargon for inference.

## Selecting the best output

| Selector | Use when |
|---|---|
| User picks | Subjective or creative output |
| Highest average logprob | No scorer exists. Sequence logprob is the sum of token logprobs, which favors short outputs, so divide by length (OpenAI's best_of option worked this way) |
| Reward model or verifier | Open-ended quality, math, domain checks. Stitch Fix and Grab use reward models; Nextdoor found one was the main driver of its quality gains |
| Application heuristic | A proxy exists, such as preferring the shortest answer |
| Regenerate until valid | Output is checkable, such as SQL that must parse |
| Majority vote (self-consistency) | Exact answers; Gemini's MMLU result used 32 samples per question |
| First valid parallel result | Latency-critical long reasoning, as TIFIN does |

## How far it scales; robustness

- OpenAI's math verifiers gave about the gain of a 30x larger model (100M with verifier matched 3B without). DeepMind (2024) argued inference scaling can beat parameter scaling.
- OpenAI saw gains peak near 400 samples, then fall, likely as adversarial candidates began fooling the verifier; Stanford's "Monkey Business" found log-linear gains from 1 to 10,000 samples. Production systems never sample at that scale. Start with 2 to 5.
- Robust models change little under small input changes. Brittle ones benefit most from retries: in one product-label extraction project, a single try succeeded about half the time but three tries recovered most images. Better still, replace the brittle model.

## Worked examples

1. **One distribution, several filters.** Logits 5, 3.5, 3, 2, -1 give about 0.71, 0.16, 0.10, 0.035, 0.002 at T = 1. At T = 0.7 the top token rises to 0.84; top-p 0.9 then keeps two tokens (0.84 + 0.10 crosses 0.9), renormalized to 0.90 and 0.10. Relative min-p 0.1 at T = 1 keeps three tokens (floor 0.071; third token 0.096). Reproduce with `scripts/sampling_demo.py`.
2. **Choosing N.** A summarizer with a verifier gains 6 points from 1 to 4 samples and 1 more from 4 to 8. Doubling cost for 1 point is not worth it; stay at 4.

## Pitfalls and glossary

Pitfalls: greedy decoding for open-ended text or high T for extraction; expecting T = 0 to be fully deterministic; summed instead of average logprob; growing N without a reliable selector; tight max tokens on structured output; assuming every provider exposes logprobs.

- **Self-consistency**: majority vote over sampled answers.
- **Verifier**: model trained to judge whether a candidate is correct.
- **Robustness**: output stability under small input perturbations.
