# ADR Practice: Storage, Documentation, Standards, Legacy Systems and AI

## Contents
- Where to store ADRs (and why not the app repo in larger organizations)
- Recommended layout by scope
- ADRs as architecture documentation
- ADRs for standards
- Retrofitting ADRs onto existing systems
- Generative AI in architectural decisions
- Pitfalls

## Storing ADRs

Baseline rule: one file or one wiki page per decision, wherever they live.

**Same repo as the code.** Attractive for small setups: ADRs are versioned alongside the code they govern. For larger organizations the chapter advises against it because:
1. Many people who need to read decisions (other teams, business analysts, enterprise architects) lack access to that repository.
2. Decisions whose scope exceeds one application (integration, enterprise-wide, cross-application standards) have no natural home there.

**Preferred options:** a dedicated, widely readable ADR Git repository; a wiki with an ADR template; or a shared file location that a wiki or document renderer can display.

## Layout by scope

Organize by the scope a decision governs. Names are suggestions; consistency across teams is what matters.

```
adr/
  application/
    common/        # applies to every application (e.g. a marker for framework classes)
    billing/       # decisions local to one application or system
    storefront/
  integration/     # how applications, systems or services talk to each other
  enterprise/      # global rules for all systems (e.g. only the owning system may touch its database)
```

In a wiki, each folder becomes a navigation landing page and each ADR a single page beneath it.

Agent heuristic for placing a new ADR:
- Affects only one app: `application/<app>`
- Same rule for all apps: `application/common`
- Concerns a contract or channel between two or more systems: `integration`
- Constrains every system in the company: `enterprise`

## ADRs as documentation

There is no agreed standard for documenting a software architecture (diagramming has some, such as C4 and ArchiMate, but documentation does not). A body of ADRs fills that gap:
- **Context** describes the area of the system in question and its options.
- **Decision** explains why; rationale is the most valuable kind of architecture documentation.
- **Consequences** captures the trade-offs, for instance why performance was favored over scalability.

Reading ADRs in order of number gives a narrative of how and why the architecture evolved.

## ADRs for standards

Standards are often resented because they feel like control without purpose. Writing each standard as an ADR changes that:
- Context explains the situation that compels the standard.
- Decision states the standard *and* why it must exist.
- Consequences forces the author to think through its implications and whether to adopt it at all.

Rules:
- If you cannot justify a standard in the ADR, it probably should not exist.
- Developers who understand the reason are more likely to follow it and less likely to contest it.

## Existing systems

ADRs still pay off after the decisions were made, because they expose whether those decisions were right.

Procedure:
1. List the most significant structural decisions already embodied in the system (shared databases, synchronous chains, deployment granularity).
2. For each, ask why. Example: several services share one database. Is there a reason? Should it be split?
3. If the original decision maker is gone, reconstruct the options and the trade-offs of each yourself.
4. Write the ADR either confirming the decision with a reconstructed rationale or flagging it as questionable, which may lead to a superseding ADR.
5. Over time this builds a shared store of reasoning for the system and surfaces inefficiencies and design errors.

Mark reconstructed rationale as such (for example in Notes: "rationale inferred, original author unavailable") so readers know its provenance.

## Generative AI and LLMs in decisions

Structural questions (messaging vs streaming vs event sourcing; one database or per-domain databases; one payment service or one per payment type) have no universal answer; they depend on context. This is the book's first law in action: every architectural choice is a trade-off.

Why LLMs struggle to decide:
- Their output tends toward the most probable answer, effectively a generic "best practice". Probability and best practices are the wrong basis for architectural decisions.
- The real work is translating business concerns (time to market, sustained growth) into architecture characteristics (maintainability, testability, deployability) and then weighing trade-offs in that specific context. That translation is not obvious and takes experience.

Worked logic: one payment service versus one per payment type is mainly performance versus maintainability. A single service performs better; separate services are easier to maintain and change. If the business mostly cares about time to market, maintainability dominates, so separate services win in that context. Change the business driver and the answer can flip.

The authors' finding from their own experiments: the best use of generative AI is to **enumerate trade-offs** for a decision so the architect can catch ones they missed. AI has broad knowledge but lacks the judgment to pick the right option for a given organization.

How an agent should behave given this:
- Do not hand back a single "best" option for a structural question without context. Ask for (or state assumptions about) the business drivers first.
- Produce a trade-off inventory per option, mapped to characteristics, and highlight which characteristic the stated business driver favors.
- Present the recommendation as conditional ("given time to market as the priority, X"), and note what driver would reverse it.
- Leave the decision and its justification to the human architect, then help draft the ADR.

## Pitfalls

- Burying cross-application ADRs inside one app's repository where other teams cannot see them.
- Inconsistent folder or page names across teams, which defeats discovery.
- Issuing standards without a recorded reason, then fighting compliance battles.
- Skipping legacy decisions because "they are already made"; that is exactly where hidden inefficiencies live.
- Accepting an AI-generated "best practice" as a decision rather than as input to trade-off analysis.
