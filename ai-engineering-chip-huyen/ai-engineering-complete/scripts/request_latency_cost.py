#!/usr/bin/env python3
"""Estimate per-request latency and cost for an LLM call (hosted API or self-hosted).

Latency model: total = TTFT + TPOT x output_tokens.

Cost, hosted API mode (--input-price/--output-price in $ per 1M tokens):
    cost = uncached_in x input_price + cached_in x input_price x (1 - cache_discount)
           + output_tokens x output_price
Cost, self-hosted mode (--hourly-cost with --decode-tps and --prefill-rpm):
    decode cost/request  = hourly / (decode_tps x 3600) x output_tokens
    prefill cost/request = hourly / (prefill_rpm x 60)

Inputs: command-line flags (see --help). Output: plain-text report with latency,
cost per request, and cost per 1,000 requests (and per day if --requests-per-day).

Examples:
    python3 request_latency_cost.py --ttft-ms 400 --tpot-ms 30 --input-tokens 3000 \
        --output-tokens 400 --input-price 3 --output-price 15 --cached-tokens 2500 \
        --cache-discount 0.9
    python3 request_latency_cost.py --ttft-ms 300 --tpot-ms 25 --output-tokens 500 \
        --hourly-cost 4 --decode-tps 400 --prefill-rpm 200
"""
import argparse
import sys


def main(argv=None):
    p = argparse.ArgumentParser(description="Per-request latency and cost estimator.")
    p.add_argument("--ttft-ms", type=float, required=True, help="time to first token (ms)")
    p.add_argument("--tpot-ms", type=float, required=True, help="time per output token (ms)")
    p.add_argument("--output-tokens", type=int, required=True, help="output tokens per request")
    p.add_argument("--input-tokens", type=int, default=0, help="input tokens per request")
    g = p.add_argument_group("hosted API pricing ($ per 1M tokens)")
    g.add_argument("--input-price", type=float, help="price per 1M input tokens")
    g.add_argument("--output-price", type=float, help="price per 1M output tokens")
    g.add_argument("--cached-tokens", type=int, default=0, help="input tokens served from prompt cache")
    g.add_argument("--cache-discount", type=float, default=0.0,
                   help="fractional discount on cached input, e.g. 0.75 or 0.9")
    s = p.add_argument_group("self-hosted pricing")
    s.add_argument("--hourly-cost", type=float, help="$ per hour for the serving instance")
    s.add_argument("--decode-tps", type=float, help="aggregate output tokens/s of the instance")
    s.add_argument("--prefill-rpm", type=float, help="requests prefilled per minute by the instance")
    p.add_argument("--requests-per-day", type=float, help="optional daily volume for a daily total")
    a = p.parse_args(argv)

    total_ms = a.ttft_ms + a.tpot_ms * a.output_tokens
    print(f"Latency: TTFT {a.ttft_ms:.0f} ms + {a.tpot_ms:.1f} ms x {a.output_tokens} tokens "
          f"= {total_ms / 1000:.2f} s")
    if a.tpot_ms > 0:
        print(f"Per-stream decode speed: {1000 / a.tpot_ms:.1f} tokens/s")

    cost = None
    if a.input_price is not None and a.output_price is not None:
        if a.cached_tokens > a.input_tokens:
            p.error("--cached-tokens cannot exceed --input-tokens")
        uncached = a.input_tokens - a.cached_tokens
        in_cost = (uncached * a.input_price
                   + a.cached_tokens * a.input_price * (1 - a.cache_discount)) / 1e6
        out_cost = a.output_tokens * a.output_price / 1e6
        cost = in_cost + out_cost
        print(f"API cost: input ${in_cost:.6f} + output ${out_cost:.6f} = ${cost:.6f} per request")
        if a.cached_tokens:
            no_cache = (a.input_tokens * a.input_price) / 1e6 + out_cost
            print(f"  without caching: ${no_cache:.6f} (saves {100 * (1 - cost / no_cache):.1f}%)")
    elif a.hourly_cost is not None and a.decode_tps and a.prefill_rpm:
        per_out_tok = a.hourly_cost / (a.decode_tps * 3600)
        decode = per_out_tok * a.output_tokens
        prefill = a.hourly_cost / (a.prefill_rpm * 60)
        cost = decode + prefill
        print(f"Self-hosted: ${per_out_tok * 1e6:.2f} per 1M output tokens")
        print(f"  decode ${decode:.6f} + prefill ${prefill:.6f} = ${cost:.6f} per request")
    else:
        print("No pricing given: pass --input-price and --output-price, or "
              "--hourly-cost, --decode-tps and --prefill-rpm.")

    if cost is not None:
        print(f"Cost per 1,000 requests: ${cost * 1000:.2f}")
        if a.requests_per_day:
            print(f"Cost per day: ${cost * a.requests_per_day:,.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
