# Contracts in Microservices and Consumer-Driven Contracts

## Contents
- The three decisions for every service interaction
- Coupling levels for shared domain data
- Consumer-driven contracts: push versus pull
- Strengths and weaknesses of CDC
- Readiness checklist
- Sketch of a CDC test
- Pitfalls

## The three decisions for every service interaction

For each interaction decide separately: the semantics (which information crosses), the implementation (how it is transported and encoded), and the coupling strength (how strict the contract is). Mixing these up leads to choosing a protocol and inheriting its coupling by accident.

## Coupling levels for shared domain data

Scenario: two services, each with its own transactional boundary, both need customer address data.

**Option A, tight.** Same stack, shared typed contract via a platform RPC or gRPC, passing a shared `Customer` type. High confidence in fidelity, but the services now evolve together, which works against a core microservices goal.

**Option B, loose.** Each service keeps its own bounded-context model of `Customer`. Integration passes only the relevant values as name/value pairs. Benefits:
- Each team reshapes its internal model as aggressively as it likes.
- Implementation independence: if one team migrates to another language or platform, the other is unaffected, because every platform can read and write name/value pairs.

The cost of Option B is fidelity: nothing guarantees the right keys and value types arrive. Two remedies: overlay a schema (for JSON, JSON Schema) where it fits, or govern the integration with consumer-driven contract tests acting as fitness functions.

## Consumer-driven contracts: push versus pull

Conventional integration is a push model: the provider decides what to emit and consumers adapt. CDC inverts this into a pull model:

1. Each consumer writes a contract (as executable tests) describing exactly the data it needs from the provider.
2. The consumer hands those tests to the provider team.
3. The provider runs all consumer contracts in its CI/CD pipeline and must keep them passing; a red contract blocks release.

With several consumers needing overlapping slices of one provider, each contributes its own contract. Each team can make its contract as strict or as loose as it wants, and fidelity is checked at build time, which recovers much of what strict schemas offered. Tooling exists to automate this (Pact and Spring Cloud Contract are well known examples).

CDC is popular in microservices precisely because it solves two goals that look contradictory: loose coupling and governed integration.

## Strengths and weaknesses of CDC

Strengths:
- **Loosest coupling with safety.** Payloads stay as name/value pairs, so implementations change with minimal breakage risk.
- **Strictness is tunable, even beyond schemas.** Schemas typically express types; fitness functions can also assert value ranges, cross-field rules, formats and business invariants (for example, "discount percent between 0 and 40 and only when tier is gold").
- **Evolvable.** Implementation details can change without disturbing the information exchanged.

Weaknesses:
- **Needs engineering maturity.** It only works when every team runs contract tests in CI and treats failures as blocking. Teams that ignore red builds or run tests irregularly leave broken integrations undetected for long periods.
- **Two mechanisms instead of one.** Name/value payloads plus a separate verification layer means more moving parts than a single schema tool, even though each part is simple.

Deciding factor: team maturity and appetite for decoupling with loose contracts plus CDC, versus accepting more complexity and coupling for the certainty of strict contracts.

## Readiness checklist

Adopt CDC only if most answers are yes:
- Do all provider teams run CI on every change?
- Is a failing contract test treated as a release blocker, organization-wide?
- Is there a shared place (broker or repository) where consumer contracts are published and versioned?
- Do consumer teams have the habit and time to keep their contracts current?
- Is there an escalation path when a provider must break a consumer contract?

If several answers are no, prefer stricter schema-based contracts until the practice matures.

## Sketch of a CDC test

Framework-agnostic illustration of a consumer's expectation run in the provider build:

```python
# Contract owned by the Loyalty service, executed in the Orders provider pipeline.
def test_order_completed_event_meets_loyalty_needs(provider):
    event = provider.sample_event("order_completed")
    assert isinstance(event.get("customerId"), str) and event["customerId"]
    assert isinstance(event.get("totalCents"), int)
    assert 0 <= event["totalCents"] <= 10_000_000      # range, beyond a type check
    assert event.get("currency") in {"BRL", "USD", "EUR"}
    # Loyalty ignores every other key, so the provider may add or remove them freely.
```

Note what is absent: no assertion on fields Loyalty does not use. That absence is what keeps the coupling need-to-know.

## Pitfalls

- Consumers asserting on the entire payload, recreating stamp coupling inside the tests.
- Contracts that nobody updates after the consumer stops using a field, freezing the provider unnecessarily.
- Treating CDC as optional or advisory; a non-blocking contract test gives false confidence.
- Assuming CDC handles semantic changes automatically; meaning changes still need human coordination.
