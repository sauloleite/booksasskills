# Trust, Accountability and Escalation

## Contents
- Trust lifecycle model
- Progressive delegation ladders
- Making trust visible
- Trust repair playbook
- Accountability frameworks to borrow
- Ethical audits and behavioral assessments
- Logging and traceability
- Escalation design
- Oversight roles and feedback loops
- Pitfalls and worked example

## Trust lifecycle model

Trust is gradual, not a switch. It grows through consistent results, transparent behavior and clear limits, and it collapses fast when an agent oversteps, fails without telling anyone, or behaves erratically. Design for four phases: earn, display, maintain, repair.

- At personal scope, trust grows when the agent remembers preferences, follows instructions and recovers well from errors.
- At team, function or organization scope the agent speaks for a shared interest; its actions may affect many people, trigger system-wide effects, or be read as company policy. Trust there must be built deliberately and spread across several stakeholders.

Cautionary case: Klarna replaced about 700 customer-service roles with a chatbot in 2024; without empathy and nuanced judgment, complaints rose and human agents were being rehired by mid-2025. Lesson: keep a strong human fallback whenever work depends on empathy or judgment.

## Progressive delegation ladders

Begin cautious, deferring to humans for review or approval, and widen autonomy as reliability is demonstrated and users become familiar. Write the ladder per capability:

- Team reporting: draft status reports, then send after approval, then send automatically.
- Finance: read-only access, then transactions submitted under supervision, then bounded autonomous transactions.
- Generic: suggest, then act with approval, then act and notify, then act and log only.

Each rung needs an entry criterion (measured quality, override rate, time at previous rung) and an exit criterion for stepping back down.

## Making trust visible

- Clear versioning and change logs so users know when behavior may have shifted.
- Audit trails for actions.
- Disclosure of confidence, the main decision factors, and whether uncertainty was involved; explain why, not only what.
- Low-friction ways to override, intervene or correct.

## Trust repair playbook

When the agent errs or expectations change, a recovery path must already exist, or small slips cause lasting loss of confidence.
1. Contain: restrict capabilities or drop one rung on the delegation ladder.
2. Explain: use logs and traces to show what happened and why.
3. Fix: reset behavior, retrain, update prompts or policies.
4. Re-earn: return to wider autonomy only through the same entry criteria.

## Accountability frameworks to borrow

Decide up front who answers for harm or wrong decisions: developers, system operators, or the deploying organization. Combine structural measures (oversight policies, escalation paths) with technical ones (logging, traceability, ethical audits) so failures are found, analyzed and fixed rather than written off as side effects of complexity.

Adapt existing templates instead of inventing process:
- NIST AI RMF: voluntary, risk-based; its functions are govern, map, measure and manage. Use its profiles and worksheets to map risk levels, record mitigations and track progress.
- A co-designed AI impact assessment template that maps to ISO 42001, the EU AI Act and NIST AI RMF: records system purpose, effects on stakeholders, fairness and bias reviews, and mitigations; usable before launch and during ongoing governance.

## Ethical audits and behavioral assessments

Ethical audits look at social, cultural and organizational effects, beyond technical tests. Treat fairness as a primary audit goal. An audit should cover:
- Whether outputs serve intended goals and ethical guidelines.
- Bias and unfair treatment, including disparate impact across demographic groups and feedback loops that amplify bias.
- How the agent reaches recommendations (decision pathway review).
- Effects on each stakeholder group.
- Side effects of optimizing only for accuracy or efficiency.

Behavioral assessments complement audits by observing the agent in realistic conditions, especially edge cases and ambiguous inputs, to catch questionable trade-offs or unpredictable responses.

Cadence: repeat both after updates, retraining or new data exposure, not once. Consider independent third-party auditors to find blind spots insiders miss.

## Logging and traceability

Three log types:
- Decision logs: inputs, intermediate reasoning, outputs, and the reason for the choice.
- Interaction logs: timestamped user inputs and agent replies.
- Error and failure logs: when and why a task failed or produced an unintended result.

Traceability means an auditor can reconstruct a specific episode and answer: why this recommendation, which data drove it, and whether outside factors (API failures, conflicting instructions) changed the result. It is essential in healthcare, finance and criminal justice.

Protect logs with encryption, access control and anonymization, since they hold sensitive data. Make them usable: documentation and visualization so developers, auditors and stakeholders can act on them. Every action should be reviewable and, where needed, reversible.

Minimal decision record (illustrative):

```python
record = {
    "trace_id": trace_id, "ts": now_iso(), "agent_version": VERSION,
    "principal": user.role, "inputs": redact(inputs),
    "retrieved_sources": [d.id for d in docs],
    "steps": step_summaries, "tool_errors": errors,
    "decision": action, "confidence": conf,
    "escalated": conf < POLICY.min_conf or action.risk == "high",
}
```

## Escalation design

Escalation design is the policy and infrastructure that keeps an agent within its authority. Define thresholds by:
- Decision type (billing dispute, abuse report, contract change).
- Risk level or monetary amount (e.g., auto-approve purchases under $1,000; require multiple sign-offs above).
- Confidence boundary.
- Conflicting constraints or explicit policy triggers.

Route by type to the right human: a support agent answers routine questions itself, sends billing disputes to a supervisor and flags suspected abuse to trust and safety.

Every handoff carries a context package: what the agent tried, why it stopped, and what information is needed to continue. Encode paths both in software and in named organizational roles.

Why it matters for trust: when users know the agent defers at the right moments and a human can step in, they rely on it without over-trusting. Without escalation logic, systems either project false confidence or freeze under uncertainty.

## Oversight roles and feedback loops

- Oversight is proactive: designated people or committees watch behavior, review logs and refine escalation policy over time.
- Roles can map to existing positions (line managers, compliance leads) or new ones such as AI operations analysts and agent governance officers.
- Oversight also includes policy and technical guardrails that keep fully autonomous modes safe, not just human-in-the-loop steps.
- Human resolutions of escalated cases feed back into policies, retraining or prompt tuning. Escalation is a normal part of responsible autonomy, not evidence of failure.

## Pitfalls

- Silent failures with no error log or user notice.
- Hiding uncertainty to look more capable.
- Escalations that arrive with no context, forcing humans to redo the work.
- Audits run once at launch and never again.
- Logs that exist but nobody can read or that leak PII.

## Worked example

A procurement agent: below $1,000 and from approved vendors it orders autonomously and logs; from $1,000 to $10,000 it routes to the budget owner with quote comparison and rationale; above $10,000 or with a new vendor it needs finance plus legal sign-off. Monthly, a governance officer reviews escalation outcomes; if humans approve over 95% of a tier unchanged for a quarter, the threshold is reviewed upward.
