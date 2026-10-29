# Agent Scope, Access Control and Memory Boundaries

## Contents
- Scope profiles (who it serves, reach, autonomy, risk, governance, memory)
- Access control rules
- Per-scope policy differentiation
- Context flow decisions
- Memory transparency checklist
- Pitfalls and worked example

## Scope profiles

Classify every agent by whom it serves. Scope drives access, autonomy, risk, governance and memory design together, so decide them as one package. Scope is a governance decision as much as an architecture one: it fixes not only what the agent can do but what it ought to do and who is watching.

**Personal** (one individual; e.g., an executive assistant or coding copilot)
- Reach: the person's mail, calendar, files, code. Autonomy low to moderate. Risk low; small mistakes stay contained.
- Governance: the user manages preferences; light oversight; explanations are optional.
- Memory: isolated by default (preferences, past questions, unfinished tasks); shared only with explicit permission.

**Team** (a group or its manager; e.g., sprint planner, meeting bot)
- Reach: shared drives, meetings, team goals. Autonomy moderate. Risk moderate.
- Governance: rules on what goes into shared memory, escalation to peers, deliberate trust calibration.
- Memory: shared space with access controls. Must not resurface content from private one-to-one exchanges.

**Project** (a cross-functional group; e.g., program agent, launch coordinator)
- Reach: trackers and deliverables. Autonomy moderate to high. Risk moderate to high.
- Governance: visibility across functions, logging, a defined way to settle conflicts between groups.
- Memory: access-controlled shared space; decide whether members' personal context may flow in.

**Functional** (a department; e.g., HR, compliance, marketing agents)
- Reach: CRM, HR information systems, finance systems. Autonomy high but bounded by domain. Risk high.
- Governance: RBAC, audit logs, alignment with compliance regimes.
- Memory: departmental access-controlled store; must not surface one business unit's confidential data to another.

**Organizational** (leadership, IT, CIO; e.g., company-wide analytics agent, AI help desk)
- Reach: enterprise systems and analytics. Autonomy high, or intentionally restricted. Risk very high and system-wide.
- Governance: several sign-off tiers, governance board review of behavior and updates, continuous ethical audits, full traceability; rigorous guardrails and explainability.
- Memory: policy-governed store with retention rules, logging and audit; may accumulate long-term patterns across the business.

General rule for memory at any scope: the agent must never assume it may carry personal or sensitive data across scopes without a policy that says so.

## Access control rules

- Personal agents can borrow the permissions of their user.
- Functional and organizational agents get explicit, role-specific privileges registered in enterprise systems, never a human's credentials.
- RBAC tightens as scope grows and should track data sensitivity (public, internal, restricted).
- Privileges depend on the principal: acting for a VP is not the same as acting for an intern.
- IT, data governance and agent developers design the access model together so the agent cannot exceed its intended scope.
- Log delegations so every action traces back to an accountable principal.

## Per-scope policy differentiation

Do not use one autonomy, escalation or logging policy for every agent. Examples:
- A personal agent may send email and book meetings without asking.
- A finance functional agent may need human approval on every action.
- An organizational agent may need several authorization layers, or a governance board to approve behavior changes and system updates.

## Context flow decisions

Answer these explicitly before launch:
- May memory move upward (personal to project, project to function)? Under what consent?
- May agents query each other for context, or are they siloed?
- What is the retention period at each scope?
- Who can audit the flows?

Unanswered questions here become leaks or scope creep later.

## Memory transparency checklist

- Memory state is visible in the interface.
- Users can switch memory off.
- Users can inspect and delete stored items.
- The agent can explain what it remembers and why it kept it.
- The agent never relies on hidden stale or private memories for a decision.
- Memory policies are auditable and enforced in code, not only documented.

Treat memory as a governed asset, a source of power and of risk. Well-governed memory feels coherent and respectful; poorly governed memory feels intrusive and opaque.

## Pitfalls

- Promoting a personal assistant to team use while keeping its personal memory store attached.
- A functional agent running with an administrator's personal token.
- One global "log everything, approve nothing" policy for all agents.

## Worked example

A company moves its meeting-notes bot from personal to team scope. Changes required: a new team memory namespace with membership-based ACLs; personal notes stay in each user's isolated store and are promoted only when the user marks them shareable; action items involving restricted HR topics are routed to the manager instead of the shared channel; the bot gains a "what I remember about this project" view with delete controls; logging moves from optional to on, with 90-day retention.
