# Architecture Katas and Requirement-by-Requirement Analysis

## Contents
- Why katas exist
- Kata format and how to run a session
- The per-requirement analysis procedure
- Silicon Sandwiches, analyzed in summary
- Design versus architecture for a characteristic
- A second worked example (invented)
- Review questions

## Why katas exist

Architects get few real chances to design whole systems (a handful per career), so practice must be manufactured. Ted Neward created architecture katas: short, timeboxed design exercises built from domain descriptions, named after martial arts form drills. The authors maintain an updated set on the book's companion site. The underlying idea, attributed to Fred Brooks, is that designers improve by designing.

## Kata format and how to run a session

A kata has four parts:
- **Description**: the domain problem.
- **Users**: expected number and/or kinds of users.
- **Requirements**: what domain experts expect.
- **Additional context**: facts outside the formal requirements that still shape design (ownership model, growth plans, labor or budget realities). The authors added this section to make exercises realistic.

Session playbook (works as a brown-bag lunch):
1. Split into small teams; give each the same kata.
2. Timebox the work. Output is a characteristics analysis plus diagrams, not a detailed design.
3. Teams present; the room votes on the best architecture.
4. An experienced architect critiques missed trade-offs and alternatives, live or afterward.

An agent can run a solo kata for a user: generate or accept a kata, produce the analysis below, then critique it as the "experienced architect" would.

## The per-requirement analysis procedure

The goal is not to design the whole system; domain design comes later. Look only for what influences design, especially structure.

1. Read the Users section first and decode volume statements into scalability and elasticity.
2. Ask about real usage rhythm to surface bursts nobody wrote down.
3. Walk each requirement and each context item. For each, record one of: no architectural impact; a design concern (handled in code, UX, patterns); or an architectural characteristic (needs structural support and is critical).
4. Separate explicit from implicit characteristics, then add the implicit ones that matter.
5. Check every candidate for overspecification and fragility.
6. Define performance together with scale.
7. Run the elimination exercise (drop the least important) and look for the simplest sufficient set.
8. Decide, with the team, which characteristics need architecture and which can be met by design.

Many requirements will map to nothing. That is normal and a sign of disciplined analysis.

## Silicon Sandwiches, analyzed in summary

Scenario: a national franchised sandwich chain adds online ordering to phone orders; user base in the thousands, possibly millions later; overseas expansion planned; low-cost labor is a corporate goal.

Outcomes of the walkthrough, in brief:
- **Scalability**: implied by the user projection, never named.
- **Elasticity**: not in the requirements at all, but mealtime peaks make it important.
- **Ordering, pickup/delivery choice, driver dispatch**: no special characteristic.
- **Directions with live traffic from external map services**: integration points touch reliability, but the site should degrade gracefully rather than fail.
- **Mobile access**: mostly a UX matter; given budget and app simplicity, one mobile-optimized web app beats several native apps, which suggests page-load performance targets. Vet this with UX designers and stakeholders, since some business needs force native apps.
- **National and local promotions**: customizability (also local overrides of directions and recipes).
- **Payments online, in shop, on delivery**: security, but only at the implicit level; with a third-party processor, design handles it.
- **Franchise ownership**: cost pressure; check feasibility against cost, time and skills and consider a simple or sacrificial architecture.
- **Overseas plans**: internationalization, solvable by design techniques; drives UX.
- **Cheap labor**: usability, again a design concern.
- **Performance**: nobody buys from a sluggish shop at peak, but define it against scale.
- **Implicit additions**: availability and stability.

Elimination result: the weakest candidates are customizability (could move into application design) and performance (least critical of the operational ones). Dropping performance as a driver does not mean accepting a slow app; it means scalability and availability win when they conflict.

## Design versus architecture for a characteristic

When a characteristic like customizability appears, decide where it lives. Architecture means structural support (for example a microkernel style with a core plus location-specific plug-ins). Design means handling it inside whatever style you pick (for example a Template Method pattern where a base workflow exposes overridable steps).

Ask three questions:
1. Are there solid reasons to avoid the structural option (performance cost, coupling)?
2. Does one option make other desired characteristics harder?
3. Which placement (structure or code) is cheaper once every chosen characteristic is accounted for?

Then decide with developers, tech lead, project manager, operations and domain analysts. Deciding alone produces the Ivory Tower antipattern.

Design-level customization sketch (original, framework-agnostic):

```python
class PromotionFlow:
    def run(self, cart):
        cart = self.apply_national(cart)
        return self.apply_local(cart)
    def apply_national(self, cart):
        return cart.discount(pct=5) if cart.weekday == "Mon" else cart
    def apply_local(self, cart):
        return cart  # default: no local promo

class LisbonFranchiseFlow(PromotionFlow):
    def apply_local(self, cart):
        return cart.add_free_item("pastel de nata")
```

## A second worked example (invented)

Kata: a city bike-share app. Users: 20,000 members, growing; commuter peaks 07:30 to 09:00. Requirements: unlock bikes by phone, show dock availability, charge per minute, monthly reports for the city. Context: docks have flaky cellular links; the operator plans to license the platform to other cities.

Analysis: scalability (growth) and elasticity (commute spikes); availability and fault tolerance (a failed unlock strands a rider), with offline-tolerant dock behavior; per-minute billing implies data integrity and auditability for disputes; city reports are a design concern; licensing to other cities suggests customizability or multi-tenancy, a strong candidate for architecture rather than design. Likely elimination candidate: the report requirement never was a characteristic; among real candidates, customizability could be deferred until the first licensing deal is signed.

## Review questions

1. Which user-volume phrase in your kata hides two different characteristics?
2. Which requirement did you tag as architectural that a design pattern could satisfy?
3. If an external dependency fails, does your design fail or degrade?
4. Which characteristic would you drop first, and what breaks if you are wrong?
