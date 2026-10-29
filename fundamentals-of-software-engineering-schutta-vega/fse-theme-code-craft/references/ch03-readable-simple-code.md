# Readable, Simple Code: Size, Structure, Names, Comments, Tests, Cleverness

Covers: keeping codebases small, cohesion and coupling, boilerplate, composition, short methods, writing for readers, naming, when comments help or hurt, tests and contracts as documentation, and avoiding clever or error-prone code.

## Contents
- Why smaller is better
- High cohesion, low coupling
- Boilerplate is still a liability
- Prefer composition to inheritance
- Short, single-purpose methods
- Writing for the next reader
- Naming techniques
- Comments: the default is "rename instead"
- Tests and contracts as living documentation
- Essential versus accidental complexity
- Error-prone forms
- Pitfalls
- Glossary

## Why smaller is better

Every line is something a person has to hold in their head. Codebases eventually exceed what any one developer can understand, which is part of what pushed the industry toward microservices and functions as a service. Large tangled systems (the "big ball of mud") come with enormous onboarding guides, painfully slow builds, and weeks or months before a newcomer is productive. A smaller codebase shortens ramp-up and speeds contribution. Some problems truly need millions of lines; most do not.

## High cohesion, low coupling

Many design rules reduce to one principle, sometimes called the zeroth law of computer science:
- Cohesion: things that belong together live together. A notification module that also formats print output has low cohesion.
- Coupling: how much modules depend on each other. Tight coupling means a change in one place unexpectedly breaks something unrelated (editing notifications should never break printing).

Many design patterns are just ways to get this property at a particular level of abstraction; well-designed microservices apply it at the service level. When reviewing a design, ask of each unit: does everything here change for the same reason, and could I change it without touching its neighbors?

## Boilerplate is still a liability

Generated code is not free code. Whether the IDE or the framework produced it, the team maintains it for the life of the project. Keep classes short, a few pages at most and ideally one screen (verbose languages stretch this). Needing to scroll is a hint the class is too big.

## Prefer composition to inheritance

Inheritance is legitimate for true "is-a" relationships but is overused, often as a reuse trick. Reuse should fall out of good design, not justify a hierarchy. Hierarchies break when a new subtype violates an assumption baked into the base class. Example of my own: a `Printer` base class that assumes every printer has an ink cartridge breaks when a thermal printer arrives. Composing behavior instead avoids this:

```python
class Printer:
    def __init__(self, marking, feeder):
        self.marking = marking   # InkCartridge(), ThermalHead(), Toner()
        self.feeder = feeder     # SheetFeeder(), RollFeeder()

    def print_page(self, page):
        self.feeder.advance()
        self.marking.render(page)
```

Rule: default to composition; reach for inheritance only when the subtype relation is genuine and stable.

## Short, single-purpose methods

- Target single-digit line counts. Like small Unix tools, each method does one job well, and methods combine to do bigger things.
- A conjunction in a method name (and, or, but) signals two jobs; split it.
- Struggling to name a method often means it does too much; try decomposing it.
- Names should be descriptive and plain, never cute.
- Remove duplicated logic even when the duplicate is small.
- Simplify, then simplify again.

## Writing for the next reader

Apply the Golden Rule: write the code you would want to inherit, and ask what the next maintainer needs to understand.

Separate intent from implementation (Fowler's guidance): the right size for a function is whatever lets a reader grasp what it does from its name alone, without reading the body. This often produces one-line functions, and that is fine.

Structure modules like a news story with an inverted pyramid: the class name is the headline, method signatures summarize the story, and bodies hold the details. A reader should be able to stop at any depth and still have the gist.

```python
class InvoiceRun:
    def execute(self, period):
        invoices = self.collect_billable_accounts(period)
        self.apply_discounts(invoices)
        self.send(invoices)
    # helpers below, in the order execute() calls them
```

## Naming techniques

Naming is hard and worth the time; slowing down here saves time later.
- Difficulty naming can reveal fuzzy understanding of the problem or code that is too complex.
- Talk it through with a teammate; explaining often surfaces the right word.
- Work backward from the expression: write the right-hand side first and let the IDE propose a variable name (postfix completion). Agentic tools can also suggest candidates.
- Rename freely with IDE refactoring support. Exception: if core domain terms keep getting renamed, the team's model of the domain is probably wrong.
- Placeholder-word technique: early in domain discovery, give a concept a made-up nonsense name so a premature real word does not bias your thinking. Replace it after more analysis; the eventual name is usually different and clearer.

## Comments: the default is "rename instead"

Heavy commenting is arguably a smell:
- It repeats the code (a DRY violation in prose).
- Comments drift from the code as it changes, leaving misleading sediment for future readers.
- Time spent explaining code is usually better spent simplifying it. Avoid obscure language "magic" that needs explanation.
- If you feel a comment is needed, first try a better method or variable name; that usually removes the need.
- Change-history banners at the top of files (ticket numbers, dates, authors) are pure noise; version control already records this.

When comments are justified (be pragmatic, not dogmatic):
- Non-obvious code you could not simplify: explain why, not what.
- Why one algorithm or approach was chosen over another.
- Warnings or notes to future maintainers, including a hack that works for reasons not yet understood.

Still, if code needs explaining, the first option is to rewrite it.

```python
# Weak: restates the code
# loop over users and check if active
# Better: name it, and keep only the "why"
def active_users(users):
    # Vendor feed marks deleted accounts active=True; status is authoritative.
    return [u for u in users if u.status == "ACTIVE"]
```

## Tests and contracts as living documentation

Tests are executable specifications that evolve with the code, whereas READMEs, specs and comments start drifting the moment they are written. Fluent, readable test styles make this stronger. Tests written alongside the code also make refactoring safe and guide later developers. Adding tests to legacy code records what you learn about its behavior so others benefit; combined with renaming and deleting dead code, it leaves the code better than you found it. Tools that generate API docs from tests (Spring REST Docs, for example) keep docs synchronized.

For services consumed by other teams, prefer consumer-driven contracts (Pact, Spring Cloud Contract) over extensive consumer-facing comments:
- Providers can change internals freely as long as contracts pass, without fear of silently breaking downstream systems.
- Consumers get runnable tests that simulate the provider, so they can change their own code safely.

## Essential versus accidental complexity

Following Fred Brooks: essential complexity comes with the problem (business rules, team communication, a constantly changing codebase) and cannot be removed. Accidental complexity is what developers add (noisy technology, heavyweight tooling, overengineering). Remove accidental complexity relentlessly and default to the simplest thing. Be skeptical of products or processes promising to revolutionize delivery; big claims need big evidence.

## Error-prone forms

Every language has constructs that invite mistakes. Classic case: omitting braces on a single-statement `if` in C-family languages. A later edit adds a second indented line that looks guarded but always runs. Brevity is not worth that risk.
- Ban such forms in the team's coding standard (create one if none exists).
- Enforce with static analysis in the pipeline rather than relying on everyone remembering.
- Your own fluency with a tricky idiom does not mean the whole team shares it.

## Pitfalls
- Treating line-count rules as absolute instead of as prompts to examine the code.
- Keeping generated getters, setters and mappers that a language feature (records, data classes) could eliminate.
- Building deep class trees for reuse.
- Comments that narrate code; history banners.
- Writing documentation for consumers instead of contracts they can execute.

## Glossary
- Big ball of mud: a system with no discernible structure where everything depends on everything.
- Inverted pyramid: most important information first, detail later.
- Consumer-driven contract: a test, owned by the consumer's expectations, that the provider must keep passing.
- Error-prone form: a legal construct that commonly leads to bugs when code is later edited.
