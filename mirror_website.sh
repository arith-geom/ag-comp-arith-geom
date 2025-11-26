#!/bin/bash

# Default URL from user request
# We target the directory to ensure we get everything under it
DEFAULT_URL="https://typo.iwr.uni-heidelberg.de/groups/arith-geom/"
URL="${1:-$DEFAULT_URL}"

echo "Starting website mirror for: $URL"
echo "This process will download all subpages, PDFs, images, and assets."
echo "The content will be saved in a local directory."

# Check if wget is installed
if ! command -v wget &> /dev/null; then
    echo "Error: wget is not installed. Please install it first (e.g., 'brew install wget' or 'sudo apt install wget')."
    exit 1
fi

# wget options explanation:
# -m (--mirror): Turn on options suitable for mirroring (infinite recursion, timestamps, etc.)
# -k (--convert-links): After downloading, convert links to make them suitable for local viewing.
# -E (--adjust-extension): Save HTML/CSS documents with proper extensions (e.g. .php -> .html).
# -p (--page-requisites): Get all images, etc. needed to display HTML page.
# -np (--no-parent): Do not ascend to the parent directory.
# -e robots=off: Ignore robots.txt to ensure we get everything.
# -U: Set User-Agent to mimic a standard browser.
# --no-check-certificate: Bypass SSL validity checks (useful for some older/internal sites).
# --random-wait: Wait between 0.5 to 1.5 * --wait seconds (if wait is specified) to be polite.

wget \
  --mirror \
  --convert-links \
  --adjust-extension \
  --page-requisites \
  --no-parent \
  --execute robots=off \
  --user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36" \
  --no-check-certificate \
  "$URL"

echo "---------------------------------------------------"
echo "Mirroring complete!"
echo "You can now browse the downloaded content in the 'typo.iwr.uni-heidelberg.de' folder."
