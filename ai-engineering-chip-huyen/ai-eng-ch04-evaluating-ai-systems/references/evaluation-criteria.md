# Evaluation criteria: capability, instructions, roleplay, cost and latency

## Contents
- Evaluation-driven development
- The four criteria buckets
- Domain-specific capability
- Generation capability (beyond factuality and safety)
- Instruction-following capability
- Roleplay and persona evaluation
- Cost and latency
- Building the criteria sheet
- Worked example
- Pitfalls
- Glossary

Factual consistency and safety are covered in their own reference file because they need dedicated methods.

## Evaluation-driven development

Decide how success will be judged before building, as test-driven development writes tests first.

- An unmeasurable shipped feature is a liability: it costs money, is awkward to retire, and nobody knows whether it helps.
- Enterprise AI that survives has a clear yardstick: recommendations (conversion), fraud detection (losses avoided), code (tests pass), close-ended classification. Even then, isolate the feature's effect with A/B tests (a promotion can lift purchases too).
- Counterweight: only building what is easy to score skips promising ideas. The author sees weak evaluation as the main brake on adoption, so better evaluation unlocks hard use cases.

## The four criteria buckets

1. **Domain-specific capability:** does the model know the subject and reason in it?
2. **Generation capability:** is free-form output faithful, relevant, coherent, safe?
3. **Instruction following:** does it respect format, length, content, style and persona constraints?
4. **Cost and latency:** affordable at your volume, fast enough for your users?

For a contract summarizer: knowing contract law (1), a faithful, well-structured summary (2), the requested length and layout (3), price and wait per summary (4). Start from each criterion and ask which method measures it.

## Domain-specific capability

- Architecture, size and training data cap domain skill; a language absent from training cannot be prompted into existence. Missing capability rules a model out.
- Measure with public or private domain benchmarks.
- **Code and SQL:** functional correctness is the default but not the only bar.
  - Efficiency: measure runtime and memory exactly, relative to a reference solution (BIRD-SQL does this). Correct but slow SQL can be unusable.
  - Readability: no exact metric; use an AI judge or human review.
- **Non-code knowledge and reasoning:** usually multiple choice (about three quarters of tasks in a popular open harness in early 2024), because it is easy to verify and reproduce.
  - Score by accuracy, by difficulty-weighted points, or with partial credit when several options are correct. For classification (same labels on every item) add precision, recall, F1.
  - The random baseline (1/k) is known; beating it usually, not always, means real skill.
- **Multiple-choice warnings:** an extra space or an added label before the options can change answers, so keep the template identical across models. It tests picking a good answer, not producing one: never use it as evidence of summarization, translation or writing quality.

## Generation capability (beyond factuality and safety)

- Classic NLG metrics: **fluency** (sounds like a fluent speaker), **coherence** (sound overall structure), and task-specific ones such as **faithfulness** (translation) and **relevance** (does a summary focus on what matters most).
- Strong models largely solved fluency and coherence. Still track them for weak models, creative writing and low-resource languages, using an AI judge or perplexity.
- The pressing concerns now are unwanted hallucination and harm. Hallucination is welcome in fiction, harmful wherever facts matter.
- App-specific qualities (controversiality, friendliness, positivity, creativity, conciseness) use the same toolbox: a rubric plus a judge.

## Instruction-following capability

- If the model ignores instructions, prompt quality stops mattering. Newer, larger models usually follow instructions better.
- Symptom: the model grasps the task but breaks the output contract (asked for one of three sentiment labels, it invents others). Domain skill present, instruction following absent.
- Critical for structured output (JSON, regex) since non-conforming answers break downstream code. Also covers unstructured constraints, such as a children's story generator limited to words a given child knows.
- **Entanglement warning:** a failure may mean the model lacks the skill (cannot write a given verse form) or misread the request, and a weak prompt can pass for a weak model. Try a clearer instruction before blaming the model; confirm the underlying skill before blaming the prompt.

### Two reference designs

| Design | What it checks | How it scores |
|---|---|---|
| IFEval style | Constraints code can verify: required or banned keywords, word/sentence/paragraph/bullet counts, language, title marker, postscript, placeholders, JSON | Fraction of instructions satisfied |
| INFOBench style | Adds content scope, linguistic register, tone and style, which code cannot verify | Each instruction split into yes/no criteria; score is criteria met over total |

- In the INFOBench study a strong LLM answered those yes/no checks more accurately than crowdworkers (though below experts) at low cost, so AI-judged decomposed criteria are a practical default.
- Public instruction benchmarks miss many real instructions. **Build your own set from your constraints:** need YAML, test YAML; banned phrase, test that it never appears.

## Roleplay and persona evaluation

- Used for user-facing characters (games, companions, storytelling) and as a prompting technique; roleplay ranks among the ten most common request types in a large public chat-log study.
- Hard to automate. Research benchmarks use reward models on a 5-point scale, similarity to expected outputs, and AI judges.
- Judge two axes: **style** (sounds like the character) and **knowledge** (knows what the character knows and nothing it should not). Negative knowledge matters: a game character must not leak spoilers or speak a language the character does not know.
- Use heuristics where the persona allows (a laconic character should have short average replies), and a role-specific judge prompt for the rest.

## Cost and latency

- A great model that is too slow or expensive is useless; many teams accept lower quality for better cost or speed.
- **Pareto approach:** name what you cannot compromise on, filter candidates on it, then pick the best survivor on the rest.
- **Latency metrics:** time to first token, time per output token, time between tokens, total time per query. Pick the ones your UX depends on (streaming chat: first token; batch jobs: total).
- Latency also depends on prompt and output length and sampling. Levers: request concise answers, set stop conditions, optimize inference.
- **Must-have vs nice-to-have:** nobody refuses faster, but slowness is usually an irritation, not a reason to quit.
- **Cost structure:** APIs bill per input and output token at a roughly flat rate as you grow. Self-hosting is mostly fixed compute: a cluster costs about the same near idle or near full (electricity aside), so per-token cost falls with utilization. Teams pick the largest model that fits GPU memory (16, 24, 48, 80 GB cards), which is why popular model sizes cluster at those limits. Revisit API vs self-hosting at every scale jump.

## Building the criteria sheet

For each criterion record **metric, data source (public benchmark or internal set), hard requirement, ideal target.** Typical rows: price per million output tokens; throughput the provider must sustain (tokens per minute); P90 time to first token and P90 total query time on your own prompts; overall quality from a public preference ranking; task capability (for example pass@1 on a code benchmark); factual consistency on an internal hallucination set. Hard requirements eliminate; ideal targets rank.

## Worked example

A travel-booking assistant must return itinerary JSON, answer in the user's language, and quote fares from a database.

- Bucket 1: 300 private fare-rule questions, accuracy.
- Bucket 2: fare quotes checked for local consistency against database rows.
- Bucket 3: JSON schema validity (code), language match (detector), no apology boilerplate (string check).
- Bucket 4: P90 first token under 1 s (hard, streaming UI); cost per session under a margin-based budget.
- Drop models failing JSON validity or latency; rank survivors by fare accuracy.

## Pitfalls

- Inferring generation quality from multiple-choice scores, or changing option formatting between models.
- Accepting code because it runs, ignoring speed, memory and readability.
- Testing what a persona should say but never what it must not know.

## Glossary

- **Automatically verifiable instruction:** a constraint a program can check.
- **Decomposed criteria:** yes/no checks derived from one instruction.
- **Negative knowledge:** facts a persona must not reveal or know.
