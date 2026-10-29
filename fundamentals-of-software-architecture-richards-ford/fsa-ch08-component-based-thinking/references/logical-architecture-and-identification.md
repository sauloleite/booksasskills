# Logical Architecture and Initial Component Identification

## Contents
- What a logical component is
- Logical vs physical architecture
- The identification and refactoring loop
- Seeding the first components
- Workflow approach
- Actor/Action approach
- The Entity Trap (antipattern)
- Assigning user stories
- Worked example: loyalty program
- Pitfalls
- Review questions

## What a logical component is

A logical component is a named unit of business behavior (for example "Settle Invoice" or "Route Parcel"). It is the level of granularity at which an architect reasons about a system; classes and functions live below it.

How it shows up in code:
- A component maps to a namespace or directory that holds the code implementing that behavior.
- The **leaf** nodes of the namespace or directory tree are the components. Higher nodes are domains and subdomains that group them.
- Example: `billing/invoicing/settlement` is the Settlement component inside the Invoicing subdomain of the Billing domain.
- Consequence: you can recover a system's logical architecture by reading its folder or package tree. If code sits in non-leaf directories, or a leaf mixes unrelated behavior, the code and the intended architecture have drifted.

Agent check when reviewing a repo:
1. List leaf directories that contain source files. Each is a candidate component.
2. Flag source files sitting in intermediate (non-leaf) directories: they belong to no component.
3. Compare the leaf list with the architect's component diagram. Mismatches are drift to fix or document.

## Logical vs physical architecture

| Aspect | Logical architecture | Physical architecture |
|---|---|---|
| Shows | Components, how they interact, actors, and optionally a repository marker showing where data flows | Deployment units: services, UIs, databases, brokers |
| Omits | UIs, databases, services, other deployables | Usually hides where a given business function lives |
| Should match | The code's namespace/directory structure | One or more architecture styles (layered, microservices, event-driven, and so on) |
| Answers | What does the system do, how is it partitioned, who talks to whom | How is it deployed and run |

Rules:
- Build the logical architecture first. Do not jump straight to boxes for services and databases.
- Why: a physical view can scatter one capability (say, payments) across several services so nobody can see how it fits; and it gives developers no guidance on how to organize code, which tends to yield shapeless codebases that resist maintenance, testing and deployment.
- The logical view is largely independent of the physical one. You can design components before deciding monolith vs distributed, or which style to use. Components are later allocated to deployment units.
- In a logical diagram, a "repository" symbol means shared data a set of components reads or writes. It is not a database product choice.

## The identification and refactoring loop

Component design is iterative. The loop:
1. **Identify core components** (a best guess).
2. **Assign user stories or requirements** to them.
3. **Analyze roles and responsibilities** (cohesion check).
4. **Analyze architecture characteristics** (may split or merge).
5. **Restructure** as needed, then return to step 2.

The loop never really finishes. Use it for greenfield work and also every time a feature is added or changed. Example: adding "reserve online, collect at a branch" to a retail system brings scheduling logic and changes to checkout; that may create components, reshape existing ones, or both.

## Seeding the first components

- Do not try to make the first set perfect. Early on you know the least, so effort spent polishing is wasted. Make a best guess and iterate.
- You need few or even zero detailed requirements to start. Seed from the major things users do or the main processing flows.
- Treat each new component as an **empty bucket**: a name expressing intended purpose, with no behavior until stories are assigned to it.
- Two useful seeding techniques (Workflow, Actor/Action) and one to avoid (Entity Trap).

## Workflow approach

Walk the main happy path (no error branches) a user takes, or the main request-processing flow, and give each step a component.

- Several steps may reuse one component (for example, two "notify the user" steps both land in a notification component).
- Model as many major workflows or journeys as you can, but not all of them. Minor flows will be absorbed as stories arrive.
- Best when: you understand the end-to-end flow but not the detailed requirements; there is essentially one dominant actor.

## Actor/Action approach

List the actors, then each actor's major actions, then map actions to components.

- The **system itself is always an actor**: it performs automated work such as billing runs, replenishment, reconciliation, scheduled jobs.
- Multiple actions can share a component (two packing-related actions by a warehouse worker can both go to a fulfillment component).
- Typically yields more components than the Workflow approach (depends how many workflows you model).
- Best when: there are several distinct actor types. It is also the recommended default when the team has no special constraints and wants a general-purpose decomposition.
- Both approaches let you sketch components and their communication before detailed requirements exist.

## The Entity Trap (antipattern)

Symptom: deriving components from data entities (Customer, Product, Order) and naming them `CustomerManager`, `ProductManager`, `OrderManager`.

Why it hurts:
1. **Vague names.** "Order Manager" tells you only that it handles orders. Compare "Validate Order", which states a role.
2. **Dumping grounds.** Everything touching the entity piles in: validation, placement, history, fulfillment, shipping, tracking. It behaves like the catch-all utility class with dozens of unrelated methods.
3. **Too coarse.** Oversized components lose a clear purpose and become hard to maintain, test and deploy, which hurts reliability.

Detection heuristic: a name ending in Manager, Supervisor, Controller, Handler, Engine or Processor is a warning sign. (A strong signal, not proof; judge by what the component does.)

Exception: if the system truly is just create/read/update/delete over entities, it does not need an architecture effort at all. Recommend a CRUD framework, scaffolding tool, or low-code/no-code platform that generates most of the code.

Fix: rename and split by action or workflow step ("Register Customer", "Update Customer Profile", "Search Catalog").

## Assigning user stories

Assigning stories fills the empty buckets and gives each component concrete responsibility. It repeats as stories emerge.

Decision rules:
- Put a story in the component the actor already interacts with for that activity, or the one that owns the related system logic.
- If a story would need the same code in several components, **do not duplicate it**. Code has to live in exactly one directory/namespace, so create a new component and have the others call it.
- After adding a component, update the communication links in the logical diagram.

## Worked example: loyalty program

Seeding with Actor/Action for a retailer's loyalty system:
- Member: join program -> Member Enrollment; check balance -> Points Balance; redeem reward -> Reward Redemption.
- Store clerk: apply member discount at till -> Checkout Discount; reverse a redemption -> Reward Redemption.
- System: accrue points nightly -> Points Accrual; expire stale points -> Points Expiry; send tier-change notice -> ?

The last story ("tell members by SMS whenever their tier changes") could be triggered by Points Accrual, Points Expiry and Reward Redemption. Rather than copy SMS logic into three places, add **Member Messaging** and have the three call it. Note there is no "Member Manager" or "Points Manager".

## Pitfalls

- Starting from the physical diagram (services and databases) and never drawing the logical one.
- Polishing the first component list instead of iterating.
- Entity-named components with Manager/Handler suffixes.
- Duplicating shared behavior across components instead of extracting one.
- Letting the code tree diverge from the diagram so the diagram stops describing reality.

## Review questions

1. Given a repo tree, which directories are components and which are domains?
2. When would you choose Actor/Action over Workflow seeding?
3. A stakeholder insists on one component per database table. What do you recommend, and when is their instinct actually fine?
