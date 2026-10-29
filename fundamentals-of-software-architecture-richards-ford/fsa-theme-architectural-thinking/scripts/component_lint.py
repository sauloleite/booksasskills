#!/usr/bin/env python3
"""Flag Entity Trap names and low-cohesion responsibility statements.

INPUT
  A text file with one component per line:
      Component Name: responsibility statement
  The statement part is optional. Blank lines and '#' lines are ignored.

CHECKS
  name-suffix   Name ends with Manager, Supervisor, Controller, Handler,
                Engine or Processor (an Entity Trap warning sign).
  conjunctions  Statement contains 'and', 'also', 'in addition' or
                'as well as' at least --min-glue times in total (default 2;
                a single 'and' is often harmless).
  commas        Statement contains 3 or more commas (tunable, --max-commas).

OUTPUT
  One line per component: OK or the list of findings, then a summary count.
  Exit code 0 always (advisory tool). Deterministic, stdlib only.

EXAMPLE
  python3 component_lint.py components.txt
  python3 component_lint.py components.txt --max-commas 2
"""
import argparse
import re
import sys

SUFFIXES = ("Manager", "Supervisor", "Controller", "Handler", "Engine", "Processor")
GLUE = ("in addition", "as well as", "also", "and")


def lint(name, statement, max_commas, min_glue=2):
    findings = []
    last = name.split()[-1] if name.split() else ""
    for s in SUFFIXES:
        if last.endswith(s):
            findings.append(f"name-suffix:{s}")
            break
    text = statement.lower()
    glue_hits = []
    for g in GLUE:
        n = len(re.findall(r"\b" + re.escape(g) + r"\b", text))
        if n:
            glue_hits.append(f"{g} x{n}")
            text = re.sub(r"\b" + re.escape(g) + r"\b", " ", text)
    total_glue = sum(int(h.rsplit("x", 1)[1]) for h in glue_hits)
    if glue_hits and total_glue >= min_glue:
        findings.append("conjunctions:" + "; ".join(glue_hits))
    commas = statement.count(",")
    if commas >= max_commas:
        findings.append(f"commas:{commas}")
    return findings


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", help="component list file ('-' for stdin)")
    ap.add_argument("--max-commas", type=int, default=3,
                    help="flag statements with at least this many commas (default 3)")
    ap.add_argument("--min-glue", type=int, default=2,
                    help="flag statements with at least this many conjunctions (default 2)")
    args = ap.parse_args()
    fh = sys.stdin if args.file == "-" else open(args.file, encoding="utf-8")
    flagged = total = 0
    with fh:
        for raw in fh:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            name, _, stmt = line.partition(":")
            name, stmt = name.strip(), stmt.strip()
            total += 1
            f = lint(name, stmt, args.max_commas, args.min_glue)
            flagged += bool(f)
            print(f"{name}: {'OK' if not f else ' | '.join(f)}")
    print(f"\ncomponents={total} flagged={flagged}")


if __name__ == "__main__":
    main()
