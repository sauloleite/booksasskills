#!/usr/bin/env python3
"""Check a layered architecture's access rules and sinkhole share.

Inputs
  --spec FILE   JSON file with:
      "layers": ordered top to bottom, each {"name": str, "open": bool}
      "dependencies" (optional): list of {"from": str, "to": str, "count": int?}
                   observed calls between layers (e.g. from a dependency scan)
      "requests" (optional): {"total": int, "pass_through": int}
                   number of request types (or calls) and how many do no work
  --total N --pass-through M   sinkhole numbers without a spec file
  --emit-allowed               print the allowed-access map implied by the
                               open/closed flags (feed it to a fitness function)
  --json                       machine-readable output

Rules applied
  A downward call from layer i to layer j is allowed only if every layer
  strictly between them is open. Upward calls are always violations.
  Same-layer calls are ignored. Sinkhole share <= 20% is acceptable,
  >= 80% suggests the layered style is a poor fit, anything between needs review.

Output
  Text or JSON report. Exit code 1 if any dependency violates the rules,
  2 on input errors, otherwise 0.
"""
import argparse
import json
import sys


def allowed_map(layers):
    """Return {layer: [layers it may call]} from ordered open/closed flags."""
    names = [l["name"] for l in layers]
    result = {}
    for i, name in enumerate(names):
        targets = []
        for j in range(i + 1, len(names)):
            targets.append(names[j])
            if not layers[j].get("open", False):
                break  # cannot skip a closed layer
        result[name] = targets
    return result


def check_dependencies(layers, deps):
    names = [l["name"] for l in layers]
    index = {n: i for i, n in enumerate(names)}
    allowed = allowed_map(layers)
    violations, ok = [], []
    for d in deps:
        src, dst, cnt = d["from"], d["to"], int(d.get("count", 1))
        for n in (src, dst):
            if n not in index:
                raise ValueError(f"unknown layer in dependency: {n}")
        if src == dst:
            continue
        if index[dst] < index[src]:
            violations.append({"from": src, "to": dst, "count": cnt,
                               "reason": "upward call"})
        elif dst not in allowed[src]:
            skipped = [names[k] for k in range(index[src] + 1, index[dst])
                       if not layers[k].get("open", False)]
            violations.append({"from": src, "to": dst, "count": cnt,
                               "reason": "skips closed layer(s): " + ", ".join(skipped)})
        else:
            ok.append({"from": src, "to": dst, "count": cnt})
    return ok, violations


def sinkhole(total, passthrough):
    if total <= 0 or passthrough < 0 or passthrough > total:
        raise ValueError("need total > 0 and 0 <= pass_through <= total")
    share = 100.0 * passthrough / total
    if share <= 20:
        verdict = "acceptable (within the ~20% normal band)"
    elif share >= 80:
        verdict = "style mismatch likely (~80% or more are pass-through)"
    else:
        verdict = "review: consider opening specific layers or reconsidering the style"
    return {"total": total, "pass_through": passthrough,
            "share_pct": round(share, 1), "verdict": verdict}


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--spec", help="JSON spec file (see module docstring)")
    p.add_argument("--total", type=int, help="total request types or calls")
    p.add_argument("--pass-through", type=int, dest="pass_through",
                   help="how many of them are pass-through (sinkhole)")
    p.add_argument("--emit-allowed", action="store_true",
                   help="print allowed-access map from open/closed flags")
    p.add_argument("--json", action="store_true", help="JSON output")
    a = p.parse_args()

    report = {}
    try:
        spec = {}
        if a.spec:
            with open(a.spec) as fh:
                spec = json.load(fh)
        layers = spec.get("layers", [])
        if layers:
            if len({l["name"] for l in layers}) != len(layers):
                raise ValueError("duplicate layer names")
            if a.emit_allowed or not spec.get("dependencies"):
                report["allowed"] = allowed_map(layers)
            if spec.get("dependencies"):
                ok, bad = check_dependencies(layers, spec["dependencies"])
                report["permitted"] = ok
                report["violations"] = bad
        req = spec.get("requests")
        if a.total is not None or a.pass_through is not None:
            if a.total is None or a.pass_through is None:
                raise ValueError("--total and --pass-through go together")
            req = {"total": a.total, "pass_through": a.pass_through}
        if req:
            report["sinkhole"] = sinkhole(int(req["total"]), int(req["pass_through"]))
        if not report:
            raise ValueError("nothing to do: give --spec and/or --total/--pass-through")
    except (ValueError, KeyError, OSError, json.JSONDecodeError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    if a.json:
        print(json.dumps(report, indent=2))
    else:
        if "allowed" in report:
            print("Allowed access (caller -> may call):")
            for k, v in report["allowed"].items():
                print(f"  {k} -> {', '.join(v) if v else '(none)'}")
        if "violations" in report:
            print(f"Permitted dependencies: {len(report['permitted'])}")
            print(f"Violations: {len(report['violations'])}")
            for v in report["violations"]:
                print(f"  {v['from']} -> {v['to']} (x{v['count']}): {v['reason']}")
        if "sinkhole" in report:
            s = report["sinkhole"]
            print(f"Sinkhole share: {s['pass_through']}/{s['total']} = "
                  f"{s['share_pct']}% -> {s['verdict']}")
    return 1 if report.get("violations") else 0


if __name__ == "__main__":
    sys.exit(main())
