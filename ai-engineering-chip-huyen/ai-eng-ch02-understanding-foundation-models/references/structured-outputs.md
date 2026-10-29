# Structured Outputs

## Contents
- When structure is required
- Tools and what JSON mode guarantees
- The escalation ladder
- Prompting, post-processing, retries
- Constrained sampling
- Finetuning and classifier heads
- Decision procedure
- Worked example
- Pitfalls and glossary

## When structure is required

1. **The task is structured.** Semantic parsing: text-to-SQL (a revenue question becomes a valid Postgres query), text-to-regex, or classification restricted to allowed labels.
2. **Downstream code consumes the output.** An email body needs no structure, but the system storing it may require JSON with fixed keys. This is critical in agent workflows, where outputs feed tools.

## Tools and what JSON mode guarantees

Libraries include guidance, outlines, instructor and llama.cpp; providers add their own methods (OpenAI shipped the first JSON mode). JSON mode typically guarantees syntax only, not correct keys or values. Output can still be cut off at the max-token limit and fail to parse, while a very high limit adds latency and cost. Observed JSON validity varies from 0% to the high 90s by model and task, so measure.

## The escalation ladder

Prompting, post-processing and retry-until-valid are bandages for a model that is nearly compliant. Constrained sampling and finetuning are intensive treatment.

| Layer | Best when | Cost | Guarantee |
|---|---|---|---|
| Prompting | Model follows formats well | Lowest | None |
| Prompting plus AI validator | Validity matters, budget allows | Two or more calls | Better, not absolute |
| Post-processing | Small, repetitive errors | Cheap | Only fixable errors |
| Retry until valid | Checkable, failures rare | Scales with failure rate | Eventually, no bound |
| Constrained sampling | Supported grammar, logit access | Grammar work, latency | Syntax |
| Finetuning | High volume, any format | Training | Very reliable; heads guarantee labels |

## Prompting, post-processing, retries

- **Prompting** is the first step; success depends on instruction-following ability and instruction clarity. A few percent invalid can still be unacceptable. A second call that checks and fixes output (AI as judge) raises validity at extra cost and latency.
- **Post-processing**: models repeat the same mistakes, so catalogue them and repair in code (add a missing closing bracket). LinkedIn's defensive YAML parser raised valid output from 90% to 99.99%; LinkedIn also picked YAML because it uses fewer output tokens than JSON. Works only when outputs are nearly right.
- **Retries**: validate mechanically (parser, schema, SQL dry run) and regenerate on failure, or run several in parallel and keep the first valid one.

## Constrained sampling

At each step, logits are filtered to tokens the constraint allows, then sampling proceeds among them. Trivial for a fixed label set; real formats need a grammar of what may follow what (in JSON, a brace cannot directly follow a brace outside a string). Trade-offs: each format needs its own grammar, so it generalizes poorly; grammar checks can add latency; logit access is required; and some argue the effort is better spent improving instruction following.

## Finetuning and classifier heads

Finetuning on examples in the target format is the most effective and general method, for any format; not a strict guarantee, but far more reliable than prompting. For fixed labels, attach a classifier head so the model can only output a valid class (feature-based transfer), training end to end (costlier, better) or just the head. Some finetuning services once added heads automatically; check current availability.

These techniques exist because models are assumed unable to produce structure unaided. As instruction following improves they may matter less, so re-test before maintaining heavy machinery.

## Decision procedure

1. Define the schema and a programmatic validator first.
2. Prompt with an explicit format and measure the invalid rate on realistic inputs.
3. Repair recurring small errors in code; remeasure.
4. Add retry-until-valid if failures are rare and checkable.
5. Use constrained decoding or provider structured modes for hard syntactic guarantees; still validate content.
6. Finetune for high volume, tight latency or unusual formats; use a classifier head for fixed labels.
7. Size max tokens with headroom and keep a fallback path.

## Worked example

An invoice extractor returns eight-field JSON. Prompting yields 94% parsable output. Most failures are trailing commas and a missing final brace; a repair function lifts parsing to 99.4%. The rest are truncations on long invoices, fixed by raising max tokens from 300 to 600 (the longest valid object was about 420). Field accuracy remains 91%, which validity does not touch, so the team plans a finetune on 2,000 labeled invoices.

## Pitfalls and glossary

Pitfalls: treating JSON mode as correctness; token limits or stop words that truncate payloads; building grammars when a modest finetune would teach the format; skipping validation because decoding is constrained; paying for an AI validator when code repair suffices.

- **Semantic parsing**: language to machine-readable structure.
- **Defensive parser**: tolerates and repairs common format slips.
- **Constrained sampling**: masking logits to grammar-permitted tokens.
- **Feature-based transfer**: adding a task head to a base model.
