---
name: fsa-ch21-architectural-decisions
description: Applies Chapter 21 of Richards and Ford's "Fundamentals of Software Architecture" (2nd ed.) on making, justifying, recording and communicating architectural decisions. Covers the Covering Your Assets, Groundhog Day and Email-Driven Architecture antipatterns, the last responsible moment, architectural significance, and Architectural Decision Records (sections, status and RFC, approval criteria, compliance, storage, standards, legacy systems, AI use). Use when deciding whether or when to decide, writing or reviewing an ADR, setting approval rules, or asking an LLM for architecture advice.
---

# Architectural Decisions (FSA Chapter 21)

## Purpose

This skill helps an agent support an architect through the full life of an architectural decision: deciding at the right time, justifying it in technical and business terms, recording it once as an Architectural Decision Record (ADR), routing it for approval, governing it afterwards, and telling only the people it affects. The chapter's core claim is that rationale (the *why*) is the most valuable architecture documentation, and that most decision failures come from missing timing, missing justification, or missing communication rather than from wrong technical choices.

## Key decision rules (apply even without opening references)

1. **Diagnose the antipattern stage.** Avoiding decisions out of fear (Covering Your Assets) leads, once fixed, to endless re-debate from weak justification (Groundhog Day), then to lost or unseen decisions (Email-Driven Architecture). Fix the earliest stage present.
2. **Decide at the last responsible moment:** when the rising cost of waiting outweighs the shrinking risk that more analysis would remove. Do not slide into Analysis Paralysis.
3. **Stay close to implementing teams** so infeasible decisions surface and get revised fast.
4. **Every decision needs a business justification** besides the technical one: cost, time to market, user satisfaction, or strategic positioning, matched to what stakeholders care about now. No business value means reconsider the decision.
5. **One system of record.** Never paste the decision into email or chat; send the context plus a link. Notify someone directly only if the decision directly affects them.
6. **Technology choices can be architectural.** A decision is architecturally significant (Nygard) if it touches structure, dependencies, interfaces, construction techniques, or the non-functional characteristics that matter for this system.
7. **ADR template:** Title (numbered), Status, Context, Decision, Consequences, plus recommended Compliance and Notes; add Alternatives when options need detailed analysis. Keep it to one or two pages, one decision per record, one consistent template.
8. **Status:** Proposed, Accepted, or Superseded (optionally RFC with a deadline). Only Accepted ADRs get superseded; link old and new in both directions.
9. **Agree approval limits up front** on cost (hours x FTE rate + fees + hardware vs a threshold), cross-team impact, and security; any of these sends the ADR to Proposed for higher approval.
10. **Decision text:** affirmative "We will..." voice, full rationale, explicit trade-off accepted. **Consequences:** both good and bad impacts plus the trade-off analysis and who agreed. **Compliance:** manual or automated fitness function, and how.
11. **Store ADRs where everyone can read them**, organized by scope (application/common, application/<app>, integration, enterprise). In larger organizations avoid keeping them only in an app's code repository.
12. **Use ADRs for standards** (no justification, no standard) and **retrofit them onto existing systems** to test whether past decisions still hold.
13. **LLMs list trade-offs; humans decide.** Do not return a context-free "best practice" for a structural question. Translate business drivers into characteristics, then weigh trade-offs in that context.

## Default workflow

1. Check significance (rule 6). If not significant, leave it to the team.
2. Check timing: what would one more iteration of analysis resolve, and what would it cost?
3. Write the Context: the forces plus at least two options.
4. Elicit the dominant business driver; map it to architecture characteristics; compare options on those characteristics.
5. Draft the ADR (rules 7 to 10) and choose a governance method for Compliance.
6. Route approval (rule 9); use RFC status with a deadline when broader validation helps.
7. Store it in the right scope folder; notify only affected people with a link.
8. When circumstances change, write a superseding ADR instead of editing history.

## References

- [references/decision-antipatterns-and-significance.md](references/decision-antipatterns-and-significance.md): read when a team is stalling, re-debating or losing decisions, when choosing a business justification, or when judging whether something is architectural at all.
- [references/adr-structure-and-authoring.md](references/adr-structure-and-authoring.md): read when writing or reviewing an ADR, setting status and supersession links, defining approval criteria, or designing a compliance check; includes an invented full example and a checklist.
- [references/adr-practice-storage-and-ai.md](references/adr-practice-storage-and-ai.md): read when deciding where ADRs live, turning standards into ADRs, documenting an existing system, or using generative AI to assist a decision.
- [references/source-map.md](references/source-map.md): read to see which reference covers each chapter section.

## Scripts

- Run `python3 scripts/adr_check.py lint <adr-file-or-dir> [...]` to check ADRs for required and recommended sections, valid status, RFC deadlines, "We will" voice and hedging words, alternatives in Context, a governance method in Compliance, length, duplicate numbers, and two-way supersession links (including superseding a non-Accepted draft). Add `--json` for machine output; exit code 1 means errors.
- Run `python3 scripts/adr_check.py route --hours 120 --fte-rate 45 --fees 1500 --threshold 5000 [--cross-team] [--security]` to compute decision cost and whether the ADR may be self-accepted or must be Proposed for escalation.
