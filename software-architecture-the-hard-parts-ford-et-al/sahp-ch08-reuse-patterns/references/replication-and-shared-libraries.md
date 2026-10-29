# Code replication and shared libraries

## Contents
- Context: why reuse is hard once a system is distributed
- Code replication
- Shared libraries: granularity
- Shared libraries: versioning, communication and deprecation
- Strengths, weaknesses and fit
- Worked example
- Pitfalls checklist

## Context

Inside a monolith, sharing a class is just an import. After decomposition, every shared piece raises the question of how it reaches each service and what happens when it changes. Slogans such as "share nothing" or WET (write everything twice, the counterpoint to DRY) push teams toward avoiding reuse, but some sharing is unavoidable. The chapter offers four mechanisms; this file covers the two compile-time ones. The underlying tension mirrors service granularity: you are always balancing how many dependencies you must manage against how far a single change spreads.

## Code replication

**What it is.** Each service repository gets its own copy of the shared source. Nothing is shared at build or run time.

**History.** It spread in early microservices adoption, when bounded context was misread as "never share any code". It mostly failed in practice because fixes had to be hunted down and applied in every copy.

**When it is still reasonable.**
- Tiny, static, effectively defect-free code. The canonical case is a marker annotation or attribute that tags the class acting as a service's entry point; it carries no logic, and other metadata (service type, domain, bounded context) can hang off it.
- A one-off class where building, publishing and versioning a library would cost more than the copies.
- Migration from a monolith: copy a general utility class into every new service and let each service delete what it does not use or adapt the rest. This is the reuse analogue of tactical forking (each copy evolves for its own context).

**Costs.** Updates for bugs or new requirements must be repeated everywhere, copies drift apart, and there is no version to tell you which service has which behavior. Its one structural benefit is that the bounded context stays intact and no coupling is introduced.

**Rule.** Use it last, after considering library, service and sidecar.

## Shared libraries: granularity

**What it is.** A separately built artifact (JAR, DLL, package, gem, wheel) bundled into each consuming service at build time.

**Two opposing forces.**
- *Dependency management*: how many artifacts each service must declare, track and upgrade.
- *Change control*: how many services are dragged into retesting and redeploying when something in a library changes.

| Library shape | Dependency management | Change control |
|---|---|---|
| One coarse library holding everything | Easy: one dependency per service | Poor: any edit eventually forces every consumer to adopt the new version when the old one is retired |
| Many fine, function-oriented libraries | Harder: a matrix of services to libraries that can resemble a distributed big ball of mud | Good: a change touches only the services that use that library |

Scale amplifies both problems. With a handful of services either shape is tolerable; with hundreds of services and dozens of libraries the wrong choice becomes unmanageable.

**Recommendation.** Lean toward smaller libraries partitioned by function, accepting dependency overhead in exchange for change control. Pull stable areas (formatting, authentication and authorization helpers, annotations) into their own artifacts so that churn in volatile code (for example, pricing calculators) never forces upgrades of the stable parts. Avoid the "common-everything" artifact.

## Shared libraries: versioning, communication and deprecation

**Always version.** Versioning gives backward compatibility and agility. Example of the mechanism: a rules library used by twelve services; one service needs a rule tweak urgently. With versioning, that service bumps its dependency and ships alone. Without it, all twelve must be retested and released together.

**Versioning is not simple.** The authors joke that "versioning is easy" deserves a place among the fallacies of distributed computing. The hidden work:

1. *Communicating changes.* Teams need to learn that a new version exists, what changed, and whether they are affected. Artifact repositories help store and annotate versions but do not replace deliberate notification to the right teams at the right time.
2. *Retiring old versions.* Decide how many back versions remain supported.

**Deprecation strategies.**

| Strategy | How it works | Upside | Downside |
|---|---|---|---|
| Per-library (custom) | Each library gets a support window matched to its change rate. A library that rarely changes might keep two or three versions; one that changes weekly might keep around ten. | Consumers upgrade at a sensible pace | Someone must track and enforce a policy per library, which is real ongoing effort |
| Global | One cap for all libraries (for example, four back versions). | Simple to govern | Volatile libraries force constant retest and redeploy cycles, hurting team velocity |

The per-library approach is usually preferable because libraries change at very different rates.

**Policy override.** A critical defect or breaking change makes every policy moot: all consumers must move to the new version almost at once. The finer the library, the fewer services this emergency touches.

**Pin versions.** Do not declare a floating "latest" dependency. During an urgent hotfix, the build silently picks up whatever newest version exists, which may be incompatible and turn a quick fix into a development and test effort.

## Strengths, weaknesses and fit

Strengths: changes can be versioned and adopted per consumer; binding happens at build time, so integration errors surface early rather than at runtime; good agility for shared changes; no effect on latency, scalability or fault tolerance of callers.

Weaknesses: dependency graphs get messy as libraries multiply; a polyglot estate needs one implementation per language (duplication across platforms); deprecation and version communication take sustained effort.

Fit: homogeneous technology stacks and shared code whose change rate is low to moderate.

## Worked example (invented)

A logistics company has 30 JVM services sharing a `core-common` artifact containing address normalization, date formatting, JWT helpers, and route-cost calculators. Route-cost rules change roughly every sprint; the rest changes a few times a year.

- Split into `addr-normalize`, `formatting`, `auth-helpers`, and `route-cost`. Only 6 services use `route-cost`.
- Deprecation: `auth-helpers` and `formatting` keep 3 versions; `route-cost` keeps 8 so its consumers are not forced to upgrade every sprint.
- Release notes for each version go to a channel subscribed to by owning teams of consumers, generated from the dependency graph.
- All services pin exact versions; a CI rule rejects version ranges or "latest".
- A small marker annotation for entry-point classes is copied into each repo rather than published, because it never changes.

## Pitfalls checklist

- [ ] One "shared stuff" artifact that every service must upgrade together.
- [ ] Library split so finely that the dependency matrix is unmanageable for the number of services.
- [ ] No version, or versions published silently with no consumer notification.
- [ ] One global deprecation window applied to libraries with very different change rates.
- [ ] Floating "latest" dependencies.
- [ ] Replicating code that contains real logic likely to need fixes.
- [ ] Using a library for code consumed from several languages (consider a service instead).
