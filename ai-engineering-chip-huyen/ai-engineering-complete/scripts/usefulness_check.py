#!/usr/bin/env python3
"""Estimate latency and cost per request and check them against usefulness thresholds.

Based on the planning guidance in Chapter 1 of Chip Huyen's "AI Engineering":
usefulness thresholds include latency (TTFT, TPOT, total latency) and cost per
inference request, and latency should be judged against the current process.

Inputs (command-line flags):
  Output size: --output-tokens, or --output-words (converted with --words-per-token,
  default 0.75, the rough English ratio for GPT-4-class tokenizers).
  --input-tokens       prompt size in tokens (default 0)
  --ttft-ms            time to first token in milliseconds
  --tpot-ms            time per output token in milliseconds
  --price-in / --price-out   USD per 1M input / output tokens (default 0)
  --max-latency-s      optional total-latency target in seconds
  --max-ttft-ms        optional TTFT target in milliseconds
  --max-cost           optional cost-per-request target in USD
  --baseline-s         optional current-process response time in seconds
  --requests-per-day   optional volume for a daily cost estimate

Model: total latency = TTFT + TPOT * (output_tokens - 1), since the first token
is covered by TTFT. Cost = input_tokens * price_in / 1e6 + output_tokens * price_out / 1e6.

Output: a plain-text report of the estimates and PASS/FAIL per supplied target.
Exit code 0 if every supplied target passes (or none is given), 1 otherwise.
Deterministic, standard library only, no network access.
"""
import argparse
import math
import sys


def estimate(output_tokens, input_tokens, ttft_ms, tpot_ms, price_in, price_out):
    """Return (total_latency_seconds, cost_usd) for one request."""
    decode_tokens = max(output_tokens - 1, 0)
    total_ms = ttft_ms + tpot_ms * decode_tokens
    cost = input_tokens * price_in / 1e6 + output_tokens * price_out / 1e6
    return total_ms / 1000.0, cost


def main(argv=None):
    p = argparse.ArgumentParser(
        description="Check estimated latency and cost per request against usefulness thresholds.")
    size = p.add_mutually_exclusive_group(required=True)
    size.add_argument("--output-tokens", type=int, help="expected output length in tokens")
    size.add_argument("--output-words", type=float, help="expected output length in words")
    p.add_argument("--words-per-token", type=float, default=0.75,
                   help="words per token for word-to-token conversion (default 0.75)")
    p.add_argument("--input-tokens", type=int, default=0, help="prompt size in tokens")
    p.add_argument("--ttft-ms", type=float, required=True, help="time to first token (ms)")
    p.add_argument("--tpot-ms", type=float, required=True, help="time per output token (ms)")
    p.add_argument("--price-in", type=float, default=0.0, help="USD per 1M input tokens")
    p.add_argument("--price-out", type=float, default=0.0, help="USD per 1M output tokens")
    p.add_argument("--max-latency-s", type=float, help="target for total latency (s)")
    p.add_argument("--max-ttft-ms", type=float, help="target for TTFT (ms)")
    p.add_argument("--max-cost", type=float, help="target cost per request (USD)")
    p.add_argument("--baseline-s", type=float,
                   help="current process response time (s), e.g. human median")
    p.add_argument("--requests-per-day", type=int, help="volume for daily cost estimate")
    a = p.parse_args(argv)

    if a.output_tokens is not None:
        out_tokens = a.output_tokens
    else:
        if a.words_per_token <= 0:
            p.error("--words-per-token must be positive")
        # round first so float noise (e.g. 100.00000000000001) does not add a token
        out_tokens = math.ceil(round(a.output_words / a.words_per_token, 6))
    if out_tokens < 1:
        p.error("output length must be at least 1 token")

    latency_s, cost = estimate(out_tokens, a.input_tokens, a.ttft_ms, a.tpot_ms,
                               a.price_in, a.price_out)

    print(f"Output tokens:          {out_tokens}")
    print(f"Input tokens:           {a.input_tokens}")
    print(f"TTFT:                   {a.ttft_ms:.0f} ms")
    print(f"Est. total latency:     {latency_s:.2f} s")
    print(f"Est. cost per request:  ${cost:.6f}")
    if a.requests_per_day:
        print(f"Est. cost per day:      ${cost * a.requests_per_day:,.2f} "
              f"({a.requests_per_day:,} requests)")

    checks = []
    if a.max_ttft_ms is not None:
        checks.append(("TTFT", a.ttft_ms <= a.max_ttft_ms,
                       f"{a.ttft_ms:.0f} ms vs target {a.max_ttft_ms:.0f} ms"))
    if a.max_latency_s is not None:
        checks.append(("Total latency", latency_s <= a.max_latency_s,
                       f"{latency_s:.2f} s vs target {a.max_latency_s:.2f} s"))
    if a.max_cost is not None:
        checks.append(("Cost per request", cost <= a.max_cost,
                       f"${cost:.6f} vs target ${a.max_cost:.6f}"))
    if a.baseline_s is not None:
        checks.append(("Faster than current process", latency_s < a.baseline_s,
                       f"{latency_s:.2f} s vs baseline {a.baseline_s:.2f} s"))

    if checks:
        print("\nThreshold checks:")
        for name, ok, detail in checks:
            print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
        if not all(ok for _, ok, _ in checks):
            print("\nAt least one threshold fails: consider streaming (TTFT drives perceived "
                  "speed), shorter outputs, a smaller or optimized model, or precomputation.")
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
