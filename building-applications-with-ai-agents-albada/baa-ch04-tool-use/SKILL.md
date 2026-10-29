---
name: baa-ch04-tool-use
description: Guidance for designing, choosing, securing and operating the tools an AI agent calls, based on Chapter 4 ("Tool Use") of Michael Albada's "Building Applications with AI Agents" (O'Reilly, 2025). Covers local, API, plug-in and MCP tools, tool metadata, stateful-tool safety, agent-generated tools and tool-choice/fallback control. Use when defining or reviewing tool schemas, deciding where a tool should live, exposing a database or API to an agent, adopting MCP, letting an agent write code, or hardening tool-call failures.
---

# Tool Use (Albada, Chapter 4)

Tools are how an agent acts on the world instead of only talking about it. This skill turns the chapter into decisions: which kind of tool to build (local function, external API wrapper, provider plug-in, MCP server, or agent-generated code), how to describe it so the model picks it correctly, how to bound its power when it touches persistent state, and how to control and recover tool calls in production. The chapter's stance: curating the agent's toolkit is one of the highest-leverage things a builder does, and binding a tool to a model is a responsibility, because the model will choose when and with what arguments to run it.

## Key decision rules

1. **Metadata is part of the tool.** The model routes on name, description and schema. Use narrow, specific names; descriptions that say what is distinct about the tool versus its neighbours; strict typed input and output schemas. Overlapping descriptions across tools reliably degrade selection.
2. **Hand-write local tools for model weak spots.** Arithmetic, unit and time-zone conversion, date/calendar math, and map or graph operations belong in deterministic code co-deployed with the agent.
3. **Know the local-tool tax.** Local tools scale poorly across teams: each agent service must ship the library, every change needs coordinated redeploys, and teams end up reimplementing the same tool. When several agents need a capability, move it behind an API or MCP server.
4. **Use API tools for fresh data, heavy compute and external actions**, and design them for failure: fallbacks or clear errors when the service is down, HTTPS plus strong auth, rate-limit awareness, privacy-law compliance (anonymize or obfuscate user data), and a second provider where availability matters.
5. **Plug-in tools trade customizability for speed.** Provider-native tool catalogs integrate at the model execution layer with little effort but are general-purpose. Pick them for commodity capabilities; build bespoke tools when domain nuance matters. Note that some vendor plug-in ecosystems exist only inside the vendor's consumer app, not its API.
6. **Adopt MCP to make a tool reusable.** Implement a capability once as an MCP server (JSON-RPC 2.0, advertised method catalog with schemas) and every agent that speaks MCP can find and use it. Do not assume the protocol secures you: add your own authentication, per-method authorization, payload validation and audit logging, often through a proxy or network policy.
7. **Least power for stateful tools.** Never expose "run arbitrary SQL" or similar. Register one narrow, tested operation per tool; give read-only agents no write or delete tools; run them under a minimally privileged account.
8. **If free-form queries are unavoidable**, reject statements containing destructive patterns (DROP, ALTER and similar), always use bound parameters or prepared statements, log every invocation, and alert on anomalies such as large deletions or schema changes.
9. **Agent-generated tools need a human gate.** Let a model draft wrappers from an OpenAPI spec, run them in a sandbox, and self-correct from errors, but require tests, schema checks and human review before CI/CD. Regenerate with the same loop when the API changes.
10. **Prefer persisted tools over real-time code generation** when repeatability, auditability or compliance matter. Code regenerated per request is non-deterministic across runs and model updates, raises security and quality risk, and can burn compute; if you allow it, sandbox it and put resource guardrails on it.
11. **Set tool_choice deliberately.** auto for general flows; any/required when the answer is worthless without tool output; none for controlled or test runs; pin a named tool for fixed, repeatable steps.
12. **Wrap every model turn in validate, retry, fall back, log.** Schema-validate arguments and outputs, auto-trigger skipped tools, ask the model to repair bad JSON, back off exponentially on transient errors, regenerate only the broken part, then fall back to a backup model or service, cached data, a clarification question or a safe default.

## Default workflow

1. List the capabilities the agent needs; for each, classify: deterministic computation, external or real-time data, external action, persistent-state mutation.
2. Choose the tool type with the selection matrix in [tool-types-and-selection.md](references/tool-types-and-selection.md).
3. Write the definition (name, description, schema), then run the linter in `scripts/` against all definitions together to catch generic names, vague or overlapping descriptions and loose schemas.
4. For anything touching state, apply the least-power checklist before registration.
5. Decide the tool_choice mode per step and implement the validate/retry/fallback/log wrapper.
6. Log every call; review the logs for misfires, skipped calls and anomalous writes, and tighten descriptions or scope.

## References

- [tool-types-and-selection.md](references/tool-types-and-selection.md): read when deciding between a local function, an API wrapper, a provider plug-in or an MCP server, or when designing API tools for reliability.
- [tool-definition-and-invocation.md](references/tool-definition-and-invocation.md): read when writing or reviewing tool names, descriptions and schemas, wiring the bind/call/append loop, choosing a tool_choice mode, or building retry and fallback logic.
- [mcp-integration.md](references/mcp-integration.md): read when exposing a service over MCP, connecting an agent to stdio or HTTP MCP servers, or reviewing MCP security.
- [stateful-tool-safety.md](references/stateful-tool-safety.md): read before giving an agent access to databases, files or any system whose data persists, or when reviewing an incident caused by a tool call.
- [automated-tool-development.md](references/automated-tool-development.md): read when having a model generate tool wrappers from specs, or when deciding whether an agent may write and execute code at runtime.
- [source-map.md](references/source-map.md): chapter section headings mapped to the reference file covering each.

## Scripts

- `scripts/lint_tool_definitions.py`: static review of tool definitions in JSON (OpenAI-style, Anthropic-style or MCP-style). Run it to flag generic or badly formatted names, missing or thin descriptions, near-duplicate descriptions between tools, untyped or unconstrained parameters, missing `required` lists, high-power free-form parameters (sql, code, command) and destructive operations.

```bash
python3 scripts/lint_tool_definitions.py tools.json
python3 scripts/lint_tool_definitions.py tools.json --read-only --overlap-threshold 0.5 --json
```

`--read-only` escalates write/delete tools to errors (for agents that should only read). Exit code is 1 when any error is found, so it can gate CI.
