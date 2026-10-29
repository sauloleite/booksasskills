# Modeling Practices and Tools

## Contents
- Why practices matter for informal diagrams
- Keep it simple
- Know your audience
- Color with a fallback
- Standards and templates without dogma
- Diagram review checklist
- Choosing a tool
- Generating code from models (and why not)
- Versioning and keeping diagrams in sync
- Pitfalls
- Practice plan
- Further reading

## Why practices matter for informal diagrams

Informal diagrams are fast to produce, which is both their strength and their danger: they multiply, sprawl and decay. The practices below keep them doing their only real job, which is carrying technical intent to a reader.

## Keep it simple

- Watch for "shock and awe" diagrams: walls of text, tangled lines, assorted shapes and sizes. They signal effort but transmit only confusion. If a reader cannot decode it, the diagram has failed regardless of its accuracy.
- There is no rule that a system must fit on one diagram. As systems grow, split views at natural boundaries (domain, subsystem, tier) and have each diagram point to its neighbors.
- An all-in-one overview is acceptable as a map, but it should rarely be the only model you maintain.
- Legibility test: imagine it printed on ordinary paper. Someone will print it. If labels become unreadable, split it.
- Show only the elements relevant to the question the diagram answers.

Refactoring pattern for an overloaded component diagram:
1. List the questions people actually ask of it.
2. Group components by the question they serve or by bounded area.
3. Produce one diagram per group, each with a "see also" pointer to adjacent views.
4. Reduce the overview to boxes for each group with only cross-group flows.

## Know your audience

Treat a diagram like code: optimize for the person consuming it. A dense technical model can be perfect for a peer developer and useless for an executive, and the reverse is equally true.

A subtler lesson: a reviewer without your domain knowledge can admire neatness (for example, a class diagram with no crossing lines) yet be unable to spot real mistakes. They end up trusting rather than verifying. So when you ask for review:
- Give a short narrative of the domain and what the diagram is meant to show.
- Point out the decisions you are unsure about.
- Prefer reviewers who know the domain for correctness, and outsiders mainly for clarity.
- Never treat a silent or shrugging review as validation.

## Color with a fallback

Color is a handy way to mark new, modified and unchanged components, or zones and ownership. Rules:
- Always include a legend. Your team's convention (green means new) is not universal.
- Assume grayscale printing will strip the meaning.
- Assume some readers are color blind.
- Therefore pair every color with a redundant cue: shape, border style (dashed for proposed), icon, or text label.

Example legend in a text-based diagram (Mermaid-style, illustrative):

```
flowchart LR
  classDef added stroke-width:3px,stroke-dasharray:0
  classDef changed stroke-dasharray:6 3
  API["Orders API (changed)"]:::changed
  Q[["Event queue (new)"]]:::added
  DB[(Orders DB)]
  API --> Q
  API --> DB
  subgraph Legend
    L1["(new): thick border"]:::added
    L2["(changed): dashed border"]:::changed
  end
```

Here meaning survives without color because of border style plus the text tag.

## Standards and templates without dogma

- Agree on an organizational set of commonly used diagrams and a shared color convention; consistency across projects lowers reading cost.
- Do not make the standard rigid. Each project should be able to add or drop diagram types.
- Push back on templates that demand artifacts with no value in context. Example: a template requiring use case diagrams on a team that works from user stories. Skip it and record the reason rather than drawing for the sake of drawing.

## Diagram review checklist

Run before sharing any diagram:
- [ ] Audience named; notation formality fits them.
- [ ] Title and a one-line statement of what question it answers.
- [ ] Scope limited to relevant elements; legible when printed.
- [ ] Links to related diagrams instead of cramming.
- [ ] Legend present; color is never the only cue.
- [ ] Logical or physical (and current or proposed) labeled where it applies.
- [ ] Uses only approved platforms and technologies for deployment views.
- [ ] Checked against current code or infrastructure; date or version noted.
- [ ] Stored under version control in an agreed location.
- [ ] Lifespan decided: throwaway, hand-maintained, or generated.

## Choosing a tool

Your organization likely has something already, and you rarely need a procurement cycle to make a good diagram. Tool families:

| Family | Examples | Strength | Watch out for |
|---|---|---|---|
| Desktop drag-and-drop | OmniGraffle (macOS/iOS), Microsoft Visio (Windows) | Low learning curve, stencils incl. cloud icons | Binary files, license limits |
| Online whiteboards | Mural, Miro, Lucidchart | Real-time collaboration, workshops | Drift from source of truth |
| Diagrams as code | Mermaid, PlantUML, Structurizr DSL (C4-oriented) | Diffable, renders in Markdown and wikis, CI-friendly | Layout control is limited |
| IDE | Built-in or plugin modelers | Create and extract from code | Output can be cluttered |
| Presentation software | PowerPoint, Keynote, Google Slides | Everyone has it; collaborative | Not built for modeling |
| AI assistants | Code-to-diagram extraction | Fast starting point | Can invent components or links; review every element |
| Analog | Paper, whiteboard | Fastest thinking aid | Capture with a photo if worth keeping |

Selection rules:
1. When unsure, choose what everyone involved can access and is licensed for.
2. Heavyweight enterprise tools bring power but also cost and a learning curve, and they can complicate simple jobs. Large, globally distributed teams may justify standardizing on one.
3. A simpler tool is fine if it gets the message across faster. The tool exists to express intent, not the reverse.
4. If a tool makes you productive, use it; if it slows you down, drop it.

## Generating code from models (and why not)

Model-driven code generation once promised big productivity gains. In practice, hand edits to generated files were often wiped out on the next regeneration unless developers followed strict tool conventions, and round-trip (bidirectional) tools did not deliver the promised gains. Today this approach mostly survives in niches such as safety-critical systems. Default advice: generate diagrams from code, not code from diagrams.

## Versioning and keeping diagrams in sync

- Put every diagram under version control. Text-based formats are the natural fit, but modern version control copes acceptably with image and tool files.
- Where possible, extract diagrams from code on demand or as a build-pipeline step so they cannot silently drift.
- Remember diagrams never replace working code; when they disagree, trust the code and fix or retire the diagram.

Sketch of a pipeline step (illustrative, tool-agnostic):

```
# ci: docs-diagrams
steps:
  - run: extract-diagrams --source src/ --out docs/diagrams/   # class/sequence from code
  - run: render-diagrams docs/diagrams/*.mmd --format svg
  - run: git diff --exit-code docs/diagrams/ || echo "diagrams changed; review in PR"
```

## Pitfalls

- Drawing to impress rather than to inform.
- One giant diagram as the sole architecture record.
- Color-only semantics with no legend.
- Formal notation for a mixed audience.
- Hand-maintained class or detailed sequence diagrams that silently go stale.
- Treating a template's artifact list as mandatory.
- Accepting AI-generated diagrams without checking each box and arrow against code.
- Letting tool selection or procurement delay the conversation the diagram was supposed to enable.

## Practice plan

Suggested exercises for a developer building the modeling habit:
1. Choose a meaningful flow in a system you know (or a familiar open source library), draw one or two sequence diagrams, and get a colleague's critique on clarity.
2. Extract a class diagram from your codebase with an IDE or tool. Note relationships that surprise you and what they reveal about coupling or design.
3. Collect existing architecture diagrams from your architect, study them, and ask about anything unclear. Then decide what you would draw differently and discuss it.
4. If your CI/CD pipeline does not produce diagrams, prototype a step that does and propose it.

An agent coaching a developer can turn these into a short loop: draw, get feedback against the review checklist, compare with code, revise.

## Further reading

- The C4 model (c4model.com)
- Jeff Patton, User Story Mapping
- Jacqui Read, Communication Patterns
- Ashley Peacock, Creating Software with Modern Diagramming Techniques
- Martin Fowler, UML Distilled

See also: diagram-catalog.md for choosing diagram types.
