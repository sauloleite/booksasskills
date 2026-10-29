#!/usr/bin/env python3
"""Automation payback calculator (Strategic Automation, FSE Chapter 11).

Decides whether automating a recurring manual task is worth it, following the
chapter's guidance: repetition signals automation, one-offs do not, wait until
a task has been done a few times, and timebox the build.

Inputs (CLI flags):
  --manual-min     minutes one manual run takes
  --runs-per-month how often the task happens per month
  --months         planning horizon in months (expected remaining task lifetime)
  --build-hours    estimated hours to write and test the automation
  --maint-min      maintenance minutes per month (default 0)
  --residual-min   minutes per run still needed after automating (default 0)
  --times-done     how many times the task has been done by hand so far (default 0)
  --min-repeats    manual repetitions to wait for before automating (default 3)
  --json           emit JSON instead of text

Outputs: manual cost, automated cost, net saving over the horizon, break-even
month, maximum build time that still breaks even (a suggested timebox), and a
verdict: AUTOMATE, WAIT (not repeated enough yet), MARGINAL (net saving under
25% of manual cost, or break-even after half the horizon), or MANUAL.
Deterministic; standard library only; no network.
"""
import argparse
import json
import sys


def compute(manual_min, runs_per_month, months, build_hours, maint_min=0.0,
            residual_min=0.0, times_done=0, min_repeats=3):
    manual_total = manual_min * runs_per_month * months
    residual_total = residual_min * runs_per_month * months
    build_min = build_hours * 60.0
    maint_total = maint_min * months
    automated_total = build_min + maint_total + residual_total
    net = manual_total - automated_total
    monthly_gain = (manual_min - residual_min) * runs_per_month - maint_min
    breakeven = build_min / monthly_gain if monthly_gain > 0 else None
    max_build_h = max(0.0, (manual_total - residual_total - maint_total) / 60.0)

    if runs_per_month * months < 2:
        verdict = "MANUAL"
        reason = "Effectively a one-off; do it by hand."
    elif net <= 0:
        verdict = "MANUAL"
        reason = "Build plus upkeep exceeds the time saved over the horizon."
    elif times_done < min_repeats:
        verdict = "WAIT"
        reason = (f"Pays off on paper, but it has been done {times_done} time(s); "
                  f"repeat it by hand until {min_repeats} to learn what to automate.")
    elif net < 0.25 * manual_total or (breakeven is not None and breakeven > months / 2):
        verdict = "MARGINAL"
        reason = ("Thin margin or slow payback; automate only for non-time benefits "
                  "(fewer errors, consistency, sharing with the team).")
    else:
        verdict = "AUTOMATE"
        reason = "Clear payback; keep the build inside the suggested timebox."

    return {
        "manual_hours": round(manual_total / 60.0, 2),
        "automated_hours": round(automated_total / 60.0, 2),
        "net_saving_hours": round(net / 60.0, 2),
        "breakeven_months": round(breakeven, 2) if breakeven is not None else None,
        "max_build_hours_to_break_even": round(max_build_h, 2),
        "verdict": verdict,
        "reason": reason,
    }


def main(argv=None):
    p = argparse.ArgumentParser(description="Estimate whether automating a recurring task pays back.")
    p.add_argument("--manual-min", type=float, required=True, help="minutes per manual run")
    p.add_argument("--runs-per-month", type=float, required=True, help="runs per month")
    p.add_argument("--months", type=float, default=12, help="horizon in months (default 12)")
    p.add_argument("--build-hours", type=float, required=True, help="hours to build the automation")
    p.add_argument("--maint-min", type=float, default=0, help="maintenance minutes per month")
    p.add_argument("--residual-min", type=float, default=0, help="minutes per run after automating")
    p.add_argument("--times-done", type=int, default=0, help="manual repetitions so far")
    p.add_argument("--min-repeats", type=int, default=3, help="repetitions to wait for (default 3)")
    p.add_argument("--json", action="store_true", help="print JSON")
    a = p.parse_args(argv)
    for name in ("manual_min", "runs_per_month", "months", "build_hours", "maint_min", "residual_min"):
        if getattr(a, name) < 0:
            p.error(f"--{name.replace('_', '-')} must be non-negative")
    if a.residual_min > a.manual_min:
        p.error("--residual-min cannot exceed --manual-min")
    r = compute(a.manual_min, a.runs_per_month, a.months, a.build_hours,
                a.maint_min, a.residual_min, a.times_done, a.min_repeats)
    if a.json:
        print(json.dumps(r, indent=2))
        return 0
    be = r["breakeven_months"]
    print(f"Manual cost over horizon:     {r['manual_hours']} h")
    print(f"Automated cost over horizon:  {r['automated_hours']} h (build + upkeep + residual)")
    print(f"Net saving:                   {r['net_saving_hours']} h")
    if be is None:
        be_txt = "never"
    else:
        be_txt = f"{be} months" + (" (beyond horizon)" if be > a.months else "")
    print(f"Break-even:                   {be_txt}")
    print(f"Timebox (max build to break even): {r['max_build_hours_to_break_even']} h")
    print(f"Verdict: {r['verdict']} - {r['reason']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
