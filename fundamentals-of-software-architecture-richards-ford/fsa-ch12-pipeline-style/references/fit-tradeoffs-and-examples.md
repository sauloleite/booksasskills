# Fit, Trade-offs and Examples

## Contents
- Classification
- Qualitative strengths and weaknesses
- The distribution trade-off
- When to use / when not to use
- Where the style appears in practice
- Worked example: telemetry routing
- Invented example: invoice ingestion
- Review questions

## Classification

- **Partitioning**: technical. Logic is separated by filter type (ingest, transform, test, output), not by business domain.
- **Architectural quantum**: one in the usual monolithic deployment.
- **Deployment**: normally a single unit; can be distributed per filter or per group.

## Qualitative strengths and weaknesses

Strong:
- **Cost** and **simplicity**: no distributed-system complexity in the default form; easy to understand, cheap to build and maintain.
- **Modularity**: a filter can be changed or swapped without touching others, as long as its pipe contracts hold.

Middling:
- **Deployability** and **testability**: a little better than a layered monolith because filters isolate change, but still a monolith, so deployments carry ceremony and risk, happen less often, and full regression testing is needed.

Weak (in the monolithic form):
- **Scalability** and **elasticity**: the whole unit scales together.
- **Fault tolerance**: one filter exhausting resources (for example running out of memory) crashes everything.
- **Availability**: monoliths tend to have high mean time to recovery, with restarts measured in minutes.

## The distribution trade-off

Turning each filter into its own deployment unit with asynchronous remote pipes substantially improves scalability, elasticity and fault tolerance. It also raises cost and erodes simplicity. Present this to stakeholders as an explicit choice:

| If the driving characteristics are... | Recommend |
|---|---|
| Cost, simplicity, time to market, modularity | Monolithic pipeline |
| Scalability, elasticity or fault tolerance, with budget for operational complexity | Distributed pipeline with async pipes |
| Those operational characteristics plus nondeterministic routing | Event-driven architecture instead |

Record the decision with the characteristic that tipped it, so it can be revisited if priorities change.

## When to use / when not to use

Use when:
- The work is a set of distinct steps in a fixed order, deterministic, flowing one way. System size or complexity is not the criterion.
- Time and budget are tight and a simple, understandable structure matters.

Avoid when:
- High scalability, elasticity and fault tolerance are required and the team will not distribute the filters (distribution helps, at a cost).
- Steps need to converse (request and reply between filters).
- The workflow is nondeterministic. It can be simulated with many testers, but that bloats a simple style and hurts maintainability, testability, deployability and reliability. Prefer event-driven architecture.

## Where the style appears in practice

- **EDI tools**: converting one document format into another through chained transformations.
- **ETL tools**: extracting, reshaping and loading data between sources and targets.
- **Integration frameworks and mediators** (Apache Camel is the classic example): moving a message through the steps of a business process.
- **Shell scripting, MapReduce jobs, stream processors**.

## Worked example: telemetry routing

Services stream telemetry into a Kafka topic. The pipeline:

1. **Producer**: subscribes to the topic and receives service information. Its only concern is connecting to and reading from the stream.
2. **Tester (duration?)**: checks whether the record describes request duration in milliseconds. Its only concern is qualification and routing.
   - Yes: go to the **duration calculator** transformer.
   - No: go to the next tester.
3. **Tester (uptime?)**: checks whether the record relates to uptime.
   - No: the flow ends; the record is irrelevant to this pipeline.
   - Yes: go to the **uptime calculator** transformer.
4. **Consumer**: writes calculated metrics to a MongoDB store.

Lessons:
- Separation of concerns is visible: ingestion knows nothing about metrics, testers know nothing about calculation.
- Modifiability: the duration formula can change inside its calculator alone.
- Extensibility: a new metric (for instance database connection wait time) is added by inserting another tester after the uptime tester plus its own calculator, with no change to existing filters.

## Invented example: invoice ingestion

Context: a finance team receives supplier invoices as PDFs and CSVs and must load approved ones into the ERP.

- Producer: watch an inbox folder.
- Transformer: extract fields to a canonical invoice record.
- Tester: reject records with missing tax IDs (divert to a quarantine consumer).
- Transformer: enrich with supplier master data.
- Tester: stop if amount exceeds an approval limit (divert to manual review consumer).
- Consumer: post to the ERP.

Assessment: ordered, deterministic, one-way; tight budget; modest volume. A monolithic pipeline fits. Risks to address: define what happens if the ERP is down (fatal condition, retry policy), and version the canonical invoice contract because three filters depend on it. If a requirement appears that the ERP must send a correction back to the extraction step, that is a back-channel: re-cut the flow (start a new pipeline triggered by the correction) rather than add a reverse pipe.

## Review questions

1. Which step in your design would need to know the outcome of a later step? What does that imply?
2. Which filter has the longest description, and does it hold more than one role?
3. If the busiest filter needed ten times the throughput, what would you change, and what would that cost?
4. What happens to in-flight data if the consumer's store is unavailable for an hour?
5. Which pipe contract has the most receivers, and how are changes to it tested?
