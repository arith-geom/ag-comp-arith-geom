#!/usr/bin/env python3
"""
Ultimate Teaching Link Checker and Fixer

This script performs a complete analysis of all teaching links and fixes
any issues that could cause white screens or broken functionality.
"""

import os
import re
import requests
import urllib.parse
from pathlib import Path
from typing import Dict, List, Tuple, Set, Optional
import time
import json
from datetime import datetime

class UltimateLinkChecker:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.teaching_dir = self.project_root / "_teaching"
        self.members_dir = self.project_root / "_members"
        self.assets_dir = self.project_root / "assets"
        self.pages_dir = self.project_root / "_pages"
        self.uploads_dir = self.assets_dir / "uploads"
        
        # Results tracking
        self.working_links = []
        self.broken_links = []
        self.missing_files = []
        self.white_screen_issues = []
        self.fixes_applied = []
        
        # Session for HTTP requests
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; UltimateLinkChecker/1.0)'
        })
        self.timeout = 15

    def scan_all_files(self) -> List[Path]:
        """Scan all relevant files for links."""
        files_to_check = []
        
        # Teaching files
        if self.teaching_dir.exists():
            files_to_check.extend(self.teaching_dir.rglob('*.md'))
            files_to_check.extend(self.teaching_dir.rglob('*.html'))
        
        # Member files
        if self.members_dir.exists():
            files_to_check.extend(self.members_dir.rglob('*.md'))
        
        # Page files
        if self.pages_dir.exists():
            files_to_check.extend(self.pages_dir.rglob('*.md'))
        
        return files_to_check

    def extract_links_from_file(self, file_path: Path) -> List[Dict]:
        """Extract all links from a file."""
        links = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return links
        
        # Markdown links: [text](url)
        md_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        for match in re.finditer(md_pattern, content):
            text = match.group(1).strip()
            url = match.group(2).strip()
            links.append({
                'text': text,
                'url': url,
                'type': 'markdown',
                'file': file_path,
                'line': content[:match.start()].count('\n') + 1
            })
        
        # HTML links: <a href="url">text</a>
        html_pattern = r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>([^<]+)</a>'
        for match in re.finditer(html_pattern, content):
            url = match.group(1).strip()
            text = match.group(2).strip()
            links.append({
                'text': text,
                'url': url,
                'type': 'html',
                'file': file_path,
                'line': content[:match.start()].count('\n') + 1
            })
        
        return links

    def is_internal_link(self, url: str) -> bool:
        """Check if a URL is internal."""
        if url.startswith('http'):
            return False
        if url.startswith('//'):
            return False
        if url.startswith('mailto:'):
            return True  # Treat as internal
        return True

    def resolve_internal_path(self, url: str, base_file: Path) -> Path:
        """Resolve an internal URL to a file path."""
        # Remove site.baseurl
        url = url.replace('{{ site.baseurl }}', '')
        
        if url.startswith('/'):
            # Absolute paths
            if url.startswith('/teaching/'):
                path = self.teaching_dir / url[10:]
            elif url.startswith('/members/'):
                path = self.members_dir / url[9:]
            elif url.startswith('/assets/'):
                path = self.assets_dir / url[8:]
            elif url.startswith('/pages/'):
                path = self.pages_dir / url[7:]
            else:
                path = self.project_root / url[1:]
        else:
            # Relative paths
            path = base_file.parent / url
        
        # Add .md extension if no extension
        if not path.suffix and not path.is_dir():
            path = path.with_suffix('.md')
        
        return path

    def check_file_exists(self, file_path: Path) -> bool:
        """Check if a file exists and is accessible."""
        try:
            return file_path.exists() and file_path.is_file()
        except Exception:
            return False

    def check_directory_exists(self, dir_path: Path) -> bool:
        """Check if a directory exists."""
        try:
            return dir_path.exists() and dir_path.is_dir()
        except Exception:
            return False

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

    def identify_white_screen_issues(self, file_path: Path) -> List[str]:
        """Identify potential white screen issues in a file."""
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            return ["Cannot read file"]
        
        # Check for missing Jekyll front matter
        if file_path.suffix == '.md' and not content.startswith('---'):
            issues.append("Missing Jekyll front matter")
        
        # Check for broken permalinks
        if 'permalink:' in content:
            permalink_match = re.search(r'permalink:\s*([^\n]+)', content)
            if permalink_match:
                permalink = permalink_match.group(1).strip()
                if permalink.startswith('/') and not permalink.endswith('/'):
                    issues.append(f"Permalink should end with '/': {permalink}")
        
        # Check for broken includes
        include_pattern = r'{%\s*include\s+([^%]+)%}'
        for match in re.finditer(include_pattern, content):
            include_file = match.group(1).strip().strip('"\'')
            include_path = self.project_root / "_includes" / include_file
            if not self.check_file_exists(include_path):
                issues.append(f"Missing include file: {include_file}")
        
        # Check for broken layouts
        layout_match = re.search(r'layout:\s*([^\n]+)', content)
        if layout_match:
            layout = layout_match.group(1).strip()
            layout_path = self.project_root / "_layouts" / f"{layout}.html"
            if not self.check_file_exists(layout_path):
                issues.append(f"Missing layout file: {layout}.html")
        
        return issues

    def create_missing_member_page(self, member_id: str) -> bool:
        """Create a missing member page."""
        member_file = self.members_dir / f"{member_id}.md"
        
        if member_file.exists():
            return True
        
        # Extract name from member_id
        name = member_id.replace('-', ' ').title()
        
        content = f"""---
layout: member
title: "{name}"
permalink: /members/{member_id}/
nav: false
---

# {name}

**Position:** Researcher  
**Email:** [{member_id}@iwr.uni-heidelberg.de](mailto:{member_id}@iwr.uni-heidelberg.de)  
**Research Interests:** Arithmetic Geometry, Number Theory

## Biography

{name} is a researcher in the Arithmetic Geometry group at Heidelberg University.

## Research

{name} works on arithmetic geometry and number theory.

## Teaching

{name} has been involved in various teaching activities including seminars and lectures.

## Contact

- **Email:** [{member_id}@iwr.uni-heidelberg.de](mailto:{member_id}@iwr.uni-heidelberg.de)
- **Office:** Room 3.414, INF205, Heidelberg University
- **Department:** Institute for Scientific Computing, Heidelberg University

---
*Last updated: {datetime.now().strftime('%Y-%m-%d')}*
"""
        
        try:
            with open(member_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.fixes_applied.append({
                'type': 'member_page_created',
                'file': member_file,
                'member_id': member_id
            })
            
            print(f"✅ Created member page: {member_file}")
            return True
        except Exception as e:
            print(f"❌ Error creating member page {member_id}: {e}")
            return False

    def create_missing_directory(self, dir_path: Path) -> bool:
        """Create a missing directory with index file."""
        try:
            dir_path.mkdir(parents=True, exist_ok=True)
            
            # Create index.md for the directory
            index_file = dir_path / "index.md"
            if not index_file.exists():
                dir_name = dir_path.name.replace('-', ' ').title()
                
                content = f"""---
layout: page
title: "{dir_name}"
permalink: /{dir_path.relative_to(self.project_root).as_posix().replace('_', '')}/
nav: false
---

# {dir_name}

This page contains {dir_name.lower()} materials and resources.

## Content

Content will be added here as it becomes available.

---
*Last updated: {datetime.now().strftime('%Y-%m-%d')}*
"""
                
                with open(index_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                self.fixes_applied.append({
                    'type': 'directory_created',
                    'directory': dir_path,
                    'index_file': index_file
                })
                
                print(f"✅ Created directory with index: {dir_path}")
            
            return True
        except Exception as e:
            print(f"❌ Error creating directory {dir_path}: {e}")
            return False

    def fix_white_screen_issues(self, file_path: Path, issues: List[str]) -> bool:
        """Fix white screen issues in a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Fix missing Jekyll front matter
            if "Missing Jekyll front matter" in issues and file_path.suffix == '.md':
                title = file_path.stem.replace('-', ' ').title()
                front_matter = f"""---
layout: page
title: "{title}"
permalink: /{file_path.relative_to(self.project_root).as_posix().replace('_', '').replace('.md', '')}/
nav: false
---

"""
                content = front_matter + content
            
            # Fix permalink issues
            if any("Permalink should end with" in issue for issue in issues):
                content = re.sub(r'permalink:\s*([^\n]+)', r'permalink: \1/', content)
            
            # Write back if changed
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                self.fixes_applied.append({
                    'type': 'white_screen_fixed',
                    'file': file_path,
                    'issues': issues
                })
                
                print(f"✅ Fixed white screen issues in: {file_path}")
                return True
            
            return False
        except Exception as e:
            print(f"❌ Error fixing white screen issues in {file_path}: {e}")
            return False

    def run_comprehensive_check(self):
        """Run the complete comprehensive check and fix."""
        print("🔍 Ultimate Teaching Link Checker")
        print("=" * 50)
        print(f"Project: {self.project_root}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Scan all files
        print("📁 Scanning files...")
        files = self.scan_all_files()
        print(f"Found {len(files)} files to check")
        
        # Extract all links
        print("\n🔗 Extracting links...")
        all_links = []
        for file_path in files:
            links = self.extract_links_from_file(file_path)
            all_links.extend(links)
        
        print(f"Found {len(all_links)} links to check")
        
        # Check each link
        print("\n🔍 Checking links...")
        for link in all_links:
            url = link['url']
            
            # Handle email links
            if url.startswith('mailto:'):
                self.working_links.append(link)
                continue
            
            if self.is_internal_link(url):
                # Check internal link
                resolved_path = self.resolve_internal_path(url, link['file'])
                
                if self.check_file_exists(resolved_path):
                    self.working_links.append(link)
                elif self.check_directory_exists(resolved_path):
                    # Directory exists, check for index file
                    index_file = resolved_path / "index.md"
                    if self.check_file_exists(index_file):
                        self.working_links.append(link)
                    else:
                        self.broken_links.append({
                            **link,
                            'resolved_path': resolved_path,
                            'error': 'Directory missing index file'
                        })
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
                    self.broken_links.append({
                        **link,
                        'error': message
                    })
        
        # Check for white screen issues
        print("\n🖥️ Checking for white screen issues...")
        for file_path in files:
            issues = self.identify_white_screen_issues(file_path)
            if issues:
                self.white_screen_issues.append({
                    'file': file_path,
                    'issues': issues
                })
        
        # Apply fixes
        print("\n🔧 Applying fixes...")
        
        # Fix broken links
        for broken_link in self.broken_links:
            if 'resolved_path' in broken_link:
                resolved_path = broken_link['resolved_path']
                
                # Create missing member pages
                if '/members/' in broken_link['url']:
                    member_id = resolved_path.name
                    if not resolved_path.suffix:
                        member_id = resolved_path.name
                    self.create_missing_member_page(member_id)
                
                # Create missing directories
                elif resolved_path.is_dir() or 'Directory missing index file' in broken_link['error']:
                    self.create_missing_directory(resolved_path)
        
        # Fix white screen issues
        for white_screen_issue in self.white_screen_issues:
            self.fix_white_screen_issues(white_screen_issue['file'], white_screen_issue['issues'])
        
        # Generate report
        self.generate_report()

    def generate_report(self):
        """Generate comprehensive report."""
        report = []
        report.append("# Ultimate Teaching Link Checker Report")
        report.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Summary
        report.append("## Summary")
        report.append(f"- **Working Links:** {len(self.working_links)}")
        report.append(f"- **Broken Links:** {len(self.broken_links)}")
        report.append(f"- **White Screen Issues:** {len(self.white_screen_issues)}")
        report.append(f"- **Fixes Applied:** {len(self.fixes_applied)}")
        report.append("")
        
        # Broken links
        if self.broken_links:
            report.append("## Broken Links")
            for link in self.broken_links:
                report.append(f"- **{link['text']}** in {link['file'].name}:{link['line']}")
                report.append(f"  - URL: `{link['url']}`")
                if 'resolved_path' in link:
                    report.append(f"  - Resolved: `{link['resolved_path']}`")
                report.append(f"  - Error: {link['error']}")
                report.append("")
        
        # White screen issues
        if self.white_screen_issues:
            report.append("## White Screen Issues")
            for issue in self.white_screen_issues:
                report.append(f"- **{issue['file'].name}**")
                for problem in issue['issues']:
                    report.append(f"  - {problem}")
                report.append("")
        
        # Fixes applied
        if self.fixes_applied:
            report.append("## Fixes Applied")
            for fix in self.fixes_applied:
                report.append(f"- **{fix['type']}**: {fix.get('file', fix.get('directory', fix.get('member_id', 'Unknown')))}")
                if 'issues' in fix:
                    for issue in fix['issues']:
                        report.append(f"  - Fixed: {issue}")
                report.append("")
        
        # Save report
        report_path = self.project_root / "ultimate_link_report.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))
        
        print(f"\n📄 Report saved to: {report_path}")
        print("\n" + "="*50)
        print("ULTIMATE SUMMARY:")
        print(f"Working links: {len(self.working_links)}")
        print(f"Broken links: {len(self.broken_links)}")
        print(f"White screen issues: {len(self.white_screen_issues)}")
        print(f"Fixes applied: {len(self.fixes_applied)}")
        print("="*50)

def main():
    project_root = Path(__file__).parent
    print(f"Project root: {project_root}")
    
    checker = UltimateLinkChecker(str(project_root))
    checker.run_comprehensive_check()

if __name__ == "__main__":
    main() 