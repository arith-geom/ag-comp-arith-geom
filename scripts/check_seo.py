#!/usr/bin/env python3
"""Validate generated search and social metadata without modifying content."""

from __future__ import annotations

import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
SITE_DIR = ROOT / "_site"
SITEMAP_NAMESPACE = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


def nonempty_attribute(element, attribute: str) -> bool:
    return element is not None and bool(str(element.get(attribute, "")).strip())


def main() -> int:
    errors: list[str] = []
    canonical_urls: dict[str, Path] = {}

    for path in sorted(SITE_DIR.rglob("*.html")):
        relative = path.relative_to(ROOT)
        soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
        if soup.html is None:
            continue

        robots = soup.select_one('meta[name="robots"]')
        if robots and "noindex" in robots.get("content", "").lower():
            continue

        title = soup.title.get_text(strip=True) if soup.title else ""
        if not title:
            errors.append(f"{relative}: missing document title")

        description = soup.select_one('meta[name="description"]')
        if not nonempty_attribute(description, "content"):
            errors.append(f"{relative}: missing meta description")

        canonical = soup.select_one('link[rel="canonical"]')
        if not nonempty_attribute(canonical, "href"):
            errors.append(f"{relative}: missing canonical URL")
        else:
            url = canonical["href"].strip()
            parsed = urlparse(url)
            if parsed.scheme != "https" or not parsed.netloc:
                errors.append(f"{relative}: canonical URL must be absolute HTTPS: {url}")
            if url in canonical_urls:
                errors.append(
                    f"{relative}: duplicate canonical URL also used by {canonical_urls[url]}: {url}"
                )
            canonical_urls[url] = relative

        for selector, attribute, label in (
            ('meta[property="og:title"]', "content", "Open Graph title"),
            ('meta[property="og:description"]', "content", "Open Graph description"),
            ('meta[property="og:url"]', "content", "Open Graph URL"),
            ('meta[property="og:image"]', "content", "Open Graph image"),
        ):
            if not nonempty_attribute(soup.select_one(selector), attribute):
                errors.append(f"{relative}: missing {label}")

        for script in soup.select('script[type="application/ld+json"]'):
            try:
                json.loads(script.get_text())
            except json.JSONDecodeError as error:
                errors.append(f"{relative}: invalid JSON-LD: {error}")

    sitemap_path = SITE_DIR / "sitemap.xml"
    try:
        sitemap = ET.parse(sitemap_path)
    except (ET.ParseError, OSError) as error:
        errors.append(f"_site/sitemap.xml: cannot parse sitemap: {error}")
        sitemap_urls: list[str] = []
    else:
        sitemap_urls = [
            node.text.strip()
            for node in sitemap.findall("sm:url/sm:loc", SITEMAP_NAMESPACE)
            if node.text and node.text.strip()
        ]
        if len(sitemap_urls) != len(set(sitemap_urls)):
            errors.append("_site/sitemap.xml: contains duplicate URLs")

    missing_from_sitemap = sorted(set(canonical_urls) - set(sitemap_urls))
    for url in missing_from_sitemap:
        errors.append(f"_site/sitemap.xml: missing canonical URL {url}")

    unexpected_sitemap_urls = sorted(set(sitemap_urls) - set(canonical_urls))
    for url in unexpected_sitemap_urls:
        errors.append(f"_site/sitemap.xml: non-canonical URL should be excluded: {url}")

    for error in errors:
        print(f"[ERROR] {error}")
    if errors:
        print(f"\nSEO validation failed with {len(errors)} error(s).")
        return 1

    print(
        f"SEO validation passed for {len(canonical_urls)} indexable pages and "
        f"{len(sitemap_urls)} sitemap URLs."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
