# Protecting Data in Agentic Systems

## Contents
- Why data is the soft target
- Privacy and encryption
- Provenance and integrity
- Integrity verification workflow
- Handling sensitive data
- Tamper-evident audit trails
- Checklist
- Pitfalls

## Why data is the soft target

Agents pull from many sources, pass data between each other, cache intermediate results and write logs. Every hop is a chance to leak, corrupt or over-collect. Data protection is therefore a precondition for trust and compliance, not an add-on. Work through three areas in order: confidentiality (privacy and encryption), trustworthiness (provenance and integrity), and disciplined handling of sensitive categories.

## Privacy and encryption

- **At rest**: AES-256 for databases, object storage and also the temporary buffers and memory stores agents use. Pair with RBAC and fine-grained permissions so only the intended agents and people can decrypt.
- **In transit**: TLS on every link between agents, APIs and stores; for highly sensitive flows add mTLS so both sides prove identity. Aim for end-to-end protection rather than termination at an intermediate proxy that stores plaintext.
- **Minimization**: encryption limits who can read data, minimization limits what exists to read. Design each agent to receive only the fields its task needs; use anonymization or pseudonymization to keep analytic utility without identities. This also eases GDPR and CCPA obligations.
- **Retention and deletion**: logs, intermediate outputs and caches often hold sensitive fragments. Encrypt them, monitor them and purge them on a defined schedule.
- **Governance**: define how data may move between agents and subsystems; audit access logs; verify encryption standards are applied across all workflows; review privacy-policy compliance regularly.

## Provenance and integrity

- **Provenance** answers: where did this come from, what processed it, who or what changed it, and is it still original? Capture timestamps, source IDs, transformation logs and signatures as metadata alongside the payload.
- **Integrity** answers: has it changed since it was recorded? Use cryptographic hashes (SHA-256) as fingerprints; any bit change breaks the match. Digital signatures add proof of origin on top of proof of non-modification.
- **Immutable storage**: append-only logs or ledgers let agents verify that historical records (for example financial transactions) were not edited after entry.
- **Third-party and multiparty data**: add independent checks before ingestion, such as cryptographic attestation of API responses, or cross-verification of the same fact across several independent sources (federated trust).
- **Real-time checks before acting**: validate hashes, check timestamps for staleness or replay, and compare replicas for consistency before an agent executes a consequential step. Alert on mismatches so a human or another agent can step in.

High-stakes domains (finance, healthcare, critical infrastructure) should treat unverifiable data as unusable for actions, even if it is fine for drafting.

## Integrity verification workflow

1. On receipt, compute a SHA-256 digest of the payload.
2. Sign it with an asymmetric key (RSA or ECDSA) belonging to the ingesting service.
3. Store digest and signature in a metadata layer separate from the payload.
4. At every downstream stage, recompute and verify; on mismatch, halt that item and raise an automated alert.

In multiagent pipelines, put the verification step at each hand-off (a flow tool such as Apache NiFi can host it as a processor). For training or fine-tuning data, batch-verify dataset hashes against a manifest so poisoned files never enter training.

Original sketch:

```python
import hashlib, hmac

def fingerprint(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()

def verify_stage(payload: bytes, meta: dict, verify_sig) -> bool:
    digest = fingerprint(payload)
    if not hmac.compare_digest(digest, meta["sha256"]):
        return False                      # tampered or corrupted
    return verify_sig(meta["signer"], digest, meta["signature"])
```

## Handling sensitive data

Sensitive data includes PII, financial records, health data, proprietary intelligence and confidential communications.

- **Minimize per task**: a clinical-triage agent can work with pseudonymous patient IDs plus treatment history; it does not need names or addresses.
- **RBAC and ABAC**: roles grant categories of data; attributes (purpose, region, data classification, time) refine them. Example: support agent sees interaction history only; billing agent sees payment details only.
- **Granular verbs**: grant read-only or write-only where possible instead of full access.
- **Encryption everywhere**: TLS in transit between agents, APIs and databases; AES-256 at rest.
- **Log hygiene**: sensitive values must never appear in plaintext in logs, stack traces, error messages or debug dumps. Enforce redaction in the logging layer, audit logs regularly, and run anomaly detection over access patterns.
- **Retention**: automated deletion once the purpose is served, including caches and intermediate artifacts, aligned with GDPR and CCPA.
- **Cross-boundary sharing**: agents working across organizations or with third-party plug-ins operate under explicit data-sharing agreements. Where parties must compute jointly without revealing raw data, consider secure multiparty computation (SMPC) or federated learning.
- **People**: train developers and operators on common leak paths (misconfigured endpoints, verbose errors) and define accountability and escalation for breaches.

## Tamper-evident audit trails

Without resorting to blockchain:
- **Hash chaining / Merkle trees**: each entry includes the hash of the previous one (or is rolled into a Merkle root), so any retroactive edit is detectable by walking the chain.
- **Event sourcing**: record every state change as an immutable event, for example in append-only Kafka topics; agents or auditors can replay history to reconstruct and check a workflow.
- **Search and visualization**: an ELK-style stack makes the trail queryable for investigations.

```python
import hashlib, json

def append(chain: list, event: dict) -> dict:
    prev = chain[-1]["hash"] if chain else "0" * 64
    body = json.dumps(event, sort_keys=True)
    entry = {"event": event, "prev": prev,
             "hash": hashlib.sha256((prev + body).encode()).hexdigest()}
    chain.append(entry)
    return entry
```

## Checklist

- [ ] Data inventory per agent with justification for each sensitive field
- [ ] AES-256 at rest including caches and memory; TLS everywhere; mTLS on sensitive hops
- [ ] RBAC plus ABAC; read-only/write-only where feasible
- [ ] Pseudonymization or anonymization before model context where possible
- [ ] Hash-and-sign at ingestion; verification at each hand-off; alerts on mismatch
- [ ] Attestation or multi-source cross-checks for third-party data
- [ ] Log redaction enforced centrally; regular log audits
- [ ] Retention schedule with automated purge of logs, intermediates, caches
- [ ] Tamper-evident audit trail (hash chain or event sourcing)
- [ ] Data-sharing agreements for external parties; SMPC or federated options assessed
- [ ] Named owners and breach escalation procedure

## Pitfalls

- Encrypting the database but leaving the vector store, agent memory or debug logs in plaintext.
- Passing a full customer record into the prompt because it was convenient.
- Trusting a retrieved document because it came from an internal index, without provenance.
- Retention policies that cover primary tables but not caches and traces.
