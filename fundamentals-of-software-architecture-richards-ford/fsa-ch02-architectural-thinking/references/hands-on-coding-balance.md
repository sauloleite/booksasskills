# Balancing Architecture Work and Hands-On Coding

## Position

The authors hold that every architect should keep coding and keep some technical depth, while accepting that breadth is the priority. The difficulty is practical: the architect's calendar (diagrams, meetings, more meetings) fragments the time needed for development work.

## The Bottleneck Trap

**What it is.** The architect claims ownership of code on the system's critical path, typically the shared framework or the hardest parts, and then cannot deliver it on time because they are not a full-time developer. The team waits on them.

**Symptoms an agent can detect in a user's description:**

- The architect is sole owner of the core framework, shared library, or a central integration.
- Pull requests for foundational code queue up for the architect.
- Sprint goals slip because a framework piece is unfinished.

**Remedy.**

1. Hand the critical-path and framework code to developers on the team.
2. Have the architect take a small piece of business functionality (a service, a screen) scheduled one to three iterations ahead, so there is slack if meetings eat their time.

**Why the remedy works (three effects):**

- The architect still writes real production code without blocking anyone.
- The team owns and understands the hard parts of the system, which is where that ownership belongs.
- The architect experiences the same day-to-day friction as the team (process, tooling, environment) and is more likely to fix it.

## Staying hands-on when team coding is not possible

| Technique | How it keeps skills alive | Extra payoff | Guidance |
|---|---|---|---|
| Frequent proofs of concept | Writing real code to compare options | Validates decisions against implementation detail and effort | Write production-quality code: POC code often lands in the repo and becomes the template others copy, and sloppy POCs train sloppy habits |
| Technical debt items | Real code changes | Frees developers for critical stories | Low priority, so missing one in an iteration does little harm |
| Bug fixes | Contact with the real code base | Reveals weaknesses in code and possibly in the architecture | Unglamorous but informative |
| Automation | Building small CLI tools, analyzers, custom validators, checklists, scripted refactorings | Makes the team faster; they will appreciate it | Target repetitive team tasks; include architecture fitness functions (for example, ArchUnit-style dependency rules) to check compliance |
| Code reviews | Reading code regularly | Checks architectural compliance; spots mentoring and coaching opportunities | Least hands-on option, but keeps the architect close to the source |

### Example: POC for choosing between two caches (invented)

An architect deciding between two caching products builds the same small read-through cache in each, runs a short load test, and records latency, failure behavior under node loss, and lines of glue code needed. The comparison exposes integration effort that vendor documentation hid, and the code is clean enough to serve as the team's reference if one product is chosen.

### Example: a tiny fitness function (original)

```python
# Fails the build if any module under app/domain imports from app/web.
import ast, pathlib, sys

violations = []
for path in pathlib.Path("app/domain").rglob("*.py"):
    tree = ast.parse(path.read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and (node.module or "").startswith("app.web"):
            violations.append(f"{path}: imports {node.module}")
        if isinstance(node, ast.Import):
            violations += [f"{path}: imports {a.name}" for a in node.names
                           if a.name.startswith("app.web")]

if violations:
    print("\n".join(violations))
    sys.exit(1)
```

## Advice checklist for an architect asking "how much should I code?"

- Do you own anything the team is blocked on? If yes, hand it over now.
- Pick one business feature one to three iterations out.
- Schedule at least one POC per significant pending decision.
- Keep a short list of debt items and bugs you can pick up between meetings.
- Automate one repetitive team task per quarter; prefer ones that enforce architecture rules.
- Review code weekly, looking for compliance gaps and coaching moments.

## Closing note from the chapter

This chapter is only the foundation of architectural thinking. The book later extends it to understanding overall system structure, translating business concerns into architecture characteristics, and viewing a system through its logical components.
