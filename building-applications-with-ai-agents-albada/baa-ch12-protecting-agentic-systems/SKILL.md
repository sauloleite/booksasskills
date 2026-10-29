---
name: baa-ch12-protecting-agentic-systems
description: Security and resilience guidance for LLM agent systems, based on Chapter 12 of Michael Albada's "Building Applications with AI Agents" (O'Reilly, 2025). Covers agent-specific risks, HITL weaknesses, prompt-injection threat taxonomy, model selection and layered defenses, red teaming, MAESTRO threat modeling, data privacy/provenance, agent safeguards, external threats and internal failures. Use when designing, reviewing, threat-modeling, red-teaming, hardening or monitoring an agent, its tools, data flows or multiagent setup.
---

# Protecting Agentic Systems (Albada, Ch. 12)

Agents widen the attack surface of ordinary software because they act autonomously, reason probabilistically, adapt to context, and depend on foundation models and data the team does not fully control. This skill turns the chapter into a working method: classify the risk, model threats layer by layer, pick and harden the model, protect the data, fence the agent with safeguards, defend the perimeter, and engineer for internal failure. Security here is never a one-off deliverable; every control is assumed to decay unless it is re-tested.

## Decision rules to apply by default

1. **Name the agent-specific risk first.** Check for goal misalignment (vague objectives optimized literally), probabilistic error (hallucination), dynamic adaptation (small input shifts change actions) and limited visibility (acting on partial data). Generic appsec checklists miss these.
2. **Do not treat HITL as a free safety net.** Human reviewers suffer automation bias, alert fatigue, skill decay and incentive conflicts (speed vs safety). Pair any approval step with escalation paths, adaptive alert tiers and recurring hands-on adversarial training.
3. **Assume every external text is a potential instruction.** Treat direct and indirect injection, system-prompt extraction, jailbreak personas, fake "maintenance mode" framing, encoding-based evasion (e.g. base64 output), instructions dressed as JSON/config/logs, and swarm-propagated memory updates as distinct test cases.
4. **Model choice is a security decision.** Larger general models give versatility with less predictability; small fine-tuned models are easier to monitor. Open weights give auditability but need hardening; proprietary gives built-in guardrails but less visibility. Sensitive workloads favor on-prem or air-gapped hosting. Check certifications (GDPR, SOC 2) and explainability. Prefer a hybrid: small specialized models for high-stakes precise steps, large models for open-ended ones. Re-evaluate as models change.
5. **Layer defenses; no single filter is enough.** Input sanitization and validation, injection prevention (instruction anchoring, rigid prompt templates, context isolation), output filtering plus business-rule validation, authenticated and rate-limited model endpoints with full interaction logs, and sandboxed tool execution.
6. **Measure guardrails, do not assume them.** Benchmark detectors with injection suites (Lakera PINT: 4,314 inputs; published scores ranged from 92.5% to 61.4% across products) and indirect-injection suites such as Microsoft BIPIA. Treat a score as a snapshot.
7. **Red team continuously and with both humans and tools.** Iterate implement, attack, evaluate, mitigate. Use LLM-generated off-distribution data, automated frameworks (DeepTeam, Garak, PyRIT) for breadth, and humans for nuance. Rank findings by severity, exploitability and real-world impact. Re-run after any fine-tune, model swap or new deployment context.
8. **Threat-model with MAESTRO, not only STRIDE/PASTA.** Walk the seven layers (foundation models, data operations, agent frameworks, deployment/infrastructure, evaluation/observability, security/compliance, agent ecosystem) and trace how a flaw in one cascades to another.
9. **Data: minimize, encrypt, prove.** Process the least sensitive data needed; AES-256 at rest, TLS in transit, mTLS for high-sensitivity hops; RBAC/ABAC with read-only or write-only grants; hash-and-sign at ingestion and re-verify at every stage; no plaintext secrets or PII in logs; automatic purge of caches, intermediates and logs on schedule.
10. **Least privilege per agent, enforced outside the model.** Each agent gets a scoped role, a policy layer that checks every action before execution (a summarizer must not run code or call the network), sandboxed runtime, I/O validation, rate limits, anomaly detection, immutable audit logs, and a fail-safe that reverts to a safe state or escalates.
11. **Perimeter for external threats.** DMZ plus internal segmentation, firewalls/IDPS, mTLS between components, OAuth 2.0 or API keys, RBAC for external callers, SCA scanning plus signature checks plus an SBOM for dependencies, honeytokens, hardened hosts, and a rehearsed incident-response plan that can isolate a compromised agent.
12. **Engineer for internal failure.** Constraints validated pre-execution, fallbacks (cached data, operator notice, deferral), health checks and agent self-reported uncertainty, idempotent and transactional state changes, isolated dependencies, explicit inter-agent coordination and quorum for critical decisions, chaos experiments, transparent escalation, blameless postmortems.
13. **Default alert thresholds** (tune for load peaks to avoid fatigue): error/hallucination rate above 5% over a rolling hour; P99 latency above 2 s on critical paths; sustained CPU/GPU/memory at 80%; output drift similarity below 0.85; any race or sync failure in a multiagent setup.

## Default workflow

1. Draw the system diagram; list agents, tools, data stores, external inputs and human checkpoints.
2. Run a MAESTRO pass: assets and entry points per layer, cross-layer cascades, score each risk (CVSS-style).
3. Choose or confirm the model mix and hosting against capability, transparency, deployment and compliance needs.
4. Audit the tool manifest for privileged actions lacking approval, scope or sandboxing (script below).
5. Specify data controls: minimization, encryption, provenance chain, log sanitization, retention.
6. Specify agent safeguards, perimeter controls and failure handling; wire the KPI alerts.
7. Red team (automated plus human), fix by priority, add regressions, schedule the next round and a chaos game day.

## References

- [references/agent-risks-and-threat-vectors.md](references/agent-risks-and-threat-vectors.md): read when explaining why agents need special security, designing human oversight, or building an attack taxonomy and test cases.
- [references/model-selection-defenses-red-teaming.md](references/model-selection-defenses-red-teaming.md): read when picking a model/hosting option, designing input/output guardrails, benchmarking detectors, or planning a red-team program and tooling.
- [references/maestro-threat-modeling.md](references/maestro-threat-modeling.md): read when running a structured threat model of an agent or multiagent system.
- [references/data-protection.md](references/data-protection.md): read when handling PII or confidential data, designing encryption, provenance, integrity checks, audit trails, retention or cross-party data sharing.
- [references/agent-safeguards-and-resilience.md](references/agent-safeguards-and-resilience.md): read when scoping agent permissions, hardening against external attackers, setting monitoring KPIs, or planning fallbacks, chaos experiments and postmortems.
- [references/source-map.md](references/source-map.md): chapter headings mapped to the file that covers each.

## Scripts

- Run `python3 scripts/audit_tool_manifest.py manifest.json` to flag tools whose capabilities (write, delete, payment, network, exec, credential, messaging) lack approval, scoping, sandboxing or rate limits. Add `--json` for machine output; exit code 1 when any HIGH finding exists.
- Run `python3 scripts/check_agent_kpis.py metrics.json` to compare observed agent metrics with the chapter's default alert thresholds; override any threshold with flags such as `--error-rate-max 0.03`. See `--help` for input format.
