# Model Context Protocol (MCP) integration

## Why MCP

Agents increasingly need to read cloud documents, write to business systems, hit internal services and work alongside other agents. Writing a bespoke adapter per data source per agent produces brittle, duplicated glue that is hard to extend. MCP, an open standard started by Anthropic and since adopted by OpenAI, Google DeepMind and Microsoft, gives a single model-agnostic interface: a service exposes it once, and any compliant agent consumes it.

## Roles and mechanics

- MCP server: wraps a resource (object storage, SQL database, CRM, proprietary logic) and exposes methods over JSON-RPC 2.0, advertising each method with input and output schemas.
- MCP client: the agent side. It fetches the server's method catalogue, lets the model reason about which method and arguments to use, wraps the chosen call as a JSON-RPC request, sends it, and returns the structured response to the model. The client needs only the exposed methods, not the server internals.
- Transports: stdio, where the client launches the server as a subprocess (good for local, single-user tools), and streamable HTTP, where the client connects to an already running server at a URL (good for shared, remotely deployed tools).

The chapter's demo has one agent connecting to two servers at once (a subprocess "math" server and an HTTP "weather" server), caching the discovered tool list on first use, picking a tool with a simple keyword heuristic, and declining politely when neither matches. In real systems let the model choose from the catalogue instead of hard-coded routing; keep the polite refusal for out-of-scope requests.

Minimal client configuration shape (illustrative):

```python
servers = {
    "fx":     {"transport": "stdio", "command": "python3", "args": ["fx_server.py"]},
    "ledger": {"transport": "streamable_http", "url": "https://ledger.internal/mcp",
               "headers": {"Authorization": f"Bearer {token}"}},
}
tools = await client_for(servers).list_tools()   # cache; refresh on catalogue change
```

## What MCP buys you

- Decoupling: service implementation is separated from agent logic.
- Write once, reuse everywhere: a new data source or legacy system needs one compliant server, after which every agent that speaks MCP finds and uses it with no extra code.
- Modular, reusable architecture with far less integration code; the chapter notes this is already working in production at major organizations.
- Discoverability: public directories list large numbers of servers, from small utilities to complex stateful services.

## Security gaps you must close yourself

The chapter is explicit that the core specification does not mandate one security model, and several concerns remain open, especially when many agents share an endpoint:

- Authentication: confirm which agent is calling.
- Authorization: only approved agents may call specific methods; role-based access for sensitive data.
- Payload validation: block malicious or injected arguments.
- Audit logging: who called what, with which arguments, and the outcome.

Common mitigations: put an authenticating proxy or gateway in front of servers, apply network policies, scope each server to the minimum set of methods, and treat any third-party server from a directory as untrusted code. Apply the same least-power rules as for any stateful tool.

## Adoption checklist

1. Is the capability needed by more than one agent or team? If not, a local tool may be simpler.
2. Define narrow methods with strict schemas and distinct descriptions (the model still routes on metadata).
3. Choose transport: stdio for local and per-user, HTTP for shared services.
4. Add authentication, per-method authorization, input validation and audit logs.
5. Version the method catalogue; clients should refresh cached tool lists when it changes.
6. Monitor usage per calling agent.

Outlook in the chapter: maturing security practice, standardized method catalogues, and a growing ecosystem of public and private endpoints.
