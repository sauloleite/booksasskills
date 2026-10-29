# Elastic Leadership: How Involved Should the Architect Be?

## Idea

Effectiveness depends on calibrating involvement: when to engage closely and when to step back. The chapter adapts Roy Osherove's Elastic Leadership to architecture-specific factors. The same calibration also tells an architect how many teams or projects they can realistically support at once.

## The five factors

| Factor | Pushes toward MORE involvement | Pushes toward LESS involvement |
|---|---|---|
| Team familiarity | Members are new to one another; architect must foster collaboration and break up cliques | Members have worked together; they self-organize |
| Team size | Large (the book treats more than 12 developers as big) | Small (5 or fewer) |
| Overall experience | Mostly junior; weak grasp of technology or domain; architect mentors | Mostly senior; architect acts as facilitator |
| Project complexity | High; architect must be available for hard issues | Simple and straightforward |
| Project duration | Long (around two years) | Short (around two months) |

Notes:
- For complex business domains, rate technical experience and domain experience separately; a team can be strong in one and weak in the other.
- Larger teams also raise the risk of the dysfunctions in the team warning signs reference.

### The duration factor is counterintuitive

Short project, less involvement: a two-month effort already carries urgency. The team is pressed to clarify requirements, experiment, build, test and release, so heavy architect intervention only slows it down. Lean toward armchair behavior here.

Long project, more involvement: a two-year effort lacks urgency, and pace slackens. The architect is needed to keep the schedule honest and to make sure the hardest work is tackled first rather than deferred.

## Scoring scale

Place each factor on a fixed scale from -20 (less involvement, armchair end) to +20 (more involvement, control-freak end). Add the five. The book's illustrations use only the extremes (+20 or -20 per factor), giving a range of -100 to +100.

Interpreting the total:
- Strongly negative: largely hands-off; facilitate, answer questions, confirm the team is on track, and let them move fast.
- Near zero to moderately positive: mentoring and coaching with regular day-to-day presence, without disrupting the team.
- Strongly positive: close guidance is justified, but remember the control-freak dividing line still applies (do not design the internals of components).

### Worked examples (invented, same mechanics as the book)

**Example A: payments reconciliation microsite.** Team of 4 who have never worked together (+20), small (-20), all senior (-20), simple scope (-20), 10 weeks (-20). Total -60. Stance: facilitator. The architect's first act should be helping the new team gel, then stepping back.

**Example B: core policy administration rewrite.** Team has worked together for years (-20), 14 developers (+20), two thirds junior (+20), heavy regulatory logic (+20), 5 months (-20). Total +20. Stance: mentor and coach. Schedule pairing sessions, run frequent design reviews, but let developers own component internals.

**Example C: same as B but planned for 24 months.** Duration flips to +20. Total +60. Expect to be deeply embedded; this team likely consumes most of one architect's capacity, so do not plan to lead another large effort in parallel.

## Caveats the chapter states

- **Re-evaluate continuously.** Score at kickoff to set initial involvement, then rescore as the team and project change (people join, juniors grow, complexity surfaces).
- **The scale is imprecise.** Factors are not equally important in every situation. Weight them (for example, double the experience factor when the team is mostly new graduates) or adjust values to fit.
- **The message is the variability, not the number.** The right amount of involvement changes with these factors; using them lets the architect size the room appropriately.

## Capacity planning use

Summing involvement across teams gives a rough sense of load. An architect carrying two strongly positive teams is at risk of drifting into armchair behavior on both, which the personalities reference describes as the usual route into that trap.

## Script

`scripts/involvement_score.py` computes the total, supports keyword or numeric ratings, optional weights, and derives size and duration ratings from headcount and months with documented interpolation heuristics.
