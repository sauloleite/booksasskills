# Service-Level Optimization and Serving Modes

## Contents
- Scope
- Online, batch and streaming APIs
- Batching
- Decoupling prefill and decode
- Prompt caching
- Parallelism
- Choosing techniques by workload
- Playbooks
- Worked examples
- Pitfalls

## Scope

Service-level techniques manage resources: given fixed compute and memory and a shifting stream of requests (possibly for several models), allocate them to meet latency and cost goals. They leave the model untouched and should not change outputs, so they are the safest first stop when self-hosting.

## Online, batch and streaming APIs

| Mode | Optimizes | Terms | Use for |
|---|---|---|---|
| Online | Latency; handled on arrival (may still micro-batch if latency allows) | Standard price | Chat, coding assistants, anything a user waits on |
| Batch | Cost and throughput via aggressive batching and cheaper hardware | Gemini and OpenAI offered about 50% off, turnaround in hours | Synthetic data; periodic reports (channel digests, brand sentiment, ticket analysis); onboarding a customer's document set; reprocessing after a model migration; personalized recommendations or newsletters at scale; knowledge base reindexing |
| Streaming | Perceived latency; tokens sent as generated | Same as online | Long human-read responses |

Streaming means you cannot score the whole response before the user sees it. Mitigate with incremental checks and the ability to retract or edit output once a problem is detected.

**Not classical batch inference.** Traditional ML precomputes predictions for a finite, predictable input set (recommendations for every user) before requests arrive. Open-ended prompts cannot be enumerated; only predictable parts like the system prompt can be prepared, which is what prompt caching does.

**If you run the service** and demand can exceed the rate you serve without latency loss, expose separate online and batch endpoints so less urgent traffic queues and online capacity goes to latency-sensitive requests.

## Batching

Grouping concurrent requests is one of the easiest cost cuts: one weight read serves many sequences. Careless batching makes everyone wait; good batching costs little latency.

| Type | Rule | Strength | Weakness |
|---|---|---|---|
| Static | Run when a fixed count has arrived | Full batches | First request waits for the last; bad for interactive use |
| Dynamic | Run when full or when a time window expires (e.g., 8 requests or 50 ms) | Bounded wait | Partly empty batches waste compute |
| Continuous (in-flight) | Batch per decode step; finished sequences return at once and new requests take their slot (Orca paper) | High occupancy, no waiting on long neighbors | Needs a server that supports it (vLLM, TensorRT-LLM, TGI and similar) |

Request-level batching is especially bad for LLMs because output lengths vary: a 10-token answer batched with a 1,000-token answer waits for it. Continuous batching removes that coupling. For dynamic batching, set both max size and max wait and tune them against goodput. For continuous batching, KV cache memory usually sets the effective cap.

## Decoupling prefill and decode

On shared GPUs the phases fight: a GPU near full compute could absorb more decode work, but each new request also brings a prefill that grabs compute and stalls running decodes, inflating their TPOT.

**Disaggregation** runs prefill and decode on separate instances. DistServe and Inference Without Interference found this substantially increases requests served within latency limits for popular models. The KV state must move from prefill to decode instances, but on modern clusters with fast links such as NVLink within a node that overhead is small.

Prefill:decode instance ratio depends on input lengths and priorities:

| Workload | Priority | Starting ratio |
|---|---|---|
| Long inputs | TTFT | 2:1 to 4:1 |
| Short inputs | TPOT | 1:2 to 1:1 |

These are starting points (Meta has discussed such ratios publicly); tune from measured traffic. Shifting instances between pools is also how you trade TTFT against TPOT.

## Prompt caching

Also called context or prefix cache: store the processed state of shared prompt segments and reuse it.

Pays off for long system prompts, long documents queried repeatedly (a book, a codebase), long conversations (earlier turns processed once) and many-shot prompts.

Scale: a multi-thousand-token system prompt across hundreds of thousands of daily calls means hundreds of millions to billions of repeated input tokens a day avoided. Provider terms at the time of writing: Gemini discounted cached input 75% but charged for storage (about $1 per million tokens per hour); Anthropic advertised up to 90% cost savings (larger for longer cached prefixes) and up to 75% lower latency. Anthropic's published scenarios showed the largest TTFT gain when chatting over a very long cached document, a smaller latency gain but large cost cut for many-shot prompts, and roughly halved cost for multi-turn chat with a long system prompt.

Constraints:

- The cache uses memory, like the KV cache.
- Building one yourself takes significant engineering; prefer provider or framework support. (llama.cpp's caching appeared limited to reusing earlier messages within one session at the time of writing.)
- Caching works on prefixes: put stable content first; timestamps, user IDs or retrieved snippets placed early break reuse.
- Hosted caches may impose minimum lengths, expiry and write or storage fees; include them in cost models.

## Parallelism

Data parallelism (called replica parallelism in serving) and model parallelism apply to any model; context and sequence parallelism target long LLM inputs. Deployments often combine several.

- **Replica**: run several full copies. Simplest; more concurrency; each replica handles fewer requests so latency improves, at the cost of more chips. With many model sizes and GPU types, placement is bin-packing: with a fixed fleet, decide replicas per model and which GPU type hosts each. (Buying chips for a fixed replica set is the rarer reverse problem.)
- **Model parallelism** splits one model across devices when it does not fit, making placement harder.
  - **Tensor (intra-operator)**: partition each operator's tensors (e.g., split a weight matrix by columns) and run the pieces in parallel. Serves models too big for one device and lowers latency, minus communication overhead. The most common split for inference.
  - **Pipeline**: assign consecutive layer groups to devices and stream micro-batches through them. Good for throughput and common in training, but stage-to-stage communication adds per-request latency; for strict latency use replicas instead.
- **Context**: split the input sequence across devices (first half here, second half there).
- **Sequence**: split the operators for the whole input across devices (attention on one, feedforward on another).

Context and sequence parallelism are less common and mostly matter for very long inputs.

## Choosing techniques by workload

- Long contexts: KV cache management matters far more than for short ones.
- Long shared prefixes or multi-turn chat: prompt caching is crucial.
- Latency over cost: add replicas so each machine gives each request more resources.
- Model too big: tensor parallelism first; pipeline only for throughput.
- Mixed output lengths: continuous batching.
- Interference between new and running requests: disaggregate prefill and decode.
- No deadline: batch API or internal batch queue.

Across use cases the author ranks four as most consistently impactful: quantization, tensor parallelism, replica parallelism and attention optimization.

## Playbooks

**Hosted API user**
1. Send every job nobody waits on to the batch API.
2. Stream long human-read responses; add retroactive moderation.
3. Order prompts stable-first (instructions, tool definitions, examples, shared documents); enable caching; verify hit rates in usage data.
4. Constrain output length.
5. Stay under rate limits with queueing and backoff.

**Self-hoster**
1. Use a mature server with continuous batching, paged KV cache, fused attention, prefix caching and speculative decoding.
2. Replicas if the model fits one device; tensor parallelism if not or if latency must drop; no pipeline parallelism for interactive traffic.
3. Treat placement as bin-packing over your model mix and GPU types.
4. At scale, split prefill and decode pools and set the ratio from input lengths and priorities.
5. Offer separate online and batch endpoints if demand can exceed capacity.
6. Load-test with realistic length distributions; tune for goodput.

## Worked examples

**Caching savings.** A support assistant sends a 3,000-token stable prefix on 200,000 calls/day: 600M prefix tokens. At $3 per million input tokens, $1,800/day uncached; with 90% off cached reads, about $180/day plus write and storage fees. A timestamp at the start of the prompt would make every call miss.

**Bin-packing.** An 80 GB GPU with 8-bit models: one 70B replica (about 70 GB, little cache room) or two 34B replicas (about 68 GB). If the 34B queue is backing up and the 70B tier has spare replicas elsewhere, choose two 34B; if the 70B tier is the bottleneck, choose it. Decide from per-model demand and SLO data, not memory occupancy.

## Pitfalls

- Static batching for user-facing traffic.
- Tuning batch size for throughput while goodput drops.
- Co-locating prefill and decode at high load.
- Variable content ahead of stable content; ignoring cache storage fees.
- Building a prompt cache from scratch without budgeting memory and effort.
- Pipeline parallelism for latency-critical serving.
- Streaming with no plan to retract bad output.
