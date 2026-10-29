---
name: ai-eng-ch09-inference-optimization
description: Makes LLM and foundation model inference faster and cheaper, based on Chapter 9 of Chip Huyen's "AI Engineering". Covers latency/cost metrics (TTFT, TPOT, goodput, MFU, MBU), compute vs bandwidth bottlenecks, accelerator selection, KV cache sizing, quantization, speculative decoding, batching, prefill/decode split, prompt caching and parallelism. Use when an endpoint is slow or expensive, when sizing GPUs or memory, choosing online vs batch APIs, or comparing inference providers and serving frameworks.
---

# Inference Optimization (AI Engineering, Ch. 9)

## Purpose

Guide an agent through diagnosing and reducing the latency and cost of running foundation models, whether through a hosted API or a self-hosted server. The chapter's stance: name the bottleneck first, measure with the right metrics, then pick from model-level, hardware-level and service-level levers, combining several in production. Hosted-API users mostly control API mode, prompt caching, prompt and output length, model choice and measurement; self-hosters control everything else too. Either way, understanding the techniques is what lets you judge providers and frameworks.

## Key decision rules

Apply these even without opening a reference.

1. **Find the bound before fixing anything.** Prefill is compute-bound and drives TTFT; decode is memory bandwidth-bound and drives TPOT. Compute-bound work wants FLOP/s or more chips; bandwidth-bound work wants faster memory or fewer bytes per step. "Memory-bound" is ambiguous (bandwidth vs capacity/OOM): clarify which.
2. **Latency = TTFT + TPOT x output tokens.** For streamed reading, about 6 to 8 tokens/s per stream (roughly 120 ms/token) is enough. In agent or chain-of-thought flows, track time to publish (first token the user sees), not model TTFT.
3. **Report percentiles, never just the mean.** p50 plus p90/p95/p99; investigate outliers; plot TTFT against input length.
4. **Optimize goodput, not raw throughput.** Goodput counts only requests that meet the SLO. Batching can double or triple throughput while hurting TTFT/TPOT.
5. **Compare providers by cost per request on your own traffic,** not tokens/s, because tokenizers differ.
6. **Ignore nvidia-smi "GPU utilization" as an efficiency signal.** Use MFU and MBU. Utilization is diagnostic; the goals are speed and cost.
7. **Output tokens are the expensive ones.** Priced around 2 to 4x input tokens, and one output token costs roughly as much latency as 100 input tokens. Shorter outputs and faster decode pay off disproportionately.
8. **Route deadline-free work to batch APIs** (about 50% cheaper, hours of turnaround). Stream long human-read responses, with a plan to retract bad output after display.
9. **Put stable content first in prompts and enable prompt caching** whenever system prompts, shared documents, many-shot examples or chat history repeat.
10. **Weight-only quantization is the default first model-level step;** distillation if you can fund training for a narrow task; pruning last. Re-run quality evals after any model-level change, since providers serving the same model can score differently.
11. **Lossless decode speed-ups:** speculative decoding for decode-bound serving with idle compute (gains shrink when MFU is already saturated; draft model should share the tokenizer); inference with reference when outputs copy the input (RAG, code edits, chat).
12. **KV cache = 2 x batch x seq_len x layers x hidden x bytes** (replace hidden with kv_heads x head_dim for GQA/MQA). It can exceed weight memory; budget it before buying hardware.
13. **Self-hosting defaults:** a server with continuous batching, paged KV cache, fused attention kernels and prefix caching; compile the model.
14. **Parallelism:** replicas for scale and latency; tensor parallelism when the model does not fit or latency must drop; avoid pipeline parallelism for latency-critical serving.
15. **At scale, split prefill and decode onto separate instances.** Start near 2:1 to 4:1 prefill:decode for long inputs prioritizing TTFT, and 1:2 to 1:1 for short inputs prioritizing TPOT.
16. **Most consistently impactful techniques:** quantization, tensor parallelism, replica parallelism, attention optimization.

## Default workflow

1. **Set targets.** Per use case: p95 TTFT (or time to publish), p95 TPOT, total latency, cost per request.
2. **Instrument.** Per request: input/output tokens, TTFT, TPOT, total, cache hits. Run `scripts/latency_report.py` for percentiles and goodput.
3. **Locate the bottleneck.** High TTFT means prefill (long prompts, queueing, no cache); high TPOT means decode (bandwidth, interference from prefills, oversized batches). If self-hosting, compute MFU/MBU with `scripts/mfu_mbu.py`.
4. **Take cheap wins first.** Batch API for offline jobs, prompt caching, shorter outputs, streaming.
5. **Fit and size.** Use `scripts/kv_cache_size.py` for weights plus KV cache at target batch and context; quantize or add tensor parallelism if it does not fit.
6. **Apply serving levers.** Continuous batching, prefix caching, speculative decoding or inference with reference, replicas, disaggregation at scale.
7. **Model-level changes last,** each followed by a quality eval.
8. **Re-measure one change at a time,** using goodput and cost per request (`scripts/request_latency_cost.py`).

## References

- [references/metrics-and-measurement.md](references/metrics-and-measurement.md): read when defining SLOs, building dashboards, computing cost per request, goodput, MFU or MBU, or interpreting utilization numbers.
- [references/bottlenecks-and-hardware.md](references/bottlenecks-and-hardware.md): read when deciding whether a workload is compute- or bandwidth-bound, comparing or buying accelerators, or reasoning about memory hierarchy, power and TDP.
- [references/model-compression-and-decoding.md](references/model-compression-and-decoding.md): read when choosing among quantization, distillation and pruning, or tuning speculative decoding, inference with reference, or parallel decoding (Lookahead, Medusa).
- [references/attention-kv-cache-and-kernels.md](references/attention-kv-cache-and-kernels.md): read when the KV cache limits batch or context, when selecting attention variants (GQA, MQA, local, cross-layer), PagedAttention or KV compression, or when working with kernels and compilers.
- [references/service-level-optimization.md](references/service-level-optimization.md): read when choosing online, batch or streaming APIs, configuring batching, splitting prefill and decode, setting up prompt caching, or picking a parallelism strategy and GPU placement.
- [references/source-map.md](references/source-map.md): read to find which reference covers a given section of the chapter.

## Scripts

All scripts use only the Python 3 standard library; each supports `--help`.

- Run `python3 scripts/kv_cache_size.py --layers 32 --hidden 4096 --heads 32 --kv-heads 8 --batch 16 --seq-len 8192 --params-b 8 --gpu-gb 80 --overhead-gb 8` to compute KV cache size (MHA, GQA or MQA), compare it with weight memory, and estimate how many sequences fit on a GPU.
- Run `python3 scripts/request_latency_cost.py --ttft-ms 400 --tpot-ms 30 --input-tokens 3000 --output-tokens 400 --input-price 3 --output-price 15 --cached-tokens 2500 --cache-discount 0.9` to compute total latency and API cost per request with prompt caching; or pass `--hourly-cost 4 --decode-tps 400 --prefill-rpm 200` instead of prices to compute self-hosted cost per request.
- Run `python3 scripts/mfu_mbu.py --params-b 7 --bytes-per-param 2 --tokens-per-s 100 --peak-bw-tbs 2 --peak-tflops 312` to compute MBU, MFU and the bandwidth-limited decode ceiling (add `--batch` and `--kv-gb-per-step` for batched decode).
- Run `python3 scripts/latency_report.py timings.csv --slo-ttft-ms 500 --slo-tpot-ms 50 --window-s 60` to compute p50/p90/p95/p99 latency, SLO attainment, throughput and goodput from a CSV with `ttft_ms` and optional `tpot_ms`, `output_tokens`, `total_ms`, `start_s` columns.
