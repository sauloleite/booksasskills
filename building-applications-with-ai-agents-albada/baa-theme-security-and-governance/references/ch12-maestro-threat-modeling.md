# Threat Modeling Agentic Systems with MAESTRO

## Contents
- Why a specialized framework
- The seven layers: what to protect and how
- Running a MAESTRO session
- Cross-layer cascade analysis
- Worked example
- Pitfalls

## Why a specialized framework

STRIDE and PASTA were built for systems whose behavior is fixed by code. They underweight autonomy, learning from context, and agents acting on each other. MAESTRO, published by the Cloud Security Alliance (the acronym spans multiagent environment, security, threat, risk and outcome), is a layered reference architecture for agentic AI: it splits the system into seven stacked layers, each depending on the ones beneath, so teams can analyze concerns separately while still tracing how a weakness in a low layer surfaces as damage higher up.

Motivating cases: the 2024 Hong Kong deepfake fraud, where impersonated executives led to a $25M transfer, and memory-poisoning scenarios in 2025 CSA wargames where tainted data persisted across cooperating agents.

## The seven layers: what to protect and how

Ordered bottom to top. Threats and controls below are a working checklist, expanded beyond the chapter's summary.

**1. Foundation models**
- Threats: adversarial inputs, model extraction through repeated black-box queries, implanted backdoors.
- Controls: adversarial robustness training or vendor evidence of it, query quotas and anomaly detection on API usage, provenance of weights.

**2. Data operations** (ingestion, vector stores, RAG, memory)
- Threats: poisoning, exfiltration, tampering; injected content in RAG corpora leading to leaks.
- Controls: content hashing such as SHA-256, encryption, retrieval-time sanitization and source allowlists, write controls on memory.

**3. Agent frameworks** (orchestration libraries, tool adapters, plug-ins)
- Threats: supply-chain compromise of AI libraries in the style of SolarWinds, missing input validation in tool adapters.
- Controls: software composition analysis, pinned and verified dependencies, SBOM.

**4. Deployment and infrastructure**
- Threats: hijacked containers, denial of service, lateral movement (Kubernetes-based AI deployments were targeted in 2025).
- Controls: image scanning, mutual TLS between services, resource quotas, network segmentation.

**5. Evaluation and observability**
- Threats: poisoned metrics or benchmarks that hide bias or regressions, sensitive data leaking through logs.
- Controls: drift detection (Evidently AI is one option), append-only or immutable logs, log sanitization, independent evaluation sets.

**6. Security and compliance**
- Threats: agents evading controls, biased outcomes, decisions nobody can explain (GDPR penalties have followed opaque automated decisions in the EU).
- Controls: periodic audits, explainability techniques, decision records.

**7. Agent ecosystem** (agents, users, external agents and services interacting)
- Threats: unauthorized actions, attacks between agents, swarm privilege escalation.
- Controls: role-based controls per agent, quorum or multi-party approval for critical actions, signed inter-agent messages.

## Running a MAESTRO session

1. **Diagram first.** Draw components, trust boundaries, data flows and every place untrusted text enters.
2. **Inventory per layer.** For each of the seven layers list assets (weights, corpora, memory, credentials, logs) and entry points (APIs, uploads, retrieved pages, inter-agent channels).
3. **Enumerate threats per layer** using the checklist above plus a current external catalog such as the OWASP Top 10 for LLM applications (2025 edition).
4. **Trace cascades** (next section).
5. **Score and rank.** Use a consistent scheme; the chapter suggests a CVSS-style scoring adapted to AI. Include exploitability and blast radius.
6. **Assign mitigations** with owners and verification method.
7. **Validate by red teaming** the top risks.
8. **Repeat** at each significant change; embed in the SDLC rather than running it once. Existing tooling such as Microsoft's Threat Modeling Tool can be adapted to hold MAESTRO layers.

A minimal per-row record for the threat register:

```
id | layer | asset | entry_point | threat | cascade_to | likelihood(1-5) | impact(1-5) | score | mitigation | owner | verified_by
```

## Cross-layer cascade analysis

The point of layering is to see chains. For each high-score threat, ask: if this succeeds, which higher layer receives the corrupted artifact, and what action becomes possible there? Common chains:
- Poisoned document (layer 2) -> injected instruction executed by a tool adapter lacking validation (layer 3) -> unauthorized transfer by an over-privileged agent (layer 7).
- Compromised dependency (layer 3) -> container escape (layer 4) -> log tampering hides it (layer 5).
- Manipulated benchmark (layer 5) -> biased model shipped -> regulatory exposure (layer 6).

Break chains at the cheapest point and at more than one point.

## Worked example

Supply-chain planning swarm: a forecasting agent, a purchasing agent with order-placing tools, and a supplier-communication agent reading inbound email.
- Layer 2: supplier emails feed shared memory. Threat: an attacker emails fake "updated bank details" that is stored as fact. Mitigation: memory writes from external sources tagged untrusted, not usable for payment fields.
- Layer 7: the purchasing agent can change supplier payment data. Mitigation: payment-detail changes need quorum (two agents plus a human) and out-of-band confirmation.
- Layer 5: alerts on any change to payee records; immutable log.
- Score: likelihood 4, impact 5, highest in the register, so it is red-teamed first with a crafted phishing email.

## Pitfalls

- Modeling only the model layer and ignoring memory, plug-ins and the inter-agent channel.
- Treating each layer in isolation without cascade tracing.
- A threat model frozen at design time while tools and data sources keep changing.
- Scoring without considering how easy the exploit is for an outsider.
