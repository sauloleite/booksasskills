# Nonparametric Learning: Exemplars, Reflexion, Experiential Insights

## Contents
- Framing: what "learning" means here
- Ladder of nonparametric techniques
- Exemplar learning (fixed and dynamic few-shot, case memory)
- Reflexion (failure-driven self-critique)
- Experiential learning (ExpeL-style insight lists)
- Choosing between the three
- Pitfalls
- Worked example: a ticket-routing agent
- Glossary

## Framing: what "learning" means here

In this chapter, learning means the agentic system gets measurably better by interacting with its environment. It is optional. Every learning loop adds design work, an evaluation signal, and monitoring, so add one only when the expected gain pays for that overhead.

Nonparametric learning improves behavior while leaving model weights untouched: what changes is the context the model sees (examples, reflections, rules). Parametric learning changes the weights (see the fine-tuning references). The author's default is to begin with nonparametric methods because they are cheap, fast to ship, transparent and reversible.

Every technique below needs a quality signal per attempt: a success flag, a score, a KPI hit/miss, or a human comment. No signal, no learning.

## Ladder of nonparametric techniques

| Rung | What is stored | What is injected into the prompt | Learns from |
|---|---|---|---|
| Fixed few-shot | Nothing at runtime | Hand-picked static examples | Designer judgment |
| Dynamic exemplars | Successful (problem, solution, outcome) cases | Top-k most relevant past successes | Successes |
| Reflexion | Trial logs plus short self-critiques | Latest few reflections for the same or similar task | Failures, per task |
| Experiential (ExpeL) | Experience pool plus a curated rule list | A small distilled set of general rules | Successes and failures, across tasks |

Climb only as far as needed. Each rung adds an LLM call or a curation step.

## Exemplar learning

**Fixed few-shot.** Examples are baked into the system prompt. Fine for a prototype. Two limits appear as the example set grows: every extra example adds tokens (cost and latency) on every call, and many examples are irrelevant to a given input.

**Dynamic few-shot.** Store examples outside the prompt and select the most relevant ones at runtime. Selection can be by task type (metadata filter), by lexical text retrieval, or by semantic similarity. Move from fixed to dynamic once you have more good examples than you can afford to inline.

**Case memory (case-based reasoning).** Each record holds: the problem description, the solution or action sequence applied, the outcome, and any feedback. At run time the agent finds similar past cases, inspects what was done, and adapts it to the current situation. Because outcomes are stored, the agent can lean toward what worked and away from what did not.

Design checklist for an exemplar bank:
- Gate writes on the quality signal; by default only store successes as exemplars (failures are useful later for Reflexion or ExpeL).
- Store context, actions, outcome and feedback, not just the final answer.
- Index on the fields you will retrieve by (task type, key entities, embedding of the problem statement).
- Cap k so the prompt budget stays predictable.
- Apply the technique to the whole task or to a sub-step independently (for example, only to the query-planning step). Sub-step banks are often cleaner and more reusable.
- Version the bank like code: you need to know which exemplars were live when behavior changed.

The chapter treats this as a well-replicated result: retrieving saved successful examples into the prompt lifts performance across many task types. It is the cheapest first learning loop to try.

## Reflexion

Reflexion gives the agent a habit of verbal self-critique after failed attempts. Reflections accumulate in a memory buffer and are read back before the next attempt, so the strategy improves while the model stays frozen. It accepts both numeric feedback (pass/fail) and free-text comments, and has reported gains on tasks such as code debugging and multistep reasoning.

The loop:
1. Run the task with the normal planning prompt.
2. Persist the whole trial (each action, each observation, final status) to durable storage such as a JSON file or a database table.
3. On failure, build a reflection request that contains the recent history and asks what strategy was missed and what to change.
4. Have a memory-update step call the model on that request and append the resulting reflection to the agent's memory for that task or environment.
5. On the next attempt at the same or a similar task, prepend the latest reflections to the prompt.

Building the reflection prompt well (three parts, in this order):
- **Framing:** tell the model it failed, ask it to diagnose strategy rather than summarize the environment, and to emit its corrective plan after a fixed marker word so the output is easy to parse.
- **Goal restatement:** repeat the original instruction so the critique is anchored to the true objective.
- **Full transcript:** include every action, observation and internal thought, ending with an explicit failure status, so the critique rests on evidence.
End with the marker (for example a trailing "Plan:" cue) to push the model from diagnosis into prescription.

Engineering rules:
- Bound the memory: feed only the most recent few reflections (the chapter's sample keeps the last three) to cap context growth.
- Skip reflection on successful trials and on trials flagged to be ignored.
- Keep each LLM call behind a small wrapper so graph nodes stay focused and reusable.
- Key reflections by task or environment so they are injected only where relevant.

Minimal shape (illustrative, framework-agnostic):

```python
def after_trial(task_id, transcript, success, store, llm, keep=3):
    if success:
        return
    recent = store.reflections(task_id)[-keep:]
    prompt = "\n\n".join(recent + [
        "You failed this task. Diagnose the strategic mistake, not the scenery.",
        f"Goal: {store.goal(task_id)}",
        transcript + "\nSTATUS: FAIL",
        "Plan:",
    ])
    store.add_reflection(task_id, llm(prompt))

def build_prompt(task_id, base_prompt, store, keep=3):
    notes = store.reflections(task_id)[-keep:]
    return ("Lessons from earlier attempts:\n" + "\n".join(notes) + "\n\n" + base_prompt) if notes else base_prompt
```

## Experiential learning (ExpeL-style)

Experiential learning extends Reflexion from per-task notes to cross-task lessons. The agent still logs experiences, but it adds an aggregation step that turns many experiences into a short, maintained list of general rules. This transfers good practice between different tasks and lets the policy drift with a nonstationary environment.

Pipeline:
1. **Collect** experiences into a pool (observation, action, outcome).
2. **Extract** insights: ask the model to analyze an observation, or better, to contrast a failed trial with a successful one, and propose rules that would have avoided the failure.
3. **Maintain** the rule list with four operations, each emitted in a strict, parseable format with the rule number:
   - AGREE: an existing rule is strongly relevant (reinforce it).
   - REMOVE: a rule contradicts or duplicates another.
   - EDIT: a rule is too narrow or can be improved.
   - ADD: a new rule that is distinct and likely useful elsewhere.
   Rules not touched are carried forward unchanged.
4. **Rank** insights: promote those associated with success, demote those associated with misses, so a small high-value set rises to the top.
5. **Distill and inject** only the top rules into future prompts.
6. **Optionally review**: a human can refine a promoted insight before it spreads.

Rules for the rule list:
- Insist that rules be general and high level, about how to think and act better, not restatements of one episode.
- Keep three tiers (candidate, promoted, demoted) or a score per rule; inject only promoted or top-scoring rules.
- Parse operations strictly; reject malformed lines instead of guessing.
- Periodically re-run the maintenance pass so stale rules lose rank as the environment changes.
- Use a downstream reflection over promoted rules to plan the next experiment, as in the chapter's marketing-KPI example where hits promote and misses demote.

## Choosing between the three

| Situation | Pick |
|---|---|
| You have a handful of good examples and a stable task | Fixed few-shot |
| Many successful examples, varied inputs | Dynamic exemplar retrieval |
| Same task is retried and failures are diagnosable from the transcript | Reflexion |
| Many related tasks, want lessons that transfer, environment drifts | Experiential insight list |
| Thousands of examples and the prompt is getting expensive | Consider fine-tuning (see fine-tuning decisions) |

They stack: exemplars for "how a good answer looks", reflections for "what went wrong last time on this task", rules for "what generally works here".

## Pitfalls

- No reliable success signal: the loop learns noise. Fix the evaluator first.
- Unbounded memory: prompts bloat, latency climbs, and old advice crowds out new. Cap k and recency.
- Storing failures as exemplars: the model imitates bad trajectories. Keep failures for critique, not imitation.
- Over-specific insights: rules that mention one product or one date do not transfer. Force generality in the extraction prompt.
- Duplicate or contradictory rules: run REMOVE and EDIT, not only ADD.
- Silent drift: track which exemplars, reflections and rules were active per run so regressions can be traced and rolled back.

## Worked example: a ticket-routing agent

An agent routes support tickets to queues; a human reassignment marks a miss.
- Week 1: fixed few-shot with eight hand-written tickets.
- Week 3: 1,200 correctly routed tickets exist. Switch to dynamic selection of the five most similar past tickets, filtered by product line.
- Week 4: some ticket families keep failing on retry. Add Reflexion keyed by ticket family; the last three reflections are injected.
- Week 6: run an ExpeL pass weekly over successful versus reassigned pairs. Rules such as "billing words plus a contract ID mean the contracts queue, not billing" get promoted; a rule tied to a retired product gets demoted and later removed.
- Week 10: prompts carry five exemplars plus three reflections plus eight rules, and the volume is high and stable. Now the fine-tuning decision checklist becomes relevant.

## Glossary

- **Exemplar:** a stored past interaction, with its outcome, reused as an in-context example.
- **Memory buffer (Reflexion):** the per-task store of recent self-critiques.
- **Experience pool:** the raw log of trials that insight extraction reads from.
- **Insight / rule:** a short, general lesson distilled from many experiences; ranked by promotion and demotion.
- **Nonstationary environment:** one whose correct policy shifts over time; insight lists adapt to it without retraining.
