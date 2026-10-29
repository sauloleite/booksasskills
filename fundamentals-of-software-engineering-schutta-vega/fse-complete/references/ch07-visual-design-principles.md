# Visual Design Principles: Contrast, Repetition, Alignment, Proximity

## Contents
- Origin and when to bend the rules
- Contrast
- Repetition
- Alignment
- Proximity
- Applying the four together (review procedure)
- Worked critique
- Glossary

## Origin and when to bend the rules

The four principles come from Robin Williams's *The Non-Designer's Design Book*. Written for print, they transfer directly to screens and let a non-designer produce a coherent layout. Ignoring them hurts usability, not just looks. Experienced designers break them on purpose; match rule-breaking to the product. An irregular layout can suit a marketing campaign; it does not suit a timesheet app.

## Contrast

- Any meaningful difference creates contrast: size, weight, line thickness, color, shape, alignment.
- Make differences strong. Two near-identical grays read as a mistake; clearly different treatments read as intent. Erring toward too much difference beats elements that look almost the same.
- Contrast organizes: a glance should reveal the hierarchy (title, section heading, body). Accidental contrast creates false groupings that confuse.
- Reserve your accent color for the one or two things you want clicked (primary call to action) or noticed.
- Accessibility overlap: color contrast must also meet WCAG ratios; check with `scripts/contrast_check.py`.

## Repetition

- Reuse visual elements consistently: fonts, palette, layout grid, bullet style, header, navigation, separators. At minimum it tells users they are still in the same product; a shifting visual language is disorienting.
- Go beyond "consistent": choose a distinctive element to repeat intentionally (for example a doubled thin rule above every footer) so a region becomes instantly recognizable.
- Repetition builds familiarity, so users learn what they can skip and notice what changed.
- Do not overdo it. A brand color sprinkled everywhere becomes noise and kills its own contrast.
- Across a product family, share structure (search placement, fonts, icon style) but vary one accent so users know which app they are in.

## Alignment

- Nothing goes on the screen merely because space was free; place each element relative to something else.
- Left or right alignment yields crisp edges and a professional look; centered text yields ragged edges and reads worse. Prefer flush alignment except for short, deliberate cases.
- Align images and icons as well as text; alignment visually connects items even when they are far apart.
- Choose one alignment scheme and use it everywhere; consistency makes structure legible.

## Proximity

- Items placed close together are read as related, whether or not they are. Spacing or styling a subset differently makes users hunt for a relationship that may not exist.
- Group related items; separate unrelated ones. Put whitespace between groups to strengthen each group.
- Limit the number of visual groups on a screen; if you count more than about five, regroup or nest (for example, category cards that expand into detail, as in a fitness app that moved from one long badge wall to grouped award categories).
- Placement can encode risk: put dangerous settings in their own distant group (see the destructive-actions guidance).

## Applying the four together (review procedure)

1. Squint test: blur the screen; can you still see the hierarchy and the single primary action? (contrast)
2. Count groups; target five or fewer at the top level. (proximity)
3. Trace vertical edges; each element should sit on a shared line. (alignment)
4. Compare two or three screens side by side; fonts, header, nav, button styles and spacing should match. (repetition)
5. Check that the accent color is rare enough to keep its pull. (contrast vs repetition)
6. Verify text and control contrast ratios.

The chapter illustrates the principles with a content-learning site (big covers and a brand accent for contrast, one highlighted button per page, grouped search and filter blocks, the same font and top menu on every page) and with sibling desktop media apps that share sidebar structure but differ in accent color.

## Worked critique

Original settings page: centered labels, four shades of gray text, eleven controls in a single column with equal spacing, a red "Reset all data" button next to "Save", and a different header font from the rest of the app.

Fixes:
- Alignment: left-align labels and inputs on a common edge.
- Contrast: two text weights (heading, body), one accent for "Save".
- Proximity: split into three groups (Profile, Notifications, Data) separated by whitespace.
- Repetition: reuse the app's standard header and button styles.
- Danger: move "Reset all data" to a separate bottom section, labeled, with confirmation.

## Glossary

- **Visual unit / group**: a cluster the eye reads as one thing because of proximity, repetition or contrast.
- **Squint test**: blurring your view to see only hierarchy and grouping.
- **Accent color**: a sparingly used color reserved for emphasis.
