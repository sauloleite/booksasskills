---
name: fsa-ch08-component-based-thinking
description: Guides identifying, sizing and refining logical components and analyzing coupling between them, based on Chapter 8 of Richards and Ford's "Fundamentals of Software Architecture" (2nd ed.). Use when drawing a logical architecture before a physical one, seeding components with the Workflow or Actor/Action approach, spotting Entity Trap "Manager" components, assigning user stories, splitting components for cohesion or architecture characteristics, computing afferent/efferent coupling, finding temporal coupling, or applying the Law of Demeter.
---

# Component-Based Thinking (FSA Chapter 8)

Architects reason about a system through its logical components (named units of business behavior), not its classes. This skill helps an agent build and evolve that logical view: map components to the code tree, seed an initial set without full requirements, fill and refine them with stories, cohesion analysis and architecture characteristics, and judge the coupling between them. Output is a component list with responsibility statements, communication links and recorded reasons for splits, ready to be allocated to an architecture style later.

## Key decision rules

1. **A component is a leaf namespace or directory.** Higher levels are domains and subdomains. Code in non-leaf folders, or diagrams that disagree with the tree, signal drift.
2. **Logical before physical.** Draw components and their interactions (plus actors and an optional data repository marker) before services, UIs and databases. The logical view is mostly independent of monolith vs distributed and of style choice.
3. **Iterate, do not perfect.** Seed a best-guess set from major workflows or actor actions; treat each as an empty bucket until stories land in it. The identify, assign, analyze, restructure loop runs for the system's whole life, including every feature change.
4. **Seeding choice.** Workflow approach: one component per happy-path step, reusing components across steps. Actor/Action approach: list actors (always include the system itself) and their major actions; it yields more components and is the good general-purpose default when no special constraints apply.
5. **Avoid the Entity Trap.** Entity-derived components (`OrderManager`) have vague names, become dumping grounds and grow too coarse. Suffixes Manager, Supervisor, Controller, Handler, Engine, Processor are warning signs. Name by role ("Validate Order"). If the system is pure CRUD over entities, recommend a CRUD framework or low-code tool instead of architecture work.
6. **Never duplicate a story's code across components.** If several components need the same behavior, create a new shared component and link them to it.
7. **Cohesion test.** Write a responsibility statement; heavy use of "and", "also", "in addition", "as well as" or long comma runs means the component does too much, even when every task relates to one theme. Extract different kinds of work (payments, stock, messaging).
8. **Characteristics can split what function would merge.** Scalability, elasticity, reliability, availability, fault tolerance and agility influence size. Separate parts with different needs (thousands of bidders vs one auctioneer). Do this only after the characteristics are prioritized.
9. **Coupling includes change impact.** Components are coupled if they talk or if changing one may force changes in the other. Track afferent Ca (incoming) and efferent Ce (outgoing) per component; high Ca demands stability, high Ce often means too much knowledge.
10. **Hunt temporal coupling explicitly.** Ordering and same-transaction dependencies are mostly invisible to tools; ask for them and write them down.
11. **Law of Demeter: knowledge is coupling.** Move "if X then also Y" knowledge to the component that owns X. Keep edges intrinsic to the caller's job; an intermediary that leaves the caller's Ce unchanged adds nothing. Expect coupling to move, not disappear system-wide.
12. **No one true design.** Offer a few viable decompositions and pick the one with the least bad trade-offs.

## Default workflow

1. Clarify scope: greenfield, major change, or a single new feature.
2. If code exists, list leaf directories as current components (run the coupling script on dependencies if available).
3. Seed or update components with Workflow or Actor/Action; reject entity-named buckets.
4. Assign each story or requirement; extract shared components rather than duplicate.
5. Write a responsibility statement per component; split low-cohesion ones (run the lint script).
6. Check prioritized architecture characteristics; split where operational needs diverge; record why.
7. Compute Ca/Ce, ask about temporal dependencies, apply Demeter to high-Ce knowledge hubs.
8. Present the logical diagram (components, links, actors) and alternatives with trade-offs; note that restructuring will continue.

## References

- [references/logical-architecture-and-identification.md](references/logical-architecture-and-identification.md): read when defining components from code, contrasting logical and physical views, seeding components (Workflow, Actor/Action), diagnosing the Entity Trap, or assigning user stories.
- [references/refining-components.md](references/refining-components.md): read when judging cohesion, splitting for architecture characteristics, planning ongoing restructuring, or using the auction case study pattern and trade-off framing.
- [references/component-coupling.md](references/component-coupling.md): read when measuring afferent/efferent coupling, looking for temporal coupling, or applying the Law of Demeter with a worked redistribution example.
- [references/source-map.md](references/source-map.md): read to check which reference covers a given chapter section.

## Scripts

- Run `python3 scripts/component_coupling.py deps.txt` to compute Ca and Ce per component from lines like `A -> B` (component names). Run `python3 scripts/component_coupling.py class_deps.txt --paths --strip-prefix src/` to map class-file dependencies to leaf-directory components first; intra-component edges are ignored. Add `--json` for machine-readable output.
- Run `python3 scripts/component_lint.py components.txt` to flag Entity Trap suffixes and low-cohesion responsibility statements in lines like `Name: statement`. Tune with `--max-commas N` and `--min-glue N`. Findings are advisory prompts for judgment, not verdicts.
