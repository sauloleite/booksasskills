# Style Fit, Risks, Governance and Teams

## Contents
- Choosing request-based vs event-based
- Characteristics profile (qualitative)
- Partitioning and quantum counting
- Cloud fit
- Common risks
- Governance and fitness functions
- Team topology fit
- Use cases and a fit worked example
- Self-review questions

## Choosing request-based vs event-based

Default rule from the chapter:
- **Request model** for well-structured, data-driven requests (fetch a profile, list orders) where certainty and control of the workflow matter most.
- **Event model** for flexible, action-driven situations needing high responsiveness and scale, with complex and dynamic processing.
- If most of the required processing is request-based, look at microservices instead of EDA.

In short, the event model wins on three fronts: reacting quickly to changing, real-world situations; absorbing load (speed, scale, elasticity); and absorbing change (new consumers and features attach easily). It loses on predictability: consistency is eventual, the flow is not centrally steered, its end state is uncertain, and it is hard to test and debug.

EDA is powerful but complicated. Study the actual workflows and decide whether the problem justifies that complexity.

## Characteristics profile

Strong points:
- **Performance**: async communication combined with heavy parallelism.
- **Scalability and elasticity**: competing consumers / consumer groups let you add processor instances programmatically as load rises. The database usually caps it (space-based architecture removes that cap, which is why it scores above EDA here).
- **Fault tolerance**: decoupled async processors and eventual consistency; work waits for unavailable downstream processors, as long as the requester does not need an immediate answer.
- **Evolvability**: very high. New behavior attaches to existing derived events without touching infrastructure or existing processors.

Weak points:
- **Simplicity and testability**: low, because flows are nondeterministic. Event trees can branch into hundreds or thousands of scenarios.
- **Workflow control**: hard to know when the business transaction for an initiating event is complete.
- **Error handling**: without a mediator nobody watches the transaction; a failed processor leaves that transaction stuck while other processors carry on as if all is well (inventory gets decremented although payment crashed).
- **Recoverability**: restarting a transaction is hard; resubmitting the initiating event is often impossible because side effects already happened.

## Partitioning and quantum counting

- EDA is mainly **technically partitioned**: a domain is spread over many processors, brokers, contracts and topics, so a domain change touches many artifacts.
- Quantum count ranges from one to many. Merge processors into one quantum when they:
  - share a database instance, or
  - are linked by request-reply (the requester blocks on the responder's availability, even though transport is async).
- Procedure: draw processors as nodes, connect any pair sharing a database or joined by request-reply, and count connected components. Each component is a quantum with its own characteristic profile.

## Cloud fit

Good match. EDA's decoupling fits managed async services from cloud vendors, and elastic infrastructure suits independently scaled processors.

## Common risks

1. **Nondeterministic side effects**: processors emitting unexpected derived events or failing to react when they should; hard to predict what an event will set off.
2. **Static coupling and brittleness through payload contracts**: dynamic coupling is low, but contracts couple statically, and you may not know who consumes an event before you change it. Key-based payloads reduce this but bring scale, performance and anemic-event risks.
3. **Too much synchronous communication** between processors: a strong signal EDA is the wrong style for this problem.
4. **State management**: hard to know when an initiating event is fully processed or what state it is in. Sometimes you can identify a terminal event and have the initiating processor subscribe to it; often you cannot.

## Governance

Most EDA governance is non-structural: it relies on observability (logs) feeding a governance mesh, and some metrics may need manual collection.

Two kinds of structural decay to watch:

**Static coupling (contracts)**
- Track how often each event payload contract changes; schema-less contracts are the riskiest to change because end-to-end flows are so hard to test.
- Track stamp coupling: continuously record which fields of each event each consumer actually uses. Unused fields are candidates for trimming, which cuts bandwidth and needless consumer changes.

**Dynamic coupling (synchronous calls)**
- Automated fitness functions should detect synchronous calls between processors via logs, source annotations, or a standard library that tags sync calls with a custom identifier.
- Every sync call should be reviewed to confirm it is necessary, especially under domain or dedicated data topologies.

Example fitness function sketch (pseudocode):

```python
ALLOWED = {("order-placement", "shipping")}   # approved by ADR

def check(call_log):
    violations = []
    for rec in call_log:
        if rec["mode"] == "sync" and (rec["src"], rec["dst"]) not in ALLOWED:
            violations.append(rec)
    return violations   # fail the build or alert if non-empty
```

Other useful metrics an agent can propose: fields-used ratio per event per consumer; count of event types with breaking changes per release; events with no producer; event-type cycles.

## Team topology fit

- EDA works acceptably with cross-functional teams aligned to domain areas.
- **Stream-aligned**: struggles as the system grows, because one domain change (adding a step to a workflow) may mean editing several processors and reshaping when derived events fire. Effectiveness drops with size and complexity.
- **Enabling**: poor fit. Their experimentation inside a stream disturbs the stream team's grasp of event flows and demands too much coordination around contracts.
- **Complicated-subsystem**: good fit. Complex logic isolates cleanly into separate processors; coordination with stream teams is limited to payload contracts and derived events.
- **Platform**: good fit. Brokers, event hubs, buses and channels can be offered as platform services, thanks to EDA's technical partitioning.

## Use cases

Strong candidates: anything reacting to things happening (inside or outside the system); workloads demanding responsiveness, performance, scalability, fault tolerance and elasticity. Order entry (parallel, decoupled handling) and online auctions (unknown, spiky bidder counts near close; a bid treated as a fact, then fanned out to price update, bid-history streaming and audit tracking) are the chapter's examples.

### Worked fit example (invented): parking-garage sensor platform
Sensors report spaces freed or taken. Facts, many consumers (signage, mobile app, billing, analytics), bursty load at rush hour, no user waiting on a reply. Choose choreographed EDA with small data-based payloads (space ID, state, timestamp). Billing needs ordered, recoverable steps (start session, end session, charge); put that behind a mediator. Admin screens that query occupancy history are request-based; serve them via an API over a read store rather than events.

## Self-review questions (original)
1. Which flows in this system actually need to know when they are "done", and how will you detect that?
2. Which processors would join into one quantum because of a shared database or request-reply?
3. Which contracts have consumers you cannot enumerate, and how will you change them safely?
4. Which synchronous calls exist, and which ADR approved each?
5. Which team owns the end-to-end understanding of each event flow?
