#!/usr/bin/env python3
"""Weighted trade-off worksheet: options x factors, with team-supplied weights.

Purpose
    Turn a qualitative trade-off matrix into a ranked summary that shows which
    factors actually decide the outcome, whether the ranking is fragile, and
    (optionally) how the winner shifts under different context weightings.
    The numbers are a thinking aid for qualitative analysis, not a measurement.

Input (JSON file)
    {
      "options": ["shared library", "shared service"],
      "factors": [
        {"name": "latency", "weight": 3,
         "scores": {"shared library": "high", "shared service": "low"}},
        {"name": "coupling level", "weight": 2, "lower_is_better": true,
         "scores": {"shared library": "high", "shared service": "medium"}}
      ],
      "contexts": {                                   # optional
        "polyglot, weekly rule changes": {"latency": 1, "change agility": 5}
      }
    }
    Scores: numbers 1-5 or labels very low|low|medium|high|very high.
    A score expresses how much of the factor the option has; set
    "lower_is_better": true for factors such as coupling or cost so that
    the scale is inverted before weighting. Weight defaults to 1.
    Context weights override the base weight for the named factors only.

Output
    Text report (default) or JSON (--json): weighted totals per option,
    deciding factors between the top two options, non-discriminating factors,
    single-factor sensitivity (factors whose removal flips the winner), and
    the winner under each context.

Usage
    python3 tradeoff_worksheet.py matrix.json
    python3 tradeoff_worksheet.py matrix.json --json
    python3 tradeoff_worksheet.py matrix.json --top 3
"""
import argparse
import json
import sys

LABELS = {"very low": 1, "low": 2, "medium": 3, "high": 4, "very high": 5}


def parse_score(value, where):
    if isinstance(value, (int, float)):
        num = float(value)
    else:
        key = str(value).strip().lower().replace("_", " ").replace("-", " ")
        if key not in LABELS:
            raise ValueError(f"{where}: unknown score '{value}'")
        num = float(LABELS[key])
    if not 1 <= num <= 5:
        raise ValueError(f"{where}: score {num} outside 1-5")
    return num


def load(path):
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    options = data.get("options") or []
    if len(options) < 2:
        raise ValueError("need at least two options")
    factors = []
    for f in data.get("factors") or []:
        name = f["name"]
        weight = float(f.get("weight", 1))
        if weight < 0:
            raise ValueError(f"factor '{name}': negative weight")
        invert = bool(f.get("lower_is_better", False))
        scores = {}
        for opt in options:
            if opt not in f.get("scores", {}):
                raise ValueError(f"factor '{name}': missing score for '{opt}'")
            raw = parse_score(f["scores"][opt], f"factor '{name}', option '{opt}'")
            scores[opt] = 6 - raw if invert else raw
        factors.append({"name": name, "weight": weight, "scores": scores})
    if not factors:
        raise ValueError("need at least one factor")
    contexts = data.get("contexts") or {}
    names = {f["name"] for f in factors}
    for ctx, weights in contexts.items():
        unknown = set(weights) - names
        if unknown:
            raise ValueError(f"context '{ctx}': unknown factors {sorted(unknown)}")
    return options, factors, contexts


def totals(options, factors, weights=None, skip=None):
    out = {}
    for opt in options:
        s = 0.0
        for f in factors:
            if f["name"] == skip:
                continue
            w = weights.get(f["name"], f["weight"]) if weights else f["weight"]
            s += w * f["scores"][opt]
        out[opt] = s
    return out


def ranking(tot):
    # Ties broken by option name for determinism.
    return sorted(tot, key=lambda o: (-tot[o], o))


def analyse(options, factors, contexts, top):
    tot = totals(options, factors)
    max_total = sum(5 * f["weight"] for f in factors) or 1.0
    order = ranking(tot)
    first, second = order[0], order[1]
    deciding = []
    for f in factors:
        delta = f["weight"] * (f["scores"][first] - f["scores"][second])
        if delta:
            deciding.append({"factor": f["name"], "weighted_delta": delta,
                             "favours": first if delta > 0 else second})
    deciding.sort(key=lambda d: (-abs(d["weighted_delta"]), d["factor"]))
    flat = [f["name"] for f in factors
            if len({f["scores"][o] for o in options}) == 1]
    fragile = []
    for f in factors:
        new_order = ranking(totals(options, factors, skip=f["name"]))
        if new_order[0] != first:
            fragile.append({"factor": f["name"], "new_winner": new_order[0]})
    ctx_results = {}
    for ctx, weights in contexts.items():
        ct = totals(options, factors, weights)
        ctx_results[ctx] = {"winner": ranking(ct)[0],
                            "totals": {o: round(ct[o], 2) for o in options}}
    return {
        "ranking": [{"option": o, "total": round(tot[o], 2),
                     "pct_of_max": round(100 * tot[o] / max_total, 1)}
                    for o in order],
        "margin_top_two": round(tot[first] - tot[second], 2),
        "deciding_factors": deciding[:top],
        "non_discriminating": flat,
        "fragile_on": fragile,
        "contexts": ctx_results,
    }


def render(res):
    lines = ["Ranking (weighted total, % of maximum possible):"]
    for r in res["ranking"]:
        lines.append(f"  {r['option']:<30} {r['total']:>8.2f}  {r['pct_of_max']:>5.1f}%")
    a, b = res["ranking"][0]["option"], res["ranking"][1]["option"]
    lines.append(f"\nMargin between '{a}' and '{b}': {res['margin_top_two']:.2f}")
    lines.append("\nDeciding factors (largest weighted differences, top two options):")
    for d in res["deciding_factors"]:
        lines.append(f"  {d['factor']:<30} {d['weighted_delta']:>+7.2f}  favours {d['favours']}")
    pro_a = [d["factor"] for d in res["deciding_factors"] if d["favours"] == a]
    pro_b = [d["factor"] for d in res["deciding_factors"] if d["favours"] == b]
    lines.append("\nBottom-line question for stakeholders:")
    lines.append(f"  Which matters more: {', '.join(pro_a) or '(none)'} ({a})"
                 f" or {', '.join(pro_b) or '(none)'} ({b})?")
    if res["non_discriminating"]:
        lines.append("\nNon-discriminating factors (same score everywhere, drop to simplify):")
        lines.append("  " + ", ".join(res["non_discriminating"]))
    if res["fragile_on"]:
        lines.append("\nFragile: removing one of these factors changes the winner:")
        for f in res["fragile_on"]:
            lines.append(f"  without {f['factor']}: {f['new_winner']} wins")
    else:
        lines.append("\nRobust: no single factor removal changes the winner.")
    if res["contexts"]:
        lines.append("\nWinner per context (out-of-context check):")
        for ctx, r in res["contexts"].items():
            lines.append(f"  {ctx:<40} -> {r['winner']}  {r['totals']}")
    lines.append("\nReminder: confirm the options are MECE and the scores came from"
                 " domain scenarios, not generic impressions.")
    return "\n".join(lines)


def main(argv=None):
    p = argparse.ArgumentParser(
        description="Rank options in a weighted qualitative trade-off matrix and "
                    "report which factors decide the result.")
    p.add_argument("matrix", help="path to the JSON matrix (see module docstring)")
    p.add_argument("--json", action="store_true", help="emit JSON instead of text")
    p.add_argument("--top", type=int, default=5,
                   help="number of deciding factors to list (default 5)")
    args = p.parse_args(argv)
    try:
        options, factors, contexts = load(args.matrix)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    res = analyse(options, factors, contexts, max(1, args.top))
    print(json.dumps(res, indent=2) if args.json else render(res))
    return 0


if __name__ == "__main__":
    sys.exit(main())
