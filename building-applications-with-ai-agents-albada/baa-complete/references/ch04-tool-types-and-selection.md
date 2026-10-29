# Tool types and how to choose between them

The chapter sorts agent tools by where they run and who owns them: local (in-process) tools, API-based tools, plug-in tools offered by model platforms, and MCP tools. Stateful and agent-generated tools cut across these categories and have their own files.

## Local tools

Functions defined in the agent's own codebase and deployed with it, usually rule-based.

Strengths
- Precise and predictable, because the logic is explicit.
- Cheap to write and change.
- Ideal for the classic soft spots of language models: arithmetic, unit conversion, time zones, calendar and date math, maps and graph traversal. A calculator tool turns a guess into an exact answer.

Weaknesses (the chapter names three)
- Scalability: sharing them across many agent use cases is awkward, even when packaged as a library.
- Duplication: every agent deployment must ship the library; updating it means coordinated redeploys of every consumer, so in practice teams fork or rewrite the same tool.
- Maintenance: handcrafted logic drifts as requirements change, and each fix usually means redeploying the agent service.

Rule of thumb: start local when one agent owns the capability and it is deterministic. Promote it to an API or MCP server the moment a second team wants it.

## API-based tools

Wrappers around public or private services, used when the work is impossible or too expensive to do in-process.

When they win
- Real-time data (prices, weather, live inventory) where stale answers are wrong; the chapter cites trading and emergency response as cases where freshness is critical.
- Heavy computation offloaded to a specialized service.
- Breadth: translation, finance, search or company knowledge bases, added without retraining a model.
- Internal search: the same pattern works for team- or company-specific data, pairing a retrieval tool with tools that act on what was found.

Design checklist
- Reliability: assume the service will go down; return a fallback or a clear, model-readable error instead of a stack trace.
- Security: HTTPS everywhere and strong authentication, especially for sensitive data.
- Rate limits: track quotas so a chatty agent does not lock itself out.
- Privacy: comply with data-protection law; anonymize or obfuscate user data before it leaves your boundary.
- Robust error handling: network faults and malformed responses must not break the user experience.
- Redundancy: where a capability is critical, keep an alternate provider for when the primary one degrades.

Sketch of a failure-aware wrapper (framework-agnostic):

```python
def fetch_quote(symbol: str) -> dict:
    """Latest traded price for one exchange ticker symbol, e.g. 'MSFT'."""
    for provider in (primary_quotes, backup_quotes):
        try:
            r = provider.get(symbol, timeout=3)
            if r.ok:
                return {"symbol": symbol, "price": r.json()["price"], "source": provider.name}
        except TransientError:
            continue
    return {"symbol": symbol, "error": "quote service unavailable; ask user to retry later"}
```

## Plug-in tools

Prebuilt modules from model vendors or open-source communities that attach to the model execution layer with minimal custom work.

Platform landscape as the chapter describes it (2025)
- OpenAI: its plug-in ecosystem is confined to ChatGPT itself and cannot be reached through the developer API; replicating that behaviour in your app means building your own function-calling layer.
- Anthropic: tool use is exposed directly through the Messages API (also on Bedrock and Vertex AI), with both custom and Anthropic-provided tools.
- Google Gemini: function calling via Vertex AI; you declare functions up front and handle the returned structured arguments in your code.
- Microsoft Phi: served through Azure AI Foundry; not marketed as plug-ins but tightly coupled to Azure services, so outputs flow straight into Azure workflows.
- Open source: libraries such as Hugging Face Transformers supply ready NLP components; directories such as Glama.ai and mcp.so catalogue MCP servers.

Core trade-off: integration speed versus customizability. Plug-ins are general-purpose and may miss domain nuance; bespoke tools (local or remote) fit exactly but cost build and maintenance time. A common pattern is to mix them: plug-ins for commodity capabilities, custom tools for the differentiating ones.

Example domains the chapter sketches: support (ticket handling, intent and sentiment), healthcare (image analysis, triage, record extraction, vector search for grounding), finance (anomaly detection, trend analysis, portfolio work), education (personalized learning, grading, recommendations).

Outlook: catalogues are growing fast; the chapter expects standardization and interoperability across platforms and more configurable plug-ins that narrow the gap with bespoke tools.

## Selection matrix

| Situation | Prefer |
|---|---|
| Deterministic computation the model is bad at, one agent owns it | Local tool |
| Needs live or external data, heavy compute, or acts in another system | API tool |
| Commodity capability already offered by your model platform | Plug-in tool |
| Same capability needed by several agents or teams | MCP server (or shared API) |
| Writes to or deletes persistent data | Any of the above, narrowed per the stateful-tool checklist |
| Unknown API, one-off task, no time to hand-build | Model-generated wrapper, reviewed and persisted |

Worked example: an insurance claims agent needs (a) premium arithmetic, (b) the policy record, (c) document OCR, (d) currency conversion shared with three other agents. Choose (a) local, (b) a narrow read-only API tool `get_policy_by_id`, (c) a platform plug-in or vendor OCR API, (d) an MCP server so the other agents reuse it without copying code.

See also: mcp-integration.md, stateful-tool-safety.md.
