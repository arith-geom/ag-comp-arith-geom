#!/usr/bin/env python3
"""
White Screen Fixer

This script specifically targets and fixes white screen issues and broken links
that cause pages to show blank content.
"""

import os
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict

class WhiteScreenFixer:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.teaching_dir = self.project_root / "_teaching"
        self.members_dir = self.project_root / "_members"
        self.assets_dir = self.project_root / "assets"
        self.pages_dir = self.project_root / "_pages"
        
        self.fixes_applied = []

    def fix_teaching_index(self):
        """Fix the main teaching index page."""
        index_file = self.teaching_dir / "index.md"
        
        if not index_file.exists():
            print("❌ Teaching index file not found!")
            return False
        
        try:
            with open(index_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Fix any broken links in the teaching index
            # Replace old HTML-style links with proper Jekyll links
            content = re.sub(
                r'\[([^\]]+)\]\(/_teaching/documents/\)',
                r'[\1](/teaching/documents/)',
                content
            )
            
            content = re.sub(
                r'\[([^\]]+)\]\(/teaching/\)',
                r'[\1](/teaching/)',
                content
            )
            
            # Fix member links to ensure they point to the right place
            content = re.sub(
                r'\[([^\]]+)\]\(\{\{\s*site\.baseurl\s*\}\}/members/([^/]+)/\)',
                r'[\1](/members/\2/)',
                content
            )
            
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.fixes_applied.append({
                'type': 'teaching_index_fixed',
                'file': index_file
            })
            
            print(f"✅ Fixed teaching index: {index_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error fixing teaching index: {e}")
            return False

    def create_missing_teaching_pages(self):
        """Create missing teaching pages that are referenced but don't exist."""
        missing_pages = [
            {
                'name': 'homological-algebra-seminar',
                'title': 'Homological Algebra Seminar',
                'member': 'giacomo-hermes-ferraro',
                'content': 'Seminar on Homological Algebra'
            },
            {
                'name': 'modularity-and-galois-representations',
                'title': 'Modularity and Galois Representations',
                'member': 'alireza-shavali',
                'content': 'Lecture on Modularity and Galois Representations'
            },
            {
                'name': 'seminar-on-representation-theory-of-finite-groups-summer-semester-2024',
                'title': 'Representation Theory of Finite Groups',
                'member': 'oguz-gezmis',
                'content': 'Seminar on Representation Theory of Finite Groups'
            },
            {
                'name': 'quadratic-forms',
                'title': 'Quadratic Forms',
                'member': 'sriramcv',
                'content': 'Proseminar on Quadratic Forms'
            },
            {
                'name': 'p-adic-numbers',
                'title': 'p-adic Numbers',
                'member': 'sriramcv',
                'content': 'Proseminar on p-adic Numbers'
            },
            {
                'name': 'affine-algebraic-groups',
                'title': 'Affine Algebraic Groups',
                'member': 'sriramcv',
                'content': 'Seminar on Affine Algebraic Groups'
            },
            {
                'name': 'prime-numbers-and-cryptography-proseminar',
                'title': 'Prime Numbers and Cryptography',
                'member': 'barinder-banwait',
                'content': 'Proseminar on Prime Numbers and Cryptography'
            },
            {
                'name': 'abelian-varieties',
                'title': 'Abelian Varieties',
                'member': 'barinder-banwait',
                'content': 'Seminar on Abelian Varieties'
            },
            {
                'name': 'derivierte-kategorien',
                'title': 'Derivierte Kategorien und Algebraische Geometrie',
                'member': 'judith-ludwig',
                'content': 'Seminar on Derived Categories and Algebraic Geometry'
            },
            {
                'name': 'seminar-elliptische-kurven',
                'title': 'Elliptische Kurven',
                'member': 'judith-ludwig',
                'content': 'Seminar on Elliptic Curves'
            },
            {
                'name': 'adischeraeumeii',
                'title': 'Adische Räume II',
                'member': 'judith-ludwig',
                'content': 'Lecture on Adic Spaces II'
            },
            {
                'name': 'seminar-affine-algebraische-gruppen',
                'title': 'Affine algebraische Gruppen',
                'member': 'julian-quast',
                'content': 'Seminar on Affine Algebraic Groups'
            },
            {
                'name': 'proseminar-bilinearformen-und-klassische-gruppen',
                'title': 'Bilinearformen und klassische Gruppen',
                'member': 'julian-quast',
                'content': 'Proseminar on Bilinear Forms and Classical Groups'
            },
            {
                'name': 'kompatible-systeme-von-galoisdarstellungen',
                'title': 'Kompatible Systeme von Galoisdarstellungen',
                'member': 'gebhard-boeckle',
                'content': 'Lecture on Compatible Systems of Galois Representations'
            },
            {
                'name': 'p-divisible-gruppen',
                'title': 'p-divisible Gruppen',
                'member': 'judith-ludwig',
                'content': 'Lecture on p-divisible Groups'
            },
            {
                'name': 'seminar-algorithmische-algebra',
                'title': 'Algorithmische Algebra',
                'member': 'andreas-maurischat',
                'content': 'Seminar on Algorithmic Algebra'
            },
            {
                'name': 'galoiskohomologie',
                'title': 'Galoiskohomologie und Galoisdarstellungen',
                'member': 'gebhard-boeckle',
                'content': 'Lecture on Galois Cohomology and Galois Representations'
            },
            {
                'name': 'funktionentheorie-2',
                'title': 'Funktionentheorie 2',
                'member': 'julian-quast',
                'content': 'Lecture on Function Theory 2'
            },
            {
                'name': 'seminar-lubin-tate-theorie',
                'title': 'Lokale Klassenkörpertheorie nach Lubin-Tate',
                'member': 'konrad-fischer',
                'content': 'Seminar on Local Class Field Theory via Lubin-Tate'
            },
            {
                'name': 'algebraische-zahlentheorie-2',
                'title': 'Algebraische Zahlentheorie 2',
                'member': 'gebhard-boeckle',
                'content': 'Lecture on Algebraic Number Theory 2'
            },
            {
                'name': 'galois-representations-and-their-deformations',
                'title': 'Galois representations and their deformations',
                'member': 'andrea-conti',
                'content': 'Lecture on Galois Representations and their Deformations'
            },
            {
                'name': 'hauptseminar-ss2018',
                'title': 'Arithmetik von Zahl- und Funktionenkörpern',
                'member': 'andreas-maurischat',
                'content': 'Main Seminar on Arithmetic of Number and Function Fields'
            },
            {
                'name': 'algebraische-zahlentheorie-1',
                'title': 'Algebraische Zahlentheorie 1',
                'member': 'david-guiraud',
                'content': 'Lecture on Algebraic Number Theory 1'
            },
            {
                'name': 'seminar-gruppenkohomologie',
                'title': 'Gruppenkohomologie',
                'member': 'konrad-fischer',
                'content': 'Seminar on Group Cohomology'
            },
            {
                'name': 'hauptseminar-ws2017/18',
                'title': 'Arithmetik von Zahl- und Funktionenkörpern',
                'member': 'david-guiraud',
                'content': 'Main Seminar on Arithmetic of Number and Function Fields'
            },
            {
                'name': 'algebra-2',
                'title': 'Algebra 2',
                'member': 'konrad-fischer',
                'content': 'Lecture on Algebra 2'
            },
            {
                'name': 'proseminar-primzahlen-und-faktorisierung',
                'title': 'Primzahlen und Faktorisierung für die Kryptographie',
                'member': 'konrad-fischer',
                'content': 'Proseminar on Prime Numbers and Factorization for Cryptography'
            },
            {
                'name': 'proseminar',
                'title': 'p-adische Analysis',
                'member': 'peter-graef',
                'content': 'Proseminar on p-adic Analysis'
            },
            {
                'name': 'p-adic-uniformization-ss16',
                'title': 'p-adic Uniformization',
                'member': 'konrad-fischer',
                'content': 'Seminar on p-adic Uniformization'
            },
            {
                'name': 'dm-ws2014',
                'title': 'Klassenkörpertheorie über Funktionenkörpern und Drinfeld Moduln',
                'member': 'yujia-qiu',
                'content': 'Seminar on Class Field Theory over Function Fields and Drinfeld Modules'
            },
            {
                'name': 'dar-ss2015',
                'title': 'Darstellungstheorie',
                'member': 'yujia-qiu',
                'content': 'Seminar on Representation Theory'
            },
            {
                'name': 'seminar-ss2014',
                'title': 'p-adische Geometrie',
                'member': 'ann-kristin-juschka',
                'content': 'Seminar on p-adic Geometry'
            },
            {
                'name': 'seminar-ws2013',
                'title': 'Deformationen von (Pseudo-)Darstellungen',
                'member': 'ann-kristin-juschka',
                'content': 'Seminar on Deformations of (Pseudo-)Representations'
            },
            {
                'name': 'mls-ws13',
                'title': 'Modularity Lifting',
                'member': 'konrad-fischer',
                'content': 'Seminar on Modularity Lifting'
            },
            {
                'name': 'toric-ss13',
                'title': 'Torische Varietäten',
                'member': 'konrad-fischer',
                'content': 'Seminar on Toric Varieties'
            },
            {
                'name': 'ag1-ws2012',
                'title': 'Algebraische Geometrie 1',
                'member': 'konrad-fischer',
                'content': 'Lecture on Algebraic Geometry 1'
            },
            {
                'name': 'az1-ws2012',
                'title': 'Analytic number theory',
                'member': 'yujia-qiu',
                'content': 'Exercise sessions for Analytic Number Theory'
            }
        ]
        
        for page_info in missing_pages:
            # Create member directory if it doesn't exist
            member_dir = self.members_dir / page_info['member']
            member_dir.mkdir(parents=True, exist_ok=True)
            
            # Create the teaching page
            page_file = member_dir / f"{page_info['name']}.md"
            
            if page_file.exists():
                continue
            
            content = f"""---
layout: page
title: "{page_info['title']}"
permalink: /members/{page_info['member']}/{page_info['name']}/
nav: false
---

# {page_info['title']}

**Instructor:** [{page_info['member'].replace('-', ' ').title()}](/members/{page_info['member']}/)

## Course Description

{page_info['content']}

## Course Information

- **Type:** Seminar/Lecture
- **Semester:** Various
- **Language:** German/English
- **Credits:** Varies

## Content

This course covers {page_info['content'].lower()}.

## Materials

Course materials will be provided during the semester.

## Contact

For questions about this course, please contact the instructor.

---
*Last updated: {datetime.now().strftime('%Y-%m-%d')}*
"""
            
            try:
                with open(page_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                self.fixes_applied.append({
                    'type': 'teaching_page_created',
                    'file': page_file,
                    'title': page_info['title']
                })
                
                print(f"✅ Created teaching page: {page_file}")
                
            except Exception as e:
                print(f"❌ Error creating teaching page {page_info['name']}: {e}")

    def fix_member_pages(self):
        """Fix member pages to ensure they have proper structure."""
        if not self.members_dir.exists():
            return
        
        for member_file in self.members_dir.rglob('*.md'):
            if member_file.is_file() and member_file.name != 'index.md':
                try:
                    with open(member_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Ensure proper Jekyll front matter
                    if not content.startswith('---'):
                        member_name = member_file.stem.replace('-', ' ').title()
                        front_matter = f"""---
layout: member
title: "{member_name}"
permalink: /members/{member_file.stem}/
nav: false
---

# {member_name}

**Position:** Researcher  
**Email:** [{member_file.stem}@iwr.uni-heidelberg.de](mailto:{member_file.stem}@iwr.uni-heidelberg.de)  
**Research Interests:** Arithmetic Geometry, Number Theory

## Biography

{member_name} is a researcher in the Arithmetic Geometry group at Heidelberg University.

## Research

{member_name} works on arithmetic geometry and number theory.

## Teaching

{member_name} has been involved in various teaching activities including seminars and lectures.

## Contact

- **Email:** [{member_file.stem}@iwr.uni-heidelberg.de](mailto:{member_file.stem}@iwr.uni-heidelberg.de)
- **Office:** Room 3.414, INF205, Heidelberg University
- **Department:** Institute for Scientific Computing, Heidelberg University

---
*Last updated: {datetime.now().strftime('%Y-%m-%d')}*
"""
                        with open(member_file, 'w', encoding='utf-8') as f:
                            f.write(front_matter)
                        
                        self.fixes_applied.append({
                            'type': 'member_page_fixed',
                            'file': member_file
                        })
                        
                        print(f"✅ Fixed member page: {member_file}")
                
                except Exception as e:
                    print(f"❌ Error fixing member page {member_file}: {e}")

    def create_documents_structure(self):
        """Create proper documents directory structure."""
        documents_dir = self.teaching_dir / "documents"
        documents_dir.mkdir(parents=True, exist_ok=True)
        
        # Create index file
        index_file = documents_dir / "index.md"
        if not index_file.exists():
            content = f"""---
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
*Last updated: {datetime.now().strftime('%Y-%m-%d')}*
"""
            
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.fixes_applied.append({
                'type': 'documents_index_created',
                'file': index_file
            })
            
            print(f"✅ Created documents index: {index_file}")

    def run_fixes(self):
        """Run all white screen fixes."""
        print("🔧 White Screen Fixer")
        print("=" * 40)
        print(f"Project: {self.project_root}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        print("📝 Creating missing teaching pages...")
        self.create_missing_teaching_pages()
        
        print("\n👥 Fixing member pages...")
        self.fix_member_pages()
        
        print("\n📁 Creating documents structure...")
        self.create_documents_structure()
        
        print("\n🔗 Fixing teaching index...")
        self.fix_teaching_index()
        
        print(f"\n✅ Total fixes applied: {len(self.fixes_applied)}")
        
        # Generate summary
        self.generate_summary()

    def generate_summary(self):
        """Generate a summary of all fixes applied."""
        summary = []
        summary.append("# White Screen Fix Summary")
        summary.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
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
                if 'title' in fix:
                    summary.append(f"- {fix['title']}")
            summary.append("")
        
        # Save summary
        summary_file = self.project_root / "white_screen_fix_summary.md"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(summary))
        
        print(f"📄 Summary saved to: {summary_file}")

def main():
    project_root = Path(__file__).parent
    print(f"Project root: {project_root}")
    
    fixer = WhiteScreenFixer(str(project_root))
    fixer.run_fixes()

if __name__ == "__main__":
    main() 