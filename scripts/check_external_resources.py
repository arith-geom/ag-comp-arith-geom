#!/usr/bin/env python3
"""Check generated pages for basic third-party resource protections."""

from __future__ import annotations

import sys
from pathlib import Path
from urllib.parse import urlparse

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
INTEGRITY_EXEMPT_HOSTS = {"fonts.googleapis.com", "fonts.gstatic.com"}


def main() -> int:
    errors: set[str] = set()
    pages = sorted(SITE.rglob("*.html"))
    if not pages:
        print("[ERROR] _site has no HTML files; build the site first.")
        return 1

    for page in pages:
        soup = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
        if soup.head is None:
            continue
        if not soup.find("meta", attrs={"name": "referrer"}):
            errors.add(f"{page.relative_to(SITE)}: missing referrer policy")

        resources = list(soup.find_all("script", src=True))
        resources.extend(
            link
            for link in soup.find_all("link", href=True)
            if "stylesheet" in (link.get("rel") or [])
        )
        for element in resources:
            url = element.get("src") or element.get("href")
            parsed = urlparse(url)
            if parsed.scheme not in {"http", "https"}:
                continue
            if parsed.hostname in INTEGRITY_EXEMPT_HOSTS:
                continue
            if not element.get("integrity"):
                errors.add(f"external resource lacks integrity metadata: {url}")
            if element.get("crossorigin") != "anonymous":
                errors.add(f"external resource lacks crossorigin=anonymous: {url}")

    if errors:
        for error in sorted(errors):
            print(f"[ERROR] {error}")
        return 1

    print(f"External-resource validation passed across {len(pages)} pages.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
