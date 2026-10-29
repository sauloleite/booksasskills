# Extracting Feedback from Conversations

## Contents
- Why feedback matters more for AI products
- Uses of feedback; explicit versus implicit
- Natural language feedback signals
- Complaint taxonomy and fixes
- Action-based signals
- Interpretation rules
- Worked example
- Pitfalls and glossary

## Why feedback matters more for AI products

Feedback has always evaluated software and steered its development. In AI products it is also **training data**, and proprietary data is a moat. A sound feedback system drives the data flywheel: launch early, gather signals, improve models, and stay ahead as public data grows scarce.

Constraints: feedback is user data, with the usual privacy duties and a user right to know how it is used. Distribution matters too: a self-hosted open source release gives almost no usage visibility, so collecting feedback is far harder than for a hosted product.

## Uses of feedback; explicit versus implicit

| Use | Output |
|---|---|
| Evaluation | Production monitoring metrics |
| Development | Training data, preference pairs, prompt changes, priorities |
| Personalization | Per-user adaptation |

| | Explicit | Implicit |
|---|---|---|
| Source | Direct request: thumbs, stars, votes, "did this solve it?" | Inferred from user actions and words |
| Interpretation | Easy, standard across apps | Hard, noisy, app-specific |
| Volume | Sparse (costs effort), worse for small user bases | Abundant |
| Main distortion | Response bias: unhappy users respond more, skewing negative | Ambiguity: one action, opposite meanings |

Conversational interfaces make giving feedback natural (users praise and correct as with a person) and extracting it hard (it is blended into dialogue). One reply can reveal both quality and preference: after an assistant offers three hotels, choosing the one near galleries signals interest in art, while asking for cheaper options signals price sensitivity and that the assistant has not learned the user yet. Intuition supplies initial cues; validate them with data analysis and user studies. The topic predates chat LLMs: reinforcement learning researchers have explored learning from verbal feedback since about 2018, and voice assistants (Alexa, Spotify, Yahoo) studied it earlier.

## Natural language feedback signals

Extracted from message content; track them in production.

- **Early termination**: stopping generation midway, leaving the app, telling a voice assistant to stop, or never answering an agent waiting for a choice. Usually a bad sign.
- **Error correction**:
  - Follow-ups opening with a negation or restated intent signal a miss.
  - **Rephrasing** is a correction attempt; detect with heuristics (high overlap with the prior user turn) or a model. Early stop plus rephrase strongly indicates misunderstood intent.
  - **Specific corrections** name the fix (two characters' roles swapped in a summary); the model should apply them.
  - **Action nudges** are common with agents: the user names a source or step the agent skipped.
  - **Confirmation requests** (double-check, cite sources) do not prove an error; they may mean missing detail or general distrust.
  - **Direct edits** (fixing generated code, changing a category) are a very strong negative on the edited part and yield a preference pair: original rejected, edit chosen.
- **Complaints**: wrong, irrelevant, toxic, too long, too thin, bad. Cluster them.
- **Sentiment**: negative affect without a reason. Track trajectory: rising frustration is trouble; angry at the start and calm at the end suggests resolution (call centers apply this to voice volume).
- **Model-side**: refusals and admissions of ignorance predict an unhappy user. Track refusal rate.

## Complaint taxonomy and fixes

Automatic clustering of the FITS search-grounded dialogue dataset (Xu et al., 2022) produced eight groups. Largest, at roughly a quarter, was users restating their demand; next came complaints that the bot did not answer, was irrelevant, or pushed the work back to the user; then users pointing to a specific search result with the answer, or telling the bot to use the results; then claims of factual error or ungrounded answers; then answers judged insufficiently specific or complete; then complaints about constant hedging. Repetition or rudeness was under 1%.

Build your own taxonomy the same way (cluster, label) and map types to fixes; LLMs can do the clustering at scale.

| Complaint | Likely fix |
|---|---|
| Too verbose | Conciseness instruction or length limit |
| Missing detail | Specificity instruction; better retrieval coverage |
| Wrong or ungrounded | Grounding instructions, retrieval quality, citation checks |
| Ignores available sources | Fix context assembly or prompt emphasis |
| Excessive hedging | Recalibrate refusal and uncertainty behavior |

## Action-based signals

- **Regeneration**: often dissatisfaction, but also a wish to compare (common in creative work) or a consistency check (if two answers contradict, trust neither). Stronger under usage-based billing than flat subscriptions. Asking for a new-vs-old comparison afterwards yields preference data.
- **Organization**: delete is strongly negative unless the chat was embarrassing; rename means a good chat with a poor auto-title; share and bookmark are ambiguous.
- **Length (turns)**: long is good for companion apps, bad for support and productivity bots.
- **Dialogue diversity**: distinct tokens or topics. Long plus low diversity, with the bot repeating itself, means the user is stuck in a loop.

## Interpretation rules

1. Never read one implicit signal literally; sharing can celebrate a great answer or expose a blunder, depending on the user.
2. Combine signals: share then rephrase leans negative; early stop then rephrase is strongly negative.
3. Condition on product type and billing model.
4. Study users (interviews, labeled samples) to learn why they act; calibrate weights accordingly.
5. Validate against explicit feedback where both exist.

## Worked example

A support chat: user asks how to export invoices; the bot answers for the wrong product tier; the user stops generation and writes "no, I meant from the mobile app"; the bot answers; the user asks whether it is sure and where that is documented; the bot links a help article; the user thanks it and leaves after 4 turns.

Tags: early stop, negation-led correction, confirmation request, positive close, short conversation. Reading: the first answer missed intent (tier-aware routing or retrieval is the fix candidate), the second lacked a source (cite by default), the issue resolved. `scripts/implicit_feedback.py` computes these tags and rates over a JSONL log.

## Pitfalls and glossary

Pitfalls: treating regeneration, sharing, or long sessions as uniformly good or bad; relying only on sparse, negatively skewed thumbs; ignoring model refusals; storing edits without the original output; counting complaints without clustering them.

- **Natural language feedback**: feedback carried in message text.
- **Preference example**: (prompt, chosen, rejected) triple for preference finetuning.
- **Dialogue diversity**: distinct token or topic count in a conversation.
