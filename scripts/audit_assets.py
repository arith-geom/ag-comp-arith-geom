#!/usr/bin/env python3
"""Inventory site assets without deleting or rewriting contributor content."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ASSETS_DIR = ROOT / "assets"
SOURCE_GLOBS = (
    "_config.yml",
    "index.md",
    "_data/**/*",
    "_includes/**/*",
    "_layouts/**/*",
    "_pages/**/*",
    "_plugins/**/*",
    "_research/**/*",
    "_sass/**/*",
    "_teaching/**/*",
    "assets/css/**/*",
    "assets/js/**/*",
)


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def type_matches(path: Path) -> bool | None:
    suffix = path.suffix.casefold()
    try:
        head = path.read_bytes()[:512]
    except OSError:
        return False
    if suffix == ".pdf":
        return head.startswith(b"%PDF-")
    if suffix == ".png":
        return head.startswith(b"\x89PNG\r\n\x1a\n")
    if suffix in {".jpg", ".jpeg"}:
        return head.startswith(b"\xff\xd8\xff")
    if suffix == ".gif":
        return head.startswith((b"GIF87a", b"GIF89a"))
    if suffix == ".webp":
        return head.startswith(b"RIFF") and head[8:12] == b"WEBP"
    if suffix == ".ico":
        return head.startswith(b"\x00\x00\x01\x00")
    if suffix == ".svg":
        return b"<svg" in head.lower()
    return None


def source_text() -> str:
    paths: set[Path] = set()
    for pattern in SOURCE_GLOBS:
        paths.update(path for path in ROOT.glob(pattern) if path.is_file())
    chunks: list[str] = []
    for path in sorted(paths):
        try:
            chunks.append(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError):
            continue
    return "\n".join(chunks)


def inventory() -> dict[str, Any]:
    paths = sorted(path for path in ASSETS_DIR.rglob("*") if path.is_file())
    root_favicon = ROOT / "favicon.ico"
    if root_favicon.is_file():
        paths.append(root_favicon)

    corpus = source_text()
    records: list[dict[str, Any]] = []
    hashes: dict[str, list[dict[str, Any]]] = defaultdict(list)
    mismatches: list[str] = []

    for path in paths:
        relative = path.relative_to(ROOT).as_posix()
        size = path.stat().st_size
        match = type_matches(path)
        record = {
            "path": relative,
            "size": size,
            "referenced": relative in corpus or f"/{relative}" in corpus,
            "type_matches_extension": match,
        }
        records.append(record)
        hashes[digest(path)].append(record)
        if match is False:
            mismatches.append(relative)

    duplicate_groups = [
        group for group in hashes.values() if len(group) > 1
    ]
    duplicate_bytes = sum(
        sum(item["size"] for item in group[1:]) for group in duplicate_groups
    )
    return {
        "summary": {
            "files": len(records),
            "bytes": sum(item["size"] for item in records),
            "referenced_files": sum(bool(item["referenced"]) for item in records),
            "unreferenced_files": sum(not item["referenced"] for item in records),
            "duplicate_groups": len(duplicate_groups),
            "duplicate_copies": sum(len(group) - 1 for group in duplicate_groups),
            "duplicate_bytes": duplicate_bytes,
            "type_mismatches": len(mismatches),
            "files_over_10_mb": sum(item["size"] > 10 * 1024 * 1024 for item in records),
        },
        "type_mismatches": mismatches,
        "largest_files": sorted(records, key=lambda item: item["size"], reverse=True)[:25],
        "duplicate_groups": duplicate_groups,
        "unreferenced_files": [item for item in records if not item["referenced"]],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", type=Path, help="write the complete inventory as JSON")
    parser.add_argument("--strict", action="store_true", help="fail on file-type mismatches")
    args = parser.parse_args()

    report = inventory()
    summary = report["summary"]
    print(
        "Asset inventory: "
        f"{summary['files']} files, {summary['bytes'] / 1048576:.1f} MiB; "
        f"{summary['duplicate_copies']} duplicate copies "
        f"({summary['duplicate_bytes'] / 1048576:.1f} MiB); "
        f"{summary['unreferenced_files']} files without a direct source reference."
    )
    for path in report["type_mismatches"]:
        print(f"[WARNING] {path}: content does not match its extension")

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote detailed inventory to {args.json}")

    if args.strict and report["type_mismatches"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
