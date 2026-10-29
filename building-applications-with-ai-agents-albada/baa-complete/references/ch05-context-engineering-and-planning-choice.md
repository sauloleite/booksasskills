# Context engineering and choosing a planning approach

## Context engineering

Prompt engineering is about wording instructions. Context engineering is broader: at every model call, assemble user messages, retrieved knowledge, workflow state and system instructions into a structured window that stays within the token budget and maximizes task performance. Orchestration chooses the next step; context engineering makes sure that step has what it needs. It links planning to execution.

Archetype-specific needs:
- Planner-executor: executors need the plan (or their slice of it) passed cleanly and unambiguously.
- ReAct: each cycle needs the latest tool results placed clearly in the prompt.

### What can go into the window

| Component | Include when |
|---|---|
| System instructions (role, allowed actions) | always |
| Current user input | always |
| Retrieved snippets from memory or knowledge bases | they bear on this step |
| Summaries of earlier conversations | continuity or personalization matters |
| Workflow state (plan, step index, prior tool outputs) | multistep tasks |
| Environment facts (time, location) | tools or answers depend on them |

A simple system needs only the system prompt plus the latest query. Dynamic construction becomes essential as tasks get multistep or personalized.

Invented example, insurance claims assistant at the "check coverage" step: system prompt listing permitted actions; the customer's message; a short summary of the claim record; the two policy clauses retrieved for the claim type; the output of the earlier damage-assessment tool. Not included: the full policy document, unrelated past chats, raw logs.

### Four practices

1. **Relevance first.** Retrieve the few most useful items; do not append large blocks indiscriminately. Irrelevant material distracts the model and burns tokens.
2. **Predictable structure.** Use consistent sections or schemas (Model Context Protocol is cited as one way to pass state and knowledge in an interpretable format).
3. **Compress history.** Summarize long histories, keeping decisions, identifiers and open questions.
4. **Rebuild every step.** Assemble context per inference to match the current objective, workflow stage and input; do not just keep appending.

```python
def build_context(step, state, retrieve, summarize, budget_tokens, count):
    parts = [("SYSTEM", state["system_prompt"]),
             ("GOAL", step["objective"]),
             ("USER", state["latest_user_msg"])]
    if state.get("history"):
        parts.append(("HISTORY_SUMMARY", summarize(state["history"])))
    if step.get("needs_plan"):
        parts.append(("PLAN", state["plan_slice"]))
    for doc in retrieve(step["objective"], k=4):
        parts.append(("EVIDENCE", doc))
    while sum(count(t) for _, t in parts) > budget_tokens and parts[-1][0] == "EVIDENCE":
        parts.pop()                     # drop lowest-ranked evidence first
    return "\n\n".join(f"## {k}\n{v}" for k, v in parts)
```

### Why it matters

The author argues the design frontier is moving from model architecture toward context quality: strong context lets modest models do well, while poor context undermines even top models. Expect context engineering to remain the integrating layer as memory, retrieval and orchestration tooling evolve.

### Context pitfalls

- Stuffing whole documents or full transcripts "just in case".
- Unstructured concatenation that hides which text is instruction, which is evidence and which is state.
- Reusing a stale context across steps after the objective changed.
- No token accounting until a call fails.

## Choosing a planning approach (chapter checklist)

The author closes with best practices for picking a planning strategy. Restated as a checklist:

1. **Latency vs accuracy**: quantify both; more planning buys accuracy at the cost of time.
2. **Typical number of actions**: more actions per task implies a more capable planning approach.
3. **Plan adaptivity**: if results of earlier actions often change what comes next, pick a technique that adjusts the plan incrementally.
4. **Representative test cases**: build them first and use them to compare approaches empirically.
5. **Simplest sufficient approach**: start small with well-designed scenarios and move up in complexity only as the use case requires.

Worked decision (invented): an internal IT helpdesk agent. Budget 4 s, high accuracy on account actions. Most tickets need 1 to 3 actions; plans rarely change mid-task except for escalations. Decision: semantic tool selection, a short chain with a length cap of 4, reflection only before the irreversible "disable account" tool, and a 200-case test set comparing this against a ReAct baseline on success rate and p95 latency.
