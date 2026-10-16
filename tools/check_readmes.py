#!/usr/bin/env python3
"""Check required course Markdown for broken links and common rendering errors."""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [ROOT / "README.md"]
TARGETS += sorted(ROOT.glob("lab0[0-7]_*/README.md"))
TARGETS += sorted(ROOT.glob("lab0[0-7]_*/OPTIONAL_BACKGROUND.md"))
TARGETS += sorted((ROOT / "activities" / "manipulator-dynamics").glob("*.md"))
TARGETS += sorted((ROOT / "docs").glob("*.md"))
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
BAD_ENCODINGS = ("â", "Â", "\ufffd")


def check_file(path):
    errors = []
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        return [f"invalid UTF-8: {exc}"]
    for token in BAD_ENCODINGS:
        if token in text:
            errors.append(f"contains suspicious encoding token {token!r}")
    if len(re.findall(r"(?m)^\$\$$", text)) % 2:
        errors.append("has an unmatched display-math delimiter")
    if re.search(r"\$\$\S|\S\$\$", text):
        errors.append("has display math sharing a line with content")
    if len(re.findall(r"(?m)^```", text)) % 2:
        errors.append("has an unmatched fenced-code delimiter")
    lines = text.splitlines()
    for index, line in enumerate(lines[1:], start=2):
        if re.match(r"^#{1,6} ", line) and lines[index - 2].strip():
            errors.append(f"line {index}: heading lacks a preceding blank line")
    for match in LINK_RE.finditer(text):
        target = match.group(1).strip("<>").split("#", 1)[0]
        if not target or re.match(r"^(?:https?://|mailto:|data:)", target):
            continue
        if not (path.parent / target).resolve().exists():
            errors.append(f"broken local link: {target}")
    return errors


def main():
    failed = False
    unique = list(dict.fromkeys(TARGETS))
    for path in unique:
        if not path.exists():
            continue
        problems = check_file(path)
        if problems:
            failed = True
            print(path.relative_to(ROOT))
            for problem in problems:
                print(f"  - {problem}")
    if failed:
        return 1
    print(f"Checked {len(unique)} Markdown files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
