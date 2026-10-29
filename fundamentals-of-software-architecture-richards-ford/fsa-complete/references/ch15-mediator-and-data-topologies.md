# Mediated EDA and Data Topologies

## Contents
- When to switch from choreography to a mediator
- Mediator topology components and behavior
- Choosing mediator technology; the mediator delegation model
- Walkthrough of a mediated workflow (invented)
- Choreography vs mediation trade-off
- Data topologies: monolithic, domain, dedicated
- Selecting a data topology

## When to consider a mediator

Choreographed EDA gives up control: nobody owns the workflow, knows its state, or can restart it. Reach for the **mediator topology** (orchestrated EDA) when a flow needs ordered steps, central error handling, recoverability or restart from a known point.

## Mediator topology

Components: initiating event, event queue, **event mediator**, event channels, event processors.

How it behaves:
- The initiating event goes to the mediator via a queue.
- The mediator knows only the steps of the workflow. It emits **derived messages** (commands like `ship_order`, not facts like `order_shipped`) onto dedicated point-to-point channels, usually queues.
- Processors take a command, do the work, and usually reply to the mediator. They do **not** announce their work to the rest of the system.
- Steps can be sequential, while the commands inside one step run in parallel. The mediator waits for every acknowledgment of a step before starting the next.
- The mediator can persist workflow state, so it can stop on an error (for example, an expired card blocking payment) and later resume from the failed step, rather than starting over. At the end it marks the flow done and discards its state.
- Deploy several mediators, typically one per domain or event grouping (customer, order). This avoids a single point of failure and raises throughput.

### Choosing the mediator implementation
Classify by workflow complexity:

| Workflow nature | Suitable mediator class |
|---|---|
| Simple routing, simple error handling | Integration frameworks with code-defined routes (Apache Camel, Mule ESB, Spring Integration) |
| Many conditional branches, dynamic paths, complex error directives | BPEL engines (Apache ODE, Oracle BPEL Process Manager); BPEL is powerful but hard, so teams usually use the vendor GUI tooling |
| Long-running, with human steps in the middle (for example, a senior approver for an oversized order) | BPM engines such as jBPM |

Mismatch is costly both ways: an integration framework becomes painful for long-running human workflows, and a BPM engine for a simple flow can burn months on what an integration framework does in days.

### Mediator delegation model
Events rarely share one complexity class. Recommended approach:
1. Tag each initiating event as **simple, hard, or complex**.
2. Send every initiating event to a simple mediator first.
3. The simple mediator runs simple workflows itself and forwards hard ones to a BPEL-style mediator and complex ones to a BPM-style mediator.
4. Decide whether the simple mediator still tracks completion of forwarded events or hands over the whole workflow, client notification included.

## Walkthrough (invented): insurance claim, mediated

Initiating event: `submit_claim` arrives at the Claims mediator.
- Step 1: `register_claim` to Claim Registry; reply carries a claim number. Business rules decide whether the mediator returns that number to the customer now or only at the end.
- Step 2 (parallel): `check_policy`, `score_fraud_risk`, `notify_customer_received`. Wait for all three.
- Step 3 (parallel): `assign_adjuster`, `reserve_funds`.
- Step 4: `pay_claim` and `notify_customer_paid`.
If `check_policy` reports a lapsed policy, the mediator halts, saves state, and resumes at step 3 once the policy is reinstated.

## Choreography vs mediation

| Concern | Choreographed | Mediated |
|---|---|---|
| Workflow control and state | None central | Mediator owns it |
| Error handling, recoverability, restart | Hard | Built in |
| Processor decoupling | Highest | Lower |
| Performance and scalability | Highest | Good, but mediator must scale too and can bottleneck |
| Extensibility via hooks | Strong (broadcast) | Weaker (commands go to known targets) |
| Modeling dynamic behavior | Natural | Hard to express declaratively |

Core trade: **workflow control and error handling versus top-end performance and scalability.**

Because complex dynamic processing (out-of-stock, unusual errors) is hard to model in a mediator, many real systems are **hybrids**: the mediator drives the main path and choreography handles the dynamic edges.

## Data topologies

Running question for every option: where does a processor get data it does not own without making synchronous calls? Example need: an order-placement processor wants current stock levels and the shipping options for the customer's location.

### Monolithic (single shared database)
Most common.
- Gain: any processor reads what it needs directly, so processors stay decoupled and need not call each other.
- Fault tolerance: database outage takes down every processor.
- Scalability: processors scale independently (channels act as backpressure points), but the shared database must absorb all of their combined load, which many databases cannot do at high concurrency.
- Change control: one schema change can require coordinated changes across many processors.
- Quanta: the shared database forces the whole system into a single quantum.

### Domain (one database per domain)
- Gains over monolithic: better fault tolerance (one domain's outage leaves others accepting work, with the connecting channel queueing events until recovery), scaling per domain, schema changes scoped to the domain's processors.
- Cost: cross-domain data needs synchronous calls, which reintroduce coupling and erode the gains.
- Rule: keep domains largely independent and minimize synchronous cross-domain calls. If too many are needed, redraw the domain boundaries, merge domains, or fall back to monolithic.

### Dedicated (database per processor)
Same idea as database-per-service in microservices.
- Highest fault tolerance (outage isolated to one processor), highest scalability (each database sized for one processor), narrowest change impact.
- Costs: can be expensive depending on the database technology; the biggest problem is synchronous dynamic coupling, because a processor may need calls to several others to gather data.
- Good fit when processors are mostly self-contained within their bounded context.

## Selecting a data topology

1. Inventory every processor's data needs before choosing; list data it reads but would not own.
2. Count cross-boundary reads each option would create, under domain and dedicated boundaries.
3. If cross-boundary reads are rare, prefer dedicated (or domain) for fault tolerance, scale and change isolation.
4. If processors would chatter synchronously, move toward domain or even monolithic to protect performance and scalability.
5. If the schema changes very frequently, weigh isolating change (finer topology) against the operational cost of the synchronous calls it brings.
6. Consider data-based payloads as a way to deliver needed data inside events instead of via calls (see the payload reference for its costs).
7. Record the decision and the expected synchronous links so governance can watch them.
