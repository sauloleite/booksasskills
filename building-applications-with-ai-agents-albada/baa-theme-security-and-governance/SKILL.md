---
name: baa-theme-security-and-governance
description: Theme skill on protecting agentic systems and governing human-agent work, from Michael Albada's "Building Applications with AI Agents" (chapters 12 and 13). Use when threat modeling an agent (MAESTRO), defending against prompt injection and data leaks, auditing tool permissions, red teaming, designing safeguards and incident response, or planning autonomy levels, scope-based access, memory governance, escalation, accountability and compliance.
---

# Security, governance and human-agent collaboration (Building Applications with AI Agents, ch. 12 and 13)

Agents act with real permissions under probabilistic control, so protection and governance must sit outside the model and grow with the autonomy granted.

## Cross-chapter rules

1. **Assume new failure modes.** Misaligned goals, hallucinated actions, sensitivity to small context changes and decisions on incomplete data. Human review helps but degrades through automation bias and alert fatigue.
2. **Defense in depth.** Input checks, injection resistance (separate untrusted content, restate rules, rigid templates), output checks, authenticated and rate-limited endpoints, sandboxed tools and full logging. Measure guardrails with benchmarks.
3. **Least privilege, enforced outside the model.** Policy check before every action, scoped credentials, approval for high-impact tools. Audit manifests with `scripts/audit_tool_manifest.py`.
4. **Threat model in layers** (MAESTRO) and trace how a weakness in one layer propagates upward. Red team continuously and rank fixes by severity, exploitability and impact.
5. **Protect data end to end.** Minimize collection, encrypt at rest and in transit, verify integrity at every hand-off, keep secrets and PII out of logs, and delete on schedule.
6. **Contain internal failures.** Fallbacks, health checks, idempotent state changes, isolation, alert thresholds (`scripts/check_agent_kpis.py`), chaos testing and postmortems.
7. **Delegate progressively.** Humans move from executor to reviewer, collaborator and governor; autonomy expands on measured reliability with defined entry criteria and a way back down.
8. **Govern by scope.** Personal, team, project, functional and organizational agents need rising controls; memory is a governed asset users can inspect and delete.
9. **Make escalation and accountability explicit.** Thresholds by decision type and amount, named owners, decision logs, and compliance checks in CI mapped to the applicable regulations.

## Default workflow

1. Threat model the system and audit tool permissions (ch12).
2. Layer defenses, data protection and resilience controls; schedule red teaming (ch12).
3. Define roles, autonomy stages, scope-based access and memory policy (ch13).
4. Set escalation thresholds, ownership, audits and CI compliance gates (ch13).

<!-- BEGIN GENERATED: run tools/build_bundles.py to refresh -->

## References by chapter

Each link is one level deep; read only the files whose description matches the task.

### CH12: Protecting Agentic Systems

- [ch12-agent-risks-and-threat-vectors.md](references/ch12-agent-risks-and-threat-vectors.md): read when explaining why agents need special security, designing human oversight, or building an attack taxonomy and test cases.
- [ch12-agent-safeguards-and-resilience.md](references/ch12-agent-safeguards-and-resilience.md): read when scoping agent permissions, hardening against external attackers, setting monitoring KPIs, or planning fallbacks, chaos experiments and postmortems.
- [ch12-data-protection.md](references/ch12-data-protection.md): read when handling PII or confidential data, designing encryption, provenance, integrity checks, audit trails, retention or cross-party data sharing.
- [ch12-maestro-threat-modeling.md](references/ch12-maestro-threat-modeling.md): read when running a structured threat model of an agent or multiagent system.
- [ch12-model-selection-defenses-red-teaming.md](references/ch12-model-selection-defenses-red-teaming.md): read when picking a model/hosting option, designing input/output guardrails, benchmarking detectors, or planning a red-team program and tooling.

### CH13: Human-Agent Collaboration

- [ch13-compliance-and-next-steps.md](references/ch13-compliance-and-next-steps.md): read when mapping regulations, building compliance into CI/CD, or writing a first-steps plan for an organization starting with agents.
- [ch13-roles-adoption-and-scaling.md](references/ch13-roles-adoption-and-scaling.md): read when choosing human roles, interface patterns per role, planning stakeholder alignment or a phased rollout, or deciding how an agent should grow from individual to enterprise use.
- [ch13-scope-access-and-memory.md](references/ch13-scope-access-and-memory.md): read when classifying an agent's scope, setting RBAC and per-scope policies, or designing shared memory and context-flow boundaries.
- [ch13-trust-accountability-and-escalation.md](references/ch13-trust-accountability-and-escalation.md): read when designing progressive delegation, trust repair, audits, logging and traceability, or escalation thresholds and oversight roles.

Merged section maps: [source-maps.md](references/source-maps.md).

## Scripts

Python 3 standard library only; run any script with `--help` for its arguments.

| Script | Purpose |
|---|---|
| `scripts/audit_tool_manifest.py` (ch12) | Static audit of an agent tool manifest for risky, under-guarded permissions. |
| `scripts/check_agent_kpis.py` (ch12) | Check an agent metrics snapshot against default alert thresholds. |

<!-- END GENERATED -->
