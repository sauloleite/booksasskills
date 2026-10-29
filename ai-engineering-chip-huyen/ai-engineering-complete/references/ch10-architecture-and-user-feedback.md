---
name: ai-eng-ch10-architecture-and-user-feedback
description: Use when designing or reviewing an LLM app's end-to-end architecture (context, guardrails, routers, gateways, caching, agent loops, write actions), setting up monitoring, logs, traces and drift detection, picking an orchestrator, or designing and safely using user feedback. Based on Chapter 10 of Chip Huyen's "AI Engineering".
---

# Chapter 10: Architecture and User Feedback (AI Engineering, Chip Huyen)

The chapter assembles earlier techniques into one production system, then treats user feedback as both an evaluation signal and a proprietary data asset. Guidance is organized around decisions.

## When to use this skill

- An engineer asks which components an LLM app needs and in what order to add them.
- Reviewing an architecture diagram for missing pieces (no guardrails, no gateway, no tracing, unsafe caching).
- Deciding whether to add a router, a model gateway, a semantic cache, or an orchestration framework.
- Handling PII before calling a third-party model API.
- Defining production metrics, logging policy, traces, alerts, and drift checks for an LLM system.
- Designing thumbs up/down, regeneration, side-by-side comparison, or edit-based feedback flows.
- Mining chat logs for implicit signals of failure or user preference.
- Deciding whether and how to feed user feedback back into prompts, evaluation sets, or finetuning, and what can go wrong.

## Core mental models

**Grow the architecture incrementally.** Start with the minimal loop (query to a hosted or self-hosted model, response back) and add components only when a need appears. Typical order: context, guardrails, routing and gateway, caches, agentic loops and write actions; observability throughout, orchestration as glue. The order is common, not mandatory.

**Context construction is feature engineering for foundation models.** Retrieval (text, image, tabular) and information tools (search, news, weather APIs) supply what the model needs. Providers differ in file count and type limits, retrieval and chunking choices, supported tools, parallel function calls, and long-running jobs. A dedicated RAG stack scales with your vector store; a generic upload feature usually does not.

**Guardrails sit wherever risk is exposed.** Two families:
- Input guardrails defend against (a) leaking private data to an external API and (b) malicious prompts that compromise the system. Risk can be reduced, never removed, because generation is probabilistic and humans make mistakes.
- Output guardrails do two jobs: detect failures and define a policy for each failure type.

**Routers pick the right handler per query.** Usually an intent classifier (or a next-action predictor in agents, or a memory-tier selector in systems with memory). Benefits: specialized handlers can outperform a generalist; cheap models handle easy queries; out-of-scope queries get a canned reply without an API call; ambiguous queries trigger a clarification question. Routers must be small, fast, and cheap so you can afford several. Common pattern: route, retrieve, generate, score. Routing can also happen after retrieval (for example, escalation to a human).

**A model gateway is a single controlled door to all models.** Minimum: a unified interface over hosted and self-hosted models, so an upstream API change is fixed in one place. Usual extras: access control (no raw org keys in many hands), per-user or per-app model permissions, usage limits and cost tracking, fallback when the primary provider is down or rate limited, retries, load balancing, logging, analytics, sometimes caching and guardrails. The same idea can apply to tools (a tool gateway), though it was not yet common at the time of writing.

**Caching at the system level.** (Inference-level KV and prompt caching belong to the model provider or serving stack, covered in Chapter 9.)
- Exact cache: reuse only on identical inputs. Also useful for caching vector-search results. Most valuable when a query triggers multi-step reasoning or slow actions (retrieval, SQL, web search). Back it with memory, Redis, PostgreSQL, or tiered storage, plus an eviction policy (LRU, LFU, FIFO).
- Semantic cache: reuse when a new query embeds close enough to a cached one. Raises hit rate but can lower quality, because it depends on good embeddings, working vector search, a reliable similarity metric, and a well-tuned threshold. It also adds its own vector-search latency and compute, which grows with cache size.

**Agent patterns add loops and side effects.** Outputs can be fed back for another retrieval or generation round (loops, branches, parallel steps). Write actions (sending email, placing orders, moving money) massively expand capability and risk; grant them with extreme caution. Every added component adds failure modes and debugging difficulty.

**Monitoring vs observability.** Monitoring watches external outputs to notice trouble. Observability means the system is instrumented well enough that internal state can be inferred from logs, metrics, and traces without shipping new code to debug; it covers instrumenting, tracking, and debugging. Goals mirror evaluation: reduce risk (failures, attacks, drift), find opportunities (quality, cost savings), and provide accountability. Design it in from day one; complexity raises its importance.

**Measure observability itself with DevOps metrics.** MTTD (time to detect), MTTR (time to resolve after detection), CFR (share of deployments needing a fix or rollback). Not knowing your CFR is a sign the platform needs redesign. A high CFR points at the pre-deployment evaluation pipeline more than at monitoring.

**Metrics, logs, traces form a debugging chain.** Metrics are aggregated and tell you *that* something broke. Logs are an append-only event record that tell you *what* happened. Traces link related events into a per-request timeline that tells you *where* in the pipeline it broke (bad query processing, irrelevant retrieval, or wrong generation), with per-step timing and cost.

**Drift has three common sources in LLM apps.** Silent system prompt changes (template updates, a colleague's typo fix); user behavior adapting to the product (for example, users learning to ask for brevity, causing response lengths to fall); and the provider updating the model behind an unchanged API name (documented cases show measurable benchmark shifts between dated versions of the same model family, and one company reported roughly a 10% drop after switching versions).

**User feedback is a product signal and a data moat.** It evaluates the app, guides development, and personalizes behavior per user. It is proprietary data that feeds the data flywheel: launch early, attract users, collect feedback, improve models, widen the lead. It is also user data, so privacy and transparency obligations apply. Open source self-hosted deployments make feedback collection much harder.

**Explicit vs implicit feedback.** Explicit (ratings, thumbs, a yes/no on whether the problem was solved) is easy to interpret but sparse and subject to response bias (unhappy users speak up more). Implicit (inferred from actions and conversation) is abundant and app-specific but noisy and ambiguous; the same action can mean opposite things for different users. Conversational interfaces make giving feedback natural and extracting it hard.

## Decision frameworks

### Which component to add next

| Symptom | Add | Watch out for |
|---|---|---|
| Answers lack facts the model cannot know | Retrieval or info-gathering tools | Provider limits on docs, chunking, tool modes |
| Risk of PII or secrets leaving the org | Input PII detection with mask/unmask | Detector misses; system prompts and tools also leak |
| Bad formats, hallucinations, toxic or brand-risky outputs | Output guardrails with per-failure policy | Latency; streaming bypasses checks |
| One expensive model handles everything; off-topic queries | Router (intent classifier) | Router latency and errors; context-size mismatch across models |
| Many teams, many models, leaked keys, outages | Model gateway | Gateway becomes a critical dependency |
| Repeated identical heavy queries | Exact cache | User-specific or time-sensitive answers |
| Many paraphrased repeats and high expected hit rate | Semantic cache (only after evaluating) | Wrong hits return wrong answers |
| Tasks need iteration or real-world effects | Agent loops, then write actions | Blast radius of write actions |
| Multi-step pipeline with branching, many components | Orchestrator (later, not first) | Hidden abstraction and calls |

### Output failure handling policy

- Empty or malformed output: retry (sequentially is cheap but can double perceived latency; issuing two calls in parallel and picking the better keeps latency flat at the cost of redundant calls).
- Quality failures (bad format, factual inconsistency, generally poor output) and security failures (toxicity, sensitive data, triggering remote tool or code execution, brand misrepresentation): block, regenerate, or escalate.
- Escalate to a human when: specific trigger phrases appear, a sentiment model detects anger, or the conversation exceeds N turns (loop prevention).
- Always track false refusals alongside safety failures; an overly strict system blocks legitimate work.

### Guardrail placement trade-offs

- Reliability vs latency: some teams skip guardrails for speed. Treat that as an explicit, documented risk acceptance, not a default.
- Streaming vs output checks: streaming improves perceived latency but partial outputs are hard to judge, so unsafe text may reach the user before a block decision. Options: buffer chunks, check at sentence boundaries, or disable streaming for high-risk flows.
- Third-party API vs self-hosted: providers ship many built-in safety filters, reducing what you build; self-hosting removes the external-leak risk, reducing the input guardrails you need. Providers balance safety against flexibility, so their filters may be too tight or too loose for your case.
- Where to implement: model provider, inference service, gateway, or standalone component. Off-the-shelf options include Purple Llama, NeMo Guardrails, PyRIT, Azure AI content filters, Perspective API, and OpenAI's moderation endpoint. Many cover both input and output.

### Sensitive data in inputs

If detected: block the whole query, or redact it. For redaction, replace each entity with a typed placeholder, keep a per-request reverse map, and restore originals if placeholders appear in the response. Define your own sensitive classes: personal identifiers (IDs, phone numbers, bank accounts), faces, and keywords tied to IP or privileged information. Scan all three leak paths: users pasting secrets into prompts, developers embedding internal data in system prompts, and tools pulling private records into context.

### Should this response be cached?

- Cache: generic, stable, reused across users, expensive to compute.
- Do not cache: user-specific (order status), time-sensitive (weather), or anything whose generation pulled in user-specific context even though the question looks generic; serving it to another user is a data leak.
- Many teams train a small classifier to predict cacheability; set TTL by expected reuse.
- Semantic cache only if: measured hit rate is high, threshold is tuned on real data, and the cost of a wrong hit is acceptable.

### Router context mismatch

When a routed model's context window cannot hold the context that later accumulates (for example, a tool returns far more tokens than the target model accepts), either truncate to fit or reroute to a larger-context model.

### Orchestrator selection (only once complexity justifies it)

Start without one: frameworks hide critical behavior and make debugging harder. When you do adopt one (LangChain, LlamaIndex, Haystack, Flowise, Langflow, and many RAG or agent frameworks), assess:
1. Integration and extensibility: supports your models, stores, and tools now and later; how hard to add what is missing.
2. Complex pipeline support: branching, parallelism, error handling.
3. Ease of use, performance, scale: clear APIs, docs, community; no hidden API calls or added latency; scales with apps, developers, and traffic.

Note that an AI pipeline orchestrator is a different thing from a general workflow scheduler like Airflow or Metaflow.

### Interpreting implicit signals (context dependent)

| Signal | Usually means | Caveat |
|---|---|---|
| Stopping generation, leaving, not answering the agent | Going badly | Could be satisfied early |
| Follow-up opens with a negation or a restated intent; rephrasing | Misunderstood intent | Detect via heuristics or a model |
| Specific corrections or action nudges to an agent | Concrete error or missed step | Very common in agentic use |
| Asks the model to double-check or cite sources | Missing detail or low trust | Not proof the answer was wrong |
| User edits output | Strong negative on the edited part | Also yields a preference pair |
| Complaints, negative sentiment trajectory | Failure; cluster by type | Anger that resolves to calm is a success |
| Model refusals or admissions of not knowing | User likely unhappy | Track refusal rate |
| Regenerate | Dissatisfied | Or exploring options (creative tasks); stronger with usage billing |
| Delete conversation | Bad | Or embarrassment |
| Rename conversation | Good conversation, bad auto-title | |
| Share | Either very good or very bad | Varies by user; combine signals |
| Many turns | Engaged (companion apps) | Inefficient (support/productivity apps) |
| Long + low diversity | User stuck in a loop | Measure distinct tokens or topics |

Published clustering of conversational feedback in a search-grounded chat dataset found that restating the request was the largest category (roughly a quarter), followed by complaints of non-answers or irrelevance, pointers to the right search result, and claims of factual error; complaints about hedging or rudeness were small. Use such a taxonomy to map complaint types to fixes (verbosity complaints lead to a conciseness instruction; missing-detail complaints lead to a specificity instruction).

## Step-by-step playbooks

### Playbook A: Build the production architecture

1. Ship the minimal path behind a thin internal interface, with logging from day one.
2. Add retrieval and tools; compare provider-native support against a dedicated RAG stack.
3. Add input and output guardrails with an explicit per-failure policy (retry, parallel sample, block, human handoff).
4. Introduce a gateway once there are several models or consuming teams.
5. Add small-classifier routers for intent, scope, ambiguity, and next action.
6. Add an exact cache with a cacheability policy; evaluate semantic caching separately.
7. Add loops and read-only tools before write actions; gate write actions with tight permissions and human approval where stakes are high.
8. Parallelize independent steps when latency is tight (for example, PII scrubbing and routing at once).
9. Keep components modular but accept overlap (guardrails can live in the gateway, inference service, or standalone).

### Playbook B: Instrument for observability

1. Name the failure modes first, then derive metrics from them (hallucination leads to a "is the output supported by context" check; runaway spend leads to tokens per request and cache hit rate).
2. Start with easy, verifiable ones: empty outputs, format validity, and the share of invalid outputs that are trivially repairable vs missing required fields.
3. Add open-ended quality (factual consistency, conciseness, other app-specific traits, often via AI judges) and safety (toxicity, PII in and out, guardrail trigger rate, refusal rate, anomalous queries).
4. Add conversational signals: mid-generation stops, turns per conversation, input and output token lengths, output token distribution over time.
5. Add per-component metrics (retrieval context relevance and precision; vector DB index size and query latency), latency (TTFT, TPOT, total, per user), and cost (query volume, tokens, TPS, RPS against rate limits).
6. Correlate metrics with north star business metrics (DAU, session duration, subscriptions) to learn what to optimize and what to ignore.
7. Make metrics sliceable by user, release, prompt or chain version and type, and time; mix spot checks with exhaustive checks as budget allows.
8. Log everything with tags and IDs: endpoint, model, sampling settings, prompt template, raw query, final prompt, intermediate and final outputs, tool calls and results, component start, end, and crash events. Keep ingestion delay low.
9. Emit per-request traces with step timing and cost.
10. Add drift detectors: diff the effective system prompt, track behavior trends, pin and canary model versions.
11. Read a sample of production traffic daily; your judgment of good and bad evolves with exposure and should update both prompts and evaluation.
12. Feed every incident back into the evaluation set so offline and online metrics stay aligned.

### Playbook C: Debug a production incident

1. A metric alert says something broke; pull logs for that window and check whether it happened before.
2. Correlate log errors with the metric to confirm the cause, then open traces of affected requests to locate the failing step.
3. Check drift sources (prompt diff, model version, user behavior shift).
4. Fix, add a regression case to evaluation, record MTTD and MTTR.

### Playbook D: Design a feedback system

1. Decide the uses: evaluation metrics, development data (prompts, finetuning, preference data), personalization.
2. Choose touchpoints:
   - Onboarding: calibration only if required for function; otherwise optional with a neutral default that adapts over time.
   - On failure: easy downvote, regenerate, switch model, direct edit, and escalation to a human if frustration grows. Let users finish their task despite errors (human-AI collaboration, like region-level image editing).
   - On low model confidence: offer alternatives (for example, short vs detailed summary side by side, if latency allows) or ask a targeted question.
   - On success: optional positive signal, possibly shown to a small random slice of users (the chapter's example is about 1%), knowing smaller samples carry more bias. Some design guidelines discourage soliciting praise, but positive feedback reveals which features users love.
3. Embed collection into the workflow so it costs nothing extra: accept/ignore of inline suggestions, choosing which of several outputs to upscale or vary, edits to drafts. Integrated products observe downstream use; standalone chat apps cannot see whether output was used.
4. Capture context with the signal (the preceding several turns), which requires consent: product terms or an explicit data-donation checkbox.
5. Tell users how feedback is used (personalization, aggregate stats, training) and make only true privacy promises.
6. Make options unambiguous: always offer an abstain or unsure option, never ask preference on questions with objectively correct answers the user cannot judge, use icons and tooltips, and test scale direction (a reversed emoji scale produced inverted ratings in one real form).
7. Decide private vs public visibility: private signals tend to be more candid and plentiful; public signals aid discoverability and explain recommendations.
8. Convert signals into data: edits and regenerate-then-compare choices become (prompt, preferred, rejected) triples for preference finetuning.

### Playbook E: Use feedback safely

1. Inspect rating distributions for leniency bias; use descriptive labels instead of bare numeric stars to get finer signal.
2. Randomize order in comparisons to counter position and recency bias; or model success rate conditional on position.
3. Watch for length preference and random clicks when comparisons are long.
4. Remember you only observe feedback on what you showed; add exploration so early leaders do not lock in.
5. Before training on feedback, check for sycophancy: optimizing for approval teaches models to agree rather than be accurate.
6. Monitor population drift caused by your own adaptation (a niche taste amplifying until it defines the product and user base).

## Checklists

**Architecture review**
- [ ] PII masking covers user input, system prompt, and tool results
- [ ] Per-failure output policy; false refusals tracked; streaming risk handled
- [ ] Gateway with scoped keys, quotas, fallback, logging
- [ ] Routers small and fast; out-of-scope and ambiguous paths defined
- [ ] Cache excludes personalized and time-sensitive answers; eviction set; semantic cache justified by data
- [ ] Write actions gated and auditable; independent steps parallelized

**Observability**
- [ ] MTTD, MTTR, CFR known; metrics tied to named failure modes
- [ ] Latency and cost dashboards, sliceable by user, release, prompt version, time
- [ ] Full logs with IDs, per-request traces, low ingestion delay
- [ ] System prompt diff alert; model version pinning; daily sample review

**Feedback**
- [ ] Purpose of each signal defined; collection non-intrusive and easy to ignore
- [ ] Consent path for context capture; clear UI with an abstain option
- [ ] Randomized option order; bias and degenerate-loop review before training

## Pitfalls and anti-patterns

- Adding every component up front; or assuming self-hosting or provider filters make guardrails unnecessary.
- Unmeasured over-blocking; streaming that bypasses output checks in risky domains.
- Raw provider keys shared across teams instead of a gateway.
- Caching personalized answers under a generic key (cross-user leak); semantic caching without hit-rate data.
- Casual write-action permissions.
- Observability as an afterthought; metrics tied to no failure mode or business goal; delayed or ID-less logs.
- Trusting that a model behind a fixed API name never changes.
- Starting with a heavy orchestration framework and losing visibility.
- Reading ambiguous implicit signals (regenerate, share, long chats) literally.
- Demanding extra effort for feedback (breeds lazy positive ratings) or asking users to judge what they cannot evaluate.
- Training on raw feedback: popularity loops, amplified harmful tastes, sycophancy.
- Leaving feedback design only to product teams; engineers must shape it to get usable training data.

## Key terms

- **Reverse PII map**: per-request mapping from placeholders back to original values.
- **False refusal rate**: share of legitimate requests wrongly blocked.
- **Router / intent classifier / next-action predictor**: small models that choose the handler, scope, or next step.
- **Model gateway**: unified, access-controlled interface to multiple models with fallback and usage tracking.
- **Exact cache / semantic cache**: reuse on identical input / on embedding similarity above a threshold.
- **MTTD, MTTR, CFR**: detection time, resolution time, change failure rate.
- **TTFT, TPOT, TPS, RPS**: time to first token, time per output token, tokens per second, requests per second.
- **North star metric**: core business metric (DAU, session duration, subscriptions).
- **Trace**: linked, timed record of one request through all components.
- **Drift**: changes in prompts, user behavior, or underlying models over time.
- **Orchestrator / chaining**: tool that defines components and composes them into a pipeline.
- **Natural language feedback**: feedback carried in message content (corrections, complaints, sentiment).
- **Leniency, position, recency, length (preference) bias; randomness**: distortions in feedback.
- **Degenerate feedback loop**: predictions shape the feedback that retrains them, amplifying initial bias (exposure or popularity bias, filter bubbles).
- **Sycophancy**: tendency of feedback-trained models to tell users what they want to hear.

## Source map

- AI Engineering Architecture
  - Step 1. Enhance Context
  - Step 2. Put in Guardrails (Input guardrails; Output guardrails; Guardrail implementation)
  - Step 3. Add Model Router and Gateway (Router; Gateway)
  - Step 4. Reduce Latency with Caches (Exact caching; Semantic caching)
  - Step 5. Add Agent Patterns
  - Monitoring and Observability (Monitoring versus observability; Metrics; Logs and traces; Drift detection)
  - AI Pipeline Orchestration
- User Feedback
  - Extracting Conversational Feedback (Natural language feedback: early termination, error correction, complaints, sentiment; Other conversational feedback: regeneration, conversation organization, conversation length, dialogue diversity)
  - Feedback Design (When to collect feedback; How to collect feedback)
  - Feedback Limitations (Biases; Degenerate feedback loop)
- Summary
