---
name: fse-ch15-ai-powered-software-engineer
description: Guidance for using AI as a developer's pair programmer without giving up engineering judgment, based on Chapter 15 of Schutta and Vega's "Fundamentals of Software Engineering". Covers AI/ML/GenAI/LLM basics, what AI does well and badly, choosing between chatbots, inline IDE assistants and agentic IDEs, prompt engineering, reviewing AI-generated code, avoiding vibe coding, and career positioning. Use when a developer asks how to use AI coding tools, writes or improves a prompt, reviews AI-written code, sets team AI usage rules, or worries AI will replace them.
---

# The AI-Powered Software Engineer

Purpose: help a developer treat AI as a force multiplier on top of solid fundamentals. The chapter's core position is that AI changes how engineers spend their time, not whether engineering judgment is needed. The engineer stays accountable for every line, whoever or whatever typed it, and the hours saved on generation must be partly reinvested in validation. Value moves away from producing code and toward understanding requirements, making trade-offs, reviewing, and solving business problems.

## Key decision rules

Apply these even without opening the references.

1. **Ownership is non-transferable.** "The AI wrote it" is never an excuse. Before a PR is opened, the author must be able to explain why each generated line exists and what it does.
2. **AI output is a first draft.** Run it through the same tests, reviews and integration planning as human code. Budget review time out of the time generation saved.
3. **Match stakes to rigor.** Prompt-and-accept is tolerable only for throwaway personal projects where a bug costs little. Anything with users, money, legal or compliance exposure needs requirements, tests, review and a pipeline.
4. **Pick the tool by task shape.**
   - Chatbot: understanding concepts, debugging hard problems, architecture discussion, learning a stack.
   - Inline assistant: boilerplate, standard patterns, tests for existing code, comments, quick API or syntax lookups.
   - Agentic IDE: multi-file refactors, features touching several places, migrations, work needing whole-project context.
5. **Agentic work needs a frame.** Give specific requirements plus nonfunctional ones (style, security, testing approach) up front. Slice big tasks small. Keep every AI change in version control. Review before committing. Expect and check an analyze, plan, implement sequence.
6. **Do not let suggestions override architecture.** The human owns design decisions. Start AI use on simple repetitive work and widen scope as trust is earned.
7. **Know the model's blind spots.** Assume no fresh knowledge (training cutoff), possible hallucination, no knowledge of the codebase or business rules, weaker results in niche or new tech and low-level code, inherited bias, and no ability to weigh business trade-offs. Distinguish model limits from product features (for example, web search tools) that compensate.
8. **Protect secrets and IP.** Never paste API keys, credentials, proprietary logic, sensitive schemas or customer data into tools whose retention and training policy is unknown or unapproved.
9. **Prompt quality drives output quality.** A good prompt states context (greenfield or legacy, hobby or mission critical), environment (language version, frameworks, constraints), the exact target, edge cases, desired output structure and length, and optionally a role and examples.
10. **Escalate prompting technique with task complexity.** Zero-shot first, then one-shot or few-shot to pin a style or label set, delimited sections (task, requirements, constraints) for multipart requests, and phased decomposition for large problems. Ask for reasoning steps rather than bare commands.
11. **Low temperature for code and facts.** Roughly 0.0 to 0.5 for code generation and factual work. Higher values (about 0.7 to 1.0) add creativity and hallucination risk.
12. **Understand before accepting.** If the developer cannot explain a suggestion, they research it until they can. The aim is faster learning, not skipped learning.
13. **Measure impact, not lines.** Lines of code is a poor productivity signal. Frame outcomes as business impact (cost, latency, reliability, users served).

## Default workflow

1. Classify the task: stakes (throwaway vs production), shape (single snippet, routine pattern, multi-file change, learning) and data sensitivity.
2. Choose the tool category (rule 4) and confirm the data can be shared (rule 8).
3. Draft the prompt with the checklist in rule 9. Decompose anything large into phases.
4. Generate. For agentic tools, review the plan before letting implementation proceed.
5. Validate: read every line, run and extend tests, check edge cases, security, conventions, bias and accessibility, and fit with the architecture.
6. Iterate on the prompt rather than hand-patching repeatedly. If stuck, ask the AI to suggest a better prompt.
7. Submit for normal code review, ready to defend every line. Save prompts that worked in a personal library.
8. Spend the reclaimed time on design questions: API usability, throughput, concurrency, graceful failure under load.

## References

- [references/ai-concepts-capabilities-limits.md](references/ai-concepts-capabilities-limits.md): read when explaining AI, ML, deep learning, GenAI or LLM concepts, picking a temperature, or deciding whether a task suits AI given its strengths and its known limitations.
- [references/ai-coding-assistants-and-usage-policy.md](references/ai-coding-assistants-and-usage-policy.md): read when choosing between chatbot, inline and agentic tools, setting up an agentic task, or writing personal or team AI usage guidelines.
- [references/prompt-engineering-playbook.md](references/prompt-engineering-playbook.md): read when writing, critiquing or rewriting a prompt, or choosing zero/one/few-shot, delimited structure or task decomposition.
- [references/reviewing-ai-code-and-career-shift.md](references/reviewing-ai-code-and-career-shift.md): read when reviewing AI-generated code, judging whether vibe coding is acceptable, addressing job-loss worries, reframing productivity, or planning practice exercises.
- [references/source-map.md](references/source-map.md): read to find which reference covers a given chapter section.

## Scripts

None. The chapter's guidance is judgment-based and does not support a meaningful calculation or deterministic checker.
