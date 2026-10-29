# Knowing Your Users and Choosing Defaults

## Core stance

- Usable software requires knowing the audience and the setting where they work. Lightweight research (a handful of questions, a few days of observation) captures most of the value; months of fieldwork are rarely needed.
- Challenge every assumption about users. Stereotypes are cheap shortcuts that produce avoidable errors (the chapter's anecdote: retirees assumed to ignore donated computers wore out the keyboards keeping in touch with family).
- You are not your user, unless the product is a developer tool. What is obvious to you, or looks fine on your large monitor, may fail for someone else.

## Discovery question bank

Ask these before designing; record answers as explicit design constraints.

- Technology fluency and operating systems in use.
- Functional limitations; behavior with screen readers, enlarged fonts, changed resolution.
- Devices: phone, tablet, laptop, headset, TV, several of these.
- Expected education and reading level.
- Turnover: stable expert population or constant newcomers?
- Frequency of use.
- Physical location: desk, home, couch, outdoors, vehicle.
- Environment: noisy, quiet, high-stress.
- Will users be trained, or will they never open the manual?

### Turning answers into design decisions

| Finding | Design response |
|---|---|
| Loud environment | Do not rely on sound; add visual or vibration alerts |
| No training, no manual | Make the easy path the correct path; constrain input (numeric fields accept only digits) |
| Field use on rugged tablets | Large targets, glare-tolerant contrast, offline tolerance |
| High turnover | Favor learnability and discoverability |
| All-day expert use | Favor efficiency and shortcuts |

## Observation

Whenever possible, shadow representative users in their real setting. Watching a few people work for a couple of days routinely reveals problems no spec review will. Ask what they like, dislike and would change.

## Secondary users

Many systems are operated on someone else's behalf: call-center agents, service schedulers, bank tellers. The person waiting is the secondary user. A slow or click-heavy flow (one scheduler counted 11 clicks to book a returning customer whose data was already on file) wastes the operator's time and damages the customer's view of your organization. Include the secondary user's wait time and experience in requirements.

## Test what users really do

Users will do reasonable things you never tried. In the chapter's polling story, call-center staff enlarged the font; randomized candidate order then pushed some names off-screen, the poll had to be discarded and the pollster's reputation suffered. Lesson: test the layout under font scaling, zoom and small windows, especially when content order or count varies.

## Defaults

Defaults are powerful because most people never change them.

Rules:
1. Do not guess defaults; ask customers and, better, test with them. A customer who immediately changes every default is telling you the defaults are wrong.
2. For new products without usage history, add telemetry to the UI (feature usage, setting changes) and even a simple thumbs up/down feedback control, then evolve defaults from data rather than hunches.
3. Persist user changes. Never silently reset a preference on the next launch.
4. Make defaults safe. When users are stressed, rushed or habituated to click through dialogs, the pre-selected option must never be destructive or irreversible. Here added friction is good.

Small sketch of safe, persisted defaults:

```python
DEFAULTS = {"export_format": "csv", "confirm_before_delete": True}

def effective_settings(user_prefs: dict) -> dict:
    merged = {**DEFAULTS, **user_prefs}      # user choices always win
    merged["confirm_before_delete"] = True   # safety default is not user-removable
    return merged

def on_setting_changed(store, user_id, key, value):
    store.save(user_id, key, value)          # remembered across sessions
    store.emit_event("setting_changed", key=key)  # telemetry for tuning defaults
```

## Culture as part of knowing users

Mental models, reading direction, color meaning and icon style differ by culture (details in the accessibility and globalization reference). Investigating these early avoids designs that feel hostile; first impressions are hard to repair, and simply listening to users earns lasting goodwill.

## Pitfalls

- Designing for yourself or your team's hardware.
- Treating "users are required to use it" as permission to ignore satisfaction.
- Shipping defaults chosen by the developer's convenience.
- Skipping research because it seems slow; basic research repays itself many times.
