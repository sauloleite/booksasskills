#!/usr/bin/env python3
"""Estimate KV cache memory for transformer inference, and how many sequences fit.

Formula (unoptimized multi-head attention):
    KV bytes = 2 x batch x seq_len x layers x kv_width x bytes_per_value
where kv_width = hidden size for standard multi-head attention, or
kv_heads x head_dim for grouped-query (GQA) / multi-query (MQA) attention.

Inputs (command-line flags):
    --layers, --seq-len, --batch, --bytes-per-value
    either --hidden (MHA) or --kv-heads with --head-dim (GQA/MQA);
    with --hidden and --heads and --kv-heads, head_dim is derived as hidden/heads.
    optional --params-b and --weight-bytes to compare with weight memory
    optional --gpu-gb and --overhead-gb to estimate max concurrent sequences.

Output: plain-text report (bytes per token, per sequence, total cache, optional
weights comparison and capacity). Decimal GB (1e9 bytes) are used throughout.

Example:
    python3 kv_cache_size.py --layers 40 --hidden 5120 --batch 32 --seq-len 2048
"""
import argparse
import sys

GB = 1e9


def main(argv=None):
    p = argparse.ArgumentParser(description="KV cache size calculator (MHA, GQA, MQA).")
    p.add_argument("--layers", type=int, required=True, help="number of transformer layers")
    p.add_argument("--seq-len", type=int, required=True, help="tokens per sequence (prompt + output)")
    p.add_argument("--batch", type=int, default=1, help="concurrent sequences (default 1)")
    p.add_argument("--bytes-per-value", type=float, default=2.0,
                   help="2 for FP16/BF16, 1 for INT8/FP8, 0.5 for 4-bit (default 2)")
    p.add_argument("--hidden", type=int, help="model dimension (used directly for MHA)")
    p.add_argument("--heads", type=int, help="number of query heads (to derive head_dim)")
    p.add_argument("--kv-heads", type=int, help="number of key/value heads (GQA/MQA)")
    p.add_argument("--head-dim", type=int, help="dimension per head")
    p.add_argument("--params-b", type=float, help="model parameters in billions (for comparison)")
    p.add_argument("--weight-bytes", type=float, default=2.0, help="bytes per weight (default 2)")
    p.add_argument("--gpu-gb", type=float, help="total accelerator memory in GB (for capacity)")
    p.add_argument("--overhead-gb", type=float, default=0.0,
                   help="memory reserved for activations/framework in GB (default 0)")
    a = p.parse_args(argv)

    if a.kv_heads is not None:
        head_dim = a.head_dim
        if head_dim is None:
            if a.hidden is None or a.heads is None:
                p.error("with --kv-heads give --head-dim, or --hidden and --heads")
            head_dim = a.hidden // a.heads
        kv_width = a.kv_heads * head_dim
        mode = f"GQA/MQA ({a.kv_heads} KV heads x head_dim {head_dim})"
    elif a.hidden is not None:
        kv_width = a.hidden
        mode = f"MHA (hidden {a.hidden})"
    else:
        p.error("give --hidden, or --kv-heads with --head-dim")

    per_token = 2 * a.layers * kv_width * a.bytes_per_value
    per_seq = per_token * a.seq_len
    total = per_seq * a.batch

    print(f"Attention layout     : {mode}")
    print(f"KV bytes per token   : {per_token:,.0f} B ({per_token / 1024:,.1f} KiB)")
    print(f"KV per sequence      : {per_seq / GB:,.3f} GB at {a.seq_len:,} tokens")
    print(f"KV total             : {total / GB:,.2f} GB for batch {a.batch}")

    weights = None
    if a.params_b is not None:
        weights = a.params_b * 1e9 * a.weight_bytes
        print(f"Weights              : {weights / GB:,.2f} GB "
              f"({a.params_b}B params x {a.weight_bytes} B)")
        print(f"KV / weights ratio   : {total / weights:,.2f}x")

    if a.gpu_gb is not None:
        free = a.gpu_gb * GB - (weights or 0) - a.overhead_gb * GB
        if free <= 0:
            print("Capacity             : weights + overhead exceed GPU memory")
        else:
            n = int(free // per_seq)
            print(f"Free for KV cache    : {free / GB:,.2f} GB")
            print(f"Max sequences        : {n} at {a.seq_len:,} tokens each")
    return 0


if __name__ == "__main__":
    sys.exit(main())
