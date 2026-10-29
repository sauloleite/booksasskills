# Writing Effective Prompts: Instructions, Context, Decomposition, Reasoning, Iteration

## Contents
- Durable practices versus hacks
- Clear and explicit instructions
  - Remove ambiguity
  - Use a persona when perspective matters
  - Add examples where behavior is non-obvious
  - Specify output format and use end markers
- Providing sufficient context
- Restricting the model to its context
- Decomposing complex tasks
- Giving the model time to think (CoT and self-critique)
- Iterating on prompts
- Worked example: from monolith to chain
- Pitfalls
- Glossary

## Durable practices versus hacks

Early tricks (a shorter question label, a promised cash tip) helped some weak models and decay as models grow more robust. Prefer practices that hold across providers (the chapter distills OpenAI, Anthropic, Meta and Google guidance plus production teams' experience), then add model-specific quirks from that model's own guide and the provider's prompt libraries.

## Clear and explicit instructions

### Remove ambiguity

Write the instruction so two different engineers would implement the same grader from it. For any scoring or labeling task, state:
- The scale and its bounds (1 to 5 or 1 to 10).
- Whether non-integers are allowed.
- What to do under uncertainty: commit to a best guess, or emit an explicit sentinel such as UNSURE.
- What to do for out-of-scope input.

Then watch outputs and patch observed misbehavior with a targeted instruction. If the grader returns 3.5 and you need integers, say integers only. Each patch should be traceable to a failure you saw.

### Use a persona when perspective matters

A persona tells the model which standards to apply. The same short, simple paragraph written by a six-year-old deserves a low score from a generic critic and a high score from an early-grade teacher. Use a persona when the right answer depends on audience or expertise (a pediatric nurse explaining dosage, a senior reviewer judging code style). Skip it when the task is purely mechanical (extract dates).

### Add examples where behavior is non-obvious

Examples resolve ambiguity that is hard to state as rules. Classic case: a children's assistant that, asked about a holiday gift-bringer, explains the character is fictional. A single demonstration of answering a similar magical-character question warmly shifts the tone without writing a long policy.

Token economy: if two example formats perform equally, choose the shorter. Compact arrow-style pairs (`item -> label`) can cost noticeably fewer tokens than labeled Input/Output blocks; one comparison in the chapter shows roughly 27 versus 38 tokens for the same three-item task. Multiply the saving by request volume before dismissing it.

### Specify output format and use end markers

- Ask for brevity explicitly when you want it. Output tokens cost money and add latency.
- Forbid preambles if the model tends to restate the question before answering.
- For machine-consumed output, name the exact JSON keys and types, and give an example if the model drifts.
- For classification and other structured completions, end the prompt with a marker that signals where the answer begins (a trailing arrow, `Label:`). Without it, the model may treat the final item as part of the list and invent more items rather than labeling the last one. A base language model does not intrinsically distinguish your input from its own continuation.
- Choose markers that cannot occur inside the inputs. If inputs may contain arrows, use a different delimiter.

Format-related tools (Guidance, Outlines, Instructor) can enforce structure at decode time; see the tooling reference for when to adopt them.

## Providing sufficient context

Giving the model the material it needs improves answers and reduces hallucination, because without it the model falls back on memory that may be wrong or stale. Two routes:
1. Put the material directly in the prompt (the paper being asked about, the policy document).
2. Give the model tools to fetch it: retrieval (RAG), web search, database lookups. Collecting the right information per query is called context construction and is covered in depth in Chapter 6.

Decision rule: if a wrong answer is costly and the facts are knowable from a source you control, supply the source rather than trusting parametric knowledge.

## Restricting the model to its context

Needed for roleplay and simulations (a game character who should know nothing of the real world), closed-domain support bots and compliance-sensitive assistants. Options, in order of strength and cost:

| Approach | How | Strength | Cost / caveat |
|---|---|---|---|
| Prompting | Instruct "use only the supplied material"; show examples of questions to decline; require quoting the passage that supports each answer | Cheap, quick | No guarantee; models do not obey every instruction |
| Finetuning on your corpus | Adapt the model to the permitted domain | Stronger | Pretraining knowledge can still leak through |
| Training only on the permitted corpus | Build a model from the allowed data alone | Only real guarantee | Usually infeasible; corpus is often too small for a good model |

Practical default: prompting plus mandatory citations plus an output check that each claim maps to a quoted span. Escalate only if audits show leakage that matters.

## Decomposing complex tasks

Split a multi-step job into subtasks, each with its own prompt, and chain them. A customer support flow becomes: (1) classify the request's intent, (2) answer using a prompt specialized for that intent. With ten intents you maintain ten response prompts plus the router. The router can itself output JSON with primary and secondary categories, and an intent-specific prompt can hand off back to classification if the user changes topic.

Benefits beyond quality (models still handle simple instructions better):
- **Monitoring**: inspect intermediate outputs, not only the final one.
- **Debugging**: fix the failing step without perturbing the others.
- **Parallelization**: independent steps run concurrently. Writing the same story for three reading levels can be three simultaneous calls.
- **Authoring effort**: simple prompts are easier to write and review.

Costs:
- **Perceived latency**: if users only see the final step, time to first visible token grows with every hidden step.
- **More calls**: but not necessarily proportionally more spend, because billing is per token and each smaller prompt is shorter. Simple steps can also use a cheaper model; a common pattern is a small model for intent routing and a strong model for the reply.
- Even if total cost rises, improved reliability can justify it.

Granularity: there is no fixed rule. Should the router split primary and secondary category into two calls? Only if the measured quality gain beats the added latency and cost. Experiment.

Signal that it is time to decompose: the prompt keeps growing with edge cases and examples. GoDaddy reported a support prompt exceeding 1,500 tokens after a single round of iteration; splitting it into subtask prompts improved quality and lowered token cost.

## Giving the model time to think

**Chain-of-thought (CoT)**: ask the model to reason step by step before answering. Introduced by Wei et al. (2022), months before ChatGPT, and one of the first techniques shown to help across model families and sizes on math word-problem benchmarks. LinkedIn reported it also reduced hallucinations.

CoT variants, from least to most prescriptive:
1. Generic cue: reason step by step before answering.
2. Ask for the rationale before the verdict.
3. Prescribe the steps (determine A, determine B, compare).
4. One-shot or few-shot CoT: show a fully worked example on an analogous question, then pose the real one.

Which works best is application-dependent; test them. Prescribed steps give more control and predictability; open-ended reasoning adapts better to unfamiliar inputs.

**Self-critique (self-eval)**: ask the model to check its own output (Chapter 3 discusses it as an evaluation method). Like CoT, it encourages scrutiny.

Latency warning: both add tokens before the user sees an answer, and letting the model invent its own steps can produce long, expensive chains. For interactive products, consider prescribing a bounded number of steps, hiding reasoning behind a streaming final answer, or applying CoT only to the hard subset of requests.

## Iterating on prompts

Iteration loop:
1. Read real outputs. A model asked for the best option may decline because tastes differ; revise to require a pick anyway.
2. Learn the model's quirks (numbers, roleplay, instruction position) via its guide, others' reports, the playground, and running the same prompt on several models.
3. Change systematically: version prompts, log runs in an experiment tracker, keep eval data and metrics fixed.
4. Judge every change against the full pipeline. A tweak that improves one step can degrade the end-to-end result.

## Worked example: from monolith to chain

Situation (invented): a claims assistant has one 1,800-token prompt with 14 edge-case patches; quality is flat and cost rising.
1. Split into a small-model triage prompt returning `{"claim_type", "urgency"}` (labels enumerated, end marker added) and per-claim-type reply prompts on a strong model, each with only its own rules and two examples.
2. Re-run the frozen eval end to end, comparing quality, tokens per request and p95 time to first visible token.
3. Keep the split only if quality holds or improves within the latency budget.

## Pitfalls

- Unstated scales, uncertainty handling or format, then blaming the model for inconsistency.
- Treating "use only the context" instructions as a hard guarantee.
- Ignoring hidden-step latency from chains, CoT and self-critique.

## Glossary

- **Context construction**: gathering per-query information for the prompt (retrieval, search, tools).
- **Prompt decomposition / chaining**: one prompt per subtask, linked in sequence or run in parallel.
- **Few-shot CoT**: demonstrations that include the reasoning steps, not just answers.
- **Self-critique**: the model reviews and possibly revises its own output.
