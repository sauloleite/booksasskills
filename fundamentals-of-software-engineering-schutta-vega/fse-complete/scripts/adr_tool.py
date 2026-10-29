#!/usr/bin/env python3
"""Create and lint Architectural Decision Records (ADRs) kept as Markdown files.

Subcommands
-----------
new    Create the next numbered ADR (NNN-slug.md) in a directory from a built-in
       template with sections Status, Context, Options, Decision, Consequences,
       Governance and Notes. With --supersedes NNN, the new ADR records which
       decision it replaces and the old ADR's status line is rewritten to
       "Superseded by NNN" (the only edit an accepted ADR should ever receive).
lint   Check every NNN-*.md file in a directory and report problems:
       - file name and H1 heading must carry the same three-digit ID
       - duplicate IDs and gaps in the sequence
       - required sections missing or left empty / as template placeholders
       - status not one of: Request for comment, Proposed, Accepted, Superseded
       - "Superseded" must name an existing, different ADR ID
       - Accepted ADRs with no Governance content (how is it enforced?)
index  Print a Markdown table (ID, title, status) of all ADRs, sorted by ID.

Inputs:  a directory of ADR Markdown files (created if missing for `new`).
Outputs: `new` prints the created path; `lint` prints one line per finding
         (ERROR or WARN) and exits 1 if any ERROR was found, else 0;
         `index` prints the table to stdout.
Deterministic: dates are only written when passed with --date.
Stdlib only, no network.
"""
import argparse
import os
import re
import sys

SECTIONS = ["Status", "Context", "Options", "Decision", "Consequences",
            "Governance", "Notes"]
STATUSES = ["Request for comment", "Proposed", "Accepted", "Superseded"]
PLACEHOLDER = "TODO"
FILE_RE = re.compile(r"^(\d{3})-([a-z0-9-]+)\.md$")
H1_RE = re.compile(r"^#\s+(\d{3})\.\s+(.+?)\s*$", re.M)

TEMPLATE = """# {id}. {title}

## Status

{status}

## Context

TODO: forces, constraints, quality attributes at stake, who is affected.
Write it for a reader on their first day on the project.

## Options

TODO: each option considered, with why any were ruled out early.

## Decision

TODO: what was chosen, why, and why the other options lost.

## Consequences

TODO: positive and negative effects, new risks, follow-up work.

## Governance

TODO: how compliance is checked (fitness functions, reviews, alerts).

## Notes

- Authors: {authors}
- Created: {date}
{extra}"""


def slugify(text):
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "decision"


def list_adrs(directory):
    found = []
    if not os.path.isdir(directory):
        return found
    for name in sorted(os.listdir(directory)):
        m = FILE_RE.match(name)
        if m:
            found.append((m.group(1), name))
    return found


def parse_sections(text):
    """Return {section_name: body_text} for level-2 headings."""
    parts = re.split(r"^##\s+(.+?)\s*$", text, flags=re.M)
    out = {}
    for i in range(1, len(parts) - 1, 2):
        out[parts[i].strip()] = parts[i + 1].strip()
    return out


def status_of(sections):
    body = sections.get("Status", "")
    return body.splitlines()[0].strip() if body else ""


def cmd_new(args):
    os.makedirs(args.dir, exist_ok=True)
    existing = list_adrs(args.dir)
    ids = {i for i, _ in existing}
    next_id = "%03d" % (max([int(i) for i in ids], default=0) + 1)
    extra = ""
    if args.supersedes:
        old = args.supersedes.zfill(3)
        matches = [n for i, n in existing if i == old]
        if not matches:
            sys.exit("error: ADR %s not found in %s" % (old, args.dir))
        extra = "- Supersedes: %s\n" % old
        path_old = os.path.join(args.dir, matches[0])
        with open(path_old, encoding="utf-8") as fh:
            text = fh.read()
        new_text, n = re.subn(r"(^##\s+Status\s*\n+)([^\n]*)",
                              r"\g<1>Superseded by %s" % next_id, text,
                              count=1, flags=re.M)
        if n == 0:
            sys.exit("error: ADR %s has no Status section" % old)
        with open(path_old, "w", encoding="utf-8") as fh:
            fh.write(new_text)
        print("updated %s -> Superseded by %s" % (path_old, next_id))
    body = TEMPLATE.format(id=next_id, title=args.title.strip(),
                           status=args.status, authors=args.authors,
                           date=args.date, extra=extra)
    path = os.path.join(args.dir, "%s-%s.md" % (next_id, slugify(args.title)))
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(body)
    print(path)
    return 0


def lint_one(path, fname_id, all_ids):
    findings = []
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    h1 = H1_RE.search(text)
    if not h1:
        findings.append(("ERROR", "missing H1 of form '# NNN. Title'"))
    elif h1.group(1) != fname_id:
        findings.append(("ERROR", "H1 id %s does not match file id %s"
                         % (h1.group(1), fname_id)))
    sections = parse_sections(text)
    for sec in SECTIONS:
        body = sections.get(sec)
        if body is None:
            findings.append(("ERROR", "missing section '%s'" % sec))
        elif not body or body.startswith(PLACEHOLDER):
            level = "ERROR" if sec in ("Context", "Decision") else "WARN"
            findings.append((level, "section '%s' is empty or placeholder"
                             % sec))
    status = status_of(sections)
    if status:
        base = next((s for s in STATUSES
                     if status.lower().startswith(s.lower())), None)
        if base is None:
            findings.append(("ERROR", "unknown status '%s' (allowed: %s)"
                             % (status, ", ".join(STATUSES))))
        elif base == "Superseded":
            ref = re.search(r"(\d{3})", status)
            if not ref:
                findings.append(("ERROR", "Superseded status must name the "
                                 "replacing ADR id"))
            elif ref.group(1) == fname_id:
                findings.append(("ERROR", "ADR cannot supersede itself"))
            elif ref.group(1) not in all_ids:
                findings.append(("ERROR", "superseding ADR %s does not exist"
                                 % ref.group(1)))
        elif base == "Accepted":
            gov = sections.get("Governance", "")
            if not gov or gov.startswith(PLACEHOLDER):
                findings.append(("ERROR", "Accepted ADR has no governance "
                                 "(how will compliance be checked?)"))
    return findings


def cmd_lint(args):
    adrs = list_adrs(args.dir)
    if not adrs:
        print("no ADR files (NNN-slug.md) found in %s" % args.dir)
        return 1
    errors = 0
    ids = [i for i, _ in adrs]
    seen = set()
    for i in ids:
        if i in seen:
            print("ERROR %s: duplicate id" % i)
            errors += 1
        seen.add(i)
    nums = sorted({int(i) for i in ids})
    missing = sorted(set(range(1, nums[-1] + 1)) - set(nums))
    for m in missing:
        print("WARN  %03d: gap in sequence (deleted ADR? keep and supersede "
              "instead)" % m)
    for fid, name in adrs:
        for level, msg in lint_one(os.path.join(args.dir, name), fid, seen):
            print("%-5s %s: %s" % (level, name, msg))
            if level == "ERROR":
                errors += 1
    print("checked %d ADR(s): %d error(s)" % (len(adrs), errors))
    return 1 if errors else 0


def cmd_index(args):
    print("| ID | Title | Status |")
    print("|----|-------|--------|")
    for fid, name in list_adrs(args.dir):
        with open(os.path.join(args.dir, name), encoding="utf-8") as fh:
            text = fh.read()
        h1 = H1_RE.search(text)
        title = h1.group(2) if h1 else name
        print("| %s | %s | %s |" % (fid, title,
                                     status_of(parse_sections(text)) or "?"))
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    n = sub.add_parser("new", help="create the next numbered ADR")
    n.add_argument("--dir", required=True, help="ADR directory")
    n.add_argument("--title", required=True, help="descriptive decision title")
    n.add_argument("--status", default="Proposed", choices=STATUSES[:3],
                   help="initial status (default: Proposed)")
    n.add_argument("--authors", default="TBD", help="author names")
    n.add_argument("--date", default="YYYY-MM-DD", help="creation date")
    n.add_argument("--supersedes", help="id of the ADR this one replaces")
    n.set_defaults(func=cmd_new)
    lt = sub.add_parser("lint", help="check ADRs for structure and status")
    lt.add_argument("--dir", required=True, help="ADR directory")
    lt.set_defaults(func=cmd_lint)
    ix = sub.add_parser("index", help="print a Markdown index of ADRs")
    ix.add_argument("--dir", required=True, help="ADR directory")
    ix.set_defaults(func=cmd_index)
    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
