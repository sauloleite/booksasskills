# Automated tool development

Models can write code, so they can write tools: either ahead of time (model as toolmaker, output reviewed and persisted) or on the fly during a task (real-time code generation). The chapter's conclusion also lists imitation learning and reinforcement learning as routes by which agents refine their own abilities, without developing them further here.

## Foundation models as tool makers (offline generation)

Playbook
1. Feed the model an OpenAPI spec, SDK samples or example inputs.
2. Ask for narrow wrappers, helpers or higher-level atomic operations, one per tool.
3. Execute drafts in a sandbox against the real or a mock service.
4. Feed failures back (for example a 400 response with the body) and let the model critique and revise.
5. Stop after a few iterations when tests pass; then a human reviews for security, edge cases and business-logic fit.
6. Merge through normal CI/CD.
7. When the API changes, repeat the draft, test, fix cycle to bring wrappers back in sync.

Where it pays off: a sprawling API estate with dozens of microservices where hand-writing every client would take weeks of boilerplate.

Non-negotiables: explicit validation criteria (unit tests, response checks, schema enforcement) and developer ownership of the result. The model's natural-language critique explains its fixes, but responsibility for correctness and security stays with the team.

## Real-time code generation (online generation)

The agent analyses the task, writes a snippet, runs it, observes the result, and revises until it works. This lets it handle a novel API or problem without waiting for a human.

Benefits
- Adaptability to new tasks and environments.
- Speed: no human in the loop for each new need, less downtime.
- Fits dynamic work such as ad-hoc data analysis or complex integration.

Risks the chapter stresses
- Quality: unreviewed code can fail systems or open security holes.
- Security: executing self-written code is an injection channel for malicious actors (data exfiltration, unauthorized access, damage).
- Repeatability (the less obvious one): rebuilding a tool each time means one success does not predict the next; prompt tweaks or model updates change the code path, which breaks debugging, testing and compliance certification.
- Resource use: naive generated solutions can consume a lot of CPU and memory.

## Decision guide

| Question | If yes |
|---|---|
| Will this capability be needed again? | Generate once offline, review, persist as a tool |
| Is the action regulated, audited or user-facing at scale? | Do not regenerate per request; require a reviewed tool |
| Is it exploratory analysis on non-sensitive data? | Real-time generation acceptable in a sandbox |
| Does the code touch production state or secrets? | Forbid real-time generation; use narrow stateful tools |

Guardrails if you allow runtime code
- Isolated sandbox: no network by default, no production credentials, read-only mounts.
- CPU, memory, wall-clock and output-size limits.
- Allow-listed libraries; static checks before execution.
- Log generated code with its inputs and outputs; promote snippets that recur into reviewed, persisted tools.

Worked example: a reporting agent repeatedly writes pandas code to pivot sales exports. Logs show the same transformation 40 times a week with three variants, one of which mishandles currencies. Freeze the correct variant as a tested `pivot_sales_by_region` tool, register it, and set tool choice to force it for that step.
