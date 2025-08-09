#!/usr/bin/env python3
"""
Normalize YAML front matter in Markdown files under content collections.
- Fixes duplicate starting delimiter ("---\n---\n...") by collapsing into a single block
- Ensures a single front matter block at the top followed by body
- Preserves YAML content; aborts file if YAML parse fails

Collections processed: _members, _publications, _research, _teaching, _links, _pages
"""

from __future__ import annotations
import os
import sys
from pathlib import Path
import re
import yaml

CONTENT_DIRS = [
    "_members",
    "_publications",
    "_research",
    "_teaching",
    "_links",
    "_pages",
]

THREE_DASH = re.compile(r"^\s*---\s*$")


def normalize_file(path: Path) -> bool:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"SKIP {path}: read error: {e}")
        return False

    lines = text.splitlines(keepends=True)
    if not lines:
        return False

    changed = False

    # Only process if it starts with a YAML delimiter
    if not THREE_DASH.match(lines[0]):
        return False

    # Find delimiter indices among the first part of the file
    delim_indices = [i for i, line in enumerate(lines) if THREE_DASH.match(line)]

    # If there are fewer than 2 delimiters, nothing to do
    if len(delim_indices) < 2:
        return False

    # Handle duplicate starting delimiter: --- on line 0 and line 1
    if delim_indices[0] == 0 and delim_indices[1] == 1:
        # Try to treat the third delimiter as the closing of the true front matter
        if len(delim_indices) >= 3:
            start = 1  # after the spurious second '---'
            end = delim_indices[2]
            fm_lines = lines[start + 1 : end]  # lines between 2nd and 3rd '---'
            body_lines = lines[end + 1 :]
        else:
            # Fallback: treat empty front matter
            fm_lines = []
            body_lines = lines[2:]
        changed = True
    else:
        # Normal case: first block between first two delimiters
        start = delim_indices[0]
        end = delim_indices[1]
        fm_lines = lines[start + 1 : end]
        body_lines = lines[end + 1 :]

    fm_text = "".join(fm_lines)

    # Validate YAML
    try:
        fm = yaml.safe_load(fm_text) or {}
        if not isinstance(fm, dict):
            # Non-dict front matter is unexpected for Jekyll; skip
            print(f"WARN {path}: front matter not a mapping; skipping")
            return False
    except Exception as e:
        print(f"WARN {path}: YAML parse failed; skipping: {e}")
        return False

    # Re-emit normalized file
    new_text = "---\n" + yaml.safe_dump(
        fm, allow_unicode=True, sort_keys=False
    ) + "---\n" + "".join(body_lines)

    if new_text != text:
        try:
            path.write_text(new_text, encoding="utf-8")
            print(f"FIX  {path}")
            return True
        except Exception as e:
            print(f"ERROR {path}: write failed: {e}")
            return False
    return changed


def main() -> int:
    project_root = Path(__file__).resolve().parents[1]
    os.chdir(project_root)

    total = 0
    fixed = 0

    for rel_dir in CONTENT_DIRS:
        dir_path = Path(rel_dir)
        if not dir_path.exists():
            continue
        for md_path in dir_path.glob("*.md"):
            total += 1
            if normalize_file(md_path):
                fixed += 1

    print(f"\nNormalized {fixed}/{total} markdown files where needed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
