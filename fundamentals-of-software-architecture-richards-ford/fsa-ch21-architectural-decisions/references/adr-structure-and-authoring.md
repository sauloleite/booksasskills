# ADR Structure and Authoring

## Contents
- What an ADR is, and tooling
- The seven-section template (five standard plus two recommended)
- Section-by-section authoring rules
- Status lifecycle, supersession and the RFC status
- Approval criteria: who may accept a decision
- Worked example (invented)
- Authoring checklist

## What an ADR is

An Architectural Decision Record is a short text document, typically one or two pages, capturing a single architectural decision. Michael Nygard popularized the format in 2011 and Thoughtworks Technology Radar recommended adoption in 2017. Markdown or AsciiDoc is usual; a wiki template also works. Nat Pryce's open source **ADR Tools** offers a command line for numbering, file locations and supersession links.

## Template

Standard sections: **Title, Status, Context, Decision, Consequences**.
Recommended additions: **Compliance** and **Notes**.
Optional extension: **Alternatives**, when each rejected option needs detailed analysis.

You may add other sections, but keep one template across the organization and keep it brief.

## Section rules

### Title
- Sequential number plus a short phrase that removes ambiguity about scope and subject.
- Shape: `<number>. <What> Between/For <Where>`, for example "17. Event Streaming for Inventory Updates to Storefront".

### Status
Allowed values: **Proposed**, **Accepted**, **Superseded** (plus the optional RFC status below).
- *Proposed*: awaits approval from a higher authority (lead architect, architecture review board).
- *Accepted*: approved and ready to implement.
- *Superseded*: replaced by a later ADR. Only an Accepted ADR can be superseded; a Proposed one is simply edited until it is Accepted.
- Link both directions: the old record says "Superseded by N", the new one says "Accepted, supersedes M". This trail preserves what was decided, why, what replaced it and why, and pre-empts "did anyone consider the old approach?" questions.

**RFC status.** To validate assumptions with a wider audience, publish a draft with status "Request for Comments" and a firm review deadline. After the deadline, analyze feedback, adjust, then move to Proposed (or Accepted if you hold approval authority). This is also a low-friction way to involve developers.

### Approval criteria (discovered through the Status field)
Having to set a status forces a conversation with your manager or lead architect: which decisions can you accept yourself, and which need escalation? Start with three criteria:
1. **Cost**: licensing or purchase fees, extra hardware, and implementation effort. Estimate effort as `estimated hours x standard FTE hourly rate` (the project manager or owner usually knows the rate). Agree a threshold above which the ADR must be Proposed and approved by someone else.
2. **Cross-team impact**: affects other teams or systems, so escalate.
3. **Security**: any security implication, so escalate.
Write the agreed rules down (for instance, "anything over $X goes to the review board") so every architect knows their approval limits.

### Context
- Answers "what forces make this decision necessary?"
- Describe the situation and briefly name the options. If options need deep analysis, put it in an Alternatives section instead.
- Because it describes a slice of the system, the Context doubles as architecture documentation.
- Good context is two sentences: the scenario plus the candidate options.

### Decision
- State the decision in an affirmative, commanding voice ("We will..."), not as an opinion ("I believe X might be best"). Hedged phrasing leaves readers unsure a decision was taken.
- Include the full justification. Knowing *why* matters more than knowing *how*; it is what lets future maintainers avoid undoing a decision whose purpose they cannot see.
- Name what was traded away. A future architect who sees "chosen to cut latency, accepting tighter coupling" will not swap it out for consistency's sake without weighing latency.

### Consequences
- Record every significant impact, positive and negative, and use it to check whether the downsides outweigh the gains.
- Record the trade-off analysis and who agreed to it. This is what settles later objections: when a developer raises a risk that was already weighed with stakeholders, the Consequences section shows it was considered and accepted.

### Compliance (recommended)
- State how conformance will be measured and governed: manual review, or an automated fitness function.
- If automated, say how the check will be written and what code changes it needs (for example, a marker annotation or attribute on the classes the rule targets, created through new backlog stories).
- Tools: ArchUnit (Java), NetArchTest (.NET), or equivalents in other ecosystems.

Original illustration of a layering rule as a fitness function (Python, stdlib only):

```python
import ast, pathlib

def forbidden_imports(root, layer_pkg, banned_prefix):
    """Report modules in layer_pkg that import from banned_prefix."""
    hits = []
    for path in pathlib.Path(root, layer_pkg).rglob("*.py"):
        tree = ast.parse(path.read_text())
        for node in ast.walk(tree):
            names = []
            if isinstance(node, ast.Import):
                names = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                names = [node.module]
            hits += [(str(path), n) for n in names if n.startswith(banned_prefix)]
    return hits

assert not forbidden_imports("src", "presentation", "persistence"), "layer violation"
```

### Notes (recommended)
Metadata: original author, approval date, approver(s), superseded date, last modified date, modified by, and what the last modification was. Keep it even when ADRs live in Git; version control history does not capture approvals or supersession dates cleanly.

## Worked example (invented)

The chapter's own example is an auction system where one service fans bids out to two consumers with different needs and the ADR picks dedicated queues over a shared topic. Below is a different decision in the same spirit.

```
ADR 23. Dedicated Queues for Shipment Label and Customer Notification Consumers
STATUS: Accepted
CONTEXT: When an order is packed, the Fulfillment service must inform the
Label service and the Notification service. Options: one pub/sub topic,
one point-to-point queue per consumer, or synchronous REST calls.
DECISION: We will publish to a dedicated queue per consumer.
 - Fulfillment needs no reply, so the flow is one-way.
 - Label printing must process orders strictly in packing order; a FIFO
   queue gives this without consumer-side sequencing logic.
 - Notification calls a slow third-party SMS API and needs its own
   backpressure point so it never delays labels.
CONSEQUENCES: Queues must be clustered for availability. Fulfillment now
writes the same event twice. Adding a third consumer requires a code change.
COMPLIANCE: Automated test fails the build if Fulfillment references a topic
or an HTTP client for these flows; quarterly manual review of broker config.
NOTES: Author: R. Okafor. Approved: ARB, 2026-03-02. Last updated 2026-03-02.
```

Lessons the example encodes: the context lists real alternatives; each decision bullet ties to a concrete requirement (direction, ordering, backpressure); consequences admit costs; compliance is specific and checkable; any later review outcome is appended as a dated update rather than silently rewriting history.

## Authoring checklist

- [ ] Numbered, unambiguous title
- [ ] Valid status; supersession links in both records; RFC has a deadline
- [ ] Approval route matches the agreed cost, cross-team and security criteria
- [ ] Context names the forces and at least two options
- [ ] Decision uses "We will..." and gives technical and business reasons
- [ ] Consequences list negatives and the trade-off accepted, with who agreed
- [ ] Compliance says manual or automated, and how
- [ ] Notes carry author, approver, dates
- [ ] One to two pages; one decision per record
