# Modern Use: ESB Integration, Risks, Cloud and Governance

## Contents
- Where the style still fits
- Cloud considerations
- Risks: then and now (Accidental SOA)
- Governance and testing
- Fitness function: integration write-direction guard
- Playbook: introducing an ESB without sliding into SOA

## Where the style still fits

The full style is mostly historical, but its building blocks remain useful for integration architecture:
- An ESB combines an integration hub (communication, protocol and contract transformation) with an orchestration engine (workflows across endpoints).
- Layers of indirection let an enterprise service be backed by an integration point, a packaged product, legacy code or new bespoke code, without callers knowing which.
- The client asks the bus; the bus chooses the enterprise services, their sequence, and the data to combine; enterprise services talk via APIs to whatever implements them.

Good fit: organizations with legacy or packaged systems (ERP, CRM, mainframe) that must cooperate with modern systems, combining results and aggregating behavior. Poor fit: using the bus as the backbone for all new domain behavior.

Historical perspective: the style was an inventive answer to integration at scale under that era's licensing and hardware limits. Keep the parts that still work, and internalize why the rest failed.

## Cloud considerations

The original style predates the cloud by decades and has no cloud-native form. Its modern role as an integration layer, however, suits hybrid estates where cloud services and on-premises systems must join shared workflows. Use it as glue between cloud and on-prem participants, not as the host of domain logic.

## Risks: then and now

Historical risks: high cost, multiyear timelines, and systems that turned out very hard to maintain and change. Decisions were made high in the hierarchy. Rather than declaring failure, most companies reshaped these systems into integration architectures with clearer boundaries aligned to DDD.

Modern risk, the Accidental SOA antipattern: an ESB introduced for integration gradually absorbs more and more logic until the organization has unintentionally built a full orchestration-driven SOA. Countermeasures:
- Define explicit encapsulation boundaries for what orchestration may do.
- Watch transactional boundaries closely; do not let the bus own transactions across domain services.
- Keep domain rules inside bounded contexts; the bus routes, transforms and sequences.

## Governance and testing

In the style's heyday, testing happened mostly at formal QA stages; tools rarely supported testing individual parts, and mocking or stubbing the bus machinery was clumsy and inconsistent. Governance meant manual heavyweight frameworks, meetings and code reviews; automating it was unheard of.

Modern approach: when you use an ESB strategically, wrap it in automated fitness functions that stop data or bounded contexts from leaking into parts of the ecosystem where they do not belong.

## Fitness function: integration write-direction guard

Scenario pattern: a bus coordinates sources that should be read-only (say, an ERP package and a sales tool) with a modern target that is the only legitimate write destination (say, accounting microservices).

Steps:
1. First add a fitness function guaranteeing that every integration interaction is logged in a consistent structure (source, operation, target, timestamp). The guard depends on it.
2. Over a rolling window (for example, the last 24 hours), scan each source's interactions.
3. Fail on any write-type operation whose target is not on the allowed list for that source.
4. Run it on a schedule and in the deployment pipeline so violations block or alert.

Illustrative check (original sketch):

```python
def violations(entries, allowed_writes, write_ops=("update", "create", "delete")):
    bad = []
    for e in entries:
        if e["operation"] in write_ops:
            if e["target"] not in allowed_writes.get(e["source"], set()):
                bad.append(e)
    return bad

allowed = {"erp": {"accounting"}, "sales": {"accounting"}}
```

The bundled script `scripts/integration_flow_guard.py` implements this check against a JSON Lines log.

Variants worth adding: no direct calls that bypass the bus between named contexts; no domain entity schema crossing a context boundary; bounded workflow depth (number of orchestrated steps) to detect logic creeping into the bus.

## Playbook: introducing an ESB without sliding into SOA

1. State the integration problem: which legacy or packaged systems, which modern ones, which data flows and directions.
2. Confirm you need both a hub (protocol and contract transformation) and an orchestrator; if only one, pick a lighter tool.
3. Write down what the bus may do (route, transform, sequence, aggregate) and may not do (own domain rules, own cross-service transactions, host canonical entity models).
4. Assign ownership so the integration team does not become a mandatory gate for domain changes.
5. Add the logging fitness function, then direction and boundary guards.
6. Review periodically for Accidental SOA signs: growing workflow count, business rules in transformations, teams waiting on the integration team.
