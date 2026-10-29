# Core and Plug-in Design

## Contents
- Defining the core
- Shaping the core internally
- Presentation options
- Plug-in components: rules and packaging
- Binding modes: compile, runtime, remote
- Registry design
- Contracts and adapters
- Data topology
- Design checklist

## Defining the core

Two complementary ways to draw the core boundary:

- **Minimal functionality**: the smallest thing that still runs. An IDE whose core is a bare text editor is the classic case; nearly all value arrives through plug-ins.
- **Happy path**: the general flow that applies to every case with little or no customization. Everything conditional on who, where or what is pushed out.

Practical heuristic: find the code with the highest branching (cyclomatic complexity) keyed on a variation dimension (device model, state, client, payment type). Each branch becomes a plug-in; the core keeps only "look up the right plug-in, call it, handle the result". This improves extensibility (new variant = new plug-in plus a registry entry), maintainability and testability (each variant tested in isolation).

Illustration (original, Python):

```python
# Before: the core knows every variant
def price_shipment(country, parcel):
    if country == "BR": ...
    elif country == "DE": ...
    elif country == "JP": ...

# After: the core only dispatches
def price_shipment(country, parcel):
    plugin = registry.resolve("pricing", country)
    return plugin.price(parcel)
```

## Shaping the core internally

The core can itself use another structure, chosen by size and complexity:
- a layered architecture (small to mid cores),
- a modular monolith (core partitioned by domain modules),
- separately deployed domain services, each hosting the plug-ins of its own domain (for example a payment service whose plug-ins are card, wallet, store credit, gift card, purchase order).

The last option moves toward a distributed system; apply the same trade-off scrutiny as for remote plug-ins.

## Presentation options

The UI may live inside the core, or sit apart as a separate front end that calls core services. A separate UI can itself be built as a microkernel (a shell plus UI plug-ins), which is useful when screens vary by customer.

## Plug-in components: rules and packaging

Plug-ins hold specialized processing, optional features and custom code, and they quarantine the most volatile code. Rules:
- self-contained, no dependencies on other plug-ins;
- a single entry point the core calls;
- no knowledge of other plug-ins or of the core's database.

Packaging choices for in-process plug-ins:
- **Shared library** per plug-in (JAR, DLL, Gem, wheel). Name the artifact after the variant it serves so it is easy to locate. Gives physical separation and independent versioning.
- **Namespace or package** within one code base. Simpler. Use a naming scheme that marks the component as a plug-in and groups it, such as `app.plugin.<domain>.<context>` (for example `app.plugin.pricing.brazil`). The `plugin` segment signals that isolation rules apply; the domain segment groups plug-ins sharing a contract; the context segment identifies the specific variant for maintenance and testing.

## Binding modes: compile, runtime, remote

| Mode | How it connects | Gains | Costs |
|---|---|---|---|
| Compile-based, in-process | direct call to entry class | simplest to build and manage | any plug-in change redeploys the whole app |
| Runtime, in-process | plug-in framework (OSGi, Jigsaw-style modules, Prism for .NET) loads/unloads | add/remove without redeploying core or others | framework complexity, lifecycle management |
| Remote | REST or messaging to a plug-in service, possibly containerized | stronger decoupling, plug-in scalability and throughput, runtime change without a framework, asynchronous flows | becomes distributed; hard for on-prem third-party products; more cost and deployment complexity; synchronous calls fail if the plug-in is down |

Asynchronous remote example (invented): a document-intake core enqueues "classify this upload" to a classifier plug-in and returns immediately; when the plug-in finishes it publishes a completion event, and the core notifies the user. Responsiveness improves, but you now own queues, retries and eventual consistency.

Whatever the binding, the system is still one quantum because the core is in every request path. Remote plug-ins scale the plug-ins, not the core.

## Registry design

The core must know what plug-ins exist and how to reach them. A registry entry typically records:
- plug-in name or key (the variation value it serves);
- data contract (input and output shapes) and its format (JSON, XML, objects);
- access details: class or module name for in-process, queue name for messaging, URL for REST.

Implementation range: from an in-core dictionary keyed by variant, to an embedded discovery component, to an external service registry (ZooKeeper, Consul). Start with the simplest that satisfies your binding mode. Original sketch:

```python
REGISTRY = {
    ("pricing", "BR"): {"kind": "inproc", "target": "app.plugin.pricing.brazil:Plugin"},
    ("pricing", "DE"): {"kind": "queue",  "target": "pricing.de.requests"},
    ("pricing", "JP"): {"kind": "http",   "target": "https://plugins.internal/pricing/jp"},
}
```

## Contracts and adapters

- One standard contract per plug-in domain, covering behavior (operations such as execute, register, deregister), input data and output data.
- When plug-ins come from third parties with contracts you do not control, put an adapter between their contract and your standard one. The core then has no per-plug-in special code.
- Decide what the core must understand in the output. Fields the core only shows or stores (for example a preformatted report) stay opaque to it; fields it acts on (a yes/no decision, a computed amount) must be typed and documented.

## Data topology

- Usual shape: monolithic deployment, one database (often relational).
- The core reads and writes the shared database and hands plug-ins the data they need. Plug-ins do not query it directly, so schema changes touch only the core.
- A plug-in may own a private store (its own small database or rules engine with variant-specific rules). It can be external or embedded/in-memory inside the plug-in or the deployment. No other component accesses it.

## Design checklist

- [ ] Core boundary justified as minimal functionality or happy path
- [ ] Every high-branching variation point mapped to a plug-in domain
- [ ] No plug-in imports another plug-in
- [ ] Standard contract per domain; adapters for third-party plug-ins
- [ ] Binding mode chosen and recorded with its trade-offs
- [ ] Registry entries include key, contract, access details
- [ ] Plug-ins do not touch the shared database
- [ ] Remote plug-ins have timeout, fallback and async options considered
