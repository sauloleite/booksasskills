---
name: baa-ch07-learning-in-agentic-systems
description: Guidance for making agents improve from experience, based on Chapter 7 of Michael Albada's "Building Applications with AI Agents". Covers nonparametric learning (dynamic few-shot exemplars, Reflexion, ExpeL-style insight lists) and parametric learning (when to fine-tune, SFT for function calling, DPO, RLVR, small vs large models). Use when deciding whether an agent should learn at all, designing a feedback or memory loop, choosing between prompting and fine-tuning, preparing tool-call or preference datasets, or picking a model size to tune.
---

# Learning in Agentic Systems (Albada, Chapter 7)

## Purpose

Help an engineer add the right amount of learning to an agent. "Learning" here means the system measurably improves through interaction with its environment. It is optional: every loop costs design, evaluation and monitoring effort. The chapter orders the options from cheap and reversible (change what goes into the prompt) to expensive and durable (change the weights), and says to climb only as far as the evidence requires.

## Key decision rules

Apply these even without opening a reference.

**Whether to learn**
1. Learning is not required for a working agent. Add it only when the expected gain beats the extra design, evaluation and monitoring cost.
2. Every loop needs a per-attempt quality signal (success flag, score, KPI hit, human comment). Without one, fix evaluation first.

**Nonparametric first**
3. Default to nonparametric learning: weights stay frozen, only context changes. It is cheap, fast, transparent and reversible.
4. Ladder: fixed few-shot, then dynamic exemplar retrieval, then Reflexion, then experiential insight lists. Stop at the lowest rung that works.
5. Store successful cases (problem, actions, outcome, feedback) and retrieve the most relevant ones by type, text or semantic similarity once there are too many to inline. Can be done for the whole task or for one sub-step.
6. Reflexion: after a failure only, generate a short strategic critique and inject the latest few (the chapter keeps three) into the next attempt. Build the critique prompt as framing, restated goal, full transcript ending in a failure status, then a plan cue.
7. Experiential learning: contrast failures with successes, maintain a small list of general rules via AGREE, REMOVE, EDIT, ADD; promote rules tied to wins, demote those tied to misses; inject only top rules. Good for cross-task transfer and drifting environments.

**When to fine-tune**
8. Consider fine-tuning only when there are many examples and carrying them in prompts is too costly, and when performance needs, data and operational capacity all align.
9. Signals for: narrow domain or jargon, rigid template or tone, high-consequence tool calls, hundreds to thousands of curated examples plus budget, sustainable retraining cadence.
10. Signals against: prototyping or low volume, fast-improving upstream base models that could erase your work, scarce GPUs or annotation budget, tight latency (prefer RAG and nonparametric methods).
11. Never pretrain. Start from a suitably licensed instruction-tuned open model and check whether prompting alone meets the bar. When in doubt, do not fine-tune.
12. Always keep a plan for retraining or migrating when the next base model ships.

**Which method**
13. You can write the right answer: SFT. You can only say which of two is better: DPO. You can score answers automatically or with a scalable grader: RLVR. Image inputs: vision fine-tuning. Expert-graded complex reasoning in legal or medical: RFT.
14. Progression: SFT establishes behavior, DPO adds preferences, RLVR optimizes any verifiable reward and can generalize past observed rankings.

**SFT for tool use**
15. First rely on built-in function calling plus runtime schema validation. Tune only when prompts become unwieldy, arguments are repeatedly mis-parsed, accuracy misses a strict bar, and volume justifies it.
16. One schema per tool, included in training examples and enforced on every call at run time (same version). Reject or repair mismatches before execution.
17. Train both "call" and "do not call" cases (hypotheticals and conditionals need no call), plus argument extraction, asking for missing parameters, and fallback on tool errors.
18. Separate reasoning and actions with special tokens, register them in the tokenizer, and use the identical chat template at train and inference time. Use LoRA (optionally 4-bit base) and hold out a test split.

**Model size**
19. Under 8B for on-device or lowest cost; 8B to 70B for general reasoning; frontier proprietary for highest-stakes accuracy. A small model tuned on a narrow task can match a large one.
20. The best small family changes within months: recheck third-party leaderboards and confirm on your own eval set.

**Combine**
21. Run nonparametric loops continuously; periodically distill stable, high-volume patterns into weights; keep the nonparametric layer on top for what changes later.

## Default workflow

1. Confirm a reliable per-attempt quality signal and log every trial (inputs, actions, observations, outcome).
2. Ship with fixed few-shot examples; switch to dynamic retrieval of successful cases when examples outgrow the prompt.
3. Add Reflexion for retried tasks with diagnosable failures; add an insight list when lessons should transfer across tasks or the environment drifts.
4. Bound every memory (top-k, recency), version what was injected per run, and watch cost and latency.
5. If prompts stay long, volume is high and the use case is stable, run the fine-tuning go/no-go checklist.
6. If go: curate data from logged trials, validate it with the script below, pick SFT, DPO or RLVR, train with LoRA, evaluate on a hold-out, ship behind a version flag, and trim now-redundant prompt examples.

## References

- [references/nonparametric-learning.md](references/nonparametric-learning.md): read when designing exemplar banks, Reflexion loops or insight lists, or choosing between them; includes a worked example and pitfalls.
- [references/fine-tuning-decisions.md](references/fine-tuning-decisions.md): read when deciding whether to fine-tune, which method to use, or whether a small or large model fits; includes decision walkthroughs.
- [references/sft-dpo-rlvr-playbook.md](references/sft-dpo-rlvr-playbook.md): read when building tool-calling SFT data, configuring LoRA/SFT or DPO runs, designing RLVR graders, or combining both learning families.
- [references/source-map.md](references/source-map.md): read to find which file covers a given chapter section.

## Scripts

- `scripts/validate_finetune_jsonl.py`: run `python3 scripts/validate_finetune_jsonl.py data.jsonl --schemas tools.json --min-no-call-share 0.2` to check an SFT tool-calling dataset before training (role order, every tool call answered by a matching tool result, arguments parse and match the tool schema, balanced think/tool_call tags, duplicates) and to report the share of examples that correctly make no tool call. Run `python3 scripts/validate_finetune_jsonl.py pairs.jsonl --format dpo` to check DPO pairs (non-empty prompt, chosen and rejected; chosen differs from rejected; length comparison). Add `--json` for machine-readable output. Exit code 1 means errors were found.
