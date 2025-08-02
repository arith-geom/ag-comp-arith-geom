#!/usr/bin/env python3
"""
Fix Teaching Links Properly Based on Original Heidelberg Website

This script properly fixes the teaching index by replacing old teaching page links
with the correct member page links and PDF links.
"""

import re
from pathlib import Path

class TeachingLinksProperFixer:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.teaching_dir = self.project_root / "_teaching"
        
        # Correct link mappings based on original Heidelberg website
        self.link_replacements = {
            # 2025
            r'\[Homological Algebra\]\(.*?ss25-homological-algebra.*?\)': '[Homological Algebra]({{ site.baseurl }}/members/giacomo-hermes-ferraro/)',
            
            # 2024/25
            r'\[Commutative Algebra\]\(.*?comm_alg_announcement\.pdf.*?\)': '[Commutative Algebra](/assets/uploads/comm_alg_announcement.pdf)',
            r'\[Modularity and Galois Representations\]\(.*?ws24-modularity.*?\)': '[Modularity and Galois Representations]({{ site.baseurl }}/members/alireza-shavali/)',
            r'\[Congruence Modules and the Wiles–Lenstra–Diamond Numerical Criterion in Higher Codimension\]\(.*?GAUS-AG-WiSe2024-25-IKM-2024-12-11\.pdf.*?\)': '[Congruence Modules and the Wiles–Lenstra–Diamond Numerical Criterion in Higher Codimension](/assets/uploads/GAUS-AG-WiSe2024-25-IKM-2024-12-11.pdf)',
            
            # 2024
            r'\[Representation theory of finite groups\]\(.*?ss24-representation-theory.*?\)': '[Representation theory of finite groups]({{ site.baseurl }}/members/oguz-gezmis/)',
            r'\[Algebra 2\]\(.*?ss24-algebra-2.*?\)': '[Algebra 2]({{ site.baseurl }}/members/alireza-shavali/)',
            
            # 2023/24
            r'\[Quadratic forms\]\(.*?ws23-24-quadratic-forms.*?\)': '[Quadratic forms]({{ site.baseurl }}/members/sriramcv/)',
            r'\[Algebra 1\]\(.*?ws23-24-algebra-1.*?\)': '[Algebra 1]({{ site.baseurl }}/members/alireza-shavali/)',
            
            # 2023
            r'\[p-adic numbers\]\(.*?ss23-p-adic-numbers.*?\)': '[p-adic numbers]({{ site.baseurl }}/members/sriramcv/)',
            
            # 2022/23
            r'\[Affine Algebraic Groups\]\(.*?ws22-23-affine-algebraic-groups.*?\)': '[Affine Algebraic Groups]({{ site.baseurl }}/members/sriramcv/)',
            
            # 2022
            r'\[Prime numbers and Cryptography\]\(.*?ss22-prime-numbers-cryptography.*?\)': '[Prime numbers and Cryptography]({{ site.baseurl }}/members/barinder-banwait/)',
            
            # 2021/22
            r'\[Abelian Varieties\]\(.*?ws21-22-abelian-varieties.*?\)': '[Abelian Varieties]({{ site.baseurl }}/members/barinder-banwait/)',
            
            # 2021
            r'\[Derivierte Kategorien und Algebraische Geometrie\]\(.*?ss21-derivierte-kategorien.*?\)': '[Derivierte Kategorien und Algebraische Geometrie]({{ site.baseurl }}/members/judith-ludwig/)',
            
            # 2020/21
            r'\[Elliptische Kurven\]\(.*?ws20-21-elliptische-kurven.*?\)': '[Elliptische Kurven]({{ site.baseurl }}/members/judith-ludwig/)',
            
            # 2020
            r'\[Algebra 2\]\(.*?ss20-algebra-2.*?\)': '[Algebra 2]({{ site.baseurl }}/members/julian-quast/)',
            r'\[Adische Räume II\]\(.*?ss20-adische-raeume-ii.*?\)': '[Adische Räume II]({{ site.baseurl }}/members/judith-ludwig/)',
            
            # 2019/20
            r'\[Affine algebraische Gruppen\]\(.*?ws19-20-affine-algebraische-gruppen.*?\)': '[Affine algebraische Gruppen]({{ site.baseurl }}/members/julian-quast/)',
            
            # 2019
            r'\[Bilinearformen und klassische Gruppen\]\(.*?ss19-bilinearformen.*?\)': '[Bilinearformen und klassische Gruppen]({{ site.baseurl }}/members/julian-quast/)',
            r'\[p-divisible Gruppen\]\(.*?ss19-p-divisible-gruppen.*?\)': '[p-divisible Gruppen]({{ site.baseurl }}/members/judith-ludwig/)',
        }

    def fix_teaching_index(self):
        """Fix the teaching index with correct links."""
        index_file = self.teaching_dir / "index.md"
        
        if not index_file.exists():
            print(f"Teaching index not found: {index_file}")
            return
        
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Apply all link replacements
        for old_pattern, new_link in self.link_replacements.items():
            content = re.sub(old_pattern, new_link, content)
        
        # Write the updated content
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Fixed teaching index with correct links: {index_file}")

    def run_fixes(self):
        """Run all the fixes."""
        print("🔧 FIXING TEACHING LINKS PROPERLY")
        print("="*50)
        
        # Fix teaching index with correct links
        self.fix_teaching_index()
        
        print("\n" + "="*50)
        print("TEACHING LINKS FIXED")
        print("="*50)
        print("Actions taken:")
        print("- Updated teaching index to use correct member page links")
        print("- Updated teaching index to use correct PDF links")
        print("- Removed references to non-existent teaching pages")

def main():
    project_root = "/home/victorrr/Downloads/hiwiwebsiteaddingnewstuff/ag-comp-arith-geom"
    
    fixer = TeachingLinksProperFixer(project_root)
    fixer.run_fixes()

if __name__ == "__main__":
    main() 