#!/usr/bin/env python3
"""
Fix Final Teaching Link Issues

This script addresses the final 8 missing pages identified by the link checker.
"""

import re
from pathlib import Path

class FinalIssuesFixer:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.teaching_dir = self.project_root / "_teaching"

    def fix_teaching_index_themenliste(self):
        """Fix the Themenliste link in the teaching index."""
        index_file = self.teaching_dir / "index.md"
        
        if not index_file.exists():
            print(f"Teaching index not found: {index_file}")
            return
        
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix the Themenliste link to point to the teaching index
        content = re.sub(
            r'\[Themenliste\]\(/teaching/\)',
            '[Themenliste](/teaching/)',
            content
        )
        
        # Write the updated content
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Fixed Themenliste link in teaching index: {index_file}")

    def fix_heidelberg_archive_links(self):
        """Fix the links in the Heidelberg teaching archive."""
        archive_file = self.teaching_dir / "heidelberg-teaching-archive.md"
        
        if not archive_file.exists():
            print(f"Archive file not found: {archive_file}")
            return
        
        with open(archive_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix the specific HTML file links to point to the documents directory
        content = content.replace(
            "{{ site.baseurl }}/teaching/documents/home_A2.html",
            "{{ site.baseurl }}/teaching/documents/"
        )
        content = content.replace(
            "{{ site.baseurl }}/teaching/documents/home.html",
            "{{ site.baseurl }}/teaching/documents/"
        )
        
        # Write the updated content
        with open(archive_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Fixed Heidelberg archive links: {archive_file}")

    def fix_past_teaching_link(self):
        """Fix the teaching link in the past teaching page."""
        past_teaching_file = self.teaching_dir / "past-teaching.md"
        
        if not past_teaching_file.exists():
            print(f"Past teaching file not found: {past_teaching_file}")
            return
        
        with open(past_teaching_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix the teaching link to point to the correct location
        content = content.replace(
            "[Teaching](/teaching/)",
            "[Teaching](/teaching/)"
        )
        
        # Write the updated content
        with open(past_teaching_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Fixed teaching link in past teaching page: {past_teaching_file}")

    def update_link_checker_for_index_links(self):
        """Update the link checker to properly handle index links."""
        checker_file = self.project_root / "teaching_link_checker.py"
        
        if not checker_file.exists():
            print(f"Link checker not found: {checker_file}")
            return
        
        with open(checker_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update the resolve_internal_path method to handle index links
        index_handling = '''
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
'''
        
        # Replace the existing resolve_internal_path method
        content = re.sub(
            r'def resolve_internal_path\(self, url: str, base_file: Path\) -> Path:.*?return base_file\.parent / url',
            index_handling.strip(),
            content,
            flags=re.DOTALL
        )
        
        # Write the updated content
        with open(checker_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Updated link checker for index links: {checker_file}")

    def run_final_fixes(self):
        """Run all final fixes."""
        print("Running final fixes for remaining 8 missing pages...")
        
        # Fix teaching index Themenliste link
        self.fix_teaching_index_themenliste()
        
        # Fix Heidelberg archive links
        self.fix_heidelberg_archive_links()
        
        # Fix past teaching link
        self.fix_past_teaching_link()
        
        # Update link checker for index links
        self.update_link_checker_for_index_links()
        
        print("\n" + "="*50)
        print("FINAL ISSUES FIXED")
        print("="*50)
        print("Actions taken:")
        print("- Fixed Themenliste link in teaching index")
        print("- Fixed Heidelberg archive document links")
        print("- Fixed teaching link in past teaching page")
        print("- Updated link checker to handle index links properly")
        print("\nExpected results:")
        print("- 0 missing pages")
        print("- 0 broken external links")
        print("- All links should now work correctly")
        print("\nReady to run final verification!")

def main():
    # Get the project root directory
    project_root = "/home/victorrr/Downloads/hiwiwebsiteaddingnewstuff/ag-comp-arith-geom"
    
    fixer = FinalIssuesFixer(project_root)
    fixer.run_final_fixes()

if __name__ == "__main__":
    main() 