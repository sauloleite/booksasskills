#!/usr/bin/env python3
"""Scan source and config files for production-readiness risks in configuration.

Checks (heuristic, line based):
  SECRET      HIGH    literal value assigned to a secret-like key (password, api_key,
                      secret, token, private_key, ...). Placeholders such as ${VAR},
                      {{ var }}, os.environ / getenv lookups and empty values are ignored.
  LOCALHOST   MEDIUM  localhost / 127.0.0.1 / 0.0.0.0 endpoint hardcoded in a file that
                      is not clearly a dev/test/local file.
  PLAIN_HTTP  MEDIUM  http:// URL to a non-local host (production traffic should use HTTPS).
  OLD_TLS     HIGH    SSLv2/SSLv3/TLSv1.0/TLSv1.1 referenced (allow TLS 1.2 or newer only).
  DEBUG_LOG   LOW     DEBUG or TRACE log level inside a file whose name suggests prod.

Inputs : one or more files or directories (recursed). Binary files, .git, node_modules,
         virtualenvs and files over --max-bytes are skipped.
Outputs: one finding per line "SEVERITY RULE path:line  snippet" sorted by path and line,
         followed by a per-rule summary; or a JSON document with --json.
Exit code: 1 if any finding at or above --fail-on severity, else 0.

Example:
  python3 scan_config_risks.py ./my-service --fail-on HIGH
"""
import argparse
import json
import os
import re
import sys

SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build", "target"}
SEV_RANK = {"LOW": 1, "MEDIUM": 2, "HIGH": 3}

SECRET_KEY = re.compile(
    r"""(?ix)(?P<key>[\w.-]*(password|passwd|pwd|secret|api[_-]?key|apikey|token|
    private[_-]?key|access[_-]?key|client[_-]?secret)[\w.-]*)
    \s*["']?\s*[:=]\s*(?P<val>.+)$""")
PLACEHOLDER = re.compile(r"""^\s*["']?\s*(\$\{|\{\{|%\(|<|None\b|null\b|""|''|$)""", re.I)
ENV_LOOKUP = re.compile(r"environ|getenv|process\.env|\benv\(|secret_?manager|vault|keyvault", re.I)
BARE_IDENT = re.compile(r"^[A-Za-z_][\w.]*(\(\))?$")
CODE_EXT = {".py", ".java", ".js", ".ts", ".go", ".cs", ".kt", ".rb", ".php", ".scala", ".rs", ".swift"}
LOCAL_HOST = re.compile(r"\b(localhost|127\.0\.0\.1|0\.0\.0\.0)\b", re.I)
HTTP_URL = re.compile(r"http://([^\s/:'\"]+)", re.I)
OLD_TLS = re.compile(r"\b(SSLv2|SSLv3|TLSv1(\.0)?(?![.\d])|TLSv1\.1|TLS1_0|TLS1_1|TLSv1_1)\b", re.I)
DEBUG_LEVEL = re.compile(r"\b(level|log[_-]?level|logging\.level[\w.]*)\b\s*[:=]\s*[\"']?(DEBUG|TRACE)\b", re.I)
DEV_NAME = re.compile(r"(^|[\W_])(dev|local|test|tests|spec|example|sample|fixture)s?([\W_]|$)", re.I)
PROD_NAME = re.compile(r"(^|[\W_])(prod|production|live)([\W_]|$)", re.I)


def iter_files(paths, max_bytes):
    for p in paths:
        if os.path.isfile(p):
            yield p
            continue
        for root, dirs, files in os.walk(p):
            dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
            for name in sorted(files):
                full = os.path.join(root, name)
                try:
                    if os.path.getsize(full) <= max_bytes:
                        yield full
                except OSError:
                    continue


def read_text(path):
    try:
        with open(path, "rb") as fh:
            data = fh.read()
    except OSError:
        return None
    if b"\0" in data[:4096]:
        return None
    return data.decode("utf-8", errors="replace")


def literal_secret(value, is_code):
    """True when the assigned value looks like a hardcoded literal, not a lookup."""
    if is_code:
        value = value.split(";")[0]
        typed = re.match(r"^\s*[A-Za-z_][\w\[\], .|]*?\s*=\s*(.*)$", value)
        if typed:  # type annotation such as `password: str = ...`
            value = typed.group(1)
    if PLACEHOLDER.match(value) or ENV_LOOKUP.search(value):
        return False
    raw = value.strip().rstrip(",;)} ").strip()
    val = raw.strip("\"'")
    if len(val) < 3 or val.startswith(("$", "{")):
        return False
    if is_code and raw == val and BARE_IDENT.match(val):
        return False  # reference to another variable, e.g. self.pw = pw
    return True


def scan_file(path):
    text = read_text(path)
    if text is None:
        return []
    rel = path.replace("\\", "/")
    is_dev = bool(DEV_NAME.search(rel))
    is_prod = bool(PROD_NAME.search(os.path.basename(rel)))
    is_code = os.path.splitext(rel)[1].lower() in CODE_EXT
    out = []
    for no, line in enumerate(text.splitlines(), 1):
        snippet = line.strip()[:120]
        m = SECRET_KEY.search(line)
        if m and literal_secret(m.group("val"), is_code):
            out.append(("HIGH", "SECRET", rel, no, snippet))
        if OLD_TLS.search(line):
            out.append(("HIGH", "OLD_TLS", rel, no, snippet))
        if LOCAL_HOST.search(line) and not is_dev:
            out.append(("MEDIUM", "LOCALHOST", rel, no, snippet))
        for host in HTTP_URL.findall(line):
            if not LOCAL_HOST.search(host):
                out.append(("MEDIUM", "PLAIN_HTTP", rel, no, snippet))
                break
        if is_prod and DEBUG_LEVEL.search(line):
            out.append(("LOW", "DEBUG_LOG", rel, no, snippet))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+", help="files or directories to scan")
    ap.add_argument("--fail-on", choices=["LOW", "MEDIUM", "HIGH", "NONE"], default="HIGH",
                    help="exit 1 when a finding at or above this severity exists (default HIGH)")
    ap.add_argument("--max-bytes", type=int, default=1_000_000, help="skip larger files (default 1 MB)")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of text")
    args = ap.parse_args(argv)

    findings = []
    for f in iter_files(args.paths, args.max_bytes):
        findings.extend(scan_file(f))
    findings.sort(key=lambda r: (r[2], r[3], r[1]))
    summary = {}
    for sev, rule, *_ in findings:
        summary[rule] = summary.get(rule, 0) + 1

    if args.json:
        print(json.dumps({"findings": [dict(zip(("severity", "rule", "path", "line", "snippet"), r))
                                       for r in findings], "summary": summary}, indent=2))
    else:
        for sev, rule, path, no, snip in findings:
            print(f"{sev:<6} {rule:<10} {path}:{no}  {snip}")
        print(f"\n{len(findings)} finding(s)" + ("".join(f"\n  {k}: {v}" for k, v in sorted(summary.items()))))
    if args.fail_on != "NONE" and any(SEV_RANK[r[0]] >= SEV_RANK[args.fail_on] for r in findings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
