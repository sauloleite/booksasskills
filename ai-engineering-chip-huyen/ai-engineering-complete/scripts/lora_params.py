#!/usr/bin/env python3
"""Count LoRA trainable parameters for a transformer and size adapter storage.

For each targeted weight matrix W of shape (n x m), LoRA trains A (n x r) and B (r x m),
so it adds r * (n + m) parameters. LoRA is applied uniformly to every layer, so

  trainable = layers * sum over targets of r * (n_t + m_t)

Supported targets and shapes (d = hidden size, kv = key/value width, f = FFN width):
  q, o          d x d
  k, v          d x kv        (kv = d without grouped-query attention)
  gate, up      d x f
  down          f x d

Inputs: --hidden, --layers, --rank, --targets, optional --kv-dim, --ffn-dim,
--total-params, --bytes (adapter storage format), --adapters (multi-LoRA count),
--budget (trainable-parameter budget).
Outputs: per-layer and total trainable params, adapter size in MB, share of the base
model, the largest rank that fits a budget, and storage for N variants served as
merged full copies versus one shared base plus N adapters.

Example (GPT-3 175B, the LoRA paper's budget setting):
  python3 lora_params.py --hidden 12288 --layers 96 --rank 2 --targets q,k,v,o
  -> 18,874,368 trainable params
Deterministic, standard library only.
"""
import argparse

BYTES = {"fp32": 4, "fp16": 2, "bf16": 2, "int8": 1, "int4": 0.5}


def parse_count(text):
    t = text.strip().upper()
    mult = {"K": 1e3, "M": 1e6, "B": 1e9, "T": 1e12}
    if t and t[-1] in mult:
        return float(t[:-1]) * mult[t[-1]]
    return float(t)


def shapes(d, kv, f):
    return {"q": (d, d), "o": (d, d), "k": (d, kv), "v": (d, kv),
            "gate": (d, f), "up": (d, f), "down": (f, d)}


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--hidden", type=int, required=True, help="model dimension d")
    p.add_argument("--layers", type=int, required=True, help="number of transformer blocks")
    p.add_argument("--rank", type=int, default=8, help="LoRA rank r (default 8)")
    p.add_argument("--targets", default="q,v",
                   help="comma list from q,k,v,o,gate,up,down (default q,v)")
    p.add_argument("--kv-dim", type=int, help="key/value width for GQA (default = hidden)")
    p.add_argument("--ffn-dim", type=int, help="feedforward width (needed for gate/up/down)")
    p.add_argument("--bytes", default="bf16", choices=sorted(BYTES),
                   help="adapter storage format (default bf16)")
    p.add_argument("--total-params", type=parse_count,
                   help="base model parameter count, e.g. 7B (for shares and storage)")
    p.add_argument("--adapters", type=int, default=1,
                   help="number of finetuned variants to store/serve (default 1)")
    p.add_argument("--budget", type=parse_count,
                   help="trainable-parameter budget; prints the largest rank that fits")
    a = p.parse_args()

    targets = [t.strip() for t in a.targets.split(",") if t.strip()]
    kv = a.kv_dim or a.hidden
    if any(t in ("gate", "up", "down") for t in targets) and not a.ffn_dim:
        p.error("--ffn-dim is required for gate/up/down targets")
    table = shapes(a.hidden, kv, a.ffn_dim or 0)
    bad = [t for t in targets if t not in table]
    if bad:
        p.error(f"unknown targets: {bad}")

    per_rank_layer = sum(sum(table[t]) for t in targets)  # params per unit rank per layer
    per_layer = a.rank * per_rank_layer
    total = per_layer * a.layers
    b = BYTES[a.bytes]
    print(f"targets={','.join(targets)} rank={a.rank} layers={a.layers} hidden={a.hidden}")
    for t in targets:
        n, m = table[t]
        print(f"  {t:<5} {n} x {m}: {a.rank * (n + m):,} params per layer")
    print(f"per layer:        {per_layer:,}")
    print(f"total trainable:  {total:,}")
    print(f"adapter size:     {total * b / 1e6:,.2f} MB ({a.bytes})")
    if a.total_params:
        print(f"share of base:    {100 * total / a.total_params:.4g}%")
        print(f"base weights:     {a.total_params * b / 1e9:,.2f} GB ({a.bytes})")
        if a.adapters > 1:
            merged = a.adapters * a.total_params
            separate = a.total_params + a.adapters * total
            print(f"{a.adapters} variants, merged copies:     {merged:,.0f} params "
                  f"({merged * b / 1e9:,.2f} GB)")
            print(f"{a.adapters} variants, base + adapters:   {separate:,.0f} params "
                  f"({separate * b / 1e9:,.2f} GB)")
    if a.budget:
        max_r = int(a.budget // (per_rank_layer * a.layers))
        print(f"largest rank within budget {a.budget:,.0f}: r = {max_r}")


if __name__ == "__main__":
    main()
