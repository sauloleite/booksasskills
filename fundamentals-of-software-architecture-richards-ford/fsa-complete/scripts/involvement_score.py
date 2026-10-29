#!/usr/bin/env python3
"""Elastic-leadership involvement calculator (FSA Chapter 24 five-factor scale).

Purpose
-------
Scores how involved an architect should be with one development team, using
the five factors the chapter names: team familiarity, team size, overall
experience, project complexity and project duration. Each factor sits on a
fixed scale from -20 (less involvement, the armchair extreme) to +20 (more
involvement, the control-freak extreme). The sum points to a leadership stance.

Inputs
------
Each factor accepts either a keyword or a number in [-20, 20]:
    more / high      -> +20
    less / low       -> -20
    neutral / mixed  ->   0
Factors (all optional, omitted factors count as 0 and are reported):
    --familiarity   how new the team is to each other (new team = more)
    --size          rating, or use --team-size N to derive it
    --experience    junior-heavy = more, senior-heavy = less
    --complexity    complex = more, simple = less
    --duration      rating, or use --duration-months M to derive it
Derivation helpers (heuristics consistent with the chapter's examples, not
rules from the book; override them by passing the rating directly):
    --team-size N        N <= 5 -> -20, N >= 12 -> +20, linear in between
    --duration-months M  M <= 6 -> -20, M >= 24 -> +20, linear in between
Optional weights, e.g. --weights experience=2,complexity=1.5 (default 1 each).

Outputs
-------
A table of factor ratings, the raw weighted total, the total normalized to the
-100..+100 range of the unweighted scale, a recommended stance, and, when
--team-size is given, the pairwise communication-channel count n(n-1)/2
(Brooks's standard formula, given as context for process-loss discussions).
Use --json for machine-readable output. Stdlib only, deterministic, no network.
"""
import argparse
import json
import sys

FACTORS = ["familiarity", "size", "experience", "complexity", "duration"]
KEYWORDS = {"more": 20, "high": 20, "less": -20, "low": -20, "neutral": 0, "mixed": 0}

BANDS = [
    (-60, "Hands-off facilitator: answer questions, check direction, otherwise stay out of the way."),
    (-1, "Light-touch facilitator: periodic check-ins, unblock, guard the boundaries."),
    (39, "Mentor and coach: regular day-to-day presence, teach and guide without dictating design."),
    (100, "Heavily involved: close guidance and frequent reviews; still leave class-level design to developers."),
]


def parse_rating(text, name):
    key = text.strip().lower()
    if key in KEYWORDS:
        return float(KEYWORDS[key])
    try:
        value = float(key)
    except ValueError:
        raise SystemExit(f"error: {name} must be more/less/neutral or a number, got {text!r}")
    if not -20 <= value <= 20:
        raise SystemExit(f"error: {name} must be within -20..20, got {value}")
    return value


def interpolate(x, low, high):
    if x <= low:
        return -20.0
    if x >= high:
        return 20.0
    return -20.0 + 40.0 * (x - low) / (high - low)


def parse_weights(text):
    weights = {f: 1.0 for f in FACTORS}
    if not text:
        return weights
    for part in text.split(","):
        name, _, val = part.partition("=")
        name = name.strip()
        if name not in weights:
            raise SystemExit(f"error: unknown factor in --weights: {name!r}")
        try:
            weights[name] = float(val)
        except ValueError:
            raise SystemExit(f"error: bad weight for {name}: {val!r}")
        if weights[name] < 0:
            raise SystemExit(f"error: weight for {name} must be >= 0")
    return weights


def stance(normalized):
    for upper, text in BANDS:
        if normalized <= upper:
            return text
    return BANDS[-1][1]


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0],
                                formatter_class=argparse.RawDescriptionHelpFormatter,
                                epilog="Example: %(prog)s --familiarity more --team-size 4 "
                                       "--experience less --complexity less --duration-months 2")
    for f in FACTORS:
        p.add_argument(f"--{f}", help="more | less | neutral | number in [-20, 20]")
    p.add_argument("--team-size", type=int, help="headcount; derives --size if not given")
    p.add_argument("--duration-months", type=float, help="derives --duration if not given")
    p.add_argument("--weights", help="comma list factor=weight, e.g. experience=2")
    p.add_argument("--json", action="store_true", help="emit JSON")
    a = p.parse_args(argv)

    ratings, sources = {}, {}
    for f in FACTORS:
        raw = getattr(a, f)
        if raw is not None:
            ratings[f], sources[f] = parse_rating(raw, f), "given"
        else:
            ratings[f], sources[f] = 0.0, "omitted"
    if a.size is None and a.team_size is not None:
        if a.team_size < 1:
            raise SystemExit("error: --team-size must be >= 1")
        ratings["size"], sources["size"] = interpolate(a.team_size, 5, 12), f"derived from {a.team_size} people"
    if a.duration is None and a.duration_months is not None:
        if a.duration_months <= 0:
            raise SystemExit("error: --duration-months must be > 0")
        ratings["duration"] = interpolate(a.duration_months, 6, 24)
        sources["duration"] = f"derived from {a.duration_months:g} months"

    weights = parse_weights(a.weights)
    total = sum(ratings[f] * weights[f] for f in FACTORS)
    max_abs = 20.0 * sum(weights.values())
    normalized = 0.0 if max_abs == 0 else 100.0 * total / max_abs
    result = {
        "factors": {f: {"rating": round(ratings[f], 2), "weight": weights[f], "source": sources[f]} for f in FACTORS},
        "total": round(total, 2),
        "normalized_-100_to_100": round(normalized, 2),
        "stance": stance(normalized),
        "omitted": [f for f in FACTORS if sources[f] == "omitted"],
    }
    if a.team_size is not None:
        result["communication_channels"] = a.team_size * (a.team_size - 1) // 2

    if a.json:
        print(json.dumps(result, indent=2))
        return 0
    print(f"{'factor':<12} {'rating':>7} {'weight':>6}  source")
    for f in FACTORS:
        r = result["factors"][f]
        print(f"{f:<12} {r['rating']:>7.1f} {r['weight']:>6g}  {r['source']}")
    print(f"total (weighted): {result['total']:g}")
    print(f"normalized score: {result['normalized_-100_to_100']:g} on -100 (armchair) .. +100 (control freak)")
    print(f"stance: {result['stance']}")
    if result["omitted"]:
        print(f"note: omitted factors counted as 0: {', '.join(result['omitted'])}")
    if "communication_channels" in result:
        print(f"pairwise communication channels: {result['communication_channels']}")
    print("reminder: re-score as the project evolves; involvement is not fixed at kickoff.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
