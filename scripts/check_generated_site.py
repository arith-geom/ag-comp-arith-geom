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

        if soup.html is None:
            continue

        is_redirect = soup.select_one('meta[http-equiv="refresh"]') is not None
        if not is_redirect and soup.select_one("main h1, [role='main'] h1") is None:
            errors.append(f"{relative}: main content is missing an h1")

        ids = [str(element["id"]) for element in soup.select("[id]")]
        duplicate_ids = sorted({value for value in ids if ids.count(value) > 1})
        for duplicate_id in duplicate_ids:
            errors.append(f"{relative}: duplicate id {duplicate_id!r}")

        for image in soup.find_all("img"):
            if not image.has_attr("alt"):
                errors.append(f"{relative}: image is missing alt text")

        for frame in soup.find_all("iframe"):
            if not str(frame.get("title", "")).strip():
                errors.append(f"{relative}: iframe is missing a title")

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
