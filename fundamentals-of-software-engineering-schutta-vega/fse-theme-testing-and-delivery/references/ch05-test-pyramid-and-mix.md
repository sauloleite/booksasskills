# The Test Pyramid and Choosing a Test Mix

## Contents
- The model
- Comparison of the three levels
- Unit tests
- Integration tests
- End-to-end tests
- Deciding the mix
- Decision guide: which level for this check?
- Glossary

## The model

The testing pyramid, credited to Mike Cohn, is the chapter's organizing idea, and it notes the model is often misunderstood or skipped. Three layers, widest at the bottom:

- **Unit** (base, most numerous)
- **Integration** (middle)
- **End-to-end** (top, fewest)

The shape follows from cost. Climbing the pyramid, each test runs slower, costs more to maintain and breaks more easily. A unit test may take microseconds; an E2E test may take minutes. Multiply by hundreds or thousands of tests and the shape of the suite decides whether feedback arrives in seconds or hours.

## Comparison of the three levels

| Property | Unit | Integration | End-to-end |
|---|---|---|---|
| Scope | One component or function, isolated | Several real components interacting | Whole application, UI through backend |
| Speed | Very fast | Slower | Slowest |
| Typical cadence | Every save / every CI run | Less often than unit tests | Often scheduled |
| Failure localization | Points at a function or line | Needs investigation of which interaction failed | May need substantial debugging |
| Brittleness | Low | Medium | High; prone to false failures from cosmetic UI changes |
| Confidence about the whole system | Low per test | Medium | High |
| Dependencies | Mocked | Real or test doubles | Real environment |

## Unit tests

- Act like a contract: if the code's functional behavior changes, a unit test should fail.
- First line of defense, alongside static analysis and code review.
- Must be cheap to write and fast to run so developers run them constantly.
- Their precision is the payoff: a failure tells you where to look.

## Integration tests

- Verify that modules cooperate correctly; they catch defects that only appear when individually correct parts are combined.
- Broader than unit tests, narrower than full-system tests.
- Slower and run less often; when they fail, expect to investigate which interaction broke.
- Managing several dependencies and their state is the main source of complexity. Keep the number of real collaborators per test small and reset state between tests.

## End-to-end tests

- Simulate real user scenarios across the full stack in a realistic environment.
- Resource-hungry and slow, so keep them few and focused on the most important journeys.
- Brittle: a renamed button or moved element can fail a test even though the feature works (the chapter calls this a false negative). Prefer stable selectors or API-level entry points to reduce this.
- Despite the cost, they give the strongest evidence that the pieces work together.

## Deciding the mix

There is no universal ratio. The chapter says the right numbers depend on:
1. Application complexity.
2. Technology stack.
3. How critical the application is.
4. Organizational standards (some companies prescribe coverage or quality benchmarks).

Keep the pyramid's proportions as the default, then tailor. A safety-critical payments system justifies more integration and E2E coverage of money paths; a small internal tool may need almost only unit tests plus one smoke E2E.

Anti-pattern to flag (common industry name, not the chapter's term): the "ice cream cone" (many slow UI tests, few unit tests). Symptoms: CI takes very long, failures are hard to diagnose, and the team learns to ignore red builds.

## Decision guide: which level for this check?

Ask in order and stop at the first "yes":
1. Is it pure logic or a rule inside one class (calculation, validation, branching)? Write a **unit** test.
2. Is the risk in how two or more of your components talk, or in your code's contract with a database, queue or framework configuration? Write an **integration** test.
3. Is it a business-critical user journey where only the full stack proves correctness? Write one **E2E** test for the happy path, and push edge cases down to lower levels.

Worked example (invented): a discount feature.
- Unit: percentage math, rounding, expiry dates, stacking rules (many tests).
- Integration: the discount repository persists and loads codes correctly; the pricing service uses it (a few tests).
- E2E: a shopper applies a code at checkout and sees the reduced total (one test).

## Glossary

- **Regression test**: a test that guards existing behavior against being broken by later changes.
- **False negative (chapter's usage)**: a failing E2E test where the feature actually works, caused by an incidental change such as UI markup.
- **SDLC**: software development life cycle; integration testing is presented as an essential stage of it.
