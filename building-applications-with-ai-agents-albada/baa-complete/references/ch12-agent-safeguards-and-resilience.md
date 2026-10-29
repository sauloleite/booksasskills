# Securing Agents: Safeguards, External Threats, Internal Failures

## Contents
- Three lenses
- Safeguards (preventive controls)
- Protections from external threats
- Protections from internal failures
- Monitoring KPIs and default thresholds
- Chaos engineering for agents
- Escalation and postmortems
- Worked example
- Pitfalls

## Three lenses

After the model and the data, the agent itself needs hardening. Split the work into: safeguards that prevent misuse up front, defenses against outside attackers, and engineering that keeps internal faults contained. Internal faults deserve as much attention as attackers, since they slip past perimeter controls and spread quietly through connected workflows.

## Safeguards (preventive controls)

| Safeguard | What it means for an agent | Test for it |
|---|---|---|
| Role and permission management | Each agent has an explicit list of tasks, data and actions; RBAC with periodic review | Can the support agent read finance tables or call admin functions? It must not |
| Behavior constraints | A policy layer outside the model checks every proposed action against rules before execution; response filters for ethics, regulation, policy | Ask a summarizer to run code or fetch a URL; the policy layer must refuse |
| Environment isolation | Sandbox or container per agent, limited network egress and resource access, to shrink blast radius | Escape attempts from the sandbox; egress to unapproved hosts |
| I/O validation pipelines | Sanitize incoming prompts/data; screen outputs for harmful content, unintended actions, policy breaches before they flow downstream | Injection and leak suites at both ends |
| Rate limiting and anomaly detection | Cap interaction volume to stop exhaustion/DoS; flag unusual behavior such as a sudden burst of outbound API calls | Load spikes; synthetic bursts |
| Audit trails | Log every significant decision, input, output and event; logs immutable, encrypted, reviewed | Can an operator reconstruct why an action happened? |
| Fallback and fail-safe | On ambiguity, limit breach or anomaly: revert to a safe state, follow a predefined workflow, alert, pause, or hand to a human | Force each trigger and observe the response |

Safeguards age. Review them regularly and keep them under penetration testing and red teaming.

Minimal action-gate sketch (original):

```python
RISKY = {"payment", "delete", "exec", "external_email"}

def gate(agent, action, args, policy, approvals):
    if action not in policy.allowed_actions(agent.role):
        return "deny"
    if not policy.args_in_scope(agent.role, action, args):   # e.g. amount cap, path prefix
        return "deny"
    if action in RISKY and not approvals.granted(agent.id, action, args):
        return "escalate"
    return "allow"
```

## Protections from external threats

Entry points: APIs, data streams, plug-ins, user input. Attack types: adversarial manipulation, exfiltration, DDoS against endpoints.

1. **Network architecture**
   - Put public-facing services (web front ends, webhook receivers) in a DMZ behind firewalls; route traffic to internal agent services and databases through an internal router with access control lists.
   - Segment the internal side into subnets (web tier, agent tier, data tier) so a compromised server cannot pivot freely; restrict ports and protocols between subnets; alert on unusual cross-subnet traffic. This fits a zero-trust posture.
   - Use mTLS between components to curb lateral movement.
2. **Network security controls**: firewalls and intrusion detection/prevention systems; mTLS on endpoints talking to external APIs; throttling and rate limits on public interfaces.
3. **Authentication and authorization**: OAuth 2.0 or API keys for callers; extend RBAC to external systems so each outside party gets a narrow scope.
4. **Supply chain**: SCA tools scanning dependencies continuously, signature verification for third-party plug-ins and integrations, a maintained SBOM with the security status of each component.
5. **Adversarial input defenses**: sanitize all inbound data before it reaches the reasoning layer; instruction anchoring and context isolation against injection; detect attempts to extract secrets or trigger commands.
6. **Real-time anomaly detection**: watch traffic, prompts and responses for repeated auth failures, unexpected API calls and known attack signatures.
7. **Honeytokens**: plant fake credentials or records in data flows; any access or exfiltration of them is a high-confidence alarm.
8. **Endpoint hardening**: least privilege on hosts, prompt OS and dependency patching, disable unused services and ports.
9. **Proactive testing**: regular penetration tests, vulnerability scans and red-team exercises aimed at external interfaces and data flows, with findings fed back.
10. **Incident response**: written procedures to isolate a compromised agent (revoke its credentials, cut its tools, quarantine its memory), escalate, and recover; rehearse with drills.

## Protections from internal failures

Causes: misconfiguration, vague goals, missing safeguards, agents working against each other, cascading errors.

- **Misaligned objectives**: unclear or too-narrow directives lead to side effects (an optimizer trading safety for speed). Embed boundaries in the architecture and validate decisions against rules before execution.
- **Error handling and graceful degradation**: catch invalid inputs, API failures and inconsistent data locally. Example fallback when a dependency is down: serve cached data, notify an operator, defer noncritical work.
- **Monitoring and telemetry**: real-time logs, error reports, performance metrics; periodic automated health checks of core functions; agent self-assessment signals raised when instructions are ambiguous, data is incomplete or goals conflict.
- **State management**: keep shared state synchronized; make operations idempotent (safe to retry) and transactional (all-or-nothing with rollback).
- **Dependency isolation**: containers or virtual environments around plug-ins and libraries so one unstable component does not sink the system.
- **Feedback loops and emergent behavior**: define inter-agent protocols with explicit message contracts and conflict-resolution rules; use quorum or voting for critical decisions to avoid single points of failure; cap recursion and message rates between agents.
- **Validation and testing**: unit, integration and stress tests that cover interactions, plus simulation sandboxes for edge cases.

## Monitoring KPIs and default thresholds

| KPI | Default alert | Notes |
|---|---|---|
| Error rate (failed tasks or hallucinations on valid input) | above 5% over a rolling 1-hour window | Needs a labeled or judged sample to count hallucinations |
| Response latency | P99 above 2 s on critical operations | Track mean too; P99 catches overload |
| Resource utilization (CPU, GPU, memory) | 80% sustained | Preempts saturation failures |
| Output anomaly score (e.g. semantic similarity to expected) | below 0.85 | Drift detection model |
| State consistency (race or sync failures) | any nonzero count in multiagent setups | Page immediately |

Tooling: Prometheus to collect, Grafana to visualize, drift and anomaly prediction with tools such as Evidently AI. Make thresholds context-aware (raise during known peaks) to curb alert fatigue while still catching misconfigurations and emergent behavior. The `scripts/check_agent_kpis.py` script applies these defaults to a metrics snapshot.

## Chaos engineering for agents

Deliberately inject controlled faults to verify recovery paths, in a staging or production-like setting first.
- **Fault injection**: add latency (e.g. +500 ms on an API), corrupt or noise inputs, kill a dependent plug-in. Platforms: Gremlin, Azure Chaos Studio.
- **Game days**: state a hypothesis ("if state sync between planner and executor fails, orders are not duplicated"), inject gradually, measure recovery time objective (RTO) and recovery point objective (RPO), targeting sub-minute recovery.
- **AI-specific faults**: model drift, floods of adversarial inputs, degraded retrieval; AI-assisted chaos tooling (e.g. Harness) can suggest weak spots and scale experiments.
- **Blast radius control**: start in isolated sandboxes, expand to production only with automated rollback; document each lesson and turn it into an improved fallback.

The lineage is Netflix's Chaos Monkey; the aim is to discover feedback loops and dependency cascades before customers do.

## Escalation and postmortems

- Agents must surface errors, ambiguous states and critical decision points to humans rather than silently retrying or guessing.
- After any incident, run a postmortem: root cause, corrective actions with owners, lessons recorded, and changes fed back into design and deployment.

## Worked example

An IT-operations agent can restart services and open tickets.
- Safeguards: role allows restart only for services tagged non-critical; restarts of critical ones escalate. Sandbox has egress only to the orchestration API.
- External: webhook receiver in the DMZ, OAuth client credentials, SBOM for its plug-ins, a honeytoken admin password in its config store.
- Internal: restart is idempotent keyed by incident ID; if the orchestration API times out, the agent opens a ticket and pages on-call instead of retrying in a loop.
- KPIs: alert if more than 5% of runbooks fail in an hour or if P99 latency passes 2 s.
- Chaos: game day kills the metrics exporter; hypothesis is that the agent pauses automated restarts rather than acting blind. It did not, so a "no telemetry, no action" rule was added.

## Pitfalls

- Relying on the system prompt to restrict actions instead of an external policy gate.
- Retry loops without idempotency, producing duplicate payments or orders.
- Alert thresholds so tight they page constantly, recreating alert fatigue.
- Agents that can message each other without rate caps, enabling runaway feedback loops.
- No rehearsed way to cut off a single compromised agent without taking down the whole system.
