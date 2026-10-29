---
name: fsa-ch11-modular-monolith
description: Guidance for evaluating, designing and governing a modular monolith (one deployable, code partitioned by business domain), based on Chapter 11 of Richards and Ford's "Fundamentals of Software Architecture" (2nd ed.). Covers single-repo vs per-module artifacts, peer-to-peer vs mediator communication, data topology, risks, fitness functions and team alignment. Use when choosing a starting architecture, restructuring a layered monolith by domain, reviewing module boundaries, writing boundary checks, or deciding when a monolith has outgrown itself.
---

# Modular Monolith (FSA Chapter 11)

Purpose: help an agent decide whether a modular monolith fits, shape its modules and inter-module communication, protect its boundaries with automated checks, and recognize when it is time to move on. The style is a single deployment unit (quantum of 1) whose code is organized by domain, so its big wins are low cost, simplicity and modularity, and its big losses are anything operational: scaling, elasticity, fault tolerance and recovery time.

## Key decision rules

1. **Domain first in every path.** The segment right after the app root must name a business area (`app.billing.invoice`), never a layer. Layer sub-splits are allowed only beneath the domain.
2. **Module = domain or subdomain**, composed of one or more components (namespaces/folders).
3. **Structure choice:** keep all modules in one code base when they interact a lot or the system is small; build modules as separate artifacts (JAR/DLL/package) when they are largely independent, large, owned by different teams, or need distinct expertise. Separate artifacts lose their value once modules must talk often.
4. **Every cross-module call is a cost.** Allow it only for workflows that truly span domains. In a single code base the ease of reaching into any class is the main path to a Big Ball of Mud; with separate artifacts, chatty modules produce DLL/JAR Hell.
5. **Direct calls vs mediator:** direct calls for a few stable interactions; a mediator (orchestrator) when workflows chain several modules. A mediator concentrates coupling on itself rather than removing it, and only it needs the other modules' APIs.
6. **Heavy chatter means bad boundaries.** If modules still need lots of communication, redraw the domains before adding plumbing.
7. **Data:** one shared database is the default and reduces calls; give independent modules their own database or schema when their data is contextual to them.
8. **Watch for "too big":** slow changes, unrelated breakage, developers colliding, long startup. Two or more of these means reassess.
9. **Limit reuse:** heavy shared code blurs modules into an unstructured monolith.
10. **Govern with fitness functions:** (a) every namespace belongs to a declared module, (b) per-module coupling budget (the chapter illustrates a ceiling of five; tune per system), (c) forbidden module pairs. Run in CI.
11. **Fit:** good for tight budget/time, unclear early direction (start here, migrate to service-based or microservices later), domain-aligned teams, mostly domain-driven change, DDD. Poor for high scalability, elasticity, availability, fault tolerance, responsiveness or performance, and for change streams dominated by technology swaps (prefer layered there).
12. **Teams:** align teams by domain. Teams split into UI/backend/DB groups struggle. Stream-aligned, enabling, complicated-subsystem and platform teams all map well onto modules.
13. **Cloud:** runs fine for small systems and can use managed services, but cannot exploit on-demand, per-function provisioning.

## Default workflow

1. **Assess fit.** List the top three architecture characteristics, classify the expected change stream (domain vs technical), and check team shape. Stop and suggest a distributed or layered style if rule 11 fails.
2. **Identify modules.** Derive domains/subdomains (DDD bounded contexts if available); list each module's components as namespaces.
3. **Pick the structure** (rule 3) and the **data topology** (rule 7).
4. **Map cross-module workflows.** Minimize them; choose direct calls or a mediator per workflow (rule 5). Re-cut domains if chatter stays high.
5. **Write governance.** Declare the module list, coupling budget and forbidden pairs; implement with ArchUnit, ArchUnitNET/NetArchTest, PyTestArch, TSArch, or the bundled script on an exported edge list.
6. **Align teams** to modules and record the decision (an ADR noting the trade-offs accepted and the "too big" triggers that would reopen it).
7. **Monitor** the warning signs and coupling trend each release.

## References

- [references/structure-and-communication.md](references/structure-and-communication.md): read when laying out namespaces, choosing single code base vs separate artifacts, picking direct calls vs a mediator, choosing a data topology, or assessing cloud deployment.
- [references/risks-and-governance.md](references/risks-and-governance.md): read when reviewing an existing modular monolith, writing fitness functions, setting a coupling budget, or deciding how to remediate boundary erosion or size problems.
- [references/fit-teams-and-example.md](references/fit-teams-and-example.md): read when deciding whether to adopt the style, explaining its strengths and weaknesses, aligning team topologies, or wanting a worked example and review questions.
- [references/source-map.md](references/source-map.md): read to find which file covers a given chapter section.

## Scripts

Run `scripts/check_module_boundaries.py` to compute module membership violations, per-module incoming/outgoing coupling against a budget, and forbidden module dependencies. Exit code 1 means violations (CI-friendly).

```bash
# From an exported dependency edge list ("from.ns -> to.ns" per line)
python3 scripts/check_module_boundaries.py \
  --modules shop.catalog,shop.cart,shop.billing,shop.shipping \
  --edges deps.txt --max-coupling 5 --forbid shop.cart:shop.shipping

# Directly over a Python source tree, exempting a mediator from the budget
python3 scripts/check_module_boundaries.py \
  --modules clinic.booking,clinic.billing,clinic.mediator \
  --python-root src --exempt clinic.mediator --count refs --json
```

`--count links` counts distinct module-to-module pairs; `--count refs` counts distinct namespace-level references crossing modules. State which one you used when reporting.
