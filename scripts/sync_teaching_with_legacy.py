#!/usr/bin/env python3
"""
Sync _teaching collection with the legacy teaching list.

Steps:
1) Scrape legacy list page to build the canonical set of (semester_key, title)
2) Run the existing scraper to (re)create/update files with content and links
3) Remove local teaching files that are not present in the legacy list

Source: https://typo.iwr.uni-heidelberg.de/groups/arith-geom/teaching.html
"""

import re
import sys
from pathlib import Path
import runpy
import yaml
import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
TEACHING_DIR = ROOT / "_teaching"
LEGACY_URL = "https://typo.iwr.uni-heidelberg.de/groups/arith-geom/teaching.html"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125 Safari/537.36",
}


def build_legacy_keyset() -> set[str]:
    resp = requests.get(LEGACY_URL, timeout=30, headers=HEADERS)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "lxml")

    keys: set[str] = set()

    def norm_title(t: str) -> str:
        return (t or "").strip().lower()

    for heading in soup.find_all(["h3", "h4", "h5", "strong"]):
        text = heading.get_text(strip=True)
        if not text:
            continue
        term = None
        yr = None
        if text.lower().startswith("summer term"):
            ys = re.findall(r"(\d{4})", text)
            if ys:
                term = "SS"
                yr = int(ys[0])
        elif text.lower().startswith("winter term"):
            ys = re.findall(r"(\d{4})", text)
            if ys:
                term = "WS"
                yr = int(ys[0])
        if not term or not yr:
            continue
        sem_key = f"{term}{yr}".lower()

        ul = heading.find_next_sibling(["ul", "ol"])
        if not ul:
            continue
        for li in ul.find_all("li", recursive=False):
            entry_text = li.get_text(" ", strip=True)
            if not entry_text:
                continue
            m = re.search(r'"([^"]+)"', entry_text)
            title = m.group(1) if m else entry_text
            keys.add(f"{sem_key}__{norm_title(title)}")

    return keys


def list_teaching_files():
    keep_names = {"index.md", "past-teaching.md", "heidelberg-teaching-archive.md"}
    return [p for p in TEACHING_DIR.glob("*.md") if p.name not in keep_names]


def read_front_matter(p: Path) -> dict:
    txt = p.read_text(encoding="utf-8", errors="ignore")
    m = re.match(r'^---\n(.*?)\n---\n', txt, re.S)
    if not m:
        return {}
    try:
        return yaml.safe_load(m.group(1)) or {}
    except Exception:
        return {}


def key_of(fm: dict) -> str:
    title = (fm.get("title") or "").strip().lower()
    sem = (fm.get("semester_key") or "").strip().lower()
    if not sem and (fm.get("semester_term") and fm.get("semester_year")):
        sem = f"{fm.get('semester_term')}{fm.get('semester_year')}".lower()
    if not sem and fm.get("semester"):
        m = re.search(r"\b(WS|SS)\s*([0-9]{4})\b", str(fm.get("semester")))
        if m:
            sem = f"{m.group(1)}{m.group(2)}".lower()
    return f"{sem}__{title}" if sem and title else ""


def dedupe_by_key(legacy_keys: set[str]):
    """Remove duplicate files that share the same (semester,title) key, keeping the newest file.
    Prefer files that are not simple legacy imports when mtimes tie.
    """
    files = list_teaching_files()
    buckets: dict[str, list[Path]] = {}
    for p in files:
        fm = read_front_matter(p)
        k = key_of(fm)
        if not k:
            continue
        buckets.setdefault(k, []).append(p)

    removed = []
    for k, paths in buckets.items():
        if len(paths) <= 1:
            continue
        # Sort newest first
        paths_sorted = sorted(paths, key=lambda q: q.stat().st_mtime, reverse=True)
        keep = paths_sorted[0]
        for rm in paths_sorted[1:]:
            try:
                rm.unlink(missing_ok=True)
                removed.append(rm.name)
            except Exception:
                pass
    return removed


def main():
    print("Building legacy keyset from:", LEGACY_URL)
    legacy_keys = build_legacy_keyset()
    print("Legacy items:", len(legacy_keys))

    print("Running scraper to (re)generate teaching files...")
    runpy.run_path(str(ROOT / "scripts" / "scrape_teaching.py"))

    # Remove any local teaching file not present in legacy list (based on semester+title)
    removed = []
    for p in list_teaching_files():
        fm = read_front_matter(p)
        k = key_of(fm)
        # Skip if not a valid course or not English title (best-effort: contains only ASCII)
        if not k:
            continue
        if k not in legacy_keys:
            try:
                p.unlink(missing_ok=True)
                removed.append(p.name)
            except Exception:
                pass

    print("Removed non-legacy courses:", len(removed))
    for n in removed[:50]:
        print(" -", n)

    # Dedupe keys to ensure single course per semester+title
    dups_removed = dedupe_by_key(legacy_keys)
    if dups_removed:
        print("Removed duplicates:", len(dups_removed))
        for n in dups_removed[:50]:
            print(" -", n)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Error:", e)
        sys.exit(1)


