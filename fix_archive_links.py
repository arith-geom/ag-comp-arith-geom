#!/usr/bin/env python3
"""
Fix Heidelberg Teaching Archive Links

This script fixes the Heidelberg teaching archive file by updating it to use
the correct member page links and PDF links instead of old teaching page links.
"""

import re
from pathlib import Path

class ArchiveLinksFixer:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.teaching_dir = self.project_root / "_teaching"
        
        # Link replacements for the archive file
        self.archive_link_replacements = {
            # 2025
            r'\[Homological Algebra\]\(.*?ss25-homological-algebra.*?\)': '[Homological Algebra]({{ site.baseurl }}/members/giacomo-hermes-ferraro/)',
            
            # 2024/25
            r'\[Commutative Algebra\]\(.*?ws24-commutative-algebra.*?\)': '[Commutative Algebra](/assets/uploads/comm_alg_announcement.pdf)',
            r'\[Modularity and Galois Representations\]\(.*?ws24-modularity.*?\)': '[Modularity and Galois Representations]({{ site.baseurl }}/members/alireza-shavali/)',
            r'\[Congruence Modules and the Wiles–Lenstra–Diamond Numerical Criterion in Higher Codimension\]\(.*?ws24-congruence-modules.*?\)': '[Congruence Modules and the Wiles–Lenstra–Diamond Numerical Criterion in Higher Codimension](/assets/uploads/GAUS-AG-WiSe2024-25-IKM-2024-12-11.pdf)',
            
            # 2024
            r'\[Representation theory of finite groups\]\(.*?ss24-representation-theory.*?\)': '[Representation theory of finite groups]({{ site.baseurl }}/members/oguz-gezmis/)',
            
            # 2023/24
            r'\[Quadratic forms\]\(.*?ws23-24-quadratic-forms.*?\)': '[Quadratic forms]({{ site.baseurl }}/members/sriramcv/)',
            
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

    def fix_archive_file(self):
        """Fix the Heidelberg teaching archive file."""
        archive_file = self.teaching_dir / "heidelberg-teaching-archive.md"
        
        if not archive_file.exists():
            print(f"Archive file not found: {archive_file}")
            return
        
        with open(archive_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Apply all link replacements
        for old_pattern, new_link in self.archive_link_replacements.items():
            content = re.sub(old_pattern, new_link, content)
        
        # Write the updated content
        with open(archive_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Fixed Heidelberg teaching archive: {archive_file}")

    def run_fixes(self):
        """Run all the fixes."""
        print("🔧 FIXING HEIDELBERG TEACHING ARCHIVE LINKS")
        print("="*50)
        
        # Fix archive file with correct links
        self.fix_archive_file()
        
        print("\n" + "="*50)
        print("ARCHIVE LINKS FIXED")
        print("="*50)
        print("Actions taken:")
        print("- Updated Heidelberg teaching archive to use correct member page links")
        print("- Updated Heidelberg teaching archive to use correct PDF links")
        print("- Removed references to non-existent teaching pages")

def main():
    project_root = "/home/victorrr/Downloads/hiwiwebsiteaddingnewstuff/ag-comp-arith-geom"
    
    fixer = ArchiveLinksFixer(project_root)
    fixer.run_fixes()

if __name__ == "__main__":
    main() 