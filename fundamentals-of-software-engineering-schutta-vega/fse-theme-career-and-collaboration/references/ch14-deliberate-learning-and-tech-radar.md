# Deliberate Learning and the Personal Tech Radar

## Why deliberate

Choosing software means signing up for lifelong learning, yet nobody can learn everything. Chasing whatever is trending wastes scarce hours, and many hyped tools vanish within a few years. Learning a tool mainly to decorate a resume is called resume-driven development; treat it as an anti-pattern. Unstructured study produces unstructured results. The chapter's remedy has three layers: fundamentals, a T-shaped profile, and a filter for each new topic. It pairs well with general learning techniques (the book covers those in its learning chapter).

## Layer 1: Core skills

These keep their value regardless of fashion and form the stem of the T. Master them before stacking on complexity:
- Data structures and algorithms
- Design patterns
- Testing approaches
- Version control
- Database design

Agent heuristic: if a junior asks whether to learn a new framework while shaky on, say, schema design or testing, recommend closing the fundamental gap first or pairing the two (learn the framework by building something that forces good tests and a real schema).

## Layer 2: T-shaped expertise

- **Vertical bar:** deep command of a primary stack.
- **Horizontal bar:** working familiarity with neighboring areas.

Depth makes you valuable; breadth makes you adaptable as the industry shifts. Example (my own) for a TypeScript frontend developer:
- Deep: TypeScript, React, browser performance, accessibility.
- Broad: a backend language, REST and GraphQL API design, CI pipelines, basic cloud deployment, system design.

The chapter's example is a Java backend developer with depth in Java, Spring and SQL/NoSQL storage, and breadth in basic frontend, DevOps and system design.

## Layer 3: The five-question filter

Before investing time in any skill, ask:
1. Does it serve my stated career goal?
2. Will it still matter in three to five years?
3. Does it give me an edge over peers?
4. Does it make me more useful to my current team?
5. Am I genuinely excited by it?

Usage guidance for an agent:
- A "no" on question 1 plus "no" on question 4 usually means Hold, unless question 5 is a strong yes and the cost is small (weekend exploration).
- Question 5 is not a tiebreaker afterthought. Without interest, the learner will not supply time and attention, the two scarcest inputs.
- Re-run the filter whenever the career goal changes.

## The personal technology radar

Thoughtworks created the technology radar for organizations to track and classify tools, platforms, languages and techniques over time and to spark discussion. The chapter adapts it for individuals.

**Quadrants**
1. Languages and frameworks
2. Tools and infrastructure
3. Platforms and APIs
4. Techniques and methodologies

**Rings (personal meaning)**
- **Adopt:** in daily use; you are deepening mastery.
- **Trial:** actively studying or prototyping with it.
- **Assess:** on your research list; learning not yet started.
- **Hold:** consciously parked for now (declining tech, unproven experiments, or simply off-goal).

**Building it, step by step**
1. Inventory today's stack: languages, frameworks, tools used daily. Rate your proficiency and flag gaps.
2. Pull in technologies from postings for roles you want within one to two years. Note frequency and whether each is a hard requirement or a bonus.
3. Add emerging items seen in blogs and talks that are gaining traction in your domain. Look for what leaders are adopting, not every shiny thing.
4. Review on a schedule; a quarterly calendar reminder is the suggested default. Items migrate between rings as their relevance to your goals changes.

Medium does not matter: paper, a spreadsheet, or Thoughtworks' Build Your Own Radar (BYOR) tool all work. What matters is that it captures your ecosystem and drives decisions. The radar should mix today's mainstream with near-future bets and point attention at short- and medium-term learning.

**Example radar (my own, for a mid-level Python data engineer)**

| Quadrant | Adopt | Trial | Assess | Hold |
|---|---|---|---|---|
| Languages and frameworks | Python, SQL | Rust for hot paths | Scala | Legacy Pig scripts |
| Tools and infrastructure | Git, Airflow | Terraform | Kubernetes operators | Self-managed Hadoop |
| Platforms and APIs | PostgreSQL | A cloud data warehouse | Streaming platform | Niche proprietary ETL suite |
| Techniques and methodologies | Unit and data testing | Data contracts | Event sourcing | Rewrites for novelty |

**Review ritual (quarterly, about 30 minutes)**
- What moved from Trial to Adopt? Celebrate it in the wins log.
- What sat in Assess for two quarters without action? Either schedule it or move it to Hold.
- Re-scan five postings for the target role; adjust Assess.
- Check alignment with the backward milestone plan.

None of these placements is permanent; adapt as needs and interests change.

## Pitfalls

- Filling Trial with five items at once; keep it to one or two so something actually reaches Adopt.
- Letting the radar drift from the career roadmap; they should be read together.
- Treating Hold as failure. Deciding what not to learn is the point.
- Skipping fundamentals because frameworks feel more marketable.

## Glossary

- **Resume-driven development:** picking technologies for how they look on a CV rather than for growth or fit.
- **T-shaped:** one deep specialty plus broad adjacent literacy.
- **BYOR:** Thoughtworks' tool for generating a radar visualization from your own data.
