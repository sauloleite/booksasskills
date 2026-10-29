# Context Construction and Guardrails (Steps 1 and 2)

## Contents
- Starting point and build order
- Step 1: enhance context
- Step 2: input guardrails
- Step 2: output guardrails and failure policies
- Guardrail implementation trade-offs
- Worked example: bank support assistant
- Pitfalls and glossary

## Starting point and build order

The baseline is a single hop: the app forwards the query to a model (hosted API or self-hosted server) and returns the result, with no context augmentation, checks, or optimization. Every later component should be justified by a named weakness of this baseline. Common progression: context, guardrails, routing plus gateway, caching, agentic logic with write actions; observability throughout, orchestration as glue. Reorder when your risk or cost profile demands it (a healthcare app may need guardrails before retrieval).

## Step 1: enhance context

Context construction is to foundation models what feature engineering was to classical ML: it decides what information the model sees. Sources are retrieval (text, image, tabular) and information-gathering tools (web search, news, weather, events APIs). Nearly every provider offers native file upload and tool calling, so the decision is whether that suffices.

| Axis | What to check |
|---|---|
| Document volume | File count and format limits; a dedicated RAG stack is bounded mainly by your vector store |
| Retrieval configuration | Retrieval algorithm, tunable chunk size and overlap |
| Tools | Supported tool categories |
| Execution modes | Parallel function calls, long-running jobs |

Rule of thumb: prototype on provider-native features; move to a dedicated retrieval pipeline when volume, format variety, or tuning needs exceed them.

## Step 2: input guardrails

Two risks: **private data leaving the organization** through an external API, and **malicious prompts** that compromise the system. Neither reaches zero, because generation is probabilistic and people err; plan for residual risk.

**Three leak paths** (scanning only user text covers one):
- Users paste confidential or personal data into a prompt (a well-known case involved an employee pasting proprietary code into a public chatbot).
- Developers embed internal policies or data in the system prompt.
- Tools pull private records from internal databases into context.

**Detection.** You define the sensitive classes: personal identifiers (ID, phone, bank account, address), faces, and keywords tied to intellectual property or privileged information. Detectors are often ML models with false negatives; measure their recall on your data.

**Response.** Block the whole query when the data class is too dangerous or the query is meaningless once redacted; otherwise redact and continue:
1. Replace each entity with a numbered typed placeholder (`[PHONE_1]`, `[EMAIL_2]`); numbering avoids ambiguity when several entities share a type.
2. Keep a per-request reverse map (placeholder to original) in request memory; never send it to the model.
3. Send the masked prompt; substitute originals back into the response; discard the map.

## Step 2: output guardrails and failure policies

Output guardrails **detect** failures and **apply a policy** per failure type. The cheapest detection is an empty response where one was expected (a user may legitimately request empty output).

- **Quality failures**: wrong format (invalid JSON, missing keys), factual inconsistency, simply poor output.
- **Security failures**: toxic content, leaked private data, output that triggers remote tool or code execution, brand risk (misrepresenting you or competitors).

**False refusals.** An over-strict system blocks legitimate work and frustrates users. Report false refusal rate next to every safety metric.

| Failure | Default policy |
|---|---|
| Empty or malformed | Retry up to a cap or until valid |
| Low quality | Regenerate or fall back to a stronger model, after a scorer flags it |
| Unsafe | Block, return a safe message, log for review |
| Tricky or charged conversation | Human handoff |

**Retry economics.** A retry issued after a failure adds a call and roughly doubles perceived latency for that request. Sending two calls at once and keeping the better one holds latency flat but pays for redundant calls on every request. Prefer parallel when latency binds and failures are frequent; sequential when failures are rare and cost dominates.

**Handoff triggers seen in practice:** specific phrases (legal threats, billing disputes), a sentiment model detecting anger, or a turn count past a limit to stop users from looping.

## Guardrail implementation trade-offs

- **Reliability vs latency.** Guardrails add calls. Some teams skip them for speed; if you do, record it as an owned risk acceptance.
- **Streaming vs checks.** Non-streamed output can be checked but makes users wait; streamed partial text is hard to judge, so unsafe content may display before a block. Mitigate by buffering a window of tokens, checking at sentence boundaries, retracting on detection, or disabling streaming on risky routes.
- **Hosted vs self-hosted.** Hosted APIs bundle safety filters, so you build less, but providers tune for a broad customer base, so filters may be too strict or too loose for you. Self-hosting removes external-leak risk and shrinks input guardrails, but you own all output filtering.
- **Placement.** Provider, inference service, gateway, or standalone service. Off-the-shelf: Meta Purple Llama, NVIDIA NeMo Guardrails, Microsoft PyRIT, Azure AI content filters, Perspective API, OpenAI moderation. Most cover inputs and outputs because the risks overlap.
- **Scorers** are usually smaller models; place them behind the gateway with other models or inside the output guardrail block, whichever keeps ownership clearest.

## Worked example: bank support assistant

A support bot on a hosted model retrieves FAQs and the customer's recent transactions.
1. Leak paths: user may type a card number; system prompt holds internal escalation codes; the transaction tool injects account numbers. Scan all three.
2. Input policy: mask card and account numbers with numbered placeholders; block any query containing a full PIN or password.
3. Output policy: validate JSON (two retries), scan for toxicity and PII, block on failure, hand off on detected anger or after eight turns.
4. Streaming: off for answers mentioning transfers, sentence-level checks elsewhere.
5. Metrics: guardrail trigger rate, false refusal rate on a labeled sample, latency added per check.

## Pitfalls and glossary

Pitfalls: scanning only user messages; assuming provider filters or self-hosting remove the need for your own guardrails; measuring blocks but not wrongful blocks; streaming a risky flow with no partial-output strategy; one placeholder per type when several entities share it.

- **Reverse PII map**: per-request table from placeholders back to original values.
- **False refusal rate**: share of legitimate requests wrongly declined.
- **Scorer**: model grading output quality or safety, typically smaller than the generator.
