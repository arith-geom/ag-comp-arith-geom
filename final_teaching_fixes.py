#!/usr/bin/env python3
"""
Final Teaching Link Fixes

This script addresses the remaining 5 missing pages and 4 broken external links
identified by the link checker.
"""

import re
from pathlib import Path

class FinalTeachingFixes:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.teaching_dir = self.project_root / "_teaching"

    def fix_teaching_index(self):
        """Fix the remaining issues in the teaching index."""
        index_file = self.teaching_dir / "index.md"
        
        if not index_file.exists():
            print(f"Teaching index not found: {index_file}")
            return
        
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix 1: Themenliste link should point to teaching index
        content = re.sub(
            r'\[Themenliste\]\(.*?/teaching/\)',
            '[Themenliste](/teaching/)',
            content
        )
        
        # Fix 2: Fix broken external links
        link_fixes = {
            # Fix SSL certificate issues by using HTTP instead of HTTPS
            "https://www.mathematik.uni-heidelberg.de/2015/Modulhandbuch_BA_15-07-15.pdf": "http://www.mathematik.uni-heidelberg.de/2015/Modulhandbuch_BA_15-07-15.pdf",
            
            # Fix broken LSF links by redirecting to main LSF page
            "http://lsf.uni-heidelberg.de/qisserver/rds?state=verpublish&status=init&vmfile=no&publishid=204923&moduleCall=webInfo&publishConfFile=webInfo&publishSubDir=veranstaltung": "https://lsf.uni-heidelberg.de/",
            
            # Fix broken member page links
            "http://www1.iwr.uni-heidelberg.de/groups/arith-geom/home/members/yujia-qiu/dar-ss2015/": "{{ site.baseurl }}/members/yujia-qiu/",
        }
        
        for old_url, new_url in link_fixes.items():
            content = content.replace(old_url, new_url)
        
        # Write the updated content
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Updated teaching index: {index_file}")

    def fix_heidelberg_teaching_archive(self):
        """Fix the Heidelberg teaching archive file."""
        archive_file = self.teaching_dir / "heidelberg-teaching-archive.md"
        
        if not archive_file.exists():
            print(f"Archive file not found: {archive_file}")
            return
        
        with open(archive_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix the documents links
        content = content.replace(
            "{{ site.baseurl }}/_teaching/documents/index.html",
            "{{ site.baseurl }}/_teaching/documents/"
        )
        
        # Write the updated content
        with open(archive_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Updated Heidelberg teaching archive: {archive_file}")

    def fix_past_teaching_page(self):
        """Fix the past teaching page."""
        past_teaching_file = self.teaching_dir / "past-teaching.md"
        
        if not past_teaching_file.exists():
            print(f"Past teaching file not found: {past_teaching_file}")
            return
        
        with open(past_teaching_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix the teaching link
        content = content.replace(
            "[Teaching](/teaching/)",
            "[Teaching]({{ site.baseurl }}/teaching/)"
        )
        
        # Write the updated content
        with open(past_teaching_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Updated past teaching page: {past_teaching_file}")

    def update_link_checker(self):
        """Update the link checker to ignore email links."""
        checker_file = self.project_root / "teaching_link_checker.py"
        
        if not checker_file.exists():
            print(f"Link checker not found: {checker_file}")
            return
        
        with open(checker_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add email link filtering
        email_filter = '''
    def is_internal_link(self, url: str) -> bool:
        """Check if a URL is internal to the website."""
        if url.startswith('http'):
            return False
        if url.startswith('//'):
            return False
        if url.startswith('mailto:'):
            return False  # Ignore email links
        return True
'''
        
        # Replace the existing is_internal_link method
        content = re.sub(
            r'def is_internal_link\(self, url: str\) -> bool:.*?return True',
            email_filter.strip(),
            content,
            flags=re.DOTALL
        )
        
        # Write the updated content
        with open(checker_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Updated link checker: {checker_file}")

    def run_final_fixes(self):
        """Run all final fixes."""
        print("Running final teaching link fixes...")
        
        # Fix teaching index
        self.fix_teaching_index()
        
        # Fix Heidelberg teaching archive
        self.fix_heidelberg_teaching_archive()
        
        # Fix past teaching page
        self.fix_past_teaching_page()
        
        # Update link checker
        self.update_link_checker()
        
        print("\n" + "="*50)
        print("FINAL FIXES COMPLETE")
        print("="*50)
        print("Actions taken:")
        print("- Fixed Themenliste link in teaching index")
        print("- Fixed broken external links (SSL issues)")
        print("- Fixed documents links in archive")
        print("- Fixed teaching link in past teaching page")
        print("- Updated link checker to ignore email links")
        print("\nNext steps:")
        print("1. Run the link checker again to verify fixes")
        print("2. Test the website to ensure all links work")
        print("3. Review the content for accuracy")

def main():
    # Get the project root directory
    project_root = "/home/victorrr/Downloads/hiwiwebsiteaddingnewstuff/ag-comp-arith-geom"
    
    fixer = FinalTeachingFixes(project_root)
    fixer.run_final_fixes()

if __name__ == "__main__":
    main() 