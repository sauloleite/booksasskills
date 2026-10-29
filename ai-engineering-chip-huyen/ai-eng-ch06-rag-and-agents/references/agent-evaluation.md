# Agent Failure Modes and Evaluation

## Contents
- Evaluation philosophy
- Failure taxonomy
- Planning failures and their metrics
- Tool failures
- Efficiency
- Benchmarks and harnesses
- Worked example: scoring a planning dataset

## Evaluation philosophy

Evaluation is failure detection, and complex tasks have more failure points. Agents inherit generic AI failures and add planning, tool and efficiency failures, some subtle. Since success needs both a good tool inventory and a good planner, test both.

Core method: **enumerate the failure modes, then measure each one's frequency.** (The book's GitHub repo holds a small illustrative benchmark.)

## Failure taxonomy

| Family | Mode | Invented illustration |
|---|---|---|
| Planning: tool use | Invalid tool | Plan calls `web_lookup` but no such tool is in the inventory |
| Planning: tool use | Valid tool, invalid parameters | `convert_currency(amount, from)` called without the required `to` argument, or with an extra unknown one |
| Planning: tool use | Valid tool, wrong parameter values | Correct signature, but amount 1,500 passed when the invoice says 1,050 |
| Planning: goal | Plan does not solve the task | Asked to book a venue in Porto, books one in Braga |
| Planning: goal | Constraint violated | Venue in Porto but 40% over budget, or for the wrong dates |
| Planning: goal | Time constraint missed | A tax filing prepared after the filing deadline |
| Planning: reflection | False completion | Asked to tag 200 tickets, tags 170 and reports success |
| Tool | Tool returns wrong output | OCR misreads a total; generated SQL is wrong |
| Tool | Translation error | Natural-language step mapped to the wrong command |
| Tool | Missing tool | Needs live exchange rates but has no internet access |
| Efficiency | Too many steps, too costly, too slow | Valid result after 60 calls where 8 would do |

**Time is the most overlooked constraint.** Often you can hand a task off and check back later, so duration seems irrelevant; but many tasks lose value as time passes, and an output delivered after its deadline is a failure even if perfect.

**Reflection failures** are the sneaky ones: the agent believes, and asserts, that it is done. Never accept self-reported completion without an independent check against the goal.

## Planning failures and their metrics

The most common planning failure is tool-use failure. Build a **planning dataset** of (task, tool inventory) tuples. For each task, sample K plans. Compute:

1. Share of generated plans that are valid.
2. Average number of plans needed per task to obtain a valid one.
3. Share of all tool calls that are valid.
4. Frequency of invalid-tool calls.
5. Frequency of valid tools called with invalid parameters.
6. Frequency of valid tools called with incorrect parameter values.

Then look for patterns:
- Which task types fail most, and what is your hypothesis for why?
- Which tools attract the most mistakes? Some tools are intrinsically harder for a model.
- Remedies for a hard tool, in order: better prompting, more examples, finetuning; if all fail, swap the tool for an easier one.

Goal-failure checks need the constraints encoded: destination, budget, dates, deadline. Score whether the final outcome satisfies each.

## Tool failures

Definition: the right tool was chosen but its output is wrong, or the tool needed does not exist.

Practices:
- Tool failures depend on the tool, so **test each tool independently** with its own test cases.
- **Print every tool call and its output** so you can inspect and evaluate them.
- If plans pass through a translator, build a **benchmark for the translator** itself.
- **Missing tools** are diagnosed through domain analysis: if failure rates cluster in a domain, the agent may lack a tool for it. Ask domain experts what tools they would reach for and observe their workflow.

## Efficiency

An agent can be correct and still wasteful. Track:
- Average number of steps per completed task.
- Average cost per completed task.
- Typical duration per action, and which actions are outliers in time or cost.

Compare against a **baseline** (another agent or a human), remembering their cost structures differ: reading 100 web pages is slow for a person but trivial for an agent fetching them concurrently, and the reverse holds for other work.

## Benchmarks and harnesses

- **Berkeley Function Calling Leaderboard**: function-calling accuracy.
- **AgentOps** evaluation harness.
- **TravelPlanner** benchmark: constrained planning, a good test of goal and constraint failures.

Use them for model and framework selection, but your own planning dataset over your own tools is what predicts production behavior.

## Worked example: scoring a planning dataset

Invented numbers: 50 tasks, K = 4 plans each, so 200 plans.
- 130 plans valid, so plan validity = 65%.
- Per task, plans until the first valid one average 1.6 (tasks with no valid plan in 4 tries reported separately: 6 tasks).
- Plans contain 900 tool calls: 45 invalid tools (5.0%), 36 invalid parameter sets (4.0%), 72 wrong values (8.0%); valid calls = 900 - 45 - 36 = 819, or 91.0% (wrong values are well-formed calls but still failures, so correct calls are 747, 83.0%).
- Breakdown shows 40 of the 72 wrong values hit `date_range_lookup`. Action: rewrite its description with explicit formats, add examples; if still failing, split into `start_date` and `end_date` helpers.
- Reflection audit: in 9 runs the agent claimed success with incomplete output. Action: add a deterministic completion checker before the finish action is accepted.
