# Practice Drills and Further Reading

Use these when a developer asks how to build the skill deliberately, or as stretch tasks during onboarding. Each drill names the skill it trains.

## Drills

1. **Read-only reconnaissance (structure).** Pick an open source repo you find interesting. Set a timer for half an hour and write no code: identify its architectural pattern, its entry points and its build tooling. Write a five-line summary.
2. **Full request trace (execution flow).** In a small web app, choose one user action and follow it from the click through the network call, the handler, log lines, and the database write. Use devtools, then logs, then the debugger, in that order. Record each hop.
3. **Readability refactor (safe refactoring).** Find a confusing method in an open source project. Make it clearer without changing behavior, running the tests after every step.
4. **Pin legacy behavior (characterization tests).** Take a lightly tested legacy module and write tests that capture what it does now, including any odd behavior.
5. **One-process diagram (mental models).** Choose one business process in a real codebase and draw it as a sketch, flowchart, sequence or component diagram. Ask a teammate to correct it.
6. **Small-commit change (version control).** Implement a non-trivial change as a series of small, reversible commits. Ask a peer to critique the commit sequence, not just the final diff.
7. **Three scout improvements (scout rule).** In your current project, find three small cleanups in files you are already touching and ship them as separate commits.
8. **Dependency upgrade plan (change safety).** Choose one external dependency and write an upgrade or replacement plan: what calls it, what could break, how you would verify, and how you would roll back.
9. **Hotspot triage (history).** Run `scripts/git_hotspots.py` on a repo you are new to. Pick the top hotspot and its strongest coupled partner, and explain why they change together.

## Further reading (titles only)

- Martin Fowler, Refactoring: Improving the Design of Existing Code (2nd ed.)
- Michael Feathers, Working Effectively with Legacy Code
- Trisha Gee and Helen Scott, Getting to Know IntelliJ IDEA
