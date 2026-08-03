#!/usr/bin/env python3
"""Backward-compatible entry point for the repository validator."""

from __future__ import annotations

import runpy
from pathlib import Path


runpy.run_path(
    Path(__file__).resolve().parents[2] / "scripts" / "validate.py",
    run_name="__main__",
)
