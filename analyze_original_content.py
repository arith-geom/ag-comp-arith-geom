#!/usr/bin/env python3
"""
Analyze Original Heidelberg Website Content

This script analyzes the original Heidelberg website content to determine
which teaching pages should be PDFs, actual content pages, or external links.
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple

class OriginalContentAnalyzer:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.teaching_dir = self.project_root / "_teaching"
        
        # Original Heidelberg website content analysis
        self.original_content = {
            # 2025
            "ss25-homological-algebra": {
                "type": "member_page",
                "original_link": "members/giacomo-hermes-ferraro/homological-algebra-seminar.html",
                "should_be": "Link to member page"
            },
            
            # 2024/25
            "ws24-commutative-algebra": {
                "type": "pdf",
                "original_link": "../../fileadmin/groups/arithgeo/comm_alg_announcement.pdf",
                "should_be": "PDF file"
            },
            "ws24-modularity": {
                "type": "member_page", 
                "original_link": "members/alireza-shavali/modularity-and-galois-representations.html",
                "should_be": "Link to member page"
            },
            "ws24-congruence-modules": {
                "type": "pdf",
                "original_link": "../../fileadmin/groups/arithgeo/GAUS-AG-WiSe2024-25-IKM-2024-12-11.pdf",
                "should_be": "PDF file"
            },
            
            # 2024
            "ss24-representation-theory": {
                "type": "member_page",
                "original_link": "members/oguz-gezmis/seminar-on-representation-theory-of-finite-groups-summer-semester-2024.html",
                "should_be": "Link to member page"
            },
            "ss24-shtukas": {
                "type": "pdf",
                "original_link": "../../fileadmin/groups/arithgeo/Seminar.pdf",
                "should_be": "PDF file"
            },
            "ss24-algebra-2": {
                "type": "html_file",
                "original_link": "../../fileadmin/groups/arithgeo/Algebra_2/home_A2.html",
                "should_be": "HTML file"
            },
            
            # 2023/24
            "ws23-24-quadratic-forms": {
                "type": "member_page",
                "original_link": "members/sriramcv/quadratic-forms.html",
                "should_be": "Link to member page"
            },
            "ws23-24-algebra-1": {
                "type": "html_file",
                "original_link": "../../fileadmin/groups/arithgeo/Algebra_1/home.html",
                "should_be": "HTML file"
            },
            "ws23-24-rigid-cocycles": {
                "type": "pdf",
                "original_link": "../../fileadmin/groups/arithgeo/RMCprogram_01.pdf",
                "should_be": "PDF file"
            },
            
            # 2023
            "ss23-lineare-algebra-2": {
                "type": "html_file",
                "original_link": "../../fileadmin/groups/arithgeo/LA2/home.html",
                "should_be": "HTML file"
            },
            "ss23-p-adic-numbers": {
                "type": "member_page",
                "original_link": "members/sriramcv/p-adic-numbers.html",
                "should_be": "Link to member page"
            },
            "ss23-vectorial-drinfeld": {
                "type": "external_pdf",
                "original_link": "https://crc326gaus.de/wp-content/uploads/2023/03/VectorialDrinfeldModForms.pdf",
                "should_be": "External PDF link"
            },
            
            # 2022/23
            "ws22-23-lineare-algebra-1": {
                "type": "html_file",
                "original_link": "../../fileadmin/groups/arithgeo/LA1/home.html",
                "should_be": "HTML file"
            },
            "ws22-23-affine-algebraic-groups": {
                "type": "member_page",
                "original_link": "members/sriramcv/affine-algebraic-groups.html",
                "should_be": "Link to member page"
            },
            
            # 2022
            "ss22-prime-numbers-cryptography": {
                "type": "member_page",
                "original_link": "members/barinder-banwait/prime-numbers-and-cryptography-proseminar.html",
                "should_be": "Link to member page"
            },
            
            # 2021/22
            "ws21-22-abelian-varieties": {
                "type": "member_page",
                "original_link": "members/barinder-banwait/abelian-varieties.html",
                "should_be": "Link to member page"
            },
            "ws21-22-etale-kohomologie": {
                "type": "no_link",
                "original_link": "No link provided",
                "should_be": "No content page needed"
            },
            "ws21-22-computational-number-theory": {
                "type": "pdf",
                "original_link": "../../fileadmin/groups/arithgeo/templates/data/Vorlesungen/program_comp_nt.pdf",
                "should_be": "PDF file"
            },
            "ws21-22-plectic-stark-heegner": {
                "type": "no_link",
                "original_link": "No link provided",
                "should_be": "No content page needed"
            },
            
            # 2021
            "ss21-derivierte-kategorien": {
                "type": "member_page",
                "original_link": "members/judith-ludwig/derivierte-kategorien.html",
                "should_be": "Link to member page"
            },
            "ss21-algebraische-geometrie-2": {
                "type": "html_file",
                "original_link": "../../fileadmin/groups/arithgeo/templates/data/Julian_Quast/AlgGeo_2/index.html",
                "should_be": "HTML file"
            },
            "ss21-higher-hida-theory": {
                "type": "no_link",
                "original_link": "No link provided",
                "should_be": "No content page needed"
            },
            
            # 2020/21
            "ws20-21-elliptische-kurven": {
                "type": "member_page",
                "original_link": "members/judith-ludwig/seminar-elliptische-kurven.html",
                "should_be": "Link to member page"
            },
            "ws20-21-algebraische-geometrie-1": {
                "type": "html_file",
                "original_link": "../../fileadmin/groups/arithgeo/templates/data/Julian_Quast/AlgGeo_1/index.html",
                "should_be": "HTML file"
            },
            
            # 2020
            "ss20-algebra-2": {
                "type": "member_page",
                "original_link": "home/members/julian-quast/2020algebra2",
                "should_be": "Link to member page"
            },
            "ss20-adische-raeume-ii": {
                "type": "member_page",
                "original_link": "members/judith-ludwig/adischeraeumeii.html",
                "should_be": "Link to member page"
            },
            
            # 2019/20
            "ws19-20-algebra-1": {
                "type": "broken_link",
                "original_link": "https://typo.iwr.uni-heidelberg.de/https//typoiwruni-heidelbergde/fileadmin/groups/arithgeo/templates/data/judith-ludwig/algebra1/indexhtml",
                "should_be": "Broken link - needs fixing"
            },
            "ws19-20-affine-algebraische-gruppen": {
                "type": "member_page",
                "original_link": "members/julian-quast/seminar-affine-algebraische-gruppen.html",
                "should_be": "Link to member page"
            },
            "ws19-20-hauptseminar": {
                "type": "no_link",
                "original_link": "No link provided",
                "should_be": "No content page needed"
            },
            
            # 2019
            "ss19-bilinearformen": {
                "type": "member_page",
                "original_link": "members/julian-quast/proseminar-bilinearformen-und-klassische-gruppen.html",
                "should_be": "Link to member page"
            },
            "ss19-kompatible-systeme": {
                "type": "member_page",
                "original_link": "members/gebhard-boeckle/kompatible-systeme-von-galoisdarstellungen.html",
                "should_be": "Link to member page"
            },
            "ss19-p-divisible-gruppen": {
                "type": "member_page",
                "original_link": "members/judith-ludwig/p-divisible-gruppen.html",
                "should_be": "Link to member page"
            },
            "ss19-hauptseminar": {
                "type": "pdf",
                "original_link": "../../fileadmin/groups/arithgeo/templates/data/Hauptseminare/Programm_la-courbe_SoSe19.pdf",
                "should_be": "PDF file"
            }
        }

    def analyze_current_pages(self):
        """Analyze what pages currently exist and what they should be."""
        print("Analyzing current teaching pages vs original content...")
        print("="*60)
        
        current_pages = list(self.teaching_dir.glob("*.md"))
        current_page_names = [p.stem for p in current_pages if p.stem != "index" and p.stem != "past-teaching" and p.stem != "heidelberg-teaching-archive"]
        
        issues = []
        correct_pages = []
        
        for page_name in current_page_names:
            if page_name in self.original_content:
                original_info = self.original_content[page_name]
                current_file = self.teaching_dir / f"{page_name}.md"
                
                print(f"\n📄 {page_name}:")
                print(f"   Current: Content page")
                print(f"   Should be: {original_info['should_be']}")
                print(f"   Original link: {original_info['original_link']}")
                
                if original_info['type'] in ['pdf', 'html_file', 'external_pdf', 'no_link', 'broken_link']:
                    issues.append({
                        'page': page_name,
                        'current_type': 'content_page',
                        'should_be': original_info['type'],
                        'original_link': original_info['original_link'],
                        'file_path': current_file
                    })
                else:
                    correct_pages.append(page_name)
            else:
                print(f"\n❓ {page_name}: Not found in original content")
        
        return issues, correct_pages

    def generate_fix_plan(self, issues: List[Dict]):
        """Generate a plan to fix the issues."""
        print("\n" + "="*60)
        print("FIX PLAN")
        print("="*60)
        
        pdf_pages = [i for i in issues if i['should_be'] == 'pdf']
        html_pages = [i for i in issues if i['should_be'] == 'html_file']
        external_pdfs = [i for i in issues if i['should_be'] == 'external_pdf']
        no_link_pages = [i for i in issues if i['should_be'] == 'no_link']
        broken_links = [i for i in issues if i['should_be'] == 'broken_link']
        
        print(f"\n📊 Summary:")
        print(f"   PDF pages to create: {len(pdf_pages)}")
        print(f"   HTML files to create: {len(html_pages)}")
        print(f"   External PDF links: {len(external_pdfs)}")
        print(f"   Pages to remove: {len(no_link_pages)}")
        print(f"   Broken links to fix: {len(broken_links)}")
        
        if pdf_pages:
            print(f"\n📄 PDF Pages to create:")
            for issue in pdf_pages:
                print(f"   - {issue['page']}: {issue['original_link']}")
        
        if html_pages:
            print(f"\n🌐 HTML Files to create:")
            for issue in html_pages:
                print(f"   - {issue['page']}: {issue['original_link']}")
        
        if external_pdfs:
            print(f"\n🔗 External PDF links:")
            for issue in external_pdfs:
                print(f"   - {issue['page']}: {issue['original_link']}")
        
        if no_link_pages:
            print(f"\n🗑️ Pages to remove:")
            for issue in no_link_pages:
                print(f"   - {issue['page']}")
        
        if broken_links:
            print(f"\n⚠️ Broken links to fix:")
            for issue in broken_links:
                print(f"   - {issue['page']}: {issue['original_link']}")

    def run_analysis(self):
        """Run the complete analysis."""
        print("🔍 ANALYZING ORIGINAL HEIDELBERG WEBSITE CONTENT")
        print("="*60)
        
        issues, correct_pages = self.analyze_current_pages()
        
        print(f"\n✅ Correct pages ({len(correct_pages)}):")
        for page in correct_pages:
            print(f"   - {page}")
        
        self.generate_fix_plan(issues)
        
        return issues, correct_pages

def main():
    project_root = "/home/victorrr/Downloads/hiwiwebsiteaddingnewstuff/ag-comp-arith-geom"
    
    analyzer = OriginalContentAnalyzer(project_root)
    issues, correct_pages = analyzer.run_analysis()
    
    print(f"\n📋 Total issues found: {len(issues)}")
    print(f"📋 Correct pages: {len(correct_pages)}")

if __name__ == "__main__":
    main() 