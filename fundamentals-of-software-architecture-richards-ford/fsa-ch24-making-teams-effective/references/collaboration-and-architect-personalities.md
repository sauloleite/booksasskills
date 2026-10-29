# Collaboration, Boundaries and Architect Personalities

## Why this matters

The chapter opens with a claim: an architect's job does not end at the diagram. Leading the team through implementation is part of the role, and doing it well is a major differentiator between successful and unsuccessful architects. A design produced in isolation and then handed over tends to be implemented wrongly, not because developers are careless but because the knowledge never crossed the gap.

## The handoff model versus the collaborative model

**Handoff (traditional) model.** The architect owns requirements analysis, extraction of architecture characteristics, selection of styles and patterns, and identification of logical components. Developers then own class design, UI, code and tests. Information flows one way across a physical and organizational wall.

Failure mechanics of the handoff model:
- Decisions the architect makes do not reliably reach the people who implement them.
- Changes developers make while implementing rarely flow back to the architect, so the architect's mental model drifts from reality.
- The architecture therefore misses its goals, even if it was sound on paper.

**Collaborative model.** Architect and developers form one virtual team with communication flowing both ways. Benefits beyond accuracy: the architect gets a channel to mentor and coach, and the architecture can evolve each iteration instead of being frozen at the start. Modern architectures change with almost every iteration, so a one-way handoff cannot keep up.

Agent heuristics:
- If a user describes "the architects designed it, then we got the docs", probe for drift: what changed during implementation, and does the architect know?
- Recommend a concrete two-way loop: shared rituals (design reviews developers attend, architect attending standups or demos), a place where implementation deviations are recorded and fed back (for example, ADR updates).

## Constraints as a room

One core architect responsibility is defining and communicating the constraints developers implement within. Picture those constraints as the walls of a room the team works in.

| Room size | Cause | Symptoms in the team |
|---|---|---|
| Too small | Excessive, fine-grained constraints | Blocked from needed tools, libraries and practices; frustration; good people leave |
| Too large | Few or no constraints | Developers forced to make architecture decisions themselves; excessive proofs of concept; design debates without resolution; low productivity and confusion |
| Right size | Guidance matched to the team and project | Team has what it needs and knows which decisions are theirs |

Note that teams cut off from their architect often simply do not know the constraints that exist, which produces the "too large" failure even when the architect believes the constraints are clear.

## Three personalities (a deliberate simplification)

The authors caricature three types to make the boundary idea concrete. Each produces a characteristic room size.

### Control-freak architect (room too small)

Behavior: decides at too fine a grain. Examples of overreach: forbidding open source or third-party libraries the team genuinely needs, mandating naming conventions, class shapes or method lengths, even writing pseudocode for developers to transcribe. Effect: developers lose ownership of the craft and stop respecting the architect.

Why it happens: it is the natural trap for developers newly promoted into architecture, because they are used to choosing design patterns and drawing class diagrams themselves.

**The dividing line between architect work and developer work:**
- Architect: identify the logical component, name its responsibility, define its core operations, and determine which other components interact with it.
- Developer: decide the internal design of that component (data structures, caching, patterns, class layout).

Invented example: an architect defines a `TaxRules` component with operations `lookupRate`, `refreshRules` and `subscribeToChanges`, and states that `Checkout` and `Invoicing` call it. Specifying that it must use a trie keyed by postal code with a write-through cache crosses into developer territory. That design may be fine, but it is one of many valid designs and choosing it is not the architect's call.

Exception: sometimes a degree of control-freak behavior is warranted, depending on project complexity and team skill (see the involvement scoring reference). As a default it is disruptive.

### Armchair architect (room too large)

Behavior: has not coded in a long time (or ever), ignores implementation details, appears briefly for initial diagrams and then moves to the next project. Some are simply out of their depth in the technology or domain. The authors observe that code cannot be faked, whereas drawing boxes and lines can.

Invented example: an architecture for a claims-processing platform consisting of two boxes, "Claims System" and "Fraud Engine", with an arrow between them. Not wrong, but useless as guidance.

Effect: the team ends up doing the architect's job, velocity drops, and nobody shares a clear picture of how the system should work.

Warning signs (self-check for the architect):
- No time, or no willingness, to spend time with the implementing teams.
- Shallow understanding of the business domain, the business problem, or the technology in use.
- Too little hands-on development experience.
- Not thinking through what a given implementation of the design implies for complexity, maintenance and testing.

Cause and cure: almost nobody chooses to be an armchair architect. It happens when the architect is stretched across too many teams and loses touch. The remedy is deeper involvement in the project's technology and a firmer grasp of the business problem.

### Effective architect (room right-sized)

Responsibilities:
- Sets constraints and boundaries that fit the team.
- Ensures team members work well together.
- Gives the right amount of guidance.
- Makes sure the right tools and technologies are in place.
- Removes roadblocks between the team and its goals.

This requires close collaboration and earning the team's respect; it is an art as much as a technique. The rest of the chapter supplies the tools: deciding how involved to be, spotting team dysfunction, checklists, and principle-based guidance.

## Diagnostic questions an agent can ask

1. Which decisions does the team believe they own, and which do they believe the architect owns? Do the two lists match the architect's view?
2. When did the architect last read or write code in this codebase?
3. How many teams is the architect currently supporting?
4. What was the last implementation change that altered the architecture, and how did the architect learn of it?
5. Has the team been blocked from a library or tool in the last month? Did they run multiple spikes on a question an architect should have settled?
