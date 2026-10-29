#!/usr/bin/env python3
"""Compute afferent (Ca) and efferent (Ce) coupling per logical component.

INPUT
  A text file of dependencies, one per line, in either form:
      Source -> Target
      Source,Target
  A line holding a single name declares a component with no edges.
  Blank lines and lines starting with '#' are ignored.

  Default mode: Source/Target are component names.
  --paths mode: Source/Target are source-file paths (e.g. a/b/c/Foo.java);
  each file is mapped to its directory, treating the leaf directory as the
  logical component. Use --strip-prefix to drop a common root such as src/.

OUTPUT
  A table (or JSON with --json) listing, per component: Ca (distinct
  components depending on it), Ce (distinct components it depends on), and
  the names on each side. Dependencies inside one component are ignored and
  counted in a summary line. Output is sorted and deterministic.

EXAMPLE
  python3 component_coupling.py deps.txt
  python3 component_coupling.py class_deps.txt --paths --strip-prefix src/ --json
"""
import argparse
import json
import posixpath
import sys


def parse_line(line):
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    for sep in ("->", ","):
        if sep in line:
            left, right = line.split(sep, 1)
            return left.strip(), right.strip()
    return line, None


def to_component(name, use_paths, prefix):
    if not use_paths:
        return name
    path = name.replace("\\", "/")
    if prefix and path.startswith(prefix):
        path = path[len(prefix):]
    comp = posixpath.dirname(path)
    return comp or "(root)"


def analyze(lines, use_paths=False, prefix=""):
    comps, edges, internal = set(), set(), 0
    for raw in lines:
        parsed = parse_line(raw)
        if parsed is None:
            continue
        src, dst = parsed
        a = to_component(src, use_paths, prefix)
        comps.add(a)
        if dst is None:
            continue
        b = to_component(dst, use_paths, prefix)
        comps.add(b)
        if a == b:
            internal += 1
        else:
            edges.add((a, b))
    result = {}
    for c in sorted(comps):
        incoming = sorted(a for a, b in edges if b == c)
        outgoing = sorted(b for a, b in edges if a == c)
        result[c] = {"Ca": len(incoming), "Ce": len(outgoing),
                     "dependents": incoming, "depends_on": outgoing}
    return result, len(edges), internal


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("depfile", help="dependency list file ('-' for stdin)")
    ap.add_argument("--paths", action="store_true",
                    help="treat endpoints as file paths; component = leaf directory")
    ap.add_argument("--strip-prefix", default="", help="root prefix to drop in --paths mode")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of a table")
    args = ap.parse_args()

    fh = sys.stdin if args.depfile == "-" else open(args.depfile, encoding="utf-8")
    with fh:
        result, n_edges, internal = analyze(fh, args.paths, args.strip_prefix)

    if args.json:
        print(json.dumps({"components": result, "cross_component_edges": n_edges,
                          "internal_dependencies_ignored": internal}, indent=2, sort_keys=True))
        return
    width = max([len(c) for c in result] + [9])
    print(f"{'Component':<{width}}  {'Ca':>3}  {'Ce':>3}  dependents | depends_on")
    for c, r in result.items():
        print(f"{c:<{width}}  {r['Ca']:>3}  {r['Ce']:>3}  "
              f"{', '.join(r['dependents']) or '-'} | {', '.join(r['depends_on']) or '-'}")
    print(f"\ncomponents={len(result)} cross_component_edges={n_edges} "
          f"internal_dependencies_ignored={internal}")


if __name__ == "__main__":
    main()
