# Refining Components: Cohesion, Characteristics, Restructuring

## Contents
- Roles and responsibilities analysis
- The responsibility-statement test
- Architecture characteristics as a sizing force
- Restructuring as a continuous activity
- Case study pattern: one capability, two characteristic profiles
- Choosing among valid designs
- Checklist
- Review questions

## Roles and responsibilities analysis

Goal: confirm that the stories assigned to a component belong there and that it is not doing too much. The concern is **cohesion**: how strongly, and how much, the operations of a component relate to one another.

Key subtlety: a component can grow too large even when every operation is related to the same theme. "All of this is about checkout" is not proof that it belongs in one component.

Also remember the physical consequence: a component is one directory/namespace. If the list of responsibilities implies a large amount of code in one folder, that alone is a hint to split.

## The responsibility-statement test

Procedure:
1. Write a short prose statement of what the component is responsible for, covering every assigned story.
2. Scan it for conjunctive glue: "and", "also", "in addition", "as well as", and long comma-separated runs.
3. Each clause joined by glue is a candidate for its own component. Prefer extracting clauses that are a different kind of work (moving money, changing stock, messaging customers) from the component's core purpose.
4. Rewrite the statement for the slimmed component. It should read as one sentence with one verb phrase or a tight cluster.

Invented example, a `Claim Intake` component in an insurance system with these stories: validate claim form; show policy coverage summary; capture photos of damage; assign claim number; run fraud scoring; reserve funds for payout; text the claimant a confirmation.

Statement: "Validates the claim form and shows coverage, captures damage photos, assigns a claim number, and also runs fraud scoring, reserves payout funds, as well as texting the claimant."

Split result:
- Claim Intake: validate form, show coverage, capture photos, assign claim number.
- Fraud Scoring: run fraud scoring.
- Payout Reserve: reserve funds.
- Claimant Messaging: send confirmation text.

Each piece now has a crisp purpose and is easier to maintain, test and deploy.

The bundled `scripts/component_lint.py` automates steps 2 and 3 as an advisory scan (glue words, comma runs, Entity Trap suffixes). A single "and" is often harmless, so it flags only repeated glue by default.

## Architecture characteristics as a sizing force

After functional cohesion, check the characteristics the system must support. Several of them influence component size:

| Characteristic | Pressure on component size |
|---|---|
| Scalability, elasticity | Split parts with very different load or burst profiles |
| Fault tolerance, reliability, availability | Split parts that need stronger guarantees so failures elsewhere do not drag them down |
| Agility (fast response to change), maintainability, testability | Smaller, focused components are easier to change and test |

Rules:
- Two parts that look functionally identical may still need separating if their characteristic needs differ (for example, one input path serves hundreds of concurrent users, another serves a handful).
- This step requires knowing which characteristics matter, so do it after the characteristics have been identified and prioritized, not before.
- A purely functional view tends to merge; a characteristics view may subdivide. Record the reason for any split so it is not "simplified" back later.

## Restructuring as a continuous activity

- Iterate on component design together with developers; feedback is essential.
- Two reasons iteration is unavoidable: you cannot foresee every discovery and edge case that forces redesign, and building the system gives the team a sharper sense of where behavior belongs.
- Expect frequent restructuring for the whole life of the system, not only during greenfield design; any system under active maintenance will need it.
- Practical moves: split a component, merge two thin ones that always change together, move a story, introduce a shared component, rename to reflect the real role, and move the code to match.

## Case study pattern: one capability, two characteristic profiles

The chapter's auction example (Going, Going, Gone) shows the full loop:
1. Seed with Actor/Action (recommended default when there are no special constraints). Actors: bidder, auctioneer, and the system. Actions map to components such as video streaming, bid streaming, bid capture, bid tracking (system of record), auction session control, and an external payment processor.
2. Revisit with characteristics. A single bid-capture component is fine functionally, but the two sources differ: online bidders may number in the thousands (scalability, elasticity), while the single on-site auctioneer needs connections that never drop and a system that stays up (reliability, availability). Losing a bidder is bad; losing the auctioneer is a disaster.
3. Split: keep bid capture for online bidders and add a separate auctioneer capture component. Rewire it to feed both the bid streamer and the bid tracker; the tracker now merges one auctioneer stream with many bidder streams.
4. Accept that this is a starting point. Registration, payment administration and more remain to be discovered.

Generalize: whenever one component serves actors with sharply different operational needs, consider splitting along the actor boundary even if the logic is the same.

Invented parallel: a ride-hailing "Location Update" component receives GPS pings from drivers (massive volume, tolerant of occasional loss) and from dispatch supervisors manually overriding a vehicle position (rare, must never be lost). Split into Driver Telemetry Intake and Dispatch Position Override.

## Choosing among valid designs

- Most systems can be decomposed in many reasonable ways. Do not hunt for a single perfect design.
- Compare alternatives on their trade-offs as objectively as you can and pick the one whose trade-offs hurt least.
- When presenting options to a user, show two or three candidate decompositions with the trade-off each makes, rather than one "answer".

## Checklist

- [ ] Every component has a responsibility statement of one or two sentences without heavy conjunctions.
- [ ] No component contains a distinct kind of work (payments, stock, messaging) that is only incidentally related.
- [ ] Characteristics were prioritized before characteristic-driven splits.
- [ ] Parts with different load, reliability or availability needs are separated, and the reason is recorded.
- [ ] Component list and code directories still match after restructuring.

## Review questions

1. A component's statement has no conjunctions but its directory holds a very large amount of code. What do you investigate?
2. Name a case where splitting for scalability would be wrong because the two parts must change together.
3. How would you explain to a team why the design will keep changing after go-live?
