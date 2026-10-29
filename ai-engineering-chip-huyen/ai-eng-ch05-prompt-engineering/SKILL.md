---
name: ai-eng-ch05-prompt-engineering
description: Prompt design, iteration, organization and defense for LLM applications, based on Chapter 5 of Chip Huyen's "AI Engineering". Use when writing or debugging production prompts, choosing zero- vs few-shot, splitting system and user prompts, fixing chat-template bugs, placing content in long contexts, enforcing output formats, decomposing tasks or adding chain-of-thought, evaluating prompt optimizers, versioning prompts in a catalog, or threat-modeling and defending against prompt extraction, jailbreaks, indirect injection and data extraction.
---

# Prompt Engineering (AI Engineering, Chapter 5)

## Purpose

Prompting steers a model without changing its weights, so it is the first adaptation to exhaust before finetuning. This skill treats it as engineering: explicit instructions, enough context, measured iteration on fixed evals, prompts stored and versioned like code, and layered defenses because instruction-following models also follow attackers. It routes to five references for depth and two scripts for catalog hygiene and safety measurement.

## Key decision rules

Apply these even without opening a reference.

**Before writing prompts**
- Check instruction following first; if the model cannot obey, wording will not save it.
- Gauge robustness by perturbing prompts trivially (digits vs words, whitespace, casing). High output variance means more prompt work or a stronger model.
- Prefer durable practices over model-specific hacks (magic labels, promised tips); hacks decay as models improve. Read the target model's own prompting guide for its quirks.

**Structure**
- Task description, examples, and the concrete task are the three parts. Developer rules go in the system prompt, user material in the user prompt, but test alternatives.
- System prompts help only through position and post-training (instruction hierarchy); the model sees one concatenated sequence.
- Use the model's chat template exactly; templates change between versions of the same family, and errors (even one extra newline) fail silently. Print the rendered prompt.
- Test instruction placement per model (GPT-4 era preferred start, Llama 3 seemed to prefer end). Keep critical facts at the start or end of long inputs; mid-context recall is weakest.
- Probe long-context use with NIAH on private, production-like data, or RULER; if quality falls with length, shorten or retrieve less but better.

**Content**
- Remove ambiguity: scale, integer vs fractional, behavior when unsure, out-of-scope handling.
- Use a persona when the correct answer depends on audience or expertise.
- Few-shot adds little for strong models on common tasks but still matters for niche domains and tone. Sweep shot counts; choose compact example formats.
- For structured outputs, state exact keys, forbid preambles if needed, and end with a marker that cannot occur in inputs.
- Supply context (or retrieval tools) whenever a wrong answer is costly. "Use only the context" instructions plus citations are cheap but not guaranteed; finetuning is stronger; only training on the permitted corpus is strict.

**Complexity and reasoning**
- Decompose when a prompt keeps growing (one team passed 1,500 tokens and improved both quality and cost by splitting). Gains: monitoring, debugging, parallelism, cheaper models for easy steps. Costs: more calls and longer time to first visible token.
- Add CoT (generic cue, rationale-first, prescribed steps, or worked example) or self-critique for reasoning-heavy tasks; bound open-ended reasoning for latency.

**Process**
- Version prompts, track experiments, freeze eval data and metrics, and evaluate end to end, since a subtask gain can hurt the system.
- Hand-write prompts before adopting optimizers (DSPy, Promptbreeder, TextGrad). Estimate hidden calls as variants x examples x calls per evaluation; always read the prompts tools send.
- Keep prompts out of code with metadata (model, endpoint, app, creator, date, sampling params, input and output schemas). Use a catalog with per-prompt versions when apps share prompts so each can pin.

**Security**
- Write system prompts assuming they will leak; extracted prompts are often hallucinated, and secrecy is a liability, not a moat.
- Treat all tool, web, email, document and database text as untrusted data. Indirect injection is the most dangerous family.
- Layer defenses: model (instruction hierarchy, borderline-aware safety), prompt (explicit prohibitions, restate task after untrusted content, audit library defaults), system (sandbox code, human approval for destructive actions, input and output guardrails, intent and usage-pattern monitoring).
- Measure violation rate and false refusal rate together. Residual risk never reaches zero if the system can act.

## Default workflow

1. Confirm the model follows instructions and check its prompting guide.
2. Draft: role, unambiguous task, output format, end marker, needed context; add examples only where they resolve ambiguity.
3. Render with the exact chat template and inspect the final prompt.
4. Evaluate on a frozen dataset with fixed metrics; sweep shot count and instruction position.
5. Iterate on observed failures; decompose if the prompt bloats; add CoT where reasoning fails.
6. Store the prompt with metadata in the catalog; lint it; pin versions per application.
7. Threat-model tools and data flows; apply layered defenses; measure violation and false refusal rates before release and per release.

## References

- [references/prompt-anatomy-and-context.md](references/prompt-anatomy-and-context.md): read when choosing zero vs few-shot, splitting system and user prompts, debugging chat templates, or designing long-context and NIAH tests.
- [references/writing-effective-prompts.md](references/writing-effective-prompts.md): read when drafting or revising a prompt, enforcing output formats, restricting a model to its context, decomposing a task, or adding CoT or self-critique.
- [references/prompt-tooling-and-versioning.md](references/prompt-tooling-and-versioning.md): read when evaluating prompt optimizers or structured-output libraries, budgeting their API calls, or designing prompt storage, metadata and a versioned catalog.
- [references/prompt-attacks.md](references/prompt-attacks.md): read when threat-modeling an LLM feature, assessing prompt extraction, jailbreak, indirect injection, training-data extraction or copyright risk.
- [references/prompt-defenses.md](references/prompt-defenses.md): read when choosing and layering defenses, planning red teaming, or setting up violation and false refusal measurement.
- [references/source-map.md](references/source-map.md): read to find which reference covers a given chapter section.

## Scripts

Python 3 standard library only; each supports `--help`.

- Run `python3 scripts/prompt_catalog_lint.py catalog.json` to check a JSON prompt catalog for required metadata (model, version, creator, date, sampling params, input and output schemas), template placeholders that do not match the input schema, duplicate versions, and application pins that are missing or behind the latest version. Add `--strict` to fail on warnings. Exit code 1 on errors.
- Run `python3 scripts/safety_metrics.py results.jsonl --by-group` to compute violation rate and false refusal rate from labeled red-team results (one JSON object per line with `kind` attack or benign, `outcome` complied or refused, optional `group`).
