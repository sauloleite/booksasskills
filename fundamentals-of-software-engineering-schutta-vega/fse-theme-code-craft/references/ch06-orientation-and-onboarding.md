# Orientation and Onboarding: Purpose, Docs, Structure, First-Week Process

## Contents
- Mindset for inherited code
- Step 1: learn why the system exists
- Step 2: mine the documentation (and distrust it)
- Step 3: read the shape of the repository
- A first-week onboarding checklist
- Pitfalls
- Worked example

## Mindset for inherited code

- Most professional work happens on systems that already exist. Treat that as an advantage: the platform, build, hosting and many design choices are settled, so effort goes straight to the business problem.
- Anxiety on a new codebase usually comes from unknown languages, frameworks or tools. A deliberate plan reduces it.
- Nobody holds the whole system in their head, including people who have been on it for years. Partial understanding is the normal state; aim for "enough to act safely on this task."
- This chapter extends basic code-reading mechanics (covered elsewhere in the book) to whole systems.

## Step 1: learn why the system exists

Order matters: purpose before code. Details such as framework versions are noise until you know what the product is for.

Questions to answer first:
- What business reason justifies this system? Who are its stakeholders?
- How important is it to the company? Core revenue path or side utility?
- Who are the end customers, and what do they struggle with?

Who to ask, in this order:
1. A product-side expert (product manager or product owner) for the high-level story. Prepare questions, take notes, and ask to record if the session is remote. Ask freely; unasked questions are the only costly ones.
2. Engineers currently on the project for the technical overview.
3. The original builders, if any are still reachable. They are rare and extremely valuable because they remember the reasons behind decisions.
4. A tech lead or architect, specifically for the "why" behind structural decisions.

Then look outward: read anything public about the product and try the customer's point of view. If the company maintains user personas (fictional profiles of typical users with goals and pain points), read them. Personas often explain technical choices that look odd from inside the code.

## Step 2: mine the documentation (and distrust it)

- Read everything available, including Architecture Decision Records (ADRs). With the business context from step 1, this material becomes far easier to absorb.
- Work through the onboarding or local-setup guide. Containers have made these simpler, but they are still slow and often stale.
- Do not rewrite docs yet. Instead, keep a running list of gaps, errors and missing steps. Fixing them later is an easy, visible early contribution.
- Documentation drifts; running code does not. Before investing hours in a doc, ask a teammate whether it still describes the current version. A few minutes of conversation can save days of studying a design that was replaced.

## Step 3: read the shape of the repository

Before reading any function, identify the architectural pattern (or mix of patterns, since many codebases evolved rather than being designed). The folder layout is the cheapest clue.

| Pattern | Telltale layout | What it implies for exploration |
|---|---|---|
| Package by layer | Top-level folders named after technical roles (controllers, services, repositories, models) | Easy to find "all X of a type"; one feature is spread across many folders, so tracing a feature means hopping between them |
| Package by feature | Top-level folders named after business areas (billing, catalog, accounts) | One folder holds a full slice of a capability; ideal for learning one workflow end to end |
| Hexagonal (ports and adapters) | A domain core plus folders for ports (interfaces) and adapters (web, persistence, messaging) | Business rules live in the core with no technical dependencies; infrastructure detail lives in adapters. Read the core to learn the rules, the adapters to learn integrations |
| Microservices | Several sibling deployables, each with its own build and container file, often plus a gateway and shared libraries | Learn your service's internal layout and also its place in the wider ecosystem: callers, callees, gateway routing, shared models |

## A first-week onboarding checklist

A repeatable sequence (adapted from a method Christopher Judd teaches in his boot camps), paraphrased:

1. Clone the repository.
2. Read the README, coding standards, architecture notes and any other supporting docs.
3. Keep notes throughout: architecture, build commands, frequently used queries, domain vocabulary, relevant industry standards. Share them with the team.
4. Read the build scripts.
5. Review declared dependencies.
6. Map the structure: modules, packages, namespaces, produced artifacts.
7. Read the CI/CD pipeline definitions.
8. Install the toolchain the project needs (runtimes, languages, build tools).
9. In the IDE: run the app under the debugger, place breakpoints in methods that look interesting and trigger them through the running app; then run and debug the unit tests the same way.
10. On the command line: build the artifacts, run the unit tests, start required containers such as the database, and launch the app locally, noting ports and URLs.

Expect multiple passes. Each ticket you complete deepens the picture.

## Pitfalls

- Diving into code before knowing the business purpose.
- Trusting a polished document over the running system.
- Rewriting documentation before you understand the system well enough.
- Staying stuck alone for days instead of asking.
- Assuming the folder names reflect a clean pattern; many codebases blend several.

## Worked example

A developer joins a team that owns a clinic-scheduling platform. Day 1: a 45-minute call with the product owner reveals that appointment reminders drive most revenue retention. Day 2: a talk with the tech lead explains that a message queue was introduced after reminder emails timed out. Reading ADRs confirms it. The repository shows feature folders (appointments, reminders, billing) plus an adapters folder, so the developer starts with the reminders folder and its adapters. The setup guide misses one environment variable; the developer logs it in a notes file and opens a small docs fix in week two.
