# Inference Metrics and Measurement

## Contents
- Who cares about which metric
- Latency: TTFT, TPOT, time to publish
- Percentiles and outliers
- Throughput
- Cost per request
- The latency/throughput trade-off and goodput
- Utilization: nvidia-smi, MFU, MBU
- Measurement playbook
- Worked examples
- Pitfalls

## Who cares about which metric

Users feel **latency**. Quality belongs to the model, not the serving stack (but re-check it after lossy optimizations). Developers feel **throughput** and **utilization**, because they set cost. Tie everything to explicit service-level objectives (SLOs).

## Latency: TTFT, TPOT, time to publish

- **TTFT**: time to first token. Mostly prefill, so it rises with input length and queueing. Chat should feel immediate; long-document summarization may wait longer. (Some early chatbots were slowed on purpose to seem human; users no longer want that.)
- **TPOT**: time per output token after the first. Mostly decode. At 50 ms per token, 600 tokens take 30 s.
- **TBT / ITL**: time between tokens (LinkedIn) and inter-token latency (NVIDIA); same idea as TPOT.

**Total latency = TTFT + TPOT x output tokens.**

For streamed reading, TPOT only needs to beat reading speed. A very fast reader manages about 120 ms per token, so 6 to 8 tokens/s per stream suffices for most streamed UIs; extra speed mainly helps non-streamed or machine-consumed output.

**Profiles matter, not just totals.** Equal totals can feel different: an instant first token then slow tokens, or a short wait then fast tokens. Settle the preference with user studies. You move along this trade-off by shifting instances between prefill and decode.

**Time to publish.** Agents and chain-of-thought may plan, call tools and log results before writing anything visible. The model's first token comes early; the user's first visible token comes late. Track time to publish separately or dashboards will look healthy while users wait.

## Percentiles and outliers

One pathological request (network error, huge prompt) can multiply the mean and make a fast service look slow. At volume, such outliers are certain.

- Report p50 plus p90, p95, p99. The median shows the typical user, the tails show the unlucky ones and expose faults.
- Investigate tails rather than trimming them.
- Plot TTFT against input length. A smooth upward trend means prompt size explains slowness; high points at short lengths suggest queueing or infrastructure trouble.

## Throughput

- **Output TPS**: output tokens per second across all requests; the default meaning of "throughput".
- **Input (prefill) throughput**: count separately. Blending input and output hides that they have different bottlenecks and often run on different machines.
- **Tokens/s/user**: shows how per-user speed degrades with concurrency.
- **RPS / RPM**: completed requests per second or minute; RPM suits multi-second LLM calls. It shows how the system handles concurrency, and providers may throttle bursts.

Smaller models and stronger chips go faster; steady input/output lengths are far easier to optimize than variable ones. Tokens are not a common currency across tokenizers, so compare servers or providers by **cost per request** on your traffic.

## Cost per request

Self-hosted:

1. Decode cost per output token = hourly price / (output tokens/s x 3,600).
2. Decode cost per request = that x average output tokens.
3. Prefill cost per request = hourly price / requests prefilled per hour.
4. Total = prefill + decode.

Hosted: input tokens x input price + output tokens x output price, with cached input discounted. Output tokens are typically priced 2 to 4x input, and one output token was measured to affect latency about as much as 100 input tokens. Shortening outputs is often the cheapest lever.

## The latency/throughput trade-off and goodput

Batching and concurrency raise throughput and cut cost but slow each request. LinkedIn's team reported 2x to 3x throughput is common if you accept worse TTFT and TPOT. Lower cost can be bought with latency; lower latency usually costs money.

**Goodput** (borrowed from networking) counts requests per unit time that meet the SLO. Maximize it when tuning batch size, concurrency limits and instance ratios; push throughput only while goodput keeps rising.

## Utilization: nvidia-smi, MFU, MBU

**nvidia-smi GPU utilization** is the fraction of time the GPU is busy at all. A GPU doing 1% of its possible work, continuously, reports 100%. It says nothing about value for money.

**MFU** (model FLOP/s utilization, named in the PaLM paper): observed throughput relative to what the chip would achieve at advertised peak FLOP/s; equivalently achieved FLOP/s over peak (use about 2 x parameters FLOPs per generated token as the forward-pass estimate).

- Training MFU exceeds inference MFU (predictable, well-batched work).
- Prefill MFU exceeds decode MFU.
- For training, above 50% is considered good and hard to reach; well-known large runs landed roughly between 20% and 46%.

**MBU** (model bandwidth utilization): achieved bandwidth over peak. At batch 1, bandwidth used is about parameters x bytes per parameter x tokens/s. Halving bytes per parameter halves bandwidth for the same speed, the clearest argument for quantization.

Reading them together:

- Compute-bound: high MFU, low MBU. Bandwidth-bound: the reverse.
- MBU tends to fall as concurrent users increase, because each weight read serves more sequences and work drifts toward compute-bound (published Llama 2-70B measurements across chips show this).
- Both scale linearly with throughput, so some people say "throughput" meaning either.

Rising utilization on the same workload and hardware usually signals better efficiency. But a change that lifts utilization while making cost and latency worse is a bad change.

## Measurement playbook

1. Write SLOs per use case: p95 TTFT (or time to publish), p95 TPOT, max cost per request.
2. Log per request: arrival time, input and output tokens, TTFT, TPOT, total latency, cache hit, model, hardware.
3. Aggregate percentiles, input and output TPS, RPM, goodput, cost per request.
4. Self-hosted: add MFU and MBU per phase.
5. Plot TTFT vs input length and TPOT vs concurrency.
6. Benchmark candidates on a replay of your traffic by cost per request and goodput.
7. After every change, rerun performance and quality evals.

## Worked examples

**Self-hosted cost.** $4/hour instance, 400 output tokens/s: 1.44M tokens/hour, about $2.78 per million. 1,000 requests at 500 output tokens: about $1.39. Prefill runs 200 requests/minute, so 1,000 requests take 5 minutes: $0.33. Total about $1.72 per 1,000 requests. Cutting average output to 300 tokens saves about $0.56 per 1,000.

**MBU.** 8B model in INT8 decoding one stream at 150 tokens/s moves 8e9 x 1 x 150 = 1.2 TB/s; on a 3.35 TB/s chip, about 36% MBU. In FP16 the same speed needs 2.4 TB/s (about 72%). Check arithmetic carefully: a 7B FP16 model is 14 GB per step, so 100 tokens/s at batch 1 needs 1.4 TB/s (70% of a 2 TB/s A100-80GB), not 0.7 TB/s. At batch B, divide tokens/s by B to get steps/s, and add KV cache bytes read per step.

**MFU of that run.** About 2 x 8e9 x 150 = 2.4 TFLOP/s, well under 1% of a modern GPU's peak. Normal for single-stream decode, and exactly the idle compute that batching and speculative decoding reclaim.

**Goodput.** SLO: TTFT at most 500 ms and TPOT at most 50 ms. In one minute, 60 requests finish and 45 meet both: throughput 60 RPM, goodput 45 RPM. If a bigger batch lifts throughput to 80 RPM but only 40 meet the SLO, the product got worse.

**Mean vs median.** Nine requests near 100 ms TTFT and one at 2,500 ms: mean about 340 ms, median about 100 ms. One incident to investigate, not a slow service.

## Pitfalls

- Average-only dashboards.
- Measuring model TTFT instead of time to publish in agent pipelines.
- Blending input and output tokens into one throughput figure.
- Comparing tokens/s across tokenizers.
- Tuning for throughput or utilization while goodput falls.
- Treating nvidia-smi busy time as efficiency.
