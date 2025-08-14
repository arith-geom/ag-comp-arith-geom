#!/usr/bin/env python3
"""
Scrape legacy teaching listings and basic subpages from
https://typo.iwr.uni-heidelberg.de/groups/arith-geom/teaching.html
and import/update _teaching/*.md entries for our site.

- Extract semester blocks and course titles with instructors
- Infer course_type from keywords (Vorlesung, Seminar, Proseminar, Hauptseminar)
- Attach external_url back to the legacy website where a link is found
"""

import re
import sys
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
TEACHING_DIR = ROOT / "_teaching"
SOURCE_URL = "https://typo.iwr.uni-heidelberg.de/groups/arith-geom/teaching.html"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125 Safari/537.36",
}


def normalize_semester(raw: str) -> tuple[str | None, int | None, str | None]:
    m = re.search(r"(SS|WS)\s*(\d{4})", raw)
    if not m:
        return None, None, None
    term, year = m.group(1), int(m.group(2))
    key = f"{term}{year}"
    sort = (year * 10) + (2 if term == "WS" else 1)
    return term, year, key, sort


def guess_course_type(title: str) -> str:
    t = title.lower()
    if "vorlesung" in t:
        return "Vorlesung"
    if "proseminar" in t:
        return "Proseminar"
    if "hauptseminar" in t:
        return "Hauptseminar"
    if "seminar" in t:
        return "Seminar"
    return "Seminar"


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def write_course_md(course: dict):
    title_slug = slugify(course["title"]) or "course"
    semester = course.get("semester_key") or "SS2000"
    filename = f"{semester}-{title_slug}.md"
    path = TEACHING_DIR / filename

    fm = []
    fm.append("---")
    fm.append("layout: teaching")
    fm.append(f"title: {course['title']}")
    if course.get("semester_key"):
        fm.append(f"semester: {course['semester_key']}")
    if course.get("instructor"):
        fm.append(f"instructor: {course['instructor']}")
    if course.get("course_type"):
        fm.append(f"course_type: {course['course_type']}")
    if course.get("language"):
        fm.append(f"language: {course['language']}")
    if course.get("links"):
        fm.append("links:")
        for link in course["links"]:
            label = link.get("label") or link.get("url")
            url = link.get("url")
            if not url:
                continue
            fm.append(f"  - label: \"{label}\"")
            fm.append(f"    url: \"{url}\"")
    if course.get("pdfs"):
        fm.append("pdfs:")
        for pdf in course["pdfs"]:
            label = pdf.get("label") or "PDF"
            file_url = pdf.get("file")
            if not file_url:
                continue
            fm.append(f"  - label: \"{label}\"")
            fm.append(f"    file: \"{file_url}\"")
    if course.get("semester_term"):
        fm.append(f"semester_term: {course['semester_term']}")
    if course.get("semester_year"):
        fm.append(f"semester_year: {course['semester_year']}")
    if course.get("semester_key"):
        fm.append(f"semester_key: {course['semester_key']}")
    if course.get("semester_sort"):
        fm.append(f"semester_sort: {course['semester_sort']}")
    fm.append("active: false")
    fm.append("---")
    # Store main content into front matter 'content' for CMS visibility
    if course.get("content_md"):
        content_text = course["content_md"].strip()
        # Escape YAML triple-dash if present
        # Use block scalar style would be nicer, but PagesCMS expects markdown field; we store plain string
        fm.append(f"content: |\n  {content_text.replace('\n', '\n  ')}")
        body = "Imported from legacy teaching listing."
    else:
        body = course.get("description") or "Imported from legacy teaching listing."

    path.write_text("\n".join(fm) + "\n\n" + body + "\n", encoding="utf-8")
    return path


def fetch_absolute(href: str, base: str) -> str | None:
    if not href:
        return None
    href = href.strip()
    if href.startswith("mailto:"):
        return None
    if href.startswith("http://") or href.startswith("https://"):
        return href
    # Relative path
    try:
        return urljoin(base, href)
    except Exception:
        return None


def extract_main_content(soup: BeautifulSoup, base_url: str) -> tuple[str | None, list[dict]]:
    # Try to find a main content container
    candidates = []
    for sel in ["main", "#content", "#main", ".content", "article", "#cBody", "#cContent", ".tx-indexedsearch"]:
        node = soup.select_one(sel)
        if node and len(node.get_text(strip=True)) > 100:
            candidates.append(node)
    if not candidates:
        # fallback: choose the div with most text
        divs = soup.find_all(["div", "section", "article"]) or []
        divs = sorted(divs, key=lambda d: len(d.get_text(strip=True)), reverse=True)
        if divs:
            candidates.append(divs[0])

    text = None
    links: list[dict] = []
    if candidates:
        container = candidates[0]
        # Collect important links only (PDFs and likely course materials)
        seen = set()
        def keep_link(url: str, label: str) -> bool:
            u = url.lower()
            if u.endswith('.pdf'):
                return True
            keywords = ['program', 'syllabus', 'slides', 'script', 'notes', 'material', 'handout', 'moodle', 'announcement', 'description']
            if any(k in label.lower() for k in keywords):
                return True
            hosts_allow = ['iwr.uni-heidelberg.de', 'mathi.uni-heidelberg.de', 'ub.uni-heidelberg.de']
            try:
                host = urlparse(url).netloc
            except Exception:
                host = ''
            if any(h in host for h in hosts_allow):
                return True
            return False

        for a in container.find_all("a", href=True):
            absu = fetch_absolute(a.get("href"), base_url)
            if not absu:
                continue
            label = a.get_text(strip=True) or absu
            if not keep_link(absu, label):
                continue
            if absu in seen:
                continue
            seen.add(absu)
            links.append({"label": label, "url": absu})
        # Extract a readable text (limit length)
        parts = []
        for el in container.find_all(["h1", "h2", "h3", "p", "li"], recursive=True):
            t = el.get_text(" ", strip=True)
            if t:
                parts.append(t)
            if sum(len(x) for x in parts) > 3000:
                break
        text = "\n\n".join(parts)
    return text, links


def fetch_course_page(url: str) -> tuple[str | None, list[dict]]:
    try:
        resp = requests.get(url, timeout=25, headers=HEADERS, allow_redirects=True)
        if resp.status_code != 200 or not resp.text:
            return None, []
        soup = BeautifulSoup(resp.text, "lxml")
        text, links = extract_main_content(soup, url)
        return text, links
    except Exception:
        return None, []


def scrape():
    print(f"Fetching {SOURCE_URL}")
    resp = requests.get(SOURCE_URL, timeout=30, headers=HEADERS)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "lxml")

    # Heuristic: semester headings look like 'Summer term 2025', 'Winter term 2024/25'
    results = []
    for heading in soup.find_all(["h3", "h4", "h5", "strong"]):
        text = heading.get_text(strip=True)
        if not text:
            continue
        # Map English semester labels to WS/SS
        if text.lower().startswith("summer term"):
            year = re.findall(r"(\d{4})", text)
            if year:
                term = "SS"
                yr = int(year[0])
                key = f"{term}{yr}"
            else:
                continue
        elif text.lower().startswith("winter term"):
            years = re.findall(r"(\d{4})", text)
            if years:
                # take the first year for key
                term = "WS"
                yr = int(years[0])
                key = f"{term}{yr}"
            else:
                continue
        else:
            continue

        # Next sibling list items
        ul = heading.find_next_sibling(["ul", "ol"])
        if not ul:
            continue
        for li in ul.find_all("li", recursive=False):
            entry_text = li.get_text(" ", strip=True)
            if not entry_text:
                continue
            # capture anchor as external_url if present
            a = li.find("a", href=True)
            external_url = None
            if a and a.get("href"):
                external_url = fetch_absolute(a.get("href"), SOURCE_URL)

            # Extract title in quotes if present
            m = re.search(r'"([^"]+)"', entry_text)
            title = m.group(1) if m else entry_text
            # Extract instructors in parentheses if present
            instr = None
            m2 = re.search(r"\(([^\)]+)\)$", entry_text)
            if m2:
                instr = m2.group(1)

            course = {
                "title": title.strip(),
                "instructor": instr.strip() if instr else None,
                "course_type": guess_course_type(entry_text),
                "semester_term": term,
                "semester_year": yr,
                "semester_key": key,
                "semester_sort": (yr * 10) + (2 if term == "WS" else 1),
                "external_url": external_url,
                "description": None,
            }
            # Attempt to fetch content from external_url
            if external_url:
                content_text, ext_links = fetch_course_page(external_url)
                if content_text:
                    # Short description and full content markdown
                    course["description"] = content_text.split("\n\n")[0][:600]
                    course["content_md"] = content_text
                if ext_links:
                    # Separate PDFs from other links, limit total
                    pdfs = []
                    links = []
                    for l in ext_links:
                        u = l.get('url','').lower()
                        if u.endswith('.pdf'):
                            pdfs.append({"label": l.get('label') or 'PDF', "file": l.get('url')})
                        else:
                            links.append({"label": l.get('label') or l.get('url'), "url": l.get('url')})
                    course["pdfs"] = pdfs[:8]
                    course["links"] = links[:8]
            results.append(course)

    print(f"Found {len(results)} courses")
    TEACHING_DIR.mkdir(parents=True, exist_ok=True)
    written = 0
    for course in results:
        path = write_course_md(course)
        print(f"Wrote/updated: {path.relative_to(ROOT)}")
        written += 1
        time.sleep(0.05)
    print(f"Done. {written} teaching files written.")


if __name__ == "__main__":
    try:
        scrape()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

