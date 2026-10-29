# Cohesion and LCOM

## Contents
- What cohesion measures
- The cohesion scale (best to worst)
- Deciding where an operation belongs
- LCOM: structural cohesion metric
- Limits of LCOM
- Worked example
- Review questions

## What cohesion measures

Cohesion asks how strongly the parts of a module belong together. A fully cohesive module holds everything it needs; carving it up would only force the fragments to call each other to get anything done. Constantine's warning applies: dividing a cohesive unit raises coupling and lowers readability. So the goal is not "smaller modules" but "modules whose parts belong together".

## The cohesion scale (best to worst)

| Level | Parts are grouped because... | Smell to look for |
|---|---|---|
| Functional | every part contributes to one well-defined job, and nothing essential lives elsewhere | (ideal) |
| Sequential | one part's output feeds the next part's input | pipeline steps scattered across modules |
| Communicational | parts operate on the same data or jointly produce one output (save a record, then send a confirmation about it) | |
| Procedural | parts must run in a set order | "step 1, step 2" modules |
| Temporal | parts happen at the same time, e.g. the grab bag of unrelated startup initialization | `init`, `bootstrap`, `onStartup` dumping grounds |
| Logical | parts are conceptually similar but do different things (converters for text, streams, serialized objects) | `*Utils`, `*Helpers`, `Common` |
| Coincidental | parts share only a file | anything you cannot name without "and" or "misc" |

Use the scale as vocabulary in reviews ("this is temporal cohesion; move each initializer next to the thing it initializes").

## Deciding where an operation belongs

Cohesion is judged more than measured, so make the reasoning explicit. When a module contains operations that might belong elsewhere, ask:

1. **Size of the candidate new module.** If only one or two operations would move, a separate module may be too thin; keeping them is often fine.
2. **Growth trajectory.** If the current module is expected to keep growing, extract early along a natural seam before it becomes hard to split.
3. **Knowledge dependency.** If the moved operations need so much of the original module's data or logic that the split would create heavy coupling, keep them together.
4. **Rate and reason of change.** Operations that change for different business reasons or teams are candidates to separate.

Record the answer and the reason; the right structure depends on context, and this weighing is ordinary architecture trade-off work.

## LCOM: structural cohesion metric

Lack of Cohesion in Methods comes from the Chidamber and Kemerer OO metrics suite (which also includes complexity and coupling measures). It looks only at which methods touch which fields.

Intuition: count how much of the class's method set does not overlap through shared fields. If methods split into groups that never touch the same fields, the class is really several classes glued together, and LCOM is high.

Two common forms:
- **LCOM1 (CK original):** over all method pairs, P = pairs sharing no field, Q = pairs sharing at least one field. LCOM1 = P - Q when positive, otherwise 0. Sensitive to class size; compare only like with like.
- **LCOM96b (Henderson-Sellers):** with m methods, a fields, and mu(Aj) the number of methods using field j: LCOM96b = (1/a) * sum over j of (m - mu(Aj)) / m. Range 0 (every method uses every field) toward 1 (each field used by one method).

A useful companion, not in the chapter: count connected clusters of methods linked by shared fields. Each extra cluster is a concrete split candidate. The bundled script reports all three.

Where LCOM pays off:
- Assessing a code base you are new to.
- Preparing a migration or restructuring: shared utility classes are a classic obstacle when moving to a new architecture, and LCOM flags the ones that are only incidentally one class.
- Prioritizing refactoring of god classes.

## Limits of LCOM

- It sees structure only. It cannot tell whether methods belong together conceptually. A class of pure functions with no fields scores as perfectly cohesive or undefined, and a class whose methods share one logger field looks cohesive.
- This is the "why over how" principle in action: the metric tells you how code is wired, never why. Pair every LCOM finding with a domain judgment before acting.
- Thresholds are local. Baseline your own code base and watch trends rather than chasing an absolute number.

## Worked example (invented)

`InvoiceService` has fields `taxRules`, `ledger`, `smtpClient`, `pdfRenderer`.
- `computeTax`, `applyDiscount` use `taxRules`.
- `post`, `reverse` use `ledger` and `taxRules`.
- `emailInvoice`, `emailReminder` use `smtpClient` and `pdfRenderer`.

Clusters: {computeTax, applyDiscount, post, reverse} and {emailInvoice, emailReminder}. LCOM96b = average over fields of unused share: taxRules (6-4)/6, ledger (6-2)/6, smtpClient (6-2)/6, pdfRenderer (6-2)/6, giving (0.33+0.67+0.67+0.67)/4 = 0.58. Domain check: invoice delivery is a separate concern with a separate change cadence, so extract `InvoiceDelivery`. Had the second cluster been, say, audit logging of postings, the structural split would still exist, but the domain might argue to keep it (communicational cohesion).

## Review questions (original)

1. Name a module in your system with temporal or logical cohesion. What would functional cohesion look like for its contents?
2. When would you keep two operations in a module even though LCOM says they share no fields?
3. Why is extracting a two-method module often a poor trade?
