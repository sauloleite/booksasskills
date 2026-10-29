---
name: baa-ch01-introduction-to-agents
description: Scoping guidance for agentic systems, based on Chapter 1 of Michael Albada's "Building Applications with AI Agents". Covers the real-agent test, choosing code vs workflow vs RAG vs agent, async "work arrives prepared" design, agent types and reference use cases, model selection and routing, LangGraph/AutoGen/CrewAI/OpenAI Agents SDK trade-offs, five build principles, and organizing teams. Use when someone asks whether a problem needs an agent, which model or framework to start with, how to make an agent scalable and maintainable, or how to govern agent experiments.
---

# Building Applications with AI Agents, Ch. 1: Introduction to Agents

This skill helps an agent advise at the start of an agentic project: deciding whether the problem needs an agent at all, which tier of solution fits, which model and framework to start with, which principles the design must satisfy, and how an organization should manage many parallel agent experiments. It distills the opening chapter of Albada's book, which is a map; deep material on tools, memory, orchestration, evaluation and multiagent coordination belongs to later chapters.

## Key decision rules

Apply these even without opening a reference.

**Is it really an agent?**
1. Agency is a spectrum. A system is an agent only if it makes real run-time decisions (which tool, which path, which next step); a fixed script or scripted flow is not, whatever it is called.
2. Separate the agent (the deciding model) from the agentic system (tools, memory, model, orchestration, infrastructure). Budget most effort for the system.

**Choose the lowest tier that works**
3. Score four factors first: input variability, reasoning complexity, performance or compliance constraints, maintenance burden.
4. Plain code when inputs are fully predictable, outputs can be specified ahead, the domain is static, latency must be milliseconds, or regulation demands deterministic auditable logic.
5. Deterministic workflow when every branch can be listed up front and you need explicit retries, approval pauses and auditable error paths (Airflow, Step Functions, structured scripts).
6. Chatbot or RAG when the need is question answering over a corpus with little need for API calls or decision orchestration. RAG surfaces information; it does not choose follow-up actions.
7. Agent only when inputs are open-ended or novel AND the task needs adaptive multistep planning, parallel subtask orchestration or learning from feedback. That need must justify higher latency, compute and governance cost.
8. Gate with five questions: unpredictable inputs? plans that adapt to intermediate results? must it act, not just retrieve? should it self-improve? can we afford model latency and upkeep?

**Design for asynchronous value**
9. Prefer patterns where the agent works ahead and the human receives prepared work (drafted replies, prefilled invoices, tickets with candidate fixes and tests, enriched security alerts). Design for humans as reviewers and approvers, not executors.
10. Concurrent fan-out (many lookups at once) is a strong signal for an agent over a sequential workflow.

**Models**
11. Start with the latest general-purpose frontier model; it goes far with little tuning. Top models score within a few points of each other, so do not chase leaderboard rank.
12. Optimize model choice only when scale or constraints demand it. Then try smaller models for well-defined, low-latency or cost-sensitive tasks, and add fine-tuning or retrieval.
13. Expect a multimodel future: route easy requests to small models and hard ones to large models, and keep the model behind an interface.

**Frameworks**
14. Fast prototype: CrewAI or OpenAI Agents SDK. Production control: LangGraph (explicit graph flow, single or light multiagent) or AutoGen (conversation-centric multiagent). Direct provider APIs are a valid no-framework option.

**Build principles (each with its failure mode)**
15. Scalability: autoscale so a 100x ticket spike does not stall the agent.
16. Modularity: tools behind clear interfaces so changing one does not redeploy the agent.
17. Continuous learning: feedback loops so mistakes are not repeated.
18. Resilience: timeouts, retries, fallbacks and redundancy so one failed call does not crash the run.
19. Future-proofing: open standards and no vendor-specific prompt formats so models can be swapped.

**Organization**
20. Encourage free exploration early; converge as patterns prove out using one standard per large group (department or function), not one company-wide mandate.
21. Avoid lock-in with open standards such as OpenAPI and modular design; share lessons from failures as well as wins; keep governance to light guiding principles; reassess the balance regularly.

## Default workflow

1. Restate the task and apply the real-agent test to any existing "agent" in scope.
2. Score the four factors and answer the five gating questions; pick the lowest viable tier and note which sub-parts can drop to cheaper tiers.
3. If an agent is justified, classify its type, pick the nearest reference use case, and list read vs write actions with human approval points.
4. Look for asynchronous "prepared work" opportunities and design the review UX.
5. Start with a frontier general-purpose model; define an evaluation set; plan later experiments with smaller models, routing, fine-tuning or retrieval.
6. Choose a framework (or none) based on prototype vs production needs and multiagent requirements.
7. Run the five-principle design review and record each gap with an owner.
8. For organizations, place the effort in the explore or converge phase and set up the sharing and lightweight governance artifacts.

## References

- [references/solution-tier-selection.md](references/solution-tier-selection.md): read when deciding between code, workflow, RAG and agent, defining what counts as an agent, designing asynchronous prepared-work flows, or writing a tier decision record.
- [references/models-and-frameworks.md](references/models-and-frameworks.md): read when choosing a model, planning small-model routing, judging benchmark gaps, mapping needed model capabilities, or picking among LangGraph, AutoGen, CrewAI, OpenAI Agents SDK or no framework.
- [references/agent-types-and-use-cases.md](references/agent-types-and-use-cases.md): read when classifying a request into an agent type (including browser, voice, video) or borrowing actions and risks from the book's seven reference agents.
- [references/principles-and-organization.md](references/principles-and-organization.md): read when reviewing an agent design for scalability, modularity, learning, resilience and future-proofing, or advising how teams should explore, standardize and govern agent work.
- [references/source-map.md](references/source-map.md): read to find which reference covers a given chapter section.

## Scripts

None. The chapter offers qualitative decision criteria, not calculations.
