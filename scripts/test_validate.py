#!/usr/bin/env python3
"""Unit tests for repository validation helpers."""

from __future__ import annotations

import unittest
from pathlib import PurePosixPath

from validate import (
    has_safe_path_components,
    is_sensitive_query_parameter,
    resolve_repo_file,
)


class ValidationHelpersTest(unittest.TestCase):
    def test_upload_paths_require_safe_components(self) -> None:
        self.assertTrue(has_safe_path_components(PurePosixPath("course/notes-01.pdf")))
        self.assertFalse(has_safe_path_components(PurePosixPath("bad dir/notes.pdf")))
        self.assertFalse(has_safe_path_components(PurePosixPath("course/notes (final).pdf")))

    def test_repo_paths_reject_absolute_and_traversing_values(self) -> None:
        self.assertIsNotNone(resolve_repo_file(".pages.yml"))
        self.assertIsNone(resolve_repo_file("/etc/passwd"))
        self.assertIsNone(resolve_repo_file("../outside.yml"))
        self.assertIsNone(resolve_repo_file("_data\\contact.yml"))

    def test_secret_parameter_variants_are_detected(self) -> None:
        for name in (
            "key",
            "api_key",
            "apikey",
            "maps-key",
            "access_token",
            "client_secret",
            "private.token",
        ):
            with self.subTest(name=name):
                self.assertTrue(is_sensitive_query_parameter(name))

        for name in ("query", "language", "marker", "tokenize"):
            with self.subTest(name=name):
                self.assertFalse(is_sensitive_query_parameter(name))


if __name__ == "__main__":
    unittest.main()
