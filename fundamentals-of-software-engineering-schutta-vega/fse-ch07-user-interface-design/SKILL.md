---
name: fse-ch07-user-interface-design
description: UI design guidance for software engineers: usability quality components and how to prioritize them by usage context, accessibility, i18n/l10n and culture, user research and safe defaults, contrast/repetition/alignment/proximity, discoverability, error messages and friction for destructive actions. Based on Chapter 7 of Schutta and Vega's "Fundamentals of Software Engineering". Use when building or reviewing a screen, form, dialog or settings page, writing error messages, designing delete flows, choosing defaults, checking color contrast, or planning accessibility and localization.
---

# User Interface Design (Schutta and Vega, Ch. 7)

Purpose: help an engineer without design training ship interfaces that their real users can operate easily, including users with different abilities, languages, devices and environments. The chapter's position is that a few principles, applied deliberately and early, separate a usable product from a hostile one; usability is not a specialist-only concern and is costly to retrofit. Apply the rules below directly; open a reference for checklists, worked examples and detail.

## Key decision rules

Users and context
- You are not the user (unless building developer tools). Replace assumptions with quick research: ask about skill, abilities, devices, frequency, location, noise, stress, turnover and training; shadow a few real users for a few days if possible.
- Count secondary users: people waiting while an operator uses your app also bear its slowness.
- A captive internal audience is not an excuse for poor usability.
- Test what users plausibly do, such as enlarging fonts or zooming, especially where content order or length varies.

Prioritizing usability qualities (learnability, efficiency, memorability, discoverability, error handling, satisfaction, accessibility)
- Never optimize all seven equally; let frequency and context decide.
- All-day or complex tools: favor efficiency, memorability, satisfaction; some less discoverable power features are fine.
- Casual or competitive consumer apps: favor learnability and discoverability.
- Rarely used apps: learnability and discoverability over memorability; trade a little efficiency for clarity.
- High-volume work: tiny per-task savings multiply (time saved x tasks x users).
- Training is never a substitute for a usable design.

Inclusion
- Build accessibility, i18n and l10n in from the start; retrofitting is far more expensive. Check legal obligations (ADA, Section 508, European Accessibility Act).
- Cover visual, auditory, dexterity and cognitive needs: labels for screen readers, keyboard-only paths, large targets, no sound-only or color-only signals, plain language. Use platform accessibility APIs.
- Accessibility benefits everyone (curb-cut effect): shortcuts help experts, low bandwidth helps mobile users.
- i18n = externalized strings, locale formats, RTL support; l10n = the per-market translation and formats. Unless one locale is guaranteed forever, do i18n now. Budget for roughly 35% text growth (English to German).
- Colors, icons and metaphors carry cultural meaning; expect layout changes after translation.

Defaults
- Do not guess defaults: ask and test; instrument the UI (telemetry, simple thumbs feedback) and evolve from data.
- Remember user changes across sessions.
- Defaults must be safe; never pre-select a destructive, irreversible option.

Visual design (contrast, repetition, alignment, proximity)
- Contrast: make differences bold, not subtle; use it to show hierarchy and the single primary action.
- Repetition: reuse fonts, colors, layout and a signature element; do not flood the UI with the brand color.
- Alignment: place every element against an edge of something else; prefer flush left/right over centered; one scheme throughout.
- Proximity: group related, separate unrelated, whitespace between groups, about five groups max per view.
- Break these rules only on purpose and only where the product type allows it.

Discoverability, errors, destructive actions
- Stick with obvious, conventional interactions unless the alternative is radically better; discoverable designs are also more memorable.
- Hide a feature only if it is high-benefit, learnable in seconds, actively taught, and the UI works without it.
- Make shortcuts discoverable: show them in menus, add command search.
- Prevent errors first (field types, masks, hints, examples). Error messages say what happened, why, and what to do; retry automatically where safe while offering a manual action; preserve work; support undo.
- Irreversible actions get deliberate friction: isolated danger section, warning color, labels naming the exact action, a consequence warning, typed confirmation of the resource name.

## Default workflow

1. Identify primary and secondary users and their environment; write constraints from the question bank.
2. Rank the usability qualities for this product's usage pattern.
3. Set inclusion baselines: accessibility checks, i18n scaffolding, cultural review.
4. Lay out screens with the four visual principles; run the squint and group-count checks; verify color contrast with the script.
5. Make key paths obvious; add shortcut discovery; constrain inputs.
6. Write error states and recovery; add friction ladders for irreversible actions; confirm defaults are safe and persisted.
7. Ship telemetry and feedback, observe real users, and iterate on defaults and flows.

## References

- [references/usability-qualities-and-prioritization.md](references/usability-qualities-and-prioritization.md): read when auditing usability or deciding which qualities to optimize for a product's usage pattern; includes the efficiency multiplier example.
- [references/accessibility-and-globalization.md](references/accessibility-and-globalization.md): read when planning or reviewing accessibility, localization, internationalization, RTL support or cultural fit.
- [references/user-research-and-defaults.md](references/user-research-and-defaults.md): read when gathering user requirements, considering secondary users, or choosing, persisting and instrumenting defaults.
- [references/visual-design-principles.md](references/visual-design-principles.md): read when laying out or critiquing a screen's visual hierarchy, grouping, alignment and consistency.
- [references/discoverability-errors-and-destructive-actions.md](references/discoverability-errors-and-destructive-actions.md): read when deciding what to expose or hide, designing shortcuts, writing error messages, building delete or other irreversible flows, or setting practice exercises.
- [references/source-map.md](references/source-map.md): read to find which reference covers a given chapter section.

## Scripts

- Run `python3 scripts/contrast_check.py "#767676:#ffffff" "#777:#fff"` to compute WCAG relative luminance, contrast ratio, and AA/AAA pass/fail (normal text, large text, UI components) for each foreground:background pair.
- Run `python3 scripts/contrast_check.py --file pairs.csv --strict` to check a palette file (one `fg,bg[,label]` per line); exits 1 if any pair fails AA for normal text, useful in CI. Add `--json` for machine-readable output.
