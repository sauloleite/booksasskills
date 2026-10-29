#!/usr/bin/env python3
"""saga_check.py: lint a transactional saga definition.

Based on the ideas of Chapter 12 ("Transactional Sagas") of Ford, Richards,
Sadalage and Dehghani, "Software Architecture: The Hard Parts". The script
contains no rating tables; it only applies structural checks and prints
qualitative warnings written for this skill.

INPUT: a JSON file (or "-" for stdin) shaped like:
{
  "name": "place_order",
  "communication": "sync" | "async",
  "consistency": "atomic" | "eventual",
  "coordination": "orchestrated" | "choreographed",
  "workflow_complexity": "simple" | "complex",          (optional)
  "steps": [
    {"name": "reserve_stock", "service": "inventory",
     "compensation": "release_stock",                    (optional)
     "side_effects": ["emits StockReserved event"],      (optional)
     "idempotent": true,                                  (optional)
     "user_facing": true}                                 (optional: caller must wait for it)
  ],
  "state_machine": {                                      (optional)
    "start": "START", "terminal": ["CLOSED"],
    "transitions": [{"from": "START", "to": "CREATED", "action": "..."}]
  }
}

OUTPUT: a text report (or JSON with --json) listing the identified pattern
(three-letter code: communication, consistency, coordination), steps without
compensation and what that implies for the declared consistency model,
side-effect and idempotence warnings, combination warnings, and state machine
structure problems (unreachable states, dead ends, states that cannot reach a
terminal state).

EXIT CODES: 0 = report produced; 1 = findings present and --strict given;
2 = invalid input.
"""
import argparse
import json
import sys

PATTERNS = {
    ("sync", "atomic", "orchestrated"): ("sao", "Epic Saga"),
    ("sync", "atomic", "choreographed"): ("sac", "Phone Tag Saga"),
    ("sync", "eventual", "orchestrated"): ("seo", "Fairy Tale Saga"),
    ("sync", "eventual", "choreographed"): ("sec", "Time Travel Saga"),
    ("async", "atomic", "orchestrated"): ("aao", "Fantasy Fiction Saga"),
    ("async", "atomic", "choreographed"): ("aac", "Horror Story"),
    ("async", "eventual", "orchestrated"): ("aeo", "Parallel Saga"),
    ("async", "eventual", "choreographed"): ("aec", "Anthology Saga"),
}
ALLOWED = {
    "communication": ("sync", "async"),
    "consistency": ("atomic", "eventual"),
    "coordination": ("orchestrated", "choreographed"),
}


def fail(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(2)


def load(path):
    try:
        if path == "-":
            return json.load(sys.stdin)
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read JSON: {exc}")


def validate(spec):
    if not isinstance(spec, dict):
        fail("top level must be an object")
    for key, values in ALLOWED.items():
        if spec.get(key) not in values:
            fail(f"'{key}' must be one of {values}")
    steps = spec.get("steps")
    if not isinstance(steps, list) or not steps:
        fail("'steps' must be a non-empty list")
    for i, st in enumerate(steps):
        if not isinstance(st, dict) or not st.get("name"):
            fail(f"step #{i + 1} needs a 'name'")
    wc = spec.get("workflow_complexity")
    if wc is not None and wc not in ("simple", "complex"):
        fail("'workflow_complexity' must be 'simple' or 'complex'")


def combination_notes(spec):
    comm, cons, coord = spec["communication"], spec["consistency"], spec["coordination"]
    complexity = spec.get("workflow_complexity")
    notes = []
    if cons == "atomic":
        notes.append("Atomic consistency is the strongest coupling force; confirm the business "
                     "truly cannot accept a window of partial completion.")
        if comm == "async" and coord == "choreographed":
            notes.append("Atomicity with async messages and no mediator forces every service to "
                         "track undo data for overlapping, out-of-order transactions. Consider "
                         "dropping global atomicity (aec).")
        elif comm == "async":
            notes.append("Async calls do not make an atomic saga fast; the orchestrator must track "
                         "many pending transactions and their dependencies. If speed is the goal, "
                         "relax consistency instead (aeo).")
        elif coord == "choreographed":
            notes.append("Without a mediator, the first service becomes the coordinator and every "
                         "participant needs unwind logic. Keep this for short chains with rare errors.")
        else:
            notes.append("The orchestrator waits on every participant: expect a throughput and "
                         "availability bottleneck. Keep the saga scope as small as possible.")
    if coord == "choreographed" and complexity == "complex":
        notes.append("Choreography with a complex workflow: services will absorb mediator duties. "
                     "An orchestrated variant is usually easier to reason about.")
    if coord == "orchestrated" and complexity == "simple" and cons == "eventual" and comm == "sync":
        notes.append("Simple linear workflow: a choreographed pipeline (sec, later aec) may give "
                     "more throughput if the orchestrator becomes a bottleneck.")
    if comm == "async":
        notes.append("Async communication: plan for ordering, duplicate delivery, race conditions "
                     "and queue reliability.")
    if cons == "eventual":
        notes.append("Eventual consistency: model the saga as a state machine with explicit error "
                     "states, background retries and an escalation path to humans.")
    return notes


def step_findings(spec):
    cons = spec["consistency"]
    steps = spec["steps"]
    findings = []
    missing = [s for s in steps if not s.get("compensation")]
    last = steps[-1]["name"]
    for s in missing:
        name = s["name"]
        if cons == "atomic":
            if name == last:
                findings.append(f"{name}: final step without compensation. Fine as long as its "
                                "failure triggers undo of all earlier steps, since nothing runs after it.")
            else:
                findings.append(f"{name}: no compensation in an atomic saga. If any later step fails, "
                                "this write cannot be reversed and atomicity is broken.")
        else:
            findings.append(f"{name}: no compensation. Under eventual consistency define the error "
                            "state and the forward repair (retry, resync, manual task) instead.")
    for s in steps:
        if s.get("side_effects") and cons == "atomic" and s["name"] != last:
            findings.append(f"{s['name']}: side effects ({'; '.join(s['side_effects'])}) may be "
                            "consumed before a later failure; compensating this step will not "
                            "reverse them, and there is no isolation hiding the interim state.")
        if s.get("compensation") and s.get("idempotent") is False:
            findings.append(f"{s['name']}: not idempotent, so retries of the step or of its "
                            "compensation can double-apply. Compensation can also fail: define "
                            "what happens then.")
    if cons == "atomic":
        non_user = [s["name"] for s in steps if s.get("user_facing") is False]
        if non_user:
            findings.append("Steps the caller does not own are inside the atomic boundary ("
                            + ", ".join(non_user) + "); the user is coupled to their failures. "
                            "Consider moving them to state-managed background handling.")
    return findings


def state_machine_findings(sm):
    if sm is None:
        return []
    out = []
    start = sm.get("start")
    terminal = set(sm.get("terminal") or [])
    trans = sm.get("transitions") or []
    if not start:
        out.append("state machine has no 'start' state")
    if not terminal:
        out.append("state machine has no 'terminal' states")
    graph, rev, states = {}, {}, set()
    for t in trans:
        a, b = t.get("from"), t.get("to")
        if not a or not b:
            out.append(f"transition missing from/to: {t}")
            continue
        graph.setdefault(a, set()).add(b)
        rev.setdefault(b, set()).add(a)
        states.update((a, b))
        if not t.get("action"):
            out.append(f"transition {a} -> {b} has no action")
    if start:
        states.add(start)
    states |= terminal

    def reach(origin, edges):
        seen, stack = set(origin), list(origin)
        while stack:
            for nxt in edges.get(stack.pop(), ()):
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
        return seen

    if start:
        for s in sorted(states - reach([start], graph)):
            out.append(f"state {s} is unreachable from {start}")
    for s in sorted(states - terminal):
        if not graph.get(s):
            out.append(f"state {s} is a dead end (not terminal, no outgoing transition)")
    if terminal:
        for s in sorted(states - reach(list(terminal), rev)):
            out.append(f"state {s} can never reach a terminal state")
    for s in sorted(terminal):
        if graph.get(s):
            out.append(f"terminal state {s} has outgoing transitions")
    return out


def main():
    ap = argparse.ArgumentParser(description="Check a saga definition for missing compensations, "
                                 "risky force combinations and state machine gaps.")
    ap.add_argument("spec", help="path to saga JSON, or - for stdin")
    ap.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    ap.add_argument("--strict", action="store_true", help="exit 1 if any step or state finding exists")
    args = ap.parse_args()

    spec = load(args.spec)
    validate(spec)
    key = (spec["communication"], spec["consistency"], spec["coordination"])
    code, nickname = PATTERNS[key]
    report = {
        "saga": spec.get("name", "(unnamed)"),
        "pattern_code": code,
        "pattern_nickname": nickname,
        "steps": len(spec["steps"]),
        "steps_without_compensation": [s["name"] for s in spec["steps"] if not s.get("compensation")],
        "combination_notes": combination_notes(spec),
        "step_findings": step_findings(spec),
        "state_machine_findings": state_machine_findings(spec.get("state_machine")),
    }
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"Saga: {report['saga']}")
        print(f"Pattern: {code} ({nickname}); {len(spec['steps'])} steps")
        print("Steps without compensation: " + (", ".join(report["steps_without_compensation"]) or "none"))
        for title, field in (("Combination notes", "combination_notes"),
                             ("Step findings", "step_findings"),
                             ("State machine findings", "state_machine_findings")):
            print(f"\n{title}:")
            for line in report[field] or ["none"]:
                print(f"  - {line}")
    has_findings = bool(report["step_findings"] or report["state_machine_findings"])
    sys.exit(1 if args.strict and has_findings else 0)


if __name__ == "__main__":
    main()
