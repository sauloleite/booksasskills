#!/usr/bin/env python3
"""Rank files in an unfamiliar repository by change activity, from git history.

Purpose: when you join an existing codebase, version control history tells you
where the action is. This script summarizes `git log --numstat` output so you
can see which files change most, how many people touch them, how recently they
changed, and which files tend to change together (temporal coupling). Use it to
pick a first area to study, to decide whether a refactor is worth doing now
(busy, multi-author files) or can wait (stable, rarely touched files), and to
spot hidden dependencies that the folder structure does not show.

Input (file path or stdin), produced by either of:
    git log --numstat --date=iso > log.txt                        (default format)
    git log --numstat --date=short --pretty=format:'--%h--%ad--%aN' > log.txt
Merge commits without numstat lines are ignored. Renames written as
`dir/{old => new}/f.py` or `old => new` are credited to the new path, and,
because git log lists newest commits first, older history recorded under the
old name is folded into the new name too (do not pass --reverse logs).

Output: plain-text tables (or JSON with --json):
    1. Hotspots: commits, lines added+deleted (churn), distinct authors,
       last change date, commits inside the recent window, per file.
    2. Temporal coupling: file pairs that changed in the same commit at least
       --min-shared times, with degree = shared / mean(commits of both) * 100.
"Recent" is measured back from the newest commit in the input, not from the
wall clock, so results are deterministic for a given log.

Examples:
    git log --numstat --date=iso | python3 git_hotspots.py
    python3 git_hotspots.py log.txt --top 15 --recent-days 90 --min-shared 3
"""
import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from itertools import combinations

NUMSTAT = re.compile(r"^(\d+|-)\t(\d+|-)\t(.+)$")
CUSTOM = re.compile(r"^--([0-9a-f]+)--(.+?)--(.*)$")
DATE_FORMATS = ("%Y-%m-%d %H:%M:%S %z", "%a %b %d %H:%M:%S %Y %z", "%Y-%m-%d")


def parse_date(text):
    text = text.strip()
    for fmt in DATE_FORMATS:
        try:
            dt = datetime.strptime(text, fmt)
            return dt if dt.tzinfo is None else dt.astimezone(timezone.utc).replace(tzinfo=None)
        except ValueError:
            continue
    try:
        dt = datetime.fromisoformat(text)
        return dt if dt.tzinfo is None else dt.astimezone(timezone.utc).replace(tzinfo=None)
    except ValueError:
        return None


def resolve_rename(path):
    """Return (old_path, new_path) for git rename notation, else (None, path)."""
    brace = re.search(r"\{(.*?) => (.*?)\}", path)
    if brace:
        def build(mid):
            return re.sub(r"/{2,}", "/", path[:brace.start()] + mid + path[brace.end():]).strip("/")
        return build(brace.group(1)), build(brace.group(2))
    if " => " in path:
        old, new = path.split(" => ", 1)
        return old, new
    return None, path


def parse_log(lines):
    commits, cur, alias = [], None, {}

    def close():
        if cur and cur["files"]:
            commits.append(cur)

    for raw in lines:
        line = raw.rstrip("\n")
        m = CUSTOM.match(line)
        if m:
            close()
            cur = {"sha": m.group(1), "date": parse_date(m.group(2)), "author": m.group(3).strip(), "files": {}}
            continue
        if line.startswith("commit "):
            close()
            cur = {"sha": line.split()[1], "date": None, "author": "", "files": {}}
            continue
        if cur is None:
            continue
        if line.startswith("Author:"):
            cur["author"] = re.sub(r"\s*<[^>]*>\s*$", "", line[7:]).strip()
        elif line.startswith("Date:"):
            cur["date"] = parse_date(line[5:])
        else:
            m = NUMSTAT.match(line)
            if m:
                added = 0 if m.group(1) == "-" else int(m.group(1))
                deleted = 0 if m.group(2) == "-" else int(m.group(2))
                old_path, path = resolve_rename(m.group(3))
                path = alias.get(path, path)
                if old_path:
                    alias[old_path] = path
                prev = cur["files"].get(path, 0)
                cur["files"][path] = prev + added + deleted
    close()
    return commits


def analyze(commits, recent_days, min_shared, max_files):
    stats = defaultdict(lambda: {"commits": 0, "churn": 0, "authors": set(), "last": None, "recent": 0})
    dates = [c["date"] for c in commits if c["date"]]
    newest = max(dates) if dates else None
    cutoff = newest - timedelta(days=recent_days) if newest else None
    pairs = Counter()
    for c in commits:
        for path, churn in c["files"].items():
            s = stats[path]
            s["commits"] += 1
            s["churn"] += churn
            if c["author"]:
                s["authors"].add(c["author"])
            if c["date"]:
                if s["last"] is None or c["date"] > s["last"]:
                    s["last"] = c["date"]
                if c["date"] >= cutoff:
                    s["recent"] += 1
        if len(c["files"]) <= max_files:
            for a, b in combinations(sorted(c["files"]), 2):
                pairs[(a, b)] += 1
    hotspots = [
        {
            "file": f,
            "commits": s["commits"],
            "churn": s["churn"],
            "authors": len(s["authors"]),
            "last_change": s["last"].strftime("%Y-%m-%d") if s["last"] else "",
            "recent_commits": s["recent"],
        }
        for f, s in stats.items()
    ]
    hotspots.sort(key=lambda h: (-h["commits"], -h["churn"], h["file"]))
    coupling = []
    for (a, b), shared in pairs.items():
        if shared < min_shared:
            continue
        mean = (stats[a]["commits"] + stats[b]["commits"]) / 2
        coupling.append({"file_a": a, "file_b": b, "shared": shared, "degree": round(100 * shared / mean)})
    coupling.sort(key=lambda p: (-p["degree"], -p["shared"], p["file_a"], p["file_b"]))
    return {
        "commits_analyzed": len(commits),
        "newest_commit": newest.strftime("%Y-%m-%d") if newest else "",
        "recent_window_days": recent_days,
        "hotspots": hotspots,
        "coupling": coupling,
    }


def print_report(result, top):
    print(f"Commits analyzed: {result['commits_analyzed']}  newest: {result['newest_commit']}  "
          f"recent window: {result['recent_window_days']} days")
    print("\nHOTSPOTS (most-changed files first)")
    hdr = f"{'commits':>7} {'churn':>7} {'authors':>7} {'recent':>6}  {'last':10}  file"
    print(hdr)
    for h in result["hotspots"][:top]:
        print(f"{h['commits']:>7} {h['churn']:>7} {h['authors']:>7} {h['recent_commits']:>6}  "
              f"{h['last_change']:10}  {h['file']}")
    print("\nTEMPORAL COUPLING (files that change together)")
    if not result["coupling"]:
        print("  none at the current --min-shared threshold")
    for p in result["coupling"][:top]:
        print(f"  {p['degree']:>3}%  shared={p['shared']:<3} {p['file_a']}  <->  {p['file_b']}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("logfile", nargs="?", help="git log --numstat output; omit or '-' for stdin")
    ap.add_argument("--top", type=int, default=20, help="rows per table (default 20)")
    ap.add_argument("--recent-days", type=int, default=90, help="recent window before newest commit (default 90)")
    ap.add_argument("--min-shared", type=int, default=2, help="min co-changes to report a pair (default 2)")
    ap.add_argument("--max-files", type=int, default=30,
                    help="skip commits touching more files than this for coupling (bulk edits; default 30)")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of tables")
    args = ap.parse_args()
    if args.logfile and args.logfile != "-":
        with open(args.logfile, encoding="utf-8", errors="replace") as fh:
            lines = fh.readlines()
    else:
        lines = sys.stdin.readlines()
    result = analyze(parse_log(lines), args.recent_days, args.min_shared, args.max_files)
    if args.json:
        json.dump(result, sys.stdout, indent=2)
        print()
    else:
        print_report(result, args.top)


if __name__ == "__main__":
    main()
