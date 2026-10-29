# Stamp Coupling: Over-Coupling, Bandwidth and Workflow State

## Contents
- What stamp coupling is
- When it is legitimate: industry documents
- Accidental stamp coupling (over-coupling)
- Bandwidth: the cost model
- Stamp coupling for workflow management
- Strengths and weaknesses
- Diagnostic checklist
- Pitfalls

## What stamp coupling is

A service passes a large data structure to others, and each recipient reads or writes only a small part of it. It can be a deliberate pattern or an accident, and you must decide which you have.

## When it is legitimate: industry documents

Some industries standardize a large interchange document (often XML). Travel itinerary standards are the classic case: many systems pass the whole document along and each updates only its own section. Here the shared structure is an external standard, so carrying it whole is reasonable.

## Accidental stamp coupling (over-coupling)

The common accident: a contract specifies a provider's whole structure when the consumer needs a fragment, often as misguided future-proofing. Invented example: a `ShippingLabel` service needs only `recipientName` and `postalCode` from `Customer`, but is bound to the full strict `Customer` contract. When the CRM team renames `loyaltyTier`, the label service fails validation and two teams must coordinate a release over a field the label service never reads.

Effects:
- Brittleness and unnecessary breaking changes.
- Release coordination across teams with no shared business reason.
- Wasted network capacity (see below).

It is easy to slide into this when the team also uses stamp coupling intentionally elsewhere (for workflow state), because the pattern starts to feel normal.

## Bandwidth: the cost model

Assuming bandwidth is infinite is one of the Fallacies of Distributed Computing. Inside a monolith, call payload size rarely matters; in distributed systems, the natural limits disappear and payloads cross the network on every call.

Per-edge bandwidth = requests per second x payload size.

Invented calculation: a pricing service is called 1,500 times per second and returns a 300 KB product document, of which the caller uses a 150-byte price block.
- Full payload: 1,500 x 300 KB = 450,000 KB/s, about 450 MB/s on one edge.
- Need-to-know payload: 1,500 x 150 B = 225,000 B/s, about 225 KB/s.
- Waste: roughly 2,000 times more traffic than necessary.

Always run this arithmetic for high-rate edges; `scripts/contract_usage.py` automates it per consumer when field sizes are supplied.

## Stamp coupling for workflow management

Mediated (orchestrated) coordination is usually the better default for complex workflows. But sometimes scale or throughput requirements push toward choreography even though the workflow is complex. Without an orchestrator, workflow state must live somewhere, and the contract itself can carry it.

How it works:
1. Design the message to hold both domain data and workflow data: overall status, per-step state, transactional state, error details.
2. Each service receiving the message updates its own section and the workflow state, then forwards it.
3. The final receiver (or any interested party) inspects the message to learn whether the workflow succeeded, and why it failed if not.
4. If the workflow needs atomic-style consistency, a failing service sends the contract back to services already visited so they can apply compensating updates.

Sketch of such a carrier (illustrative):

```json
{
  "workflowId": "wf-7781",
  "status": "IN_PROGRESS",
  "steps": {
    "reserveStock": {"state": "DONE", "reservationId": "r-55"},
    "chargeCard":   {"state": "FAILED", "error": "card_declined"},
    "shipOrder":    {"state": "PENDING"}
  },
  "order": {"orderId": "o-901", "sku": "A12", "qty": 2}
}
```

Coupling consequence: every participant now depends on the shape of the whole carrier, so coupling is higher than nominal. That is accepted because the semantic coupling of a complex workflow has to live somewhere: implementation cannot remove it, only relocate it (into an orchestrator or into the message). Choreography in exchange often improves throughput and scalability, which can make this a good trade.

## Strengths and weaknesses

Strengths:
- Enables complex workflows under choreography, keeping its scalability benefits without a central mediator.
- Workflow outcome and error information travels with the work, so no separate state store is needed.

Weaknesses:
- Higher, sometimes artificial, coupling among all collaborators.
- Payload grows with each step, creating bandwidth pressure at high request rates.
- Compensation by re-broadcast adds message traffic and complexity.

## Diagnostic checklist

- For each consumer, what fraction of received fields does it actually read or write?
- Is the large structure an external standard, a deliberate workflow carrier, or accidental?
- What is requests/s x payload size on the busiest edges, and how does it compare to the needed subset?
- Has any consumer broken because of a change to a field it ignores? That is the signature of over-coupling.
- If it is a workflow carrier, is the choice of choreography justified by measured throughput or scale needs?

## Pitfalls

- "Just send the whole object" defaults in serializers and ORMs.
- Using a workflow carrier pattern for simple request/response edges.
- Forgetting payload growth as steps append data.
- Strict schema plus full structure: the worst combination for brittleness.
