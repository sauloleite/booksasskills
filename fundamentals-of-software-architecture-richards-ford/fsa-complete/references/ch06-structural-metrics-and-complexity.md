# Structural Measures and Cyclomatic Complexity

## Contents
- Structural characteristics are implicit and hard to score
- Cyclomatic Complexity: definition and formulas
- Worked calculation
- Interpreting CC: essential versus accidental
- Thresholds
- Engineering practices that keep CC low
- Review checklist

## Structural characteristics are implicit and hard to score

Well-defined modularity is rarely requested by stakeholders, yet the architect owns component boundaries and their interactions, so it is an implicit characteristic. No comprehensive metric yet scores "architecture quality" as a whole. What exists are narrow, code-level metrics and tools that each illuminate one dimension: complexity, coupling (afferent and efferent), abstractness and instability, distance from the main sequence, cycles. Use several narrow lenses together rather than hunting for a single score.

## Cyclomatic Complexity: definition and formulas

Cyclomatic Complexity (CC), introduced by Thomas McCabe Sr. in 1976, counts the independent execution paths through code by treating it as a control-flow graph. It applies at function, class or application level.

- Straight-line function, no branches: CC = 1. One conditional: CC = 2.
- Single function: CC = E - N + 2, with E edges and N nodes of the control-flow graph.
- General form for several connected components (fan-out into other routines): CC = E - N + 2P, P = number of connected components.
- Practical shortcut used by most tools (and by `scripts/complexity_gate.py`): CC = 1 + number of decision points (if/elif, loops, catch blocks, ternaries, each extra boolean operand, comprehension filters, case arms).

## Worked calculation

An original example:

```python
def shipping_fee(weight_kg, express, member):
    if weight_kg <= 0:                    # decision 1
        raise ValueError("weight")
    fee = 5 + 2 * weight_kg
    if express and not member:            # decision 2, extra operand 3
        fee *= 2
    for _ in range(int(weight_kg // 50)): # decision 4
        fee += 10
    return fee
```

CC = 1 + 4 = 5. Every independent path needs a test case to be covered, so CC is also a lower bound on the tests required for full branch coverage. Splitting the surcharge loop into its own function gives two functions with CC 4 and 2: total paths do not vanish, but each unit becomes easier to read and test.

## Interpreting CC: essential versus accidental

CC is blunt. It tells you code is complex, not why. Two causes look the same in the number:

- **Essential complexity**: the problem itself is intricate (pricing rules, scheduling algorithms).
- **Accidental complexity**: a poor design or poor partitioning made the code harder than the problem.

Questions to ask about a high-CC unit:

1. Is the domain genuinely algorithmic here, or is this glue code?
2. Is the work badly partitioned? Could the large method split into smaller, logically named steps that distribute the paths?
3. Is the complexity growing over time? Unwatched, it gradually takes over a code base and erodes modularity, testability and deployability.

Overly complex code is a widely recognized code smell. CC is equally useful for reviewing code from generative AI tools, which tend to brute-force solutions and pile up accidental complexity (long branch ladders, duplicated special cases).

## Thresholds

| Value | Reading |
|---|---|
| under 5 | Authors' preference: cohesive, well-factored code |
| under 10 | Common industry ceiling, absent a complex domain |
| above 10 | Justify as essential or refactor |
| above 50 | Beyond rescue by tests; the Crap4J tool (which combines CC with coverage) treats such code as poor regardless of coverage |

Context matters: an algorithmically hard domain legitimately produces higher values, so record such exceptions explicitly (an allowlist with a reason) rather than raising the global limit. Extreme cases exist in the wild: a single C function in a commercial product with CC above 800, spanning more than 4,000 lines and using GOTO to escape deeply nested loops. Treat that as the cautionary endpoint of unwatched growth.

## Engineering practices that keep CC low

- **Test-driven development** tends to yield smaller, simpler methods: writing one small test, then the minimum code to pass it, keeps each method focused on a discrete behavior with clear test boundaries.
- Extract method / replace conditional with polymorphism or lookup tables.
- Run a CC gate in CI with a hard limit and a softer warning target, so growth is visible per change.

## Review checklist

- [ ] CC measured per function, and trend tracked over time, not only snapshots.
- [ ] Hard limit (e.g. 10) fails the build; target (e.g. 5) produces warnings.
- [ ] Every exception above the limit has a written domain justification.
- [ ] High-CC units examined for poor partitioning before being accepted as essential.
- [ ] AI-generated changes checked with the same gate as human code.
- [ ] CC combined with other structural lenses (coupling, cycles, main-sequence distance).
