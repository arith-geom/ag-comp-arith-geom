#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

echo "== Smoke tests =="

echo "1) Checking internal links for baseurl safety"
python3 scripts/check_internal_links.py || true

echo "2) Checking member external links"
python3 scripts/check_links.py || true

echo "3) Validating Pages CMS config/files"
python3 scripts/validate_pagescms.py || true

echo "4) Teaching front matter quick fix scan"
python3 scripts/fix_teaching_pages.py || true

echo "Done."

