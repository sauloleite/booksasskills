# Routers, Model Gateways, and System Caches (Steps 3 and 4)

## Contents
- Routers: purpose and kinds
- Router design and placement
- Model gateway
- System caching scope
- Exact caching and cacheability
- Semantic caching and the adoption decision
- Pitfalls and glossary

## Routers: purpose and kinds

With more than one model or handler, a router picks which serves each query. Benefits:
- **Specialization**: a domain handler (troubleshooting, billing) can beat a generalist on its slice.
- **Cost**: cheap models for easy queries, the expensive one for hard queries.
- **Scope control**: out-of-scope queries (politics, unrelated chat) get an approved stock decline with no generation call.
- **Ambiguity**: a vague query (one word that could be an account action or small talk) triggers a clarifying question.

| Router | Decides | Example |
|---|---|---|
| Intent classifier | Which handler | Password reset to an FAQ link, billing correction to a human, troubleshooting to a specialist bot |
| Next-action predictor | Agent's next step | Code interpreter or search API |
| Memory-tier selector | Where to look | A document attached earlier in the session, or the web |

## Router design and placement

- **Small, fast, cheap**, because you will chain several. Teams adapt BERT-class, GPT-2-class, or 7B-scale open models, or train tiny classifiers from scratch.
- **Context-window mismatch.** Context can grow after routing. Example: a 1,000-token query goes to a 4K-window model; a web search then returns 8,000 tokens. Truncate to fit, or reroute to a larger-window model. Decide in advance.
- **Placement.** Routers are models, so they sit with other models behind the gateway. Logically, routing usually precedes retrieval (is the query in scope; does it need retrieval) but can follow it (escalate to a human given what was found). The dominant shape is route, retrieve, generate, score.

## Model gateway

A single internal layer through which every app reaches every model, hosted or self-hosted. **Core function:** a unified interface, so a provider API change is fixed once instead of in every app; the minimal version is a thin wrapper mapping a model-type field to the right client.

Functions added because all traffic passes through it:

| Function | Benefit |
|---|---|
| Access control | Teams hold gateway credentials, never raw organization keys that leak easily |
| Fine-grained permissions | Which user or app may call which model |
| Quotas and cost tracking | Abuse prevention, spend attribution |
| Fallback | On outage or rate limit (outages are common): alternate model, retry after a pause, graceful degradation |
| Load balancing, logging, analytics | One consistent control point |
| Caching, guardrails | Offered by some gateways |

Off-the-shelf examples: Portkey AI Gateway, MLflow AI Gateway, Wealthsimple LLM Gateway, TrueFoundry, Kong, Cloudflare. Building in-house is also common. A tool gateway is a plausible analog but was uncommon at the time of writing; orchestrators and gateways increasingly absorb each other's features.

**Adopt when two or more hold:** multiple providers or a hosted plus self-hosted mix; multiple consuming teams; raw keys copied across codebases; need for per-team spend or quotas; an outage or rate limit has already hurt you. Then treat the gateway as critical infrastructure with redundancy and its own monitoring.

## System caching scope

KV and prompt caches live in the serving stack and are out of scope here. This step adds application-level exact and semantic caches; standard caching practice applies.

## Exact caching and cacheability

Reuse only on an identical key: a summary of a specific product, or **vector search results** for a previously seen query. Highest payoff when the uncached path is multi-step or slow (chain-of-thought, retrieval, SQL, web search). Store in memory for speed, or Redis, PostgreSQL, or tiered storage for capacity; always set an eviction policy (LRU, LFU, FIFO).

Retention depends on expected reuse. **Do not cache:**
- User-specific queries (my order status); nobody else will ask.
- Time-sensitive queries (current weather); answers go stale.
- Any answer generated with user-specific context, even if the question looks generic.

The last is a data leak. If a retailer's return policy varies by membership tier, an answer to customer A's generic-looking question may embed A's account details; cached under the question text, it is then served to customer B. **Rule:** key on everything that shaped the answer (user or tier IDs included), or skip caching whenever personal context was retrieved. Many teams train a small classifier to predict cacheability and set TTL by expected reuse.

## Semantic caching and the adoption decision

Reuse an answer when a new query is similar enough: embed the query, find the nearest cached query embedding, return its answer if similarity exceeds a threshold, otherwise run the pipeline and insert the new entry. Requires a vector store.

Its value is doubtful by default because many parts can fail: embedding quality, nearest-neighbor accuracy, a similarity metric that reflects true equivalence, and a threshold that takes much trial and error (too low serves wrong answers confidently, too high yields few hits). A false match returns a wrong answer with no generation-time check. The lookup also costs latency and compute on every query, growing with cache size.

**Adopt only if, on real traffic:** many queries are genuine paraphrases; a threshold exists with acceptable wrong-hit rate on a labeled sample; and hit rate times avoided cost exceeds per-query lookup cost plus the cost of wrong hits.

Worked numbers: generation 1.2 s and $0.004 per query; lookup 40 ms and $0.0001. At a 30% hit rate, latency is 0.04 + 0.7 x 1.2 = 0.88 s and cost 0.0001 + 0.7 x 0.004 = $0.0029. At 3%, latency is 0.04 + 0.97 x 1.2 = 1.204 s, worse than no cache. Latency break-even is lookup time over generation time, 0.04 / 1.2, about 3.3%. `scripts/cache_savings.py` computes this, including a wrong-hit penalty.

## Pitfalls and glossary

Pitfalls: routers expensive enough to erase their savings; no policy for context outgrowing the routed model; raw keys spread across teams; a gateway without fallback or monitoring; personalized answers cached under generic keys; semantic caching without measured hit and wrong-hit rates.

- **Next-action predictor**: router inside an agent choosing the next tool or step.
- **Fallback policy**: gateway behavior when the primary model is unavailable.
- **Eviction policy**: rule for removing cache entries (LRU, LFU, FIFO).
