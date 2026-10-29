#!/usr/bin/env python3
"""Report shape warnings for Python source: long functions, deep nesting,
long parameter lists, high cyclomatic complexity, conjunctions in names,
and long classes.

Inputs:
    One or more paths (files or directories). Directories are searched
    recursively for *.py files. Thresholds are configurable via flags.

Outputs:
    A plain-text report (default) or JSON (--json) listing every function
    and class that crosses at least one threshold, sorted by file and line,
    followed by a summary count. Files that fail to parse are reported as
    parse errors and skipped.

Exit code:
    0 normally; 1 if --fail-on-findings is set and anything was flagged;
    2 on bad arguments or unreadable paths.

The numbers are prompts for human judgment, not verdicts. A flagged item
may be legitimately complex (essential complexity) or a deliberate facade.

Metric definitions:
    body_lines   distinct source lines spanned by the statements in the
                 body, excluding a leading docstring, blank lines and
                 comment-only lines.
    max_nesting  deepest stack of if/for/while/with/try/match blocks
                 inside the function; an elif does not add depth
                 (nested defs are measured separately).
    params       all parameters including *args/**kwargs, excluding a
                 leading self/cls on methods.
    complexity   McCabe-style: 1 + branches (if, elif, ternary, loops,
                 except handlers, match cases, extra boolean operands,
                 comprehension loops and filters).
    conjunction  name contains the word and/or/but/then as a separate
                 token in snake_case or camelCase.
    class_lines  physical lines from the class statement to its end.
"""
import argparse
import ast
import json
import os
import re
import sys

BLOCK_NODES = (ast.If, ast.For, ast.AsyncFor, ast.While, ast.With,
               ast.AsyncWith, ast.Try)
if hasattr(ast, "Match"):
    BLOCK_NODES = BLOCK_NODES + (ast.Match,)
if hasattr(ast, "TryStar"):
    BLOCK_NODES = BLOCK_NODES + (ast.TryStar,)

FUNC_NODES = (ast.FunctionDef, ast.AsyncFunctionDef)
CONJUNCTIONS = {"and", "or", "but", "then"}


def split_words(name):
    words = []
    for part in name.strip("_").split("_"):
        words.extend(re.findall(r"[A-Z]+(?=[A-Z][a-z])|[A-Z]?[a-z]+|[A-Z]+|\d+", part))
    return [w.lower() for w in words]


def iter_children_no_defs(node):
    """Yield direct children, skipping nested function/class definitions."""
    for child in ast.iter_child_nodes(node):
        if isinstance(child, FUNC_NODES + (ast.ClassDef, ast.Lambda)):
            continue
        yield child


def is_elif(parent, child):
    return (isinstance(parent, ast.If) and isinstance(child, ast.If)
            and len(parent.orelse) == 1 and parent.orelse[0] is child)


def max_nesting(node, depth=0):
    best = depth
    for child in iter_children_no_defs(node):
        nests = isinstance(child, BLOCK_NODES) and not is_elif(node, child)
        child_depth = depth + 1 if nests else depth
        best = max(best, max_nesting(child, child_depth))
    return best


def complexity(node):
    score = 0
    for child in iter_children_no_defs(node):
        if isinstance(child, (ast.If, ast.IfExp, ast.For, ast.AsyncFor,
                              ast.While, ast.ExceptHandler)):
            score += 1
        elif isinstance(child, ast.BoolOp):
            score += len(child.values) - 1
        elif isinstance(child, ast.comprehension):
            score += 1 + len(child.ifs)
        elif hasattr(ast, "match_case") and isinstance(child, ast.match_case):
            score += 1
        score += complexity(child)
    return score


def body_lines(func, code_lines):
    body = list(func.body)
    if (body and isinstance(body[0], ast.Expr)
            and isinstance(getattr(body[0], "value", None), ast.Constant)
            and isinstance(body[0].value.value, str)):
        body = body[1:]
    seen = set()
    for stmt in body:
        for ln in range(stmt.lineno, (stmt.end_lineno or stmt.lineno) + 1):
            if ln in code_lines:
                seen.add(ln)
    return len(seen)


def param_count(func, is_method):
    a = func.args
    names = [p.arg for p in getattr(a, "posonlyargs", [])] + [p.arg for p in a.args]
    if is_method and names and names[0] in ("self", "cls"):
        names = names[1:]
    count = len(names) + len(a.kwonlyargs)
    count += 1 if a.vararg else 0
    count += 1 if a.kwarg else 0
    return count


def code_line_set(source):
    lines = set()
    for i, text in enumerate(source.splitlines(), start=1):
        stripped = text.strip()
        if stripped and not stripped.startswith("#"):
            lines.add(i)
    return lines


def analyze_file(path, limits):
    with open(path, encoding="utf-8") as fh:
        source = fh.read()
    tree = ast.parse(source, filename=path)
    code_lines = code_line_set(source)
    findings = []

    def visit(node, qual, in_class):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, ast.ClassDef):
                name = qual + child.name
                length = (child.end_lineno or child.lineno) - child.lineno + 1
                if length > limits["class_lines"]:
                    findings.append({"file": path, "line": child.lineno,
                                     "kind": "class", "name": name,
                                     "issues": ["class_lines=%d>%d" % (length, limits["class_lines"])]})
                visit(child, name + ".", True)
            elif isinstance(child, FUNC_NODES):
                name = qual + child.name
                m = {
                    "body_lines": body_lines(child, code_lines),
                    "max_nesting": max_nesting(child),
                    "params": param_count(child, in_class),
                    "complexity": 1 + complexity(child),
                }
                issues = ["%s=%d>%d" % (k, v, limits[k]) for k, v in m.items() if v > limits[k]]
                conj = sorted(CONJUNCTIONS.intersection(split_words(child.name)))
                if conj:
                    issues.append("conjunction_in_name=" + ",".join(conj))
                if issues:
                    findings.append({"file": path, "line": child.lineno,
                                     "kind": "function", "name": name,
                                     "metrics": m, "issues": issues})
                visit(child, name + ".", False)
            else:
                visit(child, qual, in_class)

    visit(tree, "", False)
    return findings


def collect_files(paths):
    files = []
    for p in paths:
        if os.path.isdir(p):
            for root, dirs, names in os.walk(p):
                dirs[:] = sorted(d for d in dirs if not d.startswith("."))
                files.extend(os.path.join(root, n) for n in sorted(names) if n.endswith(".py"))
        elif os.path.isfile(p):
            files.append(p)
        else:
            raise FileNotFoundError(p)
    return sorted(set(files))


def main():
    parser = argparse.ArgumentParser(
        description="Flag Python functions and classes whose shape suggests "
                    "they are hard to read (long, deeply nested, many "
                    "parameters, branchy, conjunction names, long classes).")
    parser.add_argument("paths", nargs="+", help="Python files or directories")
    parser.add_argument("--max-body-lines", type=int, default=9,
                        help="flag functions with more body lines (default 9)")
    parser.add_argument("--max-nesting", type=int, default=2,
                        help="flag deeper block nesting (default 2)")
    parser.add_argument("--max-params", type=int, default=4,
                        help="flag more parameters (default 4)")
    parser.add_argument("--max-complexity", type=int, default=5,
                        help="flag higher cyclomatic complexity (default 5)")
    parser.add_argument("--max-class-lines", type=int, default=60,
                        help="flag longer classes, roughly one screen (default 60)")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    parser.add_argument("--fail-on-findings", action="store_true",
                        help="exit 1 when anything is flagged")
    args = parser.parse_args()

    limits = {"body_lines": args.max_body_lines, "max_nesting": args.max_nesting,
              "params": args.max_params, "complexity": args.max_complexity,
              "class_lines": args.max_class_lines}
    try:
        files = collect_files(args.paths)
    except FileNotFoundError as exc:
        print("error: no such path: %s" % exc, file=sys.stderr)
        return 2

    findings, errors = [], []
    for f in files:
        try:
            findings.extend(analyze_file(f, limits))
        except (SyntaxError, UnicodeDecodeError) as exc:
            errors.append({"file": f, "error": str(exc)})
    findings.sort(key=lambda x: (x["file"], x["line"], x["name"]))

    if args.json:
        print(json.dumps({"limits": limits, "files_scanned": len(files),
                          "findings": findings, "parse_errors": errors}, indent=2))
    else:
        for item in findings:
            print("%s:%d %s %s  %s" % (item["file"], item["line"], item["kind"],
                                       item["name"], "; ".join(item["issues"])))
        for err in errors:
            print("%s: parse error: %s" % (err["file"], err["error"]))
        print("summary: files=%d flagged=%d parse_errors=%d" % (len(files), len(findings), len(errors)))

    return 1 if (args.fail_on_findings and findings) else 0


if __name__ == "__main__":
    sys.exit(main())
