#!/usr/bin/env python3
"""
Focused Site Scraper for Heidelberg AG Computational Arithmetic Geometry Website
Extracts content only from the specific arith-geom group pages, not external sites.
"""

import requests
from bs4 import BeautifulSoup
import re
import os
import time
import json
from urllib.parse import urljoin, urlparse
import yaml
from pathlib import Path

class HeidelbergScraper:
    def __init__(self, base_url="https://typo.iwr.uni-heidelberg.de/groups/arith-geom/"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.visited_urls = set()
        self.content_data = {
            'pages': {},
            'members': [],
            'publications': [],
            'research': [],
            'teaching': [],
            'links': [],
            'news': []
        }
        
    def get_page_content(self, url):
        """Fetch page content with error handling"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def extract_text_content(self, soup):
        """Extract clean text content from BeautifulSoup object"""
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text and clean it up
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        return text
    
    def extract_links(self, soup, base_url):
        """Extract only links within the same arith-geom group"""
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(base_url, href)
            
            # Only include links within the same arith-geom group
            if 'groups/arith-geom' in full_url:
                links.append({
                    'text': link.get_text(strip=True),
                    'url': full_url,
                    'title': link.get('title', '')
                })
        return links
    
    def scrape_members_page(self, url):
        """Scrape the members page specifically"""
        print(f"Scraping members page: {url}")
        content = self.get_page_content(url)
        if not content:
            return []
        
        soup = BeautifulSoup(content, 'html.parser')
        members = []
        
        # Look for member sections
        sections = soup.find_all(['h3', 'h4', 'h5'])
        
        current_section = None
        for section in sections:
            section_text = section.get_text(strip=True).lower()
            
            if 'head' in section_text:
                current_section = 'head'
            elif 'secretary' in section_text:
                current_section = 'secretary'
            elif 'members' in section_text:
                current_section = 'members'
            elif 'former' in section_text:
                current_section = 'former'
            
            if current_section:
                # Find the next list or paragraph
                next_elem = section.find_next_sibling()
                while next_elem and next_elem.name not in ['ul', 'ol', 'p']:
                    next_elem = next_elem.find_next_sibling()
                
                if next_elem and next_elem.name in ['ul', 'ol']:
                    for item in next_elem.find_all('li'):
                        member_text = item.get_text(strip=True)
                        if member_text:
                            members.append({
                                'name': member_text,
                                'role': current_section,
                                'section': current_section
                            })
        
        return members
    
    def scrape_publications_page(self, url):
        """Scrape the publications page specifically"""
        print(f"Scraping publications page: {url}")
        content = self.get_page_content(url)
        if not content:
            return []
        
        soup = BeautifulSoup(content, 'html.parser')
        publications = []
        
        # Extract all text content
        text_content = self.extract_text_content(soup)
        
        # Look for publication sections
        sections = soup.find_all(['h2', 'h3', 'h4'])
        
        for section in sections:
            section_text = section.get_text(strip=True)
            if 'publication' in section_text.lower() or 'software' in section_text.lower():
                # Get content after this section
                content_after = []
                next_elem = section.find_next_sibling()
                while next_elem and next_elem.name not in ['h2', 'h3', 'h4']:
                    if next_elem.name in ['p', 'ul', 'ol']:
                        content_after.append(next_elem.get_text(strip=True))
                    next_elem = next_elem.find_next_sibling()
                
                publications.append({
                    'title': section_text,
                    'content': ' '.join(content_after)
                })
        
        return publications
    
    def scrape_research_page(self, url):
        """Scrape the research page specifically"""
        print(f"Scraping research page: {url}")
        content = self.get_page_content(url)
        if not content:
            return []
        
        soup = BeautifulSoup(content, 'html.parser')
        research_areas = []
        
        # Look for research themes
        sections = soup.find_all(['h2', 'h3', 'h4'])
        
        for section in sections:
            section_text = section.get_text(strip=True)
            if 'research' in section_text.lower() or 'theme' in section_text.lower():
                # Get content after this section
                content_after = []
                next_elem = section.find_next_sibling()
                while next_elem and next_elem.name not in ['h2', 'h3', 'h4']:
                    if next_elem.name in ['p', 'ul', 'ol']:
                        content_after.append(next_elem.get_text(strip=True))
                    next_elem = next_elem.find_next_sibling()
                
                research_areas.append({
                    'title': section_text,
                    'content': ' '.join(content_after)
                })
        
        return research_areas
    
    def scrape_teaching_page(self, url):
        """Scrape the teaching page specifically"""
        print(f"Scraping teaching page: {url}")
        content = self.get_page_content(url)
        if not content:
            return []
        
        soup = BeautifulSoup(content, 'html.parser')
        courses = []
        
        # Look for semester sections
        sections = soup.find_all(['h2', 'h3', 'h4'])
        
        for section in sections:
            section_text = section.get_text(strip=True)
            if any(term in section_text.lower() for term in ['summer', 'winter', 'term', 'semester']):
                # Get content after this section
                content_after = []
                next_elem = section.find_next_sibling()
                while next_elem and next_elem.name not in ['h2', 'h3', 'h4']:
                    if next_elem.name in ['p', 'ul', 'ol']:
                        content_after.append(next_elem.get_text(strip=True))
                    next_elem = next_elem.find_next_sibling()
                
                courses.append({
                    'semester': section_text,
                    'content': ' '.join(content_after)
                })
        
        return courses
    
    def scrape_page(self, url):
        """Scrape a single page and extract all content"""
        if url in self.visited_urls:
            return
        
        self.visited_urls.add(url)
        print(f"Scraping: {url}")
        
        content = self.get_page_content(url)
        if not content:
            return
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Extract page title
        title = soup.find('title')
        title_text = title.get_text(strip=True) if title else "Untitled"
        
        # Extract main content
        main_content = soup.find('main') or soup.find('body')
        if main_content:
            text_content = self.extract_text_content(main_content)
        else:
            text_content = self.extract_text_content(soup)
        
        # Extract links (only within arith-geom group)
        links = self.extract_links(soup, url)
        
        # Store page data
        page_data = {
            'url': url,
            'title': title_text,
            'content': text_content,
            'links': links
        }
        
        # Categorize based on URL
        if 'members' in url:
            self.content_data['members'].append(page_data)
        elif 'publications' in url:
            self.content_data['publications'].append(page_data)
        elif 'research' in url:
            self.content_data['research'].append(page_data)
        elif 'teaching' in url:
            self.content_data['teaching'].append(page_data)
        elif 'links' in url:
            self.content_data['links'].append(page_data)
        elif 'news' in url or 'index' in url:
            self.content_data['news'].append(page_data)
        else:
            self.content_data['pages'][url] = page_data
        
        # Find more links to scrape (only within arith-geom group)
        for link in links:
            link_url = link['url']
            if link_url not in self.visited_urls and 'groups/arith-geom' in link_url:
                time.sleep(1)  # Be respectful
                self.scrape_page(link_url)
    
    def scrape_all(self):
        """Scrape all pages starting from the base URL"""
        print("Starting focused scrape of Heidelberg arith-geom website...")
        
        # Only scrape the main arith-geom pages
        main_pages = [
            self.base_url,
            self.base_url + "members.html",
            self.base_url + "publications.html",
            self.base_url + "research.html",
            self.base_url + "teaching.html",
            self.base_url + "links.html",
            self.base_url + "contact.html"
        ]
        
        for page in main_pages:
            self.scrape_page(page)
            time.sleep(2)  # Be respectful to the server
        
        # Also scrape specific content types
        if self.base_url + "members.html" not in self.visited_urls:
            members = self.scrape_members_page(self.base_url + "members.html")
            self.content_data['members'].extend(members)
        
        if self.base_url + "publications.html" not in self.visited_urls:
            publications = self.scrape_publications_page(self.base_url + "publications.html")
            self.content_data['publications'].extend(publications)
        
        if self.base_url + "research.html" not in self.visited_urls:
            research = self.scrape_research_page(self.base_url + "research.html")
            self.content_data['research'].extend(research)
        
        if self.base_url + "teaching.html" not in self.visited_urls:
            teaching = self.scrape_teaching_page(self.base_url + "teaching.html")
            self.content_data['teaching'].extend(teaching)
        
        print(f"Scraping complete! Visited {len(self.visited_urls)} pages.")
        return self.content_data
    
    def save_data(self, filename="scraped_data.json"):
        """Save scraped data to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.content_data, f, indent=2, ensure_ascii=False)
        print(f"Data saved to {filename}")
    
    def update_existing_files(self):
        """Update existing Pages CMS files with scraped data"""
        print("Updating existing Pages CMS files with scraped data...")
        
        # Update member files
        for i, member in enumerate(self.content_data['members']):
            if isinstance(member, dict) and 'name' in member:
                filename = f"_members/{member['name'].lower().replace(' ', '-').replace('.', '')}.md"
                if os.path.exists(filename):
                    # Read existing file
                    with open(filename, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Update with scraped data
                    updated_content = f"""---
name: "{member['name']}"
title: "{member.get('role', 'Member').title()}"
email: "arithgeo@iwr.uni-heidelberg.de"
photo: "/assets/img/placeholder.jpg"
order: {i + 1}
---

{member['name']} is a {member.get('role', 'member')} in the research group "Computational Arithmetic Geometry" at the Interdisciplinary Center for Scientific Computing (IWR) in Heidelberg.

{member.get('content', '')}
"""
                    
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(updated_content)
                    print(f"Updated: {filename}")
        
        # Update publication files
        for i, pub in enumerate(self.content_data['publications']):
            if isinstance(pub, dict) and 'title' in pub:
                # Find existing publication file
                existing_files = list(Path('_publications').glob('*.md'))
                if existing_files:
                    filename = existing_files[0]  # Use first existing file
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(f"""---
title: "{pub['title']}"
year: 2024
publication_type: "Publication"
journal: "Heidelberg University"
publication_details: "{pub['title']}"
order: {i + 1}
---

{pub.get('content', '')}
""")
                    print(f"Updated: {filename}")
        
        # Update research files
        for i, research in enumerate(self.content_data['research']):
            if isinstance(research, dict) and 'title' in research:
                # Find existing research file
                existing_files = list(Path('_research').glob('*.md'))
                if existing_files:
                    filename = existing_files[0]  # Use first existing file
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(f"""---
title: "{research['title']}"
order: {i + 1}
---

{research.get('content', '')}
""")
                    print(f"Updated: {filename}")
        
        # Update teaching files
        for i, course in enumerate(self.content_data['teaching']):
            if isinstance(course, dict) and 'semester' in course:
                # Find existing teaching file
                existing_files = list(Path('_teaching').glob('*.md'))
                if existing_files:
                    filename = existing_files[0]  # Use first existing file
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(f"""---
title: "{course['semester']}"
year: 2024
course_type: "Course"
language: "English"
order: {i + 1}
---

{course.get('content', '')}
""")
                    print(f"Updated: {filename}")
        
        # Update link files
        for i, link in enumerate(self.content_data['links']):
            if isinstance(link, dict) and 'title' in link:
                # Find existing link file
                existing_files = list(Path('_links').glob('*.md'))
                if existing_files:
                    filename = existing_files[0]  # Use first existing file
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(f"""---
title: "{link['title']}"
url: "{link.get('url', '#')}"
category: "Link"
order: {i + 1}
---

{link.get('content', '')}
""")
                    print(f"Updated: {filename}")
        
        print("Existing Pages CMS files updated successfully!")

def main():
    """Main function to run the scraper"""
    scraper = HeidelbergScraper()
    
    # Scrape all content
    data = scraper.scrape_all()
    
    # Save raw data
    scraper.save_data()
    
    # Update existing Pages CMS files
    scraper.update_existing_files()
    
    print("\n" + "="*50)
    print("SCRAPING COMPLETE!")
    print("="*50)
    print(f"Total pages scraped: {len(scraper.visited_urls)}")
    print(f"Members found: {len(data['members'])}")
    print(f"Publications found: {len(data['publications'])}")
    print(f"Research areas found: {len(data['research'])}")
    print(f"Teaching courses found: {len(data['teaching'])}")
    print(f"Links found: {len(data['links'])}")
    print(f"News items found: {len(data['news'])}")
    print("="*50)

if __name__ == "__main__":
    main() 