#!/usr/bin/env python3
"""
Check internal links and asset references for correctness with GitHub Pages baseurl.
Scans Markdown and Liquid files for href/src values that start with '/' and ensures
they would resolve correctly when prefixed with the configured baseurl.
"""

import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE_DIRS = [
    ROOT / "_pages",
    ROOT / "_members",
    ROOT / "_publications",
    ROOT / "_research",
    ROOT / "_teaching",
]

LINK_REGEX = re.compile(r"(href|src)\s*=\s*\"(/[^\"#\s]+)\"", re.IGNORECASE)

def check_file(path: Path):
    issues = []
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        return [(str(path), f"read_error: {e}")]

    for m in LINK_REGEX.finditer(text):
        attr, val = m.groups()
        # Skip absolute URLs handled elsewhere
        if val.startswith("//"):
            continue
        # Allow explicitly handled with Liquid filters
        before = text[: m.start()]
        # Heuristic: if within a Liquid filter pipe, likely using relative_url already
        if "| relative_url" in text[m.start(): m.start()+120]:
            continue
        issues.append((str(path), f"{attr} uses root-relative '{val}'. Prefer '{{{{ '{val}' | relative_url }}}}'"))
    return issues

def main():
    all_issues = []
    for base in SITE_DIRS:
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if path.suffix.lower() not in {".md", ".markdown", ".html", ".liquid"}:
                continue
            all_issues.extend(check_file(path))

    if not all_issues:
        print("✅ No obvious internal link issues found.")
        return 0

    print("⚠ Potential internal link issues:\n")
    for fp, msg in all_issues:
        print(f"- {fp}: {msg}")
    print("\nTip: Use Liquid 'relative_url' filter or the JS prefixBase helper for dynamic links.")
    return 1

if __name__ == "__main__":
    raise SystemExit(main())


