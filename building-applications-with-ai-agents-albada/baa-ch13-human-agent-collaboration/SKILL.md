---
name: baa-ch13-human-agent-collaboration
description: Human-agent collaboration guidance based on Chapter 13 of Michael Albada's "Building Applications with AI Agents". Covers human roles (executor to governor), progressive delegation, adoption rollouts, agent scopes and RBAC, scoped memory, trust repair, accountability (audits, logs, traceability), escalation thresholds, and compliance in CI. Use when deciding how much autonomy an agent gets, designing approval or handoff flows, planning a pilot, scoping memory or permissions for team or enterprise agents, or preparing governance and regulatory controls.
---

# Human-Agent Collaboration (Albada, Chapter 13)

This skill helps an agent advise engineers on the human side of agentic systems: who does what as autonomy grows, how far an agent of a given scope may act alone, when it must ask or hand off, how trust is earned, displayed and repaired, and which accountability and compliance machinery has to exist before autonomy expands. The chapter's core stance is that collaboration is a staged journey rather than an on/off switch, and that autonomy, access, oversight and governance must rise together. Apply the rules below directly; open a reference when you need the full playbook, tables in prose form, checklists or worked examples.

## Key decision rules

**Roles and autonomy**
- Map the deployment to a human role: executor (starts tasks, checks every output), reviewer (spot-checks, handles exceptions), collaborator (co-plans and annotates while the agent drafts and acts), governor (writes policy, audits, owns escalation). Design the UI for the current role and the next one.
- Each role needs different tooling: executors get guided steps and fast feedback; reviewers get exception queues, confidence scores, dashboards; collaborators get shared plans and inline annotation; governors get policy configuration, audit and escalation logs, explainability.
- Roles can coexist in one system (front-line reviewers plus senior auditors). Promote a role only after measured accuracy or false-positive rates clear a set bar.

**Adoption**
- Treat rollout as change management. Bring legal, engineering and end users in as co-designers; surface conflicting expectations early instead of designing for a fictional average user.
- Before building, write down: outcomes to improve, decisions the agent owns vs. humans keep, and what success and failure look like.
- Success metrics must include trust, friction and workflow fit, not only speed or accuracy.
- Expand in phases, gating each phase on quantitative thresholds plus qualitative confirmation (example in the reference: a 50-engineer pilot gated on acceptance rate and satisfaction before reaching 400+).

**Scope, access and memory**
- Classify scope: personal, team, project, functional, organizational. Autonomy, risk and governance burden rise along that ladder; never apply one policy to all.
- Personal agents may inherit their user's permissions. Functional and organizational agents need explicit role-based privileges, set jointly with IT and data governance, and privileges should vary by whom the agent acts for.
- Governance scales: user preferences (personal), shared memory rules and peer escalation (team), logging and conflict resolution (project), RBAC, audit logs and compliance (functional), multi-tier sign-off, review board and continuous ethical audits (organizational).
- Memory defaults: personal is isolated unless sharing is explicitly allowed; team and department use access-controlled shared spaces; organizational memory sits under retention, logging and audit policy. Decide explicitly whether context may flow upward or across agents.
- Users must be able to see, disable, inspect and delete what is remembered, and the agent must be able to say what it remembers and why. Never act on stale or private memory silently.

**Trust**
- Start cautious (drafts, read-only, approval required) and widen autonomy as reliability is shown (e.g., draft reports, then send them; read-only finance, then supervised transactions).
- Make trustworthiness visible: versions, change logs, audit trails, stated confidence and decision factors, and frictionless override.
- Provide a trust-repair path: reset, retrain, or reduce capabilities after mistakes. Never remove human fallback for empathy- or judgment-heavy work (the over-automation case in the reference reversed within about a year).

**Accountability and escalation**
- Name who is responsible (developer, operator, deploying organization) before launch. Borrow existing frameworks such as NIST AI RMF or an impact assessment template rather than inventing process.
- Run ethical audits repeatedly: outputs vs. goals, bias and disparate impact, decision pathways, stakeholder impact; add behavioral tests on edge cases and consider third-party auditors.
- Keep decision, interaction and error logs that let an auditor reconstruct why, with what data, and under what external conditions. Encrypt, restrict and anonymize logs; make them readable.
- Define escalation triggers by decision type, risk level and confidence (e.g., auto-approve purchases below $1,000, multi-party sign-off above). Every escalation carries what was tried, why it stopped, and what is needed.
- Feed human resolutions back into policies, prompts or training. Escalation is part of responsible autonomy, not a failure signal.

**Compliance**
- Identify applicable regimes (EU AI Act risk tiers, GDPR, CCPA, HIPAA, PCI DSS, SOX) and design for change.
- Put compliance in the pipeline: automated gates that fail the build, policy-as-code tests, and model cards plus datasheets generated per version. Apply minimization, PII stripping, encryption at rest and in transit, and least-privilege access.

## Default workflow

1. Pick a low-risk pilot domain and name the starting human role and agent scope.
2. Define success metrics (technical plus trust and adoption) and phase gates before building.
3. Set access (inherited vs. explicit RBAC) and memory boundaries for the scope.
4. Write escalation thresholds and the context package each handoff carries.
5. Stand up logging, traceability, audit cadence and compliance gates before go-live.
6. Expose confidence, change logs and override controls in the interface.
7. Review metrics and escalation outcomes; widen autonomy one step at a time, or roll back using the repair path.

## References

- [roles-adoption-and-scaling.md](references/roles-adoption-and-scaling.md): read when choosing human roles, interface patterns per role, planning stakeholder alignment or a phased rollout, or deciding how an agent should grow from individual to enterprise use.
- [scope-access-and-memory.md](references/scope-access-and-memory.md): read when classifying an agent's scope, setting RBAC and per-scope policies, or designing shared memory and context-flow boundaries.
- [trust-accountability-and-escalation.md](references/trust-accountability-and-escalation.md): read when designing progressive delegation, trust repair, audits, logging and traceability, or escalation thresholds and oversight roles.
- [compliance-and-next-steps.md](references/compliance-and-next-steps.md): read when mapping regulations, building compliance into CI/CD, or writing a first-steps plan for an organization starting with agents.
- [source-map.md](references/source-map.md): chapter headings mapped to the reference covering each.

## Scripts

None. The chapter offers qualitative frameworks and example thresholds, not calculations.
