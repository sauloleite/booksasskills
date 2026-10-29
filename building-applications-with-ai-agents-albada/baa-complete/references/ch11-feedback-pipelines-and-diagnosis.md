# Feedback Pipelines, Issue Detection, RCA and Human Review

## Contents
- The improvement loop as a whole
- Automated feedback pipelines: job description
- Optimizer frameworks (DSPy, Trace, APO)
- Automated issue detection
- Root cause analysis (RCA)
- Human-in-the-loop (HITL) review and escalation design
- Worked example: refund agent
- Pitfalls
- Glossary

## The improvement loop as a whole

Treat failure in a production multiagent system as guaranteed, not exceptional. Quality is judged by how fast the system learns from failures. The chapter frames improvement as a cycle borrowed from reinforcement learning: the agent acts in an environment, observes the result and a reward signal, and adjusts. Most teams running pretrained foundation models never close that cycle; they ship and patch by hand. The fix is three linked stages:

| Stage | Question it answers | Main risk if skipped |
|---|---|---|
| Feedback pipelines | What is failing, why, and what matters most? | Fixing symptoms, chasing noise |
| Experimentation | Does the proposed fix actually help, safely? | Regressions shipped to everyone |
| Continuous learning | How does the validated fix become part of the system? | Gains evaporate or never generalize |

Feedback pipelines depend on data quality and can miss genuinely novel problems unless there is an escalation path. Experimentation needs enough traffic for significance, costs resources, and is not acceptable alone for very high risk changes (add approval gates). Continuous learning risks overfitting and regressions and needs strong monitoring.

The loop is also organizational: engineering, data science, product and UX must agree on how insights are recorded, ranked and protected against side effects. Documentation is what ties the stages together and preserves memory across teams.

## Automated feedback pipelines: job description

Automation is the first analyst. At scale nobody can read raw traces, so the pipeline must:

1. Monitor every interaction continuously (traces of reasoning steps, skill selection, tool calls with parameters, outputs, user signals).
2. Detect failure patterns and cluster similar failures so a trend is visible as one item, not a thousand log lines.
3. Map clusters to likely causes. Repeated wrong skill choice usually means the agent's reasoning does not match user intent; repeated tool execution errors usually mean the agent builds parameters ambiguously.
4. Propose concrete changes and send the highest impact items to people.

Two capabilities matter most:

- **Text-feedback back-propagation.** Modern optimizers convert critiques into edits of prompts, skill parameters and reasoning order. Examples: tighten wording where outputs are ambiguous, add constraints, reorder reasoning steps, add parameter validation or a fallback path where tool calls are malformed.
- **Proactive detection.** Watching input distributions lets the pipeline notice drift (for example user queries shifting toward a new pattern) and adjust prompts before the drift becomes an outage.

Hard limit: automation finds patterns but cannot weigh context or business strategy. Engineers review, approve, and sometimes reject its proposals. Position automation as an amplifier of engineers, never a replacement.

## Optimizer frameworks (DSPy, Trace, APO)

All share one loop: a candidate prompt runs on a target model over a dataset, an evaluator model or metric scores the outputs, and an optimizer model proposes a better prompt. Repeat until the score plateaus.

- **DSPy** (Stanford NLP, open source). Treat the LM pipeline as a declarative program: declare signatures (typed inputs and outputs), compose modules (chain of thought, ReAct), then compile with an optimizer such as BootstrapFewShot or MIPROv2 against a labeled set and a metric. Output: better instructions, selected few-shot demos, optionally fine-tuned weights. Supports multistage compilation and major model APIs.
- **Microsoft Trace** (open source). Generative optimization of whole workflows from any feedback signal: scalar scores, natural language critiques, pairwise preferences. No gradients or differentiable objective required, so it suits black-box, multistep agents.
- **APO (Automatic Prompt Optimization).** Same propose, score, refine loop focused on prompt text.

Choosing: DSPy when you can express the task as modules with a measurable metric and have labeled examples; Trace when feedback is heterogeneous or the system is a black box you cannot decompose cleanly.

Dataset sizing guidance from the chapter: a handful of synthetic examples demonstrates the mechanics only. Aim for 100 or more annotated cases for agent-level optimization and roughly 50 to 200+ real examples for a tool-level classifier. Exact match is a toy metric; use semantic similarity or a custom scorer in production.

## Automated issue detection

Detection mechanisms, used together: rule-based triggers, anomaly detection, statistical clustering, and ML models for slow trends. Signals worth alerting on:

- One skill or tool failing repeatedly
- Sudden jumps in error rate or latency
- Shifts in engagement or satisfaction
- Behavior that differs between agent versions or between environments
- Gradual drift in decision patterns
- Correlations between particular input types and downstream failures

Example pattern: a log search tool starts rejecting many calls because the agent writes overly elaborate query syntax. A good pipeline logs every call, clusters the rejections by error message, and links the cluster to the reasoning step that produced the query.

## Root cause analysis (RCA)

Detection says what broke; RCA says why. Treat it as continuous inquiry across user intent, agent reasoning, architecture and environment, not a one-off postmortem. Steps in order:

1. **Workflow tracing.** Rebuild the full chain of decisions, tool calls and user turns that led to the failure.
2. **Fault localization.** Pin the responsible component: a prompt the model misread, a wrong skill choice, a tool whose parameter logic is too strict.
3. **Pattern recognition.** Decide if it is a one-off or a trend, and whether it clusters by user cohort, input type or system state.
4. **Impact assessment.** Estimate frequency and severity to set priority.

Expect non-technical root causes: vague task definitions, gaps in training or example data, changed user expectations, and organizational blind spots, for instance KPIs that reward the wrong behavior or workflows that no longer fit users. Good RCA produces improvement opportunities (prompt, tool, orchestration, or how user needs are represented), not blame.

## Human-in-the-loop (HITL) review and escalation design

HITL is a structured escalation route for cases automation cannot settle: ambiguous intent, ethical questions, conflicting goals, novel edge cases. The flow: agent produces candidate outputs, a human reviewer approves or corrects them, approved outputs go to users, and review findings feed back into the system.

**Escalate when** errors persist without a technical explanation; anomalies touch regulated or ethical territory; high-value or mission-critical tasks fail; automated tools disagree with each other.

**Two escalation axes.** Send humans the cases with the lowest certainty or the largest consequences.

Uncertainty signals, from cheapest:
- Self-reported certainty: instruct the model to append a 0 to 1 confidence. Example cutoffs from the chapter: escalate below 0.7 in general, below 0.8 for a sensitive classification.
- Entropy of classification probabilities: high entropy means ambiguity.
- Self-consistency: run 3 to 5 samples and escalate when they disagree by more than about 20%.
- A second model acting as critic that scores coherence.

Consequence signals: domain severity labels, critical assets or privileged accounts, regulatory exposure.

Combine as risk = uncertainty x consequence and escalate above a threshold. Tune thresholds offline on historical data (DSPy can search them) by simulating escalation volume; keep escalations under roughly 10% of cases so reviewers do not burn out. Clear triggers stop automation from taking narrow or inappropriate actions while routine confident cases flow through.

**Review procedure** for an escalated case, run by a mixed team (engineering, product, data science, UX):
1. Contextual analysis: reproduce the failure in a controlled environment.
2. Trace inspection: read logs and decision chains to see how intent was interpreted and actions chosen.
3. Impact assessment: scope and severity, covering correctness and user experience.
4. Resolution design: choose the intervention (prompt fix, workflow redesign, new skill, user-facing change, or a confirmation step inside a dangerous tool).

Log each decision, its rationale and its outcome so cases are reproducible and recurring issues surface. Product managers judge whether the failure reflects a misread user need; data scientists spot hidden patterns; UX researchers find friction metrics miss. Every reviewed case becomes an entry in a knowledge base used for onboarding, design and future pipeline tuning.

## Worked example: refund agent

A customer-support agent approves refunds via an `issue_refund` tool. Weekly pipeline output shows a cluster of 140 tool errors, all "amount exceeds order total".

- Tracing: the agent adds shipping fees twice when the user mentions shipping.
- Localization: the prompt says "refund the full cost including shipping" while the order API already includes shipping in the total.
- Pattern: concentrated in orders with free-shipping promotions.
- Impact: frequent, low severity (the tool rejects the call), but users wait for a human.
- Escalation config: refunds over $500 or certainty under 0.7 go to a person; simulated on last month's data this escalates 7% of cases.
- Fix proposal: reword the prompt, add a validation step in the tool that clamps to the order total and returns a structured error, then send both changes to experimentation.

## Pitfalls

- Letting the optimizer push prompt changes straight to production without offline tests and a shadow run.
- Clustering by raw error string only; cluster by upstream reasoning step too, or you treat symptoms.
- Escalation thresholds set by gut feel, producing either reviewer overload or silent failures.
- HITL decisions not recorded, so the same debate repeats next month.
- Treating RCA output as an engineering-only ticket when the cause is a product definition.

## Glossary

- **Drift:** gradual mismatch between what the system assumes (threat patterns, query styles) and current reality, often visible first as a rise in one error type.
- **Signature (DSPy):** declared input and output fields of a task, from which the framework builds and optimizes prompts.
- **Generative optimization (Trace):** using a foundation model to propose and judge system edits from non-differentiable feedback.
- **Risk score:** product of uncertainty and consequence used to rank escalation.
