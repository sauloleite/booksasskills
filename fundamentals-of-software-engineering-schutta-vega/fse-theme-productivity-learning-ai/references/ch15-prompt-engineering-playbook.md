## Contents
- What prompt engineering is (and is not)
- The delegation analogy
- Core techniques
- Quick-win checklist
- Advanced: structuring techniques
- Advanced: organizational techniques
- Prompt rewrite examples
- Building a prompt library
- Pitfalls

# Prompt Engineering Playbook

## What prompt engineering is (and is not)

It is simply communicating well with an AI, a general skill comparable to learning to search the web effectively, not a specialist discipline. Many developers blame the tools when the real gap is how they phrase their needs. The same habits that produce good tickets, good requirements for teammates and good documentation produce good prompts. Treat the exchange like a conversation with a coworker.

Central rule: output quality tracks prompt quality.

## The delegation analogy

Ask a new colleague to "fix the login bug" and they may waste hours: which of several login forms, which ticket, what is the symptom? Tell them which form, what validation is failing and what downstream damage it causes, and they can go straight to the fix. Write prompts the second way.

## Core techniques

### 1. Be specific
Name the data structure, element type, criterion, ordering, language version and edge cases. If the model must guess any of those, it will guess something.

### 2. Shape the output
State depth, audience, sections, length per section and whether to include code. An unstructured "explain X" can come back as one sentence or a thesis. A numbered outline with length limits per part and a concrete example request gets predictable results.

### 3. Teach rather than command (chain-of-thought)
Guide the model through the reasoning you would use, as a good mentor would with a junior. Instead of "optimize this", define what optimize means (speed on large inputs, memory, readability), then ask it to (a) analyze the current complexity, (b) propose specific changes, (c) present revised code with comments explaining the gain.

## Quick-win checklist

Run through this before sending any nontrivial prompt:

- [ ] Context: greenfield or legacy (and constraints that blocks modern practices)? Hobby or mission critical?
- [ ] Environment: language and version, frameworks, libraries allowed or banned, runtime limits.
- [ ] Example: show what good output looks like if format or style matters.
- [ ] Role: give a persona (for example, security reviewer or performance specialist) to set perspective and depth.
- [ ] Output format: sections, length, code or prose, file layout.
- [ ] Edge cases: nulls, empty input, large input, failure modes.
- [ ] Iteration plan: expect a second round; use the first answer to sharpen the prompt.
- [ ] Meta-prompt fallback: if results keep missing, tell the AI what you wanted and what was wrong, and ask how to rephrase.
- [ ] Save it: if it worked, store it for reuse.

## Advanced: structuring techniques

| Technique | What you provide | Use when |
|---|---|---|
| Zero-shot | instruction only | task is common and unambiguous; often enough |
| One-shot | one example of desired style plus the new request | you want a sibling that matches an existing function's conventions |
| Few-shot | several input to output pairs, then a new input | classification, labeling, formatting with consistent rules |

Few-shot is effectively classification by example: you show labeled cases so the model infers the decision boundary. Choose examples that cover each label and at least one tricky or mixed case, otherwise the model will be unsure how to handle ambiguity.

Example few-shot skeleton (original):

```
Label each commit message as feat, fix, or chore.
"add CSV export to reports" -> feat
"handle null user in session refresh" -> fix
"bump linter version" -> chore
Now label: "retry upload when S3 returns 503"
```

## Advanced: organizational techniques

### Delimited sections
For multipart requests, separate kinds of information with XML-style tags, Markdown headings or JSON fields. Typical sections: task (what to build), requirements (what it must include), constraints (versions, banned dependencies, limits), context (existing code), output (format). Separation stops important details from being lost or misweighted in one long paragraph.

```
<task>Add rate limiting to the public search endpoint</task>
<requirements>
- 60 requests per minute per API key
- Return 429 with a Retry-After header
</requirements>
<constraints>
- Python 3.12, no new third-party packages
- Must work behind multiple app instances
</constraints>
<output>Code plus a short note on trade-offs</output>
```

### Task decomposition
Large requests overwhelm models and yield incomplete or wrong answers. Break the work into phases exactly as you would for yourself or a junior, run one phase at a time, and adjust between phases. Start with the decision that constrains the rest (for example, streaming versus batch for very large files) and ask for pros and cons before any code.

Recommended phase order for a new component: design choice, core logic, validation, error handling and logging, tests.

## Prompt rewrite examples

Weak: "write a regex for emails"
Stronger: "Python 3.12. Write a pragmatic email validation regex for a signup form; accept plus-addressing and subdomains, reject spaces and missing TLD. Give 5 passing and 5 failing test strings and note what the regex deliberately does not cover."

Weak: "review my code"
Stronger: "Act as a senior reviewer focused on security and readability. This Go handler parses user uploads. List issues by severity with line references, then suggest fixes. Do not rewrite unrelated code."

Weak: "make this faster"
Stronger: "This query runs on a 50M-row Postgres table and takes 4s. First explain the likely plan, then propose index or query changes, then show the revised SQL with expected impact."

## Building a prompt library

Keep 5 to 10 proven prompts for recurring jobs: code review, documentation, debugging, test generation, explaining unfamiliar code, commit or PR summaries. Store them with placeholders, the tool and model they worked with, and notes on what made them work. Revisit them when tools change. This fits within a broader personal knowledge management habit.

## Pitfalls

- Vague verbs ("optimize", "improve", "fix") without a target metric.
- Missing version information, leading to outdated APIs.
- Dumping a large multi-goal request in one prompt.
- Accepting the first answer instead of iterating.
- Memorizing technique names instead of building clear communication habits; the techniques serve clarity, not the other way round.
