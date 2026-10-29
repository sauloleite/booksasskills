# Language Modeling Metrics: Entropy, Cross Entropy, BPC, BPB, Perplexity

## Contents
- Why these metrics matter
- Entropy
- Cross entropy and KL divergence
- Bits-per-character and bits-per-byte
- Perplexity, bits vs nats
- Computing perplexity for a text
- Interpreting values
- Use cases beyond training
- When perplexity misleads
- Worked examples
- Glossary

## Why these metrics matter

Many foundation models are built around an autoregressive language model, and that component's predictive quality correlates (imperfectly; still researched) with downstream performance. Cross entropy, perplexity, BPC and BPB are the training signal for such models and are interconvertible given tokenizer statistics and character encoding. They apply to any model emitting token sequences, not only text. Even without training anything, you use them to compare base models on your domain, detect contamination, filter training data and flag anomalous inputs. Fit is always relative to data: the closer your data is to the training distribution, the lower the model's cross entropy on it.

## Entropy

H(P) is the average information per token of a source. Higher entropy, less predictable tokens, more bits needed. Invented example: two equally likely tokens need 1 bit (entropy 1); eight equally likely tokens need 3 bits (entropy 3). A perfectly predictable next token carries no information.

## Cross entropy and KL divergence

With P the true data distribution and Q the model's:
- H(P, Q) = H(P) + KL(P || Q), where KL is the Kullback-Leibler divergence.
- Two ingredients: the data's own predictability and the model's distance from it.
- Training minimizes H(P, Q). A perfect model has KL 0, so its cross entropy equals the data's entropy; cross entropy is the model's (upper-bound) estimate of that entropy.
- Not symmetric: H(P, Q) differs from H(Q, P).
- Empirically: the mean negative log probability the model assigns to each actual next token.

## Bits-per-character and bits-per-byte

Bits per token is not comparable across tokenizers.
- **BPC** = bits per token / average characters per token.
- **BPB** = BPC / bytes per character; also removes encoding differences (ASCII 7 bits per char, UTF-8 8 to 32 bits).
- Cleanest computation: total bits for the text / UTF-8 byte count of the text.
- Compression reading: BPB below 8 means the model compresses the text; BPB 2 is about a 4x ratio.

Rule: compare models with different tokenizers on BPB.

## Perplexity, bits vs nats

- PPL = 2^H with H in bits; PPL = e^H with H in nats. PyTorch and TensorFlow losses are in nats, so exponentiate with e.
- Because of unit confusion, many reports give perplexity instead of cross entropy.
- Reading: the effective number of equally likely options the model hesitates between at each step.
- Conversion: H_bits = H_nats / ln 2.

## Computing perplexity for a text

Perplexity = exp(mean of negative natural-log probabilities of each token given its prefix), the inverse geometric mean of per-token probabilities.

Caveats:
- You need per-token logprobs. Many commercial APIs expose few or none, especially for a supplied text; you may need an open-weights model.
- Decide consistently whether the first token (no prefix) is scored.
- Long texts exceed the context window; use a sliding window and record the conditioning length, since it changes the result.
- `scripts/lm_metrics.py` turns logprobs into cross entropy, perplexity, BPC and BPB.

## Interpreting values

No universal target. Expected perplexity depends on:

| Factor | Effect | Example |
|---|---|---|
| Structure of the data | More structure, lower | Markup or code with paired tags vs casual prose |
| Vocabulary size / richness | Bigger, higher | Literary novel vs picture book; word-level vs character-level |
| Context length | Longer, lower | Thousands of tokens of context vs a handful |

Shannon's early experiments conditioned on about 10 characters; modern measurements use hundreds to tens of thousands of tokens, capped by the context window. Values around 3 or lower occur for strong models, remarkable given vocabularies of tens or hundreds of thousands of tokens.

Before comparing two perplexities, confirm: same tokenizer (else BPB), same unit, same conditioning length and windowing, same text and preprocessing, and both models are base models (not chat-tuned or quantized).

## Use cases beyond training

1. **Capability proxy for base models.** Within a family, larger models show consistently lower perplexity across datasets alongside better downstream accuracy. Score a sample of your domain text to shortlist base models for adaptation; providers increasingly omit perplexity, so compute it yourself.
2. **Contamination detection.** Perplexity is lowest on memorized text. Unusually low perplexity on a benchmark, relative to comparable fresh text, suggests leakage and untrustworthy scores.
3. **Novelty filtering for training data.** Add a candidate sample only if the current model finds it high-perplexity, meaning it is not already covered.
4. **Anomaly detection.** Perplexity spikes on gibberish, scrambled word order and genuinely unusual claims. It cannot distinguish creative novelty from garbage, so route flagged items to a second check.

## When perplexity misleads

- **Post-training.** SFT and RLHF optimize task completion, not raw next-token prediction; perplexity usually rises afterward (sometimes called entropy collapse) while usefulness improves. Do not rank chat models by it.
- **Quantization** can move perplexity unpredictably; validate quantized models on task metrics.
- **Cross-tokenizer comparisons** without BPB.
- **Domain mismatch**: generic-corpus perplexity says little about your specialized documents.
- **It is a proxy**: fit to a distribution, not correctness, safety or usefulness.

## Worked examples

Invented numbers.
1. PyTorch reports mean loss 1.10. Perplexity = e^1.10, about 3.0. In bits: 1.10 / 0.693, about 1.59 per token.
2. Model A: 4.5 bits per token, 4 characters per token, so BPC 1.125; ASCII text in UTF-8 (1 byte per char) gives BPB 1.125. Model B: 3.2 bits per token, 2.5 characters per token, so BPB 1.28. B looks better per token, but A predicts the text better.
3. Your model has perplexity 2.1 on a benchmark's questions and 7.8 on freshly written questions of similar style and difficulty. Treat its benchmark score as unreliable and build a private held-out set.

## Glossary

- **Nat**: information unit using the natural log; 1 nat is about 1.443 bits.
- **Entropy collapse**: post-trained models' sharper distributions, which worsen raw next-token fit.
- **Data contamination**: evaluation data present in training data, inflating scores.
- **Sliding-window perplexity**: scoring long text in overlapping chunks so each token has bounded context.
