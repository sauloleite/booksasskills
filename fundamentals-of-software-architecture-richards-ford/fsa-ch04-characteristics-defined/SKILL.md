---
name: fsa-ch04-characteristics-defined
description: Defines what counts as an architecture characteristic, how to tell it apart from domain requirements and ordinary design hygiene, how to categorize and name characteristics (operational, structural, cloud, cross-cutting, ISO families), and why to keep the set small and accept least-worst trade-offs. Based on Chapter 4 of Richards and Ford's "Fundamentals of Software Architecture" (2nd ed.). Use when sorting a requirements list into domain vs. capabilities, deciding whether a concern needs structural support, building a shared glossary of "-ilities", or pruning an overlong list of quality goals.
---

# Architecture Characteristics Defined (FSA Chapter 4)

Purpose: help an agent decide which system capabilities deserve architect-level attention. Structural design has two halves: understanding the problem domain (behavior) and identifying architecture characteristics (capabilities the system needs to succeed). This skill covers the second half: a three-part test for what qualifies, a working vocabulary grouped by category, the ambiguity problem and its fix (an organizational glossary), and the trade-off mindset that keeps the list short. It feeds later work such as characteristic identification from domain concerns, fitness functions, and style selection.

## Key decision rules (apply without opening references)

1. **Three-part qualification test.** A concern is an architecture characteristic only if it (a) is not a domain behavior, (b) affects the structure of the design, and (c) is critical or important to success. Fail any one and it is a design detail, a domain requirement, or noise.
2. **Design vs. structure.** Ask: can good coding practice satisfy this, or does it need its own structural support (separate deployable, isolated service, distribution, redundancy)? Only the second case makes it architectural. The same concern can land on either side depending on context (security in a monolith via hygiene vs. a hardened, isolated service in a distributed system).
3. **Some characteristics force structure.** Scalability past a monolith's ceiling cannot be designed in; it requires a distributed style. Watch operational characteristics most closely, since they most often demand structural support.
4. **Fewest, not most.** Every supported characteristic costs design effort, implementation and maintenance effort, and possibly structure. Prefer the smallest set that secures success. A design that tries to honor everything becomes a generic, unwieldy solution that rarely works.
5. **Hunt for implicit characteristics.** Requirements documents list explicit ones. Availability, reliability, security, and domain-specific norms (low latency in trading) are usually unstated; uncover them from domain knowledge.
6. **Characteristics interact.** Improving one usually degrades another (security adds encryption and indirection that cost performance). Treat selection as balancing coupled controls, never as independent maximization.
7. **Least worst, not best.** A perfect architecture does not exist; target the option whose weaknesses hurt least for this context. Record what was sacrificed and why.
8. **Define terms locally.** No universal standard exists; terms overlap (availability vs. reliability) or carry multiple meanings (learnability). Build an organizational ubiquitous language with objective definitions before debating priorities.
9. **Keep domain function out of the list.** Functional correctness and completeness are why the software exists, not architecture characteristics; do not let them crowd the capability list.
10. **Favor changeability.** The easier the architecture is to change, the less pressure to get every characteristic right the first time. Iterate.

## Default workflow

1. Collect candidate concerns from requirements, stakeholders, and domain norms. Tag each as explicit (written) or implicit (inferred).
2. Separate domain behavior from capabilities. Push functional items back to domain design.
3. Run the three-part test on each capability. For criterion (b), state concretely what structure it would require; if none, downgrade to a coding or design standard.
4. Normalize names against the team glossary; split ambiguous terms (for example, "learnability" for users vs. self-tuning systems) and merge synonyms.
5. Categorize (operational, structural, cloud, cross-cutting) to check for blind spots, especially implicit operational and legal concerns.
6. Map pairwise tensions among the survivors; trim to the few that matter most.
7. Write down the chosen set, the rejected candidates, the main trade-offs accepted, and how the design keeps future change cheap.

## References

- [references/qualifying-characteristics.md](references/qualifying-characteristics.md): read when deciding whether a specific concern is an architecture characteristic, explaining implicit vs. explicit, or arguing about terminology (non-functional requirements, quality attributes).
- [references/characteristics-catalog.md](references/characteristics-catalog.md): read when you need definitions and examples per category (operational, structural, cloud, cross-cutting), the ISO-style families, ambiguous term pairs, or guidance on building a glossary.
- [references/trade-offs-least-worst.md](references/trade-offs-least-worst.md): read when pruning a list, explaining why characteristics cannot all be maximized, framing a least-worst decision, or reviewing an analysis with self-check questions.
- [references/source-map.md](references/source-map.md): read to locate which reference covers a given chapter section.

## Scripts

None. The chapter offers definitions and judgment criteria, not calculations, so no script is provided.
