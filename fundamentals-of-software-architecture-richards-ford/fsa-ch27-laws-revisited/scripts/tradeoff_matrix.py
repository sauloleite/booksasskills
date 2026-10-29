#!/usr/bin/env python3
"""Weighted trade-off matrix (FSA Chapter 27: contextual weighting of trade-offs).

Input: a CSV file (or '-' for stdin) with a header row
    factor,weight,<option1>,<option2>[,...]
and one row per factor. 'weight' is a non-negative number elicited from
stakeholders (blank means 1). Option cells hold '+' (factor favors the option),
'-' (factor counts against it) or '0' / blank (neutral). Lines starting with '#'
are ignored.

Output: for each option, the unweighted tally (+count, -count, net) and the
weighted score (sum of +weight and -weight). Reports the raw winner and the
weighted winner, and warns when they differ (the weights changed the answer,
so the weights must be justified and recorded; ignoring them is the Out of
Context antipattern). Also lists the factors that contributed most to the
weighted gap between the top two options. Use --json for machine output.
Exit code 0 on success, 2 on input errors. Deterministic, stdlib only.
"""
import argparse
import csv
import json
import sys

SYMBOLS = {"+": 1, "-": -1, "0": 0, "": 0}


def load(path):
    fh = sys.stdin if path == "-" else open(path, newline="", encoding="utf-8")
    try:
        rows = [r for r in csv.reader(fh) if r and not r[0].lstrip().startswith("#")]
    finally:
        if fh is not sys.stdin:
            fh.close()
    if len(rows) < 2:
        raise ValueError("need a header row and at least one factor row")
    header = [h.strip() for h in rows[0]]
    if len(header) < 4 or [h.lower() for h in header[:2]] != ["factor", "weight"]:
        raise ValueError("header must be: factor,weight,<option1>,<option2>[,...]")
    options = header[2:]
    factors = []
    for n, row in enumerate(rows[1:], start=2):
        row = [c.strip() for c in row] + [""] * (len(header) - len(row))
        w_txt = row[1] or "1"
        try:
            weight = float(w_txt)
        except ValueError:
            raise ValueError(f"row {n}: weight '{w_txt}' is not a number")
        if weight < 0:
            raise ValueError(f"row {n}: weight must be non-negative")
        marks = []
        for opt, cell in zip(options, row[2:2 + len(options)]):
            if cell not in SYMBOLS:
                raise ValueError(f"row {n}, option '{opt}': use +, - or 0, got '{cell}'")
            marks.append(SYMBOLS[cell])
        factors.append({"factor": row[0], "weight": weight, "marks": marks})
    return options, factors


def winner(scores):
    best = max(scores.values())
    tops = sorted(k for k, v in scores.items() if v == best)
    return tops[0] if len(tops) == 1 else "tie: " + ", ".join(tops)


def analyze(options, factors):
    result = {"options": {}, "factors": len(factors)}
    for i, opt in enumerate(options):
        plus = sum(1 for f in factors if f["marks"][i] > 0)
        minus = sum(1 for f in factors if f["marks"][i] < 0)
        weighted = sum(f["weight"] * f["marks"][i] for f in factors)
        result["options"][opt] = {"plus": plus, "minus": minus,
                                  "net": plus - minus, "weighted": round(weighted, 4)}
    raw = {o: v["net"] for o, v in result["options"].items()}
    wtd = {o: v["weighted"] for o, v in result["options"].items()}
    result["raw_winner"] = winner(raw)
    result["weighted_winner"] = winner(wtd)
    result["flip"] = result["raw_winner"] != result["weighted_winner"]
    ranked = sorted(options, key=lambda o: (-wtd[o], o))
    a, b = ranked[0], ranked[1]
    ia, ib = options.index(a), options.index(b)
    drivers = sorted(((f["weight"] * (f["marks"][ia] - f["marks"][ib]), f["factor"])
                      for f in factors), key=lambda t: (-t[0], t[1]))
    result["top_two"] = [a, b]
    result["drivers"] = [{"factor": name, "contribution": round(c, 4)}
                         for c, name in drivers if c > 0][:5]
    return result


def report(res):
    lines = [f"Factors: {res['factors']}",
             f"{'Option':<24}{'+':>4}{'-':>4}{'net':>6}{'weighted':>11}"]
    for opt, v in res["options"].items():
        lines.append(f"{opt:<24}{v['plus']:>4}{v['minus']:>4}{v['net']:>6}{v['weighted']:>11g}")
    lines.append(f"Raw winner: {res['raw_winner']}")
    lines.append(f"Weighted winner: {res['weighted_winner']}")
    if res["flip"]:
        lines.append("WARNING: weighting changes the answer. Justify and record the weights "
                     "in the ADR; a raw count alone would be out of context.")
    a, b = res["top_two"]
    if res["drivers"]:
        tied = res["options"][a]["weighted"] == res["options"][b]["weighted"]
        suffix = " (weighted scores tied)" if tied else ""
        lines.append(f"Main factors favoring {a} over {b}{suffix}:")
        lines += [f"  {d['factor']}: +{d['contribution']:g}" for d in res["drivers"]]
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("csv", help="CSV path, or '-' for stdin")
    p.add_argument("--json", action="store_true", help="emit JSON instead of text")
    args = p.parse_args()
    try:
        options, factors = load(args.csv)
    except (OSError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    res = analyze(options, factors)
    print(json.dumps(res, indent=2) if args.json else report(res))
    return 0


if __name__ == "__main__":
    sys.exit(main())
