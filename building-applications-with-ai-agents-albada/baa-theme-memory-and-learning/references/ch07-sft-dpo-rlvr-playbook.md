# SFT, DPO and RLVR Playbook for Agents

## Contents
- Ordering of the three techniques
- SFT for function calling
  - Prerequisites and when to start
  - Schema discipline (train time and run time)
  - Dataset design: call, no-call, recover
  - Special tokens and chat templates
  - LoRA plus SFT training recipe
  - What you get
- DPO for output quality
- RLVR for any measurable reward
- Combining nonparametric and parametric learning
- Pitfalls
- Glossary

## Ordering of the three techniques

The chapter presents a progression, each step building on the last:
1. **SFT** teaches the model to reproduce gold outputs. Foundation of behavior shaping.
2. **DPO** adds preference learning: the model learns which of two outputs is better.
3. **RLVR** adds policy optimization against an explicit, measurable reward from any grader.

A typical path is SFT first (establish format and correct behavior), then DPO or RLVR to polish quality.

## SFT for function calling

### Prerequisites and when to start

SFT on tool use teaches both the mechanics (formatting the call) and the judgment (whether a call is warranted at all). It goes beyond what hosted function calling gives you, offering tighter control and consistency.

Start with the base model's built-in function calling plus runtime schema validation. Move to SFT only after showing that prompting and the stock function-calling API are insufficient, for example:
- prompts have become unwieldy trying to patch tool behavior,
- the same parameters keep getting mis-parsed,
- accuracy is below a strict domain requirement,
- and traffic is high enough that each point of reliability matters.

At high volume, a tuned (often smaller, self-hosted) model can also lower per-call cost versus expensive proprietary endpoints, partly by cutting retries and malformed calls.

### Schema discipline (train time and run time)

- Define a machine-readable contract for every exposed tool: name, argument names and types, required fields, return shape. JSON Schema or a TypeScript/Zod schema both work.
- Include those schemas in the training examples so the model learns the exact JSON payload, not just which function to pick.
- At run time, check each call the model proposes against that identical schema (Pydantic, Zod, Ajv) before executing. Reject or repair mismatches. This catches malformed and malicious requests early, simplifies debugging and hardens the system against odd inputs.
- The schema used in training and the schema enforced at run time must be identical; version them together.

Run-time gate sketch:

```python
def gate_tool_call(call, schemas):
    schema = schemas.get(call["name"])
    if schema is None:
        return False, f"unknown tool {call['name']}"
    args = call["arguments"]
    missing = [k for k in schema.get("required", []) if k not in args]
    extra = [k for k in args if k not in schema.get("properties", {})]
    if missing or extra:
        return False, f"missing={missing} unexpected={extra}"
    return True, "ok"   # then type-check with a full validator before executing
```

### Dataset design: call, no-call, recover

Each example shows the full exchange: user turn, the assistant's decision, the tool call with arguments, the tool result, and the final reply that uses the result. Cover these behaviors deliberately:
- **Should call:** a factual request maps to a tool ("weather in Lisbon now" leads to a weather call with location set to Lisbon, and the answer cites the result).
- **Should not call:** hypotheticals, conditionals and chit-chat ("suppose it snows in Lisbon, what should I pack?" or "if the meeting moves I'll skip lunch") are answered by reasoning alone.
- **Argument extraction:** turning messy user phrasing into valid typed arguments.
- **Recovery:** asking for a missing required parameter instead of inventing it.
- **Graceful fallback:** a tool returns an error and the assistant explains or retries sensibly.

Hold out a test split (the chapter's recipe uses 10% with a fixed seed) and measure call precision, no-call accuracy and argument validity on it. Use `scripts/validate_finetune_jsonl.py` to check structure and the call/no-call mix before training.

### Special tokens and chat templates

Mark segments so the model can tell dialogue, private reasoning and actions apart: wrap reasoning in think tags and tool invocations in tool_call tags (`<think>...</think>`, `<tool_call>...</tool_call>`). Practical consequences:
- Register these as additional special tokens in the tokenizer and resize the model's embedding matrix to match.
- Set an explicit chat template, and render every training conversation through it so formatting is consistent.
- If the base template has no system role, merge the system message into the first user turn during preprocessing.
- Use the identical template at inference; a mismatch silently degrades tool behavior.

### LoRA plus SFT training recipe

The chapter's minimal pattern, described in prose:
1. Load the base model, optionally in 4-bit (NF4, double quantization, bf16 compute) to cut memory.
2. Build the tokenizer with the special tokens and the chat template; resize embeddings.
3. Load the conversation dataset, render each conversation to text through the template, split train/test.
4. Attach LoRA adapters so only targeted layers are trained.
5. Train with Hugging Face TRL's SFT trainer, which supports sequence packing and gradient checkpointing.

Starting hyperparameters used in the chapter's example (treat as a baseline, then tune): 1 epoch, learning rate 1e-4, per-device batch 1 with gradient accumulation 4 (effective batch 4), max sequence length about 1,500 tokens, cosine schedule with 10% warmup, gradient clipping at 1.0, bf16, evaluation each epoch, packing on, gradient checkpointing on.

### What you get

- Lower tool-call error rates and fewer retries, which also reduces token spend.
- Contextual judgment about when not to call.
- More dependable automation as agents take on larger decision-making roles; the author regards structured function calling as a foundational skill worth tuning for.

## DPO for output quality

DPO trains on ranked pairs instead of single gold answers. For each prompt, the data holds a preferred ("chosen") and a dispreferred ("rejected") completion, typically produced by sampling several completions and having humans pick the better one. The model learns to favor the kind of output that wins.

When to use it: your goal is shaping quality (tone, concision, empathy, summary focus) rather than replicating a single correct output. It complements SFT rather than replacing it.

Data format, one JSON object per line: a prompt, a chosen response, a rejected response. Good pairs differ mainly in the quality dimension you care about; if the rejected answer is also factually wrong, the model may learn the wrong lesson.

The chapter's worked example tunes a small Phi-3-mini model on IT help-desk replies with LoRA and 4-bit loading. Settings worth knowing:
- **beta (0.1 in the example):** how strongly training pushes toward the chosen response relative to the reference behavior. Higher is more aggressive; lower stays closer to the starting model.
- **Loss type:** sigmoid (the standard DPO loss).
- **Reference-free mode:** skips a separate frozen reference model, saving memory.
- **Learning rate much lower than SFT:** 5e-6 versus 1e-4, over 3 epochs, effective batch 16 (4 x 4 accumulation).
- **Length limits and truncation:** cap prompt and completion lengths and keep the end of long prompts when truncating, so the most recent context survives.
- **LoRA on all attention and MLP projections**, rank 8, alpha 16, dropout 0.05.

Evaluate with blind pairwise comparison of base versus tuned outputs on held-out prompts.

## RLVR for any measurable reward

RLVR optimizes the policy against an explicit reward function. Its key property is that any grader you can build can drive training: rule checks, automatic metrics, a separate judge model, or people. Targets include summarization quality, tool-call correctness, retrieval factuality and adherence to safety constraints.

How it differs from DPO: DPO only learns from the pairwise rankings it observed. RLVR couples preference signals with reinforcement learning, predicting value scores and optimizing toward them, so it can generalize beyond the rankings in the data.

Loop: sample prompts, generate several completions each, score them with the grader, feed rewards to the trainer, update the policy, repeat.

Choose RLVR when:
- you have ranked preference data or can write a dependable scoring function,
- you want continual quality improvement,
- rewards are sparse, or human labeling at scale is too costly.

Grader design notes (practical additions consistent with the chapter's premise):
- Prefer verifiable checks: unit tests, schema validation, exact-match on tool arguments, citation presence.
- Combine signals with explicit weights and log each component so reward hacking is visible.
- Keep a held-out eval that the grader never trains against.

```python
def reward(completion, case):
    score = 0.0
    call = parse_tool_call(completion)            # your parser
    if case["expects_call"]:
        score += 0.5 if call and call["name"] == case["tool"] else 0.0
        score += 0.5 if call and call["arguments"] == case["args"] else 0.0
    else:
        score += 1.0 if call is None else 0.0     # reward restraint
    return score
```

The chapter does not print the full RLVR code (it lives in the book's companion repository); the summary is that RLVR extends RFT so models predict and optimize for what is most useful, opening a path to self-improving, task-specialized models.

## Combining nonparametric and parametric learning

The closing message: nonparametric learning is agile, cheap and responsive to real-world change; parametric learning gives deeper specialization (SFT for structured output and tool calls, DPO for nuanced quality). Use both: keep exemplars, reflections and insight lists running for fast adaptation, and periodically distill the stable, high-volume patterns into weights. Every learning investment must match operational constraints and performance goals.

A practical cadence:
1. Nonparametric loop runs continuously and logs every trial with its quality signal.
2. Successful trials accumulate into a curated SFT set; graded or paired outcomes into DPO or RLVR data.
3. When volume and stability justify it, train, evaluate on the hold-out, and ship behind a version flag.
4. Shrink the in-prompt exemplars the tuned model no longer needs, cutting tokens.
5. Keep the nonparametric loop on top for whatever changes after the training cutoff.

## Pitfalls

- Training on tool calls whose schema differs from what production validates.
- A dataset with almost no negative (no-call) examples, producing a trigger-happy agent.
- Mismatched chat template or missing special tokens at inference.
- DPO pairs whose rejected side is wrong in several ways at once.
- A reward that can be gamed (format-only checks) with no hold-out to reveal it.

## Glossary

- **LoRA:** low-rank adapter matrices trained on top of frozen weights; cheap to train and swap.
- **Packing:** concatenating short examples into one sequence to fill the context window during training.
- **Gradient checkpointing:** recomputes activations in the backward pass to save memory.
- **beta (DPO):** strength of the preference push away from the reference behavior.
- **Verifiable reward:** a score produced by a check that can be rerun and audited.
