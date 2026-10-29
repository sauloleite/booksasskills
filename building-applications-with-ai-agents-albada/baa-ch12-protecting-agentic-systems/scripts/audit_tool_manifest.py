#!/usr/bin/env python3
"""Static audit of an agent tool manifest for risky, under-guarded permissions.

Applies the least-privilege safeguards from Chapter 12 of Albada's
"Building Applications with AI Agents": scoped roles, policy gates before
execution, sandboxing, rate limits and human escalation for consequential
actions. Defensive review only; it never executes or calls any tool.

INPUT: a JSON file, either a list of tools or {"tools": [...]}. Each tool:
  {
    "name": "send_payment",                 # required
    "capabilities": ["payment", "network"], # categories, see RISK below
    "requires_approval": true,              # human/quorum approval before run
    "scope": {"max_amount": 500},           # any non-empty constraint object
    "sandboxed": false,                     # runs in isolated env/container
    "rate_limit": "10/min",                 # any non-empty value
    "agents": ["billing"]                   # roles allowed to call it
  }
Unknown capability names are treated as low risk and reported as INFO.

OUTPUT: a text report (or JSON with --json) listing findings per tool with
severity HIGH / MEDIUM / LOW / INFO. Exit code 1 if any HIGH finding exists,
else 0, so it can gate CI.
"""
import argparse
import json
import sys

# capability -> (risk weight, needs approval, needs scope, needs sandbox)
RISK = {
    "payment":        (3, True,  True,  False),
    "delete":         (3, True,  True,  False),
    "exec":           (3, True,  True,  True),
    "credential":     (3, True,  True,  False),
    "write":          (2, False, True,  False),
    "external_email": (2, True,  True,  False),
    "messaging":      (2, False, True,  False),
    "network":        (2, False, True,  True),
    "file_read":      (1, False, True,  False),
    "read":           (1, False, False, False),
}
SEV_ORDER = {"HIGH": 0, "MEDIUM": 1, "LOW": 2, "INFO": 3}


def audit_tool(tool):
    name = tool.get("name", "<unnamed>")
    caps = [str(c).lower() for c in tool.get("capabilities", [])]
    findings = []

    def add(sev, msg):
        findings.append({"tool": name, "severity": sev, "issue": msg})

    if not caps:
        add("MEDIUM", "no capabilities declared; cannot assess risk")
    known = [c for c in caps if c in RISK]
    for c in caps:
        if c not in RISK:
            add("INFO", f"unrecognized capability '{c}' treated as low risk")
    top = max((RISK[c][0] for c in known), default=0)

    for c in known:
        weight, need_appr, need_scope, need_box = RISK[c]
        sev = "HIGH" if weight == 3 else "MEDIUM" if weight == 2 else "LOW"
        if need_appr and not tool.get("requires_approval"):
            add(sev, f"'{c}' action runs without approval or escalation")
        if need_scope and not tool.get("scope"):
            add(sev, f"'{c}' has no scope constraint (amount cap, path, allowlist)")
        if need_box and not tool.get("sandboxed"):
            add(sev, f"'{c}' not sandboxed; blast radius not contained")

    if top >= 2 and not tool.get("rate_limit"):
        add("MEDIUM", "consequential tool lacks a rate limit")
    if top >= 2 and not tool.get("agents"):
        add("MEDIUM", "no agent roles listed; any agent may call it")
    if "exec" in caps and "network" in caps:
        add("HIGH", "combines code execution with network access")
    return findings


def load(path):
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    tools = data.get("tools", []) if isinstance(data, dict) else data
    if not isinstance(tools, list):
        raise ValueError("manifest must be a list or {'tools': [...]}")
    return tools


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("manifest", help="path to tool manifest JSON")
    ap.add_argument("--json", action="store_true", help="emit JSON")
    args = ap.parse_args()

    tools = load(args.manifest)
    findings = [f for t in tools for f in audit_tool(t)]
    findings.sort(key=lambda f: (SEV_ORDER[f["severity"]], f["tool"], f["issue"]))
    counts = {s: sum(f["severity"] == s for f in findings) for s in SEV_ORDER}

    if args.json:
        print(json.dumps({"tools": len(tools), "counts": counts,
                          "findings": findings}, indent=2))
    else:
        print(f"Audited {len(tools)} tools: " +
              ", ".join(f"{k}={v}" for k, v in counts.items()))
        for f in findings:
            print(f"[{f['severity']}] {f['tool']}: {f['issue']}")
        if not findings:
            print("No findings.")
    sys.exit(1 if counts["HIGH"] else 0)


if __name__ == "__main__":
    main()
