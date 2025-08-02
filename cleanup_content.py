#!/usr/bin/env python3
"""
Clean up scraped content to make it more readable and properly formatted
"""

import re
from pathlib import Path

def clean_content(content):
    """Clean up scraped content"""
    # Remove navigation elements
    content = re.sub(r'HomeMembersResearchPublicationsTeachingLinksContact', '', content)
    content = re.sub(r'Uni Heidelberg > IWR > ARITHGEO', '', content)
    content = re.sub(r'Interna\s*>\s*', '', content)
    content = re.sub(r'\[english\]\s*\|\s*\[\]', '', content)
    
    # Remove copyright and update info
    content = re.sub(r'Last Update:.*?Impressum\.', '', content)
    content = re.sub(r'© Copyright Universität Heidelberg\.\s*Impressum\.', '', content)
    
    # Clean up email addresses
    content = re.sub(r'<at>', '@', content)
    
    # Clean up extra whitespace
    content = re.sub(r'\s+', ' ', content)
    content = content.strip()
    
    # Fix special characters
    content = content.replace('Ã¶', 'ö')
    content = content.replace('Ã¤', 'ä')
    content = content.replace('Ã¼', 'ü')
    content = content.replace('ÃŸ', 'ß')
    
    return content

def update_index_md():
    """Update the main index.md file with cleaned content"""
    if Path('index.md').exists():
        with open('index.md', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract the content between the front matter and end
        lines = content.split('\n')
        front_matter_end = 0
        for i, line in enumerate(lines):
            if line.strip() == '---':
                front_matter_end = i
                break
        
        # Get the content after front matter
        main_content = '\n'.join(lines[front_matter_end+1:])
        cleaned_content = clean_content(main_content)
        
        # Create new content
        new_content = f"""---
layout: page
title: "Computational Arithmetic Geometry"
permalink: /
---

{cleaned_content}
"""
        
        with open('index.md', 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("Updated: index.md")

def update_contact_md():
    """Update the contact.md file with cleaned content"""
    contact_file = Path('_links/contact.md')
    if contact_file.exists():
        with open(contact_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract the content between the front matter and end
        lines = content.split('\n')
        front_matter_end = 0
        for i, line in enumerate(lines):
            if line.strip() == '---':
                front_matter_end = i
                break
        
        # Get the content after front matter
        main_content = '\n'.join(lines[front_matter_end+1:])
        cleaned_content = clean_content(main_content)
        
        # Create new content
        new_content = f"""---
title: "Contact"
url: "#"
category: "Contact"
order: 1
---

{cleaned_content}

**Email:** arithgeo@iwr.uni-heidelberg.de  
**Phone:** +49-6221-54-14734  
**Fax:** +49-6221-54-14737
"""
        
        with open(contact_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("Updated: _links/contact.md")

def main():
    """Main function to clean up content"""
    print("Cleaning up scraped content...")
    
    update_index_md()
    update_contact_md()
    
    print("\n" + "="*50)
    print("CONTENT CLEANUP COMPLETE!")
    print("="*50)
    print("All content has been cleaned and formatted properly.")
    print("="*50)

if __name__ == "__main__":
    main() 