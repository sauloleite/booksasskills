# IDE Navigation, Code Analysis, and Reading Tests

## Contents
- Learning the IDE continuously
- Navigation moves
- Hierarchy and dependency views
- Automated inspections as a teacher
- Structure views
- Tests as executable specification
- Workflow tests
- Edge-case tests
- Pitfalls

## Learning the IDE continuously

An IDE is an exploration instrument, not just a text editor, and it matters most when the code is unfamiliar. No one learns every feature at once, so adopt a steady habit:

- Learn one new feature or shortcut per week. Start with keyboard shortcuts for navigation; they pay off fastest.
- Use built-in tip mechanisms (for example, IntelliJ IDEA's "Tip of the Day," reachable from the Help menu). Other IDEs have similar features or documentation sections.
- Keep a personal "IDE tricks" note: record each new shortcut or feature, review it regularly, and deliberately use entries until they become reflexes.
- Tips span shortcuts, refactorings, debugging, code templates (such as live templates that expand common constructs), and plug-ins.

## Navigation moves

| Move | Question it answers | When it shines |
|------|--------------------|----------------|
| Find usages / references | Where is this class, method, or field used? | Learning a component's role from its consumers |
| Go to implementations | Which concrete types fulfill this interface or abstract type? | Seeing how an abstraction is used in practice |
| Jump to definition | What is this symbol, and how is it implemented? | Following logical flow from call site to body |
| Create in another file | Can I add a missing method without opening the file manually? | Quick experiments while exploring |

Jump to definition is especially useful for:
- third-party library internals,
- framework code,
- base classes and interfaces,
- shared utility helpers called all over the codebase.

Reading library or framework source this way often explains behavior faster than external docs.

## Hierarchy and dependency views

- **Call hierarchy:** both directions, who calls this method and what it calls. Shows a method's position in the larger flow.
- **Type hierarchy:** inheritance and implementation trees.
- **Dependency diagram:** how packages or modules depend on each other; reveals layering and coupling.

Use call hierarchy when a method's purpose is unclear; use type hierarchy when polymorphism hides which code actually runs; use dependency views before proposing structural refactors.

## Automated inspections as a teacher

IDEs analyze code continuously and propose refactorings. Treat them as suggestions:
- Review each one; you are not obliged to accept.
- Their real value for a learner is exposure to idioms of the language and its frameworks, for example replacing an explicit loop with a higher-order collection operation.
- Accept when the result is clearer for this team; decline when it obscures intent or conflicts with house style.

Illustration of the kind of nudge an inspection might give (Python, invented):

```python
# Before: works, but verbose
names = []
for user in users:
    if user.active:
        names.append(user.name)

# After: idiomatic comprehension the tool may propose
names = [user.name for user in users if user.active]
```

## Structure views

- **Project view:** reveals architecture at a glance, such as a single monolith with package-by-feature organization versus layered packages.
- **Class or file outline:** lists members without scrolling through bodies. Faster and more current than generated API docs, which may not match the version in front of you.
- **Collapse all bodies:** shrinks the surface to signatures. Read the method names as a table of contents: what do they say about the module's job?

## Tests as executable specification

Implementation shows how the code works; tests show how it is supposed to work, and often why. Because tests must pass in CI, they are a more reliable, current source of truth than prose docs.

Read tests first to learn:
- expected inputs and outputs of a unit,
- interactions between collaborators,
- overall system behavior.

Then open the implementation with that expectation in mind; it becomes much easier to follow. A given/when/then structure makes intent especially readable.

Invented example:

```python
def test_loyalty_points_double_on_member_birthday():
    # Given a member whose birthday is today
    member = Member(birthday=date(1990, 3, 14))
    # When they spend 100
    points = loyalty.points_for(member, amount=100, today=date(2026, 3, 14))
    # Then they earn double the usual 100 points
    assert points == 200
```

From this alone you learn the base rate, the birthday rule, and that `today` is injected (so the implementation should avoid reading the clock directly).

## Workflow tests

- Tests frequently correspond to user stories, which makes them a map of business processes.
- Zoom out to integration or end-to-end tests to see how components collaborate on a full requirement.
- Their setup code models realistic scenarios, which hints at production usage patterns.
- Look for assertions on multiple effects of one action (for example, a stored state change plus a verified notification) to learn the whole consequence chain of a user action.

## Edge-case tests

Edge cases are valid but unusual inputs or conditions where assumptions fail. Mature codebases tend to accumulate such tests because each one was usually added after a bug surfaced.
- Scan test names for words like empty, invalid, reject, timeout, expired, overflow, concurrent, null.
- These tests reveal system limits and likely failure points, and they document behavior that is hard to infer from implementation alone (for example, a graceful rejection path).
- After reading one, find the code that implements that guard; it often lives far from the happy path.

## Pitfalls

- Trusting tests that have no assertions (they document nothing; see the onboarding reference on metrics).
- Treating an inspection suggestion as mandatory.
- Navigating by scrolling and manual file opening instead of symbol-aware moves.
- Reading API docs that may not match the code version in use instead of the structure view.
