# The Three Laws and How to Apply Them

Covers: the section on the laws of software architecture, including both corollaries of the first law.

## Background

The authors set out hoping to collect a dozen or so universal truths about architecture. They found only two while writing the first edition and a third during the second. The scarcity is itself instructive: almost nothing in architecture holds universally, because nearly every judgment depends on context. The laws below are the few exceptions, and the book returns to them repeatedly (and revisits them with more examples near the end).

## Law 1: trade-offs are unavoidable

In short: no architectural choice comes free; every option buys some qualities by giving up others.

Each decision juggles many variables whose values shift with circumstances, and options rarely line up along a tidy single axis.

**Corollary A (hidden trade-off).** If something looks like a pure win, the cost has simply not been discovered yet.

**Corollary B (no permanent answers).** Trade-off analysis cannot be done once and frozen.

### Playbook: hunting the hidden trade-off

When a user or document presents a choice as cost-free, probe these axes before accepting it:

- Operational complexity and on-call burden
- Coupling (data, deployment, temporal, semantic)
- Consistency versus availability under failure
- Performance and latency across new network hops
- Team cognitive load, skills and hiring
- Cost: licensing, cloud spend, migration effort
- Testability, debuggability and observability
- Reversibility: how expensive is undoing the choice later

If none of these reveals a downside, widen the time horizon (what happens in two years, at ten times the load, after the original team leaves).

### Pitfall: the one-shot standards meeting

Teams like standards, and it is tempting to hold a single session that fixes defaults for styles, communication patterns, handling of shared functionality and similar recurring questions. Resist it. Each new situation shifts the variables. The book cites teams that mandated choreography for every distributed workflow and found it worked in some cases and failed badly in others.

Acceptable alternative: publish defaults as *starting hypotheses* with the conditions under which they hold, and require a fresh trade-off check when those conditions are not met.

## Law 2: rationale outweighs mechanism

An experienced architect can usually work out how an unfamiliar architecture functions by reading it. What cannot be recovered from the artifact is why the team chose it: the context, the alternatives rejected and the trade-offs accepted. Because decisions are made in very specific contexts, sweeping generic decisions are hard to justify, which makes the recorded "why" the most valuable and most perishable part of an architecture.

### Checklist: minimum rationale for any significant decision

- Context and forces at the time (constraints, deadlines, team, costs)
- Options considered, including "do nothing"
- The characteristics each option favors and harms
- The chosen option and why its costs were acceptable
- Conditions that would trigger revisiting the decision

## Law 3: decisions live on a spectrum

Most architectural choices are not binary. Between "fully shared database" and "one database per service" lie schema-per-service, shared read replicas, and domain-scoped databases. Between "synchronous" and "asynchronous" lie request/reply over messaging, async with callbacks, and so on.

### Technique: reframing a binary debate

1. Name the two extremes the debate is stuck on.
2. List three or more intermediate positions.
3. For each, note which characteristics improve and which degrade.
4. Choose the position whose profile matches the prioritized characteristics, and record why neighbors on the spectrum were rejected.

## Worked example (invented)

A tech lead says: "We should put all shared code in a common library; reuse has no downside."

- Law 1, Corollary A: the hidden cost is coupling. Every consumer must upgrade in lockstep, and a change to the library can break unrelated services.
- Law 3: options range from copying code, to a versioned library, to a shared service, to a sidecar. Each moves the cost between duplication, coupling, latency and operational overhead.
- Law 2: whatever is picked, record the volatility of the shared code and the team topology that justified it.
- Corollary B: if the shared code later starts changing weekly, re-run the analysis.

## Self-check questions (original)

- Can you name the downside of the option you currently favor? If not, which axis have you not examined?
- Which of your team's standing defaults was last re-validated more than a year ago?
- Would a newcomer reading your decision records understand why, not only what?
- In your latest either/or debate, what were the middle options?
