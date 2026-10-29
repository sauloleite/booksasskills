# Tool definition, invocation loop and tool-call control

## Contents
- The basic invocation loop
- Writing tool metadata
- Tool-choice modes
- Validate, retry, fall back, log
- Pitfalls

## The basic invocation loop

The chapter grounds tool use in LangChain's building blocks (chat model wrapper, human and AI message types, a decorator that derives a schema from a typed function, a bind step and an invoke step). The same loop exists in every framework and raw provider API:

1. Register tool definitions with the model (name, description, JSON schema).
2. Send the conversation.
3. If the reply contains tool calls, dispatch each by name, execute it, and append each result as a tool message.
4. Call the model again so it can compose a final answer from the results.

A single reply can request several calls (for example one multiply and one add for a two-part question); handle them all before the second model call. The important consequence: once a function is bound, the model decides which program runs with which arguments. Bind only tools whose worst plausible misuse you can accept.

```python
def run_turn(model, tools: dict, messages: list):
    reply = model.invoke(messages, tools=[t.spec for t in tools.values()])
    messages.append(reply)
    for call in reply.tool_calls:
        tool = tools.get(call.name)
        result = tool.run(**call.args) if tool else {"error": f"unknown tool {call.name}"}
        messages.append(tool_message(call.id, result))
    return model.invoke(messages) if reply.tool_calls else reply
```

## Writing tool metadata

Name, description and schema are what the model sees; they matter as much as the code.

Names
- Narrow and specific: `convert_timezone`, not `time` or `helper`. A broad name pulls in calls where the tool does not belong.
- Verb plus object; consistent casing across the toolset.

Descriptions
- State what it does, what it does not do, and when to prefer it over similar tools.
- Make each description distinguishable from every other one in the set. Broad or overlapping wording across tools is a near-certain source of mis-selection.
- Mention units, formats and side effects (read-only versus writes).

Schemas
- Type every parameter; mark required fields; use enums for closed sets; forbid extra properties where your provider supports it.
- Define the output shape too, so callers and validators know what success looks like.
- Explicit schemas reduce misfires because the model sees exactly when and how a tool applies.

Before/after example:

- Weak: name `data`, description "Gets data.", parameter `q` (string).
- Strong: name `get_invoice_by_number`, description "Read-only lookup of one invoice by its invoice number (format INV-######). Returns amount, currency, status. Use search_invoices for fuzzy or date-range queries.", parameter `invoice_number` (string, pattern), required.

Run `scripts/lint_tool_definitions.py` on the whole toolset, since overlap is a property of the set, not of one tool.

## Tool-choice modes

Most provider APIs expose a tool-choice setting that moves the system from model-driven to deterministic behaviour.

| Mode | Behaviour | Use when |
|---|---|---|
| auto | Model decides whether to call | General conversational agents |
| any / required | At least one tool call is forced | The answer is invalid without tool output (lookups, calculations, actions) |
| none | Tool calls blocked | Controlled outputs, summarization steps, tests |
| specific tool | One named tool is forced | Fixed pipeline steps needing repeatable flow |

Pick per step, not per agent: a workflow can force `extract_entities` in step one, then run auto afterwards.

## Validate, retry, fall back, log

Agents skip needed calls, emit invalid JSON and hit runtime errors. After every model response check three things: were the right tools called, is the JSON valid, did execution succeed. Then:

1. Validate against the schema (jsonschema, Pydantic or equivalent). Missing fields or malformed structure: send a targeted repair request. Skipped tool: invoke it yourself.
2. Retry smartly: exponential backoff for transient faults; regenerate only the broken fragment rather than restarting the exchange.
3. Fall back when retries are exhausted: a backup model or service, cached data, a clarification question to the user, or a safe default.
4. Log everything: prompts, calls, arguments, validation errors, retries, fallbacks.

The aim is to convert random failures into bounded, predictable behaviour, which the chapter treats as the line between a demo and a production agent.

## Pitfalls

- Toolsets that grow by accretion until three tools describe "search".
- Treating the description as documentation for humans rather than routing instructions for the model.
- Forcing `required` globally, which makes the model invent calls for chit-chat.
- Retrying non-idempotent writes blindly; pair retries with idempotency keys.
- Logging only failures, which hides the slow drift in selection quality.
