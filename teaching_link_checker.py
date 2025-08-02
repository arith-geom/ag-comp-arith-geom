#!/usr/bin/env python3
"""
Teaching Link Checker for Heidelberg Arithmetic Geometry Website

This script checks all links in the teaching section and identifies broken links,
missing pages, and provides suggestions for fixes.
"""

import os
import re
import requests
import urllib.parse
from pathlib import Path
from bs4 import BeautifulSoup
import json
from typing import Dict, List, Tuple, Set
import time

class TeachingLinkChecker:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.teaching_dir = self.project_root / "_teaching"
        self.assets_dir = self.project_root / "assets"
        self.members_dir = self.project_root / "_members"
        self.pages_dir = self.project_root / "_pages"
        
        # Track results
        self.broken_links = []
        self.missing_pages = []
        self.external_links = []
        self.working_links = []
        
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
            'User-Agent': 'Mozilla/5.0 (compatible; TeachingLinkChecker/1.0)'
        })

    def extract_links_from_markdown(self, content: str) -> List[Dict]:
        """Extract all links from markdown content."""
        links = []
        
        # Pattern for markdown links: [text](url)
        md_link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        for match in re.finditer(md_link_pattern, content):
            text = match.group(1)
            url = match.group(2)
            links.append({
                'text': text,
                'url': url,
                'type': 'markdown',
                'line': content[:match.start()].count('\n') + 1
            })
        
        # Pattern for HTML links: <a href="url">text</a>
        html_link_pattern = r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>([^<]+)</a>'
        for match in re.finditer(html_link_pattern, content):
            url = match.group(1)
            text = match.group(2)
            links.append({
                'text': text,
                'url': url,
                'type': 'html',
                'line': content[:match.start()].count('\n') + 1
            })
        
        return links

    def is_internal_link(self, url: str) -> bool:
        """Check if a URL is internal to the website."""
        if url.startswith('http'):
            return False
        if url.startswith('//'):
            return False
        if url.startswith('mailto:'):
            return False  # Ignore email links
        return True

    def resolve_internal_path(self, url: str, base_file: Path) -> Path:
        """Resolve an internal URL to a file path."""
        # Remove site.baseurl if present
        url = url.replace('{{ site.baseurl }}', '')
        
        # Handle relative paths
        if url.startswith('/'):
            # Handle Jekyll collection URLs
            if url.startswith('/teaching/'):
                # Convert /teaching/course-name/ to _teaching/course-name.md
                course_name = url.replace('/teaching/', '').rstrip('/')
                if not course_name:  # Handle /teaching/ -> _teaching/index.md
                    return self.teaching_dir / "index.md"
                elif course_name == 'documents':  # Handle /teaching/documents/ -> _teaching/documents/index.md
                    return self.teaching_dir / "documents" / "index.md"
                return self.teaching_dir / f"{course_name}.md"
            elif url.startswith('/members/'):
                # Convert /members/member-name/ to _members/member-name.md
                member_name = url.replace('/members/', '').rstrip('/')
                return self.members_dir / f"{member_name}.md"
            else:
                return self.project_root / url.lstrip('/')
        elif url.startswith('./'):
            return base_file.parent / url[2:]
        elif url.startswith('../'):
            return base_file.parent / url
        else:
            return base_file.parent / url

    def check_file_exists(self, file_path: Path) -> bool:
        """Check if a file exists and is accessible."""
        if not file_path.exists():
            return False
        
        # Check if it's a directory and has an index file
        if file_path.is_dir():
            index_files = ['index.html', 'index.md', 'index.liquid']
            return any((file_path / f).exists() for f in index_files)
        
        return True

    def check_external_url(self, url: str) -> Tuple[bool, str]:
        """Check if an external URL is accessible."""
        # Skip email links
        if url.startswith('mailto:'):
            return True, "Email link (skipped)"
        
        try:
            response = self.session.head(url, timeout=10, allow_redirects=True)
            return response.status_code < 400, f"HTTP {response.status_code}"
        except requests.exceptions.RequestException as e:
            return False, str(e)

    def check_teaching_page(self, file_path: Path) -> List[Dict]:
        """Check all links in a teaching page."""
        print(f"Checking {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        links = self.extract_links_from_markdown(content)
        results = []
        
        for link in links:
            url = link['url']
            text = link['text']
            
            if self.is_internal_link(url):
                # Check internal link
                resolved_path = self.resolve_internal_path(url, file_path)
                exists = self.check_file_exists(resolved_path)
                
                result = {
                    'file': str(file_path),
                    'line': link['line'],
                    'text': text,
                    'url': url,
                    'type': 'internal',
                    'exists': exists,
                    'resolved_path': str(resolved_path)
                }
                
                if not exists:
                    self.missing_pages.append(result)
                else:
                    self.working_links.append(result)
                    
            else:
                # Check external link
                is_accessible, error_msg = self.check_external_url(url)
                
                result = {
                    'file': str(file_path),
                    'line': link['line'],
                    'text': text,
                    'url': url,
                    'type': 'external',
                    'accessible': is_accessible,
                    'error': error_msg if not is_accessible else None
                }
                
                if not is_accessible:
                    self.broken_links.append(result)
                else:
                    self.external_links.append(result)
            
            results.append(result)
        
        return results

    def scan_all_teaching_files(self):
        """Scan all teaching-related files for links."""
        # Check main teaching index
        teaching_index = self.teaching_dir / "index.md"
        if teaching_index.exists():
            self.check_teaching_page(teaching_index)
        
        # Check individual teaching pages
        for file_path in self.teaching_dir.glob("*.md"):
            if file_path.name != "index.md":
                self.check_teaching_page(file_path)
        
        # Check member pages that might be linked
        if self.members_dir.exists():
            for file_path in self.members_dir.glob("*.md"):
                self.check_teaching_page(file_path)

    def generate_report(self) -> str:
        """Generate a comprehensive report of all findings."""
        report = []
        report.append("# Teaching Link Checker Report")
        report.append(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Summary
        report.append("## Summary")
        report.append(f"- Total working links: {len(self.working_links)}")
        report.append(f"- Total external links: {len(self.external_links)}")
        report.append(f"- Missing pages: {len(self.missing_pages)}")
        report.append(f"- Broken external links: {len(self.broken_links)}")
        report.append("")
        
        # Missing pages
        if self.missing_pages:
            report.append("## Missing Pages")
            report.append("These internal links point to non-existent files:")
            report.append("")
            
            for item in self.missing_pages:
                report.append(f"### {item['text']}")
                report.append(f"- **File:** {item['file']}")
                report.append(f"- **Line:** {item['line']}")
                report.append(f"- **URL:** `{item['url']}`")
                report.append(f"- **Resolved Path:** `{item['resolved_path']}`")
                report.append("")
        
        # Broken external links
        if self.broken_links:
            report.append("## Broken External Links")
            report.append("These external links are not accessible:")
            report.append("")
            
            for item in self.broken_links:
                report.append(f"### {item['text']}")
                report.append(f"- **File:** {item['file']}")
                report.append(f"- **Line:** {item['line']}")
                report.append(f"- **URL:** `{item['url']}`")
                report.append(f"- **Error:** {item['error']}")
                report.append("")
        
        return "\n".join(report)

    def suggest_fixes(self) -> str:
        """Generate suggestions for fixing broken links."""
        suggestions = []
        suggestions.append("# Suggested Fixes")
        suggestions.append("")
        
        # Group missing pages by type
        missing_by_type = {}
        for item in self.missing_pages:
            url = item['url']
            if 'teaching/' in url:
                missing_by_type.setdefault('teaching_pages', []).append(item)
            elif 'members/' in url:
                missing_by_type.setdefault('member_pages', []).append(item)
            elif 'assets/' in url:
                missing_by_type.setdefault('assets', []).append(item)
            else:
                missing_by_type.setdefault('other', []).append(item)
        
        # Teaching pages
        if 'teaching_pages' in missing_by_type:
            suggestions.append("## Missing Teaching Pages")
            suggestions.append("Create these teaching page files:")
            suggestions.append("")
            
            for item in missing_by_type['teaching_pages']:
                url = item['url']
                # Extract page name from URL
                page_name = url.split('/')[-1]
                if not page_name.endswith('.md'):
                    page_name += '.md'
                
                suggestions.append(f"### {item['text']}")
                suggestions.append(f"- **Create file:** `_teaching/{page_name}`")
                suggestions.append(f"- **Template:** Use existing teaching page as template")
                suggestions.append("")
        
        # Member pages
        if 'member_pages' in missing_by_type:
            suggestions.append("## Missing Member Pages")
            suggestions.append("Create these member page files:")
            suggestions.append("")
            
            for item in missing_by_type['member_pages']:
                url = item['url']
                member_name = url.split('/')[-1]
                if not member_name.endswith('.md'):
                    member_name += '.md'
                
                suggestions.append(f"### {item['text']}")
                suggestions.append(f"- **Create file:** `_members/{member_name}`")
                suggestions.append(f"- **Template:** Use existing member page as template")
                suggestions.append("")
        
        # Assets
        if 'assets' in missing_by_type:
            suggestions.append("## Missing Assets")
            suggestions.append("These files need to be added to the assets directory:")
            suggestions.append("")
            
            for item in missing_by_type['assets']:
                suggestions.append(f"- **File:** {item['url']}")
                suggestions.append(f"- **Location:** {item['resolved_path']}")
                suggestions.append("")
        
        return "\n".join(suggestions)

    def run_full_check(self):
        """Run the complete link checking process."""
        print("Starting teaching link check...")
        self.scan_all_teaching_files()
        
        # Generate reports
        report = self.generate_report()
        suggestions = self.suggest_fixes()
        
        # Save reports
        with open(self.project_root / "teaching_link_report.md", 'w', encoding='utf-8') as f:
            f.write(report)
        
        with open(self.project_root / "teaching_fix_suggestions.md", 'w', encoding='utf-8') as f:
            f.write(suggestions)
        
        print(f"Report saved to: {self.project_root / 'teaching_link_report.md'}")
        print(f"Suggestions saved to: {self.project_root / 'teaching_fix_suggestions.md'}")
        
        return report, suggestions

def main():
    # Get the project root directory
    project_root = "/home/victorrr/Downloads/hiwiwebsiteaddingnewstuff/ag-comp-arith-geom"
    
    checker = TeachingLinkChecker(project_root)
    report, suggestions = checker.run_full_check()
    
    print("\n" + "="*50)
    print("QUICK SUMMARY:")
    print(f"Missing pages: {len(checker.missing_pages)}")
    print(f"Broken external links: {len(checker.broken_links)}")
    print(f"Working links: {len(checker.working_links)}")
    print("="*50)

if __name__ == "__main__":
    main() 