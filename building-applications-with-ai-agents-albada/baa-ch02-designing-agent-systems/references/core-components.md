# Core Components: Model, Tools, Memory, Orchestration

## Contents
- Model selection (complexity, modality, openness, pretrained vs custom, cost and latency, benchmarks, hardware)
- Tools (local, API-based, MCP; modularity)
- Memory (short-term, long-term, management and retrieval)
- Orchestration
- Pitfalls

## Model selection

The model sets how inputs are understood and outputs produced, and it drives performance, scalability, latency and cost. Decide along five axes, starting with task complexity.

**1. Task complexity (start here)**
- Open-ended, ambiguous, multistep work (personal assistants, research agents, enterprise systems facing unpredictable queries): large frontier models. Expect high compute, cloud dependence and more latency.
- Well-defined, repetitive work (support triage, retrieval, labeling): small models such as distilled encoders or compact LLMs. They run locally, answer fast and cost little. When latency or hardware is the binding constraint, the small model can be the better system even if it is the weaker model.

**2. Modality**
- Use a multimodal model only when decisions really combine images, audio or structured data with text (healthcare, robotics, support with photos).
- Otherwise prefer text-only: simpler, faster inference.

**3. Openness**
- Open-weight models (Llama, DeepSeek class): full inspection, fine-tuning, private hosting, no license fees. Choose for privacy-sensitive, regulated or highly domain-specific work. Price: you own the engineering and serving.
- Proprietary API models: managed infrastructure and monitoring, fastest path to production. Price: limited customization and spend that grows with usage.

**4. Pretrained vs custom-trained**
- Pretrained general models plus prompting or light fine-tuning: fine for general language tasks and prototypes where domain precision is not critical.
- Custom training on curated domain data: worth it in specialized, high-stakes fields (medicine, law, technical support) where accuracy and trust matter.

**5. Cost and latency (often decisive)**
- If a large model's cost or delay is unacceptable, use a smaller or compressed model.
- Hybrid tiering: strong model for hard queries, light model for routine ones.
- Dynamic routing: score each request on complexity or urgency and send it to the cheapest model that can handle it.

### Reading benchmarks and prices

- General benchmarks (MMLU, reported through Stanford CRFM's HELM) give a shared ruler but imperfect task alignment. Larger models tend to score higher, with exceptions; top scores need far more compute, which also means decent quality is available very cheaply.
- Price and benchmark score are not tightly correlated. At publication, the cheapest hosted large model in the comparison (Llama 3.1 405B) cost about $0.20 per million input and $0.60 per million output tokens, and some premium models cost tens of times more for similar MMLU.
- Rule: run candidates on your own task set and choose by price per unit of task performance. `scripts/model_cost_compare.py` computes this.

### Hardware rules of thumb (open weights)

- Full-precision memory is roughly 2 to 2.5 GB of VRAM per billion parameters (16-bit weights plus overhead).
- Up to about 14B parameters fits one 24 GB consumer GPU (RTX 3090 class). Above that, plan for server GPUs (A100 40 or 80 GB); 70B class needs several.
- Frontier-size models need a dozen or more GPUs and live in data centers; providers bill per input and output token, which removes serving work from your team.
- Small open models improve quickly; they will not solve your hardest problems but cover routine ones cheaply. For the support example, a small fast model suffices; recommendations or sentiment-driven escalation could justify a bigger one.

Treat model choice as recurring: revisit it as capabilities, user needs and infrastructure change.

## Tools

Tools are the agent's action surface; its usefulness is bounded by their range and quality. Design them for the tasks and conditions the agent will meet.

| Category | What it is | Examples | Notes |
|---|---|---|---|
| Local | Internal logic, no external dependency | Math, local DB reads, rule-based approve/deny | Deterministic, cheap, easy to test |
| API-based | Calls to external services | Weather, prices, social feeds, backend APIs | Real-time data; add timeouts, retries, auth |
| MCP | Standard protocol for supplying context and capabilities | User profile, history, world state, task metadata | Chapter frames it as feeding live context into reasoning to cut redundant calls and keep state |

Note: in current practice an MCP server exposes tools, resources and prompts through one standard interface, so it is both a context channel and a tool transport.

**Modularity rule**: build every tool as a self-contained, replaceable unit with a clear schema. You should be able to add dispute resolution or advanced troubleshooting later without touching the agent's core loop.

## Memory

| Type | Holds | Typical implementation | Example |
|---|---|---|---|
| Short-term | Current task or conversation state | Rolling (sliding) context window; old turns dropped | Support agent recalls earlier questions in the same session |
| Long-term | Knowledge and experience across sessions | Databases, knowledge graphs, fine-tuned weights | Health monitor tracks vitals over months to spot trends |

Management and retrieval checklist:
- Organize and index stored data for fast lookup.
- Filter relevant from irrelevant before it reaches the prompt.
- Forget deliberately: expire stale or useless entries.
- Weight recency where preferences drift (a recommender should favor recent purchases over old ones).

## Orchestration

Orchestration composes, schedules and supervises skills so each step feeds the next toward a goal. It weighs candidate sequences of tool calls, predicts their outcomes and picks the most promising path (route planning under traffic and time windows; multistage data pipelines).

Operating rules:
- Monitor both progress and the environment; pause or reroute when inputs, priorities or resources change.
- Plan incrementally: run a few steps, re-evaluate, update the rest of the plan.
- In conversation, confirm each subtask result before planning the next.
- Without an orchestration layer, strong tools can work against each other or stall.

## Pitfalls

- Defaulting to the biggest model for a narrow, repetitive task.
- Choosing by leaderboard rank or price alone instead of task-level evaluation.
- Adding multimodality "just in case".
- Business rules living only in prompts instead of in tools.
- Monolithic tools that cannot be swapped.
- Memory that only grows, never forgets, and ignores recency.
