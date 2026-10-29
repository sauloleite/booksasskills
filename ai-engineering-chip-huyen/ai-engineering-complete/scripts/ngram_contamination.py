#!/usr/bin/env python3
"""Flag benchmark examples whose word n-grams also appear in a training corpus.

Inputs
  benchmark   Text file, one evaluation example per line (blank lines skipped).
              With --jsonl, each line is a JSON object and --field names the
              text field to check (default "text").
  corpus      Text file (any layout) standing in for the training data.

Method
  Both files are lowercased and split into alphanumeric word tokens. An example
  is "dirty" if at least --min-hits of its n-grams (default n=13, the size used
  in well-known contamination analyses) occur anywhere in the corpus; the
  threshold is capped at the example's own n-gram count. Examples shorter than
  n tokens are checked as one whole-sequence gram instead.

Outputs
  A summary (examples checked, dirty count and percentage), then one line per
  dirty example: its 1-based line number, matched n-grams / total n-grams, and
  a preview. With --clean-out, writes the clean examples to a file so you can
  report scores on the full set and on the clean subset side by side.

Deterministic, standard library only, no network access. The whole corpus is
held in memory as a set of n-grams, so very large corpora need sharding.

Example:
  python3 ngram_contamination.py bench.txt corpus.txt --n 13 --clean-out clean.txt
"""
import argparse
import json
import re
import sys

TOKEN = re.compile(r"[a-z0-9]+")


def tokens(text):
    return TOKEN.findall(text.lower())


def grams(toks, n):
    if len(toks) < n:
        return [tuple(toks)] if toks else []
    return [tuple(toks[i:i + n]) for i in range(len(toks) - n + 1)]


def load_examples(path, jsonl, field):
    out = []
    with open(path, encoding="utf-8") as fh:
        for ln, line in enumerate(fh, 1):
            if not line.strip():
                continue
            if jsonl:
                try:
                    text = str(json.loads(line)[field])
                except (ValueError, KeyError) as e:
                    sys.exit(f"{path}:{ln}: cannot read field {field!r}: {e}")
            else:
                text = line.rstrip("\n")
            out.append((ln, line.rstrip("\n"), text))
    return out


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("benchmark", help="benchmark file, one example per line")
    p.add_argument("corpus", help="corpus file standing in for training data")
    p.add_argument("--n", type=int, default=13, help="n-gram length in word tokens (default 13)")
    p.add_argument("--min-hits", type=int, default=1,
                   help="matched n-grams needed to call an example dirty (default 1)")
    p.add_argument("--jsonl", action="store_true", help="benchmark lines are JSON objects")
    p.add_argument("--field", default="text", help="JSON field holding the example text (default text)")
    p.add_argument("--clean-out", help="write clean examples (original lines) to this file")
    p.add_argument("--preview", type=int, default=70, help="characters of each dirty example to show")
    args = p.parse_args()
    if args.n < 1 or args.min_hits < 1:
        sys.exit("--n and --min-hits must be >= 1")

    examples = load_examples(args.benchmark, args.jsonl, args.field)
    if not examples:
        sys.exit("benchmark file has no examples")
    with open(args.corpus, encoding="utf-8") as fh:
        corpus_toks = tokens(fh.read())

    # Corpus n-grams of length n, plus shorter whole-sequence lengths needed
    # for short examples.
    lengths = {args.n}
    for _, _, text in examples:
        k = len(tokens(text))
        if 0 < k < args.n:
            lengths.add(k)
    corpus_grams = {k: {tuple(corpus_toks[i:i + k]) for i in range(len(corpus_toks) - k + 1)}
                    for k in lengths}

    dirty, clean_lines = [], []
    for ln, raw, text in examples:
        g = grams(tokens(text), args.n)
        hits = sum(1 for x in g if x in corpus_grams.get(len(x), ()))
        needed = min(args.min_hits, len(g)) if g else 1
        if g and hits >= needed:
            dirty.append((ln, hits, len(g), text))
        else:
            clean_lines.append(raw)

    total = len(examples)
    print(f"Benchmark examples: {total}; corpus tokens: {len(corpus_toks):,}; n = {args.n}; min hits = {args.min_hits}")
    print(f"Dirty: {len(dirty)} ({100 * len(dirty) / total:.1f}%); clean: {len(clean_lines)}")
    for ln, hits, ng, text in dirty:
        prev = text if len(text) <= args.preview else text[:args.preview] + "..."
        print(f"  line {ln}: {hits}/{ng} n-grams matched | {prev}")
    if args.clean_out:
        with open(args.clean_out, "w", encoding="utf-8") as fh:
            fh.write("\n".join(clean_lines) + ("\n" if clean_lines else ""))
        print(f"Clean examples written to {args.clean_out}")


if __name__ == "__main__":
    main()
