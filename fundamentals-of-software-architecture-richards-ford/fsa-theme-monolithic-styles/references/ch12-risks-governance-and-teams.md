# Risks, Governance and Team Topologies

## Contents
- Risk register
- Error-handling playbook
- Contract management
- Structural governance with role tags
- Review checklist
- Team topology fit

## Risk register

| Risk | How it shows up | Root cause | Mitigation |
|---|---|---|---|
| Overloaded filters | A transformer also validates, routes or persists; filter code grows and becomes hard to replace | Convenience; unclear role ownership | Role tags, review against the one-role rule, split filters |
| Bidirectional communication | A filter calls back upstream, or waits for a downstream answer | Wrong style, or boundaries drawn in the wrong place | Re-cut filters; if the dialogue is inherent, change style (often event-driven) |
| Error handling | A failure mid-flow leaves unclear state; nobody knows how to exit or resume | Error paths not designed up front | Enumerate fatal conditions before defining the architecture (playbook below) |
| Contract drift | A changed payload silently breaks a downstream filter | Pipes treated as private details | Contract ownership, versioning, consumer tests |

The overarching danger is decay: once filters accumulate unrelated duties, the pipeline stops being a pipeline and becomes an unstructured monolith with none of the modularity benefits.

## Error-handling playbook

Errors are hard in pipelines because data has already moved through earlier filters when a later one fails. Do this before freezing the design:

1. List every condition that should abort the flow (bad input, missing reference data, downstream store unavailable, resource exhaustion).
2. For each, decide the exit: drop silently, divert to a dead-letter or quarantine sink, or halt the whole pipeline.
3. Decide recovery: replay from the producer, resume from a checkpoint, or manual intervention.
4. Make filters idempotent where replay or at-least-once execution is possible.
5. Remember that in a monolithic deployment one filter exhausting memory takes down every filter; isolate heavy filters if that is unacceptable.

## Contract management

- Treat every pipe as a published interface with a named owner.
- Prefer additive, backward-compatible changes; for breaking changes, version the contract and migrate receivers first.
- Run contract tests for each receiving filter whenever a sender changes its payload.
- Keep payloads small; large blobs increase coupling and slow the chain.

## Structural governance with role tags

Operational fitness functions (latency, throughput, availability) are specific to each system, so this chapter's governance focus is structural: is each filter doing only its role's job? That is hard to verify automatically (a tool cannot easily prove a tester really makes a continue-or-stop decision, or that a producer is really the start). The practical technique is metadata:

1. Define a role marker with the four values (producer, transformer, tester, consumer). Use whatever the language offers: Java annotations, C# attributes, Python decorators, TypeScript decorators.
2. Define a separate entry-point marker so multi-class filters have one obvious class that carries the role.
3. Require both markers on every filter entry point.
4. Optionally add light automated checks: every entry point has exactly one role; untagged classes do not receive pipe input; producers have no inbound pipe; consumers have no outbound pipe.

The markers do nothing at run time. Their value is context: a developer editing a class marked as a transformer is reminded not to add gating logic. It will not stop every violation, but it makes them visible in review.

Original Python illustration:

```python
from enum import Enum

class Role(Enum):
    PRODUCER = "producer"; TRANSFORMER = "transformer"
    TESTER = "tester"; CONSUMER = "consumer"

def filter_entrypoint(role: Role):
    def mark(cls):
        cls.__filter_role__ = role
        cls.__filter_entrypoint__ = True
        return cls
    return mark

@filter_entrypoint(Role.TRANSFORMER)
class ResponseTimeCalculator:
    def handle(self, event: dict) -> dict:
        return {**event, "p95_ms": compute_p95(event["samples"])}
```

A simple governance check then scans for classes with `__filter_entrypoint__` and verifies role-specific rules (for example, a transformer's `handle` always returns a payload, a tester's may return none).

## Review checklist

- [ ] Each filter entry point tagged with exactly one role.
- [ ] No transformer contains routing or drop logic.
- [ ] No tester mutates the payload.
- [ ] No callbacks or replies flow upstream.
- [ ] Fatal error list exists, with exit and recovery for each.
- [ ] Every pipe contract has an owner and tests on the receiving side.

## Team topology fit

The style is largely indifferent to team structure; it works with all four team types:

- **Stream-aligned**: a pipeline usually represents one journey through the system, so a single team can own it from producer to consumer, matching the shape of the work.
- **Enabling**: specialists can experiment by inserting an extra filter without disturbing the main flow. Example: in a trend-analysis pipeline, add a second transformer after the time-window selector that tries an alternative trend algorithm on the same data, side by side with the existing analyzer.
- **Complicated-subsystem**: a filter with hard internals (a pricing model, a signal-processing step) can be owned by specialists who only need to honor its input and output contracts; one-way handoffs keep their focus narrow.
- **Platform**: high modularity lets a platform team supply shared tooling, services, APIs and reusable task filters (connectors, serializers, observability wrappers) used across pipelines.
