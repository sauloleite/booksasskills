# Scoping and Proving the First Agent

Covers the chapter's opening example: how to carve a first slice of work for an agent, and how to show it works before widening it.

## Picking the slice

A good first slice is a job humans already do by reading unstructured input, looking something up, pressing a button in some system, and writing a short reply. If people follow written rules to do it, a model plus a few tools can usually follow them too.

The chapter's running case is ecommerce support email: refund a damaged item, cancel an order that has not shipped, change a delivery address. Each request takes a person about two minutes and repeats all day.

Three scoping failure modes to check a proposal against:

| Failure | Symptom | Consequence |
|---|---|---|
| Too narrow | One intent only (cancellations) | Real but tiny impact; neighbouring high-volume intents still go to humans |
| Too broad | "Handle every support ticket" | Billing disputes, recommendations and troubleshooting bury the team in edge cases |
| Too vague | "Make customers happier" | No way to tell when you are done or whether you improved |

A slice is right when it has all three properties:

- **Concrete inputs**: e.g. the customer's message plus the order record.
- **Structured outputs**: a tool call with typed arguments, then a confirmation text.
- **Tight feedback loop**: each run can be checked quickly and automatically.

Practical sequence: ship one intent end to end (cancel), then add the sibling intents that share the same inputs and output shape (refund, address change). Only then consider broader categories.

## Translating the human procedure into an agent

Write down what a person does, step by step, and map each step:

| Human step | Agent equivalent |
|---|---|
| Read the email | Model reads message in context |
| Look up the order | Order record injected into state, or a lookup tool |
| Check eligibility (not shipped yet) | Rule inside the tool or a guard before it |
| Click the action | Business tool such as `cancel_order(order_id)` |
| Reply to customer | Second model pass that writes the confirmation |

The minimal loop is: model decides whether a tool applies, the tool runs, the model sees the tool result and writes the reply. Keep the system prompt specific about which intent maps to which tool and what to do otherwise.

Put hard business rules (refund limits, shipped status) inside the tool or a deterministic guard, not only in the prompt.

## Proving it works

The chapter's position: an agent you have not tested is an agent you cannot trust. Before expanding scope, check three things per case:

1. Was the right tool selected?
2. Were the arguments correct (the right order ID)?
3. Was the confirmation clear and accurate?

Then scale the same checks over hundreds of real tickets and report aggregate metrics:

- **Tool precision / recall**: of calls made, how many were right; of calls needed, how many happened.
- **Parameter accuracy**: share of calls with exactly correct arguments.
- **Task success rate**: end-to-end correct outcome.
- **Confirmation quality**: rubric or reviewer score of the reply.

Framework-agnostic harness sketch (illustrative, not from the book):

```python
def score_case(run_agent, case):
    trace = run_agent(case["message"], case["order"])   # returns tool calls + reply
    calls = trace["tool_calls"]
    want = case["expected_tool"]                       # None if no tool should fire
    tool_ok = (want is None and not calls) or any(c["name"] == want for c in calls)
    args_ok = all(c["args"] == case["expected_args"] for c in calls if c["name"] == want)
    reply_ok = all(k in trace["reply"].lower() for k in case["reply_must_mention"])
    return {"tool": tool_ok, "args": tool_ok and args_ok, "reply": reply_ok,
            "success": tool_ok and args_ok and reply_ok}

def summarize(results):
    n = len(results)
    return {k: sum(r[k] for r in results) / n for k in results[0]}
```

Include negative cases (messages that should trigger no tool, or a different tool) so precision is measured, not only recall.

## Worked example (invented)

A team proposes an agent to "automate HR inbox". Apply the rules:

- Vague and broad. Mine the inbox: 40% are payslip copy requests, 15% address updates, the rest varied.
- First slice: payslip requests. Input: employee message plus HR record. Output: `send_payslip(employee_id, month)` and a confirmation.
- Eval set: 200 historical emails, 30 of them negatives (questions about tax, which must not trigger the tool).
- Gate to expand: tool precision and parameter accuracy high enough that reviewers stop correcting it; then add address updates.
