# Diagramming Standards and Visual Guidelines

## Contents

- Choosing a notation: UML, C4, ArchiMate
- Standards policy: adopt, but allow exceptions
- Visual guidelines: titles, lines, shapes, labels, color, keys
- Review checklist
- Self-review questions

## Choosing a notation

**UML.** Created by Booch, Jacobson and Rumbaugh to merge their rival methods. Designed by committee, it never gained much traction outside organizations that required it. Two diagram types remain in everyday use: class diagrams (structure) and sequence diagrams (interaction over time). Treat the rest as rarely worth the effort.

**C4.** Developed by Simon Brown (2006 to 2011) as a modern answer to UML's shortcomings. Four zoom levels:

| Level | Shows | Typical audience |
|---|---|---|
| Context | The whole system, its users (roles) and external systems | Everyone, including business stakeholders |
| Container | Deployment and runtime boundaries (apps, services, databases, brokers) | Architects and operations; a natural meeting ground for both |
| Component | Components inside a container | Architects and senior developers; closest to the architect's own view |
| Class (code) | Reuses UML class diagrams, since those already work | Developers |

Why the authors rate C4 as a good standardization choice: an active, long-lived community; it evolves with the ecosystem; many drawing tools ship C4 templates; there are supporting tools and frameworks; and it specifies standard notation for the usual building blocks (containers, components, databases, connecting lines).

**ArchiMate.** An open standard from The Open Group for modeling enterprise architecture (the name blends "architecture" and "animate"). Its scope is modeling, analysis and visualization of architecture inside a single business domain and across several, and is deliberately minimal, favoring a compact core over exhaustive coverage of corner cases. Lighter than full enterprise modeling suites, and popular with enterprise architects.

### Selection heuristic

| Situation | Lean toward |
|---|---|
| Organization wants one standard for software-system diagrams across teams | C4 |
| Need to show business capabilities, processes and IT across domains (enterprise scope) | ArchiMate |
| Need precise class structure or call ordering | UML class or sequence diagram, alone or as C4's fourth level |
| Early exploration, whiteboard discussion | No formal notation; informal sketch with a key |

Whatever is chosen, the authors encourage each architect to develop a personal diagramming style, borrowing freely from notations that communicate well.

## Standards policy

Standards make communication across an organization consistent. Yet architects routinely break them, typically when the notation has no good way to express the design at hand. Recommended stance: establish a standard, and permit reasonable exceptions rather than forcing a design into a notation that distorts it. When you deviate, say so in the key.

## Visual guidelines

**Titles.** Give every element a title unless the audience already knows it well. Rotate or position titles so it is obvious which element they belong to, and so they use space efficiently.

**Lines.** Make lines thick enough to read at presentation distance. For information flow, use arrowheads to show direction (one-way or both). Different arrowhead styles may carry different meanings, provided you use them consistently. The one near-universal convention in architecture diagrams: solid line means synchronous communication, dotted line means asynchronous.

**Shapes.** Outside the formal notations there is no industry-wide shape vocabulary, so most architects define their own, and organizations sometimes adopt one as a shared language. The authors' own habits: 3D boxes for deployable units, plain rectangles for containers, cylinders for databases. Pick a set and stick to it.

**Labels.** Label every item, and be especially strict wherever a reader could interpret an element or line in more than one way.

**Color.** Architects tend to under-use color, a habit left over from black-and-white print. The authors still lean monochrome but add color when it separates artifacts, for example shading the services that belong to the same group or quantum. Never let color alone carry a critical distinction: viewers with color vision deficiency will miss it. Pair color with a distinct icon, pattern or shape, the way pedestrian signals pair red and green with different figures.

**Keys.** Whenever shapes, line styles or colors could be ambiguous, add a legend explaining each. The authors' strongest warning in this section: a diagram that is easy to misread does more harm than having none.

## Review checklist

Run this against any diagram an agent produces or reviews:

- [ ] Every element has a title or label; no unlabeled boxes or lines.
- [ ] Direction of flow is shown with arrowheads where flow matters.
- [ ] Synchronous edges are solid and asynchronous edges dotted (or the key states otherwise).
- [ ] Shape vocabulary is consistent (deployables, containers, databases distinguishable).
- [ ] Color is never the only carrier of meaning; an icon, pattern, shape or label repeats it.
- [ ] A key is present if any symbol could be misread.
- [ ] The diagram's scope is clear (title names the view level; for detail views, context was shown first).
- [ ] Topology is described in architectural terms; implementation specifics live in a separate layer or view.
- [ ] Any departure from the organization's notation is intentional and noted.

## Self-review questions

1. A diagram uses red and green borders to mark legacy versus new services. What must change?
2. Your team's notation has no symbol for an event stream partition. Do you invent one, and what else must you add?
3. When would a UML sequence diagram serve better than a C4 container diagram?
4. A reviewer cannot tell whether an arrow means "calls" or "depends on at build time". Which two guidelines were violated?
