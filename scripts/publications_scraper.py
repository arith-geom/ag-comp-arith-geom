#!/usr/bin/env python3
"""
Comprehensive Publications Scraper for AG Computational Arithmetic Geometry

This scraper will:
1. Scrape all publications from https://typo.iwr.uni-heidelberg.de/groups/arith-geom/publications.html
2. Keep the original content intact (no summarizing)
3. Download all PDFs and images
4. Create new publication files with the same structure as current cards
5. Update the website with the new content
"""

import os
import re
import sys
import time
import requests
from pathlib import Path
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import yaml
import urllib.request
from urllib.error import HTTPError, URLError

# Configuration
BASE_URL = "https://typo.iwr.uni-heidelberg.de/groups/arith-geom/"
PUBLICATIONS_URL = urljoin(BASE_URL, "publications.html")
ROOT_DIR = Path(__file__).resolve().parents[1]
PUBLICATIONS_DIR = ROOT_DIR / "_publications"
ASSETS_DIR = ROOT_DIR / "assets/uploads"
DOWNLOAD_DIR = ASSETS_DIR

# Create directories
PUBLICATIONS_DIR.mkdir(parents=True, exist_ok=True)
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125 Safari/537.36",
}

def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    if not text:
        return "publication"
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
        response = requests.get(url, headers=HEADERS, timeout=30, stream=True)
        if response.status_code == 200:
            filepath = DOWNLOAD_DIR / filename
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"✅ Downloaded: {filename}")
            return f"/assets/uploads/{filename}"
        else:
            print(f"❌ Failed to download {url}: HTTP {response.status_code}")
            return ""
    except Exception as e:
        print(f"❌ Error downloading {url}: {e}")
        return ""

def extract_publications_from_page(url: str) -> list:
    """Extract all publications from the publications page."""
    publications = []

    try:
        print(f"🌐 Scraping publications from: {url}")
        response = requests.get(url, headers=HEADERS, timeout=30)
        if response.status_code != 200:
            print(f"❌ Failed to fetch {url}: HTTP {response.status_code}")
            return publications

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the main content area with publications
        content_div = soup.find('div', {'id': 'c1579'})
        if not content_div:
            print("❌ Could not find publications content area")
            return publications

        # Extract member publication links
        member_links = content_div.find_all('a', href=True)
        for link in member_links:
            href = link.get('href')
            if not href or 'members' not in href:
                continue

            # Convert relative URLs to absolute
            if href.startswith('/'):
                href = urljoin(BASE_URL, href)
            elif not href.startswith(('http://', 'https://')):
                href = urljoin(BASE_URL, href)

            member_name = link.get_text().strip()
            print(f"🔗 Found member publications link: {member_name} -> {href}")

            # Scrape individual member publication pages
            member_publications = scrape_member_publications(href, member_name)
            publications.extend(member_publications)

        # Extract software packages
        software_packages = extract_software_packages(content_div, url)
        publications.extend(software_packages)

        # Also try to extract publications from the entire page content
        page_publications = extract_publications_from_content(soup.get_text(), url)
        publications.extend(page_publications)

        print(f"📚 Found {len(publications)} publications")

    except Exception as e:
        print(f"❌ Error scraping {url}: {e}")

    return publications

def extract_publications_from_content(content: str, base_url: str) -> list:
    """Extract publications from plain text content."""
    publications = []

    # Look for patterns that indicate publications
    lines = content.split('\n')
    current_pub = {}
    in_publication = False

    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue

        # Look for publication indicators
        pub_indicators = [
            'journal', 'proceedings', 'conference', 'arxiv', 'preprint',
            'published', 'submitted', 'accepted', 'in press', 'forthcoming'
        ]

        # Look for year patterns - more specific patterns for journal articles
        year_patterns = [
            r'\b(19|20)\d{2}\b',  # General year pattern
            r'\((\d{4})\)',      # Year in parentheses
            r'(\d{4}),\s*no\.',  # Year followed by issue number
            r'(\d{4})\s*,\s*\d+', # Year, volume
            r'vol\.\s*\d+.*(\d{4})', # Volume with year
        ]

        # Check if this line contains publication information
        contains_pub_info = any(indicator in line.lower() for indicator in pub_indicators)
        contains_year = any(re.search(pattern, line) for pattern in year_patterns)

        # Look for specific patterns like journal names with years
        journal_patterns = [
            r'\. Algebra.*(\d{4})',
            r'J\. Reine Angew\. Math\.*(\d{4})',
            r'Math\. Z\.*(\d{4})',
            r'Compos\. Math\.*(\d{4})',
            r'J\. Number Theory.*(\d{4})',
            r'Amer\. J\. Math\.*(\d{4})',
            r'Duke Math\. J\.*(\d{4})',
            r'Inventiones Math\.*(\d{4})',
            r'Manuscripta Math\.*(\d{4})',
            r'Math\. Ann\.*(\d{4})',
            r'J\. Math\. Cryptol\.*(\d{4})',
            r'Compositio Math\.*(\d{4})',
            r'Asterisque.*(\d{4})',
            r'LMS Lecture Note.*(\d{4})',
            r'Trans\. Amer\. Math\. Soc\.*(\d{4})',
        ]

        has_journal_info = any(re.search(pattern, line) for pattern in journal_patterns)

        if contains_pub_info or contains_year or has_journal_info:
            if current_pub and current_pub.get('title'):
                publications.append(current_pub.copy())

            # Start new publication
            current_pub = {
                'title': '',
                'authors': '',
                'year': '',
                'type': 'Journal Article',
                'abstract': '',
                'links': [],
                'pdfs': [],
                'content': '',
                'keywords': []
            }
            in_publication = True

        if in_publication:
            # Extract title (usually the first substantial line that doesn't contain URLs)
            if not current_pub['title'] and len(line) > 10 and not line.startswith('http') and not 'pdf' in line.lower():
                # Clean up the title - remove common prefixes and HTML
                title = line
                title = re.sub(r'<[^>]+>', '', title)  # Remove HTML tags
                title = re.sub(r'\([^)]*\)', '', title)  # Remove parenthetical content
                title = re.sub(r'\s+', ' ', title)  # Normalize whitespace
                title = title.strip()

                if title:
                    current_pub['title'] = title

            # Extract year using multiple patterns
            if not current_pub['year']:
                # Try journal-specific patterns first
                for pattern in journal_patterns:
                    match = re.search(pattern, line)
                    if match:
                        current_pub['year'] = match.group(1)
                        break

                # If no journal pattern matched, try general year patterns
                if not current_pub['year']:
                    for pattern in year_patterns:
                        match = re.search(pattern, line)
                        if match:
                            current_pub['year'] = match.group(1)
                            break

            # Extract URLs
            urls = re.findall(r'https?://[^\s\)]+', line)
            for url in urls:
                url = url.rstrip('.,)')
                if url.lower().endswith('.pdf'):
                    filename = os.path.basename(url)
                    local_path = download_file(url, filename)
                    if local_path:
                        current_pub['pdfs'].append({
                            'label': 'PDF',
                            'file': local_path,
                            'url': url
                        })
                else:
                    current_pub['links'].append({
                        'label': 'Link',
                        'url': url
                    })

    # Add the last publication
    if current_pub and current_pub.get('title'):
        publications.append(current_pub)

    return publications

def scrape_member_publications(url: str, member_name: str) -> list:
    """Scrape publications from an individual member's page."""
    publications = []

    try:
        print(f"👤 Scraping publications for {member_name}")
        response = requests.get(url, headers=HEADERS, timeout=30)
        if response.status_code != 200:
            print(f"❌ Failed to fetch member page {url}")
            return publications

        soup = BeautifulSoup(response.text, 'html.parser')

        # Look for publication content in various possible locations
        content_candidates = [
            soup.find('div', {'id': 'content'}),
            soup.find('div', {'class': 'content'}),
            soup.find('main'),
            soup.body
        ]

        content_area = None
        for candidate in content_candidates:
            if candidate and len(candidate.get_text().strip()) > 100:
                content_area = candidate
                break

        if not content_area:
            print(f"❌ Could not find content area for {member_name}")
            return publications

        # Extract links and PDFs
        links, pdfs = extract_links_and_pdfs(content_area, url)

        # Get all text content
        content_text = content_area.get_text()

        # Create a publication entry for the member
        publication = {
            'title': f"Publications by {member_name}",
            'authors': member_name,
            'year': '2024',  # Default year
            'type': 'Publications',
            'abstract': f'Complete list of publications by {member_name}',
            'content': content_text[:2000],  # Limit content length
            'links': links,
            'pdfs': pdfs,
            'keywords': ['publications', 'research', member_name.lower().replace(' ', '-')]
        }

        publications.append(publication)

    except Exception as e:
        print(f"❌ Error scraping member {member_name}: {e}")

    return publications

def extract_software_packages(content_div, base_url: str) -> list:
    """Extract software packages from the content."""
    software_packages = []

    try:
        # Find software packages section
        h2_tags = content_div.find_all('h2')
        software_section = None

        for h2 in h2_tags:
            if 'software' in h2.get_text().lower():
                software_section = h2
                break

        if not software_section:
            return software_packages

        # Get all list items after the software heading
        ul = software_section.find_next('ul')
        if not ul:
            return software_packages

        for li in ul.find_all('li'):
            text = li.get_text().strip()
            if not text:
                continue

            # Extract links from the list item
            links = []
            pdfs = []

            for a in li.find_all('a', href=True):
                href = a.get('href')
                label = a.get_text().strip()

                if href.startswith('/'):
                    href = urljoin(base_url, href)
                elif not href.startswith(('http://', 'https://')):
                    href = urljoin(base_url, href)

                if href.lower().endswith('.pdf'):
                    filename = os.path.basename(urlparse(href).path)
                    local_path = download_file(href, filename)
                    if local_path:
                        pdfs.append({
                            'label': label or 'PDF',
                            'file': local_path,
                            'url': href
                        })
                else:
                    links.append({
                        'label': label,
                        'url': href
                    })

            # Create software package entry
            package = {
                'title': text[:100] + '...' if len(text) > 100 else text,
                'authors': 'AG Computational Arithmetic Geometry',
                'year': '2024',
                'type': 'Software',
                'abstract': text,
                'content': text,
                'links': links,
                'pdfs': pdfs,
                'keywords': ['software', 'magma', 'package']
            }

            software_packages.append(package)

    except Exception as e:
        print(f"❌ Error extracting software packages: {e}")

    return software_packages

def extract_links_and_pdfs(soup, base_url: str) -> tuple:
    """Extract all links and PDFs from the page."""
    links = []
    pdfs = []

    for a in soup.find_all('a', href=True):
        href = a.get('href')
        if not href:
            continue

        # Convert relative URLs to absolute
        if href.startswith('/'):
            href = urljoin(base_url, href)
        elif not href.startswith(('http://', 'https://')):
            href = urljoin(base_url, href)

        text = a.get_text().strip()
        if not text:
            text = href

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

        # Add as general link
        elif any(keyword in text.lower() for keyword in ['preprint', 'journal', 'arXiv', 'doi', 'proceedings']):
            links.append({
                'label': text,
                'url': href
            })

    return links, pdfs

def create_publication_file(publication: dict, index: int):
    """Create a publication markdown file."""
    if not publication.get('title'):
        return None

    # Generate filename with proper year handling
    year = publication.get('year', '2024')
    # Ensure year is a 4-digit number
    if not year.isdigit() or len(year) != 4:
        year = '2024'

    title_slug = slugify(publication.get('title', f'publication-{index}'))
    # Limit filename length to avoid filesystem issues
    if len(title_slug) > 80:
        title_slug = title_slug[:80]

    filename = f"{year}-{title_slug}.md"
    filepath = PUBLICATIONS_DIR / filename

    # Determine publication type
    pub_type = publication.get('type', 'Preprint')

    # Prepare front matter with better validation
    front_matter = {
        'layout': 'publication',
        'title': publication.get('title', 'Untitled Publication'),
        'authors': publication.get('authors', ''),
        'year': year,
        'type': pub_type,
        'status': 'Published' if pub_type != 'Preprint' else 'Preprint',
        'order': int(year) * 100 + (100 - (index % 100)),  # Sort by year, then by index
    }

    # Don't add abstract or keywords to front matter to match original website structure

    # Add links if available and valid
    if publication.get('links'):
        valid_links = []
        for link in publication['links']:
            if isinstance(link, dict) and link.get('url'):
                valid_links.append(link)
        if valid_links:
            front_matter['links'] = valid_links

    # Add PDFs if available and valid
    if publication.get('pdfs'):
        valid_pdfs = []
        for pdf in publication['pdfs']:
            if isinstance(pdf, dict) and (pdf.get('file') or pdf.get('url')):
                # Ensure PDF file path is correct
                if pdf.get('file') and not pdf['file'].startswith('/'):
                    pdf['file'] = f"/assets/uploads/{pdf['file']}"
                valid_pdfs.append(pdf)
        if valid_pdfs:
            front_matter['pdfs'] = valid_pdfs

    # Write the file
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('---\n')
            yaml.dump(front_matter, f, allow_unicode=True, sort_keys=False)
            f.write('---\n\n')

            # Add content section
            # Simple content structure matching original website
            if publication.get('content') and publication['content'].strip():
                f.write('## Publication Details\n\n')
                f.write(publication['content'].strip() + '\n\n')

        print(f"✅ Created publication file: {filename} (Year: {year}, Type: {pub_type})")
        return filepath

    except Exception as e:
        print(f"❌ Error creating file {filename}: {e}")
        return None

def cleanup_existing_files():
    """Clean up existing publication files and uploads before starting fresh."""
    try:
        # Remove all files from publications directory
        if PUBLICATIONS_DIR.exists():
            print("  📁 Removing old publication files...")
            for file_path in PUBLICATIONS_DIR.glob("*.md"):
                file_path.unlink()
                print(f"    🗑️ Removed: {file_path.name}")

        # Remove all files from uploads directory
        if DOWNLOAD_DIR.exists():
            print("  📥 Removing old uploaded files...")
            for file_path in DOWNLOAD_DIR.glob("*"):
                if file_path.is_file():
                    file_path.unlink()
                    print(f"    🗑️ Removed: {file_path.name}")

        print("  ✅ Cleanup completed!")

    except Exception as e:
        print(f"  ⚠️ Error during cleanup: {e}")

def implement_original_heidelberg_content():
    """Implement the exact content from the original Heidelberg website HTML provided by the user."""
    print("🚀 Implementing original Heidelberg website content...")
    print(f"📂 Publications will be saved to: {PUBLICATIONS_DIR}")
    print(f"📥 Downloads will be saved to: {DOWNLOAD_DIR}")

    # Clean up existing files before starting
    print("🧹 Cleaning up existing files...")
    cleanup_existing_files()

    # Read and parse all three HTML files provided by the user
    html_sources = []

    # Pub1.txt - Prof. Dr. Gebhard Böckle's publications
    try:
        with open('/home/victorrr/Downloads/hiwiwebsiteaddingnewstuff/Pub1.txt', 'r', encoding='utf-8') as f:
            html_sources.append(('gebhard', f.read()))
        print("✅ Loaded Pub1.txt (Gebhard Böckle's publications)")
    except Exception as e:
        print(f"⚠️ Error loading Pub1.txt: {e}")

    # Pub2.txt - Peter Gräf's publications
    try:
        with open('/home/victorrr/Downloads/hiwiwebsiteaddingnewstuff/Pub2.txt', 'r', encoding='utf-8') as f:
            html_sources.append(('peter', f.read()))
        print("✅ Loaded Pub2.txt (Peter Gräf's publications)")
    except Exception as e:
        print(f"⚠️ Error loading Pub2.txt: {e}")

    # Pub3.txt - Main publications page with links
    try:
        with open('/home/victorrr/Downloads/hiwiwebsiteaddingnewstuff/Pub3.txt', 'r', encoding='utf-8') as f:
            html_sources.append(('main', f.read()))
        print("✅ Loaded Pub3.txt (Main publications page)")
    except Exception as e:
        print(f"⚠️ Error loading Pub3.txt: {e}")

    print(f"📊 Total HTML sources loaded: {len(html_sources)}")

    # Parse all HTML sources to extract individual publications
    publications = []

    for source_name, html_content in html_sources:
        print(f"🔍 Parsing {source_name} publications...")

        soup = BeautifulSoup(html_content, 'html.parser')

        if source_name == 'gebhard':
            # Parse Gebhard Böckle's publications (Pub1.txt)
            publications_list = soup.find_all('li')
            for li in publications_list:
                try:
                    # Extract title from the main link - be smarter about author vs title links
                    all_links = li.find_all('a', href=True)

                    # First, try to find the main title link (usually the first substantial link that's not an author)
                    main_link = None
                    title = ""
                    external_url = ""

                    # Look for the first link that looks like a title (longer text, not just initials)
                    for link in all_links:
                        link_text = link.get_text().strip()
                        link_href = link.get('href')

                        # Skip mathscinet author links (these are author references)
                        # But keep mathscinet publication links (mr=...)
                        if link_href and link_href.startswith('http://www.ams.org/mathscinet') and not 'mr=' in link_href:
                            continue

                        # Check if this looks like an author name (short, just initials, or in author list)
                        is_likely_author = (
                            len(link_text) <= 3 or  # Very short (like "R." or "C.")
                            link_text in ['R. Pink', 'G. Wiese', 'A.-K. Juschka', 'W. Gajda', 'S. Petersen', 'T. Centeleghe', 'R. Butenuth', 'M. Blickle', 'U. Hartl', 'C. Khare', 'A. Mezard', 'M. Dettweiler'] or
                            (link.previous_sibling and link.previous_sibling.strip() == '(joint with') or
                            link_text.lower() in ['joint with'] or
                            link_text.lower().strip() in ['pdf']  # PDF links should not be used as titles
                        )

                        if not is_likely_author and link_href and len(link_text) > 5:  # Must have substantial text
                            main_link = link
                            title = link_text
                            external_url = link_href
                            break

                    # Fallback: if no good title link found, try different approaches
                    if not main_link:
                        for link in all_links:
                            link_href = link.get('href')
                            link_text = link.get_text().strip()
                            # Skip PDF links even in fallback
                            if link_href and not link_href.startswith('http://www.ams.org/mathscinet') and link_text.lower().strip() != 'pdf':
                                main_link = link
                                title = link_text
                                external_url = link_href
                                break

                    # Last resort: if no external links found, extract title from text content
                    if not main_link:
                        # Extract text content and clean it up
                        text_content = li.get_text().strip()

                        # Remove PDF links and their surrounding parentheses - more comprehensive pattern
                        text_content = re.sub(r'\s*\([^)]*pdf[^)]*\)', '', text_content, flags=re.IGNORECASE)

                        # Remove extra whitespace and commas at the end
                        text_content = re.sub(r'\s*,.*$', '', text_content).strip()

                        # Remove page numbers at the end (like ", 183 pages.")
                        text_content = re.sub(r'\s*,?\s*\d+\s*pages?\.?$', '', text_content, flags=re.IGNORECASE).strip()

                        # Remove any remaining "pdf" text
                        text_content = re.sub(r'\s*pdf\.?\s*$', '', text_content, flags=re.IGNORECASE).strip()

                        # Clean up any remaining parentheses at the end
                        text_content = re.sub(r'\s*\([^)]*\)\s*$', '', text_content).strip()

                        if len(text_content) > 5:  # Must have substantial content
                            title = text_content[:100]  # Limit length
                            external_url = ""  # No external link
                            # Create a dummy main_link object for consistency
                            class DummyLink:
                                def __init__(self, text):
                                    self.text = text
                                def get_text(self):
                                    return self.text
                                def get(self, attr):
                                    return ""
                            main_link = DummyLink(title)
                        else:
                            continue  # Skip if no substantial content

                    # If still no link found, skip this item
                    if not main_link:
                        continue

                    # Extract PDF link
                    pdf_link = li.find('a', string=re.compile(r'pdf', re.IGNORECASE))
                    pdf_url = None
                    if pdf_link:
                        pdf_href = pdf_link.get('href')
                        if pdf_href:
                            # Convert relative path to absolute
                            if pdf_href.startswith('../../../../'):
                                pdf_url = 'https://typo.iwr.uni-heidelberg.de' + pdf_href[11:]
                            elif pdf_href.startswith('/'):
                                pdf_url = 'https://typo.iwr.uni-heidelberg.de' + pdf_href
                            else:
                                pdf_url = pdf_href

                            # Download the PDF
                            pdf_filename = os.path.basename(pdf_url)
                            local_path = download_file(pdf_url, pdf_filename)

                    # Extract year from the citation info
                    year_match = re.search(r'\b(19|20)\d{2}\b', li.get_text())
                    year = year_match.group() if year_match else '?'

                    # Extract journal/venue information
                    em_tags = li.find_all('em')
                    journal_info = ""
                    if em_tags:
                        journal_info = ' '.join([em.get_text().strip() for em in em_tags])

                    # Extract co-authors
                    co_authors = []
                    text_content = li.get_text()
                    if 'joint with' in text_content.lower():
                        joint_matches = re.findall(r'joint with ([^)]+)', text_content)
                        for match in joint_matches:
                            co_authors.extend([name.strip() for name in match.split(',')])

                    # Build authors list
                    authors = ["Gebhard Böckle"]
                    authors.extend(co_authors)

                    # Create publication entry (matching original website structure - no separate abstract/keywords)
                    publication = {
                        'title': title,
                        'authors': ', '.join(authors),
                        'year': year,
                        'type': 'Journal Article',
                        'abstract': '',  # No separate abstract in original site
                        'links': [{'label': 'Journal Link', 'url': external_url}],
                        'pdfs': [{'label': 'PDF', 'file': local_path if pdf_url and local_path else pdf_url, 'url': pdf_url}] if pdf_url else [],
                        'content': f"{title}. {journal_info} {li.get_text().split(')')[-1] if ')' in li.get_text() else ''}".strip(),  # Simple content like original
                        'keywords': []  # No keywords in original site
                    }

                    publications.append(publication)
                    print(f"✅ Extracted publication: {title[:50]}... ({year})")

                except Exception as e:
                    print(f"⚠️ Error parsing publication: {e}")
                    continue

        elif source_name == 'peter':
            # Parse Peter Gräf's publications (Pub2.txt)
            publications_list = soup.find_all('li')
            for li in publications_list:
                try:
                    # Look for publication links in Peter's page
                    links = li.find_all('a', href=True)
                    for link in links:
                        href = link.get('href')
                        if 'springer.com' in href or 'link.springer.com' in href or 'dx.doi.org' in href or 'jtnb.centre-mersenne.org' in href:
                            title = li.get_text().strip()
                            # Clean up title by removing URLs and extra text
                            title = re.sub(r'http[s]?://[^\s)]+', '', title)
                            title = re.sub(r'published version.*', '', title, flags=re.IGNORECASE)
                            title = re.sub(r'Journal de.*', '', title, flags=re.IGNORECASE)
                            title = re.sub(r'Research in.*', '', title, flags=re.IGNORECASE)
                            title = title.strip().strip(',').strip()

                            if len(title) > 20:  # Only include substantial titles
                                # Extract year
                                year_match = re.search(r'\b(19|20)\d{2}\b', li.get_text())
                                year = year_match.group() if year_match else '?'

                                # Create publication entry (matching original website structure)
                                publication = {
                                    'title': title,
                                    'authors': 'Peter Gräf',
                                    'year': year,
                                    'type': 'Journal Article',
                                    'abstract': '',  # No separate abstract in original site
                                    'links': [{'label': 'Journal Link', 'url': href}],
                                    'pdfs': [],
                                    'content': title,  # Simple content like original
                                    'keywords': []  # No keywords in original site
                                }

                                publications.append(publication)
                                print(f"✅ Extracted publication: {title[:50]}... ({year})")
                                break  # Only take the first journal link per publication

                except Exception as e:
                    print(f"⚠️ Error parsing Peter publication: {e}")
                    continue

        elif source_name == 'main':
            # Parse main publications page (Pub3.txt) - this has links to software packages
            # Look for software package information
            ul_elements = soup.find_all('ul')
            for ul in ul_elements:
                li_elements = ul.find_all('li')
                for li in li_elements:
                    text = li.get_text()
                    if 'Magma package' in text or 'package' in text.lower():
                        # This is a software package entry
                        title = text.strip()

                        # Extract links from the original HTML
                        links = []
                        for a_tag in li.find_all('a', href=True):
                            href = a_tag.get('href')
                            link_text = a_tag.get_text().strip()

                            # Convert relative URLs to absolute
                            if href.startswith('../') or href.startswith('members/'):
                                # These are internal links to the Heidelberg site
                                full_url = f"https://typo.iwr.uni-heidelberg.de/groups/arith-geom/{href}"
                                if 'members/ralf-butenuth' in href:
                                    links.append({'label': 'Magma package QaQuotGraphs', 'url': full_url})
                                elif 'github.com/lhofmann' in href:
                                    links.append({'label': 'GitHub Repository', 'url': href})
                                elif 'github.com/b-cakir' in href:
                                    links.append({'label': 'GitHub Repository', 'url': href})
                                elif 'Thesis_Cakir.pdf' in href:
                                    # Convert PDF link to absolute URL
                                    pdf_url = 'https://typo.iwr.uni-heidelberg.de' + href.replace('../', '/')
                                    links.append({'label': 'Thesis PDF', 'url': pdf_url})
                            else:
                                # External links (GitHub, etc.)
                                links.append({'label': link_text or 'Software Link', 'url': href})

                        publication = {
                            'title': title,
                            'authors': 'Research Group',
                            'year': '2024',
                            'type': 'Software',
                            'abstract': '',  # No abstract in original site
                            'links': links,
                            'pdfs': [],  # PDFs handled through links
                            'content': '',  # Content is already in the title for software packages
                            'keywords': []  # No keywords section in original
                        }

                        publications.append(publication)
                        print(f"✅ Extracted software: {title[:50]}... with {len(links)} links")

    print(f"📊 Total publications extracted from all HTML sources: {len(publications)}")

    # Create publication files
    created_files = []
    for i, publication in enumerate(publications):
        filepath = create_publication_file(publication, i)
        if filepath:
            created_files.append(filepath)
        time.sleep(0.1)

    print(f"✅ Successfully created {len(created_files)} publication files")

    # Update the publications page to reflect changes
    print("🔄 Updating publications page...")
    update_publications_page(len(created_files))

    return len(created_files)

def scrape_all_publications():
    """Main function - now just calls the original HTML implementation."""
    return implement_original_heidelberg_content()

def search_arxiv_publications():
    """Search for publications by group members on arXiv."""
    publications = []

    # Key group members to search for
    members = [
        "Gebhard Böckle",
        "Peter Gräf",
        "Barinder Banwait",
        "Ralf Butenuth",
        "Judith Ludwig",
        "Oguz Gezmis",
        "Alain Muller",
        "Juan Marcos Cervino",
        "Yujia Qiu",
        "Tommaso Centeleghe",
        "Patrik Hubschmid",
        "Yamidt Bermudez Tobon",
        "Sundeep Balaji",
        "Narasimha Kumar Cheraku",
        "Alireza Shavali",
        "Theresa Kaiser",
        "Sriram Chinthalagiri Venkata",
        "Paola Chilla"
    ]

    for member in members:
        try:
            print(f"🔍 Searching arXiv for {member}")
            # Search arXiv API
            search_query = f"au:{member.replace(' ', '_')}"
            arxiv_url = f"http://export.arxiv.org/api/query?search_query={search_query}&max_results=50"

            response = requests.get(arxiv_url, headers=HEADERS, timeout=30)
            if response.status_code == 200:
                # Parse arXiv XML response
                soup = BeautifulSoup(response.content, 'xml')

                for entry in soup.find_all('entry'):
                    title = entry.title.get_text().strip()
                    authors = [author.get_text().strip() for author in entry.find_all('name')]
                    year = entry.published.get_text().strip()[:4] if entry.published else "2024"
                    abstract = entry.summary.get_text().strip() if entry.summary else ""
                    pdf_url = entry.find('link', {'title': 'pdf'})['href'] if entry.find('link', {'title': 'pdf'}) else ""

                    publication = {
                        'title': title,
                        'authors': ', '.join(authors),
                        'year': year,
                        'type': 'Preprint',
                        'abstract': abstract,
                        'links': [{'label': 'arXiv', 'url': entry.id.get_text()}],
                        'pdfs': [{'label': 'PDF', 'file': pdf_url, 'url': pdf_url}] if pdf_url else [],
                        'content': abstract,
                        'keywords': ['arXiv', 'preprint']
                    }

                    publications.append(publication)

        except Exception as e:
            print(f"⚠️ Error searching arXiv for {member}: {e}")

        time.sleep(1)  # Be respectful to the API

    return publications

def search_google_scholar():
    """Search Google Scholar for publications (limited due to API restrictions)."""
    publications = []

    # This is a simplified version - in practice, Google Scholar doesn't have a public API
    # but we can try to extract some information from search results
    members = ["Gebhard Böckle", "Peter Gräf", "Barinder Banwait"]

    for member in members:
        try:
            print(f"🔍 Searching Google Scholar for {member}")
            # This would require more sophisticated scraping and is limited by Google's terms
            # For now, we'll create placeholder entries that can be filled in manually
            publication = {
                'title': f"Publications by {member}",
                'authors': member,
                'year': '2024',
                'type': 'Publications',
                'abstract': f'Complete publication list for {member} from Google Scholar',
                'links': [{'label': f'Google Scholar - {member}', 'url': f'https://scholar.google.com/scholar?q={member.replace(" ", "+")}'}],
                'pdfs': [],
                'content': f'Publication list for {member} from academic sources',
                'keywords': ['google scholar', 'publications', member.lower().replace(' ', '-')]
            }

            publications.append(publication)

        except Exception as e:
            print(f"⚠️ Error searching Google Scholar for {member}: {e}")

    return publications

def extract_publications_from_pdfs():
    """Extract publication information from downloaded PDFs."""
    publications = []

    # List of PDFs we have that might contain publication lists
    pdf_files = [
        "Dissertation_Ralf-Butenuth.pdf",
        "Diplomarbeit_Ralf-Butenuth.pdf",
        "Thesis_Cakir.pdf",
        "qaquotgraphs-magma-package.pdf"
    ]

    for pdf_file in pdf_files:
        try:
            pdf_path = DOWNLOAD_DIR / pdf_file
            if pdf_path.exists():
                print(f"📄 Analyzing {pdf_file} for publications")

                # Create a publication entry for the thesis/dissertation
                title = pdf_file.replace('.pdf', '').replace('_', ' ').replace('-', ' ')
                publication = {
                    'title': title,
                    'authors': extract_author_from_filename(pdf_file),
                    'year': extract_year_from_filename(pdf_file) or '2024',
                    'type': 'Thesis' if 'thesis' in pdf_file.lower() else 'Journal Article',
                    'abstract': f'Academic work: {title}',
                    'links': [],
                    'pdfs': [{'label': 'PDF', 'file': f'/assets/uploads/{pdf_file}', 'url': f'/assets/uploads/{pdf_file}'}],
                    'content': f'Academic publication: {title}',
                    'keywords': ['thesis', 'dissertation', 'academic work']
                }

                publications.append(publication)

        except Exception as e:
            print(f"⚠️ Error processing {pdf_file}: {e}")

    return publications

def extract_author_from_filename(filename):
    """Extract author name from filename."""
    if 'boeckle' in filename.lower():
        return 'Gebhard Böckle'
    elif 'butenuth' in filename.lower():
        return 'Ralf Butenuth'
    elif 'graef' in filename.lower():
        return 'Peter Gräf'
    elif 'cakir' in filename.lower():
        return 'Burak Cakir'
    else:
        return 'AG Computational Arithmetic Geometry'

def extract_year_from_filename(filename):
    """Extract year from filename."""
    import re
    match = re.search(r'(\d{4})', filename)
    return match.group(1) if match else None

def search_dblp_publications():
    """Search DBLP for publications by group members."""
    publications = []

    # Key group members to search for on DBLP
    members = [
        "Gebhard Böckle",
        "Peter Gräf",
        "Barinder Banwait",
        "Ralf Butenuth"
    ]

    for member in members:
        try:
            print(f"🔍 Searching DBLP for {member}")
            # DBLP search URL
            search_name = member.replace(' ', '+').replace('ö', 'o').replace('ä', 'a').replace('ü', 'u')
            dblp_url = f"https://dblp.org/search?q={search_name}"

            response = requests.get(dblp_url, headers=HEADERS, timeout=30)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # Look for publication entries
                pub_entries = soup.find_all('li', {'class': 'entry'})

                for entry in pub_entries[:10]:  # Limit to first 10 results
                    title_elem = entry.find('span', {'class': 'title'})
                    year_elem = entry.find('span', {'itemprop': 'datePublished'})

                    if title_elem:
                        title = title_elem.get_text().strip()
                        year = year_elem.get_text().strip() if year_elem else '2024'

                        publication = {
                            'title': title,
                            'authors': member,
                            'year': year,
                            'type': 'Journal Article',
                            'abstract': f'Publication by {member} from DBLP',
                            'links': [{'label': 'DBLP', 'url': dblp_url}],
                            'pdfs': [],
                            'content': title,
                            'keywords': ['dblp', member.lower().replace(' ', '-')]
                        }

                        publications.append(publication)

        except Exception as e:
            print(f"⚠️ Error searching DBLP for {member}: {e}")

        time.sleep(1)

    return publications

def extract_from_member_page_content():
    """Extract publications from the actual member page content that was scraped."""
    publications = []

    # Since we have the actual publication content from Gebhard Böckle's page,
    # let's try to parse it properly
    try:
        print("🔍 Extracting publications from member page content...")

        # Parse the HTML content from the Heidelberg website (first few publications)
        html_content = """
        <li>(joint with A.-K. Juschka) <a href="http://www.sciencedirect.com/science/article/pii/S002186931500352X">Irreducibility of versal deformation rings in the (p,p)-case for 2-dimensional representations.</a> (<a href="https://typo.iwr.uni-heidelberg.de/fileadmin/groups/arithgeo/templates/data/Gebhard_Boeckle/BoeckleJuschka-Irreducibility.pdf">pdf</a>)<br><em>J. Algebra</em> 444 (2015), 81–123.</li>
        <li>(joint with W. Gajda, S. Petersen) <a href="http://dx.doi.org/10.1515/crelle-2015-0024">Independence of l-adic representations of geometric Galois groups.</a> (<a href="https://typo.iwr.uni-heidelberg.de/fileadmin/groups/arithgeo/templates/data/Gebhard_Boeckle/Boeckle-Gajda-Petersen-crelle-2015-0024.pdf">pdf</a>)<br><em>J. Reine Angew. Math. </em> (2015), 25 p.</li>
        <li><a href="http://dx.doi.org/10.1112/S0010437X15007290">Hecke characters associated to Drinfeld modular forms</a> (Appendix B joint with T. Centeleghe). (<a href="https://typo.iwr.uni-heidelberg.de/fileadmin/groups/arithgeo/templates/data/Gebhard_Boeckle/Boeckle-Centeleghe-HeckeCharactersAssociatedToDrinfeldModularForms.pdf">pdf</a>)<br><em>Compos. Math.</em> (2015), 53 p.</li>
        <li><a href="http://www.ams.org/leavingmsn?url=http://dx.doi.org/10.1007/s00209-013-1162-9">The distribution of the zeros of the Goss zeta-function for A=F2[x,y]/(y2+y+x3+x+1).</a> (<a href="https://typo.iwr.uni-heidelberg.de/fileadmin/groups/arithgeo/templates/data/Gebhard_Boeckle/ZeroDistribForOneA.pdf">pdf</a>)<br><em>Math. Z.</em> 275 (2013), no. 3-4, 835–861.</li>
        <li><a href="http://www.springerlink.com/content/ll5v246782212835/">Algebraic Hecke characters and compatible systems of abelian mod p Galois representations over global fields.</a> (<a href="https://typo.iwr.uni-heidelberg.de/fileadmin/groups/arithgeo/templates/data/Gebhard_Boeckle/Boeckle-AlgHeckeCharsAndStrictlyCompSys.pdf">pdf</a>)<br><em>Manuscripta Math.</em> 140 (2013), no. 3-4, 303-331.</li>
        """

        # Parse the HTML content to extract individual publications
        soup = BeautifulSoup(html_content, 'html.parser')
        publications_list = soup.find_all('li')

        for li in publications_list:
            try:
                # Extract title from the main link
                main_link = li.find('a', href=True)
                if not main_link:
                    continue

                title = main_link.get_text().strip()
                external_url = main_link.get('href')

                # Extract PDF link
                pdf_link = li.find('a', string=re.compile(r'pdf', re.IGNORECASE))
                pdf_url = None
                if pdf_link:
                    pdf_href = pdf_link.get('href')
                    if pdf_href:
                        # Convert relative path to absolute
                        if pdf_href.startswith('../../../../'):
                            pdf_url = 'https://typo.iwr.uni-heidelberg.de' + pdf_href[11:]
                        elif pdf_href.startswith('/'):
                            pdf_url = 'https://typo.iwr.uni-heidelberg.de' + pdf_href
                        else:
                            pdf_url = pdf_href

                        # Download the PDF
                        pdf_filename = os.path.basename(pdf_url)
                        local_path = download_file(pdf_url, pdf_filename)

                # Extract year from the citation info
                year_match = re.search(r'\b(19|20)\d{2}\b', li.get_text())
                year = year_match.group() if year_match else '?'

                # Extract journal/venue information
                em_tags = li.find_all('em')
                journal_info = ""
                if em_tags:
                    journal_info = ' '.join([em.get_text().strip() for em in em_tags])

                # Extract co-authors
                co_authors = []
                text_content = li.get_text()
                if 'joint with' in text_content.lower():
                    joint_matches = re.findall(r'joint with ([^)]+)', text_content)
                    for match in joint_matches:
                        co_authors.extend([name.strip() for name in match.split(',')])

                # Build authors list
                authors = ["Gebhard Böckle"]
                authors.extend(co_authors)

                # Create publication entry
                publication = {
                    'title': title,
                    'authors': ', '.join(authors),
                    'year': year,
                    'type': 'Journal Article',
                    'abstract': f"{journal_info} {li.get_text().split(')')[-1] if ')' in li.get_text() else ''}".strip(),
                    'links': [{'label': 'Journal Link', 'url': external_url}],
                    'pdfs': [{'label': 'PDF', 'file': local_path if pdf_url and local_path else pdf_url, 'url': pdf_url}] if pdf_url else [],
                    'content': li.get_text().strip(),
                    'keywords': ['gebhard', 'böckle', 'arithmetic', 'geometry', 'mathematics']
                }

                publications.append(publication)
                print(f"✅ Extracted publication: {title[:50]}... ({year})")

            except Exception as e:
                print(f"⚠️ Error parsing publication: {e}")
                continue

    except Exception as e:
        print(f"⚠️ Error extracting from member page content: {e}")

    return publications

def create_comprehensive_publications():
    """Create comprehensive publication entries based on known works."""
    publications = []

    # Add comprehensive publication entries for the group
    comprehensive_entries = [
        {
            'title': 'Complete Publications List - AG Computational Arithmetic Geometry',
            'authors': 'AG Computational Arithmetic Geometry',
            'year': '2024',
            'type': 'Publications',
            'abstract': 'Complete list of all publications from the AG Computational Arithmetic Geometry research group at Heidelberg University',
            'links': [],
            'pdfs': [],
            'content': 'Comprehensive collection of publications from 1998 to present',
            'keywords': ['publications', 'research group', 'comprehensive list']
        },
        {
            'title': 'Software Packages and Tools',
            'authors': 'AG Computational Arithmetic Geometry',
            'year': '2024',
            'type': 'Software',
            'abstract': 'Collection of software packages and computational tools developed by the research group',
            'links': [{'label': 'GitHub - Buildings', 'url': 'https://github.com/lhofmann/buildings'}, {'label': 'GitHub - Hecke Operator', 'url': 'https://github.com/b-cakir/hecke-operator'}],
            'pdfs': [{'label': 'PDF', 'file': '/assets/uploads/qaquotgraphs-magma-package.pdf', 'url': '/assets/uploads/qaquotgraphs-magma-package.pdf'}],
            'content': 'Magma packages and computational tools for arithmetic geometry',
            'keywords': ['software', 'magma', 'computational tools']
        }
    ]

    publications.extend(comprehensive_entries)
    return publications

def update_publications_page(publication_count: int):
    """Update the publications page with a note about the new content."""
    publications_page = ROOT_DIR / "_pages/publications.md"

    if publications_page.exists():
        content = publications_page.read_text(encoding='utf-8')

        # Add a note about the updated content
        if "<div class=\"publications-page\">" in content:
            # Find the software packages section and update it
            old_note = "<!-- All software packages from Heidelberg website are included and up to date -->"
            new_note = f"<!-- All {publication_count} publications from Heidelberg website are included and up to date -->"

            content = content.replace(old_note, new_note)

            # Update the timestamp
            import datetime
            timestamp = datetime.datetime.now().isoformat()
            old_timestamp = "<!-- Last updated: 2025-08-04T10:26:31.561Z -->"
            new_timestamp = f"<!-- Last updated: {timestamp} -->"

            content = content.replace(old_timestamp, new_timestamp)

            # Write back the updated content
            publications_page.write_text(content, encoding='utf-8')
            print("✅ Updated publications page with new content information")

def main():
    """Main entry point."""
    try:
        publication_count = scrape_all_publications()

        print("\n🎉 Publications scraper completed successfully!")
        print(f"📚 Total publications processed: {publication_count}")
        print(f"📂 Publication files location: {PUBLICATIONS_DIR}")
        print(f"📥 Downloaded assets location: {DOWNLOAD_DIR}")
        print("\n🔄 The website has been updated with the new publication content.")
        print("📋 Make sure to rebuild your Jekyll site to see the changes.")

    except Exception as e:
        print(f"❌ Error during scraping: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
