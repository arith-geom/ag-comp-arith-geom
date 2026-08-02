#!/usr/bin/env python3
"""Validate CMS-managed data without rewriting it."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import yaml


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "_data"
UPLOADS_DIR = ROOT / "assets" / "uploads"
SAFE_FILENAME = re.compile(r"^[A-Za-z0-9._-]+$")


class Validator:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warning(self, message: str) -> None:
        self.warnings.append(message)

    def load_yaml(self, filename: str) -> Any:
        path = DATA_DIR / filename
        try:
            with path.open(encoding="utf-8") as stream:
                return yaml.safe_load(stream)
        except FileNotFoundError:
            self.error(f"{path.relative_to(ROOT)}: file not found")
        except (OSError, UnicodeError, yaml.YAMLError) as error:
            self.error(f"{path.relative_to(ROOT)}: cannot be read: {error}")
        return None

    def require_mapping(self, value: Any, location: str) -> dict[str, Any] | None:
        if not isinstance(value, dict):
            self.error(f"{location}: expected an object")
            return None
        return value

    def require_list(self, value: Any, location: str) -> list[Any] | None:
        if not isinstance(value, list):
            self.error(f"{location}: expected a list")
            return None
        return value

    def require_text(self, value: Any, location: str) -> None:
        if not isinstance(value, str) or not value.strip():
            self.error(f"{location}: expected non-empty text")

    def validate_uploads(self) -> None:
        if not UPLOADS_DIR.is_dir():
            self.warning("assets/uploads: directory not found")
            return

        for path in sorted(UPLOADS_DIR.rglob("*")):
            if not path.is_file():
                continue
            relative = path.relative_to(ROOT)
            if not SAFE_FILENAME.fullmatch(path.name):
                self.error(f"{relative}: filename contains unsafe characters")
            try:
                size_mb = path.stat().st_size / (1024 * 1024)
            except OSError as error:
                self.warning(f"{relative}: cannot read file size: {error}")
                continue
            if size_mb > 2:
                self.warning(f"{relative}: large file ({size_mb:.2f} MB)")

    def validate_members(self) -> None:
        data = self.require_mapping(self.load_yaml("members.yml"), "_data/members.yml")
        if data is None:
            return
        sections = self.require_list(data.get("sections"), "_data/members.yml.sections")
        if sections is None:
            return

        names: set[str] = set()
        for section_index, raw_section in enumerate(sections, start=1):
            location = f"_data/members.yml.sections[{section_index}]"
            section = self.require_mapping(raw_section, location)
            if section is None:
                continue
            members = self.require_list(section.get("members", []), f"{location}.members")
            if members is None:
                continue
            for member_index, raw_member in enumerate(members, start=1):
                member_location = f"{location}.members[{member_index}]"
                member = self.require_mapping(raw_member, member_location)
                if member is None:
                    continue
                name = member.get("name")
                self.require_text(name, f"{member_location}.name")
                if isinstance(name, str) and name.strip():
                    normalized = name.casefold().strip()
                    if normalized in names:
                        self.error(f"{member_location}.name: duplicate member name {name!r}")
                    names.add(normalized)

    def validate_publications(self) -> None:
        data = self.require_mapping(self.load_yaml("publications.yml"), "_data/publications.yml")
        if data is None:
            return
        publications = self.require_list(
            data.get("publications"), "_data/publications.yml.publications"
        )
        if publications is None:
            return

        titles: set[str] = set()
        for index, raw_publication in enumerate(publications, start=1):
            location = f"_data/publications.yml.publications[{index}]"
            publication = self.require_mapping(raw_publication, location)
            if publication is None:
                continue
            title = publication.get("title")
            self.require_text(title, f"{location}.title")
            if "year" not in publication:
                self.error(f"{location}.year: field is required")
            if isinstance(title, str) and title.strip():
                normalized = title.casefold().strip()
                if normalized in titles:
                    self.error(f"{location}.title: duplicate publication title {title!r}")
                titles.add(normalized)

    def validate_teaching(self) -> None:
        data = self.require_mapping(self.load_yaml("teaching.yml"), "_data/teaching.yml")
        if data is None:
            return
        years = self.require_list(data.get("courses"), "_data/teaching.yml.courses")
        if years is None:
            return

        for year_index, raw_year in enumerate(years, start=1):
            year_location = f"_data/teaching.yml.courses[{year_index}]"
            year = self.require_mapping(raw_year, year_location)
            if year is None:
                continue
            if "year" not in year:
                self.error(f"{year_location}.year: field is required")
            semesters = self.require_list(year.get("semesters", []), f"{year_location}.semesters")
            if semesters is None:
                continue
            for semester_index, raw_semester in enumerate(semesters, start=1):
                semester_location = f"{year_location}.semesters[{semester_index}]"
                semester = self.require_mapping(raw_semester, semester_location)
                if semester is None:
                    continue
                self.require_text(semester.get("semester"), f"{semester_location}.semester")
                courses = self.require_list(
                    semester.get("courses", []), f"{semester_location}.courses"
                )
                if courses is None:
                    continue
                titles: set[str] = set()
                for course_index, raw_course in enumerate(courses, start=1):
                    course_location = f"{semester_location}.courses[{course_index}]"
                    course = self.require_mapping(raw_course, course_location)
                    if course is None:
                        continue
                    title = course.get("title")
                    self.require_text(title, f"{course_location}.title")
                    if isinstance(title, str) and title.strip():
                        normalized = title.casefold().strip()
                        if normalized in titles:
                            self.error(
                                f"{course_location}.title: duplicate course title {title!r} "
                                "within the same semester"
                            )
                        titles.add(normalized)

    def validate_shortlinks(self) -> None:
        loaded = self.load_yaml("shortlinks.yml")
        if loaded is None:
            # Pages CMS represents an empty optional collection as an empty file.
            return
        data = self.require_mapping(loaded, "_data/shortlinks.yml")
        if data is None:
            return
        links = self.require_list(data.get("shortlinks"), "_data/shortlinks.yml.shortlinks")
        if links is None:
            return

        slugs: set[str] = set()
        for index, raw_link in enumerate(links, start=1):
            location = f"_data/shortlinks.yml.shortlinks[{index}]"
            link = self.require_mapping(raw_link, location)
            if link is None:
                continue
            slug = link.get("slug")
            self.require_text(slug, f"{location}.slug")
            target = link.get("target")
            self.require_text(target, f"{location}.target")
            if isinstance(slug, str) and slug.strip():
                normalized = slug.strip("/").casefold()
                if not normalized or "/" in normalized or not SAFE_FILENAME.fullmatch(normalized):
                    self.error(f"{location}.slug: expected one URL-safe path segment")
                if normalized in slugs:
                    self.error(f"{location}.slug: duplicate shortlink slug {slug!r}")
                slugs.add(normalized)
            if isinstance(target, str) and target.strip():
                value = target.strip()
                parsed = urlparse(value)
                is_internal = value.startswith("/") and not value.startswith("//")
                is_web_url = parsed.scheme in {"http", "https"} and bool(parsed.netloc)
                if not is_internal and not is_web_url:
                    self.error(
                        f"{location}.target: expected a root-relative path or HTTP(S) URL"
                    )

    def run(self) -> int:
        self.validate_uploads()
        self.validate_members()
        self.validate_publications()
        self.validate_teaching()
        self.validate_shortlinks()

        for message in self.warnings:
            print(f"[WARNING] {message}")
        for message in self.errors:
            print(f"[ERROR] {message}")

        if self.errors:
            print(f"\nValidation failed with {len(self.errors)} error(s).")
            return 1
        print(f"Validation passed with {len(self.warnings)} warning(s).")
        return 0


if __name__ == "__main__":
    sys.exit(Validator().run())
