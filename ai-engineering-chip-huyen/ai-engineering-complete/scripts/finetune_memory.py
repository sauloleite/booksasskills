#!/usr/bin/env python3
"""Back-of-the-envelope GPU memory estimator for serving and finetuning an LLM.

Implements the rough memory math from Chapter 7 of Chip Huyen's "AI Engineering":

  inference  = weights + activations/KV           (activations ~ 20% of weights)
  training   = weights + activations + gradients + optimizer states
  per trainable parameter: 1 gradient + optimizer values (SGD 0, momentum 1, Adam 2)

Modes
  inference  forward pass only
  full       every parameter is trainable
  partial    only --trainable-fraction of the existing weights is trainable
  lora       frozen base + small adapter (trainable count via --trainable-params
             or --trainable-fraction, default 1% of base)
  qlora      like lora, but the frozen base is stored in 4-bit NF4 (0.5 bytes)
  compare    prints inference, full, lora and qlora side by side

Inputs: parameter count (e.g. 7B, 13e9), numeric formats, optimizer, activation factor,
optional mixed-precision master copy, optional GPU capacity to check the fit.
Output: a plain-text table of memory components in decimal GB (1 GB = 1e9 bytes),
which matches the chapter's arithmetic (13B x 2 bytes = 26 GB).

Activations are modeled as --activation-factor times the stored weight memory in every
mode (the chapter's 20% rule). Treat it as a floor for training, where stored
activations can exceed the weights unless you use gradient checkpointing. Paged
optimizers, CPU offloading and framework overhead are not modeled.
Deterministic, standard library only.
"""
import argparse

BYTES = {"fp64": 8, "fp32": 4, "tf32": 4, "fp16": 2, "bf16": 2,
         "fp8": 1, "int8": 1, "fp4": 0.5, "int4": 0.5, "nf4": 0.5}
OPT_STATES = {"sgd": 0, "momentum": 1, "adam": 2}
GB = 1e9


def parse_count(text):
    """Accept 7B, 350M, 13e9 or 7000000000."""
    t = text.strip().upper()
    mult = {"K": 1e3, "M": 1e6, "B": 1e9, "T": 1e12}
    if t and t[-1] in mult:
        return float(t[:-1]) * mult[t[-1]]
    return float(t)


def estimate(mode, n, a):
    """Return an ordered dict of component -> bytes for one mode."""
    wb = BYTES["nf4"] if mode == "qlora" else BYTES[a.weight_format]
    sb = BYTES[a.state_format]
    k = OPT_STATES[a.optimizer]
    out = {"weights": n * wb, "activations": a.activation_factor * n * wb}
    if mode == "inference":
        return out, 0
    if mode == "full":
        t = n
    elif a.trainable_params is not None:
        t = a.trainable_params
    elif a.trainable_fraction is not None:
        t = n * a.trainable_fraction
    else:
        t = n * (0.10 if mode == "partial" else 0.01)
    if mode in ("lora", "qlora"):
        out["adapter weights"] = t * sb
    out["gradients"] = t * sb
    out["optimizer states"] = t * k * sb
    if a.master_format:
        out["master copy"] = t * BYTES[a.master_format]
    return out, t


def report(mode, n, a):
    parts, t = estimate(mode, n, a)
    total = sum(parts.values())
    print(f"== {mode} ==")
    if mode != "inference":
        print(f"  trainable params: {t:,.0f} ({100 * t / n:.4g}% of {n:,.0f})")
    for name, b in parts.items():
        print(f"  {name:<18}{b / GB:10.2f} GB")
    print(f"  {'TOTAL':<18}{total / GB:10.2f} GB")
    if a.gpu_gb:
        verdict = "fits" if total / GB <= a.gpu_gb else "does NOT fit"
        print(f"  -> {verdict} in {a.gpu_gb:g} GB")
    return total


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--params", required=True, type=parse_count,
                   help="total parameter count, e.g. 7B or 13e9")
    p.add_argument("--mode", default="compare",
                   choices=["inference", "full", "partial", "lora", "qlora", "compare"])
    p.add_argument("--weight-format", default="bf16", choices=sorted(BYTES),
                   help="storage format of model weights (default bf16)")
    p.add_argument("--state-format", default="bf16", choices=sorted(BYTES),
                   help="format of gradients, optimizer states and adapter weights "
                        "(default bf16, the chapter's 2-byte assumption)")
    p.add_argument("--optimizer", default="adam", choices=sorted(OPT_STATES))
    p.add_argument("--trainable-params", type=parse_count,
                   help="absolute trainable count (partial/lora/qlora)")
    p.add_argument("--trainable-fraction", type=float,
                   help="trainable share of params, e.g. 0.005 (partial default 0.10, "
                        "lora/qlora default 0.01)")
    p.add_argument("--activation-factor", type=float, default=0.2,
                   help="activations+KV as a fraction of weight memory (default 0.2)")
    p.add_argument("--master-format", choices=sorted(BYTES),
                   help="add a higher-precision master copy of trainable weights "
                        "(mixed precision), e.g. fp32")
    p.add_argument("--gpu-gb", type=float, help="GPU memory to check the fit against")
    a = p.parse_args()
    modes = ["inference", "full", "lora", "qlora"] if a.mode == "compare" else [a.mode]
    for m in modes:
        report(m, a.params, a)


if __name__ == "__main__":
    main()
