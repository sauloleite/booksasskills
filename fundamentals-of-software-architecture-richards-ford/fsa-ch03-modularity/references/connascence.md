# Connascence

## Contents
- What it is and why architects use it
- Static forms (weakest to strongest)
- Dynamic forms
- Properties: strength, locality, degree
- Rules for improving modularity
- Refactoring playbook with examples
- Using the vocabulary in reviews

## What it is and why architects use it

Meilir Page-Jones (1996) introduced connascence as a precise vocabulary for kinds of coupling. It is not a counting metric like Ca/Ce; it names the nature of a dependency and hints at its consequences.

Definition: two elements are connascent when changing one forces a change in the other to keep the system correct.

Value for architects is the same as for design patterns: a short name replaces a long explanation. "This is connascence of position across a service boundary" says what is wrong and which way to fix it.

## Static forms (discoverable in source code; listed roughly weakest to strongest)

| Form | Elements must agree on | Example | Typical remedy |
|---|---|---|---|
| Name | the name of something | method and parameter names | already the weakest; rename with IDE refactoring |
| Type | the type of something | parameter typed as `Money` | fine; selective typing exists even in dynamic languages (e.g. Clojure Spec) |
| Meaning (Convention) | what a value signifies | status `3` means "shipped"; a homemade TRUE = 1 | named constant or enum (moves to Name) |
| Position | the order of values | `book(seat, passenger)` called with arguments swapped; types match, meaning breaks | named parameters, parameter object, distinct types |
| Algorithm | the same algorithm on both sides | client and server must compute an identical hash or checksum | single shared implementation, or a protocol that carries the result instead of recomputing |

Static connascence is the source-level view of afferent and efferent coupling.

## Dynamic forms (visible only at run time; generally stronger than static)

| Form | Elements depend on | Example | Typical remedy |
|---|---|---|---|
| Execution | order of calls | an object must be fully configured before `send()`; setting a field afterward is silently ignored | builders, constructors that require all inputs, immutable objects |
| Timing | when things run | race between two threads | locks, single writer, message ordering |
| Values | values that must change together | four corner points of a rectangle; the same value replicated across separate databases | derive values from one source, invariants in one place, transactions or sagas across stores |
| Identity | referencing the same instance | two components updating one shared queue or cache | single owner with an API, explicit ownership |

Connascence of values across distributed databases is the expensive case: the values must all change or none do, which drags in distributed transactions or compensation logic.

## Properties: strength, locality, degree

- **Strength:** how hard the coupling is to refactor. Prefer static over dynamic, because static forms can be found by reading code and fixed with tooling. Within each group, move toward the weaker forms above (Meaning to Name is the classic easy win).
- **Locality:** how close the coupled elements are. Strong connascence inside one class or module is tolerable; the same connascence across modules, services or teams is a design smell. Page-Jones anticipated what DDD bounded contexts later made mainstream: keep implementation coupling inside a narrow boundary.
- **Degree:** how many elements are affected by a change. Strong coupling between two classes is a small problem; the same coupling touching fifty is large. Code bases grow, so a low degree today tends to rise.

Evaluate strength and locality together: a strong form close by beats a weaker-looking form spread far apart.

## Rules for improving modularity

Page-Jones' three guidelines, paraphrased:
1. Reduce total connascence by splitting the system into encapsulated units.
2. Reduce whatever connascence still crosses those unit boundaries.
3. Concentrate connascence inside the boundaries (that is what cohesion looks like in this vocabulary).

Jim Weirich's two rules (2012), paraphrased:
- **Degree rule:** refactor strong forms into weaker forms.
- **Locality rule:** the farther apart two elements are, the weaker their connascence should be.

Architecture reading: across service or component boundaries aim for name and type only (stable named contracts). Push meaning, position, algorithm, execution, timing, values and identity inside a boundary.

## Refactoring playbook with examples

1. Identify the form (use the tables).
2. Check locality: same function, class, module, component, service, or organization?
3. Check degree: how many sites must change together?
4. If it crosses a boundary or has high degree, refactor toward a weaker form or pull the elements inside one boundary.

Meaning to Name (original snippet):

```python
# before: callers must know 3 means shipped
if order.status == 3: notify(order)

# after
from enum import Enum

class Status(Enum):
    PENDING = 1
    PAID = 2
    SHIPPED = 3
if order.status is Status.SHIPPED: notify(order)
```

Position to Name:

```python
# before: reserve("Silva, A", "22C") vs reserve("22C", "Silva, A") both type-check
def reserve(passenger: str, seat: str): ...

# after: keyword-only arguments make order irrelevant
def reserve(*, passenger: str, seat: str): ...
```

Execution to Type (make invalid order unrepresentable):

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Message:
    to: str
    sender: str
    subject: str
    body: str

def send(msg: Message): ...   # no half-configured object can be sent
```

Values across services: instead of each service keeping its own copy of a customer's credit limit, let one service own it and others ask or subscribe to change events, accepting eventual consistency where the business allows.

## Using the vocabulary in reviews

- Replace "please don't hardcode that string" with "connascence of meaning; lift it to a named constant".
- In architecture reviews, list each cross-boundary dependency with its connascence form; anything stronger than type across a service boundary needs a justification in the decision record.
- In migration planning, dynamic connascence across planned boundaries (shared mutable state, ordering assumptions, replicated values) is the main cost driver; find it before drawing service lines.
