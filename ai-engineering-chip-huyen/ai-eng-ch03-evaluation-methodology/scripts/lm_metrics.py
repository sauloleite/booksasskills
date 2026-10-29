#!/usr/bin/env python3
"""Cross entropy, perplexity, bits-per-character and bits-per-byte from token logprobs.

Input: per-token log probabilities that a model assigned to the actual tokens
of a text, either as command-line numbers or a file (one number per line, or
whitespace/comma separated). Logprobs are natural log by default; pass
--base2 if they are log base 2.

Optional: --text-file (the scored text) or --chars/--bytes counts, to compute
BPC and BPB. Bytes are counted in UTF-8.

Output: number of tokens, cross entropy in nats and bits per token,
perplexity, and (if text size is known) BPC and BPB.

Formulas: H_nats = -mean(logprob); H_bits = H_nats / ln 2; PPL = e^H_nats;
BPC = total_bits / chars; BPB = total_bits / bytes.
"""
import argparse
import math
import re
import sys


def parse_numbers(text):
    return [float(x) for x in re.split(r"[\s,]+", text.strip()) if x]


def metrics(logprobs, base2=False):
    if not logprobs:
        raise ValueError("no logprobs given")
    if any(lp > 0 for lp in logprobs):
        raise ValueError("logprobs must be <= 0")
    nats = [-(lp * math.log(2) if base2 else lp) for lp in logprobs]
    h_nats = sum(nats) / len(nats)
    h_bits = h_nats / math.log(2)
    return {
        "tokens": len(nats),
        "total_bits": h_bits * len(nats),
        "ce_nats": h_nats,
        "ce_bits": h_bits,
        "perplexity": math.exp(h_nats),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("logprobs", nargs="*", type=float, help="token logprobs (natural log unless --base2)")
    ap.add_argument("--file", help="file containing logprobs")
    ap.add_argument("--base2", action="store_true", help="logprobs are log base 2")
    ap.add_argument("--text-file", help="the scored text, to derive char and UTF-8 byte counts")
    ap.add_argument("--chars", type=int, help="character count of the scored text")
    ap.add_argument("--bytes", type=int, help="byte count of the scored text")
    args = ap.parse_args()

    lps = list(args.logprobs)
    if args.file:
        with open(args.file) as f:
            lps += parse_numbers(f.read())
    m = metrics(lps, args.base2)

    chars, nbytes = args.chars, args.bytes
    if args.text_file:
        with open(args.text_file, encoding="utf-8") as f:
            text = f.read()
        chars = chars or len(text)
        nbytes = nbytes or len(text.encode("utf-8"))

    print(f"tokens:              {m['tokens']}")
    print(f"cross entropy (nat): {m['ce_nats']:.4f} per token")
    print(f"cross entropy (bit): {m['ce_bits']:.4f} per token")
    print(f"perplexity:          {m['perplexity']:.4f}")
    if chars:
        print(f"bits per character:  {m['total_bits'] / chars:.4f}")
    if nbytes:
        bpb = m["total_bits"] / nbytes
        print(f"bits per byte:       {bpb:.4f}  (compression ratio vs 8-bit bytes: {8 / bpb:.2f}x)")


if __name__ == "__main__":
    sys.exit(main())
