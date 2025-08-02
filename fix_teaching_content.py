#!/usr/bin/env python3
"""
Fix Teaching Content Based on Original Heidelberg Website

This script fixes the teaching content by:
1. Updating the teaching index to use correct links (member pages and PDFs)
2. Removing unnecessary content pages
3. Creating proper PDF links where needed
"""

import re
from pathlib import Path
from typing import Dict, List

class TeachingContentFixer:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.teaching_dir = self.project_root / "_teaching"
        self.assets_dir = self.project_root / "assets"
        
        # Mapping of what each page should actually be
        self.correct_links = {
            # 2025
            "ss25-homological-algebra": {
                "type": "member_link",
                "url": "{{ site.baseurl }}/members/giacomo-hermes-ferraro/",
                "text": "Homological Algebra"
            },
            
            # 2024/25
            "ws24-commutative-algebra": {
                "type": "pdf",
                "url": "/assets/uploads/comm_alg_announcement.pdf",
                "text": "Commutative Algebra"
            },
            "ws24-modularity": {
                "type": "member_link",
                "url": "{{ site.baseurl }}/members/alireza-shavali/",
                "text": "Modularity and Galois Representations"
            },
            "ws24-congruence-modules": {
                "type": "pdf",
                "url": "/assets/uploads/GAUS-AG-WiSe2024-25-IKM-2024-12-11.pdf",
                "text": "Congruence Modules and the Wiles–Lenstra–Diamond Numerical Criterion in Higher Codimension"
            },
            
            # 2024
            "ss24-representation-theory": {
                "type": "member_link",
                "url": "{{ site.baseurl }}/members/oguz-gezmis/",
                "text": "Representation theory of finite groups"
            },
            "ss24-algebra-2": {
                "type": "member_link",
                "url": "{{ site.baseurl }}/members/alireza-shavali/",
                "text": "Algebra 2"
            },
            
            # 2023/24
            "ws23-24-quadratic-forms": {
                "type": "member_link",
                "url": "{{ site.baseurl }}/members/sriramcv/",
                "text": "Quadratic forms"
            },
            "ws23-24-algebra-1": {
                "type": "member_link",
                "url": "{{ site.baseurl }}/members/alireza-shavali/",
                "text": "Algebra 1"
            },
            
            # 2023
            "ss23-p-adic-numbers": {
                "type": "member_link",
                "url": "{{ site.baseurl }}/members/sriramcv/",
                "text": "p-adic numbers"
            },
            
            # 2022/23
            "ws22-23-affine-algebraic-groups": {
                "type": "member_link",
                "url": "{{ site.baseurl }}/members/sriramcv/",
                "text": "Affine Algebraic Groups"
            },
            
            # 2022
            "ss22-prime-numbers-cryptography": {
                "type": "member_link",
                "url": "{{ site.baseurl }}/members/barinder-banwait/",
                "text": "Prime numbers and Cryptography"
            },
            
            # 2021/22
            "ws21-22-abelian-varieties": {
                "type": "member_link",
                "url": "{{ site.baseurl }}/members/barinder-banwait/",
                "text": "Abelian Varieties"
            },
            
            # 2021
            "ss21-derivierte-kategorien": {
                "type": "member_link",
                "url": "{{ site.baseurl }}/members/judith-ludwig/",
                "text": "Derivierte Kategorien und Algebraische Geometrie"
            },
            
            # 2020/21
            "ws20-21-elliptische-kurven": {
                "type": "member_link",
                "url": "{{ site.baseurl }}/members/judith-ludwig/",
                "text": "Elliptische Kurven"
            },
            
            # 2020
            "ss20-algebra-2": {
                "type": "member_link",
                "url": "{{ site.baseurl }}/members/julian-quast/",
                "text": "Algebra 2"
            },
            "ss20-adische-raeume-ii": {
                "type": "member_link",
                "url": "{{ site.baseurl }}/members/judith-ludwig/",
                "text": "Adische Räume II"
            },
            
            # 2019/20
            "ws19-20-affine-algebraische-gruppen": {
                "type": "member_link",
                "url": "{{ site.baseurl }}/members/julian-quast/",
                "text": "Affine algebraische Gruppen"
            },
            
            # 2019
            "ss19-bilinearformen": {
                "type": "member_link",
                "url": "{{ site.baseurl }}/members/julian-quast/",
                "text": "Bilinearformen und klassische Gruppen"
            },
            "ss19-p-divisible-gruppen": {
                "type": "member_link",
                "url": "{{ site.baseurl }}/members/judith-ludwig/",
                "text": "p-divisible Gruppen"
            }
        }

    def update_teaching_index(self):
        """Update the teaching index to use correct links."""
        index_file = self.teaching_dir / "index.md"
        
        if not index_file.exists():
            print(f"Teaching index not found: {index_file}")
            return
        
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update each link to use the correct URL
        for page_name, link_info in self.correct_links.items():
            old_pattern = f'\\[([^\\]]*)\\]\\({{ site\\.baseurl }}/teaching/{page_name}/\\)'
            new_link = f'[{link_info["text"]}]({link_info["url"]})'
            
            content = re.sub(old_pattern, new_link, content)
        
        # Write the updated content
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Updated teaching index with correct links: {index_file}")

    def remove_unnecessary_pages(self):
        """Remove the content pages that should be links instead."""
        pages_to_remove = []
        
        for page_name in self.correct_links.keys():
            page_file = self.teaching_dir / f"{page_name}.md"
            if page_file.exists():
                pages_to_remove.append(page_file)
        
        print(f"\nRemoving {len(pages_to_remove)} unnecessary content pages:")
        for page_file in pages_to_remove:
            try:
                page_file.unlink()
                print(f"   Removed: {page_file.name}")
            except Exception as e:
                print(f"   Error removing {page_file.name}: {e}")

    def create_pdf_placeholders(self):
        """Create placeholder PDF files in assets directory."""
        pdfs_to_create = {
            "comm_alg_announcement.pdf": "Commutative Algebra Announcement",
            "GAUS-AG-WiSe2024-25-IKM-2024-12-11.pdf": "GAUS-AG Winter Semester 2024-25 IKM"
        }
        
        # Ensure assets/uploads directory exists
        uploads_dir = self.assets_dir / "uploads"
        uploads_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"\nCreating PDF placeholders in {uploads_dir}:")
        for pdf_name, description in pdfs_to_create.items():
            pdf_path = uploads_dir / pdf_name
            if not pdf_path.exists():
                # Create a placeholder text file (since we can't create actual PDFs)
                placeholder_content = f"""# {description}

This is a placeholder for the PDF file: {pdf_name}

**Note:** This file should be replaced with the actual PDF from the original Heidelberg website.

Original location: {pdf_name}
"""
                with open(pdf_path, 'w', encoding='utf-8') as f:
                    f.write(placeholder_content)
                print(f"   Created placeholder: {pdf_name}")
            else:
                print(f"   Already exists: {pdf_name}")

    def run_fixes(self):
        """Run all the fixes."""
        print("🔧 FIXING TEACHING CONTENT BASED ON ORIGINAL WEBSITE")
        print("="*60)
        
        # Update teaching index with correct links
        self.update_teaching_index()
        
        # Remove unnecessary content pages
        self.remove_unnecessary_pages()
        
        # Create PDF placeholders
        self.create_pdf_placeholders()
        
        print("\n" + "="*60)
        print("TEACHING CONTENT FIXED")
        print("="*60)
        print("Actions taken:")
        print("- Updated teaching index to use correct member page links")
        print("- Updated teaching index to use correct PDF links")
        print("- Removed unnecessary content pages")
        print("- Created PDF placeholders in assets/uploads/")
        print("\nNext steps:")
        print("1. Replace PDF placeholders with actual PDF files")
        print("2. Verify all member page links work correctly")
        print("3. Test the website to ensure proper functionality")

def main():
    project_root = "/home/victorrr/Downloads/hiwiwebsiteaddingnewstuff/ag-comp-arith-geom"
    
    fixer = TeachingContentFixer(project_root)
    fixer.run_fixes()

if __name__ == "__main__":
    main() 