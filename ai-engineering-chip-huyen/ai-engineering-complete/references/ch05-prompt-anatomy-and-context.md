# Prompt Anatomy, In-Context Learning, Templates and Context Length

## Contents
- Why prompting deserves engineering rigor
- Anatomy of a prompt
- Two preconditions: instruction following and perturbation robustness
- In-context learning, shots and how many to use
- Terminology: prompt versus context
- System prompt versus user prompt
- Chat templates versus prompt templates
- Context length and where information sits
- Testing long-context use (NIAH, RULER)
- Glossary

## Why prompting deserves engineering rigor

Prompting is the cheapest adaptation (no weight changes), so push it as far as it goes before finetuning. Two warnings: easy to start is not easy to do well, so run prompt changes as ML experiments (fixed eval data and metrics, tracked results); and prompting alone does not make a production system, which also needs experiment tracking, evaluation and dataset curation. The danger is a team whose only skill is prompt writing.

## Anatomy of a prompt

A prompt can carry any subset of three parts:

| Part | What it holds | Typical home |
|---|---|---|
| Task description | Goal, role/persona, output format, constraints | System prompt |
| Demonstrations | Worked input/output pairs showing the task | System prompt or early user turn |
| The task instance | The concrete question, document or record to act on | User prompt |

When reviewing a prompt, label each span with one of these three. Spans that fit none are usually noise or leftover patches.

## Two preconditions

**Instruction following.** If the model cannot reliably obey instructions, no wording fixes it. Run a small instruction-following check (Chapter 4 covers how) before investing in prompt polish. Swapping in a more capable model is often cheaper than weeks of wording experiments.

**Robustness to perturbation.** The amount of fiddling a prompt needs scales with how much the output swings under meaningless edits: a digit versus the spelled-out number, an extra line break, different capitalization. To measure it, run 20 to 50 representative inputs through several trivially perturbed prompt variants (casing, whitespace, synonyms, number formats, bullet order) and measure output disagreement or metric variance. High variance means more prompt work ahead, or a stronger model.

Robustness tracks general capability closely, so stronger models usually need less tinkering. (HELM Lite stopped reporting robustness in late 2023, so do not expect leaderboards to answer this for you.)

## In-context learning

In-context learning (ICL) means the model picks up a behavior from what is in the prompt, with no weight update. Brown et al. (2020), introducing GPT-3, showed a next-token predictor handling translation, reading comprehension, arithmetic and exam questions from examples alone.

Practical consequences:
- **Continual learning without retraining.** A model trained before a library's new release can still answer questions about it if you put the changelog or new docs in context. This is the main argument for retrieval over retraining when facts change often.
- **Latent-program view.** François Chollet's framing: the model holds many latent programs (one for haiku, one for limericks) and the prompt selects one. Prompt engineering is search for the trigger that activates the right program. Useful when explaining why small wording changes can switch behavior entirely.

**Shots.** Each demonstration is a shot; zero examples is zero-shot, five is 5-shot.

How many shots:
- More examples generally help, but cost grows linearly in tokens and the count is capped by context length.
- For GPT-3, few-shot beat zero-shot by a wide margin. A 2023 Microsoft analysis found only small gains over zero-shot for GPT-4 and similar models on its use cases. The interpretation: better instruction followers need fewer demonstrations.
- That analysis probably undersells examples for niche domains. If the model saw little of a technology during training (the chapter's case is the Ibis dataframe API), examples can still change results a lot.
- Decide empirically: sweep 0, 1, 3, 5, 10 shots on your eval set and pick the point where quality stops improving relative to added tokens.

Worked example: an internal ticket classifier using a frontier model hits 91% at zero-shot, 92% at 3-shot and 92% at 8-shot, with 8-shot adding 600 tokens per call. Keep zero-shot or 3-shot. A code generator targeting an in-house DSL goes from 40% at zero-shot to 78% at 5-shot; there the tokens are clearly worth it.

## Terminology: prompt versus context

Usage varies: GPT-3's authors used "context" for the whole input, some practitioners mean the supporting information inside the prompt, and Google's PaLM 2 docs used it for what is really the task description. This skill follows the book: **prompt** is the whole input, **context** is the information supplied so the model can do the task. Confirm which meaning a user intends.

## System prompt versus user prompt

Convention: developer instructions (role, rules, format) go in the system prompt; the end user's request and any uploaded material go in the user prompt. This is a convention, not a law. You may move content between the two and should test alternatives.

**Why a system prompt might help.** Both prompts are concatenated into one token sequence before the model sees them, so the model has no structural separation. Any advantage comes from one or both of:
1. Position: the system prompt is first, and models tend to process early instructions well.
2. Post-training: the model may have been trained to weight system instructions above user ones, as in OpenAI's instruction hierarchy work (Wallace et al., 2024). The same training is a defense against prompt attacks.

Providers report that persona instructions placed in the system prompt are held more consistently across long conversations.

## Chat templates versus prompt templates

| | Chat template | Prompt template |
|---|---|---|
| Defined by | Model developer | Your application |
| Contains | Special tokens, role headers, turn separators | Your instructions with placeholders filled from data ("hydration") |
| Changes when | Model family or version changes | You edit it |
| Failure mode | Silent quality drop | Wrong or missing data in the prompt |

Key facts:
- Templates can change completely between versions of one family (Llama 2's bracketed markers gave way to Llama 3's header and end-of-turn tokens). Special-delimited strings are single tokens.
- Template errors fail silently: answers stay plausible, just worse. One extra newline can shift behavior; rarely a deviation helps, but expect degradation.
- Third-party libraries often lag. The author lost a day debugging a finetuning problem caused by a library that had not updated the template for a newer model version.

Template checklist:
- [ ] Inputs follow the target model's template exactly (tokens, newlines, role names).
- [ ] Any library that builds prompts uses the template for this exact model version.
- [ ] The fully rendered prompt is printed and inspected before the first real run and after every upgrade.

## Context length and where information sits

Context windows grew about 2,000x in five years, from GPT-2's 1K tokens to Gemini 1.5 Pro's 2M. Rough sizing: 100K tokens holds a moderate book (the AI Engineering book is about 160K tokens); 2M holds roughly 2,000 Wikipedia pages or a PyTorch-sized codebase.

A larger window does not mean uniform use. Liu et al. (2023) found models retrieve information placed near the start and end of a prompt much better than information in the middle. Rules that follow:
- Put the instruction and the most decision-critical material at the edges.
- Do not assume dumping everything into a long window beats selecting less.
- Instruction position is model-specific: GPT-4 era models generally preferred the task description first; Llama 3 appeared to prefer it last. Test both.

## Testing long-context use

**Needle in a haystack (NIAH).** Insert a fact at various positions in a long input and ask for it. Plot accuracy against position and total length.

Make it production-relevant:
1. Use a realistic haystack (for example, a long clinical visit transcript) and realistic needles (a medication name, a lab value mentioned once).
2. Use private facts the model could not have memorized, or it may answer from training data and inflate the score.
3. Vary both position (start, quartiles, end) and total length.
4. If accuracy falls as length grows, shorten prompts, retrieve fewer but better chunks, or move key material to the edges.

**RULER** (Hsieh et al., 2024) is a broader synthetic benchmark of long-context ability; use it when you need comparisons across models rather than a probe of your own data.

## Glossary

- **Hydration**: filling a prompt template's placeholders with request-specific data.
- **Chat template**: the model-specific serialization of roles and turns into tokens.
- **Lost in the middle**: weaker recall for information placed mid-prompt.
- **NIAH**: a planted-fact retrieval test across positions and lengths.
- **Prompt perturbation**: a meaning-preserving edit used to test output stability.
