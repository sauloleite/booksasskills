# Risks and Automated Governance

## Contents
- The three characteristic risks
- Early-warning checklist for "too big"
- Fitness functions: module membership, coupling budget, forbidden pairs
- Tooling per platform
- Governance under each structural option
- Remediation playbook

## The three characteristic risks

1. **Growing past maintainable size.** A monolith is not a problem in itself; size is. Beyond some point it becomes too slow to change, test and deploy. "Too big" is system-specific, so watch symptoms rather than line counts.
2. **Over-eager code reuse.** Sharing is normal, but heavy sharing across modules smears the boundaries until the system becomes an unstructured monolith whose code cannot be separated.
3. **Excessive inter-module communication.** Some is expected in complex workflows. A lot of it signals that the domains were cut in the wrong places; the fix is to revisit the domain boundaries, not to add more integration code.

## Early-warning checklist for "too big"

Treat two or more of these as a trigger to reassess (split modules, extract a service, or move toward a distributed style):
- [ ] Routine changes take noticeably longer than they used to.
- [ ] Editing one area breaks something in an unrelated area.
- [ ] Developers block each other (merge conflicts, waiting on each other's changes, release queues).
- [ ] Application startup takes long enough to hurt testing and recovery.

Also watch for the reuse and chatter risks:
- [ ] A "shared" or "common" package is imported by most modules and keeps growing.
- [ ] A single feature routinely requires edits in three or more modules.
- [ ] Cross-module call count trends upward release over release.

## Fitness functions

The module is the primary artifact, and it shows up as a namespace, package or directory. That makes boundaries machine-checkable. Three checks cover most needs.

### 1. Module membership
Every source namespace must start with one of the declared module prefixes. Any new top-level folder or namespace outside the list raises an alert, which forces an explicit decision ("is this a new module?") instead of silent sprawl.

Original sketch:

```python
MODULES = ["shop.catalog", "shop.cart", "shop.billing", "shop.shipping"]

def check_membership(namespaces):
    return [ns for ns in namespaces
            if not any(ns == m or ns.startswith(m + ".") for m in MODULES)]
```

### 2. Coupling budget
Count, for each module, references coming in from other modules plus references going out to other modules. Alert when the total exceeds a budget. The right number is subjective and system-specific; the chapter's illustrative ceiling is five coupling points. Start strict, measure the current baseline, and ratchet down rather than letting it creep up.

Counting choices to make explicit:
- Count distinct module-to-module links (good for structure) or distinct file-level references (good for detecting creeping chatter). Record which one you use.
- Exclude references to the module's own sub-namespaces.
- Decide whether a mediator's links count against it (usually report them separately; a mediator is expected to be highly coupled).

### 3. Forbidden pairs
Some modules must never depend on others (for example, a checkout module must not call fulfilment directly, or a reporting module must not write into ordering). Express each rule as "no class in A may access any class in B".

Original sketch in ArchUnit-style Java:

```java
@ArchTest
static final ArchRule cartMustNotTouchBilling =
    noClasses().that().resideInAPackage("..shop.cart..")
        .should().dependOnClassesThat()
        .resideInAPackage("..shop.billing..");
```

## Tooling per platform
- Java: ArchUnit
- .NET: ArchUnitNET, NetArchTest
- Python: PyTestArch
- TypeScript/JavaScript: TSArch
- Anything else: extract a dependency edge list (from imports or a build tool) and check it with a small script, such as `scripts/check_module_boundaries.py` in this skill.

Run checks in CI on every merge so drift is caught when it is cheap to fix.

## Governance under each structural option

| Check | Single code base | Separate module artifacts |
|---|---|---|
| Membership | One scan over the whole tree with the full module list | Run per repository; each one asserts all its code sits under its own module prefix |
| Coupling budget | One global analysis | Needs an assembled view (combine edge lists from each artifact, or analyze the deployable) |
| Forbidden pairs | Easy and highly valuable, since nothing else stops the call | Partly enforced by build dependencies; still worth checking shared-interface artifacts |

## Remediation playbook

| Symptom | First move | If that fails |
|---|---|---|
| Unknown top-level namespace | Decide: new module (add to list) or misplaced code (move it) | Review module catalog with the team |
| Module over coupling budget | Find the top 3 cross-module links; replace direct calls with a facade or mediator | Re-draw the domain boundary; merge or split modules |
| Forbidden dependency appears | Route the interaction through the owning module's public API or the mediator | Question whether the rule or the domain model is wrong |
| Shared code bloating | Push domain-specific helpers back into their module; keep only true infrastructure in shared | Promote the shared part to a platform library with its own owners |
| "Too big" checklist triggered | Split oversized modules; tighten boundaries | Extract the most volatile or scale-sensitive module into a separate service (service-based first) |
