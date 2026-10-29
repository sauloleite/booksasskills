## Contents

- Why model sagas as state machines
- Designing a saga state machine
- The transition table
- Worked example (invented): equipment rental
- Sagas must be built, not bought
- Tagging services with saga membership
- A saga inventory tool
- Pitfalls

# Saga State Machines and Saga Management Techniques

## Why model sagas as state machines

A saga state machine enumerates every path a distributed workflow can take: one entry state that launches the saga, intermediate states, the transitions between them, and the action fired on each transition. It is the backbone of the state-management approach: because the coordinator always knows the current state, it can respond to the user early and repair failures later through retries, automated correction or human intervention.

## Designing a saga state machine

1. **Write the happy path as numbered business steps** (request created, resource assigned, work done, follow-up sent).
2. **Turn each step outcome into a state.** Name states after facts that are true ("ASSIGNED"), not after actions in progress.
3. **Add one explicit entry state and at least one terminal state.** Errors before the entry transition mean the saga never starts; that is a validation failure, not a saga state.
4. **For each state, list every possible outcome.** Many states have a single outcome and simply wait (for example, waiting until a resource becomes available). Others branch (completed versus needs reassignment).
5. **Model waiting explicitly.** If a step cannot proceed (nobody available, target unreachable), the saga stays in its current state until it can. Decide whether that wait needs a timeout and escalation.
6. **Model loops.** Reassignment paths route back into an earlier state; make sure a loop cannot spin forever without escalation.
7. **Add an error state for each failure of a non-critical step** (for example, the main work succeeded but a notification did not). The error state's only exit is a retry that eventually reaches the terminal state.
8. **Check structure:** every state reachable from the entry; every non-terminal state has an exit; every state can reach a terminal state.

## The transition table

Capture the machine as a table of initiating state, target state and the action to perform when that transition happens. Developers implement triggers and error handling straight from it, either inside the orchestrator or, with choreography, distributed across the participating services. The table also doubles as test-case inventory: each row is at least one test.

## Worked example (invented): equipment rental

Business steps: a customer reserves equipment, a depot allocates a unit, the unit is dispatched, the customer confirms delivery, the rental is invoiced, a deposit refund is issued at return.

| From | To | Action on transition |
|---|---|---|
| START | RESERVED | Allocate a unit at the nearest depot |
| RESERVED | ALLOCATED | Schedule dispatch |
| ALLOCATED | DISPATCHED | Notify customer with tracking |
| DISPATCHED | DELIVERED | Start rental clock |
| DISPATCHED | REALLOCATE | Pick another unit (damaged or lost in transit) |
| REALLOCATE | ALLOCATED | Schedule dispatch |
| DELIVERED | RETURNED | Issue invoice and deposit refund |
| RETURNED | CLOSED | Saga complete |
| RETURNED | REFUND_PENDING | Retry deposit refund |
| REFUND_PENDING | CLOSED | Saga complete |

Notes: RESERVED waits until a unit is free; REALLOCATE loops back to ALLOCATED; REFUND_PENDING is the error state that lets the customer's return complete immediately while the payment provider outage is repaired in the background.

Minimal orchestrator sketch (original, language-neutral Python):

```python
TRANSITIONS = {
    ("RETURNED", "ok"): ("CLOSED", None),
    ("RETURNED", "refund_failed"): ("REFUND_PENDING", "retry_refund"),
    ("REFUND_PENDING", "ok"): ("CLOSED", None),
}

def advance(saga, outcome, actions):
    key = (saga.state, outcome)
    if key not in TRANSITIONS:
        raise ValueError(f"illegal transition {key}")
    saga.state, action = TRANSITIONS[key]
    saga.history.append(key)          # audit trail of the saga
    if action:
        actions.schedule(action, saga.id)  # background, idempotent
    return saga.state
```

## Sagas must be built, not bought

There is no product that drops distributed transactions into a system the way an ACID transaction manager does for one database. Architects and developers have to design, code and maintain each saga. That makes visibility of which sagas exist, and which services take part in each, a governance concern.

## Tagging services with saga membership

Use a language-level marker (Java annotations, C# attributes, Python decorators, TypeScript decorators, or a manifest file where no such feature exists) to declare which sagas each service participates in. The marker has no runtime behavior; its value is documentation that lives with the code and can be queried.

Recommended setup:

- One central enumeration of all sagas in the application context, so the full list lives in a single place.
- A marker on each service entry point naming one or more sagas from that enumeration.

Original illustration (Python, framework-agnostic):

```python
from enum import Enum

class Saga(Enum):
    PLACE_ORDER = "place_order"
    RETURN_ITEM = "return_item"

def saga(*names):
    def mark(cls):
        cls.__sagas__ = set(names)
        return cls
    return mark

@saga(Saga.PLACE_ORDER, Saga.RETURN_ITEM)
class InventoryEntrypoint: ...
```

Benefits:

- **Test scoping**: changing a service tells you which sagas need regression testing.
- **Impact analysis**: shows which other services might be affected by a change in a saga participant.
- **Shared vocabulary**: business analysts can ask which services implement a given business transaction.

## A saga inventory tool

With markers in place, a small command-line tool can walk the repository, find every class or module flagged as a service entry point, read its saga markers, and answer questions such as "which services take part in PLACE_ORDER?" or "which sagas does the inventory service touch?". This is straightforward to write and can run in CI to:

- Fail the build when a marker names a saga missing from the central enumeration.
- Flag sagas with only one participant (probably not distributed, or a missing marker).
- Publish an always-current saga-to-service map for architecture documentation.

## Pitfalls

- State machines that only model the happy path; errors then fall back to ad hoc compensation.
- Wait states with no timeout or escalation, so sagas silently stall.
- Saga markers maintained by hand in a wiki instead of beside the code; they drift.
- Treating the saga enum as optional; without a single list, nobody knows how many distributed transactions the system has.
