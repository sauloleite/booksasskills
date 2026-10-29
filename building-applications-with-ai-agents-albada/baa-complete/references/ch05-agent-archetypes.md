# Agent archetypes

The archetype fixes how an agent reasons, plans and acts, and therefore its latency, cost and ceiling on task complexity. The author treats the list as a starting taxonomy in a fast-moving field: expect hybrids, and re-evaluate as new metareasoning and planning methods appear.

## Decision grid (own synthesis)

| Archetype | Explicit plan artifact? | Revises course mid-task? | Model calls per task | Pick it if the task... |
|---|---|---|---|---|
| Reflex | no | no | 0 to 1 | is triggered by a recognizable condition and needs one action |
| ReAct | no (trace only) | every step | several, unbounded unless capped | is exploratory and the next step depends on what was just observed |
| Planner-executor | yes | on failure, by replanning | 1 large plus cheap executors | has a decomposition you can predict up front |
| Query decomposition | yes (subquestions) | per subquestion | one per fact plus synthesis | needs several external facts combined |
| Reflection | yes (critiques) | after each action | roughly double ReAct | can cause costly or irreversible harm if wrong |
| Deep research | yes (agenda) | continuously | many, the most of all | needs depth and rigor more than speed or low cost |

## Reflex agents

- Map an input directly to an action with no intermediate reasoning: a condition fires, a tool runs.
- Strengths: minimal latency, deterministic behavior, trivial to test.
- Limit: no multistep reasoning and no use of context beyond the current input.
- Fit: keyword routing, single data lookups, simple automations of the form "when X, call Y".

## ReAct agents

- Loop of think, call a tool, observe the result, repeat until done. The plan is revised after every observation.
- LangChain variants mentioned: a zero-shot form that puts tools and instructions in one prompt with no example traces, and a chat form that also feeds conversation history into each decision.
- Fit: exploratory analysis, aggregating across sources, troubleshooting, anywhere mid-course adaptation is worth more than the added latency.
- Side benefit: the reasoning trace aids debugging and audits. Side cost: higher API spend and slower responses.

## Planner-executor agents

- Phase 1 produces a multistep plan; phase 2 runs each step through tool calls.
- Advantages the author lists: clean decomposition into subtasks; debuggability because you can inspect the plan, see which step failed and replan; cost efficiency because a large model plans while smaller models or fewer calls execute.
- Design tip: persist the plan as a structured object so monitoring can attribute failures to a step and trigger a targeted replan rather than a full restart.

## Query-decomposition agents

- Break a hard question into follow-up subquestions, answer each with search or another tool, then synthesize. Commonly called self-ask with search.
- Invented example: "Which of two drugs got FDA approval first?" becomes "When was drug A approved?" (search), "When was drug B approved?" (search), then a comparison.
- Fit: whenever the answer depends on external facts, because every intermediate fact is anchored to a tool output before composition.

## Reflection (metareasoning) agents

- Extend ReAct with a review step: after acting, compare the current state with the goal state, critique the reasoning, fix logic errors, reinforce what worked. ReflAct is cited as a recent framework grounding reasoning in goal-state reflection.
- Fit: workflows where an early mistake snowballs, such as financial transactions, clinical decision support, incident response.
- Key behavior: detect when a tool result departs from expectation and replan or roll back before anything irreversible is committed.
- Accept the extra latency only where correctness matters more than speed.

## Deep research agents

- Combine patterns: planner-executor to lay out the research agenda, query decomposition to turn subtopics into targeted searches, ReAct loops to refine hypotheses as evidence arrives.
- Typical cycle: plan subtopics and sources; turn each into concrete queries; call tools (academic search, domain databases) and judge each result's relevance and reliability; fold insights into an evolving report with summarization and critique at each step.
- Strengths: handles cross-disciplinary, multistage work; shifts direction as evidence emerges; explicit plans make the method auditable.
- Weaknesses: heavy model and API usage; delay accumulates across planning, decomposition and reflection layers; depends on external sources being available and good, so it needs error handling and fallbacks.
- Fit: long-form expert tasks where depth and rigor matter more than speed.

## Selection heuristics

- Start from the cheapest archetype that can plausibly solve the task and move up only when tests show failures it cannot fix.
- Hybrid is normal: a reflex router can dispatch to a ReAct worker; a planner can use reflection only before irreversible steps.
- If you need auditability, prefer archetypes with explicit artifacts (plans, subquestions, reflections) over opaque single calls.
- Put reflection where errors are expensive, not everywhere; it multiplies latency.

## Pitfalls

- Choosing deep research or reflection for routine tasks, paying high cost and latency for no accuracy gain.
- Using reflex agents on tasks that occasionally need two steps; they will fail silently on those cases.
- Letting a ReAct loop run unbounded; set an iteration cap and a budget.
- Treating the taxonomy as fixed; revisit as new planning strategies mature.
