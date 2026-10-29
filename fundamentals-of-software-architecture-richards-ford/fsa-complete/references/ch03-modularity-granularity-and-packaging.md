# Modularity, granularity and packaging

## Why modularity is an architecture concern

- Code structure decays on its own. Treat modular soundness like an energy budget: unless someone keeps investing in it (reviews, refactoring, automated checks), the structure drifts toward disorder.
- Modularity is an implicit architecture characteristic. Stakeholders almost never write "keep module boundaries clean" into requirements, yet every long-lived code base depends on it. The architect must raise it unprompted.
- Most structural analysis tools (coupling metrics, fitness functions, dependency visualizations) assume a meaningful notion of module. If modules are arbitrary, the metrics are noise.

## Modularity versus granularity

| Concept | Question it answers | Typical failure |
|---|---|---|
| Modularity | Should this system be divided, and along which seams? | Lumping everything in one undifferentiated unit |
| Granularity | How large should each resulting piece be? | Pieces so small they must constantly call each other |

Guidance:
- Breaking a system apart is usually healthy; picking the wrong size for the parts is where projects get hurt. Richards' slogan captures it: "Embrace modularity, but beware of granularity."
- Pieces that are too fine grained become tightly coupled to each other. The resulting antipatterns are spaghetti architecture, the distributed monolith, and the big ball of distributed mud.
- Test for wrong granularity by looking at coupling between the pieces, not at their size alone. If two services must change, deploy or be called together for most features, they are probably one piece split in two.

Diagnostic questions when someone proposes splitting something:
1. Which operations would now cross the new boundary, and how often?
2. Would the split create shared data that both sides must update together?
3. Does each side have a reason to change independently (different rate of change, team, scaling need)?
4. If the answers point to heavy cross talk, keep it together (or split differently).

## What "module" means here

- A module is a logical grouping of related code: a set of classes in an OO language, a set of functions in a structured or functional one. Language constructs (Java package, .NET namespace, Python package, Go package, JS/TS module, Rust crate) are implementations of the idea.
- Logical grouping is not the same as physical separation (separate deployables, JARs, services). Keep the two apart in analysis: a monolith can be well modularized, and a set of services can be badly modularized.
- Loose logical partitioning inside a monolith is convenient early but is the thing that blocks a later decomposition. Before any migration, assess logical modularity first.
- Languages offer several overlapping packaging levels (function, class, package, plus metaprogramming hooks), each with its own visibility rules. Developers often pick inconsistently, so architects should set conventions for which construct represents an architectural component.
- Tightly coupled packages are hard to reuse individually. Packaging decisions are therefore architecture decisions, not just style.

## Namespaces

- A namespace gives every asset a unique fully qualified name so that identically named things in different contexts do not collide (internet addressing is the everyday analogy).
- In most languages the modularity mechanism doubles as the namespace. Sometimes the namespace is mirrored in the file system (Java requires directories to match package names).
- Mirroring the namespace in the directory tree removes ambiguity cheaply but becomes cumbersome at scale. Java's later archive-based classpath reintroduced the possibility of duplicate names across archives, which is why class loader conflicts became a notorious debugging chore. Lesson: a mechanism that guarantees uniqueness only holds if every distribution channel respects it.

## Historical context (why so many grouping schemes exist)

- Dijkstra's 1968 critique of GOTO pushed the industry toward structured programming (Pascal, C) in the 1970s.
- Structured languages lacked a good way to group related routines, so the mid-1980s saw explicitly modular languages (Modula, Ada) with modules but no classes.
- Object orientation then took over, but packages and namespaces survived as a separate layer. Modern languages carry modular, OO and functional mechanisms side by side, each with its own scoping quirks. The overlap is largely about preserving how developers think, not about code compatibility.

## From modules to components

- In the rest of the book, "component" is the architect's word for a module: the basic building block of an architecture.
- Deciding how to derive components from the problem domain (and whether each is logically or physically separate) is a later topic; before that the book covers architecture characteristics and their scope.

## Worked example (invented)

A team proposes splitting a "Notifications" module into three services: Templates, Channels (email, SMS, push) and Preferences.
- Every send requires all three: look up the preference, render the template, dispatch on a channel. Splitting would add two network hops and shared versioning on every call.
- Templates change weekly (marketing); Channels change rarely; Preferences change with privacy regulations.
- Verdict: keep Channels and Preferences in-process with the sender; consider extracting Templates only if marketing needs independent deployment. This embraces modularity (clear internal modules) while avoiding over-fine granularity.
