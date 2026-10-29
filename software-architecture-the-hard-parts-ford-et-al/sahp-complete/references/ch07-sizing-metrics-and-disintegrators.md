# Sizing Metrics and Granularity Disintegrators

## Contents
- Modularity versus granularity
- Measuring service size
- The two opposing forces
- Disintegrator 1: service scope and function
- Disintegrator 2: code volatility
- Disintegrator 3: scalability and throughput
- Disintegrator 4: fault tolerance
- The leftover-cohesion and naming test
- Disintegrator 5: security of access
- Disintegrator 6: extensibility
- Disintegrator checklist
- Pitfalls

## Modularity versus granularity

Keep the two words apart when advising:

- **Modularity** is the act of dividing a system into separate parts (covered in the book's Chapter 3 on architectural modularity).
- **Granularity** is about how big each of those parts should be.

The authors observe that most of the pain in distributed systems comes from getting size wrong rather than from the decision to modularize at all. When a team says "we have a modularity problem", probe whether the real issue is that services are too big or too small.

Size is defined by behavior (what a service does), not by how many classes or lines it contains. Two teams can implement identical behavior with very different line counts, so line and class counts are unreliable.

## Measuring service size

Use two semi-objective metrics and track them over time:

1. **Statement count.** Sum the executable statements across all source files of the service. A statement is one complete action, typically terminated by a semicolon (Java, C#, Go, JavaScript, C, C++) or a newline (Python, Ruby, F#). It reflects the amount of work the code performs and is less sensitive to formatting style than lines of code.
2. **Public operation count.** Count the externally exposed entry points (endpoints, operations, message handlers).

Both still carry some subjectivity, but they give a shared, numeric baseline for conversations that otherwise run on gut feeling. A sudden jump in either number signals scope creep worth reviewing.

## The two opposing forces

- **Disintegrators** answer: when is it justified to split a service into smaller parts?
- **Integrators** answer: when is it justified to merge services back together, or not split them in the first place?

The common failure is to evaluate only disintegrators, producing services that are each tidy but collectively slow, fragile and hard to keep consistent. The right size is the equilibrium point between the two sets of forces. A split usually rests on several disintegrators at once, though a single strong one can be enough.

The six disintegrators, each phrased as a diagnostic question:

| Driver | Diagnostic question |
|---|---|
| Scope and function | Does the service do several loosely related things? |
| Code volatility | Is change concentrated in one portion of the code? |
| Scalability and throughput | Do portions face very different load? |
| Fault tolerance | Can one portion crash and take critical functions with it? |
| Security | Does one portion need tighter access control than the rest? |
| Extensibility | Does the service keep growing new variants of the same context? |

## Disintegrator 1: service scope and function

This is the most frequently cited reason for splitting, especially in microservices. Evaluate two dimensions:

- **Cohesion:** how strongly the operations relate to each other and to one purpose.
- **Size:** statement count, public operation count, or both.

Decision guidance:

- If the operations share one narrow purpose (for example, a single "deliver an invoice" capability that can send by email, fax or portal upload), cohesion is already strong. Scope alone does not justify a split.
- If the operations merely share a broad noun (for example, an "Account" service that handles account settings, saved searches and product reviews), cohesion is weak and a split along those functions is likely warranted.

Why this driver is insufficient alone: it is an extension of the single-responsibility principle from class design to services, and "single purpose" is a matter of interpretation. Is "notify the customer" one responsibility, or is "notify by SMS" one? Cohesion metrics such as LCOM exist for classes but do not settle the question for services. Treat scope as a starting signal and confirm with the measurable drivers below.

## Disintegrator 2: code volatility

Volatility is how often the source code changes. Splitting along volatility lines is also called volatility-based decomposition.

How to apply:

1. Pull change frequency per module or package from version control history (commits or merged pull requests touching each area over the last several months).
2. Look for skew: one area changing every week while others change a few times a year.
3. If skew exists, isolating the hot area means each frequent change is tested and deployed alone. Benefits: smaller testing scope, lower deployment risk, and the stable functions stay available while the volatile part is redeployed.

Invented example: a document-rendering service generates PDFs, CSV exports and branded HTML statements. The HTML statement templates change twice a week for marketing campaigns; PDF and CSV change twice a year. Split into "Statement Rendering" (HTML) and "File Export" (PDF plus CSV). PDF and CSV stay together because they share a purpose and change rarely.

## Disintegrator 3: scalability and throughput

Measure the actual load on each portion of the service. If one function handles orders of magnitude more traffic than its neighbors, a combined deployment forces the low-traffic functions to scale with the high-traffic one.

Costs of keeping them together:

- Higher infrastructure cost, because every instance carries all functions.
- Worse elasticity, because larger deployment units take longer to start (mean time to start, MTTS, grows).

Invented example: a pricing service answers quote lookups at 80,000 per minute, recomputes bulk discounts at 200 per minute, and publishes nightly rate cards about once per hour. Separating quote lookup lets it scale out alone; the other two may still share a service if no other driver separates them.

Gather real numbers (peak and sustained requests per minute per operation group) before using this driver; guesses about load are a weak basis.

## Disintegrator 4: fault tolerance

Fault tolerance here means the rest of a domain keeps working when one function suffers a fatal failure, such as running out of memory and crashing the process. If one portion is unstable and shares a process with critical functions, a crash removes all of them.

Splitting the unstable portion out contains the blast radius. But check two things before accepting this driver:

- **Runtime coupling:** if the separated parts call each other synchronously to complete a request, the split buys nothing, since a request still fails when any participant fails. See the workflow integrator.
- **What remains:** see the next section.

## The leftover-cohesion and naming test

Whenever you carve out one offending function, look at what is left. If the remainder has no natural shared purpose, you have created a weakly cohesive service and violated the scope driver.

A practical test is naming. Try to give each resulting service a short, self-describing name:

- "Fax Delivery" plus "Remaining Delivery" is a bad sign.
- "Fax Delivery" plus "Non-Fax Delivery" is a bad sign.
- "Fax Delivery" plus "Email-and-Portal Delivery" is a bad sign.
- "Fax Delivery", "Email Delivery" and "Portal Delivery" are all clean names.

If you cannot name it, either split further until every piece is nameable, or reconsider the split. Also ask where the next new variant would go: if there is no obvious home, the boundary is wrong.

Contrast with the volatility case: when the stable leftovers share a meaningful purpose (for example, all electronic channels), a two-way split is fine. The same functions can legitimately end up in different groupings depending on which driver is in play.

## Disintegrator 5: security of access

A frequent mistake is to protect sensitive data only at rest (separate schemas, separate databases, segregated network zones) while leaving the code paths that read and write it bundled with ordinary functions.

If a service exposes both routine operations (update a mailing address) and sensitive ones (manage stored payment cards, change credentials), then anyone authorized to call the service for routine work is one step away from the sensitive operations, even when the endpoints differ. Moving the sensitive operations into their own service lets access be granted at the service level rather than request by request.

Use this driver for regulated data such as PCI cardholder data, credentials and PII. Note the counterweight discussed in the balancing reference: access control can sometimes be enforced through design (security libraries at the gateway and inside the service mesh) rather than through deployment boundaries.

## Disintegrator 6: extensibility

Extensibility is the ease of adding new functionality as a context grows. When a service holds many variants of the same concept (payment methods, carrier integrations, tax jurisdictions), every new variant forces retesting and redeploying all existing variants. Splitting per variant makes each addition a standalone build, test and deploy.

The authors' caution: apply this driver only when growth is known, planned or intrinsic to the domain.

- Payment methods, shipping carriers and marketplace connectors tend to keep multiplying, so per-variant services are often justified.
- Notification channels tend to stabilize, so splitting for future channels is speculative.

When growth is uncertain, do not use extensibility as the primary justification. Wait until a pattern of additions is observed or confirmed by the business, then split.

## Disintegrator checklist

For each candidate split, record evidence, not opinion:

- [ ] Scope: cohesion strong or weak? Statement and operation counts?
- [ ] Volatility: change frequency per area from version control.
- [ ] Throughput: measured peak load per operation group.
- [ ] Fault tolerance: incident history per area; are the areas runtime-independent?
- [ ] Security: which operations touch regulated data; who needs access to what?
- [ ] Extensibility: confirmed pipeline of new variants, or speculation?
- [ ] Leftover cohesion: can every resulting service be named cleanly?
- [ ] Integrators reviewed (transactions, workflow, shared code, data relationships)?

## Pitfalls

- Assuming "micro" means "as small as possible". Not every part of a system needs to be a fine-grained microservice.
- Arguing single responsibility without measurements.
- Splitting for fault tolerance when the parts depend on each other synchronously.
- Carving out one function and leaving an unnamed, incoherent remainder.
- Securing sensitive storage but not the operations that access it.
- Splitting for imagined future variants.
