# Deciding Whether to Finetune (and Finetune vs RAG)

## Contents
- What finetuning buys you
- Kinds of post-pretraining training
- Signals that favor finetuning
- Costs and signals against
- The "general models are weak in our domain" trap
- Facts versus form: RAG or finetuning
- The adaptation ladder
- Worked examples
- Glossary

## What finetuning buys you

Finetuning continues training an existing model, on all or some weights, until it handles a target task well enough. It is transfer learning: knowledge from a data-rich task (next-token prediction on web text) is reused for a data-poor one (legal QA, text-to-SQL). The payoff is sample efficiency: a task needing millions of examples from scratch may need only hundreds from a good pretrained model.

Treat finetuning as making existing capability easier to reach, not as installing knowledge. InstructGPT framed it as surfacing abilities prompting struggles to elicit; the Llama 3.1 team argued post-training should teach a model the limits of what it knows rather than add facts. The non-finetuning alternative is feature-based transfer: freeze a model and train a separate head on its embeddings.

In practice finetuning is used most for instruction following, especially sticking to a required style or format. It can also raise domain skill and strengthen safety.

## Kinds of post-pretraining training

Any training after pre-training counts as finetuning. Options for an application team:

| Variant | Data | Use for | Caveat |
|---|---|---|---|
| Continued pre-training | Raw in-domain text, no labels | Cheap domain warm-up before paying for labeled pairs | Does not teach task format |
| SFT, next-token | (instruction, response) pairs, open or closed-ended | Format, style, task behavior | Good pairs are costly when they need expertise or factual care |
| SFT, infilling | Text with a gap, context on both sides | Editing, code repair | Works on autoregressively pretrained models too |
| Preference finetuning | (instruction, preferred, rejected) | Steering toward human preference | Comparison data is a separate effort |
| Long-context finetuning | Long sequences, positional-embedding changes | Longer context (Code Llama: 4,096 to 16,384 tokens) | Harder; may degrade short inputs |

Start from a post-trained (instruct) checkpoint unless you have a reason not to; the closer the start, the less adaptation you pay for. Developers sometimes release variants trained to different degrees so you can pick the closest.

## Signals that favor finetuning

1. **Narrow-task quality gap.** Strong benchmark models can still be weak where they saw little data: an uncommon SQL dialect, customer-specific query patterns, a niche DSL.
2. **Hard output syntax.** JSON, YAML and regex usually work with strong models plus structured-output tools; rare or complex syntaxes (semantic parsing into unusual schemas) more often need finetuning.
3. **Bias mitigation.** Curated data can counter biases from pre-training (one study reduced gender and racial bias in BERT-like models by finetuning on text by women and by African authors).
4. **Small model, big-model quality.** Finetuning small models is the common case: cheaper to train and serve. Grammarly's finetuned Flan-T5 beat a text-editing GPT-3 variant about 60 times larger, using roughly 82,000 instruction pairs. Distillation from a large model is the usual route.
5. **More demonstrations than a prompt holds.** Prompt caching weakened the token-cost argument; the remaining one is that context length caps in-prompt examples while training sets have no cap.
6. **A rich open-model ecosystem**, which has made finetuning far more practical than when only closed models were strong.

## Costs and signals against

- **Regressions elsewhere** (sometimes called an alignment tax). Example: a support model good at recommendations and feedback but weak at order changes, finetuned only on order changes, can get worse at the other two. Remedies in order: train on a mix of all query types; use separate per-task models; merge them if serving several is a burden.
- **Data**: slow and costly, worst for expert tasks. Open and synthetic data help unevenly.
- **Training skill**: choosing a base model, optimizer and learning rate, sizing data, diagnosing over- and underfitting, evaluating throughout. Frameworks automate the run, not the judgment.
- **Serving**: self-hosting and optimizing an LLM is nontrivial; easier if you already run models in-house.
- **Maintenance and churn**: new bases may improve faster than your finetune. Decide in advance how much better a new base must be before you switch, and whether to try finetuning a base that does not win out of the box. Switching often yields a small increment and loses priority to new use cases.
- **Need versus want**: some engineers push finetuning to learn it. Leads should tell that apart from a real requirement.

Prompting comes first, done properly. A recurring story: a team claims prompting failed, but its experiments were few and ad hoc, instructions vague, examples unrepresentative, metrics undefined; after a disciplined process, prompting sufficed. That discipline also yields the evaluation pipeline, annotation guidelines and experiment tracking that finetuning will need.

## The "general models are weak in our domain" trap

Measure before believing it. As general models improve, they improve on specialized domains too. Cautionary case: a finance-specific 50B model from early 2023 (about 1.3M A100 hours, roughly $1.3M to $2.6M in compute excluding data) was clearly beaten on financial sentiment and financial QA benchmarks by a general frontier model released the same month and used zero-shot. Mid-size general models of similar quality, some open-weight, followed. Fair caveats: benchmarks miss some internal use cases, and building such a model teaches a team a lot. Neither excuses skipping the comparison.

## Facts versus form: RAG or finetuning

| Failure | Looks like | Next step |
|---|---|---|
| Information missing | Private facts; model refuses or hallucinates | RAG |
| Information stale | Answer reflects pre-cutoff world | RAG |
| Correct but irrelevant | Accurate, wrong focus or detail level | Finetune on well-specified outputs |
| Malformed | Code that will not compile, invalid syntax | Finetune with more target-format exposure |
| Unsafe | Policy violations | Finetune (plus guardrails) |

RAG grounds answers and can reduce hallucination. Finetuning teaches syntax and style; with plenty of good data it may reduce hallucination, with poor data it can raise it.

Evidence (Ovadia et al., 2024, 7B models):
- On current-events QA, RAG beat finetuning, and RAG over the untouched base beat RAG over finetuned models.
- RAG beat finetuning on almost all MMLU categories.
- RAG on a finetuned model beat RAG alone only 43% of the time.

With both failure types, start with RAG (no data curation, no custom hosting), and begin with term-based retrieval such as BM25 before a vector database. Complexity lands differently: better retrieval adds runtime components; finetuning adds development work but leaves inference unchanged.

## The adaptation ladder

Define evaluation criteria and build the pipeline before any step; rerun it at every rung.

1. Prompting alone, with versioned prompts.
2. Add examples, typically 1 to 50.
3. Informational failures: connect data with term-based retrieval; relevant context should give some lift even with simple retrieval.
4. Branch: still informational, try embedding or hybrid retrieval; behavioral (irrelevant, malformed, unsafe), finetune.
5. Try RAG and finetuning together; keep it only if evaluations improve.

No path fits every application; observed failure modes pick the next rung.

## Worked examples

**Warehouse SQL dialect.** A frontier model writes standard SQL well but misuses dialect functions; few-shot helps partly; schema retrieval already exists. Behavioral failure, more examples than fit in context: finetune with LoRA on an instruct model, mix in standard SQL to avoid regressions, evaluate both.

**Policy assistant citing last year's rules.** Stale information: add BM25 over the policy repository. Do not finetune on policies that will change again.

**Spec generator producing thin output.** Accurate but missing sections: behavioral. Try a strict template and two or three gold examples; finetune on a few hundred curated specs only if systematic prompting still falls short.

## Glossary

- **Sample efficiency**: quality gained per training example.
- **Feature-based transfer**: reusing a frozen model's embeddings in another model.
- **Continued pre-training**: self-supervised training on raw domain text.
- **Alignment tax**: quality lost on other tasks after specialization.
- **Semantic parsing**: natural language to a formal structure (JSON, SQL, DSL).
