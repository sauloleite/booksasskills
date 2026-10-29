# Writing Tests: Mechanics Playbook

## Contents
- Getting started in any stack
- Test-first vs test-last
- Using AI to write tests
- Assertions
- Unit tests and the system under test
- Mocking dependencies
- Integration tests
- End-to-end tests (API level)
- Naming and layout conventions
- Pitfalls

The chapter's examples are Java (JUnit 5, Mockito, Spring Boot). The ideas transfer; snippets below are original and written in Python/pytest style for neutrality.

## Getting started in any stack

1. Pick the ecosystem's mainstream test runner (JUnit for Java, pytest for Python, Jest/Vitest for JS/TS, xUnit/NUnit for .NET, `go test`).
2. Add it as a test-scoped dependency in the build file.
3. Mirror the source layout: put tests in the conventional test root, in the same package/module path as the code under test, so package-private access and navigation work.
4. Read the runner's user guide once; it pays back quickly.

## Test-first vs test-last

| | Test-first (TDD) | Test-last |
|---|---|---|
| Loop | Red (write a failing test), green (minimal code to pass), refactor (improve without changing behavior) | Implement, then add tests |
| Strength | Clarifies requirements and drives design before code exists | Natural when exploring or when the shape is unclear |
| Risk | Slower start; needs discipline | Tests bent to fit existing code; design smells go unnoticed; tests get skipped under pressure |

The chapter treats both as legitimate and leaves the choice to project needs and team preference. Practical defaults for an agent:
- **Bug fix**: always reproduce with a failing test first.
- **New feature with clear requirements**: lean test-first.
- **Spike or prototype**: test-last, then add tests before merging.

## Using AI to write tests

The chapter singles out test writing as a strong fit for AI help. To get tests that match the team:
- Feed the assistant a few representative existing tests so it copies naming, structure, assertion library and style.
- Ask it to list edge cases you missed (nulls, empty collections, boundaries, negative numbers, duplicates, time zones).
- Let it draft boilerplate and refactor clumsy tests for readability.
- Then review: confirm each generated test asserts real behavior, would fail if the code were wrong, and does not just mirror the implementation.

## Assertions

An assertion checks that a condition holds; if not, the test fails. Learn the assertion vocabulary of your library (equality, exceptions, collections, approximate floats). Note argument order conventions: JUnit's `assertEquals` takes the expected value first, then the actual. Fluent libraries such as AssertJ or Hamcrest read more like prose and give clearer failure messages.

## Unit tests and the system under test

The object being tested is called the **system under test (SUT)**. A unit test exercises only the SUT. Steps:
1. Create one SUT instance per test class or test.
2. Write one test per behavior; start with method stubs if that helps you plan.
3. Cover typical inputs plus edge cases, so users are not the ones who find them.

```python
from shipping import ShippingCalculator

sut = ShippingCalculator(free_threshold=50)

def test_charges_flat_fee_below_threshold():
    assert sut.fee(order_total=49.99) == 5.00

def test_is_free_at_exact_threshold():
    assert sut.fee(order_total=50.00) == 0.00

def test_rejects_negative_totals():
    import pytest
    with pytest.raises(ValueError):
        sut.fee(order_total=-1)
```

## Mocking dependencies

A **dependency** is any collaborator the SUT relies on. A **mock** (a test double that stands in for the real thing) looks like the collaborator but only does what the test programs it to do. If a unit test uses the real repository and real email sender, it has quietly become an integration test.

Pattern:
1. Create mocks for each collaborator.
2. Inject them into the SUT (constructor injection makes this trivial; that is another design benefit).
3. Stub the answers the scenario needs.
4. Call the SUT.
5. Verify outcomes and, where the behavior *is* the interaction, verify the calls.

```python
from unittest.mock import Mock
from accounts import SignupService

def test_signup_saves_and_greets_new_member():
    repo, mailer = Mock(), Mock()
    repo.username_taken.return_value = False
    SignupService(repo, mailer).sign_up("ana", "ana@example.org")
    repo.save.assert_called_once()
    mailer.send_welcome.assert_called_once_with("ana@example.org")

def test_signup_refuses_taken_username():
    repo, mailer = Mock(), Mock()
    repo.username_taken.return_value = True
    SignupService(repo, mailer).sign_up("ana", "ana@example.org")
    repo.save.assert_not_called()
    mailer.send_welcome.assert_not_called()
```

The collaborators get their own unit tests elsewhere. Avoid over-mocking: if a test is mostly stubbing, the SUT may have too many collaborators.

## Integration tests

Goal: check that the SUT works with its real collaborators.
- Mark them clearly. The chapter uses an `Int` suffix in the test class name; a separate folder, tag or marker also works and lets CI run them on a different cadence.
- Build real instances (manually, or via the framework's dependency injection) in a per-test setup hook so each test starts fresh.
- Cover both the valid path and rejection paths.
- Keep external systems you do not own behind test doubles or local containers; manage their state explicitly.

## End-to-end tests (API level)

The chapter's E2E example targets a backend API: start the real application on a random port with an embedded server, send an HTTP request, then check both the response and the resulting persisted state. Recipe:
1. Boot the app in a test profile on a random free port (avoids collisions in parallel CI).
2. Reset the data store before each test so runs are independent.
3. Send the request the way a client would (JSON body, real route).
4. Assert the status code and body.
5. Assert side effects (row saved, message queued). Skip nothing important "for brevity" in real suites.

## Naming and layout conventions

- Name tests as behaviors: `should_reject_expired_card`, `when_cart_empty_then_total_is_zero`.
- Include negative cases in names so the suite documents what is unsupported.
- Distinguish levels by suffix, folder or tag (`*Test`, `*IntTest`, `*E2ETest`).

## Pitfalls

- Assertion-free tests.
- Swapped expected/actual arguments, producing confusing failure messages.
- Shared mutable fixtures leaking state between tests.
- Unit tests that touch the network, file system or clock without control.
- E2E tests that depend on execution order or leftover data.
