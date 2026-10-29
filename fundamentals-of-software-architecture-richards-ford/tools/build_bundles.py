"""Rebuild the theme skills and the whole-book skill from the chapter skills.

Usage: python3 tools/build_bundles.py

For every bundle in BUNDLES it:
- copies the listed chapters' references/*.md (except source-map.md) into
  <bundle>/references/chNN-<name>.md and merges their source maps into
  <bundle>/references/source-maps.md
- copies the chapters' scripts/*.py into <bundle>/scripts/
- regenerates the router section of <bundle>/SKILL.md between the
  BEGIN/END GENERATED markers, reusing each chapter's "read when" lines.
Hand-written content (SKILL.md outside the markers and any file listed in
KEEP) is preserved. Edit the chapter skills, then rerun this script.
"""
import glob
import os
import re
import shutil

BOOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PREFIX = "fsa"
KEEP = {"architecture-playbook.md"}
BEGIN = "<!-- BEGIN GENERATED: run tools/build_bundles.py to refresh -->"
END = "<!-- END GENERATED -->"

TITLES = {
    "ch01": "Introduction",
    "ch02": "Architectural Thinking",
    "ch03": "Modularity",
    "ch04": "Architectural Characteristics Defined",
    "ch05": "Identifying Architectural Characteristics",
    "ch06": "Measuring and Governing Architecture Characteristics",
    "ch07": "The Scope of Architectural Characteristics",
    "ch08": "Component-Based Thinking",
    "ch09": "Foundations of Architecture Styles",
    "ch10": "Layered Architecture Style",
    "ch11": "The Modular Monolith Architecture Style",
    "ch12": "Pipeline Architecture Style",
    "ch13": "Microkernel Architecture Style",
    "ch14": "Service-Based Architecture Style",
    "ch15": "Event-Driven Architecture Style",
    "ch16": "Space-Based Architecture Style",
    "ch17": "Orchestration-Driven Service-Oriented Architecture",
    "ch18": "Microservices Architecture",
    "ch19": "Choosing the Appropriate Architecture Style",
    "ch20": "Architectural Patterns",
    "ch21": "Architectural Decisions",
    "ch22": "Analyzing Architecture Risk",
    "ch23": "Diagramming Architecture",
    "ch24": "Making Teams Effective",
    "ch25": "Negotiation and Leadership Skills",
    "ch26": "Architectural Intersections",
    "ch27": "The Laws of Software Architecture, Revisited",
}

BUNDLES = {
    "fsa-theme-architectural-thinking": [1, 2, 3, 8, 27],
    "fsa-theme-architecture-characteristics": [4, 5, 6, 7],
    "fsa-theme-style-foundations-and-selection": [9, 19, 20],
    "fsa-theme-monolithic-styles": [10, 11, 12, 13],
    "fsa-theme-distributed-styles": [14, 15, 16, 17, 18],
    "fsa-theme-decisions-risk-diagrams": [21, 22, 23],
    "fsa-theme-teams-and-leadership": [24, 25, 26],
    "fsa-complete": list(range(1, 28)),
}


def chapter_dir(n):
    found = glob.glob(os.path.join(BOOK, f"{PREFIX}-ch{n:02d}-*"))
    if len(found) != 1:
        raise SystemExit(f"expected one folder for chapter {n}, found {found}")
    return found[0]


def docstring_first_line(path):
    text = open(path, encoding="utf-8").read()
    m = re.search(r'^[rRuU]?("""|\'\'\')(.*?)\1', text, re.S | re.M)
    return m.group(2).strip().splitlines()[0].strip() if m else ""


def build(bundle, chapters):
    out = os.path.join(BOOK, bundle)
    ref_dir, scr_dir = os.path.join(out, "references"), os.path.join(out, "scripts")
    os.makedirs(ref_dir, exist_ok=True)
    for f in os.listdir(ref_dir):
        if f not in KEEP:
            os.remove(os.path.join(ref_dir, f))
    if os.path.isdir(scr_dir):
        shutil.rmtree(scr_dir)

    router = ["## References by chapter", "",
              "Each link is one level deep; read only the files whose description matches the task.", ""]
    scripts = []
    maps = ["# Source maps: book sections to reference files", "",
            "File names below are the chapter-prefixed names used in this folder.", ""]

    for n in chapters:
        d, tag = chapter_dir(n), f"ch{n:02d}"
        skill = open(os.path.join(d, "SKILL.md"), encoding="utf-8").read()
        router += [f"### {tag.upper()}: {TITLES[tag]}", ""]
        refs = sorted(glob.glob(os.path.join(d, "references", "*.md")))
        names = [os.path.basename(r) for r in refs if os.path.basename(r) != "source-map.md"]
        for ref in refs:
            name = os.path.basename(ref)
            if name == "source-map.md":
                body = open(ref, encoding="utf-8").read()
                for o in names:
                    body = re.sub(rf"(?<![\w-]){re.escape(o)}", f"{tag}-{o}", body)
                maps += [re.sub(r"^# ", "## ", body, flags=re.M).strip(), ""]
                continue
            new = f"{tag}-{name}"
            shutil.copyfile(ref, os.path.join(ref_dir, new))
            m = re.search(rf"\]\(references/{re.escape(name)}\)\s*[:\-]?\s*(.*)", skill)
            when = m.group(1).strip() if m else ""
            router.append(f"- [{new}](references/{new})" + (f": {when}" if when else ""))
        router.append("")
        for s in sorted(glob.glob(os.path.join(d, "scripts", "*.py"))):
            os.makedirs(scr_dir, exist_ok=True)
            dest = os.path.join(scr_dir, os.path.basename(s))
            if os.path.exists(dest):
                raise SystemExit(f"script name collision: {os.path.basename(s)}")
            shutil.copyfile(s, dest)
            scripts.append(f"| `scripts/{os.path.basename(s)}` ({tag}) | {docstring_first_line(s)} |")

    router.append("Merged section maps: [source-maps.md](references/source-maps.md).")
    open(os.path.join(ref_dir, "source-maps.md"), "w", encoding="utf-8").write("\n".join(maps).rstrip() + "\n")

    block = [BEGIN, "", *router]
    if scripts:
        block += ["", "## Scripts", "",
                  "Python 3 standard library only; run any script with `--help` for its arguments.", "",
                  "| Script | Purpose |", "|---|---|", *scripts]
    block += ["", END]
    path = os.path.join(out, "SKILL.md")
    text = open(path, encoding="utf-8").read()
    if BEGIN not in text:
        raise SystemExit(f"{path} has no generated-section markers")
    text = re.sub(re.escape(BEGIN) + r".*?" + re.escape(END), lambda _: "\n".join(block), text, flags=re.S)
    open(path, "w", encoding="utf-8").write(text)
    print(f"{bundle}: {len(os.listdir(ref_dir))} references, {len(scripts)} scripts")


def main():
    for bundle, chapters in BUNDLES.items():
        build(bundle, chapters)


if __name__ == "__main__":
    main()
