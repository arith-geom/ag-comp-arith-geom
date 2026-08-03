#!/usr/bin/env python3
"""Enforce conservative Lighthouse budgets for representative pages."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


CATEGORY_MINIMUMS = {
    "performance": 0.75,
    "accessibility": 0.90,
    "best-practices": 0.90,
    "seo": 0.90,
}
AUDIT_MAXIMUMS = {
    "largest-contentful-paint": 4000,
    "cumulative-layout-shift": 0.10,
    "total-blocking-time": 300,
}


def load_report(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError(f"{path}: cannot read Lighthouse report: {error}") from error


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("reports", nargs="+", type=Path)
    args = parser.parse_args()
    errors: list[str] = []

    for path in args.reports:
        try:
            report = load_report(path)
        except ValueError as error:
            errors.append(str(error))
            continue

        requested_url = report.get("requestedUrl", path.name)
        scores: list[str] = []
        for category, minimum in CATEGORY_MINIMUMS.items():
            score = report.get("categories", {}).get(category, {}).get("score")
            if not isinstance(score, (int, float)):
                errors.append(f"{requested_url}: missing {category} score")
                continue
            scores.append(f"{category}={score:.2f}")
            if score < minimum:
                errors.append(
                    f"{requested_url}: {category} score {score:.2f} is below {minimum:.2f}"
                )

        for audit, maximum in AUDIT_MAXIMUMS.items():
            value = report.get("audits", {}).get(audit, {}).get("numericValue")
            if not isinstance(value, (int, float)):
                errors.append(f"{requested_url}: missing {audit} measurement")
            elif value > maximum:
                errors.append(
                    f"{requested_url}: {audit} {value:.1f} exceeds budget {maximum:.1f}"
                )
        print(f"{requested_url}: {', '.join(scores)}")

    for error in errors:
        print(f"[ERROR] {error}")
    if errors:
        print(f"Lighthouse budgets failed with {len(errors)} error(s).")
        return 1
    print(f"Lighthouse budgets passed for {len(args.reports)} page(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
