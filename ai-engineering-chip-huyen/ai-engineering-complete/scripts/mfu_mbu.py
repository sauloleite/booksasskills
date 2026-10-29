#!/usr/bin/env python3
"""Compute model FLOP/s utilization (MFU) and model bandwidth utilization (MBU).

MBU: each decode step streams all weights (plus the KV cache read for the batch).
    steps/s         = tokens_per_s / batch      (one token per sequence per step)
    bytes per step  = params x bytes_per_param + kv_gb_per_step x 1e9
    bandwidth used  = bytes per step x steps/s
    MBU             = bandwidth used / peak bandwidth
  With batch 1 and no KV term this reduces to params x bytes/param x tokens/s.

MFU: achieved FLOP/s = flops_per_token x tokens_per_s, with flops_per_token
  defaulting to 2 x params (forward pass approximation); MFU = achieved / peak.

Inputs: --params-b, --bytes-per-param, --tokens-per-s, --peak-bw-tbs,
optional --batch, --kv-gb-per-step, --peak-tflops, --flops-per-token.
Output: plain-text report of bandwidth used, MBU, achieved TFLOP/s and MFU,
plus the bandwidth-limited decode ceiling at batch 1.

Example:
    python3 mfu_mbu.py --params-b 7 --bytes-per-param 2 --tokens-per-s 100 \
        --peak-bw-tbs 2 --peak-tflops 312
"""
import argparse
import sys


def main(argv=None):
    p = argparse.ArgumentParser(description="MFU and MBU calculator for LLM inference.")
    p.add_argument("--params-b", type=float, required=True, help="parameters in billions")
    p.add_argument("--bytes-per-param", type=float, default=2.0, help="2 FP16, 1 INT8, 0.5 INT4")
    p.add_argument("--tokens-per-s", type=float, required=True,
                   help="observed output tokens/s (aggregate across the batch)")
    p.add_argument("--batch", type=int, default=1, help="sequences decoded together (default 1)")
    p.add_argument("--kv-gb-per-step", type=float, default=0.0,
                   help="KV cache GB read per decode step for the whole batch (default 0)")
    p.add_argument("--peak-bw-tbs", type=float, help="chip peak memory bandwidth in TB/s")
    p.add_argument("--peak-tflops", type=float, help="chip peak TFLOP/s at the precision used")
    p.add_argument("--flops-per-token", type=float,
                   help="FLOPs per generated token (default 2 x params)")
    a = p.parse_args(argv)

    params = a.params_b * 1e9
    weight_bytes = params * a.bytes_per_param
    steps_per_s = a.tokens_per_s / a.batch
    bytes_per_step = weight_bytes + a.kv_gb_per_step * 1e9
    bw_used = bytes_per_step * steps_per_s

    print(f"Weights: {weight_bytes / 1e9:.2f} GB; decode steps/s: {steps_per_s:.2f}")
    print(f"Bandwidth used: {bw_used / 1e12:.3f} TB/s")
    if a.peak_bw_tbs:
        mbu = bw_used / (a.peak_bw_tbs * 1e12)
        print(f"MBU: {100 * mbu:.1f}% of {a.peak_bw_tbs} TB/s")
        ceiling = a.peak_bw_tbs * 1e12 / bytes_per_step
        print(f"Bandwidth ceiling: {ceiling:.1f} decode steps/s "
              f"(= tokens/s per sequence) at these bytes per step")

    fpt = a.flops_per_token if a.flops_per_token else 2 * params
    achieved = fpt * a.tokens_per_s
    print(f"Achieved compute: {achieved / 1e12:.3f} TFLOP/s ({fpt:.3g} FLOPs/token)")
    if a.peak_tflops:
        mfu = achieved / (a.peak_tflops * 1e12)
        print(f"MFU: {100 * mfu:.2f}% of {a.peak_tflops} TFLOP/s")

    if a.peak_bw_tbs and a.peak_tflops:
        if mbu > mfu:
            print("Reading: bandwidth-bound profile (MBU >> MFU); quantization, "
                  "batching, speculative decoding help.")
        else:
            print("Reading: compute-heavy profile (MFU >= MBU); more FLOP/s or "
                  "more chips help.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
