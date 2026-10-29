# Why Over How, Spectrum Thinking, and Practice

## Second law: rationale outranks mechanism

An experienced architect can read an existing system and explain how it works. What usually cannot be recovered from the system itself is why a given option beat its alternatives, because earlier architects did not write down their criteria. Every trade-off analysis produces much more context than ends up visible in the final design.

Guidance:

- Use two complementary artifacts: diagrams show the how (topology, components, flows); ADRs capture the why (factors, weights, options rejected, compromises, limitations).
- Record the analysis even when the result seems obvious. The next reader, possibly your future self, otherwise repeats the whole analysis just to understand the decision.
- Document known weaknesses of the chosen option openly; they become the mitigation backlog and the trigger list for re-analysis.

Minimum "why" content for any decision record:

1. Options considered, including those rejected.
2. Factors and the direction each one points.
3. Weights and who supplied them.
4. The chosen option and the compromises accepted.
5. Conditions that would reopen the decision.

When reviewing an existing system, an agent should flag components whose rationale is undocumented and propose retroactive records, asking stakeholders what the original drivers were.

## Third law: decisions sit on a spectrum

The authors found two laws for the first edition and recognized a third while writing the second: architecture choices are rarely binary; they are positions along a continuum between two extremes.

Why definitions in architecture are so slippery (for example, where design ends and architecture begins, or when coordination counts as orchestration rather than choreography, or a topic versus a queue): the criteria themselves are graded, so the boundary between concepts is fuzzy.

Working consequences:

- Do not reduce a decision to yes or no. Express it as a position: how much coordination is centralized, how coarse the services are, how much data is shared, how many consumers get dedicated channels.
- Hybrids are legitimate outcomes (for example, orchestrate the critical path, choreograph side effects; dedicated queues for confidential consumers, a topic for the rest).
- "It depends" really means "it depends on where the relevant criteria fall on their spectrums." Name those criteria.

### Architecture or design?

The third law yields a practical test for where a decision falls on the architecture versus design spectrum: if every option carries significant trade-offs, the decision leans architectural. If one option is clearly better with negligible cost, it leans toward design and can usually be left to the implementing team.

| Signal | Leans architecture | Leans design |
|---|---|---|
| Every option has significant costs | Yes | No |
| Affects structure or key characteristics | Yes | Rarely |
| Easy and cheap to reverse | Rarely | Often |
| Needs stakeholder weighting | Yes | Seldom |

### Deciding under uncertainty

Architects work in a fog: information is often incomplete, and even full information would not make many decisions clear-cut, because the answer lies somewhere between extremes. Accept this rather than waiting for certainty.

- State the assumptions explicitly.
- Choose the position that best fits current weights.
- Make the decision cheap to revisit where possible, and record what new information would move the position.

## Parting advice: practice deliberately

The chapter closes with a point raised by Ted Neward building on Fred Brooks: designers improve by designing, yet architects may get to shape only a handful of real systems in a career. Deliberate practice fills the gap.

- Use architecture katas (the authors publish a set on their companion website): short exercises with a problem statement and requirements, solved by a small team in limited time.
- There is no answer key; katas have trade-offs, not correct answers.
- The authors once tried to collect students' kata drawings into an answer bank and abandoned the idea: the drawings showed only topology (how), while the more valuable reasoning (why) had been spoken aloud in class and never written as ADRs. Half the story was missing.
- Lesson for practice sessions: produce at least a brief ADR alongside every kata diagram.
- Keep learning and keep widening technical breadth alongside depth.

### Running a kata session (agent playbook)

1. Pick or write a problem with a few explicit requirements and one or two implicit characteristics to discover.
2. Time-box: identify characteristics, choose a style, sketch components.
3. For each major choice, write a three-line ADR: options, deciding factors with weights, compromise accepted.
4. Critique by asking which context change would flip each choice, not by grading against a reference answer.
