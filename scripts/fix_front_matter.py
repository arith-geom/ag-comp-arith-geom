#!/usr/bin/env python3
"""
Fix malformed YAML front matter in Markdown files where the first two lines are '---'.
This repairs files like _teaching/*.md and ensures Jekyll recognizes front matter and permalinks.
"""

import sys
from pathlib import Path


def fix_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    if len(lines) < 2:
        return False
    # Only fix if first two lines are both '---' (ignoring surrounding whitespace)
    if lines[0].strip() == "---" and lines[1].strip() == "---":
        # Remove the duplicate second delimiter
        fixed_lines = [lines[0]] + lines[2:]
        path.write_text("".join(fixed_lines), encoding="utf-8")
        return True
    return False


def main():
    base = Path(__file__).resolve().parents[1]
    targets = [base / "_teaching"]
    changed = 0
    for target in targets:
        for md in target.glob("*.md"):
            try:
                if fix_file(md):
                    print(f"Fixed: {md.relative_to(base)}")
                    changed += 1
            except Exception as e:
                print(f"Error fixing {md}: {e}")
    print(f"Total fixed files: {changed}")


if __name__ == "__main__":
    main()


