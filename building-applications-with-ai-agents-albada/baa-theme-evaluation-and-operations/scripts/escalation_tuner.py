#!/usr/bin/env python3
"""Tune human-in-the-loop escalation thresholds from historical agent decisions.

Risk score per case = (1 - certainty) * consequence weight. A case is escalated
when its risk exceeds a threshold, or when certainty falls below a hard floor,
or when its severity is in the always-escalate set. The script sweeps
thresholds and reports, for each, the escalation rate (human load) and, when
ground-truth labels exist, how many agent errors would have reached a human.

Input CSV columns (header required):
  certainty   agent self-reported or derived confidence in [0, 1]
  severity    label such as low / medium / high / critical
  correct     optional, 1 if the agent's decision was right, 0 if wrong
Options:
  --weights   severity=weight pairs (default low=1,medium=2,high=4,critical=8)
  --floor     escalate anything with certainty below this (default 0, off)
  --always    comma list of severities that always escalate (default none)
  --budget    max acceptable escalation rate (default 0.10)
Output: threshold sweep table and the lowest threshold within budget
(lower threshold = more escalation = more errors caught).

Standard library only, deterministic, no network.
Example:
  python3 escalation_tuner.py cases.csv --budget 0.10 --always critical
"""
import argparse
import csv


def load(path):
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows or "certainty" not in rows[0] or "severity" not in rows[0]:
        raise SystemExit("error: CSV needs certainty and severity columns")
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv")
    ap.add_argument("--weights", default="low=1,medium=2,high=4,critical=8")
    ap.add_argument("--floor", type=float, default=0.0)
    ap.add_argument("--always", default="")
    ap.add_argument("--budget", type=float, default=0.10)
    ap.add_argument("--steps", type=int, default=20)
    args = ap.parse_args()

    weights = {k.strip(): float(v) for k, v in
               (p.split("=") for p in args.weights.split(",") if p)}
    always = {s.strip() for s in args.always.split(",") if s.strip()}
    rows = load(args.csv)
    has_label = "correct" in rows[0] and all(r["correct"] != "" for r in rows)
    cases = []
    for r in rows:
        sev = r["severity"].strip()
        if sev not in weights:
            raise SystemExit(f"error: severity '{sev}' missing from --weights")
        c = float(r["certainty"])
        risk = (1 - c) * weights[sev]
        forced = c < args.floor or sev in always
        wrong = has_label and r["correct"].strip() == "0"
        cases.append((risk, forced, wrong))

    n = len(cases)
    errors = sum(w for _, _, w in cases)
    top = max(r for r, _, _ in cases) or 1.0
    print(f"cases={n}  errors={errors if has_label else 'n/a'}  budget={args.budget:.0%}")
    print(f"{'threshold':>10}{'escalated':>11}{'rate':>8}{'errors caught':>15}{'errors missed':>15}")
    chosen = None
    for i in range(args.steps + 1):
        t = top * i / args.steps
        esc = [(r > t) or f for r, f, _ in cases]
        k = sum(esc)
        caught = sum(1 for e, (_, _, w) in zip(esc, cases) if e and w)
        rate = k / n
        if has_label:
            cs = f"{caught}/{errors}"
            ms = str(errors - caught)
        else:
            cs = ms = "n/a"
        print(f"{t:>10.3f}{k:>11}{rate:>8.1%}{cs:>15}{ms:>15}")
        if chosen is None and rate <= args.budget:
            chosen = (t, rate, cs)
    if chosen:
        print(f"lowest threshold within budget: {chosen[0]:.3f} "
              f"(escalation {chosen[1]:.1%}, errors caught {chosen[2]})")
    else:
        print("no threshold meets the budget: forced rules (--floor/--always) "
              "alone exceed it; relax them or add reviewers")


if __name__ == "__main__":
    main()
