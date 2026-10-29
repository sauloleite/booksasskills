---
name: baa-ch09-validation-and-measurement
description: Evaluation and validation playbook for LLM agents, based on Chapter 9 of Michael Albada's "Building Applications with AI Agents". Covers hero scenarios and metric choice, structured eval cases and how to grow them, unit tests for tools, planning, memory and learning, end-to-end scoring (tool recall/precision, parameter accuracy, phrase recall, task success), consistency, coherence, hallucination, hostile inputs, and release gates. Use when designing an agent eval suite, scoring agent traces, debugging regressions, or deciding if an agent is ready to ship.
---

# Validation and Measurement for Agentic Systems

This skill helps an agent advise engineers on how to prove that an agentic system works and keeps working: what to measure, how to build and grow the evaluation set, how to test each component and the whole system, and how to turn results into deployment gates. It distills Chapter 9 of Albada's book, which threads one support-agent scenario (refund for a damaged item, then cancellations and address changes) through every technique. The core stance: evaluation is part of development from day one, automated, versioned and continuously extended, never a final "eyeball" check.

## Key decision rules

**Measurement foundations**
1. Anchor metrics in hero scenarios (the few high-priority, representative use cases). If a metric does not map to one, question it.
2. Mix quantitative (accuracy, precision/recall, latency, robustness, scale, cost) with qualitative (user satisfaction, reviewer judgment). Never optimize a single score.
3. For free text, prefer semantic scoring (embedding distance, BERTScore; BLEU/ROUGE as rough proxies) over exact match; use required-phrase checks only for content that must appear.
4. Run offline evals automatically on every merge and every model or prompt change, and keep a versioned metric history so regressions are visible against the past.
5. Each new tool or workflow lands together with its own eval cases; the eval set grows with capability and becomes a living specification.
6. Automation is not the whole story: sample outputs for human review, more so in novel or high-stakes domains.

**Eval set design**
7. Every case fixes the starting state, prior turns and the expected end state (tool calls with exact params plus required reply phrases). Add tags for failure type, feature and origin.
8. Grow the set from SME-authored cases, production logs, and LLM-generated variants (ambiguity, idioms, mutated edge cases) that a human reviews before admission. Stress it with adversarial search, single-token counterfactual edits and blended intents.
9. Public benchmarks (MMLU, BBH, HELM) are context for model choice; domain agents need a custom benchmark built with subject matter experts.

**Component tests**
10. Tools: happy, rare, malformed and adversarial inputs; assert latency, resources and error handling; determinism unless randomness is by design; mock external dependencies to inject rare failures; rerun the full suite on any change.
11. Planning: score tool recall (missed actions), tool precision (unneeded actions) and parameter accuracy (grounding errors). Test multi-item, ambiguous, contradictory and failed-tool cases, and run repeats for consistency.
12. Memory: exact retrieval over time, accuracy@k, no stale or lookalike results, latency as the store grows, and controlled failure on outages or migrations.
13. Learning: the update loop works, generalizes to holdout and adversarial data, survives distribution shift, and does not forget mastered behavior.

**System-level tests**
14. End-to-end task success requires right tools, right params, no extras and the required message content; also test load, latency and fallback or escalation on failure.
15. Consistency for nondeterministic agents means policy invariants hold across phrasings and reruns and nothing contradicts earlier turns. Layer LLM judges (with few-shot examples), actor-critic checks and human review.
16. Coherence: context retained, no repeated questions, actions in a logical order across long sessions.
17. Hallucination: ground in trusted sources (RAG), audit accuracy and source freshness, add expert feedback loops, and weigh reduction against inference cost.
18. Unexpected inputs (typos, slang, malformed IDs, partial outages, mixed intents) must produce clarify, decline or escalate, never a wrong tool call or a data leak.

**Deployment**
19. Write release criteria in advance: per-slice thresholds (the chapter's illustration is 95% tool recall on refund and cancellation cases), zero regressions on multiturn slices, latency and uptime targets, no critical bugs.
20. Enforce with gates: automated blocks on regression, manual sign-off after a pilot, human escalation when results are ambiguous. Keep rollback fast.

## Default workflow

1. Name the hero scenarios and the business objective; pick 4 to 6 metrics covering actions, message content, operations and human judgment.
2. Write 20 to 50 structured cases with tags; validate that expected params match each input state.
3. Build component suites (tools, planner, memory, learning) with mocks and failure injection.
4. Run the end-to-end harness on every change; rerun each case 3 to 5 times to measure consistency.
5. Expand cases from logs, reviewed LLM variants and adversarial generation; add one case per production incident.
6. Score with the script below, compare to the last release baseline per slice, and gate promotion.
7. Pilot, monitor with the same metrics, keep rollback ready.

## References

- [references/metrics-and-evaluation-sets.md](references/metrics-and-evaluation-sets.md): read when choosing metrics, wiring evals into CI, designing the case schema, or planning how to grow and diversify an eval set.
- [references/component-testing.md](references/component-testing.md): read when writing unit tests for tools, planners, memory stores or learning loops, or when interpreting low recall, precision or parameter accuracy.
- [references/system-level-evaluation.md](references/system-level-evaluation.md): read when building an end-to-end harness or testing consistency, coherence, hallucination or robustness to odd and hostile inputs.
- [references/deployment-readiness.md](references/deployment-readiness.md): read when defining release criteria, configuring quality gates, or planning pilot, monitoring and rollback.
- [references/source-map.md](references/source-map.md): read to find which file covers a given chapter section.

## Scripts

Run `python3 scripts/agent_eval_report.py runs.jsonl` to compute parameter accuracy, tool recall and precision, phrase recall, task success (with a Wilson 95% interval), forbidden-tool violations, latency p50/p95, cost per success, step counts, per-tag slices and rerun consistency from a JSONL file of agent runs (schema in `--help`).

Run `python3 scripts/agent_eval_report.py runs.jsonl --gate tool_recall=0.95 --gate task_success=0.9 --baseline last_release.json --max-drop 0.02 --save this_release.json` to apply release gates and per-slice regression checks; exit code 1 means promotion should be blocked. Crashed or unparseable runs count as failures, never skips.
