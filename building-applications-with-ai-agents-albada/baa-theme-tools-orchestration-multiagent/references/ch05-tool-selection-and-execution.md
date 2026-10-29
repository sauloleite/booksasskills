# Tool selection and tool execution

## Contents
- Strategy comparison
- Standard tool selection
- Writing tool descriptions
- Semantic tool selection
- Hierarchical tool selection
- Parametrization and execution
- Evaluating selection quality
- Pitfalls

Tool selection is the base layer of planning: before an agent can sequence tools it must reliably pick the right one. The tools themselves are assumed to exist already (their design is the subject of the previous chapter).

## Strategy comparison

| Strategy | What the model sees | Extra infrastructure | Sequential selection steps | Main failure mode | Pick when |
|---|---|---|---|---|---|
| Standard | every tool | none | 1 model call | catalog too big, descriptions blur | a small catalog of clearly distinct tools |
| Semantic | top-k retrieved tools | embedding model plus vector index | 1 retrieval, 1 model call | right tool not retrieved, or embedding collisions | most systems (author's default) |
| Hierarchical | group list, then one group's tools | group taxonomy to maintain | 2 or more | wrong group chosen; more latency | a very large catalog with many look-alike tools |

## Standard tool selection

- Pass each tool's name, schema and description to the model and ask for the best fit; map the model's answer back to the closest registered tool.
- Latency cost: an extra model call, often seconds.
- In-context learning helps: add a few example query-to-tool mappings to lift accuracy without fine-tuning.
- Scales fine for small toolsets; past that, description engineering becomes the deciding factor.

## Writing tool descriptions

Selection accuracy depends mostly on how each capability is described. Checklist:

1. **Name**: specific verb plus object (`convert_currency`, not `handle_money`).
2. **One-line purpose** stating what makes this tool different from its neighbors.
3. **Example invocation** with realistic inputs and the shape of the output.
4. **Input constraints**: types, units, allowed ranges or enums. Constraints let the model rule a tool out.
5. **Iterate**: run representative prompts, look at wrong picks, tighten the descriptions that collided, re-run.

Watch for overlap: as tools accumulate, descriptions start to sound alike, and that overlap is a frequent source of misselection. Typical additions that blur boundaries are a general computation tool (models are weak at arithmetic and formula evaluation, so such a tool is valuable), a workflow-automation webhook, and a team-notification tool used for human-in-the-loop alerts.

Invented before/after:

```
before: name=search  "Searches for things."
after:  name=search_order_history
        "Look up a customer's past orders by customer_id (string, 'C' + 6 digits).
         Returns a JSON list of {order_id, date, total}. Example:
         search_order_history('C004211') -> [{'order_id': 'O9', ...}]"
```

## Semantic tool selection

Setup, done once per catalog version:
1. Embed each tool's name plus description with an encoder model (commercial embedding APIs or open models such as ModernBERT).
2. Store vectors in a lightweight vector index.

Runtime:
1. Embed the current context with the same encoder.
2. Retrieve the top-k tools by similarity.
3. Give only those to the model, which decides whether to call one and fills its parameters.
4. Execute and use the result to compose the reply.

Guidance:
- The author recommends this as the common default: usually faster than standard selection, performant, reasonably scalable.
- Re-embed whenever a description changes; stale vectors silently degrade selection.
- Normalize vectors if you want cosine similarity from an L2 index.
- Tune k: too small and the right tool is not in the candidate set; too large and you are back to the standard-selection problem. Track candidate recall separately from final pick accuracy.
- Collisions (two tools with near-identical embeddings) are the main accuracy risk; fix with sharper descriptions or by moving to hierarchical selection.

## Hierarchical tool selection

- Organize tools into groups (for example computation, automation, communication), each with its own description.
- Stage 1 selects a group; stage 2 searches only within that group. Either stage can be generative or embedding-based.
- Splitting one hard choice into two easier ones often raises overall accuracy.
- Costs: slower, expensive to parallelize, and the taxonomy takes ongoing effort. Not worth it unless the catalog is large.
- Handle the "no group fits" and "no tool in group fits" outcomes explicitly instead of guessing.

Sketch:

```python
def pick_tool(query, groups, choose):
    # choose(query, options) -> option name or None (LLM or embedding based)
    g = choose(query, {name: grp["description"] for name, grp in groups.items()})
    if g is None:
        return None, "no_group"
    tools = groups[g]["tools"]
    t = choose(query, {name: spec["description"] for name, spec in tools.items()})
    return (g, t) if t else (g, "no_tool")
```

## Parametrization and execution

- Parametrization: the model fills the tool's declared parameters with correctly typed values. Supply the agent's current state and progress in the prompt so values reflect what has already happened.
- Inject environmental facts tools need: current time, user location, locale, tenant.
- Validate before running: a basic parser checks types and formats; on failure, return the error to the model and ask it to correct the call.
- Execution may be local or a remote API; external data sources and computation materially improve accuracy and usefulness.
- Set timeouts and retry policies per use case, matching its latency and reliability requirements.

```python
def call_with_validation(model_fill, validate, run, max_fixes=2):
    args = model_fill(feedback=None)
    for _ in range(max_fixes + 1):
        err = validate(args)          # e.g. type, range, enum checks
        if err is None:
            return run(args)          # wrap with timeout and retry policy
        args = model_fill(feedback=err)
    raise ValueError(f"invalid arguments after {max_fixes} corrections: {err}")
```

## Evaluating selection quality

- Build a labeled set: query, expected tool(s), and for semantic pipelines the retrieved candidates.
- Compare strategies on the same set: exact-match accuracy, precision and recall of chosen tools, candidate recall at k, latency.
- Inspect the most frequent wrong picks; each recurring pair is a description collision to fix.
- `scripts/tool_selection_eval.py` computes all of these from JSONL.

## Pitfalls

- Vague or overlapping tool names and descriptions.
- Measuring only end-to-end success and missing that the retriever never surfaced the right tool.
- Adopting hierarchical selection for a 10-tool catalog.
- Skipping argument validation and letting malformed calls hit production APIs.
- One global timeout for tools with very different latency profiles.
