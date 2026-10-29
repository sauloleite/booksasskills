# Topology, Filters and Pipes

## Contents
- Origins and mental model
- Topology in one picture
- Filter roles
- Compositional reuse
- Pipes
- Data topologies
- Deployment and cloud options
- Design checklist
- Glossary

## Origins and mental model

Pipes and filters is one of the oldest styles: it appears as soon as functionality is split into separate steps. Familiar instances are Unix shell pipelines, collection operations in functional languages (map, filter, reduce chains) and MapReduce-style processing tools. Do not assume it is only for low-level tooling; the same shape serves business workflows (order intake, document conversion, data enrichment).

## Topology in one picture

Two component types only:
- **Filters** hold all behavior; each performs one business task.
- **Pipes** move data forward to the next filter or filters.

The canonical shape is one deployment unit in which filters are chained by unidirectional pipes. A filter may fan out to more than one successor (a tester choosing a branch), but data never flows backward.

```
[producer] -> [tester] --yes--> [transformer] -> [consumer]
                  \--no---> [tester] -> [transformer] -> [consumer]
                                  \--no--> (flow ends)
```

## Filter roles

Filters are self-contained, independent of each other, generally stateless, and do one thing. A filter is an architecture component even if it is implemented as a single class; complex ones span several classes and need a clearly identified entry point.

| Role | Direction | Typical job | Functional analogue | Smell that it is misassigned |
|---|---|---|---|---|
| Producer (source) | Outbound only | Accept a UI action or external request, subscribe to a stream, read a file | Generator | It also validates or reshapes data |
| Transformer | In and out | Enrich, convert format, calculate, normalize | map | It decides whether data continues |
| Tester | In, optional out | Validate, qualify, route, drop | filter / predicate (the authors liken it to reduce) | It modifies the payload |
| Consumer (sink) | Inbound only | Persist results, render a report or screen | Terminal operation | It forwards data onward |

Rules of thumb:
- If a description of a filter needs "and", split it.
- Testers are the only place conditional continuation lives. An example business guard: stop the flow when an order total is below a minimum threshold.
- Keep state out of filters; if a step needs reference data, read it from a store rather than remembering it between messages.

## Compositional reuse

Because filters are tiny and pipes go one way, new behavior often comes from recombining existing filters rather than writing new code. The well-known illustration: a word-frequency task that took a celebrated computer scientist pages of custom Pascal and a new algorithm was matched by a six-stage shell pipeline (split words, lowercase, sort, count duplicates, sort by count, take the top n). The lesson for an architect: invest in small, general filters with clean contracts, and reuse emerges, often in ways the original designers never anticipated.

## Pipes

- One-way, typically point-to-point (one source, one destination).
- Any payload format is allowed; prefer small payloads so the chain stays fast.
- Synchronous or asynchronous in either deployment model:
  - Monolithic: in-process calls, or asynchrony via threads or an embedded message channel.
  - Distributed: a one-way remote call over REST, messaging, streaming or a similar protocol.
- Each pipe defines a contract (fields and possibly types). Treat it like a public API.

Pipe specification template:

```
pipe: duration-qualified -> duration-calculator
direction: one-way
mode: async (in-process queue)
payload: {service_id: str, request_ms: int, ts: iso8601}
contract owner: telemetry team
change policy: additive only; breaking change needs consumer tests green
```

## Data topologies

Database topology is not dictated by the style. Options range from one shared database (most common, matching the monolithic deployment) to a database per filter. A useful mixed pattern, modeled on a continuous fitness function that tracks an operational characteristic in production:

1. A producer loads samples from its own raw-data store.
2. A transformer reads analysis settings (such as the time window) from a separate configuration store and narrows the series.
3. A transformer computes trends and writes them to its own analytics store.
4. A consumer renders a chart or report.

Choose per filter: does it need its own store for isolation, scale or ownership, or is a shared schema simpler? Default to shared unless a reason exists.

## Deployment and cloud options

Cloud suitability comes from high modularity and clearly separated filter types. Options, from simplest:

1. **Single service** containing all filters (the default for most pipelines, which are rarely large).
2. **Containerized filters** or groups of filters as separate services.
3. **Serverless functions**, one per filter.
4. **Managed workflow orchestration**, for example AWS Step Functions with each filter as its own Lambda task chained in order. Both of its workflow types fit: Standard (each step runs exactly once) and Express (a step may run more than once, so make filters idempotent).

Whenever filters are distributed, the pipes become remote calls and the trade-offs in the fit reference apply (better scalability and fault tolerance, worse cost and simplicity).

Original sketch of a generic, orchestrator-neutral pipeline definition:

```yaml
pipeline: scalability-trend
steps:
  - name: capture_raw      # producer
    next: select_window
  - name: select_window    # transformer
    next: analyze_trend
  - name: analyze_trend    # transformer
    next: render_report
  - name: render_report    # consumer
    end: true
```

## Design checklist

- [ ] Every step named and assigned exactly one role.
- [ ] Producers only at the start, consumers only at the ends.
- [ ] All branching done by testers; transformers never drop data.
- [ ] No pipe goes backward; no filter waits on a reply from downstream.
- [ ] Payloads small; contracts written down with an owner.
- [ ] Sync/async choice per pipe justified.
- [ ] Data store per filter decided (shared by default).
- [ ] Deployment option chosen; if Express-style at-least-once execution, filters idempotent.

## Glossary

- **Filter entry point**: the one class that represents a multi-class filter to the rest of the system and carries its role metadata.
- **Compositional reuse**: building new behavior by rearranging existing filters.
- **Point-to-point pipe**: a channel with exactly one sender and one receiver.
