# Views and Representational Consistency

## Why diagrams are an architect's job

The chapter frames diagramming as a communication skill, not a drafting chore. An architecture only becomes real when managers agree to pay for it and developers agree to build it, and a clear picture of the topology is usually the fastest route to both. A shared diagram also gives the team a common mental model of how the parts fit, which is valuable in its own right. The authors push architects to treat diagramming as a skill worth practicing deliberately.

Implication for an agent: when asked to "explain the architecture", default to producing or proposing a diagram (plus a short narrative), and tailor its level of detail to the audience that must approve or build it.

## The problem: detail without location

Architecture is normally shown through several views: a whole-system overview, then progressively narrower close-ups of one region. The failure mode is jumping straight to a close-up. Viewers see a detailed fragment but cannot tell where it sits in the system, what surrounds it, or how big a slice it is, so they misjudge its scope and importance.

## The rule: representational consistency

Before you switch to a different view, first show how the part you are about to zoom into relates to the whole. Apply this both inside a single diagram set and across a slide deck or document.

Practical forms of the rule:

- **Zoom path.** Present views in order: full topology, then the boundary between the whole and the target region (highlighted in place), then the target region's internals.
- **Context inset.** On a detail diagram, include a small thumbnail of the full topology with the zoomed region outlined or shaded.
- **Consistent geometry and naming.** Keep the same names, shapes and relative positions for an element across all views so readers can track it while zooming.
- **Explicit boundary.** On the detail view, show the edges that cross into and out of the region, even if the external nodes are drawn as stubs.

## Worked example (invented)

A team wants to explain the rule engine inside a claims-processing platform built as a microkernel.

1. Slide 1: the whole platform: web channel, claims core, rule plug-ins, payment gateway, claims database. The plug-in area is drawn as one grouped box.
2. Slide 2: same picture, everything faded except the core and the plug-in group; the contract between them (a registry plus a plug-in interface) is labeled.
3. Slide 3: the inside of the plug-in group: fraud rules, coverage rules, regional rules, and how they are ordered and called. A thumbnail of slide 1 sits in the corner with the plug-in area highlighted.

Skipping slide 2 is the classic mistake: the audience sees three rule boxes and cannot tell whether they are services, libraries or database tables, or who invokes them.

## Mapping views to C4 levels

If the team uses C4 (see the standards reference), representational consistency maps naturally onto its zoom levels: Context, then Container, then Component, then Class. Each lower-level diagram should name the parent element it expands and keep that element's label unchanged.

## Checklist before presenting a detail view

- Has the audience already seen the full topology in this session or document?
- Is the region being zoomed visibly marked on the overview?
- Do element names and shapes match between the overview and the detail?
- Are the incoming and outgoing dependencies of the region shown?
- Does the detail diagram state its scope in its title (for example, "Claims core: plug-in subsystem")?
