# Decision Antipatterns and Architectural Significance

## Contents
- What counts as a good architectural decision
- The three decision antipatterns (and why they arrive in sequence)
- Covering Your Assets: timing via the last responsible moment, plus collaboration
- Groundhog Day: technical plus business justification
- Email-Driven Architecture: one system of record, notify by impact
- Architectural significance: Nygard's five dimensions
- Pitfalls and review questions

## What a good decision does

An architectural decision is mostly about structure, but technology choices qualify too when they move an architecture characteristic. The test of quality is practical: the decision should steer development teams toward the right technical choices. Producing one has four parts, and skipping any of them produces one of the antipatterns below:

1. Gather enough relevant information.
2. Justify the decision (technical and business reasons).
3. Record it in one authoritative place.
4. Communicate it to the people it affects.

## The antipattern progression

An antipattern is a practice that looks sensible at first and then causes trouble, or a repeatable process that reliably yields bad outcomes. The chapter names three for decision making and observes that they tend to appear in order: fixing the first exposes the second, and fixing that exposes the third.

| Stage | Symptom | Root cause | Remedy |
|---|---|---|---|
| Covering Your Assets | Decisions are avoided or postponed indefinitely | Fear of being wrong | Decide at the last responsible moment; work closely with the implementing teams |
| Groundhog Day | The same decision is reargued in meeting after meeting | Missing or partial justification | Give both technical and business reasons |
| Email-Driven Architecture | People forget, lose, or never hear about the decision | Poor communication; email used as the archive | Single system of record; email only the context plus a link |

An agent reviewing a team's decision process should locate which stage they are stuck in before recommending anything.

## Covering Your Assets

**Symptom:** the architect delays or dodges a decision because a wrong call feels risky. The opposite failure, Analysis Paralysis, is endless study that never concludes; both block teams.

**Remedy 1: the last responsible moment.** Picture two curves over time:
- *Cost of deferring* starts low and climbs, because waiting consumes time and holds teams back.
- *Risk of deciding* starts high and falls, because each bit of analysis reveals more about the problem and the options.

Decide around the crossover, when the added cost of waiting is larger than the risk you would still remove by waiting. Operational prompt: "If we wait another iteration, what do we lose, and what uncertainty would that iteration actually resolve?" If the answer to the second half is "not much", decide now.

**Remedy 2: collaborate with implementers.** No architect knows every detail of every technology. Staying close to the teams who build the decision surfaces infeasibility early, so the decision can be corrected quickly rather than defended.

*Invented illustration:* an architect mandates that every service subscribe to a shared event stream for customer profile updates, to avoid synchronous lookups. During the first sprint a team discovers that their batch-oriented service cannot process the stream fast enough during month-end peaks. Because the architect attends that team's stand-ups, the decision is revised within days (that service reads from a nightly snapshot) instead of failing in production.

## Groundhog Day

**Symptom:** nobody remembers or understands why a choice was made, so it keeps resurfacing for debate without closure.

**Remedy:** justify fully, and always include the business side. A technical rationale such as "independent deployability and lower resource use" answers *how it is better*; it does not answer *why the business should fund it*.

The four most common business justifications:
- **Cost** (lower development, release or operating cost)
- **Time to market** (ship new capability faster)
- **User satisfaction**
- **Strategic positioning**

Rules of use:
- Pick the justification that matches what stakeholders actually care about now. A cost argument falls flat with sponsors who are focused on speed.
- Treat business value as a gate: if you cannot name any, reconsider whether the decision should be made at all.

## Email-Driven Architecture

**Symptom:** a decision exists but is invisible, lost in inboxes, or known only to whoever was on the thread. Email works for messaging but fails as a repository.

**Why putting the decision text in an email is harmful:**
- Every copy becomes a competing system of record.
- Copies tend to drop the rationale, which re-creates Groundhog Day.
- When the decision is later changed or superseded, there is no way to be sure everyone sees the new version.

**Remedy:**
- In the message, state only the topic and context of the decision and link to the single authoritative record (wiki page, ADR repository, shared document).
- Notify a person directly only if the decision directly affects them. This is also the filter for choosing which developers and stakeholders to contact.

*Template (your own wording):* "Hi Priya, I've recorded a decision about how the reporting jobs read customer data; it changes how your team schedules extracts. Details and rationale are here: <link>."

## Architectural significance

A common mistake is to classify anything naming a product or framework as "merely technical". If a technology is chosen because it directly serves a characteristic (performance, scalability, and so on), the choice is architectural.

Michael Nygard's term *architecturally significant* gives a scope test. A decision is significant if it affects any of:

| Dimension | What it covers | Example signal |
|---|---|---|
| Structure | Which architecture style or patterns are used | Sharing a code library across microservices widens their bounded contexts |
| Non-functional characteristics | Characteristics critical to this system | A serialization library chosen because latency is a top priority |
| Dependencies | Coupling points between components or services | Introducing a synchronous call chain that affects scalability, testability, reliability |
| Interfaces | How services and components are reached and orchestrated (gateway, hub, bus, adapter, API proxy) | Contract definition, versioning and deprecation policy |
| Construction techniques | Platforms, frameworks, tools, even processes | Adopting a build platform or release process that constrains deployability |

Agent rule: if a proposal touches any row, treat it as an architectural decision and record it; if it touches none, it is likely a design or implementation choice the team can own.

## Pitfalls

- Treating "we need more data" as a permanent state. Ask what specific data would change the outcome.
- Justifying only technically, then being surprised when the decision is reopened by someone with budget authority.
- Using cost as the default business reason without checking stakeholder priorities.
- Pasting the full decision into a chat or email "for convenience".
- Broadcasting every decision to everyone, which trains people to ignore notifications.
- Dismissing a vendor or framework choice as non-architectural when it was selected for a characteristic.

## Review questions (original)

1. A team has postponed choosing a messaging technology for three sprints. What two questions would establish whether the last responsible moment has passed?
2. Rewrite a purely technical rationale for splitting a database into one that also names a business justification aligned with a sponsor focused on time to market.
3. Which of Nygard's five dimensions does a new API versioning policy fall under, and why does that make it architectural?
