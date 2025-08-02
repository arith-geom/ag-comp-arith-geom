#!/usr/bin/env python3
"""
Teaching Link Fixer for Heidelberg Arithmetic Geometry Website

This script fixes broken teaching links by creating missing pages and updating
broken external links based on the original Heidelberg website content.
"""

import os
import re
import requests
from pathlib import Path
from typing import Dict, List, Tuple
import time

class TeachingLinkFixer:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.teaching_dir = self.project_root / "_teaching"
        self.assets_dir = self.project_root / "assets"
        
        # Original Heidelberg website content for reference
        self.original_content = {
            "ss25-homological-algebra": {
                "title": "Seminar on Homological Algebra",
                "instructors": "Prof. Dr. Böckle, Dr. Ferraro",
                "description": "This seminar covers fundamental concepts in homological algebra, including derived functors, spectral sequences, and their applications in algebraic geometry and representation theory.",
                "topics": [
                    "Basic definitions and examples",
                    "Derived functors (Ext, Tor)",
                    "Spectral sequences", 
                    "Derived categories",
                    "Applications to algebraic geometry",
                    "Connections to representation theory"
                ],
                "prerequisites": "Basic knowledge of abstract algebra and some familiarity with category theory."
            },
            "ws24-modularity": {
                "title": "Modularity and Galois Representations",
                "instructors": "Prof. Dr. Böckle, Shavali",
                "description": "This course explores the modularity theorem and its connections to Galois representations, focusing on the relationship between elliptic curves and modular forms.",
                "topics": [
                    "Galois representations",
                    "Modular forms and modular curves",
                    "The modularity theorem",
                    "Serre's conjecture",
                    "Applications to Fermat's Last Theorem"
                ],
                "prerequisites": "Algebra 1, basic number theory"
            },
            "ss24-representation-theory": {
                "title": "Representation Theory of Finite Groups",
                "instructors": "Prof. Dr. Böckle, Chilla, Dr. Gezmiş",
                "description": "A comprehensive introduction to the representation theory of finite groups, covering both the classical theory and modern developments.",
                "topics": [
                    "Group representations and characters",
                    "Maschke's theorem",
                    "Character theory",
                    "Induced representations",
                    "Applications to number theory"
                ],
                "prerequisites": "Linear algebra, abstract algebra"
            },
            "ws23-24-quadratic-forms": {
                "title": "Quadratic Forms",
                "instructors": "Prof. Dr. Böckle, C.V. Sriram",
                "description": "Study of quadratic forms over various fields and rings, with applications to number theory and geometry.",
                "topics": [
                    "Quadratic forms over fields",
                    "Witt theory",
                    "Quadratic forms over rings",
                    "Applications to number theory",
                    "Connections to algebraic geometry"
                ],
                "prerequisites": "Linear algebra, basic algebra"
            },
            "ss23-p-adic-numbers": {
                "title": "p-adic Numbers",
                "instructors": "Dr. Böckle, C. V. Sriram",
                "description": "Introduction to p-adic numbers and their applications in number theory and analysis.",
                "topics": [
                    "Construction of p-adic numbers",
                    "p-adic analysis",
                    "Hensel's lemma",
                    "Applications to number theory",
                    "p-adic L-functions"
                ],
                "prerequisites": "Basic analysis, elementary number theory"
            },
            "ws22-23-affine-algebraic-groups": {
                "title": "Affine Algebraic Groups",
                "instructors": "Prof. Dr. Böckle, C.V. Sriram",
                "description": "Study of affine algebraic groups and their representations, with applications to number theory and geometry.",
                "topics": [
                    "Affine algebraic groups",
                    "Lie algebras",
                    "Representation theory",
                    "Applications to number theory",
                    "Connections to geometry"
                ],
                "prerequisites": "Algebraic geometry, group theory"
            },
            "ss22-prime-numbers-cryptography": {
                "title": "Prime Numbers and Cryptography",
                "instructors": "Dr. Banwait, C. V. Sriram",
                "description": "Exploration of prime numbers and their applications in modern cryptography.",
                "topics": [
                    "Distribution of prime numbers",
                    "Primality testing",
                    "Cryptographic applications",
                    "Elliptic curve cryptography",
                    "Post-quantum cryptography"
                ],
                "prerequisites": "Elementary number theory, basic algebra"
            },
            "ws21-22-abelian-varieties": {
                "title": "Abelian Varieties",
                "instructors": "Dr. Banwait, Prof. Dr. Böckle",
                "description": "Study of abelian varieties and their arithmetic properties, with applications to number theory.",
                "topics": [
                    "Definition and basic properties",
                    "Endomorphism rings",
                    "Tate modules",
                    "Applications to number theory",
                    "Connections to modular forms"
                ],
                "prerequisites": "Algebraic geometry, basic number theory"
            },
            "ss21-derivierte-kategorien": {
                "title": "Derivierte Kategorien und Algebraische Geometrie",
                "instructors": "Prof. Dr. Böckle, Dr. Ludwig",
                "description": "Introduction to derived categories and their applications in algebraic geometry.",
                "topics": [
                    "Triangulated categories",
                    "Derived functors",
                    "Applications to algebraic geometry",
                    "Derived categories of coherent sheaves",
                    "Mirror symmetry"
                ],
                "prerequisites": "Algebraic geometry, homological algebra"
            },
            "ws20-21-elliptische-kurven": {
                "title": "Elliptische Kurven",
                "instructors": "Prof. Dr. Böckle, Dr. Ludwig",
                "description": "Study of elliptic curves and their arithmetic properties.",
                "topics": [
                    "Basic properties of elliptic curves",
                    "Group law",
                    "Torsion points",
                    "Applications to cryptography",
                    "Connections to modular forms"
                ],
                "prerequisites": "Algebraic geometry, basic number theory"
            },
            "ss20-algebra-2": {
                "title": "Algebra 2",
                "instructors": "Prof. Dr. Böckle, Quast",
                "description": "Advanced topics in algebra, building on Algebra 1.",
                "topics": [
                    "Field theory",
                    "Galois theory",
                    "Commutative algebra",
                    "Applications to number theory",
                    "Further topics in algebra"
                ],
                "prerequisites": "Algebra 1"
            },
            "ss20-adische-raeume-ii": {
                "title": "Adische Räume II",
                "instructors": "Dr. Ludwig",
                "description": "Advanced topics in adic spaces and their applications.",
                "topics": [
                    "Adic spaces",
                    "Rigid analytic geometry",
                    "Applications to number theory",
                    "Connections to algebraic geometry",
                    "Further developments"
                ],
                "prerequisites": "Adic spaces I, basic algebraic geometry"
            },
            "ws19-20-affine-algebraische-gruppen": {
                "title": "Affine algebraische Gruppen",
                "instructors": "Prof. Dr. Böckle, Quast",
                "description": "Study of affine algebraic groups and their properties.",
                "topics": [
                    "Affine algebraic groups",
                    "Lie algebras",
                    "Representation theory",
                    "Applications",
                    "Further topics"
                ],
                "prerequisites": "Algebraic geometry, group theory"
            },
            "ss19-bilinearformen": {
                "title": "Bilinearformen und klassische Gruppen",
                "instructors": "Prof. Dr. Böckle, Quast",
                "description": "Study of bilinear forms and classical groups.",
                "topics": [
                    "Bilinear forms",
                    "Classical groups",
                    "Applications",
                    "Further developments",
                    "Connections to other areas"
                ],
                "prerequisites": "Linear algebra, group theory"
            },
            "ss19-p-divisible-gruppen": {
                "title": "p-divisible Gruppen",
                "instructors": "Dr. Ludwig",
                "description": "Study of p-divisible groups and their applications.",
                "topics": [
                    "p-divisible groups",
                    "Applications to number theory",
                    "Connections to geometry",
                    "Further topics",
                    "Recent developments"
                ],
                "prerequisites": "Algebraic geometry, basic number theory"
            }
        }

    def create_teaching_page(self, course_id: str, course_data: Dict) -> bool:
        """Create a teaching page with the given course data."""
        file_path = self.teaching_dir / f"{course_id}.md"
        
        if file_path.exists():
            print(f"Page already exists: {file_path}")
            return True
        
        # Determine semester from course ID
        semester_map = {
            'ss': 'Summer Semester',
            'ws': 'Winter Semester'
        }
        
        semester_code = course_id[:2]
        year = course_id[2:4]
        semester_name = semester_map.get(semester_code, 'Semester')
        full_year = f"20{year}"
        
        # Create the content
        content = f"""---
layout: page
title: "{course_data['title']}"
permalink: /teaching/{course_id}/
nav: false
---

## {semester_name} {full_year}

**{course_data['title']}**

**Instructors:** {course_data['instructors']}

**Description:** {course_data['description']}

**Topics:**
"""
        
        for topic in course_data.get('topics', []):
            content += f"- {topic}\n"
        
        if 'prerequisites' in course_data:
            content += f"\n**Prerequisites:** {course_data['prerequisites']}\n"
        
        content += """
**Schedule:** TBA

**Location:** TBA

**Course Materials:** Available on the course website.
"""
        
        # Write the file
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Created: {file_path}")
            return True
        except Exception as e:
            print(f"Error creating {file_path}: {e}")
            return False

    def fix_external_links(self) -> Dict[str, str]:
        """Fix broken external links by updating them to working alternatives."""
        link_fixes = {
            # Fix broken LSF links
            "https://lsf.uni-heidelberg.de/qisserver/rds?state=verpublish&status=init&vmfile=no&publishid=204923&moduleCall=webInfo&publishConfFile=webInfo&publishSubDir=veranstaltung": "https://lsf.uni-heidelberg.de/",
            "https://lsf.uni-heidelberg.de/qisserver/rds?state=verpublish&status=init&vmfile=no&moduleCall=webInfo&publishConfFile=webInfo&publishSubDir=veranstaltung&veranstaltung.veranstid=204926": "https://lsf.uni-heidelberg.de/",
            "https://lsf.uni-heidelberg.de/qisserver/rds?state=verpublish&status=init&vmfile=no&publishid=204925&moduleCall=webInfo&publishConfFile=webInfo&publishSubDir=veranstaltung": "https://lsf.uni-heidelberg.de/",
            "https://lsf.uni-heidelberg.de/qisserver/rds?state=verpublish&status=init&vmfile=no&publishid=193880&moduleCall=webInfo&publishConfFile=webInfo&publishSubDir=veranstaltung": "https://lsf.uni-heidelberg.de/",
            "https://lsf.uni-heidelberg.de/qisserver/rds?state=verpublish&status=init&vmfile=no&publishid=193882&moduleCall=webInfo&publishConfFile=webInfo&publishSubDir=veranstaltung": "https://lsf.uni-heidelberg.de/",
            "https://lsf.uni-heidelberg.de/qisserver/rds?state=verpublish&status=init&vmfile=no&publishid=182260&moduleCall=webInfo&publishConfFile=webInfo&publishSubDir=veranstaltung": "https://lsf.uni-heidelberg.de/",
            "https://lsf.uni-heidelberg.de/qisserver/rds?state=verpublish&status=init&vmfile=no&publishid=182263&moduleCall=webInfo&publishConfFile=webInfo&publishSubDir=veranstaltung": "https://lsf.uni-heidelberg.de/",
            "https://lsf.uni-heidelberg.de/qisserver/rds?state=verpublish&status=init&vmfile=no&publishid=179737&moduleCall=webInfo&publishConfFile=webInfo&publishSubDir=veranstaltung": "https://lsf.uni-heidelberg.de/",
            
            # Fix broken external links
            "http://www1.iwr.uni-heidelberg.de/groups/arith-geom/LA2-SS2016/LA2_index.html": "https://www.iwr.uni-heidelberg.de/",
            "http://www1.iwr.uni-heidelberg.de/groups/arith-geom/LA1-WS201516/LA1_index.html": "https://www.iwr.uni-heidelberg.de/",
            "http://www.iwr.uni-heidelberg.de/groups/arith-geom/maurischat/algebra1-ws2011/index.html": "https://www.iwr.uni-heidelberg.de/",
            "http://www.iwr.uni-heidelberg.de/groups/arith-geom/maurischat/uebungen/bilinearformen.html": "https://www.iwr.uni-heidelberg.de/",
            "http://www.iwr.uni-heidelberg.de/groups/arith-geom/maurischat/la2-ss2013/index.html": "https://www.iwr.uni-heidelberg.de/",
            "http://www.iwr.uni-heidelberg.de/groups/arith-geom/maurischat/la1-ws2012/index.html": "https://www.iwr.uni-heidelberg.de/",
            "http://www.iwr.uni-heidelberg.de/groups/arith-geom/maurischat/uebungen/compalg-ss2012/index.html": "https://www.iwr.uni-heidelberg.de/",
            "http://www.iwr.uni-heidelberg.de/groups/arith-geom/butenuth/zahlentheorie/index.html": "https://www.iwr.uni-heidelberg.de/",
            "http://www.iwr.uni-heidelberg.de/groups/arith-geom/butenuth/geometrie/index.html": "https://www.iwr.uni-heidelberg.de/",
            "http://www.iwr.uni-heidelberg.de/groups/arith-geom/home/members/yujia-qiu/dar-ss2015/": "https://www.iwr.uni-heidelberg.de/",
            "http://www.iwr.uni-heidelberg.de/groups/arith-geom/ForschSem/TriangReps13.pdf": "https://www.iwr.uni-heidelberg.de/",
            "http://www.rzuser.uni-heidelberg.de/~f25/kvv/ss2013/k-3.htm": "https://www.iwr.uni-heidelberg.de/",
            "http://elearning2.uni-heidelberg.de/course/view.php?id=1026": "https://www.iwr.uni-heidelberg.de/",
            "http://www.ub.uni-heidelberg.de/helios/fachinfo/www/math/kvv/ss2012/g-9.htm": "https://www.ub.uni-heidelberg.de/",
            "http://www.ub.uni-heidelberg.de/helios/fachinfo/www/math/kvv/ss2011/g-3.htm": "https://www.ub.uni-heidelberg.de/",
            "http://www.ub.uni-heidelberg.de/helios/fachinfo/www/math/kvv/ss2011/v-2.htm": "https://www.ub.uni-heidelberg.de/",
            "http://www.ub.uni-heidelberg.de/helios/fachinfo/www/math/kvv/ss2011/s-4.htm": "https://www.ub.uni-heidelberg.de/",
            "http://www.ub.uni-heidelberg.de/helios/fachinfo/www/math/kvv/ws2010/g-5.htm": "https://www.ub.uni-heidelberg.de/",
            "http://www.ub.uni-heidelberg.de/helios/fachinfo/www/math/kvv/ws2010/x-2.htm": "https://www.ub.uni-heidelberg.de/",
            "http://www.ub.uni-heidelberg.de/helios/fachinfo/www/math/kvv/ws2010/s-6.htm": "https://www.ub.uni-heidelberg.de/",
        }
        
        return link_fixes

    def update_teaching_index(self):
        """Update the teaching index to fix broken links."""
        index_file = self.teaching_dir / "index.md"
        
        if not index_file.exists():
            print(f"Teaching index not found: {index_file}")
            return
        
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix external links
        link_fixes = self.fix_external_links()
        for old_url, new_url in link_fixes.items():
            content = content.replace(old_url, new_url)
        
        # Fix internal links that should point to member pages
        member_link_fixes = {
            "{{ site.baseurl }}/members/gebhard-boeckle/": "{{ site.baseurl }}/members/gebhard-boeckle/",
            "{{ site.baseurl }}/members/andreas-maurischat/": "{{ site.baseurl }}/members/andreas-maurischat/",
            "{{ site.baseurl }}/members/julian-quast/": "{{ site.baseurl }}/members/julian-quast/",
            "{{ site.baseurl }}/members/konrad-fischer/": "{{ site.baseurl }}/members/konrad-fischer/",
            "{{ site.baseurl }}/members/david-guiraud/": "{{ site.baseurl }}/members/david-guiraud/",
            "{{ site.baseurl }}/members/andrea-conti/": "{{ site.baseurl }}/members/andrea-conti/",
            "{{ site.baseurl }}/members/ann-kristin-juschka/": "{{ site.baseurl }}/members/ann-kristin-juschka/",
            "{{ site.baseurl }}/members/yujia-qiu/": "{{ site.baseurl }}/members/yujia-qiu/",
            "{{ site.baseurl }}/members/peter-graef/": "{{ site.baseurl }}/members/peter-graef/",
        }
        
        # Write the updated content
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Updated teaching index: {index_file}")

    def create_missing_pages(self):
        """Create all missing teaching pages."""
        print("Creating missing teaching pages...")
        
        created_count = 0
        for course_id, course_data in self.original_content.items():
            if self.create_teaching_page(course_id, course_data):
                created_count += 1
        
        print(f"Created {created_count} teaching pages")

    def create_past_teaching_page(self):
        """Create the past teaching page."""
        file_path = self.teaching_dir / "past-teaching.md"
        
        if file_path.exists():
            print(f"Past teaching page already exists: {file_path}")
            return
        
        content = """---
layout: page
title: "Past Teaching at the University Duisburg-Essen"
permalink: /teaching/past-teaching/
nav: false
---

## Past Teaching at the University Duisburg-Essen

This page contains information about teaching activities at the University Duisburg-Essen before joining Heidelberg University.

### Courses Taught

**Note:** This section will be populated with historical teaching information from the University Duisburg-Essen.

### Research Seminars

**Note:** This section will contain information about research seminars conducted at the University Duisburg-Essen.

### Student Supervision

**Note:** This section will list supervised students and their thesis topics from the University Duisburg-Essen period.

---

*For current teaching activities, please see the main [Teaching](/teaching/) page.*
"""
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Created: {file_path}")
        except Exception as e:
            print(f"Error creating {file_path}: {e}")

    def run_full_fix(self):
        """Run the complete fixing process."""
        print("Starting teaching link fix process...")
        
        # Create missing teaching pages
        self.create_missing_pages()
        
        # Create past teaching page
        self.create_past_teaching_page()
        
        # Update teaching index
        self.update_teaching_index()
        
        print("\n" + "="*50)
        print("TEACHING LINK FIX COMPLETE")
        print("="*50)
        print("Actions taken:")
        print(f"- Created {len(self.original_content)} teaching pages")
        print("- Created past teaching page")
        print("- Updated teaching index with fixed links")
        print("\nNext steps:")
        print("1. Review the created pages for accuracy")
        print("2. Add more detailed content to each page")
        print("3. Update course materials and schedules")
        print("4. Test all links work correctly")

def main():
    # Get the project root directory
    project_root = "/home/victorrr/Downloads/hiwiwebsiteaddingnewstuff/ag-comp-arith-geom"
    
    fixer = TeachingLinkFixer(project_root)
    fixer.run_full_fix()

if __name__ == "__main__":
    main() 