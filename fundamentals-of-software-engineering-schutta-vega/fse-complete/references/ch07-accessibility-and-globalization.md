# Accessibility, Internationalization, Localization and Culture

## Contents
- Vocabulary
- Why it matters (legal and practical)
- Accessibility: ability categories and checks
- The curb-cut effect
- Internationalization vs localization
- Cultural differences
- Implementation checklist
- Pitfalls

## Vocabulary

- **a11y, i18n, l10n**: numeronyms (first letter, count of omitted letters, last letter) for accessibility, internationalization and localization. Usability, accessibility and inclusion are separate concerns that overlap and must be balanced throughout design, not at the end.
- **Inclusive design**: aiming for the widest feasible set of people across ability, hardware, connectivity and geography.
- **RTL / LTR**: right-to-left (Arabic, Hebrew) and left-to-right scripts; some scripts such as Japanese can also run vertically.

## Why it matters

- Regulation may apply: the Americans with Disabilities Act, Section 508 of the US Rehabilitation Act (federal IT), and the European Accessibility Act. Check which apply to your product and market.
- Retrofitting is costly; designing in from the first sprint is cheap by comparison.
- Unless you build developer tools, the team is probably not representative of users in eyesight, hardware, bandwidth or location.

## Accessibility: ability categories and checks

| Category | Examples | Concrete checks |
|---|---|---|
| Visual | low vision, blindness, color blindness (about 8% of men, 0.4% of women) | screen-reader labels on every control; survives 200% zoom and OS font scaling; color never the sole signal; text contrast at or above WCAG AA (4.5:1 normal, 3:1 large) |
| Auditory | deaf, hard of hearing | captions or transcripts; visual or haptic alternative to every sound alert |
| Dexterity | repetitive strain, motor impairment | full keyboard operation; generous pointer/tap targets; no precision drag as the only path |
| Cognitive | autism, dyslexia, limited literacy | plain language; consistent layout; forgiving input; no time pressure without extension |

Lean on the platform: modern OSes ship assistive features (color filters, live captions, eye tracking, adaptive input hardware) and accessibility APIs. Use native controls and semantic markup so those features work for free.

Run `scripts/contrast_check.py` to verify color pairs against AA and AAA thresholds.

## The curb-cut effect

Features built for disability help everyone, in the way a sidewalk ramp also helps a traveler pulling luggage:
- larger targets help users on bumpy trains and with gloves;
- keyboard shortcuts serve power users as much as people who cannot use a mouse;
- low-bandwidth design serves rural users and anyone drifting in and out of mobile coverage.

Use this argument when accessibility work is being deprioritized as "for a small group".

## Internationalization vs localization

- **i18n is the foundation**: engineering the product so language and cultural conventions can be swapped without code changes. Examples: externalize every user-visible string to resource bundles; use locale-aware formatting for dates, numbers, currency and units; support bidirectional layout; never concatenate translated fragments.
- **l10n is the adaptation**: producing the actual translations, currency symbols, date formats and measurement units for a target market.
- Rule: unless you can guarantee a single locale forever, build i18n in from the start. Any chance of a second market justifies it.
- Plan for text expansion. Translations can be much longer; English to German can grow about 35%. Avoid fixed-width labels and buttons; let containers flex and test with pseudo-localized strings.

Small illustration (Python stdlib) of keeping strings and formats out of code:

```python
import gettext, locale
from datetime import date

def render_due_notice(lang: str, due: date, amount: float) -> str:
    t = gettext.translation("billing", "locales", languages=[lang], fallback=True)
    _ = t.gettext
    locale.setlocale(locale.LC_ALL, f"{lang}.UTF-8")
    return _("Payment of {amount} is due on {due}").format(
        amount=locale.currency(amount, grouping=True),
        due=due.strftime("%x"),  # locale date format, not a hardcoded pattern
    )
```

## Cultural differences

- Mental models differ: something as basic as which direction traffic comes from changes between countries, and UI conventions vary the same way.
- Direction: RTL languages need a mirrored layout, not just translated text.
- Color meaning varies: red signals luck and prosperity in much of East Asia but mourning in South Africa. Do not assume a single meaning for status colors.
- Icons: some audiences prefer literal pictures, others abstract symbols. Legacy metaphors (a floppy disk for Save) mean nothing to people who never used one.
- Gestures, imagery or phrases that are harmless at home can offend elsewhere; review with people from the target market.
- After translation, expect to resize or move elements, not just swap text.

## Implementation checklist

- [ ] Every input has a programmatic label; every icon button has an accessible name.
- [ ] Whole flow completes with keyboard only, with visible focus.
- [ ] Screen-reader pass done on the main journeys.
- [ ] Layout holds at large OS font sizes and small screens.
- [ ] Color contrast meets AA; meaning is also conveyed by text or shape.
- [ ] No sound-only notifications.
- [ ] All strings externalized; dates, numbers and currency locale-formatted.
- [ ] Layout tolerates 35%+ text growth and RTL mirroring.
- [ ] Icons and colors reviewed for target cultures.

## Pitfalls

- Treating accessibility as a release theme to add later.
- Hardcoded labels and date formats "because we only sell in one country".
- Encoding status only in red/green.
- Assuming users share your eyesight, monitor size or connection speed.
