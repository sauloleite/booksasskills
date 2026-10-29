# System-Level Evaluation: End-to-End, Consistency, Coherence, Hallucination, Unexpected Inputs

## Contents
- End-to-end scenarios
- Limits of automated end-to-end testing
- Consistency
- Coherence
- Hallucination
- Unexpected and hostile inputs
- Worked example: one case, five lenses

Integration tests exist because agent modules feed each other: a slightly wrong memory lookup becomes a wrong plan, which becomes a wrong tool call. These emergent problems are invisible to unit tests.

## End-to-end scenarios

Goal: complete user journeys under realistic conditions, exercising perception, planning, tool calls and the final message together.

Harness pattern:
1. Load a case (input state, conversation, expected final state).
2. Invoke the full agent once.
3. From the trace, take the last assistant message that is not a tool request as the final reply, and collect every tool call with parsed arguments.
4. Score parameter accuracy, tool recall and precision, phrase recall, plus a binary **task success** that requires all of them to be satisfied.
5. Aggregate across dozens to hundreds of cases and per tag.

Extend the same harness to latency, throughput and behavior under load, and to failure paths: when a tool fails, does the agent try a fallback or escalate to a human instead of inventing a result?

Harness decision: a case that throws (parse error, timeout, crash) should count as a failure, not be skipped. Skipping removes the hardest cases from the denominator and inflates scores.

## Limits of automated end-to-end testing

- Scores are only as good as the cases and metrics. Narrow sets produce agents that pass offline and fail live.
- Leaning on few metrics causes metric overfitting; text agents tuned to BLEU or exact match drift to formulaic wording that misses intent.
- Remedy: keep the suite alive. Add cases for new features, real user behavior and newly seen failure modes; bring in internal reviewers and pilot users to find blind spots; revise metrics as you learn what success really means.

## Consistency

LLM agents are nondeterministic, so consistency is not "same bytes every time". It means outputs stay aligned with the input, coherent over long exchanges, and on target for what the user asked.

What to check:
- **Policy invariants across phrasings**: the same required step happens regardless of wording (for example, evidence is requested before any refund call).
- **Input alignment**: answers address the actual question; automated checkers cross-reference outputs with the input context and flag mismatches for review.
- **Long-session stability**: over many turns the agent does not contradict earlier statements (for example about order status) or drift off topic. Requires long simulated conversations.
- **Run-to-run variance**: repeat each case several times and measure how often the action set matches the most common one.

Evaluation layers, combined rather than chosen:
1. **LLM-as-judge**: same or related model grades outputs for consistency and relevance; give it few-shot examples of acceptable and unacceptable responses to make grading reliable.
2. **Actor-critic**: one model generates, a critic scores against explicit alignment and relevance criteria. Useful, but insufficient alone in complex or fast-changing scenarios.
3. **Human review**: for nuance, ambiguity and edge cases where automated judges are weak.

Warning: an agent can pass every standard test and still behave erratically on out-of-distribution input. Schedule manual inspection and refresh eval data periodically.

## Coherence

Coherence is about the logic of the whole interaction: context retained, actions in a sensible goal-directed order, no contradictions.

Tests:
- Simulate extended, multi-step interactions and check that the agent's view of state stays correct.
- The agent reuses what it already knows (earlier report, uploaded evidence, preferences) and never makes the user repeat it.
- Follow-up requests (an address change after a refund) build on prior turns without contradicting them.
- Dependencies are respected: no recommendation that conflicts with an earlier one, no action that ignores a prerequisite, no forgotten items in multi-item orders.
- Tone stays professional and unambiguous.

Flag any contradiction or lapse as a coherence failure; track these as a separate tag so the trend is visible as sessions grow longer.

## Hallucination

Hallucination is fabricated, wrong or nonsensical content. It is most damaging where the agent retrieves knowledge, makes decisions, or talks to users.

Four levers:
1. **Grounding**: tie answers to verifiable sources, typically with RAG over trusted material. Domain-grounded tools (legal research is a cited example) hallucinate less than general models.
2. **Content accuracy testing**: cross-check outputs against authoritative references (clinical guidelines for medical agents, validated databases for factual QA). Audit the knowledge base and the decision logic on a schedule.
3. **Data dependence**: outputs can only be as good as their sources. Test that the agent pulls from current, complete, vetted sources and ignores unverified ones; stale or partial corpora are a hallucination risk in themselves.
4. **Feedback loops**: monitor outputs, flag errors, and route them to domain experts; in dynamic settings, compare predictions with observed outcomes and trigger data or model updates automatically.

Current direction the chapter highlights:
- Hybrid human-AI oversight in real time for high-stakes domains (healthcare, legal, crisis response) so fabrications are caught before they spread, while easing the user's cognitive load.
- Cost-aware evaluation: measure hallucination reduction against added inference cost (extra retrieval, verification passes, larger models) and choose the cheapest configuration that meets the accuracy bar.

## Unexpected and hostile inputs

Feed inputs that break design assumptions: odd formats, slang, typos, malformed identifiers, partially failed services, and malicious content. Required behavior: no crash and no harmful output; instead clarify, decline or escalate.

- Combine random fuzzing with systematic edge cases derived from past incidents and adversarial analysis.
- Mixed or contradictory intents (cancel an order that already shipped and was delivered) must lead to clarification or escalation, not a wrong tool call.
- Under stress the agent must not leak sensitive data, break policy or trigger downstream failures; this is mandatory for safety-critical use.
- Keep extending these tests as the agent gains features.

## Worked example: one case, five lenses

Case: user writes "ordr #Z77 the blender came brokn, also send future stuff to my new place". Input state: delivered order Z77 with a blender and a spare jar.

| Lens | Pass looks like | Typical failure |
|---|---|---|
| End-to-end | Refund only the blender amount; ask for the new address; reply confirms both | Refunds whole order |
| Consistency | Evidence request appears in every rephrasing of the case | Refunds without evidence in 2 of 5 reruns |
| Coherence | Address change handled after refund without restating the problem | Asks again which item broke |
| Hallucination | Refund timing quoted from policy source | Invents "24 hours" |
| Unexpected input | Typos parsed or clarified | Calls lookup with "ordr" as ID |
