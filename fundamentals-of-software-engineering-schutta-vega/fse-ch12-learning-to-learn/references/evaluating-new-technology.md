# Filtering Hype and Deciding What to Learn or Adopt

Covers "Fear of Missing Out", the "Let Your Passion Guide You" sidebar, "Where Should You Invest Your Time?" and the "Build Your Own Technology Radar" sidebar.

## Contents
- The attention problem
- Coping with FOMO
- Choosing by interest
- Learning versus adopting
- Judging staying power
- Radars
- Decision checklist
- Worked example
- Pitfalls

## The attention problem

Sources are endless: search, reading lists, podcasts, video, user groups, conferences, industry reports such as the Technology Radar. Choose formats that fit how the person learns best (reading, listening and watching, or doing). But attention is finite and cannot be scaled. Far more video is uploaded every minute than anyone could ever watch, before even counting podcasts, guides and social feeds. Consuming everything is impossible, so selectivity is mandatory.

## Coping with FOMO

Fear of missing out is common and understandable, but:
- Genuinely major shifts are impossible to miss; you hear about them even in areas you ignore. Missing the launch announcement costs little.
- **Shard learning across your network.** Colleagues and friends follow different areas. Agree to pass along what matters in each person's specialty.
- **Outsource scouting.** If a friend is already exploring an uncertain space, check in periodically. They absorb the rough patches; you inherit the lessons.
- **Focus has a price.** Going deep on a few things means deliberately letting most waves pass.

## Choosing by interest

One author sat down to study databases and, twenty minutes in, found himself reorganizing his sock drawer instead: a clear signal of no real interest. Scheduling time is easy; choosing the topic is the hard part. Lack of excitement makes it nearly impossible to keep showing up.

Rules:
- Pick topics that give you energy and go deep: follow experts, podcasts, videos, documentation.
- Quitting a book, tab or video halfway earns no penalty and wastes nothing further.
- Switch whenever interest dies; repeat the cycle.
- Personal passion does not justify adopting a tool in a project (next section).

## Learning versus adopting

Learning something is cheap and personal; adopting it imposes costs on a team and a codebase. Separate the two.

- **No resume-driven development.** Adopting a technology mainly to list it on a CV, rather than because it helps the project, is a recurring anti-pattern. Require a concrete why.
- **It is fine to wait until you need it.** A new trend will always be circulating.
- **Be a critical consumer.** Software is trade-offs; there is rarely a single best way, more often the least bad. Look past advertised benefits to the full set of consequences (operational burden, hiring, migration cost, lock-in). Rich Hickey's point applies: programmers tend to know every benefit and none of the costs.
- If instinct says something is overhyped, pausing before investing is reasonable.

## Judging staying power

Experience builds a sense of what lasts versus what fades, and of where the industry is heading. Calibrate it:

- **Temper hunches.** In 2001 Paul Graham applied his "hacker's radar" criteria and predicted Java would not succeed. It became one of the most successful languages ever. If a seasoned expert can miss that badly, treat your own gut calls as hypotheses.
- **Spot the pendulum.** Ideas swing between extremes and old approaches get polished, renamed and relaunched. A description of components in different languages on different machines cooperating over a network fits microservices, yet it also describes CORBA from the 1990s. Ask: what failed last time, and what is actually different now?
- **Repurposing happens.** A technology built for one purpose can resurface for another (the internet began as a military network).
- **Novelty is not benefit.** Ask probing questions about fit to your projects.
- **Crowd wisdom with caution.** Community excitement can point to good ideas, but crowds also chase hype. Weigh it against your own experience.

## Radars

- **Thoughtworks Technology Radar**: published twice yearly; aggregates experience across many projects into rings for tools, techniques, platforms, languages and frameworks. Use it to discover options and gauge where each sits in the adoption cycle.
- **Personal radar**: the river of new things causes analysis paralysis. A simple self-made radar, revisited periodically, records what interests you and how ready it is. It need not be elaborate; the habit of checking in is the value. (The book expands on this in a later chapter.)

Minimal personal radar format (original):
```
quadrant: languages | tools | platforms | techniques
ring:     adopt | trial | assess | hold
entry:    name, ring, date, why, next action
```

## Decision checklist

Before investing time in, or proposing, a new technology:
1. What problem of mine or my team's does it solve? (No answer: park it at survey depth.)
2. Is this genuine interest or fear of missing out?
3. What older approach does it resemble, and what limited that approach?
4. What are the costs and consequences, not just benefits?
5. What do trusted peers and curated radars say? Has anyone in my network tried it?
6. Is it past the launch roughness, or still volatile? Can I wait until the last responsible moment?
7. If adopting: does it survive a test under our real constraints? (See introducing-technology-to-teams.md.)

## Worked example

A team lead asks whether to rewrite internal services on a newly announced service mesh because it is trending.
- Need: two teams struggle with retries and mTLS; real problem exists.
- Pattern: resembles earlier ESB and client-library approaches; ask how it avoids central bottlenecks and library sprawl.
- Costs: operational complexity, sidecar overhead, learning curve, upgrade churn.
- Signals: radar lists it as "assess"; a friend at another company ran it for six months and reports painful upgrades.
- Decision: keep at shallow dive for now, run a time-boxed workshop on a fork of one real service, revisit at the next radar review.

## Pitfalls

- Equating attention-grabbing with important.
- Treating personal excitement as a project requirement.
- Trusting intuition as certainty instead of as a hypothesis.
- Getting stuck comparing options forever; a personal radar and a time box break the paralysis.
