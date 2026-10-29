# The Probabilistic Nature of AI: Inconsistency and Hallucination

## Contents
- What probabilistic means, and why it matters
- Inconsistency: two scenarios and their fixes
- Hallucination: why it is hard
- Hypothesis 1: self-delusion and snowballing
- Hypothesis 2: knowledge mismatch during SFT
- RLHF and hallucination
- Mitigation playbook
- Worked example
- Pitfalls and glossary

## What probabilistic means, and why it matters

Outputs are sampled, so the same question can get different answers. A model that gives one cuisine 70% and another 30% will name the first about 70% of the time; a deterministic system would not vary. Models aggregate a vast range of opinions, so anything with non-zero probability can appear, however wrong: a fringe essay claiming all US presidents are aliens, once in training data, can resurface and look invented.

This makes models good creative partners and a pain nearly everywhere else. In one review of three months of an AI company's support tickets, about a fifth concerned inconsistency; industry leaders broadly name hallucination the top enterprise blocker; and a law firm was fined in 2023 for filing fabricated case research from ChatGPT. Systematic evaluation is the first defense.

## Inconsistency: two scenarios and their fixes

1. **Same input, different output** (grading one essay twice yields 3/5, then 5/5). Fixes: cache answers; pin temperature, top-p and top-k; fix the seed. Residual variation remains because hardware executes and rounds differently; self-hosting gives hardware control, API users get only what the provider offers. Consistency only under pinned settings is like a grader who is fair in one room and erratic in any other: better than nothing, not trustworthy.
2. **Slightly different input, very different output** (one capital letter changes the result). Settings cannot fix this. Use careful prompt design, a memory system that keeps context stable, robustness tests with perturbed inputs (casing, spacing, paraphrase), multiple samples for brittle models, or a more robust model.

Users expect the consistency they get from people, who do not give a new name at each meeting.

## Hallucination: why it is hard

Hallucination is output not grounded in facts. It predates LLMs (discussed for text generation by 2016). Sampling explains inconsistency but not fully hallucination: the puzzle is how something apparently never seen becomes probable, and nobody can search the training data to check. Without a known cause, elimination is hard; two hypotheses dominate and complement each other (one blames self-supervision, the other supervision).

## Hypothesis 1: self-delusion and snowballing

DeepMind (Ortega et al., 2021): the model cannot tell given text from text it generated. After an off-target early statement, later tokens treat it as fact and build on it.

- Invented example: summarizing a clinic note, a model writes "knee" for "ankle" in sentence one, then recommends a knee scan and lists knee-specific risks.
- A vision model reading a shampoo label decided the bottle held milk, then listed milk as an ingredient.
- Zhang et al. (2023) call this snowballing: the model defends an early error and even fails questions it would otherwise get right (claiming a number divisible by 13 to stay consistent).

Proposed remedies: RL that teaches the model to separate user observations from its own actions, and supervised training with factual and counterfactual signals.

## Hypothesis 2: knowledge mismatch during SFT

Leo Gao, later echoed by John Schulman (2023): SFT teaches imitation of labeler answers, and when labelers use knowledge the model lacks, the model learns to assert unsupported content. Attaching sources to every demonstration would fix this but is impractical. Schulman also claimed models know what they know; if so, force answers from known information via verification (retrieve the sources behind each response) and a reward that penalizes fabrication harder, since comparison-trained reward models learn only which response won, not why.

## RLHF and hallucination

Schulman reported RLHF reduced hallucination at OpenAI, but the InstructGPT paper found its RLHF model hallucinated more than SFT alone, even though people preferred it overall. Measure rather than assume.

## Mitigation playbook

1. Ground answers in supplied context (retrieval, documents, tool results).
2. Instruct the model to answer truthfully and admit when it does not know.
3. Ask for concise answers; fewer tokens, fewer chances to invent.
4. Require sources per claim and verify them.
5. Check intermediate claims in multi-step output; restart instead of continuing from an error.
6. Add detection and factuality evaluation before serving high-stakes answers (detection is hard, as it is for human lies).
7. Compare model variants (SFT versus preference-tuned) on your own factuality set.

## Worked example

A finance assistant gives different answers to identical policy questions; T = 0, a fixed seed and caching cut repeat variation sharply but not to zero on the hosted API. Separately, 4% of answers cite nonexistent policy clauses. The team retrieves the actual policy text, instructs answers only from retrieved passages or an explicit "not found", caps length, and rejects answers citing clause IDs absent from the retrieved set. Fabricated citations fall below 0.5%; the rest go to human review.

## Pitfalls and glossary

Pitfalls: expecting T = 0 plus a seed to be identical across infrastructure; equating consistency under fixed settings with reliability; letting a model reason on from unverified claims; assuming RLHF cut hallucination for your case; long ungrounded answers to factual questions.

- **Seed**: starting point of the sampler's random number generator.
- **Self-delusion**: treating self-generated text as given fact.
- **Snowballing hallucination**: compounding errors to justify an early mistake.
- **Knowledge mismatch**: labeler knowledge beyond the model's, taught through SFT.
