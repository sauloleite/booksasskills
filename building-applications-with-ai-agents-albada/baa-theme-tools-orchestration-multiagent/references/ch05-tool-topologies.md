# Tool topologies

## Contents
- Why topologies
- Ladder of complexity
- Single tool execution
- Parallel tool execution
- Chains
- Graphs
- Graph design playbook
- Pitfalls

## Why topologies

Classic software hard-codes control flow. With agents you build the tools and define the space of allowed arrangements (the topology), and the agent composes the actual sequence at runtime from the task and context. Most production chatbots today run a single tool with no planning, which is cheaper and faster; a team building its first agent can reasonably stop there if it meets requirements.

## Ladder of complexity

| Topology | Shape | Planning needed | Cost profile | Use when |
|---|---|---|---|---|
| Single | one call | choose and parameterize one tool | lowest | one action answers the request |
| Parallel | fan-out, then synthesize | choose a set of independent tools | similar latency to single, more calls | several independent sources feed one answer |
| Chain | linear sequence | order dependent steps | grows with length | strictly linear dependencies, no fan-out |
| Graph | branches, conditions, merges | routing logic per node | most model calls, most failure modes | must branch and later consolidate |

Climb one rung at a time, and only when the lower rung demonstrably fails.

## Single tool execution

Flow: query reaches the model, the model selects and parameterizes one tool, the tool returns (often JSON), the model writes the reply from that output. Example: "What is the weather in Lisbon?" leads to a weather tool call and a natural-language summary of temperature and conditions. This minimal plan is the base every other topology extends.

## Parallel tool execution

When one input needs several independent actions (for instance assembling a patient record from multiple systems, or answering a support ticket using customer profile, order history, service logs, similar past tickets and policy text):

1. The unknown is how many tools to run. Retrieve a ceiling of candidates (say 5) with semantic selection.
2. Ask the model to keep only the ones the task needs (5 or fewer). Alternative: call the model repeatedly, telling it what is already selected, until it adds nothing.
3. Parameterize each selected tool independently and run them concurrently.
4. After all complete, pass every result to the model for one synthesized answer.

Benefit: broader evidence in a single step with latency close to the slowest tool rather than the sum.

```python
import concurrent.futures as cf

def fan_out(calls, timeout_s=10):
    # calls: {name: zero-arg callable}; returns {name: result or error string}
    out = {}
    with cf.ThreadPoolExecutor(max_workers=len(calls) or 1) as pool:
        futs = {pool.submit(fn): name for name, fn in calls.items()}
        for f in cf.as_completed(futs, timeout=timeout_s):
            name = futs[f]
            try:
                out[name] = f.result()
            except Exception as e:      # keep partial results for synthesis
                out[name] = f"ERROR: {e}"
    return out
```

## Chains

- A sequence where each step runs only after the previous one succeeds. Planning means fixing the order so each output feeds the next input.
- Natural for step-by-step and linear workflows (fetch, transform, validate, write).
- LangChain's expression language (LCEL) composes Runnables with a pipe operator; every composed chain exposes the same invoke, batch and stream interface, which cuts boilerplate compared with older Chain classes.
- The agentic chain loop: the model reasons, calls a tool against the environment, receives the observation, and reasons again until finished.
- Set a maximum chain length; errors accumulate with each link.
- Best trade-off when tools depend on each other but the task does not fan out into branching subtasks.

## Graphs

- Nodes are tool invocations or logical steps. Edges define allowed transitions; conditional edges encode business rules, and consolidation edges let parallel branches merge into a shared node.
- More expressive than chains or trees for flows with several decision points, such as customer support.
- Invented example: a classifier node labels a request "shipping" or "account"; shipping routes to track_parcel or reissue_label, account routes to unlock_account or update_email; all four handlers feed a compose_reply node, which leads to END.
- Router functions inspect the evolving state and return the next node name; a mapping restricts runtime transitions to valid successors, so invalid paths are blocked before any tool runs.
- Costs: substantially more model calls than chains (latency and money); new error classes such as cycles, unreachable nodes, dead ends and conflicting state merges.

## Graph design playbook

1. Confirm you need a graph: the flow must both branch and later merge. If it is strictly linear, use a chain; if it only branches, a tree may do.
2. Sketch on paper: one box per node labeled with its tool or step, arrows for permitted transitions, marks where branches rejoin.
3. Encode as data and validate structure: every node reachable from START, every node can reach END, no unintended cycles, branching factor and depth within caps. `scripts/topology_check.py` does this.
4. Implement incrementally, one branch at a time.
5. Unit-test every router with inputs covering each outgoing edge and edge cases (ambiguous labels, missing state keys).
6. Pass a runtime depth limit to the executor as a safety net.
7. Use the framework's tracing (LangGraph has it built in) to confirm real executions terminate.
8. Define merge rules for state keys written by multiple branches.

## Pitfalls

- Reaching for a graph because it is flexible; each node or edge multiplies execution paths and failure modes.
- Unbounded chains or graphs with no depth or branching cap.
- Routers based on fragile keyword checks without tests.
- Parallel fan-out without timeouts, so one slow source blocks the answer.
- Discarding partial results when one parallel tool fails instead of letting synthesis note the gap.
