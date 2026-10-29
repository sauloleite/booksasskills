# Securing the Foundation Model: Selection, Layered Defenses, Red Teaming

## Contents
- Model selection as a security decision
- Layered defensive techniques
- Benchmarking guardrails
- Red teaming program
- Red-team tooling
- From findings to fixes
- Worked example
- Pitfalls

## Model selection as a security decision

Evaluate candidates on five axes and record the reasoning, because the choice will be revisited.

| Axis | Trade-off | Decision hint |
|---|---|---|
| Capability fit | Big general models handle varied tasks but behave less predictably; small fine-tuned models are narrower and easier to monitor | Use the smallest model that reliably does the step |
| Openness / access | Open weights allow independent audit but ship with fewer guardrails and need hardening; proprietary APIs ship protections and support but are opaque | Open weights when audit and data control dominate; proprietary when you lack a team to harden |
| Deployment environment | On-prem or air-gapped removes external dependency risk; cloud gives scale and easier operations but needs strict IAM and encryption in transit and at rest | Highly sensitive data pushes toward on-prem/air-gapped |
| Compliance | Some use cases require attested properties (GDPR handling, SOC 2 controls) | Filter on certifications early; retrofitting is expensive |
| Explainability | Models whose reasoning is more inspectable make it easier to diagnose failure and abuse | Weigh higher for regulated or adverse-decision workloads |

Practical pattern: a **hybrid portfolio**. Route precise, high-stakes steps (classification, extraction, policy decisions) to specialized small models and route open-ended drafting or planning to a general model. This also limits how much damage a single compromised or misbehaving model can do.

Selection is continuous: re-run evaluations when a vendor updates a model, when new vulnerability classes appear, or when the agent gains new tools.

## Layered defensive techniques

Think of the model as an untrusted component sitting between two filters, behind an access gate, inside a sandbox.

1. **Input sanitization and validation**
   - Pattern filters for known attack phrasing, strict schema/syntax checks on structured inputs, rejection or quarantine of inputs carrying instructions.
   - PII detection and anonymization before text reaches the model (an open source option is the LLM Guard library, which bundles scanners for anonymization, banned substrings, toxicity and jailbreaks).
   - Tune detector thresholds empirically on your own traffic; defaults are a starting point.
2. **Prompt injection prevention**
   - Instruction anchoring: restate the governing rules and the role of untrusted text at the points where it matters, so data cannot easily masquerade as directives.
   - Rigid templates: untrusted content goes only into delimited slots and is labeled as data.
   - Context isolation: keep retrieved or third-party content in a separate channel or sub-call with no tool privileges.
3. **Output filtering and validation**
   - Keyword scans, toxicity classifiers, rule-based filters.
   - A postprocessing pipeline that checks outputs and proposed actions against business rules and safety constraints before anything reaches a user or a tool.
4. **Access control and rate limiting on model endpoints**
   - Authentication, role-based permissions, per-caller rate limits to stop brute-force probing and abuse.
   - Log and audit every model interaction so security can detect probing patterns.
5. **Sandboxing**
   - Run model-driven actions, plug-ins and external API calls in isolated environments so a misbehaving agent cannot trigger cascading failures across dependent services.

Short illustrative wrapper (original, framework-agnostic):

```python
def guarded_call(user_text, model, input_checks, output_checks, policy):
    for check in input_checks:            # e.g. pii_redact, injection_detector
        user_text, ok, reason = check(user_text)
        if not ok:
            return {"status": "rejected", "stage": "input", "reason": reason}
    reply = model(user_text)
    for check in output_checks:           # e.g. toxicity, secret_leak, schema
        ok, reason = check(reply)
        if not ok:
            return {"status": "blocked", "stage": "output", "reason": reason}
    if reply.get("action") and not policy.allows(reply["action"]):
        return {"status": "escalated", "stage": "policy", "action": reply["action"]}
    return {"status": "ok", "reply": reply}
```

Defenses must iterate: fold in lessons from adversarial testing, audits and new public techniques, and combine technical, operational and human controls.

## Benchmarking guardrails

- **Lakera PINT Benchmark**: open source, 4,314 inputs mixing multilingual injections, jailbreaks and hard negatives; yields a detection-accuracy score. Reported results spread widely (Lakera Guard 92.5%, Llama Prompt Guard 61.4%), which shows how much detectors differ.
- **BIPIA (Microsoft)**: focused on indirect prompt injection, with attack and defense sets.

How to use them: run your full guardrail stack (not just the classifier) against the benchmark, track the score over time, and add your own domain-specific cases. The field is young, so a good score is evidence, not proof, of protection.

## Red teaming program

Red teaming differs from functional QA: it asks how the system behaves under deliberate misuse, manipulation and edge cases rather than whether it computes the right answer.

Lifecycle (cyclical):
1. **Implement** the agent or change.
2. **Attack**: execute scenarios such as injection, jailbreaks, ambiguous or contradictory instructions, high-stakes decision prompts, attempts to extract secrets or break operating constraints.
3. **Evaluate**: score responses and actions; record reproductions.
4. **Mitigate**: change configuration, filters, prompts, training data or permissions.
5. Loop back; every fix becomes a regression test.

Synthetic stress data: use an LLM to generate inputs that deliberately violate developer expectations (malformed queries typical of your users, noisy text, skewed distributions, out-of-domain requests, adversarial manipulations). This simulates whole data environments, not just single prompts, and can run automatically in CI.

Humans plus machines: automated tools give breadth (thousands of variants), human red-teamers give creativity for subtle and social-engineering exploits, such as mimicking a trusted sender's tone to fool an operator. Use both.

Cadence: re-run after fine-tuning, model upgrades, new tools or new deployment contexts, since each changes the security profile. Keep red team, model developers and security operations in a shared loop.

## Red-team tooling

| Framework | Strength | Use it for |
|---|---|---|
| DeepTeam | Lightweight, extensible; automates jailbreak, injection and privacy-leak attacks and helps derive guardrails; custom multi-turn scripts | Multi-turn agent tests such as gradual context manipulation |
| Garak (NVIDIA) | Modular probe library, often compared to Nmap/Metasploit for LLMs; covers hallucination, leakage, injection, misinformation, toxicity, jailbreaks | Broad scans across many models or versions |
| PyRIT (Microsoft) | Orchestrators to generate attacks, scorers to judge responses, targets for many endpoints; multimodal and agentic support | Custom scripted campaigns, including tool-use and disclosure tests |

## From findings to fixes

- Document every finding with reproduction steps, affected component and observed impact.
- Prioritize by **severity x exploitability x real-world impact**; a trivially reproducible leak of customer data outranks an exotic jailbreak that yields only rude text.
- Feed results into model configuration, input/output filters and training or fine-tuning data.
- Report trends (classes of failure, time to fix) to leadership; red teaming is also an early warning system.

## Worked example

A bank deploys a document-QA agent. Selection: proprietary model in a private cloud region with SOC 2 attestation for drafting; a small fine-tuned classifier on-prem to decide whether a request touches account data. Defenses: PII redaction in, banned-instruction scan on retrieved chunks, output check for account numbers, per-user rate limit, retrieval sandbox with no write tools. Red team: PyRIT campaign with 2,000 synthetic malformed queries plus a human session on social engineering of the support staff. Top finding: instructions hidden in uploaded PDFs triggered summary leakage; fix by isolating retrieved text and adding the case to regression.

## Pitfalls

- Selecting a model on benchmark capability alone and treating security as a later wrapper.
- One filter at the input, none at the output.
- Thresholds copied from examples without calibration on real traffic.
- Red teaming once before launch and never again.
