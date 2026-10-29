#!/usr/bin/env python3
"""Back-of-envelope scaling calculator for foundation model training and serving.

Inputs (choose one starting point):
  --params N          model parameters (accepts suffixes K, M, B, T, e.g. 7B or 175e9)
  --budget-flops C    a compute budget; the script derives the compute-optimal N and D

Optional inputs:
  --tokens D          training tokens (default: tokens-per-param x N, Chinchilla ~20)
  --active-params A   active parameters per token for MoE models (FLOPs use A, memory uses N)
  --flops F           known training FLOPs (overrides the 6 x A x D estimate)
  --gpus G, --gpu-tflops T, --utilization U, --price P   hardware and cost assumptions
  --bytes-per-param B weight precision for the inference memory floor (default 2 = 16-bit)

Outputs (printed): compute-optimal tokens, training FLOPs, ideal and realistic wall-clock
days, GPU-hours, dollar cost, and the weight-only memory floor in GB.

Formulas: D_opt = 20 x N; FLOPs ~= 6 x N_active x D; from a budget C, N = sqrt(C / (6 x 20)).
Days = FLOPs / (G x T x 1e12 x U x 86400). Deterministic, standard library only, no network.
"""
import argparse
import math

SUFFIX = {"K": 1e3, "M": 1e6, "B": 1e9, "T": 1e12}


def parse_num(text):
    text = text.strip().upper()
    if text and text[-1] in SUFFIX:
        return float(text[:-1]) * SUFFIX[text[-1]]
    return float(text)


def human(x):
    for unit, size in (("T", 1e12), ("B", 1e9), ("M", 1e6), ("K", 1e3)):
        if abs(x) >= size:
            return f"{x / size:,.2f}{unit}"
    return f"{x:,.2f}"


def main():
    p = argparse.ArgumentParser(description="Compute-optimal tokens, training FLOPs, GPU-days, cost and weight memory.")
    start = p.add_mutually_exclusive_group(required=True)
    start.add_argument("--params", type=parse_num, help="total parameters, e.g. 7B")
    start.add_argument("--budget-flops", type=parse_num, help="compute budget in FLOPs, e.g. 1e22")
    p.add_argument("--tokens", type=parse_num, help="training tokens (default: tokens-per-param x params)")
    p.add_argument("--tokens-per-param", type=float, default=20.0, help="Chinchilla ratio (default 20)")
    p.add_argument("--active-params", type=parse_num, help="active params per token (MoE)")
    p.add_argument("--flops", type=parse_num, help="known training FLOPs (skips 6ND estimate)")
    p.add_argument("--gpus", type=int, default=256, help="number of GPUs (default 256)")
    p.add_argument("--gpu-tflops", type=float, default=60.0, help="peak TFLOP/s per GPU (default 60)")
    p.add_argument("--utilization", type=float, default=0.5, help="fraction of peak achieved (default 0.5)")
    p.add_argument("--price", type=float, default=2.0, help="USD per GPU-hour (default 2.0)")
    p.add_argument("--bytes-per-param", type=float, default=2.0, help="bytes per weight (default 2)")
    a = p.parse_args()
    if not 0 < a.utilization <= 1:
        p.error("--utilization must be in (0, 1]")

    r = a.tokens_per_param
    if a.budget_flops:
        n = math.sqrt(a.budget_flops / (6 * r))
        d = r * n
        flops = a.budget_flops
        print(f"Budget {a.budget_flops:.3e} FLOPs -> compute-optimal params {human(n)}, tokens {human(d)}")
    else:
        n = a.params
        active = a.active_params if a.active_params else n
        if a.tokens:
            d = a.tokens
        elif a.flops:
            d = a.flops / (6 * active)  # implied by FLOPs ~= 6 x N_active x D
        else:
            d = r * n
        flops = a.flops if a.flops else 6 * active * d
        print(f"Params (total)          : {human(n)}")
        if a.active_params:
            print(f"Params (active/token)   : {human(active)}")
        print(f"Compute-optimal tokens  : {human(r * n)}  ({r:g} tokens/param)")
        implied = " (implied by given FLOPs)" if a.flops and not a.tokens else ""
        print(f"Training tokens used    : {human(d)}  ({d / n:.1f} tokens/param){implied}")
        print(f"Training FLOPs          : {flops:.3e}" + ("  (given)" if a.flops else "  (6 x active params x tokens)"))

    cluster = a.gpus * a.gpu_tflops * 1e12
    ideal_days = flops / cluster / 86400
    real_days = ideal_days / a.utilization
    gpu_hours = real_days * 24 * a.gpus
    print(f"Cluster                 : {a.gpus} GPUs x {a.gpu_tflops:g} TFLOP/s peak")
    print(f"Days at 100% utilization (ideal): {ideal_days:,.1f}")
    print(f"Days at {a.utilization:.0%} utilization (realistic): {real_days:,.1f}")
    print(f"GPU-hours               : {gpu_hours:,.0f}")
    print(f"Cost at ${a.price:g}/GPU-hour   : ${gpu_hours * a.price:,.0f}")
    print(f"Weight memory floor     : {n * a.bytes_per_param / 1e9:,.1f} GB "
          f"({a.bytes_per_param:g} bytes/param; real serving needs more for KV cache and activations)")


if __name__ == "__main__":
    main()
