#!/usr/bin/env python3
"""
Heidelberg University Arithmetic Geometry Teaching Page Scraper
Downloads all PDFs and content from the teaching page
"""

import os
import requests
import re
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import time
import json
from pathlib import Path

class HeidelbergScraper:
    def __init__(self, base_url="https://typo.iwr.uni-heidelberg.de"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.downloaded_files = []
        self.failed_downloads = []
        
    def download_file(self, url, local_path):
        """Download a file from URL to local path"""
        try:
            print(f"Downloading: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            
            with open(local_path, 'wb') as f:
                f.write(response.content)
            
            self.downloaded_files.append({
                'url': url,
                'local_path': local_path,
                'size': len(response.content)
            })
            print(f"✓ Downloaded: {local_path} ({len(response.content)} bytes)")
            return True
            
        except Exception as e:
            print(f"✗ Failed to download {url}: {e}")
            self.failed_downloads.append({
                'url': url,
                'local_path': local_path,
                'error': str(e)
            })
            return False
    
    def extract_links_from_html(self, html_content):
        """Extract all links from HTML content"""
        soup = BeautifulSoup(html_content, 'html.parser')
        links = []
        
        # Find all links
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            text = link.get_text(strip=True)
            
            # Skip empty links
            if not href or href.startswith('#'):
                continue
                
            # Make relative URLs absolute
            if href.startswith('/'):
                full_url = urljoin(self.base_url, href)
            elif href.startswith('http'):
                full_url = href
            else:
                full_url = urljoin(self.base_url, href)
            
            links.append({
                'url': full_url,
                'text': text,
                'element': link
            })
        
        return links
    
    def scrape_teaching_page(self):
        """Scrape the main teaching page"""
        teaching_url = "https://typo.iwr.uni-heidelberg.de/groups/arith-geom/teaching.html"
        
        print(f"Scraping teaching page: {teaching_url}")
        response = self.session.get(teaching_url)
        response.raise_for_status()
        
        # Save the main page
        with open('_teaching/heidelberg_teaching_page.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        # Extract all links
        links = self.extract_links_from_html(response.text)
        
        # Filter for PDFs and other documents
        pdf_links = []
        other_links = []
        
        for link in links:
            url = link['url']
            if url.lower().endswith('.pdf'):
                pdf_links.append(link)
            elif any(ext in url.lower() for ext in ['.html', '.htm', '.txt', '.doc', '.docx']):
                other_links.append(link)
        
        print(f"Found {len(pdf_links)} PDF links and {len(other_links)} other document links")
        
        # Download PDFs
        for link in pdf_links:
            url = link['url']
            filename = os.path.basename(urlparse(url).path)
            if not filename:
                filename = f"document_{len(self.downloaded_files)}.pdf"
            
            local_path = f"_teaching/pdfs/{filename}"
            self.download_file(url, local_path)
            time.sleep(1)  # Be respectful to the server
        
        # Download other documents
        for link in other_links:
            url = link['url']
            filename = os.path.basename(urlparse(url).path)
            if not filename:
                filename = f"document_{len(self.downloaded_files)}.html"
            
            local_path = f"_teaching/documents/{filename}"
            self.download_file(url, local_path)
            time.sleep(1)
        
        return links
    
    def scrape_specific_pdfs(self):
        """Scrape specific PDFs mentioned in the content"""
        specific_pdfs = [
            "https://typo.iwr.uni-heidelberg.de/fileadmin/groups/arithgeo/comm_alg_announcement.pdf",
            "https://typo.iwr.uni-heidelberg.de/fileadmin/groups/arithgeo/GAUS-AG-WiSe2024-25-IKM-2024-12-11.pdf",
            "https://typo.iwr.uni-heidelberg.de/fileadmin/groups/arithgeo/Seminar.pdf",
            "https://typo.iwr.uni-heidelberg.de/fileadmin/groups/arithgeo/RMCprogram_01.pdf",
            "https://typo.iwr.uni-heidelberg.de/fileadmin/groups/arithgeo/templates/data/Vorlesungen/program_comp_nt.pdf",
            "https://typo.iwr.uni-heidelberg.de/fileadmin/groups/arithgeo/templates/data/Hauptseminare/Programm_la-courbe_SoSe19.pdf",
            "https://typo.iwr.uni-heidelberg.de/fileadmin/groups/arithgeo/templates/data/Judith_Ludwig/Programm_GL2_WS1819.pdf",
            "https://typo.iwr.uni-heidelberg.de/fileadmin/groups/arithgeo/templates/data/Hauptseminare/WS1819_lokale_G-shtukas.pdf",
            "https://typo.iwr.uni-heidelberg.de/fileadmin/groups/arithgeo/templates/data/Seminare/Ankuendigung-Modularity.pdf",
            "https://typo.iwr.uni-heidelberg.de/fileadmin/groups/arithgeo/templates/data/Vorlesungen/Bruhat-Tits.pdf",
            "https://typo.iwr.uni-heidelberg.de/fileadmin/groups/arithgeo/templates/data/Vorlesungen/DarstellungenUndInvarianten_II_SS2015.pdf",
            "https://typo.iwr.uni-heidelberg.de/fileadmin/groups/arithgeo/templates/data/Vorlesungen/Lenny_Taelman_s_body_of_work_on_Drinfeld_modules.pdf",
            "https://typo.iwr.uni-heidelberg.de/fileadmin/groups/arithgeo/templates/data/Vorlesungen/Modulbeschreibung-AutomorpheFormen.pdf",
            "https://typo.iwr.uni-heidelberg.de/fileadmin/groups/arithgeo/templates/data/Vorlesungen/DarstellungenUndInvarianten_WS201415.pdf",
            "https://typo.iwr.uni-heidelberg.de/fileadmin/groups/arithgeo/templates/data/Hauptseminare/WS201415_RecentBSD.pdf",
            "https://typo.iwr.uni-heidelberg.de/fileadmin/groups/arithgeo/templates/data/Seminare/AffineAlgebraischeGruppen_WS2012-13_Programm.pdf",
            "https://typo.iwr.uni-heidelberg.de/fileadmin/groups/arithgeo/templates/data/Hauptseminare/WS1213_TranscendencePosChar.pdf",
            "https://typo.iwr.uni-heidelberg.de/fileadmin/groups/arithgeo/templates/data/Hauptseminare/AutomorphicFormsAndRepresentationsForGL2_CentelegheCervinoChekaru.pdf",
            "https://typo.iwr.uni-heidelberg.de/fileadmin/groups/arithgeo/templates/data/Hauptseminare/BorcherdsProducts_SeminarProgram_WS2011-12_G3.pdf",
            "https://typo.iwr.uni-heidelberg.de/fileadmin/groups/arithgeo/templates/data/Seminare/Seminarprogramm_IkedaLift_WS2011-12_BouganisCervinoKasten.pdf",
            "https://typo.iwr.uni-heidelberg.de/fileadmin/groups/arithgeo/templates/data/Seminare/qF_Programm_SS2011.pdf"
        ]
        
        print(f"Downloading {len(specific_pdfs)} specific PDFs...")
        
        for url in specific_pdfs:
            filename = os.path.basename(urlparse(url).path)
            local_path = f"_teaching/pdfs/{filename}"
            self.download_file(url, local_path)
            time.sleep(1)
    
    def generate_report(self):
        """Generate a report of downloaded files"""
        report = {
            'downloaded_files': self.downloaded_files,
            'failed_downloads': self.failed_downloads,
            'summary': {
                'total_downloaded': len(self.downloaded_files),
                'total_failed': len(self.failed_downloads),
                'total_size': sum(f['size'] for f in self.downloaded_files)
            }
        }
        
        with open('_teaching/download_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n=== DOWNLOAD REPORT ===")
        print(f"Successfully downloaded: {len(self.downloaded_files)} files")
        print(f"Failed downloads: {len(self.failed_downloads)} files")
        print(f"Total size: {sum(f['size'] for f in self.downloaded_files)} bytes")
        
        if self.failed_downloads:
            print(f"\nFailed downloads:")
            for failed in self.failed_downloads:
                print(f"  - {failed['url']}: {failed['error']}")

def main():
    scraper = HeidelbergScraper()
    
    # Create directories
    os.makedirs('_teaching/pdfs', exist_ok=True)
    os.makedirs('_teaching/documents', exist_ok=True)
    
    # Scrape the teaching page
    scraper.scrape_teaching_page()
    
    # Download specific PDFs
    scraper.scrape_specific_pdfs()
    
    # Generate report
    scraper.generate_report()

if __name__ == "__main__":
    main() 