# Limiting and Prioritizing Characteristics

## Contents
- Why the list must stay short
- Overspecification and the Vasa
- The characteristics worksheet session
- Choosing the top three
- The elimination exercise
- Facilitation pitfalls

## Why the list must stay short

Every characteristic the architecture supports adds design complexity, before any domain problem has been solved. Trying to build a generic architecture that supports everything is an antipattern. Do not fixate on an exact count; keep the motivation in view: a simple design.

Characteristics are synergistic: each interacts with the others. That is why overspecifying hurts as much as underspecifying. Too few, and the system misses critical needs; too many, and it is overcomplicated, slower to build and harder to change.

There is no perfect set. Many implementations can satisfy functionality, but identifying the right structural elements makes a simpler, cleaner design possible. Treat any result as the least bad combination of trade-offs, not a best design. A useful framing from the chapter: the costly mistakes, not the "wrong" ones, are what to avoid.

## Overspecification and the Vasa

The Vasa, a Swedish warship commissioned in the 1620s, was meant to be both troop transport and gunship, with two gun decks and oversized cannons. Builders had doubts but could not refuse the king. On its maiden voyage in Stockholm harbor it fired a salute, rolled over because it was top-heavy, and sank. It was raised in 1961 and is now a museum piece. Use it as a shorthand with stakeholders: piling on capabilities can sink the whole project.

## The characteristics worksheet session

Problem: hand stakeholders a long menu of characteristics and ask which they want, and they will pick all of them. You need a forcing structure.

The authors' worksheet (downloadable from developertoarchitect.com) structures an architect-led interactive session:

- **Driving characteristics column**: a fixed small number of slots, seven in the authors' version. Six or eight also work; the point is a hard cap.
- **Implicit characteristics column**: prelisted items most systems need anyway. When one becomes a driving concern needing special design, pull it into the driving column.
- **Others considered**: when the driving column is full and a stronger candidate appears, move the displaced item here. Nothing is lost, and the record explains the trade.
- **Top three marks**: finally, mark the three highest priorities.

Agent playbook for running or simulating the session:
1. Collect candidates from the elicitation pass (domain concerns, requirements, implicit knowledge).
2. Fill driving slots up to the cap; keep everything else in implicit or others considered.
3. For each implicit item, ask whether it needs special structural design here; if yes, pull it in.
4. On overflow, compare the newcomer with the weakest slot holder and demote one to others considered, noting why.
5. Ask stakeholders to pick three.
6. Record the worksheet as an input to trade-off analysis and decision records.

Example worksheet state (invented, for a B2B invoicing platform):

```text
Driving (max 7): availability, data integrity*, auditability*, scalability,
                 interoperability*, security, deployability
Implicit kept implicit: usability, feasibility, maintainability
Others considered: elasticity (no burst pattern found), performance (beat by integrity)
* = top three
```

## Choosing the top three

Many teams want a fully ordered final list. In practice this wastes time and creates friction because stakeholders seldom agree on a total ordering. Instead ask them to choose the three most important characteristics, unordered. Consensus is far easier, the discussion surfaces what really matters, and the result is enough to steer trade-off decisions.

## The elimination exercise

After a first pass, ask: if one characteristic had to go, which one? This tests critical necessity using the definition of a characteristic (structural impact plus criticality to success).

Guidance:
- Explicit characteristics are cut more often; implicit ones usually underpin overall success.
- A cut characteristic can move into application design instead of disappearing (customizability via a design pattern).
- Deprioritizing an operational characteristic such as performance is not permission for poor quality; it states which characteristic wins in a conflict.
- There is no single right answer; the value is in the reasoning made visible.

## Facilitation pitfalls

- Presenting a long menu and asking "which do you want".
- Insisting on a complete ranking.
- Letting the list grow past the cap because everything sounds good.
- Accepting a characteristic without asking whether design alone could satisfy it.
- Running the session without developers and operations, then imposing the result (Ivory Tower).
- Hunting for the "correct" set instead of a defensible, simple one.
