"""Rebuild the ai-engineering-complete skill bundle from the chapter skills.

Usage: python3 tools/build_complete.py   (run from the book folder or anywhere)

What it does:
- copies every chapter's references/*.md (except source-map.md) into
  ai-engineering-complete/references/chNN-<name>.md
- merges the chapter source maps into references/source-maps.md
- copies every chapter's scripts/*.py into ai-engineering-complete/scripts/
- regenerates the router section of ai-engineering-complete/SKILL.md between
  the BEGIN/END GENERATED markers, reusing each chapter's "read when" lines.
Hand-written files in the bundle (SKILL.md text outside the markers and
references/lifecycle-playbook.md) are preserved.
"""
import glob
import os
import re
import shutil

BOOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BOOK, "ai-engineering-complete")
KEEP = {"lifecycle-playbook.md"}
BEGIN = "<!-- BEGIN GENERATED: run tools/build_complete.py to refresh -->"
END = "<!-- END GENERATED -->"


def chapter_dirs():
    return sorted(d for d in glob.glob(os.path.join(BOOK, "ai-eng-ch*")) if os.path.isdir(d))


def chapter_tag(d):
    return re.search(r"ai-eng-(ch\d\d)", d).group(1)


TITLES = {
    "ch01": "Introduction to Building AI Applications with Foundation Models",
    "ch02": "Understanding Foundation Models",
    "ch03": "Evaluation Methodology",
    "ch04": "Evaluate AI Systems",
    "ch05": "Prompt Engineering",
    "ch06": "RAG and Agents",
    "ch07": "Finetuning",
    "ch08": "Dataset Engineering",
    "ch09": "Inference Optimization",
    "ch10": "AI Engineering Architecture and User Feedback",
}


def chapter_title(d):
    return TITLES.get(chapter_tag(d), os.path.basename(d))


def docstring_first_line(path):
    text = open(path, encoding="utf-8").read()
    m = re.search(r'^[rRuU]?("""|\'\'\')(.*?)\1', text, re.S | re.M)
    return m.group(2).strip().splitlines()[0].strip() if m else ""


def main():
    ref_dir, scr_dir = os.path.join(OUT, "references"), os.path.join(OUT, "scripts")
    os.makedirs(ref_dir, exist_ok=True)
    os.makedirs(scr_dir, exist_ok=True)
    for f in os.listdir(ref_dir):
        if f not in KEEP:
            os.remove(os.path.join(ref_dir, f))
    for f in os.listdir(scr_dir):
        os.remove(os.path.join(scr_dir, f))

    router = ["## References by chapter", "",
              "Each link is one level deep; read only the files whose description matches the task.", ""]
    scripts = ["## Scripts", "",
               "Python 3 standard library only; run any script with `--help` for its arguments and an example.", "",
               "| Script | Purpose |", "|---|---|"]
    maps = ["# Source maps: book sections to reference files", "",
            "File names below are the chapter-prefixed names used in this folder.", ""]

    for d in chapter_dirs():
        tag = chapter_tag(d)
        skill = open(os.path.join(d, "SKILL.md"), encoding="utf-8").read()
        router.append(f"### {tag.upper()}: {chapter_title(d)}")
        router.append("")
        for ref in sorted(glob.glob(os.path.join(d, "references", "*.md"))):
            name = os.path.basename(ref)
            if name == "source-map.md":
                body = open(ref, encoding="utf-8").read()
                for other in glob.glob(os.path.join(d, "references", "*.md")):
                    o = os.path.basename(other)
                    if o != "source-map.md":
                        body = re.sub(rf"(?<![\w-]){re.escape(o)}", f"{tag}-{o}", body)
                body = re.sub(r"^# ", "## ", body, flags=re.M)
                maps += [body.strip(), ""]
                continue
            new = f"{tag}-{name}"
            shutil.copyfile(ref, os.path.join(ref_dir, new))
            m = re.search(rf"\]\(references/{re.escape(name)}\)\s*:?\s*(.*)", skill)
            when = m.group(1).strip() if m else ""
            router.append(f"- [{new}](references/{new}): {when}".rstrip(": "))
        router.append("")
        for s in sorted(glob.glob(os.path.join(d, "scripts", "*.py"))):
            shutil.copyfile(s, os.path.join(scr_dir, os.path.basename(s)))
            scripts.append(f"| `scripts/{os.path.basename(s)}` ({tag}) | {docstring_first_line(s)} |")

    router.append("Merged section maps for all chapters: [source-maps.md](references/source-maps.md).")
    open(os.path.join(ref_dir, "source-maps.md"), "w", encoding="utf-8").write("\n".join(maps).rstrip() + "\n")

    path = os.path.join(OUT, "SKILL.md")
    text = open(path, encoding="utf-8").read()
    generated = "\n".join([BEGIN, "", *router, "", *scripts, "", END])
    text = re.sub(re.escape(BEGIN) + r".*?" + re.escape(END), lambda _: generated, text, flags=re.S)
    open(path, "w", encoding="utf-8").write(text)
    print(f"references: {len(os.listdir(ref_dir))}, scripts: {len(os.listdir(scr_dir))}")


if __name__ == "__main__":
    main()
