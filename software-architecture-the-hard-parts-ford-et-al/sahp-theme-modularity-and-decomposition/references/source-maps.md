# Source maps: book sections to reference files

File names below are the chapter-prefixed names used in this folder.

## Source Map: Chapter 3, Architectural Modularity

| Chapter section | Covered in |
|---|---|
| Chapter opening (story setup, business and technical change, capacity analogy, agility) | [ch03-modularity-drivers-and-business-case.md](ch03-modularity-drivers-and-business-case.md) |
| Modularity Drivers | [ch03-modularity-drivers-and-business-case.md](ch03-modularity-drivers-and-business-case.md) |
| Maintainability | [ch03-change-characteristics.md](ch03-change-characteristics.md) |
| Testability | [ch03-change-characteristics.md](ch03-change-characteristics.md) |
| Deployability | [ch03-change-characteristics.md](ch03-change-characteristics.md) |
| Scalability | [ch03-operational-characteristics.md](ch03-operational-characteristics.md) |
| Availability/Fault Tolerance | [ch03-operational-characteristics.md](ch03-operational-characteristics.md) |
| Sysops Squad Saga: Creating a Business Case | [ch03-modularity-drivers-and-business-case.md](ch03-modularity-drivers-and-business-case.md) |

The maintainability-level formula, change and test scope, lockstep deployment, and synchronous failure spread are also computed by `scripts/modularity_impact.py`.

## Source map: Chapter 4, Architectural Decomposition

| Chapter section | Covered in |
|---|---|
| Chapter opening (story: Elephant Migration AntiPattern) | ch04-decomposition-approaches.md |
| Chapter introduction and decision tree (Figure 4-1) | ch04-decomposition-approaches.md |
| Is the Code Base Decomposable? | ch04-decomposability-assessment.md |
| Afferent and Efferent Coupling | ch04-decomposability-assessment.md |
| Abstractness, Instability, and Distance from the Main Sequence | ch04-decomposability-assessment.md |
| Distance from the Main Sequence | ch04-decomposability-assessment.md |
| Component-Based Decomposition | ch04-decomposition-approaches.md |
| Tactical Forking | ch04-decomposition-approaches.md |
| Trade-offs | ch04-decomposition-approaches.md |
| Sysops Squad Saga: Choosing A Decomposition Approach | ch04-decomposition-approaches.md (story summary, decision record template) |

Metric calculations are also implemented in `../scripts/decomposability_metrics.py`.

## Source Map: Chapter 5, Component-Based Decomposition Patterns

Where each part of the chapter is covered. Pattern names are kept so readers can find them in the book; the chapter's fitness-function headings are described here in paraphrase rather than by their exact titles.

| Part of the chapter | Covered in |
|---|---|
| Chapter introduction (pattern roadmap and three-part pattern structure) | ch05-component-inventory-and-sizing.md |
| Architecture Stories (sidebar) | ch05-component-inventory-and-sizing.md |
| Identify and Size Components Pattern, description | ch05-component-inventory-and-sizing.md |
| Identify and Size: governance checks (inventory changes, share of codebase, distance from mean size) | ch05-fitness-functions-catalog.md |
| Identify and Size: story section | ch05-component-inventory-and-sizing.md (one-line summary) |
| Gather Common Domain Components Pattern, description | ch05-common-domain-and-flattening.md (Part A) |
| Gather Common Domain: governance checks (repeated leaf names, duplicated code) | ch05-fitness-functions-catalog.md |
| Gather Common Domain: story section | ch05-common-domain-and-flattening.md (coupling checklist summary) |
| Flatten Components Pattern, description | ch05-common-domain-and-flattening.md (Part B) |
| Flatten Components: governance check (no code in non-leaf namespaces) | ch05-fitness-functions-catalog.md |
| Flatten Components: story section | ch05-common-domain-and-flattening.md (worked example summary) |
| Determine Component Dependencies Pattern, description | ch05-dependencies-domains-and-domain-services.md |
| Determine Dependencies: governance checks (dependency ceiling, forbidden component links) | ch05-fitness-functions-catalog.md |
| Determine Dependencies: story section | ch05-dependencies-domains-and-domain-services.md (filtering shared components) |
| Create Component Domains Pattern, description | ch05-dependencies-domains-and-domain-services.md |
| Create Component Domains: governance check (allowed domains under the root) | ch05-fitness-functions-catalog.md |
| Create Component Domains: story section | ch05-dependencies-domains-and-domain-services.md (procedure and business validation) |
| Create Domain Services Pattern, description | ch05-dependencies-domains-and-domain-services.md |
| Create Domain Services: governance check (shared namespace prefix per service) | ch05-fitness-functions-catalog.md |
| Create Domain Services: story section | ch05-dependencies-domains-and-domain-services.md (sequencing rules) |
| Summary | SKILL.md (workflow) and ch05-dependencies-domains-and-domain-services.md |
