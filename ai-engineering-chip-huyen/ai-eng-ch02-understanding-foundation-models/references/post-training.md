# Post-Training: SFT, Preference Finetuning, Reward Models

## Contents
- What post-training fixes
- The pipeline and what to infer from it
- Supervised finetuning and demonstration data
- Preference finetuning: goal and methods
- Reward models
- Optimizing against the reward model, or not
- Playbook for application engineers
- Worked example
- Pitfalls and glossary

## What post-training fixes

A pre-trained model has two problems: self-supervision optimizes it to continue text rather than converse (asked how to make pizza, it may extend the question or add more questions instead of answering; it talks like a web page), and indiscriminate web data makes it capable of toxic or wrong output.

Pre-training optimizes token-level prediction; users judge whole responses. Post-training targets the responses users prefer. It is cheap by comparison (InstructGPT: about 2% of compute versus 98% for pre-training) and mostly unlocks abilities the base model already has but that prompting alone struggles to reach.

## The pipeline and what to infer from it

1. Self-supervised pre-training: capable but unruly.
2. Supervised finetuning (SFT): conversational and more acceptable.
3. Preference finetuning: polished for customers.

The well-known meme of a tentacled monster wearing a smiley mask fits: the polish is a thin layer. Knowing which stages a model went through tells you roughly how aligned it is. Any stage can be skipped; training only on demonstrations from scratch is possible but usually worse than starting from pre-training.

"Instruction finetuning" may mean SFT alone or SFT plus preference tuning; ask. Both stages compensate for poor pre-training data and might become unnecessary if that improves.

## Supervised finetuning and demonstration data

SFT (behavior cloning) trains on (prompt, response) demonstrations covering every task type you want: question answering, summarization, translation and so on. InstructGPT's mix was text-only.

Demonstrations often demand research, critical thinking and judgment about whether to comply, so labelers are highly educated (for InstructGPT, about 90% held a degree and over a third a master's). A single pair may take half an hour, longer for long-context tasks. At $10 each, InstructGPT's roughly 13,000 pairs would cost around $130,000 before task design, recruiting and quality control.

| Source | Upside | Downside |
|---|---|---|
| Expert labelers | Best quality, handles judgment | Slow, costly |
| Volunteers (LAION: about 13,500 people, 10,000 conversations, 35 languages) | Cheap, multilingual | Little bias control; about 90% of surveyed volunteers were male |
| Heuristic mining of web dialogue (Gopher kept alternating two-speaker exchanges) | Scales | Inherits web quality |
| Synthetic data | Less human labor | Inherits generator bias |

Labelers who teach preference should ideally represent the users; check who produced the data.

## Preference finetuning: goal and methods

Demonstrations teach how to converse, not which conversations to have. Some requests are clear-cut; many (abortion, gun control, immigration, drug legality) divide people by culture, politics and religion. Any answer upsets someone; over-censoring makes the product dull. The goal of matching human preference assumes a universal preference exists and can be embedded, so treat it as aspirational. Deliberately misaligned models can even be useful, for example to test how persuasive generated misinformation could be.

- **RLHF** (GPT-3.5, Llama 2): train a reward model, then optimize the model to maximize its scores. More complex, more knobs; Llama 2's authors credited it for writing that surpassed annotators on some tasks.
- **DPO** (Llama 3): Meta switched to cut complexity.
- **RLAIF**: AI rather than human feedback (possibly used for Claude).

Both RLHF and DPO beat SFT alone empirically, though why is debated and methods will keep changing.

## Reward models

- **Use comparisons.** Direct scores (pointwise evaluation) are noisy: one labeler gives 5, another 7, and the same labeler may change their mind. Comparison data is (prompt, winner, loser).
- **Expect disagreement.** InstructGPT labelers agreed about 73% of the time, and published preference examples can look backwards to a thoughtful reader.
- **Cost.** A comparison takes about three to five minutes because responses must be fact-checked; one Llama 2 author cited about $3.50 per comparison versus $25 per written response. Ranking k responses yields every pair (three give three pairs, four give six). InstructGPT collected 1 to 7 scores but trained only on rankings.
- **Objective.** The model emits a scalar per (prompt, response); training minimizes the negative log-sigmoid of the winner's score minus the loser's.
- **Initialization.** Train from scratch or start from the pre-trained or SFT model; the strongest base tends to work best. A weaker judge can still score a stronger generator because judging is easier than generating.

## Optimizing against the reward model, or not

Prompts drawn from a distribution (often real user prompts) go to the SFT model; the reward model scores its responses; the model is updated, typically with PPO, to raise scores.

Some teams skip RL. Stitch Fix and Grab sample several outputs and keep the ones their reward model rates highest, a best-of-N approach that moves the benefit to inference time.

## Playbook for application engineers

1. Identify the variant: base models need completion-style or few-shot framing; chat variants follow instructions.
2. Expect refusals and tone to mirror the builder's preference data, including its demographic and language skew; test on your own sensitive cases.
3. Do not assume preference tuning reduced hallucination: InstructGPT's RLHF model hallucinated more than its SFT-only model, though people preferred it overall.
4. When collecting preferences, rank several responses per prompt and budget for fact-checking.
5. Without RL capacity, use a reward model or verifier to select among samples.

## Worked example

A team has 2,000 prompts. Gold responses at $25 each cost $50,000. Instead, labelers rank four sampled responses per prompt, giving six pairs each, 12,000 comparisons in total, for about $16,000 at around $8 per ranking. Expecting roughly 73% agreement, they double-label a subset to measure their own rate and drop prompts where labelers split evenly.

## Pitfalls and glossary

Pitfalls: saying "instruction-tuned" without naming stages; treating base-model rambling as a bug; trusting one labeler's absolute scores; assuming one preference model fits every audience; treating RLHF as a hallucination fix.

- **Behavior cloning**: imitating (prompt, response) demonstrations.
- **Pointwise evaluation**: scoring responses in isolation.
- **Comparison data**: (prompt, winner, loser) triples.
- **PPO**: RL algorithm commonly used against the reward model.
