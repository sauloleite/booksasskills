# Setting Expectations, Milestone Planning, and Maintenance

Covers the planning work after the decision to build: defining success, usefulness thresholds, measuring the starting point, budgeting the last mile, and keeping a product alive in a fast-moving field. Use it when writing success criteria, a delivery plan, or a risk register for an AI product.

## Contents
- Success starts with business metrics
- Usefulness thresholds
- Latency arithmetic for thresholds
- Milestone planning from a measured baseline
- The last-mile problem
- Maintenance: the change landscape
- Maintenance playbook
- Worked examples
- Pitfalls

## Success starts with business metrics

The most important metric is business impact. For a support chatbot: share of messages fully handled, extra volume absorbed, response-time reduction, labor saved. Give each a number and date, and map business metrics to model metrics and back.

Volume is not happiness: a bot answering more messages can still annoy users. Always pair throughput with satisfaction and feedback signals that have an owner.

## Usefulness thresholds

Define how good the product must be before users see it:

| Group | What to specify |
|---|---|
| Quality | Task-appropriate response quality measures (open-ended tasks need deliberate evaluation design) |
| Latency | TTFT and TPOT (delay until the first token; time for each later token), plus total latency |
| Cost | Cost per inference request, times expected volume |
| Other | Interpretability, fairness, domain or regulatory needs |

Benchmark latency against the current process, not an ideal: if humans answer with a median of about an hour, a one-minute reply already wins; an inline autocomplete competes with typing and needs sub-second behavior. Provisional metrics are fine at first.

## Latency arithmetic for thresholds

- Total latency is roughly TTFT + TPOT x (output tokens - 1).
- Tokens is roughly words / 0.75 (English, GPT-4-class tokenizer).
- At 10 ms per token, 100 tokens take about a second, far above the roughly 100 ms typical of web interactions. Use streaming (TTFT then dominates perceived speed), shorter outputs, or precomputation for proactive features.

The bundled `scripts/usefulness_check.py` does this arithmetic plus cost per request against targets.

## Milestone planning from a measured baseline

1. **Evaluate off-the-shelf models first.** Where you start determines the effort. The stronger the available model, the less work remains.
2. **Express the gap.** Example: target is automating 60% of tickets; the candidate model already handles 30% unaided. The remaining 30 points is the project, and it is smaller than starting from zero.
3. **Re-decide after evaluation.** Goals change once you see real numbers. If reaching the usefulness threshold will cost more than the product will return, stop or rescope. This is a successful outcome of planning, not a failure.
4. **Define milestones as metric thresholds** (for example 40%, 50%, 60% automation at a given satisfaction floor), not as feature lists.
5. **Put evaluation and versioning in place early**, so each iteration is measurable and model swaps are tests rather than gambles.

## The last-mile problem

Early success misleads: a fun demo may take a weekend, a solid product months or years. Evidence for inflated expectations:
- A research team building a chat dataset found the first 60% easy and the remaining 40% very hard.
- LinkedIn reached about 80% of its target experience in a month, badly underestimated the rest, and needed four more months to pass 95%, mostly on product rough edges and hallucinations, with each extra point slower than the last.

Rules: never extrapolate demo velocity; budget the tail explicitly (in the LinkedIn case the last 15 points took about four times as long as the first 80); track per-point progress near the top; reserve time for hallucination mitigation and UX polish.

## Maintenance: the change landscape

Building on foundation models means riding a field that moved extremely fast for a decade and likely will for the next. Classify changes by how hard they are to absorb.

- **Good but disruptive.** Longer context, better outputs, faster and cheaper inference (benchmark scores per dollar climbed steeply since 2022). Each can invalidate a past decision: self-hosting chosen as cheaper can become the expensive option when API prices halve months later; a third-party platform you built around can fold after failing to raise money.
- **Easier.** Providers converge on similar APIs, so swapping endpoints is mechanically simple, but each model has its own quirks, so prompts, workflows and data need re-tuning. Without versioning and evaluation, this hurts.
- **Hard: regulation and supply.** Many countries treat compute, talent and data as national security matters. Data protection compliance is costly (GDPR was estimated at billions for businesses). Export rules can cut off GPU supply to your country overnight.
- **Potentially fatal: intellectual property.** IP law for AI is unsettled; if your product relies on a model trained on others' data, ownership of outputs may be uncertain. IP-heavy firms such as game studios hesitate for this reason.

## Maintenance playbook

1. Schedule periodic cost-benefit reviews for each major technology choice (model, provider, hosting, vector store, framework). Assume the best option today can become the worst tomorrow.
2. Keep the model layer swappable behind an internal interface.
3. Version prompts, retrieval configs and datasets alongside code.
4. Maintain an evaluation suite that runs on any candidate model, so swaps are measurable.
5. Track vendor health and have an exit plan for critical third parties.
6. Maintain a regulatory watchlist (data protection, compute export controls, sector rules) with an owner.
7. Get legal review of IP exposure before building IP-sensitive products on third-party models.

## Worked examples

**Support bot plan.** Goals: automate 50% of tier-1 tickets in two quarters with CSAT within 2 points of the human baseline. Baseline: best API model resolves 28% unaided. Thresholds: rubric-scored quality on a labeled sample; TTFT under 1.5 s; total under 8 s for a 120-word reply (about 160 tokens); under $0.01 per request. Milestones: 35%, 42%, 50%. If 35% arrives in a month, plan at least three more months for 50%.

**Hosting reversal.** A team self-hosts to save 40% versus an API. Six months later the API halves its price and improves. The quarterly review catches it, and the swappable model layer plus evaluation suite make migration a one-sprint job.

## Pitfalls

- Optimizing automation rate while satisfaction falls.
- Using an abstract latency ideal instead of the current process as the bar.
- Shipping below the usefulness threshold because a demo impressed someone.
- Planning without a baseline evaluation, or treating "stop after evaluation" as failure.
- Assuming today's cheapest option stays cheapest, or swapping models without re-tuning and evaluation.
- Ignoring regulatory, supply and IP risk until it bites.
