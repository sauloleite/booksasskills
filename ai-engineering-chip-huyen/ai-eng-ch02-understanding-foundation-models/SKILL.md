---
name: ai-eng-ch02-understanding-foundation-models
description: Predicts foundation model strengths and failure modes from training data, architecture, size and post-training, and tunes inference-time levers. Use when choosing or sizing a model, judging non-English or domain coverage, estimating params, tokens, FLOPs, GPU-days or cost, reading MoE or Chinchilla figures, explaining base vs SFT vs RLHF/DPO behavior, setting temperature, top-k, top-p, min-p or stop conditions, applying best-of-N or verifiers, forcing JSON/SQL outputs, or reducing inconsistency and hallucination. Based on Chapter 2 of Chip Huyen's "AI Engineering".
---

# Understanding Foundation Models (AI Engineering, Chapter 2)

Application engineers rarely train foundation models, but every builder decision (training data, architecture, size, post-training) surfaces as behavior they must handle, and sampling remains fully under their control at inference. This skill helps an agent predict where a model will be strong or weak from how it was built, size and cost models with back-of-envelope arithmetic, and pick sampling, selection and structured-output strategies that turn a probabilistic model into a dependable component.

## Key decision rules

Apply these even without opening the references.

**Data and coverage**
- A model is weak wherever its training data was thin. Web crawls dominate training sets because they are available, not because they fit your task.
- English is about 46% of Common Crawl; many large languages are far below 1%. Expect lower quality, different safety behavior, and several times more tokens (up to about 10x) in under-represented languages. Measure each with your own data.
- Prefer, in order: an existing language- or domain-specific model, then a finetune on curated data, then a translate-via-English bridge (only after checking what translation loses).
- Proprietary or specialized formats (molecules, medical imaging, internal plans) are not on the web; assume a general model fails there.
- Small curated datasets can beat huge noisy ones; quantity, quality and diversity all count.

**Architecture and size**
- Separate prefill (parallel, input) from decode (sequential, output) when reasoning about latency.
- KV storage grows with context length; long context costs memory but adds no parameters.
- Compare models by generation and benchmarks, not raw parameter count (a newer 8B can beat an older 70B).
- MoE: cost and speed follow active parameters; memory follows total parameters.
- Weight memory floor = params x bytes per param (7B at 16-bit is at least 14 GB); real serving needs more.
- Compute-optimal training is about 20 tokens per parameter; training FLOPs is roughly 6 x params x tokens. Production often prefers smaller, over-trained models because inference is cheaper.
- Training time = FLOPs / (GPUs x peak FLOP/s x utilization); 50% utilization is acceptable, above 70% is great. Keep FLOPs (work) distinct from FLOP/s (rate).
- Each further quality point costs disproportionately more, but small loss gains can be very visible to users.
- Data (public web exhaustion, crawl restrictions, AI-generated content) and electricity are the scaling bottlenecks. Assume anything published online may end up in training sets.

**Post-training**
- Identify the variant: base models complete text, SFT models follow instructions, preference-tuned models (RLHF, DPO, RLAIF) are more polished. "Instruction finetuning" is ambiguous; ask which stages.
- Preference tuning encodes a particular labeler population's preferences and does not reliably cut hallucination (InstructGPT's RLHF model hallucinated more than its SFT model).
- For preference data use comparisons, not absolute scores; expect only about 73% labeler agreement.
- A reward model or verifier without RL is still valuable for picking the best of several samples.

**Sampling**
- Greedy or T = 0 for classification and extraction; around 0.7 with top-p 0.9 to 0.95 for creative work; tune empirically.
- Top-k (50 to 500) trims computation; top-p adapts the candidate set to context; min-p sets a probability floor.
- Max-token limits and stop words can truncate structured output; leave headroom.
- Logprobs are valuable for classification, scoring and debugging, but many providers expose them partially or not at all.

**Test time compute**
- Generating N outputs costs about N times as much. Start with 2 to 5 diverse candidates and a real selector.
- Selectors: majority vote for exact answers, verifier or reward model for quality, average (not summed) logprob when nothing else exists, validity checks for SQL or schemas, first valid parallel result for latency.
- Verifiers can be worth roughly a 30x model size increase, but very large N can fool the verifier. Brittle models gain most from retries; replacing them is better.

**Structured outputs**
- Escalate: prompting, then post-processing repairs, then retry-until-valid, then constrained sampling, then finetuning (or a classifier head for fixed labels).
- JSON mode guarantees syntax, not content, and not completeness under a token limit. Always validate.

**Probabilistic behavior**
- Same-input inconsistency: cache, pin sampling parameters, fix the seed; hardware can still change outputs.
- Perturbed-input inconsistency: fix with prompt design, memory and robustness testing, not settings.
- Hallucination: ground in provided context, permit "I don't know", keep answers short, require and verify sources, and restart rather than continue from an early error (snowballing).

## Default workflow

1. **Frame the requirement**: language(s), domain, data formats, output format, latency and cost targets, factuality stakes.
2. **Shortlist models** using the coverage rules; check for language- or domain-specific options; note base vs chat variant.
3. **Size it**: memory floor, active vs total params, token costs per language; run `scripts/scaling_calculator.py` for training or budget questions.
4. **Evaluate** on a small realistic set, including target-language safety probes and perturbed inputs.
5. **Set sampling** per task; inspect distributions with `scripts/sampling_demo.py` when behavior is surprising.
6. **Add reliability layers**: structured-output escalation, test time compute with a selector, consistency and hallucination mitigations.
7. **Re-measure** cost, latency, validity and factuality before shipping.

## References

- [references/training-data.md](references/training-data.md): read when judging whether a model covers a language, domain or data format, or deciding between specialized model, finetune and translation bridge.
- [references/model-architecture-and-scale.md](references/model-architecture-and-scale.md): read for transformer internals, prefill vs decode, SSM/Mamba/RWKV alternatives, parameter and MoE reasoning, FLOPs and cost math, Chinchilla limits, inverse scaling, and scaling bottlenecks.
- [references/post-training.md](references/post-training.md): read when explaining base vs SFT vs preference-tuned behavior, designing demonstration or comparison data, or using a reward model.
- [references/sampling-and-test-time-compute.md](references/sampling-and-test-time-compute.md): read when choosing temperature, top-k, top-p, min-p, stop conditions or logprob use, or designing best-of-N, beam search, voting and verifier selection.
- [references/structured-outputs.md](references/structured-outputs.md): read when outputs must be valid JSON, YAML, SQL, regex or fixed labels, or when JSON mode or constrained decoding is failing.
- [references/inconsistency-and-hallucination.md](references/inconsistency-and-hallucination.md): read when outputs vary between runs, flip on small input changes, or contain fabricated facts.
- [references/source-map.md](references/source-map.md): read to find which file covers a given chapter section.

## Scripts

Python 3, standard library only; run from this skill's directory. Each supports `--help`.

- Run `python3 scripts/scaling_calculator.py --params 7B` to compute compute-optimal tokens (20 per parameter), training FLOPs (6 x active params x tokens), GPU-days at peak and at the given utilization, GPU-hours, dollar cost, and the weight memory floor. Add `--tokens`, `--active-params` (MoE), `--flops`, `--gpus`, `--gpu-tflops`, `--utilization`, `--price`, `--bytes-per-param` as needed. Run `python3 scripts/scaling_calculator.py --budget-flops 1e22` to compute the compute-optimal model size and token count for a FLOP budget.
- Run `python3 scripts/sampling_demo.py --logits 5,3.5,3,2,-1 --temperature 0.7 --top-p 0.9` to compute how temperature, `--top-k`, `--top-p` and `--min-p` (relative by default, `--min-p-absolute` for a fixed floor) reshape a next-token distribution; add `--samples 1000 --seed 7` to see empirical frequencies.
