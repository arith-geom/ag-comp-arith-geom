#!/usr/bin/env python3
"""Validate generated search and social metadata without modifying content."""

from __future__ import annotations

import json
import struct
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


def png_dimensions(path: Path) -> tuple[int, int] | None:
    try:
        data = path.read_bytes()
    except OSError:
        return None
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", data[16:24])


def validate_favicons(errors: list[str]) -> None:
    homepage = SITE_DIR / "index.html"
    try:
        soup = BeautifulSoup(homepage.read_text(encoding="utf-8"), "html.parser")
    except (OSError, UnicodeError) as error:
        errors.append(f"_site/index.html: cannot validate favicons: {error}")
        return

    icon_hrefs = {
        str(link.get("href", "")).strip()
        for link in soup.select('link[rel~="icon"]')
    }
    for suffix in (
        "/favicon.ico",
        "/assets/img/favicon.svg",
        "/assets/img/favicon-96x96.png",
    ):
        if not any(urlparse(href).path.endswith(suffix) for href in icon_hrefs):
            errors.append(f"_site/index.html: missing favicon link ending in {suffix}")

    touch_icon = soup.select_one('link[rel~="apple-touch-icon"]')
    if not nonempty_attribute(touch_icon, "href") or not urlparse(
        str(touch_icon.get("href", ""))
    ).path.endswith("/assets/img/apple-touch-icon.png"):
        errors.append("_site/index.html: missing Apple touch icon")

    ico_path = SITE_DIR / "favicon.ico"
    try:
        ico = ico_path.read_bytes()
    except OSError as error:
        errors.append(f"_site/favicon.ico: cannot be read: {error}")
    else:
        if len(ico) < 6:
            errors.append("_site/favicon.ico: invalid icon header")
        else:
            reserved, image_type, count = struct.unpack("<HHH", ico[:6])
            if (reserved, image_type) != (0, 1) or count < 1 or len(ico) < 6 + 16 * count:
                errors.append("_site/favicon.ico: expected a valid multi-size ICO file")
            else:
                dimensions = [
                    (
                        ico[6 + index * 16] or 256,
                        ico[7 + index * 16] or 256,
                    )
                    for index in range(count)
                ]
                if not any(width == height and width >= 48 for width, height in dimensions):
                    errors.append("_site/favicon.ico: requires a square 48px-or-larger icon")

    for relative, expected_size in (
        ("assets/img/favicon-96x96.png", 96),
        ("assets/img/apple-touch-icon.png", 180),
    ):
        dimensions = png_dimensions(SITE_DIR / relative)
        if dimensions != (expected_size, expected_size):
            errors.append(
                f"_site/{relative}: expected a {expected_size}x{expected_size} PNG"
            )

    svg_path = SITE_DIR / "assets" / "img" / "favicon.svg"
    try:
        svg = ET.parse(svg_path).getroot()
        view_box = [float(value) for value in svg.attrib.get("viewBox", "").split()]
    except (ET.ParseError, OSError, ValueError) as error:
        errors.append(f"_site/assets/img/favicon.svg: cannot parse SVG: {error}")
    else:
        if len(view_box) != 4 or view_box[2] != view_box[3] or view_box[2] < 48:
            errors.append(
                "_site/assets/img/favicon.svg: expected a square viewBox of at least 48px"
            )


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

    validate_favicons(errors)

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
