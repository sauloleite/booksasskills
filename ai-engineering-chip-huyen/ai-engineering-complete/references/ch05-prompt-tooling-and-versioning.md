# Prompt Engineering Tools, Prompt Organization and Versioning

## Contents
- Landscape of prompt engineering tools
- When to adopt a tool
- Estimating hidden API calls
- Failure modes of tools
- Separating prompts from code
- Prompt metadata
- Prompt file formats
- Versioning: git versus a prompt catalog
- Catalog record design
- Pitfalls
- Glossary

## Landscape of prompt engineering tools

The space of possible prompts is unbounded and hand search is slow, so many tools try to help:

| Category | Examples | What it does |
|---|---|---|
| End-to-end optimizers | OpenPrompt (Ding et al., 2021), DSPy (Khattab et al., 2023) | You declare input/output formats, a metric and eval data; the tool searches for a prompt or prompt chain that maximizes the metric. Conceptually like AutoML hyperparameter search. |
| AI-written prompts | Asking a model to draft, critique or improve a prompt, or to generate in-context examples | Fast first drafts. Models are probably good at this partly because they trained on prompts shared online. |
| Evolutionary / gradient-style optimizers | Promptbreeder (DeepMind, Fernando et al., 2023), TextGrad (Stanford, Yuksekgonul et al., 2024) | Promptbreeder mutates a seed prompt using mutator prompts, keeps the most promising mutations and repeats until criteria are met. TextGrad uses textual feedback as a pseudo-gradient. |
| Structured-output helpers | Guidance, Outlines, Instructor | Constrain or validate generation into schemas. |
| Perturbation tools | Synonym swaps, rewrites | Try variants to find the most effective phrasing. |

## When to adopt a tool

Start without tools (keep it simple). Writing prompts by hand first teaches you the model's behavior and sharpens your own requirements. Then adopt an optimizer when all of these hold:
- The input and output formats are stable.
- You have an automatic metric you trust.
- You have an eval set large enough that optimizing against it will not simply overfit.
- You have an API budget cap and a way to count calls.

Adopt a structured-output helper earlier if downstream code breaks on malformed outputs.

## Estimating hidden API calls

Optimizers issue calls you do not see. Estimate before running:

```
calls = variants x eval_examples x calls_per_evaluation x rounds
```

`calls_per_evaluation` is often 3 rather than 1: generate the response, validate it (for instance, is it parseable JSON), and score it (often with an AI judge). Worked numbers: 10 variants on 30 examples with a single call each is 300 calls; with generate, validate and score it is 900; five optimization rounds make it 4,500. If the tool may invent prompt chains freely, multiply again by chain length, which can grow without bound. Set hard caps.

## Failure modes of tools

Tool authors make mistakes like anyone:
- Wrong chat template for the model in use.
- Building prompts by concatenating tokens rather than raw text, which can produce token sequences that never occur in normal tokenization.
- Typos in default prompts (the chapter shows a LangChain default critique prompt with several).
- Silent changes between versions: a new default template or rewritten built-in prompts.
- Permissive defaults lacking safety constraints (see the defenses reference for the injection study).

The more tools in the stack, the more places for these errors. Rule, in the spirit of Hamel Husain's "Show Me the Prompt": always look at the exact prompts a tool sends, and track how many calls it makes.

## Separating prompts from code

Keep prompts in their own module or files and import them where queries are built. Benefits:
- **Reuse**: several applications can share one prompt.
- **Testing**: test code with different prompts, and prompts independently of code.
- **Readability**: neither code nor prompt is cluttered by the other.
- **Collaboration**: domain experts can edit prompts without touching application code.

## Prompt metadata

Once there are many prompts across many apps, attach metadata so each prompt is findable and its intended use is clear. A useful record:

| Field | Why |
|---|---|
| Prompt id and version | Pinning, rollback, audit |
| Model name (and version) | Prompts are model-specific and break on model change |
| Endpoint URL | Where it is meant to run |
| Application(s) | Ownership and blast radius of changes |
| Creator | Who to ask |
| Date created | Staleness checks |
| Prompt text / template | The content itself |
| Sampling parameters (temperature, top-p, max tokens) | Results depend on them as much as on wording |
| Input schema | Which placeholders must be hydrated, and their types |
| Output schema | Contract for structured outputs consumed downstream |

A typed object (for example, a Pydantic model) is a natural way to enforce the record in Python.

## Prompt file formats

Several projects define dedicated prompt file formats with a metadata header and a templated body: Firebase Dotprompt, Humanloop, Continue Dev and Promptfile. Dotprompt, for instance, places the model id plus input and output schemas in front matter above a templated prompt. Benefit: metadata and prompt travel together and can be validated.

## Versioning: git versus a prompt catalog

| Approach | Good when | Weakness |
|---|---|---|
| Prompt files in the application repo, versioned by git | One application owns its prompts | Shared prompts update for everyone at once. A team cannot stay on an older prompt while another adopts the new one. |
| Separate prompt catalog with per-prompt explicit versions | Many applications share prompts | More infrastructure, but each app pins the version it was evaluated against |

A good catalog also:
- Stores metadata and supports search (by model, application, owner).
- Tracks which applications depend on each prompt.
- Notifies dependent owners when a newer version is published, so they can re-evaluate and upgrade deliberately.

Upgrade procedure for a shared prompt: publish version N+1 without mutating N; notify dependents; each runs its frozen end-to-end eval on N+1 and moves its pin independently, or stays on N with a recorded reason.

## Pitfalls

- Prompts stored without the model and sampling parameters they were tuned for.
- Mutating a published prompt in place, changing behavior for every consumer.

## Glossary

- **Prompt catalog / registry**: a versioned, searchable store of prompts with metadata and dependency tracking.
- **Pinning**: an application referencing an exact prompt version.
- **Mutator prompt**: in Promptbreeder, a prompt that instructs the model how to alter another prompt.
