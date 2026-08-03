#!/usr/bin/env python3
"""Enforce lightweight generated-page performance invariants."""

from __future__ import annotations

import sys
from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
SITE_DIR = ROOT / "_site"


def load_page(relative: str) -> BeautifulSoup:
    return BeautifulSoup((SITE_DIR / relative / "index.html").read_text(encoding="utf-8"), "html.parser")


def main() -> int:
    errors: list[str] = []

    for relative in ("", "contact", "links", "members"):
        soup = load_page(relative)
        if soup.select_one("#MathJax-script"):
            errors.append(f"/{relative}: MathJax should not load on this page")
        if soup.select('script[src*="mdb.umd.min.js"]'):
            errors.append(f"/{relative}: unused MDB JavaScript is still loaded")

    for relative in ("publications", "research", "teaching"):
        if not load_page(relative).select_one("#MathJax-script"):
            errors.append(f"/{relative}: MathJax is required but missing")

    homepage = load_page("")
    hero = homepage.select_one(".hero-header picture .hero-image")
    webp = homepage.select_one('.hero-header source[type="image/webp"]')
    if hero is None or hero.get("fetchpriority") != "high":
        errors.append("/: hero image must be high-priority and use a picture element")
    if webp is None or len(str(webp.get("srcset", "")).split(",")) != 3:
        errors.append("/: hero image must provide three responsive WebP candidates")

    footer_logo = homepage.select_one(".footer-logo-img")
    if footer_logo is None or footer_logo.get("loading") != "lazy":
        errors.append("/: footer logo must be lazy-loaded")

    size_limits = {
        "assets/img/heidelberg-480.webp": 50_000,
        "assets/img/heidelberg-960.webp": 160_000,
        "assets/img/heidelberg-1440.webp": 360_000,
    }
    for relative, limit in size_limits.items():
        path = SITE_DIR / relative
        if not path.is_file():
            errors.append(f"_site/{relative}: responsive image is missing")
        elif path.stat().st_size > limit:
            errors.append(f"_site/{relative}: exceeds the {limit}-byte budget")

    for error in errors:
        print(f"[ERROR] {error}")
    if errors:
        print(f"\nPerformance validation failed with {len(errors)} error(s).")
        return 1
    print("Performance validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
