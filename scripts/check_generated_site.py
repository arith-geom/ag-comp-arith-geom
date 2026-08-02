#!/usr/bin/env python3
"""Catch generated-markup problems that generic link checks intentionally allow."""

from __future__ import annotations

import sys
from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
SITE_DIR = ROOT / "_site"


def main() -> int:
    if not SITE_DIR.is_dir():
        print("[ERROR] _site does not exist; build the site first.")
        return 1

    errors: list[str] = []
    for path in sorted(SITE_DIR.rglob("*.html")):
        relative = path.relative_to(ROOT)
        soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")

        for tag, attribute in (("a", "href"), ("img", "src"), ("script", "src")):
            for element in soup.find_all(tag):
                if element.has_attr(attribute) and not str(element[attribute]).strip():
                    errors.append(f"{relative}: empty {tag}[{attribute}]")

    for error in errors:
        print(f"[ERROR] {error}")
    if errors:
        print(f"\nGenerated-site validation failed with {len(errors)} error(s).")
        return 1

    print("Generated-site validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
