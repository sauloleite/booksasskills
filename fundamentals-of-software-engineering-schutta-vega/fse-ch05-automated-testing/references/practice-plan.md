# Building the Testing Habit: Practice Plan

## Principle

Testing skill grows through repetition, not a single push. Pick one or two of the practices below that fit the current situation, make them routine, then add more. One test written today beats a perfect strategy written never.

## Practices by situation

**You want to learn how good suites look**
- Open the test folder of a well-maintained open source library you already use.
- Note behaviors you did not know the library had.
- Compare its structure, naming, fixtures and assertion style with yours; borrow one technique.

**You are new to a part of the codebase**
- Read the existing tests before the implementation.
- Where tests are thin, write new ones (characterization tests, in common parlance) that capture what the code currently does as you learn it; your learning becomes a permanent asset.

**The project has too few tests**
- Do not attempt a big-bang fix; improve incrementally.
- Set a small team norm, for example each developer adds one meaningful test per day, prioritizing code they touch.

**You are starting a new feature**
- Write the tests first. It forces the requirements into concrete examples and nudges the design toward testable seams.

**You are fixing a bug**
- First write a test that reproduces the bug and fails.
- Fix the code until it passes; keep the test as a regression guard.
- Use the moment to refactor nearby code for readability or structure, protected by the new test.

**A production issue slipped through**
- Add the test that would have caught it.
- Turn it into a blameless learning point for the team.
- Raise with your manager how better coverage of that area would prevent repeats.

**You want deliberate practice**
- Do code katas (small, repeatable exercises such as a string calculator, bowling score or roman numerals) using red-green-refactor.

## Coaching script for an agent

When a developer asks for help with a change, offer the smallest testing step that fits:
1. "Is there an existing test for this behavior? Let us read it first."
2. "Can we write a failing test that shows the bug or the new requirement?"
3. "Which collaborator should be mocked so this stays a unit test?"
4. "Does this need an integration test because the risk is in the wiring?"

## Further study (titles only)

- Single responsibility principle (any solid write-up)
- JUnit 5 user guide
- Mockito documentation
- AssertJ and Hamcrest assertion libraries
- Robert C. Martin, *Clean Code* (2008)
