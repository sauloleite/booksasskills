# Qualifying Architecture Characteristics

## Contents
- Where characteristics sit in structural design
- Terminology: why "architecture characteristics"
- The three-part qualification test
- Design versus structure: the decisive question
- Implicit versus explicit characteristics
- Interplay of the three criteria
- Worked examples
- Pitfalls

## Where characteristics sit in structural design

Structural design combines two activities that can run in either order or in parallel: characteristics analysis (this skill) and logical component design. They meet at a join point where components must be shaped to support the selected capabilities. The domain describes what the system does (behavior); characteristics describe what it must be capable of in order to succeed (capabilities), plus the operational and design criteria that explain how and why implementation choices were made. Identifying characteristics is a large part of what separates architecture work from coding and detailed design.

## Terminology: why "architecture characteristics"

- **"Non-functional requirements"** undersells the concern: labeling something as not functional makes it harder to get teams to invest in it. The phrase traces back to late-1970s function point estimation, where effort tied to capabilities was counted as "non-function points". Function point analysis looked precise but was subjective and has faded; the label survived.
- **"Quality attributes"** suggests assessment after the fact rather than intentional design.
- **"Architecture characteristics"** signals concerns critical to the system's success without diminishing them. Head First Software Architecture calls them the system's capabilities, contrasted with domain behavior.

Agent guidance: accept whatever term the user's organization uses, but frame the work as designing capabilities up front, not as auditing quality later.

## The three-part qualification test

| Criterion | Question to ask | If it fails |
|---|---|---|
| Nondomain | Is this about how the system must operate or be built, rather than a business behavior? | It belongs in domain design. |
| Structural influence | Does satisfying it require a specific architectural structure? | It is a coding or design standard. |
| Critical or important | Would the system fail or be seriously harmed without it? | Drop it; extra characteristics add complexity. |

All three must hold. A concern can be nondomain and important yet still be handled purely by design, in which case it becomes a team standard, not an architectural driver.

## Design versus structure: the decisive question

For each candidate ask: can disciplined implementation satisfy this, or must the architecture provide dedicated structure?

- **Security** can go either way. In a monolith, encryption, hashing, and salting applied consistently may suffice (design). In a distributed system, an architect may isolate sensitive functionality in a separately hardened service with tighter access rules (structure). Governance through fitness functions is a related mechanism.
- **Scalability** is the classic structural one. Past a certain load, no design cleverness lets a monolith keep scaling; the style itself must become distributed.
- **Operational characteristics** (performance, scalability, elasticity, availability, reliability) are the group most likely to need structural support, so scrutinize them first.

## Implicit versus explicit characteristics

- **Explicit**: written in requirements or given as specific instructions (for example, "support 50,000 concurrent users").
- **Implicit**: rarely written but needed for success. Availability, reliability, and security underpin nearly every system. Domain culture also creates implicit ones: in high-frequency trading, nobody writes "low latency" because everyone assumes it.
- Performance targets and avoiding technical debt are common examples of concerns that matter but seldom appear in requirements documents.

Agent guidance: after extracting explicit items, deliberately ask "what would experienced practitioners in this domain assume without saying?" and list those as implicit candidates for the three-part test.

## Interplay of the three criteria

The three criteria reinforce one another and support the overall design. Characteristics also lean on each other like weights on a balance point, which is why architecture discussions revolve around trade-offs. Treat any single characteristic decision as provisional until its effect on the others is checked.

## Worked examples

1. **"All data at rest must be encrypted."** Nondomain: yes. Structural: usually no, a platform or library standard handles it. Critical: yes (legal). Verdict: a security standard, not a structural driver, unless key isolation demands a dedicated service.
2. **"Ticket sales must survive 100x traffic at release time."** Nondomain: yes. Structural: yes, bursts of that size need elastic, independently scalable parts. Critical: yes. Verdict: elasticity and scalability are architecture characteristics.
3. **"Users can export reports as PDF."** Domain behavior. Verdict: not a characteristic.
4. **"The UI should be pleasant."** Nondomain, but not structural and too vague to be critical. Verdict: a design concern; if usability is truly critical, restate it with an objective measure.
5. **Internal B2B integration hub with no stated uptime target.** Implicit availability: partners' processes stall when it is down. Add availability as an implicit candidate and test it.

## Pitfalls

- Treating every "-ility" in a template as mandatory.
- Missing implicit characteristics because they are absent from documents.
- Promoting a concern to architectural status when a coding standard would do, which inflates complexity.
- Assuming a concern is design-only in a monolith and forgetting it may need structure after migrating to a distributed style.
