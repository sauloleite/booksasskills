# Discoverability, Error Messages, Destructive Actions, and Practice

## Contents
- Make the correct path the obvious one
- When hiding a feature is acceptable
- Shortcuts: efficient but forgettable
- Error prevention and error messages
- Destructive actions: deliberate friction
- Practice plan
- Further reading

## Make the correct path the obvious one

- If features sit where nobody expects them, learning slows, and users may conclude the feature does not exist.
- Default to the conventional, obvious design. Choose an unconventional interaction only when it is dramatically better, or when frequent use will make it memorable.
- "So bad it is memorable" is not memorability: an awkward trick is forgotten after a few months away. Discoverable designs are remembered better.
- Prevent wrong input instead of reporting it: correct field types, input masks, inline hints, formatted examples ("MM/YYYY"), visual cues.

### Worked example (pattern from the chapter)

A meeting tool required users to open a secondary "test audio" dialog and tick an obscure "stay connected after test" box to get audio into a recording. Redesign rules applied:
1. Remove the extra dialog; show the audio level meter in the main dialog.
2. If that is not possible, the "include audio" checkbox alone should do what it says.
3. Delete options that exist only to work around the design.

General rule: when a feature needs tribal knowledge or a manual, collapse steps until the label alone explains the action.

## When hiding a feature is acceptable

Not everything fits on screen, especially on mobile. A hidden interaction can be justified when all of these hold:
- the benefit is large and immediately clear once seen;
- it can be taught in seconds and is then remembered (pinch to zoom is the archetype);
- it is actively taught (onboarding, marketing, tutorials);
- the interface remains usable without it.

Once such a gesture becomes a platform convention, failing to support it breaks users' mental models.

## Shortcuts: efficient but forgettable

- Keyboard shortcuts are essential for expert efficiency, but only the most frequent ones become habit.
- Make the rest discoverable:
  - show the shortcut next to each menu item so menu use teaches it;
  - provide a command palette or "find action" search over all commands;
  - optionally nudge users who repeatedly use the slow path.
- Searchable help or menus let users find commands by name.

## Error prevention and error messages

Users will leave the happy path. How the product responds largely determines perceived usability.

A good error message:
1. says what happened in the user's terms (not an internal code or class name);
2. explains the likely cause;
3. offers a next step or alternative;
4. recovers automatically where safe (retry with backoff) while still offering a manual action;
5. preserves the user's work;
6. carries enough correlation detail (hidden or secondary) for support and debugging.

Also provide undo or revert. People explore only when mistakes are reversible.

Template:

```text
Title:   Can't reach the server
Body:    Your changes are saved on this device. We'll retry in 30 seconds.
Actions: [Retry now]  [Work offline]
Detail:  (collapsed) ref 7F3A-21, 14:02 UTC
```

Anti-patterns: raw exception text, "Something went wrong" with no action, clearing a form on a validation error, irreversible side effects triggered by a typo.

## Destructive actions: deliberate friction

The "make it easy" rule inverts for irreversible actions (deleting an account, repository, or dataset). Add steps. The repository-deletion flow of a popular code-hosting site shows the layered pattern:

1. **Placement**: dangerous settings live at the bottom of the page in a separate, clearly titled danger section (proximity), so they cannot be hit by accident.
2. **Signal**: red accents on those controls (contrast).
3. **Specific labels**: buttons name the full action and object, never a bare "Delete" or "OK".
4. **Explain consequences**: a confirmation step states what will be lost and that it cannot be undone.
5. **Typed confirmation**: the final button stays disabled until the user types the resource name.

Calibrate: use the full ladder only for rare, high-impact, irreversible operations. Reversible edits should stay frictionless; prefer soft delete plus undo where feasible.

```python
def can_confirm_delete(resource_name: str, typed: str, acknowledged: bool) -> bool:
    # Final button enabled only after explicit acknowledgment and exact name match
    return acknowledged and typed.strip() == resource_name
```

## Practice plan

Own-words exercises derived from the chapter's closing advice:
- Pick an app you use daily; annotate one screen for each of contrast, repetition, alignment and proximity.
- Time-box an hour to find principle violations across apps on your phone or laptop, and note your fix for each.
- Audit an app you built: list usability problems by quality component, then spend an hour sketching a redesign.
- Shadow real users at their workplace; log what works, what frustrates, which defaults they change and which flows cost too many steps. Ask what they would change.

## Further reading

- Norman, *The Design of Everyday Things*
- Williams, *The Non-Designer's Design Book*
- Cooper et al., *About Face*
- Tidwell et al., *Designing Interfaces*
- Edward Tufte's books on information display
