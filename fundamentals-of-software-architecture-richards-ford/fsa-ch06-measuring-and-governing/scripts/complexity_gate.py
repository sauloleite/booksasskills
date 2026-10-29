#!/usr/bin/env python3
"""Cyclomatic-complexity fitness function for Python source.

Inputs
  PATHS (positional): .py files and/or directories (searched recursively).
  --max N: hard limit; any function above it fails the gate (default 10,
      the common industry ceiling).
  --target N: preferred ceiling; functions above it are listed as warnings
      (default 5, the stricter goal for well-factored code).
  --allow FILE: optional allowlist, one "path::qualified_name" per line, for
      functions whose complexity is judged essential (domain-driven).
  --json: machine-readable output.

Method
  Per function or method, CC = 1 + number of decision points, where decision
  points are: if/elif, for, while, except, conditional expression, each extra
  operand of 'and'/'or', each 'if' clause in a comprehension, each 'case' in a
  match statement, and assert. Nested functions are scored separately.

Output
  Report sorted by CC (descending) on stdout. Exit 0 when no unallowed function
  exceeds --max, 1 otherwise, 2 on unreadable or unparsable input.
Deterministic, standard library only, no network.
"""
import argparse
import ast
import json
import os
import sys

DECISIONS = (ast.If, ast.For, ast.AsyncFor, ast.While, ast.ExceptHandler,
             ast.IfExp, ast.Assert)
FUNCS = (ast.FunctionDef, ast.AsyncFunctionDef)


def decision_count(node):
    """Count decision points inside node, not descending into nested defs."""
    total = 0
    for child in ast.iter_child_nodes(node):
        if isinstance(child, FUNCS + (ast.ClassDef,)):
            continue
        if isinstance(child, DECISIONS):
            total += 1
        elif isinstance(child, ast.BoolOp):
            total += len(child.values) - 1
        elif isinstance(child, ast.comprehension):
            total += len(child.ifs)
        elif hasattr(ast, "match_case") and isinstance(child, ast.match_case):
            total += 1
        total += decision_count(child)
    return total


def functions(tree):
    """Yield (qualified_name, node) for every function, including nested ones."""
    stack = [("", tree)]
    while stack:
        prefix, node = stack.pop()
        for child in ast.iter_child_nodes(node):
            if isinstance(child, FUNCS + (ast.ClassDef,)):
                name = f"{prefix}{child.name}"
                if isinstance(child, FUNCS):
                    yield name, child
                stack.append((name + ".", child))
            else:
                stack.append((prefix, child))


def collect(paths):
    files = []
    for p in paths:
        if os.path.isdir(p):
            for root, dirs, names in os.walk(p):
                dirs.sort()
                files += [os.path.join(root, n) for n in sorted(names) if n.endswith(".py")]
        elif p.endswith(".py"):
            files.append(p)
    return sorted(set(files))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("paths", nargs="+", help=".py files or directories")
    ap.add_argument("--max", type=int, default=10, help="fail above this CC (default 10)")
    ap.add_argument("--target", type=int, default=5, help="warn above this CC (default 5)")
    ap.add_argument("--allow", help="allowlist file of path::qualified_name entries")
    ap.add_argument("--json", action="store_true", help="emit JSON")
    args = ap.parse_args()

    allowed = set()
    if args.allow:
        with open(args.allow) as fh:
            allowed = {l.split("#", 1)[0].strip() for l in fh} - {""}

    rows = []
    for path in collect(args.paths):
        try:
            with open(path, encoding="utf-8") as fh:
                tree = ast.parse(fh.read(), filename=path)
        except (OSError, SyntaxError, UnicodeDecodeError) as exc:
            print(f"error: {path}: {exc}", file=sys.stderr)
            sys.exit(2)
        for name, node in functions(tree):
            cc = 1 + decision_count(node)
            key = f"{path}::{name}"
            status = "ok"
            if cc > args.max:
                status = "allowed" if key in allowed else "FAIL"
            elif cc > args.target:
                status = "warn"
            rows.append({"function": key, "line": node.lineno, "cc": cc, "status": status})

    rows.sort(key=lambda r: (-r["cc"], r["function"]))
    fails = [r for r in rows if r["status"] == "FAIL"]
    summary = {"functions": len(rows), "max": args.max, "target": args.target,
               "fail": len(fails), "warn": sum(r["status"] == "warn" for r in rows),
               "allowed": sum(r["status"] == "allowed" for r in rows),
               "mean_cc": round(sum(r["cc"] for r in rows) / len(rows), 2) if rows else 0}
    if args.json:
        print(json.dumps({"summary": summary, "functions": rows}, indent=2))
    else:
        for r in rows:
            if r["status"] != "ok":
                print(f"{r['status']:>7}  CC={r['cc']:<3} {r['function']} (line {r['line']})")
        print("summary: " + " ".join(f"{k}={v}" for k, v in summary.items()))
        print("result: " + ("FAIL" if fails else "PASS"))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
