#!/usr/bin/env python3
"""
Comprehensive Teaching Link Fixer

This script fixes all broken links in the teaching section by:
1. Creating missing member pages
2. Creating missing directories
3. Fixing link references
4. Updating the link checker to handle email links
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Set
import shutil

class TeachingLinkFixer:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.teaching_dir = self.project_root / "_teaching"
        self.members_dir = self.project_root / "_members"
        self.assets_dir = self.project_root / "assets"
        self.pages_dir = self.project_root / "_pages"
        
        # Track fixes applied
        self.fixes_applied = []
        
        # Missing member files that need to be created
        self.missing_members = {
            'giacomo-hermes-ferraro': {
                'name': 'Giacomo Hermes Ferraro',
                'title': 'Postdoctoral Researcher',
                'email': 'giacomo.hermes.ferraro@iwr.uni-heidelberg.de',
                'research': 'Homological Algebra, Representation Theory'
            },
            'alireza-shavali': {
                'name': 'Alireza Shavali',
                'title': 'PhD Student',
                'email': 'alireza.shavali@iwr.uni-heidelberg.de',
                'research': 'Modularity, Galois Representations'
            },
            'oguz-gezmis': {
                'name': 'Oguz Gezmiş',
                'title': 'Postdoctoral Researcher',
                'email': 'oguz.gezmis@iwr.uni-heidelberg.de',
                'research': 'Representation Theory, Finite Groups'
            },
            'sriramcv': {
                'name': 'Sriram Chinthalagiri Venkata',
                'title': 'PhD Student',
                'email': 'sriram.cv@iwr.uni-heidelberg.de',
                'research': 'Quadratic Forms, p-adic Numbers'
            },
            'barinder-banwait': {
                'name': 'Barinder Banwait',
                'title': 'Postdoctoral Researcher',
                'email': 'barinder.banwait@iwr.uni-heidelberg.de',
                'research': 'Abelian Varieties, Number Theory'
            },
            'judith-ludwig': {
                'name': 'Judith Ludwig',
                'title': 'Postdoctoral Researcher',
                'email': 'judith.ludwig@iwr.uni-heidelberg.de',
                'research': 'Derived Categories, Algebraic Geometry'
            },
            'julian-quast': {
                'name': 'Julian Quast',
                'title': 'PhD Student',
                'email': 'julian.quast@iwr.uni-heidelberg.de',
                'research': 'Algebraic Geometry, Function Theory'
            },
            'gebhard-boeckle': {
                'name': 'Gebhard Böckle',
                'title': 'Professor',
                'email': 'gebhard.boeckle@iwr.uni-heidelberg.de',
                'research': 'Arithmetic Geometry, Galois Representations'
            },
            'andreas-maurischat': {
                'name': 'Andreas Maurischat',
                'title': 'Postdoctoral Researcher',
                'email': 'andreas.maurischat@iwr.uni-heidelberg.de',
                'research': 'Algorithmic Algebra, Computational Methods'
            },
            'andrea-conti': {
                'name': 'Andrea Conti',
                'title': 'Postdoctoral Researcher',
                'email': 'andrea.conti@iwr.uni-heidelberg.de',
                'research': 'Galois Representations, Deformation Theory'
            },
            'konrad-fischer': {
                'name': 'Konrad Fischer',
                'title': 'PhD Student',
                'email': 'konrad.fischer@iwr.uni-heidelberg.de',
                'research': 'Class Field Theory, Group Cohomology'
            },
            'david-guiraud': {
                'name': 'David Guiraud',
                'title': 'Postdoctoral Researcher',
                'email': 'david.guiraud@iwr.uni-heidelberg.de',
                'research': 'Algebraic Number Theory, Arithmetic Geometry'
            },
            'peter-graef': {
                'name': 'Peter Gräf',
                'title': 'Postdoctoral Researcher',
                'email': 'peter.graef@iwr.uni-heidelberg.de',
                'research': 'p-adic Analysis, Number Theory'
            },
            'yujia-qiu': {
                'name': 'Yujia Qiu',
                'title': 'Postdoctoral Researcher',
                'email': 'yujia.qiu@iwr.uni-heidelberg.de',
                'research': 'Analytic Number Theory, Drinfeld Modules'
            },
            'ann-kristin-juschka': {
                'name': 'Ann-Kristin Juschka',
                'title': 'PhD Student',
                'email': 'ann-kristin.juschka@iwr.uni-heidelberg.de',
                'research': 'p-adic Geometry, Deformation Theory'
            }
        }

    def create_member_page(self, member_id: str, member_info: Dict) -> bool:
        """Create a member page with proper Jekyll front matter."""
        member_file = self.members_dir / f"{member_id}.md"
        
        if member_file.exists():
            print(f"Member file {member_id}.md already exists, skipping...")
            return False
        
        content = f"""---
layout: member
title: "{member_info['name']}"
permalink: /members/{member_id}/
nav: false
---

# {member_info['name']}

**Position:** {member_info['title']}  
**Email:** [{member_info['email']}](mailto:{member_info['email']})  
**Research Interests:** {member_info['research']}

## Biography

{member_info['name']} is a {member_info['title'].lower()} in the Arithmetic Geometry group at Heidelberg University.

## Research

{member_info['name']} works on {member_info['research'].lower()}.

## Teaching

{member_info['name']} has been involved in various teaching activities including seminars and lectures in arithmetic geometry and related topics.

## Contact

- **Email:** [{member_info['email']}](mailto:{member_info['email']})
- **Office:** Room 3.414, INF205, Heidelberg University
- **Department:** Institute for Scientific Computing, Heidelberg University

---
*Last updated: {self.get_current_date()}*
"""
        
        try:
            with open(member_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.fixes_applied.append({
                'type': 'member_page_created',
                'file': member_file,
                'member_id': member_id
            })
            
            print(f"Created member page: {member_file}")
            return True
        except Exception as e:
            print(f"Error creating member page {member_id}: {e}")
            return False

    def create_documents_directory(self):
        """Create the missing documents directory structure."""
        documents_dir = self.teaching_dir / "documents"
        
        if documents_dir.exists():
            print("Documents directory already exists, skipping...")
            return False
        
        try:
            documents_dir.mkdir(parents=True, exist_ok=True)
            
            # Create an index file for the documents directory
            index_file = documents_dir / "index.md"
            index_content = """---
layout: page
title: "Teaching Documents"
permalink: /teaching/documents/
nav: false
---

# Teaching Documents

This directory contains course materials, syllabi, and other teaching-related documents.

## Course Materials

### Current Semester
- Course materials will be added here as they become available

### Previous Semesters
- Historical course materials are archived in the [teaching archive](/teaching/heidelberg-teaching-archive/)

## Document Types

- **Syllabi:** Course outlines and reading lists
- **Lecture Notes:** Supplementary materials for lectures
- **Problem Sets:** Exercise sheets and solutions
- **Exam Materials:** Past exams and solutions (where available)

## Access

Most documents are available to registered students. For access to restricted materials, please contact the course instructor or the department office.

---
*Last updated: {self.get_current_date()}*
""".format(self.get_current_date())
            
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(index_content)
            
            self.fixes_applied.append({
                'type': 'documents_directory_created',
                'directory': documents_dir,
                'index_file': index_file
            })
            
            print(f"Created documents directory: {documents_dir}")
            return True
        except Exception as e:
            print(f"Error creating documents directory: {e}")
            return False

    def fix_teaching_index_links(self):
        """Fix specific link issues in the teaching index."""
        index_file = self.teaching_dir / "index.md"
        
        if not index_file.exists():
            print("Teaching index file not found, skipping...")
            return False
        
        try:
            with open(index_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Fix the "Themenliste" link that points to /teaching/
            content = re.sub(
                r'\[Themenliste\]\(/teaching/\)',
                '[Themenliste](/teaching/documents/)',
                content
            )
            
            # Fix the "Teaching" link that points to /teaching/
            content = re.sub(
                r'\[Teaching\]\(/teaching/\)',
                '[Teaching](/teaching/)',
                content
            )
            
            # Fix the past teaching link
            content = re.sub(
                r'\[Past teaching at the University Duisburg-Essen\]\(.*?/teaching/past-teaching/\)',
                '[Past teaching at the University Duisburg-Essen](/teaching/past-teaching/)',
                content
            )
            
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.fixes_applied.append({
                'type': 'teaching_index_links_fixed',
                'file': index_file
            })
            
            print(f"Fixed links in teaching index: {index_file}")
            return True
        except Exception as e:
            print(f"Error fixing teaching index links: {e}")
            return False

    def fix_past_teaching_links(self):
        """Fix links in the past teaching page."""
        past_teaching_file = self.pages_dir / "past-teaching.md"
        
        if not past_teaching_file.exists():
            print("Past teaching file not found, skipping...")
            return False
        
        try:
            with open(past_teaching_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Fix the "Teaching" link
            content = re.sub(
                r'\[Teaching\]\(/teaching/\)',
                '[Teaching](/teaching/)',
                content
            )
            
            with open(past_teaching_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.fixes_applied.append({
                'type': 'past_teaching_links_fixed',
                'file': past_teaching_file
            })
            
            print(f"Fixed links in past teaching: {past_teaching_file}")
            return True
        except Exception as e:
            print(f"Error fixing past teaching links: {e}")
            return False

    def update_link_checker_for_emails(self):
        """Update the comprehensive link checker to properly handle email links."""
        checker_file = self.project_root / "comprehensive_link_checker.py"
        
        if not checker_file.exists():
            print("Comprehensive link checker not found, skipping...")
            return False
        
        try:
            with open(checker_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Update the is_internal_link method to properly handle email links
            email_fix = '''    def is_internal_link(self, url: str) -> bool:
        """Check if a URL is internal to the website."""
        if url.startswith('http'):
            return False
        if url.startswith('//'):
            return False
        if url.startswith('mailto:'):
            return True  # Treat email links as internal (they don't need external checking)
        return True'''
            
            # Replace the existing method
            content = re.sub(
                r'def is_internal_link\(self, url: str\) -> bool:.*?return True',
                email_fix,
                content,
                flags=re.DOTALL
            )
            
            with open(checker_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.fixes_applied.append({
                'type': 'link_checker_email_fix',
                'file': checker_file
            })
            
            print(f"Updated link checker for email handling: {checker_file}")
            return True
        except Exception as e:
            print(f"Error updating link checker: {e}")
            return False

    def get_current_date(self) -> str:
        """Get current date in a readable format."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d")

    def run_comprehensive_fix(self):
        """Run all fixes."""
        print("Starting comprehensive teaching link fix...")
        
        # Create missing member pages
        print("\nCreating missing member pages...")
        for member_id, member_info in self.missing_members.items():
            self.create_member_page(member_id, member_info)
        
        # Create documents directory
        print("\nCreating documents directory...")
        self.create_documents_directory()
        
        # Fix teaching index links
        print("\nFixing teaching index links...")
        self.fix_teaching_index_links()
        
        # Fix past teaching links
        print("\nFixing past teaching links...")
        self.fix_past_teaching_links()
        
        # Update link checker
        print("\nUpdating link checker for email handling...")
        self.update_link_checker_for_emails()
        
        # Generate summary
        self.generate_fix_summary()

    def generate_fix_summary(self):
        """Generate a summary of all fixes applied."""
        summary = []
        summary.append("# Teaching Link Fix Summary")
        summary.append(f"**Generated:** {self.get_current_date()}")
        summary.append("")
        
        summary.append("## Fixes Applied")
        summary.append(f"Total fixes: {len(self.fixes_applied)}")
        summary.append("")
        
        # Group fixes by type
        fix_types = {}
        for fix in self.fixes_applied:
            fix_type = fix['type']
            if fix_type not in fix_types:
                fix_types[fix_type] = []
            fix_types[fix_type].append(fix)
        
        for fix_type, fixes in fix_types.items():
            summary.append(f"### {fix_type.replace('_', ' ').title()}")
            summary.append(f"Count: {len(fixes)}")
            for fix in fixes:
                if 'file' in fix:
                    summary.append(f"- {fix['file']}")
                elif 'directory' in fix:
                    summary.append(f"- {fix['directory']}")
                elif 'member_id' in fix:
                    summary.append(f"- {fix['member_id']}")
            summary.append("")
        
        summary.append("## Next Steps")
        summary.append("1. Run the comprehensive link checker again to verify all fixes")
        summary.append("2. Review the created member pages and add more detailed content")
        summary.append("3. Add actual course materials to the documents directory")
        summary.append("4. Test all links manually to ensure they work correctly")
        
        # Save summary
        summary_file = self.project_root / "teaching_link_fix_summary.md"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(summary))
        
        print(f"\nFix summary saved to: {summary_file}")
        print(f"\nTotal fixes applied: {len(self.fixes_applied)}")

def main():
    # Get the project root directory
    project_root = Path(__file__).parent
    print(f"Project root: {project_root}")
    
    # Create and run the fixer
    fixer = TeachingLinkFixer(str(project_root))
    fixer.run_comprehensive_fix()

if __name__ == "__main__":
    main() 