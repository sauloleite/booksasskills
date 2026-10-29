# The Eight Expectations of an Architect: Playbook

## Contents

- Overview
- 1. Making architecture decisions
- 2. Continually analyzing the architecture
- 3. Keeping current with trends
- 4. Ensuring compliance
- 5. Understanding diverse technologies
- 6. Knowing the business domain
- 7. Interpersonal skills and leadership
- 8. Understanding and navigating politics
- Quick self-assessment

## Overview

The architect role spans everything from senior hands-on programmer to setter of company-wide technical strategy, so a fixed job description is impractical. What is stable is a set of eight expectations that apply whatever the title. Use them to evaluate an architect's coverage, to plan what an architecture engagement must include, or to coach someone into the role.

## 1. Making architecture decisions

The architect sets the decisions and design principles that steer technology choices for a team, a department or the enterprise. The operative verb is *guide*.

**Decision rule: architectural vs technical.**

| Question | If yes | If no |
|---|---|---|
| Does the decision constrain a category or principle (e.g., "frontends use a reactive framework")? | Architectural: the architect owns it | Probably technical |
| Does it name a specific product (e.g., one particular UI framework)? | Technical: delegate to the team | n/a |
| Is that specific product needed to secure a critical characteristic (scalability, performance, availability)? | Architect may decide it, and should record why | Leave it to the team |

The test: does the decision help teams make good choices, or does it make the choice for them? Default to the former. Finding the balance is genuinely hard, so be explicit about which mode a decision is in.

## 2. Continually analyzing the architecture

The architect keeps examining the existing architecture and its technology environment and proposes improvements.

- **Architecture vitality**: how well an architecture designed three or more years ago still fits today's business and technology. Schedule periodic vitality reviews; the authors observe that few architects spend enough effort here.
- **Structural decay**: gradual erosion caused by code or design changes that undermine required characteristics such as performance, availability or scalability. Detect it with characteristic-focused metrics, not only code reviews.
- **Test and release environments are part of the architecture.** If code changes in hours but testing takes weeks and releasing takes months, the system is not agile. Include pipeline lead times in any agility assessment.

Checklist for a vitality review: business drivers changed? new technology options? characteristics still met (measured)? decay hotspots? test and release lead times?

## 3. Keeping current with trends

Developers must stay current to stay employable; architects even more so, because their decisions last long and cost a lot to reverse. Trend awareness helps make choices that will still make sense years later. Recent examples the authors name are cloud storage and deployment, and the broad impact of generative AI on development. The book treats techniques for tracking trends in its next chapter.

Agent implication: when advising on a long-lived decision, mention relevant emerging shifts and how they might affect the decision's lifespan.

## 4. Ensuring compliance

Defining and communicating a decision is not enough; the architect must keep verifying that teams follow it.

**Scenario (book's example, summarized).** A layered system restricts database access to the business and service layers so that database changes do not ripple into the UI. A UI developer, wanting speed, wires the presentation layer straight to the database. Without compliance checks, the violation persists and the property the rule protected (isolation from schema change) quietly disappears, so the system no longer delivers what was required.

Playbook:

- For each decision, state the characteristic it protects.
- Choose a verification mechanism: automated fitness functions, dependency or layering checks in CI, review gates.
- When a violation has a legitimate motive (here, performance), treat it as a signal to revisit the trade-off openly rather than tolerate silent drift.

Illustrative layering check (original, framework-agnostic):

```python
# Fail the build if UI modules import the data-access package directly.
import ast, pathlib, sys

FORBIDDEN = "app.persistence"
violations = []
for path in pathlib.Path("app/ui").rglob("*.py"):
    tree = ast.parse(path.read_text())
    for node in ast.walk(tree):
        names = []
        if isinstance(node, ast.Import):
            names = [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module:
            names = [node.module]
        violations += [f"{path}: {n}" for n in names if n.startswith(FORBIDDEN)]
if violations:
    print("\n".join(violations)); sys.exit(1)
```

## 5. Understanding diverse technologies

Architects need exposure to many technologies, frameworks, platforms and environments, not expertise in all. Since most estates are heterogeneous, the minimum bar is knowing how to integrate across languages and platforms.

- Prefer **technical breadth** (many things known at a summary level, plus a few known deeply) over pure depth.
- Example of the principle: knowing the pros and cons of ten caching products is worth more to an architect than mastery of one.
- Growth tactic: deliberately take on work in unfamiliar languages and platforms.

## 6. Knowing the business domain

Effective architects understand the problem, goals and requirements the system addresses (the business domain). Without that, design suffers and credibility evaporates; picture an architect in finance who does not recognize basic trading or debt terminology. The strongest architects combine broad hands-on technical knowledge with deep knowledge of one domain, and can speak to executives and business users in their own terms.

Agent implication: before proposing architecture, elicit and use the domain's vocabulary; map characteristics to business outcomes.

## 7. Interpersonal skills and leadership

Teamwork, facilitation and leadership are expected at a high level, even though technologists usually prefer technical puzzles to people problems. Gerald Weinberg's observation that problems ultimately turn out to be about people applies directly. Architects lead teams through implementation, not just hand over designs; the authors estimate leadership is at least half of effectiveness in the role. In a crowded market, strong interpersonal skills differentiate candidates, while brilliant technologists who cannot coach, mentor or communicate decisions struggle to keep their positions.

## 8. Understanding and navigating politics

Negotiation is central to the job. Compare two cases:

- A developer refactors messy code using a design pattern. Code structure, class design, pattern choice and sometimes even language choice belong to the craft of programming; no approval needed.
- An architect owns a CRM whose database is used directly by many other systems, making access control, data protection and schema change hard. The architect decides each application database will be reachable only by its owning application. Other teams must now call the CRM remotely, so product owners and managers see added cost and effort, and developers may prefer their own approach. Nearly everyone except the CRM team pushes back.

Lessons:

- Expect almost every architectural decision to be challenged, unlike most developer decisions.
- Former developers often find this frustrating: they gained authority over broad decisions but lost the ability to decide without justification.
- Prepare negotiation material in advance: who bears new costs, what they gain (security, change agility), migration support, and the business case. The book devotes a later chapter to negotiation.

## Quick self-assessment

Rate each expectation as strong, adequate or gap, then pick the weakest two for a development plan:

- Decisions guide rather than dictate
- Regular vitality reviews, including pipelines
- Active trend tracking
- Automated compliance checks for key decisions
- Breadth across technologies
- Fluency in the business domain
- Leadership, coaching and communication
- Negotiation and stakeholder navigation
