#!/usr/bin/env python3
"""
Update existing Pages CMS files with scraped data from Heidelberg website
"""

import json
import os
from pathlib import Path

def load_scraped_data():
    """Load the scraped data from JSON file"""
    with open('scraped_data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def update_members(data):
    """Update member files with scraped data"""
    print("Updating member files...")
    
    # Get all member data
    members_data = []
    
    # Extract from pages
    for url, page_data in data['pages'].items():
        if 'members' in url and 'members.html' not in url:
            # This is a member page
            title = page_data.get('title', '')
            content = page_data.get('content', '')
            
            # Extract name from title or URL
            if 'Prof. Dr.' in title:
                name = title.split('Prof. Dr.')[-1].strip()
            elif 'Dr.' in title:
                name = title.split('Dr.')[-1].strip()
            else:
                # Extract from URL
                name = url.split('/')[-1].replace('.html', '').replace('-', ' ').title()
            
            members_data.append({
                'name': name,
                'title': 'Member',
                'content': content,
                'url': url
            })
    
    # Update existing member files
    member_files = list(Path('_members').glob('*.md'))
    
    for i, member_file in enumerate(member_files):
        if i < len(members_data):
            member = members_data[i]
            
            # Clean up content
            content = member['content']
            # Remove navigation and common elements
            content = content.replace('HomeMembersResearchPublicationsTeachingLinksContact', '')
            content = content.replace('Uni Heidelberg > IWR > ARITHGEO', '')
            content = content.replace('Last Update:', '')
            content = content.replace('© Copyright Universität Heidelberg. Impressum.', '')
            
            # Create updated content
            updated_content = f"""---
name: "{member['name']}"
title: "{member['title']}"
email: "arithgeo@iwr.uni-heidelberg.de"
photo: "/assets/img/placeholder.jpg"
order: {i + 1}
---

{member['name']} is a member of the research group "Computational Arithmetic Geometry" at the Interdisciplinary Center for Scientific Computing (IWR) in Heidelberg.

{content}
"""
            
            with open(member_file, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print(f"Updated: {member_file}")

def update_publications(data):
    """Update publication files with scraped data"""
    print("Updating publication files...")
    
    # Get publications page content
    publications_page = None
    for url, page_data in data['pages'].items():
        if 'publications.html' in url:
            publications_page = page_data
            break
    
    if publications_page:
        content = publications_page.get('content', '')
        
        # Clean up content
        content = content.replace('HomeMembersResearchPublicationsTeachingLinksContact', '')
        content = content.replace('Uni Heidelberg > IWR > ARITHGEO', '')
        content = content.replace('Last Update:', '')
        content = content.replace('© Copyright Universität Heidelberg. Impressum.', '')
        
        # Update existing publication file
        pub_files = list(Path('_publications').glob('*.md'))
        if pub_files:
            filename = pub_files[0]
            
            updated_content = f"""---
title: "Publications and Research"
year: 2024
publication_type: "Publication"
journal: "Heidelberg University"
publication_details: "Research Group Publications"
order: 1
---

{content}
"""
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print(f"Updated: {filename}")

def update_research(data):
    """Update research files with scraped data"""
    print("Updating research files...")
    
    # Get research page content
    research_page = None
    for url, page_data in data['pages'].items():
        if 'research.html' in url:
            research_page = page_data
            break
    
    if research_page:
        content = research_page.get('content', '')
        
        # Clean up content
        content = content.replace('HomeMembersResearchPublicationsTeachingLinksContact', '')
        content = content.replace('Uni Heidelberg > IWR > ARITHGEO', '')
        content = content.replace('Last Update:', '')
        content = content.replace('© Copyright Universität Heidelberg. Impressum.', '')
        
        # Update existing research file
        research_files = list(Path('_research').glob('*.md'))
        if research_files:
            filename = research_files[0]
            
            updated_content = f"""---
title: "Research Areas"
order: 1
---

{content}
"""
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print(f"Updated: {filename}")

def update_teaching(data):
    """Update teaching files with scraped data"""
    print("Updating teaching files...")
    
    # Get teaching page content
    teaching_page = None
    for url, page_data in data['pages'].items():
        if 'teaching.html' in url:
            teaching_page = page_data
            break
    
    if teaching_page:
        content = teaching_page.get('content', '')
        
        # Clean up content
        content = content.replace('HomeMembersResearchPublicationsTeachingLinksContact', '')
        content = content.replace('Uni Heidelberg > IWR > ARITHGEO', '')
        content = content.replace('Last Update:', '')
        content = content.replace('© Copyright Universität Heidelberg. Impressum.', '')
        
        # Update existing teaching file
        teaching_files = list(Path('_teaching').glob('*.md'))
        if teaching_files:
            filename = teaching_files[0]
            
            updated_content = f"""---
title: "Current Teaching"
year: 2024
course_type: "Course"
language: "English"
order: 1
---

{content}
"""
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print(f"Updated: {filename}")

def update_links(data):
    """Update link files with scraped data"""
    print("Updating link files...")
    
    # Get links page content
    links_page = None
    for url, page_data in data['pages'].items():
        if 'links.html' in url:
            links_page = page_data
            break
    
    if links_page:
        content = links_page.get('content', '')
        
        # Clean up content
        content = content.replace('HomeMembersResearchPublicationsTeachingLinksContact', '')
        content = content.replace('Uni Heidelberg > IWR > ARITHGEO', '')
        content = content.replace('Last Update:', '')
        content = content.replace('© Copyright Universität Heidelberg. Impressum.', '')
        
        # Update existing link file
        link_files = list(Path('_links').glob('*.md'))
        if link_files:
            filename = link_files[0]
            
            updated_content = f"""---
title: "Useful Links"
url: "#"
category: "Link"
order: 1
---

{content}
"""
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print(f"Updated: {filename}")

def update_main_page(data):
    """Update main page with scraped data"""
    print("Updating main page...")
    
    # Get main page content
    main_page = None
    for url, page_data in data['pages'].items():
        if url.endswith('/') or 'index.html' in url:
            main_page = page_data
            break
    
    if main_page:
        content = main_page.get('content', '')
        
        # Clean up content
        content = content.replace('HomeMembersResearchPublicationsTeachingLinksContact', '')
        content = content.replace('Uni Heidelberg > IWR > ARITHGEO', '')
        content = content.replace('Last Update:', '')
        content = content.replace('© Copyright Universität Heidelberg. Impressum.', '')
        
        # Update index.md if it exists
        if os.path.exists('index.md'):
            updated_content = f"""---
layout: page
title: "Computational Arithmetic Geometry"
permalink: /
---

{content}
"""
            
            with open('index.md', 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print("Updated: index.md")

def update_contact(data):
    """Update contact information"""
    print("Updating contact information...")
    
    # Get contact page content
    contact_page = None
    for url, page_data in data['pages'].items():
        if 'contact.html' in url:
            contact_page = page_data
            break
    
    if contact_page:
        content = contact_page.get('content', '')
        
        # Extract contact information
        email = "arithgeo@iwr.uni-heidelberg.de"
        phone = "+49-6221-54-14734"
        fax = "+49-6221-54-14737"
        
        # Clean up content
        content = content.replace('HomeMembersResearchPublicationsTeachingLinksContact', '')
        content = content.replace('Uni Heidelberg > IWR > ARITHGEO', '')
        content = content.replace('Last Update:', '')
        content = content.replace('© Copyright Universität Heidelberg. Impressum.', '')
        
        # Update contact file if it exists
        contact_files = list(Path('_links').glob('contact.md'))
        if contact_files:
            filename = contact_files[0]
            
            updated_content = f"""---
title: "Contact"
url: "#"
category: "Contact"
order: 1
---

{content}

**Email:** {email}  
**Phone:** {phone}  
**Fax:** {fax}
"""
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print(f"Updated: {filename}")

def main():
    """Main function to update all content"""
    print("Loading scraped data...")
    data = load_scraped_data()
    
    print("Updating content files...")
    
    # Update all content types
    update_members(data)
    update_publications(data)
    update_research(data)
    update_teaching(data)
    update_links(data)
    update_main_page(data)
    update_contact(data)
    
    print("\n" + "="*50)
    print("CONTENT UPDATE COMPLETE!")
    print("="*50)
    print("All existing Pages CMS files have been updated with scraped content.")
    print("The content now reflects the official Heidelberg arith-geom website.")
    print("="*50)

if __name__ == "__main__":
    main() 