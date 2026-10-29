# Continuous Learning: In-Context Adaptation and Offline Retraining

## Contents
- Role in the loop
- Choosing the mechanism
- In-context learning
- Context management for adaptation
- Promotion path: from session fix to permanent fix
- Offline retraining
- Integrating the whole cycle
- Worked example
- Pitfalls

## Role in the loop

Continuous learning is where validated fixes become lasting behavior. Pipelines find the problem, experiments prove the fix, continuous learning embeds it either immediately (inside a session) or over time (periodic batch updates). It builds on Chapter 7 techniques: nonparametric ones such as exemplar retrieval and Reflexion, and parametric ones such as fine-tuning. Here the emphasis is feeding them with production data (interactions, telemetry, failure logs) while guarding against overfitting to short-lived trends and regressions.

## Choosing the mechanism

| Need | Mechanism | Persistence | Risk |
|---|---|---|---|
| Fix a failure during the current conversation, personalize to this user | In-context learning | Session only | Low |
| Try a new reasoning strategy or prompt structure on live traffic cheaply | In-context learning as test bed | Session only | Low |
| Fix a recurring, systemic misalignment across users | Offline retraining (prompts, tools, adapters) | Durable | Medium; overfitting, cost |
| Domain shift that prompts cannot absorb | Offline fine-tuning (e.g., LoRA adapter) | Durable | Higher; needs full validation |

Rule of thumb: start in context, promote what works, retrain offline for what keeps recurring.

## In-context learning

The fastest and most flexible adaptation: change behavior at runtime by placing examples, intermediate reasoning steps or contextual signals in the prompt, without touching weights or architecture.

Two modes:
- **Engineer-driven:** if an agent keeps mishandling a class of input (say one type of build error in a debugging assistant), add a demonstration of the correct handling to its prompt. Takes effect instantly, scoped to where it is applied.
- **User-driven:** corrections and clarifications from the user during the session steer the agent's next steps.

Strengths:
- User-specific adaptation: tailors to one person's preferences or recurring issues.
- Real-time feedback incorporation: reacts to clarifications and follow-ups immediately.
- Guided reasoning: explicit steps or intermediate outputs make conclusions more reliable and easier to inspect.

Best used for session-specific failures, rapid small iterations, and highly unpredictable inputs where static approaches fail. It is the low-risk first line of adaptation and a sandbox for strategies before they are made system-wide.

Limitation: everything learned disappears when the session ends.

## Context management for adaptation

Context windows are finite, so in-context learning is only as good as the curation of what goes in. Decide what to include, how to structure it and when to drop or compress it. Techniques:
- Rolling windows that keep the latest turns verbatim.
- Semantic compression (summarize older turns, keep decisions and corrections).
- Vector retrieval of the most relevant past examples or corrections.

Original sketch of retrieving corrections as exemplars:

```python
def build_prompt(base, user_msg, store, k=3, budget_tokens=1500):
    shots = store.search(user_msg, top_k=k, filter={"type": "approved_fix"})
    block, used = [], 0
    for s in shots:
        t = count_tokens(s.text)
        if used + t > budget_tokens:
            break
        block.append(s.text)
        used += t
    return f"{base}\n\nExamples of correct handling:\n" + "\n---\n".join(block) \
           + f"\n\nUser: {user_msg}"
```

## Promotion path: from session fix to permanent fix

Because in-context gains are transient, formalize the ones that prove useful:

1. Log in-session adaptations that led to success (user confirmed, task completed).
2. Aggregate them; frequent ones signal a systemic gap.
3. Promote to a durable form: prompt engineering, workflow update, tool change, or retraining.
4. Validate the promoted change like any other change (offline, shadow, live test).

## Offline retraining

Structured, periodic batches: collect interaction data (queries, outputs, labeled outcomes) from pipelines and experiments, and use it to update prompts and tools or fine-tune models in a nonproduction environment. Suited to systemic issues that accumulate over time, such as recurring reasoning or tool-use mistakes, without disrupting live traffic.

Steps:
1. **Data curation:** sample and label production traces; enforce diversity and balance across clusters, cohorts and outcomes to avoid bias.
2. **Model updates:** apply few-shot optimization (e.g., DSPy) or fine-tuning (e.g., a LoRA adapter on the base model), evaluating on held-out data with metrics such as accuracy and latency.
3. **Validation:** test offline against benchmarks, then shadow, then roll out.

Strengths:
- Durability: persists across sessions and users.
- Scalability: batch jobs can digest big volumes of logs with no added latency on live requests.
- Risk mitigation: offline testing catches regressions before exposure.

Limits and controls:
- Overfitting to historical data, or missing emerging trends: include recent data, keep a fresh holdout from the latest period, compare against the current version on both old and new slices.
- Compute cost: prefer parameter-efficient methods such as LoRA.
- Staleness: schedule retraining on a cadence (and trigger it early on detected drift).

Typical uses: refreshing prompt exemplars with newly seen cases, retraining a classifier inside a tool on recent logs. For teams on pretrained models it is a route to customization without constant online changes.

## Integrating the whole cycle

The stages only work connected: pipelines feed experiments, experiments decide what gets retrained, automation speeds discovery, humans keep changes aligned with strategy, and documentation preserves memory across teams. The cycle never ends: observe, adjust, validate, deploy, observe again. Culture matters as much as tooling; each failure is a signal to learn from. Teams that invest here gain reliability and also the ability to anticipate user needs and react to new trends.

## Worked example

A coding assistant keeps misdiagnosing a new linker error after a toolchain upgrade.

- Day 1: engineer adds one correct worked example to the system prompt for the affected repo type (in context, instant).
- Week 1: retrieval store tags confirmed fixes; similar sessions now get the example automatically. Success on that error type rises from 40% to 75% in logs.
- Week 3: aggregation shows the error in 6% of sessions overall. Team curates 180 labeled traces (balanced across languages and OSes), reoptimizes the prompt offline, checks it on a holdout from the last 7 days, shadows it for 5 days, then A/B tests it. Promoted after the test shows significance with no latency regression.
- Quarterly: the tool's internal error classifier is retrained on recent logs.

## Pitfalls

- Valuable session-level fixes never promoted, so every new session relearns them.
- Retraining on unbalanced data dominated by one loud cohort.
- Holdout drawn from the same period as training, hiding drift.
- Fine-tuning when a prompt or tool change would have solved it.
- Skipping shadow validation for retrained components because offline metrics looked good.
