# Generative AI Intersection

## Two separate concerns

1. Gen AI as a **component inside** the architecture.
2. Gen AI as an **assistant to** the architect.

The chapter's view reflects early 2025; expect this area to move quickly.

## Gen AI as a component

Recommended approach: isolate the model behind abstraction and modularity so that:
- one LLM can be replaced by another quickly (vendor, cost, quality or policy changes),
- guardrails ("rails") can be applied around inputs and outputs,
- outputs from different models can be evaluated ("evals") and compared on samples and metrics.

Observability is required, not optional. Tools such as Langfuse capture traces, samples and scores so engines can be compared.

Invented sketch of the seam:

```python
class TextModel:
    def complete(self, prompt: str) -> str: ...

class GuardedTask:
    def __init__(self, model: TextModel, checks, recorder):
        self.model, self.checks, self.recorder = model, checks, recorder

    def run(self, prompt: str) -> str:
        out = self.model.complete(prompt)
        failures = [c.__name__ for c in self.checks if not c(prompt, out)]
        self.recorder(model=type(self.model).__name__, prompt=prompt,
                      output=out, failures=failures)
        if failures:
            raise ValueError(f"guardrail failed: {failures}")
        return out
```

Worked example (invented, analogous to the chapter's): an insurer uses an LLM to redact personal data from claim notes before adjusters see them. Questions the architecture must let you answer continuously: does it strip too much (losing facts the adjuster needs)? Does it leave identifying data behind? Which model does this best at acceptable cost? Answering requires sampled outputs, labeled evaluation sets, per-model metrics, and the ability to switch models without touching callers.

Checklist:
- Model access behind one interface; no vendor SDK calls scattered across services.
- Input and output guardrails defined and tested.
- An evaluation set with expected outcomes and a regression run before any model swap.
- Tracing of prompts, outputs, latency and cost per call.
- A fallback path (another model or a human) when guardrails fail.

## Gen AI as an architect assistant

What works: specific, deterministic, well-bounded requests (generate a function with clear rules).

Typical architecture prompts people try: find risk areas, propose mitigations, spot antipatterns, choose between options such as orchestration and choreography.

The authors' experience: limited success. Asking a model to choose between styles rarely yields the right answer, because every architecture choice is a trade-off that depends on deep context: business drivers, team, infrastructure, data, enterprise rules and the other intersections in this chapter. Models have knowledge but lack the contextual judgment to decide; supplying all the context often takes longer than solving the problem directly.

Promising uses noted:
- Tools like Thoughtworks Haiven that read an architecture diagram directly and answer questions about it, such as likely bottlenecks.
- Translating a PlantUML diagram or a pseudo-code description of the architecture into executable ArchUnit rules that govern structure.

Operating rules for an agent using this skill:
- Do not issue a context-free verdict on a style or pattern. Lay out the trade-offs against the stated characteristics and intersections, and leave the decision to the architect.
- Before giving any recommendation, ask for missing context on each intersection that bears on it.
- Prefer producing artifacts the architect can verify: risk lists with reasoning, candidate fitness functions, structural test rules generated from a component description.
