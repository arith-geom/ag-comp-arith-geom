#!/usr/bin/env python3
"""
Comprehensive Teaching Scraper for AG Computational Arithmetic Geometry

This scraper will:
1. Parse the HTML content from the Heidelberg University teaching pages
2. Extract all teaching entries with their metadata
3. Download all PDFs and resources
4. Create new teaching files with the same structure as current cards
5. Update the website with the new content
"""

import os
import re
import sys
import time
import html
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.error import URLError, HTTPError
import urllib.request
from html.parser import HTMLParser

# Configuration
BASE_URL = "https://typo.iwr.uni-heidelberg.de/groups/arith-geom/"
ROOT_DIR = Path(__file__).resolve().parents[1]
TEACHING_DIR = ROOT_DIR / "_teaching"
ASSETS_DIR = ROOT_DIR / "assets/uploads"
DOWNLOAD_DIR = ASSETS_DIR

# Create directories
TEACHING_DIR.mkdir(parents=True, exist_ok=True)
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

# No external headers needed for urllib

def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    if not text:
        return "teaching"
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"-+", "-", text)
    result = text.strip("-")
    # Limit length to avoid filesystem issues
    return result[:50] if len(result) > 50 else result

def download_file(url: str, filename: str) -> str:
    """Download a file and return the local path."""
    if not url or not url.startswith(('http://', 'https://')):
        return ""

    try:
        print(f"📥 Downloading: {url}")
        filepath = DOWNLOAD_DIR / filename
        urllib.request.urlretrieve(url, filepath)
        print(f"✅ Downloaded: {filename}")
        return f"/assets/uploads/{filename}"
    except Exception as e:
        print(f"❌ Error downloading {url}: {e}")
        return ""

def scrape_subdomain_content(url: str) -> str:
    """Scrape content from Heidelberg University subdomains for expansion."""
    if not url or not url.startswith(('http://', 'https://')):
        return ""

    # Only scrape from Heidelberg University domains
    parsed_url = urlparse(url)
    if not ('heidelberg.de' in parsed_url.netloc or 'uni-heidelberg.de' in parsed_url.netloc):
        return ""

    try:
        print(f"🌐 Scraping subdomain content from: {url}")
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (compatible; Teaching Scraper)'
        })

        with urllib.request.urlopen(req, timeout=10) as response:
            html_content = response.read().decode('utf-8', errors='ignore')

        # Extract main content - look for common content containers
        content_patterns = [
            r'<div[^>]*id="content"[^>]*>(.*?)</div>',
            r'<div[^>]*class="content"[^>]*>(.*?)</div>',
            r'<main[^>]*>(.*?)</main>',
            r'<article[^>]*>(.*?)</article>',
            r'<body[^>]*>(.*?)</body>'
        ]

        for pattern in content_patterns:
            match = re.search(pattern, html_content, re.DOTALL | re.IGNORECASE)
            if match:
                content = match.group(1)
                # Clean up the content
                content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
                content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL | re.IGNORECASE)
                content = re.sub(r'<[^>]+>', '', content)  # Remove remaining HTML tags
                content = re.sub(r'\s+', ' ', content).strip()  # Normalize whitespace

                if len(content) > 100:  # Only return if we got substantial content
                    print(f"✅ Scraped {len(content)} characters from subdomain")
                    return content[:2000]  # Limit content length

        # Fallback: try to extract text between title and common footer elements
        title_match = re.search(r'<title[^>]*>(.*?)</title>', html_content, re.IGNORECASE)
        title = title_match.group(1) if title_match else ""

        # Extract body text as fallback
        body_match = re.search(r'<body[^>]*>(.*?)</body>', html_content, re.DOTALL | re.IGNORECASE)
        if body_match:
            content = re.sub(r'<[^>]+>', '', body_match.group(1))
            content = re.sub(r'\s+', ' ', content).strip()
            if len(content) > 100:
                print(f"✅ Scraped {len(content)} characters from subdomain (fallback)")
                return f"{title}\n\n{content[:2000]}" if title else content[:2000]

    except Exception as e:
        print(f"❌ Error scraping subdomain content from {url}: {e}")

    return ""

def extract_course_type(title: str, context: str) -> str:
    """Extract course type from title or context."""
    # Common course type indicators
    type_indicators = {
        'seminar': ['seminar', 'hauptseminar', 'oberseminar', 'forschungsseminar'],
        'vorlesung': ['vorlesung', 'lecture', 'course', 'kurs'],
        'proseminar': ['proseminar'],
        'übung': ['übung', 'exercise', 'tutorial'],
        'arbeitsgemeinschaft': ['arbeitsgemeinschaft', 'study group'],
        'kolloquium': ['kolloquium', 'colloquium']
    }

    # Check title first
    title_lower = title.lower()
    for course_type, indicators in type_indicators.items():
        for indicator in indicators:
            if indicator in title_lower:
                return course_type.title()

    # Check context if available
    if context:
        context_lower = context.lower()
        for course_type, indicators in type_indicators.items():
            for indicator in indicators:
                if indicator in context_lower:
                    return course_type.title()

    # Default to Seminar if we can't determine
    return "Seminar"

def parse_semester_info(semester_text: str) -> dict:
    """Parse semester information from heading text."""
    semester_info = {
        'semester_key': '',
        'semester_term': '',
        'semester_year': 0,
        'semester_sort': 0,
        'full_semester': semester_text.strip()
    }

    # Extract year
    year_match = re.search(r'(\d{4})', semester_text)
    if year_match:
        year = int(year_match.group(1))
        semester_info['semester_year'] = year

        # Determine term
        if 'summer' in semester_text.lower() or 'ss' in semester_text.lower():
            semester_info['semester_term'] = 'SS'
            semester_info['semester_key'] = f'SS{year}'
            semester_info['semester_sort'] = year * 10 + 1  # Summer comes first in year
        elif 'winter' in semester_text.lower() or 'ws' in semester_text.lower():
            semester_info['semester_term'] = 'WS'
            semester_info['semester_key'] = f'WS{year}'
            semester_info['semester_sort'] = year * 10 + 2  # Winter comes second

    return semester_info

def extract_links_and_pdfs_html(html_content: str, base_url: str) -> tuple:
    """Extract all links and PDFs from HTML string."""
    links = []
    pdfs = []

    # Find all <a> tags with href attributes
    link_pattern = r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>([^<]*)</a>'
    matches = re.findall(link_pattern, html_content, re.IGNORECASE)

    for href, text in matches:
        if not href:
            continue

        # Clean up the text
        text = html.unescape(text.strip())
        if not text:
            text = href

        # Convert relative URLs to absolute
        if href.startswith('/'):
            href = urljoin(base_url, href)
        elif not href.startswith(('http://', 'https://')):
            href = urljoin(base_url, href)

        # Check if it's a PDF
        if href.lower().endswith('.pdf'):
            filename = os.path.basename(urlparse(href).path)
            if filename:
                local_path = download_file(href, filename)
                if local_path:
                    pdfs.append({
                        'label': text,
                        'file': local_path,
                        'url': href
                    })
        else:
            # Add as general link
            links.append({
                'label': text,
                'url': href
            })

    return links, pdfs

def parse_teaching_from_html(html_content: str, source_name: str) -> list:
    """Parse teaching entries from HTML content using regex."""
    teachings = []

    try:
        # Find the teaching content area - look for the frame div with teaching content
        content_patterns = [
            r'<div[^>]*id="c1360"[^>]*>(.*?)</div>',
            r'<div[^>]*id="c\d+"[^>]*class="frame[^>]*>(.*?)</div>',
            r'<div[^>]*class="frame[^>]*id="c\d+"[^>]*>(.*?)</div>',
            r'<div[^>]*id="content"[^>]*>(.*?)</div>'
        ]

        content_html = None
        for pattern in content_patterns:
            content_match = re.search(pattern, html_content, re.DOTALL | re.IGNORECASE)
            if content_match:
                content_html = content_match.group(1)
                print(f"✅ Found content area using pattern: {pattern}")
                break

        if not content_html:
            print(f"❌ Could not find content area in {source_name}")
            print(f"📄 HTML content length: {len(html_content)}")
            # Debug: print first 500 chars
            print(f"📄 HTML preview: {html_content[:500]}...")
            return teachings

        print(f"📄 Content HTML length: {len(content_html)}")
        print(f"📄 Content preview: {content_html[:500]}...")

        # Find all semester sections using regex - look for h4 tags followed by ul
        semester_pattern = r'<h4[^>]*>(.*?)</h4>\s*<ul[^>]*>(.*?)</ul>'
        semester_matches = re.findall(semester_pattern, content_html, re.DOTALL | re.IGNORECASE)
        print(f"📅 Found {len(semester_matches)} semester sections")

        for heading_text, list_content in semester_matches:
            heading_text = html.unescape(heading_text.strip())

            # Check if this is a semester heading
            if not ('summer term' in heading_text.lower() or 'winter term' in heading_text.lower()):
                continue

            print(f"📅 Processing semester: {heading_text}")

            # Parse semester information
            semester_info = parse_semester_info(heading_text)

            # Find individual list items
            li_pattern = r'<li[^>]*>(.*?)</li>'
            li_matches = re.findall(li_pattern, list_content, re.DOTALL | re.IGNORECASE)

            for li_content in li_matches:
                try:
                    course_data = parse_course_entry_html(li_content, semester_info, source_name)
                    if course_data:
                        teachings.append(course_data)
                        print(f"✅ Extracted course: {course_data['title'][:50]}...")

                except Exception as e:
                    print(f"⚠️ Error parsing course entry: {e}")
                    continue

    except Exception as e:
        print(f"❌ Error parsing HTML from {source_name}: {e}")

    return teachings

def parse_course_entry_html(li_html: str, semester_info: dict, source_name: str) -> dict:
    """Parse individual course entry from HTML string."""
    # Decode HTML entities
    course_text = html.unescape(li_html)

    # Remove HTML tags to get plain text
    plain_text = re.sub(r'<[^>]+>', '', course_text).strip()

    # Extract clean title without quotes and HTML - clean version for display
    title = plain_text.strip()

    # Remove quotes around course names
    title = re.sub(r'"([^"]+)"', r'\1', title)

    # Clean up any remaining HTML artifacts
    title = re.sub(r'<[^>]+>', '', title)

    # Clean up extra whitespace
    title = re.sub(r'\s+', ' ', title).strip()

    if not title:
        return None

    # Extract instructors
    instructors = []
    instructor_match = re.search(r'\(([^)]+)\)', plain_text)
    if instructor_match:
        instructor_text = instructor_match.group(1)
        # Split by common separators
        instructors = [name.strip() for name in re.split(r'[,&]', instructor_text) if name.strip()]

    # Determine course type
    course_type = extract_course_type(title, plain_text)

    # Extract links and PDFs from HTML
    links, pdfs = extract_links_and_pdfs_html(li_html, BASE_URL)

    # Scrape subdomain content for Heidelberg University links
    subdomain_content = ""
    for link in links:
        if link.get('url') and ('heidelberg.de' in link['url'] or 'uni-heidelberg.de' in link['url']):
            scraped_content = scrape_subdomain_content(link['url'])
            if scraped_content and len(scraped_content.strip()) > 50:  # Only add substantial content
                subdomain_content += f"\n\n--- Content from {link['url']} ---\n{scraped_content}"

    # Use the complete original text as base content
    base_content = plain_text.strip()

    # Combine base content with subdomain content only if subdomain content exists
    final_content = base_content
    if subdomain_content.strip():
        final_content = base_content + subdomain_content

    # Create course entry
    course = {
        'title': title,  # Clean title without quotes for display
        'instructor': ', '.join(instructors) if instructors else '',
        'instructors': ', '.join(instructors) if instructors else '',
        'course_type': course_type,
        'semester': semester_info['full_semester'],
        'semester_key': semester_info['semester_key'],
        'semester_term': semester_info['semester_term'],
        'semester_year': semester_info['semester_year'],
        'semester_sort': semester_info['semester_sort'],
        'links': links,
        'pdfs': pdfs,
        'content': final_content,  # Complete original text + any meaningful subdomain content
        'description': title,  # Description matches the clean title
        'active': False,  # Default to inactive
        'language': 'English' if any(word in plain_text.lower() for word in ['english', 'englisch']) else 'German',
        'source': source_name
    }

    return course

def create_teaching_file(course: dict, index: int):
    """Create a teaching markdown file."""
    if not course.get('title'):
        return None

    # Generate filename
    semester_key = course.get('semester_key', 'unknown')
    title_slug = slugify(course.get('title', f'course-{index}'))

    # Limit filename length
    if len(title_slug) > 80:
        title_slug = title_slug[:80]

    filename = f"{semester_key.lower()}-{title_slug}.md"
    filepath = TEACHING_DIR / filename

    # Prepare front matter
    front_matter = {
        'layout': 'teaching',
        'title': course.get('title', 'Untitled Course'),
        'semester': course.get('semester', ''),
        'instructor': course.get('instructor', ''),
        'course_type': course.get('course_type', 'Seminar'),
        'semester_term': course.get('semester_term', ''),
        'semester_year': course.get('semester_year', 0),
        'semester_key': course.get('semester_key', ''),
        'semester_sort': course.get('semester_sort', 0),
        'active': course.get('active', False),
        'instructors': course.get('instructors', ''),
        'description': course.get('description', ''),
    }

    # Add links if available
    if course.get('links'):
        valid_links = []
        for link in course['links']:
            if isinstance(link, dict) and link.get('url'):
                valid_links.append(link)
        if valid_links:
            front_matter['links'] = valid_links

    # Add PDFs if available
    if course.get('pdfs'):
        valid_pdfs = []
        for pdf in course['pdfs']:
            if isinstance(pdf, dict) and (pdf.get('file') or pdf.get('url')):
                valid_pdfs.append(pdf)
        if valid_pdfs:
            front_matter['pdfs'] = valid_pdfs

    # Write the file
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('---\n')
            # Simple YAML-like front matter without external dependencies
            for key, value in front_matter.items():
                if isinstance(value, list):
                    f.write(f'{key}:\n')
                    for item in value:
                        if isinstance(item, dict):
                            clean_label = str(item.get("label", "")).replace('"', '').strip()
                            f.write(f'  - label: "{clean_label}"\n')
                            if 'url' in item:
                                f.write(f'    url: "{item["url"]}"\n')
                            if 'file' in item:
                                f.write(f'    file: "{item["file"]}"\n')
                        else:
                            clean_item = str(item).replace('"', '').strip()
                            f.write(f'  - "{clean_item}"\n')
                elif isinstance(value, bool):
                    f.write(f'{key}: {str(value).lower()}\n')
                else:
                    # Clean quotes from the value and ensure proper YAML formatting
                    clean_value = str(value).replace('"', '').strip()
                    needs_quotes = (
                        '"' in str(value) or
                        ':' in clean_value or
                        clean_value != str(value) or
                        clean_value.startswith(' ') or
                        clean_value.endswith(' ')
                    )

                    if needs_quotes:
                        # Quote values that contain special characters or need protection
                        f.write(f'{key}: "{clean_value}"\n')
                    else:
                        # Simple value without quotes
                        f.write(f'{key}: {clean_value}\n')
            f.write('---\n\n')

            # Add content section - preserve original format without legacy text
            if course.get('content') and course['content'].strip():
                f.write(course['content'].strip() + '\n\n')

        print(f"✅ Created teaching file: {filename}")
        return filepath

    except Exception as e:
        print(f"❌ Error creating file {filename}: {e}")
        return None

def implement_legacy_heidelberg_content():
    """Implement the exact content from the Heidelberg University teaching pages."""
    print("🚀 Implementing Heidelberg University teaching content...")
    print(f"📂 Teaching files will be saved to: {TEACHING_DIR}")
    print(f"📥 Downloads will be saved to: {DOWNLOAD_DIR}")

    # Clean up existing teaching files (except index.md)
    print("🧹 Cleaning up existing teaching files...")
    if TEACHING_DIR.exists():
        for file_path in TEACHING_DIR.glob("*.md"):
            if file_path.name != "index.md":  # Keep the index file
                file_path.unlink()
                print(f"  🗑️  Deleted: {file_path.name}")

    # Read the HTML files provided by the user
    html_sources = []

    # Current teaching page (page1.txt)
    try:
        with open('/home/victor/Projects/HiWiAGJob/page1.txt', 'r', encoding='utf-8') as f:
            html_sources.append(('current-teaching', f.read()))
        print("✅ Loaded page1.txt (Current teaching page)")
    except Exception as e:
        print(f"⚠️ Error loading page1.txt: {e}")

    # Past teaching page (page2.txt)
    try:
        with open('/home/victor/Projects/HiWiAGJob/page2.txt', 'r', encoding='utf-8') as f:
            html_sources.append(('past-teaching', f.read()))
        print("✅ Loaded page2.txt (Past teaching page)")
    except Exception as e:
        print(f"⚠️ Error loading page2.txt: {e}")

    print(f"📊 Total HTML sources loaded: {len(html_sources)}")

    # Parse all HTML sources to extract teaching entries
    all_teachings = []

    for source_name, html_content in html_sources:
        print(f"🔍 Parsing {source_name}...")
        teachings = parse_teaching_from_html(html_content, source_name)
        all_teachings.extend(teachings)

    print(f"📚 Total teaching entries extracted: {len(all_teachings)}")

    # Create teaching files
    created_files = []
    for i, course in enumerate(all_teachings):
        filepath = create_teaching_file(course, i)
        if filepath:
            created_files.append(filepath)
        time.sleep(0.1)

    print(f"✅ Successfully created {len(created_files)} teaching files")

    # Update the teaching index page
    print("🔄 Updating teaching index page...")
    update_teaching_page(len(created_files))

    return len(created_files)

def scrape_all_teachings():
    """Main function - parse the provided HTML content."""
    return implement_legacy_heidelberg_content()

def update_teaching_page(teaching_count: int):
    """Update the teaching page with a note about the new content."""
    teaching_index = TEACHING_DIR / "index.md"

    if teaching_index.exists():
        content = teaching_index.read_text(encoding='utf-8')

        # Add a note about the updated content
        if "teaching-page" in content:
            # Find and update any existing notes
            import datetime
            timestamp = datetime.datetime.now().isoformat()
            new_note = f"<!-- All {teaching_count} teaching entries from Heidelberg website are included and up to date as of {timestamp[:19]} -->"

            # Replace or add the note
            if "<!--" in content and "teaching entries" in content:
                # Replace existing note
                content = re.sub(r'<!--.*?teaching entries.*?-->', new_note, content, flags=re.DOTALL)
            else:
                # Add new note
                content = content.replace('<div class="teaching-page">', f'<div class="teaching-page">\n  {new_note}')

            # Write back the updated content
            teaching_index.write_text(content, encoding='utf-8')
            print("✅ Updated teaching index page with new content information")

def main():
    """Main entry point."""
    try:
        teaching_count = scrape_all_teachings()

        print("\n🎉 Teaching scraper completed successfully!")
        print(f"📚 Total teaching entries processed: {teaching_count}")
        print(f"📂 Teaching files location: {TEACHING_DIR}")
        print(f"📥 Downloaded assets location: {DOWNLOAD_DIR}")
        print("\n🔄 The website has been updated with the new teaching content.")
        print("📋 Make sure to rebuild your Jekyll site to see the changes.")

    except Exception as e:
        print(f"❌ Error during scraping: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
