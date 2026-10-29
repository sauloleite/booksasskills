#!/usr/bin/env python3
"""Estimate how per-step accuracy compounds over a multi-step agent task.

Assumes steps fail independently, so task success = p ** n.

Modes:
  forward (default): given per-step accuracy --p and one or more step
      counts --steps, print the end-to-end success rate for each.
  solve: given --target success rate and --steps, print the minimum
      per-step accuracy needed (target ** (1/n)).
  max-steps: given --p and --target, print the largest n with p**n >= target.

Optional --retries R models a validator that catches a failed step and
lets the agent retry up to R extra times (step success becomes
1 - (1-p)**(R+1)); this assumes failures are detected, which is optimistic.
Output is a plain-text table. Deterministic, standard library only.
"""
import argparse
import math


def step_success(p, retries):
    return 1 - (1 - p) ** (retries + 1)


def main():
    ap = argparse.ArgumentParser(description="Compound success of multi-step agents (p ** n).")
    ap.add_argument("--mode", choices=["forward", "solve", "max-steps"], default="forward")
    ap.add_argument("--p", type=float, help="per-step accuracy, 0..1")
    ap.add_argument("--steps", type=int, nargs="+", default=[1, 5, 10, 20, 50, 100])
    ap.add_argument("--target", type=float, help="desired end-to-end success, 0..1")
    ap.add_argument("--retries", type=int, default=0, help="extra attempts per step when a failure is caught")
    a = ap.parse_args()

    if a.mode == "forward":
        if a.p is None:
            ap.error("--p is required for forward mode")
        q = step_success(a.p, a.retries)
        print(f"per-step accuracy {a.p:.4f}" + (f" (effective {q:.4f} with {a.retries} retries)" if a.retries else ""))
        print(f"{'steps':>6}  {'task success':>12}")
        for n in a.steps:
            print(f"{n:>6}  {q ** n:>12.4%}")
    elif a.mode == "solve":
        if a.target is None:
            ap.error("--target is required for solve mode")
        print(f"target end-to-end success {a.target:.2%}")
        print(f"{'steps':>6}  {'min per-step accuracy':>22}")
        for n in a.steps:
            print(f"{n:>6}  {a.target ** (1.0 / n):>22.4%}")
    else:
        if a.p is None or a.target is None:
            ap.error("--p and --target are required for max-steps mode")
        q = step_success(a.p, a.retries)
        if q >= 1:
            print("per-step accuracy is 1.0: no step limit")
        elif q <= 0:
            print("per-step accuracy is 0: no step count reaches the target")
        else:
            n = math.floor(math.log(a.target) / math.log(q))
            print(f"max steps with success >= {a.target:.2%} at per-step {q:.4f}: {n} (p**n = {q ** n:.4%})")


if __name__ == "__main__":
    main()
