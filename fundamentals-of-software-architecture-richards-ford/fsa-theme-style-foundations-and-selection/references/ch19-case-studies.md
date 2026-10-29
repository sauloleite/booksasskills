# Worked Case Studies

## Contents
- Case A: small customizable system (monolith options)
- Case B: high-scale live auction (distributed option)
- Invented practice example
- Patterns to reuse

## Case A: small customizable system (monolith options)

Context (the book's sandwich-shop kata): a simple ordering application with a modest budget. Characteristics analysis found a single quantum sufficed, so a monolith's simplicity was attractive. Customizability was one of the required characteristics. Two earlier component designs existed, one partitioned by domain and one by technical layer, and the chapter turns them into two candidate architectures.

### Option A1: modular monolith
- Domain-aligned components, one relational database, deployed as one unit.
- A single responsive web UI (carefully designed for mobile) keeps costs low.
- If time allows, partition tables and other database assets along the same domain lines as the components. This is cheap insurance for a later move to a distributed style.
- Customization is not something this style gives you, so it must be designed into the domain: add a dedicated override component with an endpoint where customizations are uploaded, and make every domain component consult it for each customizable behavior.
- Governance: that "every component consults the override component" rule is a natural fitness function. A sketch:

```python
# Fitness function sketch: every domain module must import the override API.
import ast, pathlib, sys

def missing_override(src_root: str, override_mod: str = "override") -> list[str]:
    bad = []
    for path in pathlib.Path(src_root).glob("domains/*/*.py"):
        tree = ast.parse(path.read_text())
        mods = {n.module for n in ast.walk(tree)
                if isinstance(n, ast.ImportFrom) and n.module}
        if not any(m.split(".")[0] == override_mod for m in mods):
            bad.append(str(path))
    return bad

if __name__ == "__main__":
    offenders = missing_override(sys.argv[1])
    sys.exit(1 if offenders else 0)
```

### Option A2: microkernel
- Chosen because the problem's shape (common core plus variations) mirrors the microkernel's shape.
- Core: the domain components plus one relational database. Keeping domain and data design in step again eases a future distributed migration of the core.
- Customizations live in plug-ins: one shared set of common plug-ins with its own store, plus local plug-ins each owning its own data. Plug-ins do not depend on each other, so each can keep private data and stay decoupled.
- Backends for Frontends (BFF): the API layer acts as a thin microkernel adapter. The backend returns generic data; one adapter per client type (e.g. a native iOS app) reshapes format, page sizes, latency handling and similar details for that client. Benefits: richest per-device UI and an easy path to support new devices later.

### Communication
Synchronous throughout for both options: no extreme performance or elasticity demands and no long-running operations.

### Takeaway
When one quantum suffices, choose between monolith flavors by shape fit. If customization is central, a microkernel models it structurally; a modular monolith can still work if customization is engineered into the domain and protected by a fitness function.

## Case B: high-scale live auction (distributed option)

Context (the book's online auction kata): live auctions with bidders online and an auctioneer on site, with ambitious scale, elasticity and performance requirements, and fine-grained customization needs. Component analysis showed that roles differ in characteristics (bidder vs auctioneer availability and scale), so more than one quantum is needed.

### Style choice
- Distributed candidates that fit most characteristics: low-level event-driven and microservices.
- Microservices wins because it handles differing operational characteristics per part better; event-driven partitioning follows communication style rather than characteristics.
- Weakness: performance targets are hard in microservices, typically degraded by excessive orchestration or overly aggressive data separation. Response: design around the weakness instead of discarding the style.

### Topology
Each identified component becomes a service (component granularity equals service granularity). Three user-facing interfaces: many bidders, one auctioneer per auction, and a read-only streamer to bidders (read-only allows optimizations that writes would block).

| Service | Role | Notable decision |
|---|---|---|
| Bid Capture | Accepts online bids | No persistence (pure conduit); sends to tracker asynchronously |
| Bid Streamer | Pushes bids to online participants | Fast, read-only stream |
| Bid Tracker | Merges online and auctioneer bids, orders them near real time | Both inputs async; queues buffer very different arrival rates |
| Auctioneer Capture | Accepts auctioneer's bids | Split from Bid Capture because characteristics differ |
| Auction Session | Runs each auction's workflow | Hands off to payment when an auction ends |
| Payment | External payment provider | Downstream of session completion |
| Video Capture | Captures the live video | |
| Video Streamer | Sends video to online bidders | |

### Communication reasoning
Both styles are used deliberately. Async exists mainly because characteristics vary across services. Example: if payment can only process one transaction per half second and many auctions close together, sync calls would produce timeouts and reliability failures; a queue in front of payment protects a critical but fragile link.

### Quanta
Five quanta resulted, roughly: Payment, Auctioneer, Bidder, Bidder Streams, Bid Tracker. Several run multiple instances. Doing quantum analysis while designing components made service, data and communication boundaries easier to find.

### Takeaway
The design is neither the only nor provably the best one; it has the least-bad trade-off set. A generic style (microservices), combined with careful use of events and messaging, gets the most from the pattern while leaving room to grow.

## Invented practice example

A clinic-scheduling product for 40 small clinics, each wanting its own reminder rules and billing quirks; peak load is modest and uniform; the team deploys monthly with partial test automation.
- One set of characteristics, one quantum: monolith.
- Shape: shared core plus per-clinic variation: microkernel, with clinic rules as plug-ins.
- Data: one database for the core; plug-ins with private stores only where needed.
- Communication: all sync.
- Team maturity argues against microservices regardless.
- Outputs: ADR on microkernel vs modular monolith; fitness function ensuring plug-ins never call each other.

## Patterns to reuse

- Let quantum count decide monolith vs distributed.
- Let problem shape pick among styles of the same family.
- Split services when their characteristics differ, even if their functions look similar.
- Put queues where throughput or fragility mismatches exist; keep everything else sync.
- Encode structural rules as fitness functions.
- Leave a migration seam (domain-aligned data) in monoliths.
