---
name: ai-eng-ch05-prompt-engineering
description: Use when designing, debugging, structuring, versioning or securing LLM prompts: system vs user prompts, chat templates, zero/few-shot, context placement, output formats, decomposition, chain-of-thought, prompt tools, prompt catalogs, and defenses against prompt extraction, jailbreaks, indirect injection and data extraction. Based on Chapter 5 of Chip Huyen's "AI Engineering".
---

# Chapter 5: Prompt Engineering (AI Engineering, Chip Huyen)

## When to use this skill

Apply this skill when an engineer is:
- Writing or rewriting a prompt for a production LLM feature, or asking why a prompt behaves inconsistently.
- Choosing between zero-shot and few-shot, deciding how many examples to include, or where to put instructions in a long context.
- Splitting system and user content, wiring a chat template for an open-weight model, or debugging silent quality drops after a model or library upgrade.
- Getting structured output (JSON, labels) reliably, or reducing cost/latency of prompts.
- Deciding whether to split a big prompt into a chain, or whether to add chain-of-thought or self-critique.
- Evaluating automated prompt optimizers or prompt-building libraries.
- Organizing prompts in a codebase, adding metadata, or setting up a prompt catalog with versions.
- Threat-modeling an LLM app (especially one with tools, RAG, email/web access, code execution or DB writes) and choosing defenses.
- Measuring safety with violation rate and false refusal rate.

Do not treat prompting as the whole job. The chapter's framing: prompting is the cheapest, first adaptation technique (no weight changes) and should be exhausted before finetuning, but production work also needs experiment tracking, evaluation and dataset curation done with ML rigor.

## Core mental models

**Prompt anatomy.** A prompt typically carries up to three things: a task description (what to do, the role to play, the output format), demonstrations of the task, and the concrete input to act on. The book uses "prompt" for the entire model input and "context" for the information supplied so the model can do the task. Other sources use the words differently; clarify terms with the user when it matters.

**Instruction following is a prerequisite.** If a model cannot follow instructions, prompt craft cannot rescue it. Check instruction-following ability (an evaluation concern from Chapter 4) before investing in prompt polish.

**Robustness to perturbation determines how much fiddling you need.** If trivial edits (a numeral vs. a spelled-out number, a newline, casing) swing outputs, the model is fragile and needs more prompt work. Robustness tends to rise with general capability, so a stronger model often saves engineering time. Measure robustness by randomly perturbing prompts and observing output variance.

**In-context learning (ICL).** Models can pick up a behavior from examples or information in the prompt with no weight update (introduced with GPT-3, Brown et al., 2020). Each example is a "shot". ICL also acts as continual learning: you can feed post-cutoff facts (e.g., new API docs) without retraining. One useful framing (attributed to François Chollet): a foundation model is a library of latent programs and a prompt selects which one runs.

**Few-shot value shrinks as models improve, except off-distribution.** Few-shot gave big gains for GPT-3, but for stronger models general-task gains over zero-shot were small in a 2023 Microsoft analysis. Examples still matter a lot for niche domains the model rarely saw (an uncommon library or DSL). More shots cost more tokens and are bounded by context length.

**System prompt vs. user prompt.** Developer instructions usually go in the system prompt, end-user input in the user prompt. Internally both are concatenated into one sequence via the model's chat template. Any advantage of the system prompt likely comes from (a) appearing first and (b) post-training that teaches the model to prioritize it (the instruction hierarchy work, Wallace et al., 2024), which also helps against attacks.

**Chat template vs. prompt template.** A chat template is defined by the model developer (special tokens, role headers) and can change between versions of the same family (e.g., Llama 2 vs. Llama 3 formats differ completely). A prompt template is your application's own string with placeholders that you hydrate with data. Template mistakes fail silently: the model still produces plausible output, just worse.

**Context length and position effects.** Context windows grew roughly 2,000x in five years (about 1K tokens for GPT-2 to 2M for Gemini 1.5 Pro). Bigger windows do not mean uniform attention: models retrieve information at the start and end of a prompt better than in the middle ("lost in the middle", Liu et al., 2023). Needle in a haystack (NIAH) and RULER test this.

**Prompt attacks exist because instruction following works.** The better a model obeys instructions, the better it obeys malicious ones, and it struggles to tell trusted from untrusted instructions once everything is one token stream. Security is a moving cat-and-mouse game; risk is never zero if the system can take impactful actions.

**Proprietary prompts are a liability more than a moat.** They leak, they need maintenance on every model change, and extracted "system prompts" are often hallucinated anyway. Write system prompts assuming they will become public.

## Decision frameworks

**Zero-shot vs. few-shot**

| Situation | Lean toward |
|---|---|
| Strong frontier model, common task, clear instructions | Zero-shot first; add shots only if eval shows gains |
| Niche domain, rare library/format, idiosyncratic style or tone | Few-shot (examples carry information the model lacks) |
| Model ignores a policy (e.g., keeps "breaking character") | Add an example demonstrating the desired handling |
| Tight token budget | Fewer shots, compact example formats (e.g., `input -> label` lines instead of verbose labeled blocks) |
| Unknown | Sweep the number of shots against an eval set; pick the knee of the cost/quality curve |

**Where to place instructions.** Most models (GPT-4 era) did better with the task description at the start; some (Llama 3 was cited) did better with it at the end. Do not assume: test both positions per model. Put critical facts near the start or end of long inputs, not buried mid-context.

**Should I decompose the prompt into a chain?**
- Yes if: the prompt has bloated with edge cases and examples (one reported case grew past 1,500 tokens and improved, with lower token cost, after being split), steps are separable (classify then respond), you need per-step monitoring/debugging, some steps can run in parallel, or some steps can use a cheaper model (e.g., small model for intent routing, strong model for the reply).
- Be cautious if: users wait on hidden intermediate steps (time to first visible token rises), or call count multiplies cost. Note that two small prompts often cost less than double one large prompt because billing is per token.
- How granular: there is no rule; decide by measured quality vs. cost vs. latency.

**Should I add chain-of-thought or self-critique?**
- Use for reasoning, math, multi-step judgment, or where hallucination is a concern (CoT has been reported to reduce it).
- Variants, from cheapest to most controlled: a generic "reason before answering" cue; asking for a rationale; prescribing the explicit steps; giving one or more worked examples (few-shot CoT).
- Watch latency and cost, especially when the model invents its own open-ended steps.

**Restricting the model to provided context only** (roleplay characters, closed-domain assistants):
1. Prompt level: explicit "use only the supplied material" instruction, examples of questions it must decline, and requiring citations/quotes from the source. Cheap, not guaranteed.
2. Finetuning on your corpus: stronger, but pretraining knowledge can still leak.
3. Training only on the permitted corpus: the only strict guarantee, usually impractical and data-starved.

**Using a prompt-optimization tool?**
- Start by hand-writing prompts to learn the model and your requirements (keep it simple).
- Adopt a tool (DSPy, OpenPrompt, Promptbreeder-style evolution, TextGrad, or LLM-written/critiqued prompts; structured-output helpers like Guidance, Outlines, Instructor) when you have a defined input/output format, a metric and an eval set, since these tools optimize against exactly those.
- Budget the hidden calls: variants x eval examples x calls per evaluation (generate, validate, score). Ten variants on 30 examples is already 300+ calls.
- Always read the prompts the tool actually sends; tools ship typos, wrong templates, token-level concatenation bugs, and can change defaults silently.

**Versioning strategy**

| Approach | Good for | Weakness |
|---|---|---|
| Prompts in separate files in the app repo, versioned with git | Single app, small team | Shared prompts force every consumer to upgrade at once |
| Dedicated prompt catalog with explicit per-prompt versions | Many apps sharing prompts | More infrastructure, but apps can pin versions, search by metadata, and get notified of new versions |

**Defense layering.** Pick defenses at three levels and combine them:

| Level | Mechanisms | Limits |
|---|---|---|
| Model | Models trained on an instruction hierarchy (system > user > model output > tool output); safety tuning that handles borderline requests helpfully | Only if you train or choose the model |
| Prompt | Explicit prohibitions, restating the core instruction after untrusted content, naming expected attack styles, auditing library default templates | No compliance guarantee; duplication adds tokens |
| System | Sandboxed code execution, human approval for side-effecting actions, out-of-scope topic filters, intent classifiers over whole conversations, anomaly detection, input and output guardrails (PII, toxicity), usage-pattern monitoring | Engineering cost; keyword filters are crude |

## Step-by-step playbooks

**Playbook A: Write a first production prompt**
1. Confirm the model follows instructions well enough (quick eval) and check its prompting guide for quirks.
2. State the task unambiguously: scale and range for scores, whether fractional values are allowed, what to do when uncertain (best guess vs. an explicit "unknown").
3. Assign a persona when perspective changes the right answer (e.g., grading a child's essay as a primary-school teacher vs. as a generic critic).
4. Supply sufficient context (documents, retrieved passages, tool access) so the model does not fall back on unreliable memory.
5. Specify output format: concise vs. detailed, no preamble, exact JSON keys or schema, with an example if needed. For classification or structured completions, end the input with a clear marker (e.g., a trailing arrow or `Label:`) that will not appear inside inputs, so the model emits the answer rather than continuing the list.
6. Add examples only where they reduce ambiguity; prefer token-cheap formats.
7. Assemble with the exact chat template; print the final rendered prompt and inspect it.
8. Evaluate on a fixed dataset with fixed metrics.

**Playbook B: Iterate systematically**
1. Version every prompt and log experiments in a tracker.
2. Hold evaluation data and metrics constant across variants.
3. Read failures, patch the prompt for the observed behavior (e.g., model refuses to pick a favorite, so explicitly require a choice), rerun.
4. Try the same prompt on other models to learn your model's quirks.
5. Evaluate end to end: a change that helps one subtask can hurt the whole pipeline.

**Playbook C: Probe long-context reliability**
1. Build a haystack resembling production inputs (e.g., a long transcript).
2. Plant needles at varied positions; use private facts the model could not know from training, otherwise it may answer from memory.
3. Ask for the needles; plot accuracy vs. position and length (or run RULER).
4. If accuracy degrades, shorten prompts, retrieve less but better, or move key material to the edges.

**Playbook D: Diagnose a silent quality drop**
1. Diff the rendered final prompt before and after (library upgrade, model version change).
2. Verify the chat template matches the current model version exactly (special tokens, newlines, role headers).
3. Check third-party tools' default prompts for changes or typos.
4. Re-run the frozen eval set.

**Playbook E: Secure an LLM application**
1. Enumerate attack surfaces: prompt extraction, jailbreak/direct injection, indirect injection via tools (web pages, repos, emails, documents, DB rows), and information extraction (training data or context, including PII and copyrighted text).
2. Map impacts: remote code/tool execution, data leaks, social harm, misinformation, service subversion (wrong approvals, denial), brand damage.
3. Red-team: use benchmarks (AdvBench, PromptRobust) and scanners (PyRIT, garak, llm-security, persuasive jailbreaker) plus a human red team.
4. Apply layered defenses (table above). Treat all tool output and retrieved text as untrusted data, never as commands.
5. Gate destructive actions (DB writes such as DELETE/DROP/UPDATE, sending email, running code) behind human approval or sandboxing.
6. Add input and output guardrails, PII filters, and rate/pattern monitoring for users sending many near-duplicate probing requests.
7. Track violation rate and false refusal rate together; tune toward low values on both.

## Checklists

**Prompt quality**
- [ ] Task, role, and output format are explicit and unambiguous
- [ ] Edge-case behavior defined (uncertainty, out-of-scope, refusal)
- [ ] Necessary context supplied or retrievable
- [ ] Examples are representative and token-efficient
- [ ] End-of-input marker for structured outputs; delimiter cannot collide with input text
- [ ] Instruction position tested for this model
- [ ] Key facts not buried in the middle of long contexts
- [ ] Rendered prompt printed and template-verified

**Engineering hygiene**
- [ ] Prompts stored separately from code (reuse, independent testing, readability, domain experts can edit)
- [ ] Metadata per prompt: model, application, creator, creation date, endpoint, sampling params (temperature, top-p), input schema, output schema
- [ ] Versioning lets each consumer pin a version
- [ ] Experiment tracking and standardized evals in place
- [ ] Tool-generated prompts and API call counts reviewed

**Security**
- [ ] System prompt contains nothing you would mind seeing published
- [ ] No secrets or other users' data in context unless required
- [ ] Tool and retrieval output treated as lowest-priority, untrusted
- [ ] Generated code runs in an isolated VM/sandbox
- [ ] Human approval for impactful actions
- [ ] Input and output guardrails, PII detection
- [ ] Violation rate and false refusal rate measured on an attack set
- [ ] Borderline requests get safe, helpful answers rather than blanket refusals

## Pitfalls and anti-patterns

- Assuming prompting is trivial, or that it is the only skill needed for production AI.
- Relying on outdated hacks (magic tokens, promised tips) instead of durable practices; they decay as models improve.
- Wrong or slightly malformed chat template (even one extra newline) causing unexplained degradation; trusting a library to have updated the template for a new model version.
- Measuring a prompt change only on its own subtask, not on the full system.
- Endless ad hoc tweaking without versioning, fixed evals, or tracking.
- One monolithic prompt that keeps growing with patches.
- Ignoring the latency hit of chains, CoT and self-critique on user-visible time to first token.
- Letting prompt optimizers run unbounded, burning API budget on hidden calls and long chains.
- Using library default templates without reading them (some were found permissive enough that injection attacks succeeded every time until restrictions were added).
- Keeping prompts in git with shared ownership, forcing all apps onto the newest version.
- Treating the system prompt as a secret security boundary.
- Believing a "leaked" system prompt is authentic; extracted prompts are often hallucinated.
- Defending only with keyword blocklists; obfuscation (misspellings, mixed languages, Unicode, odd character runs), output-format tricks (poems, code, songs), and roleplay personas bypass them. Automated attackers (e.g., substitution search by Zou et al., 2023, or PAIR, which often succeeds in under twenty queries) find bypasses quickly.
- Trusting content the model reads: passive phishing (poisoned public pages or repos found via search) and active injection (malicious emails to an assistant, malicious strings stored in DB fields that a text-to-SQL step may act on). Natural language is far harder to sanitize than SQL.
- Optimizing only for violation rate; a system that refuses everything scores zero violations and is useless.
- Ignoring information extraction: memorized training data can be pulled via fill-in-the-blank probing or divergence attacks (asking the model to repeat a word indefinitely); larger models memorize more (estimated around 1% in one study); diffusion models also regurgitate near-duplicate images. Copyright risk includes non-verbatim paraphrase, which is very hard to detect automatically.

## Key terms

- **Prompt engineering**: crafting instructions to steer a model without changing weights.
- **In-context learning**: learning a behavior from the prompt at inference time.
- **Shot / zero-shot / few-shot**: number of demonstrations in the prompt.
- **System prompt / user prompt**: developer-level vs. end-user-level instructions, concatenated by the chat template.
- **Chat template**: model-specific token format for roles; distinct from your app's prompt template.
- **Context construction**: gathering the information a query needs (retrieval, web search; see Chapter 6).
- **NIAH / RULER**: tests of how well a model uses information at different positions and lengths.
- **Prompt decomposition / chaining**: splitting a task into sequential or parallel subprompts.
- **Chain-of-thought (CoT)**: prompting for intermediate reasoning (Wei et al., 2022).
- **Self-critique (self-eval)**: having the model check its own output.
- **Prompt catalog**: versioned, searchable store of prompts with metadata and dependency tracking.
- **Prompt extraction / reverse prompt engineering**: recovering an app's hidden prompt or context.
- **Jailbreaking**: subverting safety behavior; **prompt injection**: smuggling malicious instructions into input (the book uses "jailbreaking" for both).
- **Indirect prompt injection**: instructions planted in tool-accessible sources.
- **PAIR**: attacker LLM iteratively refining jailbreak prompts against a target.
- **Factual probing / LAMA**: fill-in-the-blank probing of relational knowledge, reusable for data extraction.
- **Divergence (repeated token) attack**: repetition prompts that make a model emit memorized data.
- **Instruction hierarchy**: priority order system > user > model outputs > tool outputs (reported up to 63% robustness gain with minimal capability loss).
- **Violation rate / false refusal rate**: share of successful attacks / share of safely answerable requests refused.
- **Borderline request**: a query with both safe and unsafe readings; ideal response is helpful and safe.

## Source map

Chapter 5, "Prompt Engineering":
- Introduction to Prompting
  - In-Context Learning: Zero-Shot and Few-Shot (sidebar: Terminology Ambiguity: Prompt Versus Context)
  - System Prompt and User Prompt
  - Context Length and Context Efficiency
- Prompt Engineering Best Practices
  - Write Clear and Explicit Instructions (explain without ambiguity; adopt a persona; provide examples; specify the output format)
  - Provide Sufficient Context (sidebar: How to Restrict a Model's Knowledge to Only Its Context)
  - Break Complex Tasks into Simpler Subtasks
  - Give the Model Time to Think
  - Iterate on Your Prompts
  - Evaluate Prompt Engineering Tools
  - Organize and Version Prompts
- Defensive Prompt Engineering
  - Proprietary Prompts and Reverse Prompt Engineering
  - Jailbreaking and Prompt Injection (direct manual prompt hacking; automated attacks; indirect prompt injection)
  - Information Extraction
  - Defenses Against Prompt Attacks (model-level, prompt-level, system-level defense)
- Summary
