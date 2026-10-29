# Fit Assessment, Team Alignment and a Worked Example

## Contents
- Qualitative characteristics profile
- When the style fits / when it does not
- Team topology alignment
- Worked example (invented): a clinic booking system
- The chapter's own example in brief
- Review questions

## Qualitative characteristics profile

Classification: domain-partitioned; architectural quantum normally 1.

Strong:
- **Cost** to build and run: low, no distributed infrastructure.
- **Simplicity**: one process, one deployment, easy to reason about and debug.
- **Modularity**: domain modules give real separation of concerns.

Middling (slightly better than a layered monolith thanks to modularity, but still limited):
- **Deployability**: every release ships everything, so ceremony and risk stay high and frequency stays low.
- **Testability**: modules can be tested in isolation, yet confidence in a full release still requires broad regression.

Weak:
- **Scalability and elasticity**: the whole unit scales together. Scaling one function harder than others demands threading, in-process messaging or parallel-processing tricks the style is not built for.
- **Fault tolerance**: one bad module (for example an out-of-memory condition) takes down everything.
- **Availability**: recovery means restarting the whole unit, which often takes minutes, so mean time to recovery is high.
- **Performance and responsiveness under heavy load**: no way to isolate hot paths.

## When it fits
- Tight budget or schedule.
- Greenfield work where the long-term architecture is not yet clear. Starting here and later migrating to service-based or microservices is usually cheaper than starting distributed.
- Teams organized by domain (cross-functional, each owning a business area end to end).
- Most expected changes are domain changes (a new rule, a new field on one business concept).
- Teams practicing DDD; bounded contexts map naturally onto modules.

## When it does not fit
- Demanding operational characteristics: high scalability, elasticity, availability, fault tolerance, responsiveness or performance.
- Most expected changes are technical and cross-cutting (swapping the UI framework, replacing the database technology). Each such change touches every module and forces coordination across domain teams; a layered architecture handles that pattern better.

### Quick decision rule
1. List the top 3 architecture characteristics. If any is scalability, elasticity, fault tolerance or high availability, look at distributed styles.
2. Classify the expected change stream. Mostly domain changes favors this style; mostly technology-layer changes favors layered.
3. Check team shape. Domain-aligned teams favor this style; teams split by technical layer fight it.
4. If 1 to 3 pass, prefer a modular monolith, especially under cost/time pressure or high uncertainty.

## Team topology alignment

General rule: domain-partitioned architecture wants domain-aligned teams. Teams split into UI, backend and database groups will need heavy coordination for every domain requirement.

| Team type | How it aligns |
|---|---|
| Stream-aligned | Owns a flow from front to back; matches the self-contained module shape well. |
| Enabling | Specialists can trial ideas by adding a new module with little effect on existing ones. |
| Complicated-subsystem | A module with hard domain logic (pricing, payments, forecasting) can be owned by specialists independently of others. |
| Platform | Shared tools, services and APIs are easy to consume because modules have clear seams. |

## Worked example (invented): clinic booking system

Context: a three-location physiotherapy clinic wants online booking, reminders, billing and therapist schedules. Two developers, small budget, a few hundred bookings per day, no peak-load concerns. Expected changes: new appointment types, new insurance rules.

Assessment:
- Characteristics: cost, simplicity and maintainability dominate; no elasticity need. Passes.
- Change stream: domain-driven. Passes.
- Team: one small cross-functional team. Passes.
Decision: modular monolith, single code base, one shared database with a schema per module.

Modules and components:
```
clinic.booking      .availability .reservation .cancellation
clinic.patients     .profile .consent
clinic.therapists   .schedule .leave
clinic.billing      .invoice .insurance .card
clinic.reminders    .sms .email
```

Communication: booking a session needs therapists (availability), patients (profile) and billing (deposit). A small `clinic.booking` facade orchestrates those calls; reminders listen to "appointment confirmed" via an in-process event so booking does not depend on reminders.

Governance: membership check over the five prefixes; coupling budget of 5 per module; forbidden pair `reminders -> billing`.

Revisit triggers: a franchise expansion to 50 locations with national marketing peaks would make elasticity matter; at that point extract booking first.

## The chapter's own example in brief
The book walks through a small meal-delivery restaurant with modest load and a small budget. Its modules cover ordering, payment, kitchen preparation, delivery, recipe maintenance and ingredient inventory, each subdivided into a handful of component namespaces. Two points worth keeping: a module typically contains several components, and a new variant (another payment method) slots in as one more component without disturbing other modules. Even the one sophisticated part (sales forecasting to automate ingredient purchasing) lives comfortably inside a single module.

## Review questions
1. Which namespace segment tells you whether a code base is domain- or technically partitioned?
2. Under what conditions would you build modules as separate artifacts instead of folders in one repository?
3. What coupling does a mediator remove, and what coupling does it introduce?
4. Name four symptoms that a modular monolith has grown too large.
5. Why is a modular monolith a poor choice when the UI framework is replaced every year?
6. How would you enforce that one module never calls another, on your current platform?
