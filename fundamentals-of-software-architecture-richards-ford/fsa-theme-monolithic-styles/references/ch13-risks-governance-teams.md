# Risks, Governance and Team Topology

## Contents
- Root cause of most failures
- Risk: volatile core
- Risk: plug-in dependencies
- Governance fitness functions
- Team topology mapping
- Review questions

## Root cause of most failures

Most problems with this style come from applying it where it does not fit or drifting away from its rules after launch. Governance therefore checks adherence to the philosophy (stable core, isolated plug-ins) more than code-level details.

## Risk: volatile core

The core is meant to settle down after initial development so that change concentrates in plug-ins. A core under constant modification erases the main benefit, and this is a frequent mistake, usually caused by misjudging which functionality is stable.

Symptoms:
- Most change requests or commits touch core modules.
- New variants require core edits beyond a registry entry.
- Variant-specific conditionals reappear inside the core.

Remedies:
- Refactor: move the moving parts out into new plug-in domains, or shrink the core to a true happy path.
- If the "core" is inherently volatile, step back along the spectrum (core plus optional plug-ins) or reconsider the style.

## Risk: plug-in dependencies

Plug-ins should talk only to the core. Most plug-in-capable systems keep plug-ins dependency-free (they depend on the core alone). Complex platforms sometimes allow inter-plug-in dependencies, which makes the core responsible for resolving transitive dependencies and version conflicts, for example two plug-ins requiring different versions of the same library. This is a well-known source of pain.

Guidance:
- Default rule: no plug-in depends on another plug-in.
- If two plug-ins need the same capability, promote it into the core (if stable) or duplicate it.
- If dependencies are unavoidable, the core needs explicit dependency resolution and version isolation; budget for it.

## Governance fitness functions

Checks the chapter points toward, with implementation ideas:

| Check | What it guards | How to automate (ideas) |
|---|---|---|
| Core volatility | stable core | measure commit churn on core paths from version-control history, not from code inspection; alert above an agreed share of total churn |
| Core rate of change | stable core over time | track trend of core-touching commits per release; flag sustained increases |
| Contract tests | plug-ins honoring the domain contract, including plug-ins on older contract versions during gradual evolution | consumer-driven or schema tests run per plug-in against each supported contract version |
| Structural rules | topology | dependency rules: plug-in packages may import only the core API; no plug-in-to-plug-in imports; no plug-in access to the shared database driver |

Original sketch of a churn fitness function (Python, run in CI against `git log --numstat` output):

```python
def core_churn_ratio(numstat_lines, core_prefix="src/core/"):
    core = total = 0
    for line in numstat_lines:
        parts = line.split("\t")
        if len(parts) != 3 or not parts[0].isdigit():
            continue
        changed = int(parts[0]) + int(parts[1])
        total += changed
        if parts[2].startswith(core_prefix):
            core += changed
    return core / total if total else 0.0

# Fail the build if the core absorbed more than, say, 20% of recent churn.
```

The threshold is a team decision, not a number from the book.

## Team topology mapping

The topology suggests a core vs plug-in split:
- **Stream-aligned teams**: own the core functionality; may also own plug-ins depending on the application.
- **Enabling teams**: benefit because behavior isolated in plug-ins supports A/B testing and other experiments without disturbing the core.
- **Complicated-subsystem teams**: a good match, since specialized processing (analytics, pricing science, ML scoring) can live in plug-ins built by specialists while the core team just calls them.
- **Platform teams**: handle operational concerns, much as for any monolith.

## Review questions (original)

1. Which share of the last quarter's changes touched the core, and is that trending down?
2. Can a new variant be added with only a new plug-in and a registry entry?
3. Does any plug-in import another plug-in or read the shared schema?
4. Is there a single contract per plug-in domain, and are third-party plug-ins wrapped by adapters?
5. If plug-ins are remote, what happens to a user request when one plug-in is down?
6. Would the system need independent scaling of the main flow within the next two years?
