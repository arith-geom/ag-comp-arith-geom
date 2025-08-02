#!/usr/bin/env python3
"""
Final Fix for Heidelberg Teaching Archive

This script fixes the remaining teaching page links in the archive file.
"""

import re
from pathlib import Path

class ArchiveFinalFixer:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.teaching_dir = self.project_root / "_teaching"

    def fix_archive_file(self):
        """Fix the Heidelberg teaching archive file."""
        archive_file = self.teaching_dir / "heidelberg-teaching-archive.md"
        
        if not archive_file.exists():
            print(f"Archive file not found: {archive_file}")
            return
        
        with open(archive_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace specific teaching page links with correct links
        replacements = [
            # 2025
            ('{{ site.baseurl }}/teaching/ss25-homological-algebra/', '{{ site.baseurl }}/members/giacomo-hermes-ferraro/'),
            
            # 2024/25
            ('{{ site.baseurl }}/teaching/ws24-commutative-algebra/', '/assets/uploads/comm_alg_announcement.pdf'),
            ('{{ site.baseurl }}/teaching/ws24-modularity/', '{{ site.baseurl }}/members/alireza-shavali/'),
            ('{{ site.baseurl }}/teaching/ws24-congruence-modules/', '/assets/uploads/GAUS-AG-WiSe2024-25-IKM-2024-12-11.pdf'),
            
            # 2024
            ('{{ site.baseurl }}/teaching/ss24-representation-theory/', '{{ site.baseurl }}/members/oguz-gezmis/'),
            
            # 2023/24
            ('{{ site.baseurl }}/teaching/ws23-24-quadratic-forms/', '{{ site.baseurl }}/members/sriramcv/'),
            
            # 2023
            ('{{ site.baseurl }}/teaching/ss23-p-adic-numbers/', '{{ site.baseurl }}/members/sriramcv/'),
            
            # 2022/23
            ('{{ site.baseurl }}/teaching/ws22-23-affine-algebraic-groups/', '{{ site.baseurl }}/members/sriramcv/'),
            
            # 2022
            ('{{ site.baseurl }}/teaching/ss22-prime-numbers-cryptography/', '{{ site.baseurl }}/members/barinder-banwait/'),
            
            # 2021/22
            ('{{ site.baseurl }}/teaching/ws21-22-abelian-varieties/', '{{ site.baseurl }}/members/barinder-banwait/'),
            
            # 2021
            ('{{ site.baseurl }}/teaching/ss21-derivierte-kategorien/', '{{ site.baseurl }}/members/judith-ludwig/'),
            
            # 2020/21
            ('{{ site.baseurl }}/teaching/ws20-21-elliptische-kurven/', '{{ site.baseurl }}/members/judith-ludwig/'),
            
            # 2020
            ('{{ site.baseurl }}/teaching/ss20-algebra-2/', '{{ site.baseurl }}/members/julian-quast/'),
            ('{{ site.baseurl }}/teaching/ss20-adische-raeume-ii/', '{{ site.baseurl }}/members/judith-ludwig/'),
            
            # 2019/20
            ('{{ site.baseurl }}/teaching/ws19-20-affine-algebraische-gruppen/', '{{ site.baseurl }}/members/julian-quast/'),
            
            # 2019
            ('{{ site.baseurl }}/teaching/ss19-bilinearformen/', '{{ site.baseurl }}/members/julian-quast/'),
            ('{{ site.baseurl }}/teaching/ss19-p-divisible-gruppen/', '{{ site.baseurl }}/members/judith-ludwig/'),
        ]
        
        # Apply all replacements
        for old_url, new_url in replacements:
            content = content.replace(old_url, new_url)
        
        # Write the updated content
        with open(archive_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Fixed Heidelberg teaching archive: {archive_file}")

    def run_fixes(self):
        """Run all the fixes."""
        print("🔧 FINAL FIX FOR HEIDELBERG TEACHING ARCHIVE")
        print("="*50)
        
        # Fix archive file with correct links
        self.fix_archive_file()
        
        print("\n" + "="*50)
        print("ARCHIVE FINAL FIX COMPLETE")
        print("="*50)
        print("Actions taken:")
        print("- Replaced all teaching page links with correct member page links")
        print("- Replaced all teaching page links with correct PDF links")
        print("- All links should now point to existing pages")

def main():
    project_root = "/home/victorrr/Downloads/hiwiwebsiteaddingnewstuff/ag-comp-arith-geom"
    
    fixer = ArchiveFinalFixer(project_root)
    fixer.run_fixes()

if __name__ == "__main__":
    main() 