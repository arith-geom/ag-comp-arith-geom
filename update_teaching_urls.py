#!/usr/bin/env python3
"""
Script to remove old URLs from teaching files and clean up the content.
"""

import os
import re
from pathlib import Path

def update_teaching_file(file_path):
    """Update a single teaching file to remove old URLs."""
    print(f"Processing: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Remove links section if it only contains old URLs
    content = re.sub(
        r'links:\s*\n\s*- label: "[^"]*"\s*\n\s*url: "https://typo\.iwr\.uni-heidelberg\.de[^"]*"\s*\n',
        '',
        content,
        flags=re.MULTILINE
    )

    # Remove PDFs section with old URLs
    content = re.sub(
        r'pdfs:\s*\n\s*- label: "[^"]*"\s*\n\s*url: "https://typo\.iwr\.uni-heidelberg\.de[^"]*"\s*\n\s*file: "[^"]*"\s*\n',
        '',
        content,
        flags=re.MULTILINE
    )

    # Remove content source comments
    content = re.sub(
        r'--- Content from https://typo\.iwr\.uni-heidelberg\.de[^\n]* ---\n',
        '',
        content,
        flags=re.MULTILINE
    )

    # Clean up multiple blank lines
    content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)

    # Remove trailing blank lines at end of frontmatter
    content = re.sub(r'(---\s*\n\n)\s+', r'\1', content)

    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Updated: {file_path}")
        return True
    else:
        print(f"  No changes needed: {file_path}")
        return False

def main():
    """Process all teaching files."""
    teaching_dir = Path('/home/victor/Downloads/HiwiAgWebsite/ag-comp-arith-geom/_teaching')

    if not teaching_dir.exists():
        print(f"Directory not found: {teaching_dir}")
        return

    updated_count = 0
    for md_file in teaching_dir.glob('*.md'):
        if md_file.name in ['index.md', 'past-teaching.md', 'heidelberg-teaching-archive.md']:
            continue  # Skip index files

        if update_teaching_file(md_file):
            updated_count += 1

    print(f"\nUpdated {updated_count} teaching files")

if __name__ == '__main__':
    main()
