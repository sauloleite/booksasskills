#!/usr/bin/env python3
"""WCAG 2.x color contrast checker for foreground/background pairs.

Inputs
  - One or more positional pairs written as FG:BG, each color a hex value
    (#RGB or #RRGGBB, leading '#' optional), e.g. "#767676:#ffffff".
  - Or --file PATH: a text/CSV file with one pair per line ("fg,bg" or
    "fg:bg"); blank lines and lines starting with '#' followed by a space
    are skipped. A third optional column is used as a label.
  - --json switches output to JSON.

Outputs
  For each pair: relative luminance of both colors, the contrast ratio
  (rounded to 2 decimals), and PASS/FAIL for:
    AA normal text   >= 4.5     AA large text   >= 3.0
    AAA normal text  >= 7.0     AAA large text  >= 4.5
    UI components / graphical objects (WCAG 1.4.11) >= 3.0
  "Large" text means at least 18pt (24px) regular or 14pt (~18.66px) bold.
  Exit code is 1 if any pair fails AA normal text and --strict is given.

Formulas (WCAG 2.x)
  channel c in [0,1]: c <= 0.04045 ? c/12.92 : ((c+0.055)/1.055)**2.4
  L = 0.2126 R + 0.7152 G + 0.0722 B
  ratio = (L_lighter + 0.05) / (L_darker + 0.05)

Deterministic, standard library only, no network access.
"""
import argparse
import json
import sys

THRESHOLDS = [
    ("AA_normal", 4.5),
    ("AA_large", 3.0),
    ("AAA_normal", 7.0),
    ("AAA_large", 4.5),
    ("UI_component", 3.0),
]


def parse_hex(value):
    v = value.strip().lstrip("#")
    if len(v) == 3:
        v = "".join(ch * 2 for ch in v)
    if len(v) != 6:
        raise ValueError(f"not a hex color: {value!r}")
    try:
        return tuple(int(v[i:i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        raise ValueError(f"not a hex color: {value!r}") from None


def linearize(channel):
    c = channel / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(rgb):
    r, g, b = (linearize(x) for x in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(fg, bg):
    l1, l2 = luminance(fg), luminance(bg)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def evaluate(fg_s, bg_s, label=""):
    fg, bg = parse_hex(fg_s), parse_hex(bg_s)
    ratio = contrast_ratio(fg, bg)
    # Compare on the unrounded value so 4.499 never passes as 4.5.
    checks = {name: ratio >= t for name, t in THRESHOLDS}
    return {
        "label": label,
        "fg": fg_s,
        "bg": bg_s,
        "fg_luminance": round(luminance(fg), 4),
        "bg_luminance": round(luminance(bg), 4),
        "ratio": round(ratio, 2),
        "checks": checks,
    }


def split_pair(text):
    sep = "," if "," in text else ":"
    parts = [p.strip() for p in text.split(sep)]
    if len(parts) < 2:
        raise ValueError(f"expected FG{sep}BG, got {text!r}")
    return parts[0], parts[1], (parts[2] if len(parts) > 2 else "")


def read_file(path):
    pairs = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            s = line.strip()
            if not s or s.startswith("# ") or s.lower().startswith("fg"):
                continue
            pairs.append(split_pair(s))
    return pairs


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Compute WCAG contrast ratios and AA/AAA pass/fail for color pairs.")
    ap.add_argument("pairs", nargs="*", help='pairs like "#333:#fff" or "333,fff"')
    ap.add_argument("--file", help="file with one fg,bg[,label] pair per line")
    ap.add_argument("--json", action="store_true", help="emit JSON")
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 if any pair fails AA for normal text")
    args = ap.parse_args(argv)

    pairs = [split_pair(p) for p in args.pairs]
    if args.file:
        pairs += read_file(args.file)
    if not pairs:
        ap.error("give at least one FG:BG pair or --file")

    try:
        results = [evaluate(*p) for p in pairs]
    except ValueError as exc:
        ap.error(str(exc))
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        names = [n for n, _ in THRESHOLDS]
        print(f"{'pair':<28}{'ratio':>7}  " + "  ".join(f"{n:<12}" for n in names))
        for r in results:
            name = r["label"] or f"{r['fg']} on {r['bg']}"
            marks = "  ".join(f"{'PASS' if r['checks'][n] else 'FAIL':<12}" for n in names)
            print(f"{name:<28}{r['ratio']:>7.2f}  {marks}")
    if args.strict and any(not r["checks"]["AA_normal"] for r in results):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
