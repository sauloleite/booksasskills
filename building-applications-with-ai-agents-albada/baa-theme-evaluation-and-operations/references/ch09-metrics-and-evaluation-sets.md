# Metrics and Evaluation Sets

## Contents
- Why measurement comes first
- Choosing metrics
- Wiring evaluation into the development loop
- Anatomy of a scorable eval case
- Growing the eval set
- Benchmarks: public vs custom
- Pitfalls
- Glossary

## Why measurement comes first

Without a stable, repeatable score, a team cannot tell a real improvement from noise, cannot see how the agent behaves under realistic or hostile input, and cannot catch regressions. Shipping pressure tempts teams to skip this; the chapter's position is that the time spent on rigorous evaluation is repaid because decisions about what to ship become fast and defensible. Informal review ("looks better to me") is explicitly ruled out: even experienced teams convince themselves of progress that is not there.

Start from **hero scenarios**: a short list of high-priority, representative use cases that define whether the agent is worth having. Every metric should trace back to one of them. For a support agent, a hero scenario might be "customer reports one damaged item in a multi-item delivered order and gets a partial refund".

## Choosing metrics

Pick a mix, tied to the objective (engagement, automation of a process, resolution rate):

| Family | Examples | Use for |
|---|---|---|
| Action correctness | tool recall, tool precision, parameter accuracy | Did the agent do the right things with the right arguments |
| Output content | phrase recall, semantic similarity | Did the user-facing message say what it had to |
| Classic quality | accuracy, precision, recall | Classification-like sub-decisions (intent, routing) |
| Operational | latency, throughput, robustness, scalability, cost | Can it run in production |
| Human | satisfaction, reviewer ratings, user feedback | What automated scores miss |

Text outputs: exact match under-credits correct answers phrased differently. Prefer meaning-aware scoring: embedding distance, BERTScore, or n-gram overlap scores (BLEU, ROUGE) as rough proxies. Use required-phrase checks only for things that truly must appear (a refund timeline, a legal disclaimer).

Decision rule: never let one score stand alone. Optimizing a single text metric pushes agents toward stilted, template-like replies (see "metric overfitting" in the glossary).

## Wiring evaluation into the development loop

1. Automate offline evaluation and trigger it on every merge and every model or prompt change.
2. Keep one consistent, versioned record of key metrics over time so regressions show up as a drop against history, not as a vague feeling.
3. Every new tool or workflow ships together with new eval cases covering it. The eval set grows with capability; progress is measured across the whole expanding scope, not a frozen benchmark.
4. Compare historical results per slice to catch the classic trap: a headline gain that hides a new failure in some older feature.
5. Supplement automation with regular sampling and human review, especially in novel or high-stakes domains.
6. Treat both the agent and the metrics as iterable; revise metrics when requirements or user behavior change.

## Anatomy of a scorable eval case

A case must pin down the starting state and the expected end state so scoring needs no human. Minimum fields:

- **Input state**: the domain objects the agent sees (order with items, prices, status, dates).
- **Conversation history**: prior turns, including any evidence the user already provided.
- **Expected final state**: tool calls with exact parameters, plus phrases the final reply must contain.
- **Metadata** (strongly recommended): tags such as intent, difficulty, failure type, feature area, origin (hand-written, mined, generated). These drive coverage tracking and per-slice reporting.
- **Forbidden actions** (an addition worth making): tools that must not be called, for example no cancellation on an already-delivered order.

One well-built case checks several skills at once. Example (invented): an order holds a lamp at 45.00 and a shade at 15.00; the user says the shade arrived torn and has sent a photo. Expected: one refund call for 15.00 on that order ID, and a reply mentioning the refund and its timing. Refunding 60.00 drops parameter accuracy; omitting the timeline drops phrase recall; also calling a cancel tool drops precision. Each failure lands in a different metric, which makes the signal actionable.

Validate the cases themselves: check that the expected parameters are consistent with the input state (same order ID, amounts that exist in the order). A typo in ground truth silently caps the score of a correct agent.

## Growing the eval set

Hand-curated, static suites are not enough: they overfit, miss the long tail, and fall behind changing workflows. Sources, in rough order of trustworthiness:

1. **Hand-written by engineers with subject matter experts**: defines tasks, ground truth and success criteria for new domains.
2. **Mined from production**: support logs and API traces converted into cases (scrub personal data first).
3. **Model-generated, human-reviewed**: ask an LLM to add ambiguity, unusual idioms, or to mutate passing cases into edge cases. Never admit generated cases without review.
4. **Targeted stress generation**:
   - Adversarial search: hunt for a user message that makes the agent contradict itself or break policy.
   - Counterfactual edits: change a single token (an item name, a date) and check whether the outcome flips when it should, and only then.
   - Intent interpolation: blend two intents (refund plus address change) to create deliberately ambiguous requests.

Over time the set becomes a **living specification**: the authoritative statement of what the agent must handle. It powers regression detection and continuous monitoring and keeps attention on the places that matter, not just the average.

## Benchmarks: public vs custom

Public suites (MMLU, BBH, HELM) position a model against the field and help with model selection. They say little about a domain agent's tool use. For a domain agent, a custom benchmark with SME-defined ground truth is mandatory; public scores are context only.

## Pitfalls

- Evaluating only at the end of the project instead of continuously.
- Narrow or unrepresentative cases: offline scores look great, production fails.
- A single headline metric hiding slice-level regressions.
- Generated cases admitted without review, encoding the generator's own mistakes.
- Ground truth that contradicts its own input state.
- No metadata, so a failure rate cannot be traced to a feature or failure type.

## Glossary

- **Hero scenario**: a high-priority, representative use case used to anchor metrics.
- **Living specification**: an eval set that is continuously extended and serves as the definition of required behavior.
- **Metric overfitting**: tuning to a benchmark score at the expense of real usefulness.
- **Phrase recall**: share of required phrases present in the final reply.
