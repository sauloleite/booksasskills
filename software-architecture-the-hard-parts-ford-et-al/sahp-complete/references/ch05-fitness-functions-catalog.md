# Fitness Functions for Governing Decomposition

## Contents
- Why governance is part of every pattern
- Common design rules
- Catalog by pattern
- Original example snippets
- Pitfalls

## Why governance is part of every pattern

A monolith under migration keeps changing: features and fixes land while the architects are restructuring it. Without automated checks, new components appear unnoticed, sizes drift, orphaned code creeps back into root namespaces and forbidden dependencies return. Each decomposition pattern is therefore paired with automated, holistic fitness functions that run in the CI/CD pipeline (typically on deployment) and alert the architect when a constraint breaks. An alert is a prompt for a conversation with the team and often results in a new architecture story.

## Common design rules

- Implement with custom code, open source tools (ArchUnit for JVM, NetArchTest for .NET, import-linter or custom AST scans for Python, dependency-cruiser for JavaScript) or commercial analyzers.
- Derive components automatically by walking the source tree and treating each directory path or namespace that holds code as a candidate component.
- Persist state (last known inventory, exclusion lists) in a small store so checks can compare runs and suppress known false positives.
- One rule per check. For dependency restrictions, write one check per forbidden pair so each failure has a clear owner and message.
- Thresholds are per codebase. Choose them from the current distribution and tighten over time.
- Prefer alerting the architect for subjective checks (common domain logic) and failing the build for objective ones (code in a root namespace, forbidden dependency, domain prefix violation).

## Catalog by pattern

**Identify and Size Components**
1. *Inventory drift.* Compare the current set of component namespaces to the stored set; record and report additions and removals. Other patterns depend on an accurate inventory, so this one is foundational.
2. *Maximum share of the codebase.* Alert when any component exceeds a set percentage of total statements. Scale the limit to component count (around 30 percent for a ten-component system, around 10 percent for fifty components).
3. *Maximum distance from the mean.* Alert when any component's size is more than a set number of sample standard deviations from the mean (3 is a stable governance default; 2 is useful during active analysis).

**Gather Common Domain Components**
4. *Repeated leaf names.* Alert when two or more component namespaces end in the same node (for example, several `.audit` leaves), excluding names on a stored allow list such as `.validate` or `.calculate`.
5. *Shared source files.* Alert when the same source file (or class) is used by more than one component, again filtered by an exclusion list. Noisy but useful as a prompt for manual review. These two checks are inherently advisory because classifying logic as domain or infrastructure requires judgment.

**Flatten Components**
6. *No code in root namespaces.* Fail when any namespace that has child namespaces also contains source files. Especially valuable during ongoing maintenance of the monolith while migration is underway.

**Determine Component Dependencies**
7. *Maximum total coupling.* Alert when a component's CA plus CE exceeds a threshold (15 is high for most applications). Variants: separate limits for incoming only or outgoing only. The limit depends on component count and current coupling.
8. *Forbidden dependency.* Fail when component X references component Y where the architecture says it must not. Write one check per restriction.

**Create Component Domains**
9. *Approved domain list.* Fail when code appears under a top-level namespace node that is not in the approved list of domains. Prevents teams from inventing domains without review.

**Create Domain Services**
10. *Domain prefix per service.* For each domain service, fail when any class does not reside under that domain's namespace prefix. Keeps each service aligned and splittable later.

## Original example snippets

Inventory drift and orphan detection in one pass (Python, directory-based components):

```python
import json, os, pathlib

SRC_EXT = {".java", ".cs", ".py", ".ts", ".go"}

def scan(root):
    """Return {namespace: has_code} for every directory under root."""
    out = {}
    for d, subdirs, files in os.walk(root):
        ns = ".".join(pathlib.Path(d).relative_to(root).parts)
        if ns:
            out[ns] = any(pathlib.Path(f).suffix in SRC_EXT for f in files)
    return out

def check(root, state_file):
    nodes = scan(root)
    current = {n for n, code in nodes.items() if code}
    prior = set(json.load(open(state_file))) if os.path.exists(state_file) else current
    roots = {n for n in nodes if any(m.startswith(n + ".") for m in nodes)}
    json.dump(sorted(current), open(state_file, "w"))
    return {"added": sorted(current - prior), "removed": sorted(prior - current),
            "orphans": sorted(n for n in current if n in roots)}
```

Forbidden dependency and domain prefix as Python import-linter contracts (config, not code):

```ini
[importlinter]
root_package = clinic

[importlinter:contract:scheduling-not-billing]
name = Scheduling must not import Billing
type = forbidden
source_modules = clinic.scheduling
forbidden_modules = clinic.billing

[importlinter:contract:domains-independent]
name = Domains stay independent of each other
type = independence
modules = clinic.patient
          clinic.scheduling
          clinic.billing
```

For an approved domain list, a simple check lists the second namespace node of every source file and fails on any value outside the allowed set. The sizing and percentage checks can reuse `scripts/component_sizing.py` with `--fail-on-flags` in the pipeline.

## Pitfalls

- Writing checks once the migration is "done" instead of right after each pattern is applied.
- Failing the build on inherently subjective checks, which teaches teams to ignore them.
- No exclusion lists, so the same false positive fires on every build.
- A single catch-all dependency rule that obscures which constraint broke.
- Static thresholds that are never revisited as the component count changes.
