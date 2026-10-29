# Models and Frameworks for Agentic Systems

## Contents
- Why pretrained models changed the build path
- Capabilities that make a model usable as an agent core
- Model selection playbook
- Routing and the multimodel future
- Framework selection
- Pitfalls

## Why pretrained models changed the build path

Classic ML projects were bounded by dataset size and quality, and most practitioner time went into collecting and cleaning data rather than training. Large pretrained generative models flip this: a single hosted model handles many tasks with no extra training, so a working ML-backed feature can start as one API call instead of a hire, a data collection effort and a model deployment. Practical consequence: prototype against a hosted frontier model first, and only invest in data collection or training once a measured gap justifies it.

## Capabilities that make a model usable as an agent core

Base language skills: understanding natural input, holding context across a long interaction, and emitting structured content (text, code, JSON).

What turns those into agent behavior once an orchestrator is attached:
- Interpreting ambiguous situations and deciding without exhaustive rules
- Calling tools to fetch data or change external systems
- Planning and carrying out multistep sequences
- Condensing long documents into key findings (legal, research, curation)
- Making sense of unstructured material such as emails, logs, reports
- Writing and running code, including unit tests
- Absorbing repetitive service and admin work so people handle the nuanced cases
- Analyzing images, audio and video at scale

Use this list as a capability checklist when scoping: for each step of the target task, name which capability it depends on, then test the candidate model on exactly that capability. Static ML models cannot cover the dynamic, multi-capability cases this list enables.

## Model selection playbook

There is no universally right model. The factors to balance: task complexity, required modalities, latency and cost budgets, and integration requirements.

1. **Start with a current frontier general-purpose model from a major provider.** It works well with little customization and goes surprisingly far. On the HELM Core leaderboard of August 2025, the ten best models clustered tightly (mean scores roughly 0.77 to 0.82 across five benchmarks: GPQA, MMLU-Pro, Omni-MATH, IFEval and WildBench), with GPT-5 mini on top at 0.819. Lesson: among frontier models the gap is small, so pick on fit, cost and integration rather than leaderboard rank.
2. **Do not over-optimize early.** Large effort spent on model choice often buys marginal gains. Only optimize when scale or hard constraints demand it.
3. **Then try smaller models for well-defined, low-latency or cost-sensitive tasks.** They frequently come close to the large model at a fraction of the cost. Distillation, quantization and synthetic data are why compact models now inherit much of the bigger models' capability.
4. **Improve with fine-tuning or retrieval** once you have evaluation data, to raise quality and cut cost.
5. **Consider open-weight models** (Llama, Mistral, Gemma, Qwen, gpt-oss) when you need local deployment, fine-tuning freedom or data control.
6. **Design for model flexibility now.** Keep the model behind an interface, avoid vendor-specific prompt formats, and keep an evaluation set so a swap is a measured decision rather than a gamble.

## Routing and the multimodel future

A growing pattern is automated model selection at request time: send easy queries to a fast, cheap small model and reserve the large model for hard reasoning. Treat multimodel systems as the expected end state.

Minimal routing skeleton (illustrative, provider-agnostic):

```python
def route(request, classify, small_model, large_model, threshold=0.7):
    # classify returns an estimated difficulty in [0, 1]
    difficulty = classify(request)
    model = small_model if difficulty < threshold else large_model
    result = model(request)
    if result.get("low_confidence") and model is small_model:
        result = large_model(request)   # escalate on doubt
    return result
```

Checklist for a router: an offline eval showing the small model is acceptable on the routed slice, logging of which model served each request, an escalation path, and periodic re-tuning of the threshold as models change.

## Framework selection

Frameworks differ in how they handle tool integration, memory, planning, orchestration, learning from experience and multiagent coordination. Snapshot of the four leading options as characterized in the chapter:

- **LangGraph**: orchestration as a directed graph where nodes are units of logic (often model calls) and edges route state, cycles allowed. Good ergonomics, native async and retries. You write your own advanced planning and memory; multiagent support is thinner. Fit: robust single-agent or light multiagent systems where you want explicit, inspectable control flow. The book's main framework.
- **AutoGen**: strong multiagent orchestration with dynamic roles and message passing between agents. Heavier and more opinionated about interaction patterns, overkill for simple cases. Fit: systems built on agent dialogue such as manager-worker or self-reflection loops.
- **CrewAI**: quick to learn, fast prototyping, intuitive crew and task abstractions. Less control over orchestration internals and less mature for complex flows. Fit: getting practical human-facing assistants or support agents running fast.
- **OpenAI Agents SDK**: tight integration with OpenAI tooling, easy and secure function calling, memory primitives and tool routing. Coupled to OpenAI infrastructure, less portable. Fit: teams already on the OpenAI API wanting tool-using agents with little scaffolding.

Decision rules:
- Prototype quickly: CrewAI or OpenAI Agents SDK.
- Production scale with fine control: LangGraph or AutoGen (AutoGen when agent-to-agent conversation is central).
- A framework is optional. Building directly on provider APIs is a legitimate choice, especially for small agents or when you want zero abstraction overhead.
- Expect churn; choose based on current needs and keep business logic and tools separable from framework glue so you can migrate.

## Pitfalls

- Choosing by leaderboard rank alone when the top models are within a few points.
- Running every request on the largest model when most traffic is simple.
- Hardcoding one provider's prompt format or SDK types throughout the codebase.
- Adopting a heavyweight multiagent framework for a single-agent task.
- Locking orchestration logic into a prototyping framework that will not support production control needs.

See also: principles-and-organization.md (modularity and future-proofing).
