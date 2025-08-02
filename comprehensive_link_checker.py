#!/usr/bin/env python3
"""
Comprehensive Link Checker and Fixer for Heidelberg Arithmetic Geometry Website

This script performs a thorough check of all links in the teaching section,
verifies PDF files, tests external websites, and provides detailed reporting
with automatic fixes where possible.
"""

import os
import re
import requests
import urllib.parse
from pathlib import Path
from bs4 import BeautifulSoup
import json
from typing import Dict, List, Tuple, Set, Optional
import time
import hashlib
from urllib.parse import urlparse
import mimetypes

class ComprehensiveLinkChecker:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.teaching_dir = self.project_root / "_teaching"
        self.assets_dir = self.project_root / "assets"
        self.members_dir = self.project_root / "_members"
        self.pages_dir = self.project_root / "_pages"
        self.uploads_dir = self.assets_dir / "uploads"
        
        # Track results
        self.broken_links = []
        self.missing_pdfs = []
        self.broken_external_links = []
        self.working_links = []
        self.verified_pdfs = []
        self.fixes_applied = []
        
        # Known external domains that should work
        self.known_external_domains = {
            'typo.iwr.uni-heidelberg.de',
            'www.iwr.uni-heidelberg.de',
            'www1.iwr.uni-heidelberg.de',
            'lsf.uni-heidelberg.de',
            'www.mathematik.uni-heidelberg.de',
            'www.ub.uni-heidelberg.de',
            'elearning2.uni-heidelberg.de',
            'www.rzuser.uni-heidelberg.de',
            'jmcrv.org',
            'crc326gaus.de'
        }
        
        # Session for HTTP requests
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; ComprehensiveLinkChecker/1.0)'
        })
        
        # Timeout for requests
        self.timeout = 10

    def extract_all_links(self, content: str, file_path: Path) -> List[Dict]:
        """Extract all links from content (markdown and HTML)."""
        links = []
        
        # Pattern for markdown links: [text](url)
        md_link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        for match in re.finditer(md_link_pattern, content):
            text = match.group(1)
            url = match.group(2)
            links.append({
                'text': text.strip(),
                'url': url.strip(),
                'type': 'markdown',
                'line': content[:match.start()].count('\n') + 1,
                'file': file_path
            })
        
        # Pattern for HTML links: <a href="url">text</a>
        html_link_pattern = r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>([^<]+)</a>'
        for match in re.finditer(html_link_pattern, content):
            url = match.group(1)
            text = match.group(2)
            links.append({
                'text': text.strip(),
                'url': url.strip(),
                'type': 'html',
                'line': content[:match.start()].count('\n') + 1,
                'file': file_path
            })
        
        return links

    def is_internal_link(self, url: str) -> bool:
        """Check if a URL is internal to the website."""
        if url.startswith('http'):
            return False
        if url.startswith('//'):
            return False
        if url.startswith('mailto:'):
            return True  # Treat email links as internal (they don't need external checking)
        return True

    def is_pdf_link(self, url: str) -> bool:
        """Check if a URL points to a PDF file."""
        return url.lower().endswith('.pdf') or '/assets/uploads/' in url

    def resolve_internal_path(self, url: str, base_file: Path) -> Path:
        """Resolve an internal URL to a file path."""
        # Remove site.baseurl if present
        url = url.replace('{{ site.baseurl }}', '')
        
        # Handle relative paths
        if url.startswith('/'):
            # Handle Jekyll collection URLs
            if url.startswith('/teaching/'):
                path = self.teaching_dir / url[10:]  # Remove '/teaching/'
                # Add .md extension if it's a directory or doesn't have an extension
                if path.is_dir() or not path.suffix:
                    return path / "index.md" if path.is_dir() else path.with_suffix('.md')
                return path
            elif url.startswith('/members/'):
                path = self.members_dir / url[9:]  # Remove '/members/'
                # Add .md extension if it doesn't have an extension
                if not path.suffix:
                    return path.with_suffix('.md')
                return path
            elif url.startswith('/assets/'):
                return self.assets_dir / url[8:]  # Remove '/assets/'
            else:
                path = self.project_root / url[1:]  # Remove leading '/'
                # Add .md extension if it doesn't have an extension
                if not path.suffix:
                    return path.with_suffix('.md')
                return path
        else:
            # Relative to current file
            path = base_file.parent / url
            # Add .md extension if it doesn't have an extension
            if not path.suffix:
                return path.with_suffix('.md')
            return path

    def check_file_exists(self, file_path: Path) -> bool:
        """Check if a file exists and is accessible."""
        try:
            return file_path.exists() and file_path.is_file()
        except Exception:
            return False

    def check_pdf_file(self, file_path: Path) -> Tuple[bool, str]:
        """Check if a PDF file exists and is valid."""
        if not self.check_file_exists(file_path):
            return False, "File does not exist"
        
        try:
            # Check file size
            if file_path.stat().st_size == 0:
                return False, "File is empty"
            
            # Check if it's actually a PDF by reading first few bytes
            with open(file_path, 'rb') as f:
                header = f.read(4)
                if header != b'%PDF':
                    return False, "Not a valid PDF file"
            
            return True, "Valid PDF file"
        except Exception as e:
            return False, f"Error reading file: {str(e)}"

    def check_external_url(self, url: str) -> Tuple[bool, str]:
        """Check if an external URL is accessible."""
        try:
            response = self.session.get(url, timeout=self.timeout, allow_redirects=True)
            if response.status_code == 200:
                return True, f"Status: {response.status_code}"
            else:
                return False, f"Status: {response.status_code}"
        except requests.exceptions.Timeout:
            return False, "Timeout"
        except requests.exceptions.ConnectionError:
            return False, "Connection error"
        except requests.exceptions.RequestException as e:
            return False, f"Request error: {str(e)}"

    def find_pdf_in_uploads(self, filename: str) -> Optional[Path]:
        """Find a PDF file in the uploads directory."""
        if not self.uploads_dir.exists():
            return None
        
        # Look for exact match
        pdf_path = self.uploads_dir / filename
        if pdf_path.exists():
            return pdf_path
        
        # Look for case-insensitive match
        for file in self.uploads_dir.glob('*'):
            if file.name.lower() == filename.lower():
                return file
        
        return None

    def scrape_pdf_from_old_website(self, url: str, filename: str) -> bool:
        """Attempt to scrape a PDF from the old website."""
        try:
            print(f"  Attempting to scrape PDF from: {url}")
            response = self.session.get(url, timeout=self.timeout)
            if response.status_code == 200:
                # Check if response is actually a PDF
                content_type = response.headers.get('content-type', '')
                if 'pdf' in content_type.lower() or response.content.startswith(b'%PDF'):
                    # Save the PDF
                    pdf_path = self.uploads_dir / filename
                    with open(pdf_path, 'wb') as f:
                        f.write(response.content)
                    print(f"  Successfully scraped PDF: {filename}")
                    return True
                else:
                    print(f"  Response is not a PDF (content-type: {content_type})")
            else:
                print(f"  Failed to fetch PDF (status: {response.status_code})")
        except Exception as e:
            print(f"  Error scraping PDF: {str(e)}")
        
        return False

    def check_teaching_file(self, file_path: Path) -> List[Dict]:
        """Check all links in a teaching file."""
        print(f"Checking {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return []
        
        links = self.extract_all_links(content, file_path)
        results = []
        
        for link in links:
            url = link['url']
            
            # Handle email links separately
            if url.startswith('mailto:'):
                self.working_links.append(link)
                continue
            
            if self.is_internal_link(url):
                # Check internal link
                resolved_path = self.resolve_internal_path(url, file_path)
                
                if self.is_pdf_link(url):
                    # Check PDF file
                    is_valid, message = self.check_pdf_file(resolved_path)
                    if is_valid:
                        self.verified_pdfs.append({
                            'url': url,
                            'file': resolved_path,
                            'source': file_path
                        })
                    else:
                        self.missing_pdfs.append({
                            'url': url,
                            'file': resolved_path,
                            'source': file_path,
                            'error': message
                        })
                else:
                    # Check regular file
                    if self.check_file_exists(resolved_path):
                        self.working_links.append(link)
                    else:
                        self.broken_links.append({
                            **link,
                            'resolved_path': resolved_path,
                            'error': 'File not found'
                        })
            else:
                # Check external link
                is_working, message = self.check_external_url(url)
                if is_working:
                    self.working_links.append(link)
                else:
                    self.broken_external_links.append({
                        **link,
                        'error': message
                    })
        
        return results

    def scan_all_teaching_files(self):
        """Scan all teaching-related files for links."""
        print("Starting comprehensive link scan...")
        
        # Scan teaching files
        for file_path in self.teaching_dir.rglob('*.md'):
            self.check_teaching_file(file_path)
        
        # Scan member files for teaching-related links
        for file_path in self.members_dir.rglob('*.md'):
            self.check_teaching_file(file_path)
        
        # Scan pages for teaching-related links
        for file_path in self.pages_dir.rglob('*.md'):
            if 'teaching' in file_path.name.lower():
                self.check_teaching_file(file_path)

    def fix_missing_pdfs(self):
        """Attempt to fix missing PDF files."""
        print("\nAttempting to fix missing PDFs...")
        
        # Create uploads directory if it doesn't exist
        self.uploads_dir.mkdir(parents=True, exist_ok=True)
        
        # Map of known PDF URLs to their filenames
        pdf_mappings = {
            'comm_alg_announcement.pdf': 'https://www.iwr.uni-heidelberg.de/groups/arith-geom/fileadmin/groups/arithgeo/comm_alg_announcement.pdf',
            'GAUS-AG-WiSe2024-25-IKM-2024-12-11.pdf': 'https://www.iwr.uni-heidelberg.de/groups/arith-geom/fileadmin/groups/arithgeo/GAUS-AG-WiSe2024-25-IKM-2024-12-11.pdf',
            'Seminar.pdf': 'https://www.iwr.uni-heidelberg.de/groups/arith-geom/fileadmin/groups/arithgeo/Seminar.pdf',
            'RMCprogram_01.pdf': 'https://www.iwr.uni-heidelberg.de/groups/arith-geom/fileadmin/groups/arithgeo/RMCprogram_01.pdf',
            'VectorialDrinfeldModForms.pdf': 'https://crc326gaus.de/wp-content/uploads/2023/03/VectorialDrinfeldModForms.pdf',
            'program_comp_nt.pdf': 'https://www.iwr.uni-heidelberg.de/groups/arith-geom/fileadmin/groups/arithgeo/templates/data/Vorlesungen/program_comp_nt.pdf',
            'Programm_la-courbe_SoSe19.pdf': 'https://www.iwr.uni-heidelberg.de/groups/arith-geom/fileadmin/groups/arithgeo/templates/data/Hauptseminare/Programm_la-courbe_SoSe19.pdf',
            'Programm_GL2_WS1819.pdf': 'https://www.iwr.uni-heidelberg.de/groups/arith-geom/fileadmin/groups/arithgeo/templates/data/Judith_Ludwig/Programm_GL2_WS1819.pdf',
            'WS1819_lokale_G-shtukas.pdf': 'https://www.iwr.uni-heidelberg.de/groups/arith-geom/fileadmin/groups/arithgeo/templates/data/Hauptseminare/WS1819_lokale_G-shtukas.pdf',
            'Ankuendigung-Modularity.pdf': 'https://www.iwr.uni-heidelberg.de/groups/arith-geom/fileadmin/groups/arithgeo/templates/data/Seminare/Ankuendigung-Modularity.pdf',
            'Bruhat-Tits.pdf': 'https://www.iwr.uni-heidelberg.de/groups/arith-geom/fileadmin/groups/arithgeo/templates/data/Vorlesungen/Bruhat-Tits.pdf',
            'DarstellungenUndInvarianten_II_SS2015.pdf': 'https://www.iwr.uni-heidelberg.de/groups/arith-geom/fileadmin/groups/arithgeo/templates/data/Vorlesungen/DarstellungenUndInvarianten_II_SS2015.pdf',
            'Lenny_Taelman_s_body_of_work_on_Drinfeld_modules.pdf': 'https://www.iwr.uni-heidelberg.de/groups/arith-geom/fileadmin/groups/arithgeo/templates/data/Vorlesungen/Lenny_Taelman_s_body_of_work_on_Drinfeld_modules.pdf',
            'Modulbeschreibung-AutomorpheFormen.pdf': 'https://www.iwr.uni-heidelberg.de/groups/arith-geom/fileadmin/groups/arithgeo/templates/data/Vorlesungen/Modulbeschreibung-AutomorpheFormen.pdf',
            'DarstellungenUndInvarianten_WS201415.pdf': 'https://www.iwr.uni-heidelberg.de/groups/arith-geom/fileadmin/groups/arithgeo/templates/data/Vorlesungen/DarstellungenUndInvarianten_WS201415.pdf',
            'WS201415_RecentBSD.pdf': 'https://www.iwr.uni-heidelberg.de/groups/arith-geom/fileadmin/groups/arithgeo/templates/data/Hauptseminare/WS201415_RecentBSD.pdf',
            'AffineAlgebraischeGruppen_WS2012-13_Programm.pdf': 'https://www.iwr.uni-heidelberg.de/groups/arith-geom/fileadmin/groups/arithgeo/templates/data/Seminare/AffineAlgebraischeGruppen_WS2012-13_Programm.pdf',
            'WS1213_TranscendencePosChar.pdf': 'https://www.iwr.uni-heidelberg.de/groups/arith-geom/fileadmin/groups/arithgeo/templates/data/Hauptseminare/WS1213_TranscendencePosChar.pdf',
            'AutomorphicFormsAndRepresentationsForGL2_CentelegheCervinoChekaru.pdf': 'https://www.iwr.uni-heidelberg.de/groups/arith-geom/fileadmin/groups/arithgeo/templates/data/Hauptseminare/AutomorphicFormsAndRepresentationsForGL2_CentelegheCervinoChekaru.pdf',
            'BorcherdsProducts_SeminarProgram_WS2011-12_G3.pdf': 'https://www.iwr.uni-heidelberg.de/groups/arith-geom/fileadmin/groups/arithgeo/templates/data/Hauptseminare/BorcherdsProducts_SeminarProgram_WS2011-12_G3.pdf',
            'Seminarprogramm_IkedaLift_WS2011-12_BouganisCervinoKasten.pdf': 'https://www.iwr.uni-heidelberg.de/groups/arith-geom/fileadmin/groups/arithgeo/templates/data/Seminare/Seminarprogramm_IkedaLift_WS2011-12_BouganisCervinoKasten.pdf',
            'qF_Programm_SS2011.pdf': 'https://www.iwr.uni-heidelberg.de/groups/arith-geom/fileadmin/groups/arithgeo/templates/data/Seminare/qF_Programm_SS2011.pdf'
        }
        
        for missing_pdf in self.missing_pdfs:
            filename = missing_pdf['file'].name
            if filename in pdf_mappings:
                old_url = pdf_mappings[filename]
                if self.scrape_pdf_from_old_website(old_url, filename):
                    self.fixes_applied.append({
                        'type': 'pdf_scraped',
                        'filename': filename,
                        'source_url': old_url,
                        'target_path': self.uploads_dir / filename
                    })

    def generate_comprehensive_report(self) -> str:
        """Generate a comprehensive report of all findings."""
        report = []
        report.append("# Comprehensive Link Check Report")
        report.append(f"**Generated:** {time.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Summary
        report.append("## Summary")
        report.append(f"- **Working Links:** {len(self.working_links)}")
        report.append(f"- **Broken Internal Links:** {len(self.broken_links)}")
        report.append(f"- **Broken External Links:** {len(self.broken_external_links)}")
        report.append(f"- **Missing PDFs:** {len(self.missing_pdfs)}")
        report.append(f"- **Verified PDFs:** {len(self.verified_pdfs)}")
        report.append(f"- **Fixes Applied:** {len(self.fixes_applied)}")
        report.append("")
        
        # Broken internal links
        if self.broken_links:
            report.append("## Broken Internal Links")
            for link in self.broken_links:
                report.append(f"- **{link['text']}** in {link['file'].name}:{link['line']}")
                report.append(f"  - URL: `{link['url']}`")
                report.append(f"  - Resolved: `{link['resolved_path']}`")
                report.append(f"  - Error: {link['error']}")
                report.append("")
        
        # Missing PDFs
        if self.missing_pdfs:
            report.append("## Missing PDF Files")
            for pdf in self.missing_pdfs:
                report.append(f"- **{pdf['file'].name}** referenced in {pdf['source'].name}:{pdf['line']}")
                report.append(f"  - URL: `{pdf['url']}`")
                report.append(f"  - Error: {pdf['error']}")
                report.append("")
        
        # Broken external links
        if self.broken_external_links:
            report.append("## Broken External Links")
            for link in self.broken_external_links:
                report.append(f"- **{link['text']}** in {link['file'].name}:{link['line']}")
                report.append(f"  - URL: `{link['url']}`")
                report.append(f"  - Error: {link['error']}")
                report.append("")
        
        # Verified PDFs
        if self.verified_pdfs:
            report.append("## Verified PDF Files")
            for pdf in self.verified_pdfs:
                report.append(f"- **{pdf['file'].name}** ({pdf['file'].stat().st_size} bytes)")
                report.append(f"  - Referenced in: {pdf['source'].name}")
                report.append("")
        
        # Fixes applied
        if self.fixes_applied:
            report.append("## Fixes Applied")
            for fix in self.fixes_applied:
                report.append(f"- **{fix['type']}**: {fix['filename']}")
                report.append(f"  - Source: {fix['source_url']}")
                report.append(f"  - Target: {fix['target_path']}")
                report.append("")
        
        return "\n".join(report)

    def run_comprehensive_check(self):
        """Run the complete comprehensive link check."""
        print("Starting comprehensive link check...")
        
        # Scan all files
        self.scan_all_teaching_files()
        
        # Attempt to fix missing PDFs
        self.fix_missing_pdfs()
        
        # Generate report
        report = self.generate_comprehensive_report()
        
        # Save report
        report_path = self.project_root / "comprehensive_link_report.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\nReport saved to: {report_path}")
        print("\n" + "="*50)
        print("COMPREHENSIVE SUMMARY:")
        print(f"Working links: {len(self.working_links)}")
        print(f"Broken internal links: {len(self.broken_links)}")
        print(f"Broken external links: {len(self.broken_external_links)}")
        print(f"Missing PDFs: {len(self.missing_pdfs)}")
        print(f"Verified PDFs: {len(self.verified_pdfs)}")
        print(f"Fixes applied: {len(self.fixes_applied)}")
        print("="*50)

def main():
    # Get the project root directory
    project_root = Path(__file__).parent
    print(f"Project root: {project_root}")
    
    # Create and run the checker
    checker = ComprehensiveLinkChecker(str(project_root))
    checker.run_comprehensive_check()

if __name__ == "__main__":
    main() 