## Contents
- Why "how" needs a method: the Elephant Migration anti-pattern
- The decision tree
- Component-based decomposition
- Service-based architecture as target or stepping stone
- Tactical forking
- Tactical forking trade-offs
- Choosing between the two
- Worked examples
- Decision record template
- Pitfalls

# Choosing and applying a decomposition approach

## Why "how" needs a method: the Elephant Migration anti-pattern

Modularity arguments explain why to break a monolith apart; decomposition explains how. The tempting path is to peel off whatever looks easy first (a standalone feature here, a reporting module there) with no overall plan. This is the Elephant Migration anti-pattern: piecemeal extraction without a holistic view, which typically ends in a distributed big ball of mud, also called a distributed monolith. It looks like progress early on and becomes expensive later, because the remaining dependencies have not been understood.

Also beware picking a first target that drags data along with it. Pulling reporting out as a service, for instance, achieves little until its data is split or fed through a separate store, which can be too large a first step.

Take a whole-system view and pick one of two methods: component-based decomposition or tactical forking.

## The decision tree

1. Is the codebase decomposable at all? (Assess with coupling metrics and inspection; see decomposability-assessment.md.) If not, decomposition patterns do not apply; consider replacement.
2. If decomposable, does it have identifiable components (namespaces or directories grouping related functionality, even loosely)?
   - Mostly unstructured, few observable components: tactical forking.
   - Well-defined or even loosely defined components: component-based decomposition.

The single biggest selection factor is how well the existing source is structured.

## Component-based decomposition

An extraction approach. Apply a series of refactoring patterns to refine components inside the monolith, then extract them into separately deployed services, incrementally and under control. (The concrete patterns are the subject of the following chapter of the book.)

Key definitions:

- Component: a building block with a clear role, responsibility and set of operations. It is usually expressed as a namespace or directory, with the source files inside it as its implementation. Example: a directory `acme/claims/intake/validation` is the component Claims Intake Validation with namespace `acme.claims.intake.validation`.
- The namespace derived from the directory path is the component's identity, so directory layout is architecture.

Core rule: form services out of groups of components, not one service per component. Components are the unit of analysis; services are clusters of them, and the service boundaries emerge as related components are grouped by domain.

Why the authors favour it when possible: in their migration experience, most of the pain of moving to microservices traces back to poorly defined components. Fixing component boundaries inside the monolith first removes that pain before any network boundary exists.

## Service-based architecture as target or stepping stone

Component-based decomposition naturally lands on service-based architecture: a hybrid style in which the application is split into a handful of coarse-grained, separately deployed domain services, each holding all business logic for its domain.

Recommendation: when heading for microservices, move to service-based architecture first. Reasons it makes a good intermediate (or final) state:

- Granularity can be decided later, per domain. Some domain services will need to split further into microservices; others are fine as they are.
- The database can stay shared. Teams partition functionality and domains before tackling data decomposition, which is usually the harder problem.
- No new operational platform is needed. Each domain service can ship with the same packaging as the old monolith (a WAR, EAR, .NET assembly, and so on); containers and deployment automation are optional.
- It is a technical change. Business stakeholders are generally not involved, and neither the IT organization nor test and deployment environments need to change.

## Tactical forking

A pragmatic method, whose name comes from Fausto De La Torre, for systems that are essentially a big ball of mud.

Insight: there are two ways to isolate a part of a system. Extraction pulls the wanted piece out, but in tangled code every piece you pull drags further dependencies along, so the unravelling never ends. Deletion removes what is not wanted; dependencies of the remaining code stay in place, so there is nothing to unravel. Tactical forking chooses deletion.

Procedure:

1. Decide the target services and which team owns each (for example, two teams: one for policy and quoting, one for claims).
2. Clone the entire monolith once per target service; each team receives a full copy.
3. Each team deletes code its service does not need. Verification is cheap: if the build and the tests still pass after a deletion, the code was not needed.
4. Repeat until each copy contains only its intended behaviour, still coarse-grained.
5. End state: several coarse-grained services, each a trimmed fork of the original.

Example of a deletion loop in pseudocode:

```
for module in candidate_unneeded(service_scope):
    remove(module)
    if not build_passes() or not tests_pass():
        restore(module)      # still needed by retained behaviour
        mark_as_dependency(module)
```

## Tactical forking trade-offs

Strengths:

- Work begins immediately; almost no upfront analysis.
- Deleting is easier than extracting in highly coupled code, and the compiler plus a basic test suite tell you whether a deletion was safe.

Weaknesses:

- Each resulting service carries a lot of leftover, mostly dead or latent code from the monolith.
- Code quality inside each service is no better than before; there is simply less of it, unless the team invests in cleanup afterwards.
- Shared code is now copied into every fork. Naming of shared classes and files can drift between forks, making it hard to recognise what is common and to keep it consistent. A bug fix in shared logic must be applied to every fork.
- Service boundaries must be decided upfront (to know how many forks to make), rather than emerging from analysis.
- Each fork needs its own team, increasing coordination across teams.

The name is deliberate: it is a tactical, not a strategic, move. It lets a team get an important system onto a new platform quickly, accepting that the result is not well structured.

## Choosing between the two

Favour component-based decomposition when:

- Components are identifiable, even loosely.
- Pain points include maintainability, testability or reliability (duplicated shared code would worsen them).
- There is significant shared infrastructure code (logging, security, persistence helpers) that forks would duplicate.
- A safer, incremental, controlled migration is valued over speed.
- The team should collaborate on finding shared functionality, component boundaries and domain boundaries together.

Favour tactical forking when:

- The code is a genuine big ball of mud with few observable components.
- Speed of migration matters more than internal quality, at least initially.
- Teams can be split per target service and target boundaries are already known.
- Extraction attempts keep pulling in most of the monolith.

Accepted cost of component-based decomposition: it usually takes longer than tactical forking.

## Worked examples

A logistics company has a ten-year-old dispatch monolith. Metrics put most packages near the main sequence and the packages map cleanly to domains (routing, fleet, billing, notifications). Shared logging and auth helpers are used everywhere. Choice: component-based decomposition toward service-based architecture, keeping the shared database for now; routing may later split into finer microservices if its scalability needs diverge.

A retailer has a legacy storefront in which the UI layer calls stored procedures directly and almost everything lives in two namespaces. A deadline requires moving checkout and catalogue onto a new runtime within a quarter. Choice: tactical forking into two forks, one per team, followed by a scheduled cleanup phase to remove latent code and reconcile duplicated shared utilities.

Book context in brief: the chapter's running story shows a team first tempted to peel off easy features one at a time, being steered toward a holistic method, and then, after finding their code mostly near the main sequence with clear components, preferring component-based decomposition because duplicated shared code would aggravate their maintainability problems.

## Decision record template

Capture the choice as an ADR in your own words:

- Context: the system being split and the two approaches considered.
- Decision: the approach chosen.
- Justification: structure of the code (metric findings), shared-code volume, how service boundaries will be determined (upfront for forking, emergent for components), risk tolerance, current quality attributes under strain.
- Consequences: expected duration, team organisation implications (one team collaborating versus several teams per fork), follow-up work such as cleanup of forks or later data decomposition.

## Pitfalls

- Extracting the "easy" pieces first with no plan (Elephant Migration).
- Mapping one component to one service, which yields services that are too fine and chatty.
- Splitting the database in the same step as the first service extraction.
- Choosing tactical forking for code that actually has good components, and paying for duplicated shared code without needing to.
- Treating a tactical fork as finished; without a cleanup phase each service keeps the monolith's quality problems.
- Jumping straight to microservices instead of stopping at service-based architecture to learn which domains really need finer granularity.
