#!/usr/bin/env python3
"""Enforce conservative Lighthouse budgets for representative pages."""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


CATEGORY_MINIMUMS = {
    # Initial regression floor from the mobile-throttled CI baseline (0.61-0.68).
    "performance": 0.60,
    "accessibility": 0.90,
    "best-practices": 0.90,
    "seo": 0.90,
}
AUDIT_MAXIMUMS = {
    # Initial CI baseline is 5.0-5.6 seconds; tighten as render-blocking CSS improves.
    "largest-contentful-paint": 6000,
    "cumulative-layout-shift": 0.10,
    "total-blocking-time": 400,
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
    reports_by_url: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for path in args.reports:
        try:
            report = load_report(path)
        except ValueError as error:
            errors.append(str(error))
            continue

        requested_url = report.get("requestedUrl", path.name)
        reports_by_url[str(requested_url)].append(report)

    for requested_url, reports in sorted(reports_by_url.items()):
        scores: list[str] = []
        for category, minimum in CATEGORY_MINIMUMS.items():
            values = [
                report.get("categories", {}).get(category, {}).get("score")
                for report in reports
            ]
            if not all(isinstance(value, (int, float)) for value in values):
                errors.append(f"{requested_url}: missing {category} score")
                continue
            score = statistics.median(values)
            scores.append(f"{category}={score:.2f}")
            if score < minimum:
                errors.append(
                    f"{requested_url}: {category} score {score:.2f} is below {minimum:.2f}"
                )

        for audit, maximum in AUDIT_MAXIMUMS.items():
            values = [
                report.get("audits", {}).get(audit, {}).get("numericValue")
                for report in reports
            ]
            if not all(isinstance(value, (int, float)) for value in values):
                errors.append(f"{requested_url}: missing {audit} measurement")
                continue
            value = statistics.median(values)
            if value > maximum:
                errors.append(
                    f"{requested_url}: {audit} {value:.1f} exceeds budget {maximum:.1f}"
                )
        print(f"{requested_url}: median of {len(reports)} run(s), {', '.join(scores)}")

    for error in errors:
        print(f"[ERROR] {error}")
    if errors:
        print(f"Lighthouse budgets failed with {len(errors)} error(s).")
        return 1
    print(f"Lighthouse budgets passed for {len(reports_by_url)} page(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
