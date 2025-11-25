import os
import yaml
from bs4 import BeautifulSoup
import re
import sys

# Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TYPO_MIRROR_DIR = os.path.join(BASE_DIR, 'typo_mirror', 'groups', 'arith-geom')
DATA_DIR = os.path.join(BASE_DIR, '_data')
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')

def clean_text(text):
    if not text:
        return ""
    # Remove non-breaking spaces and extra whitespace
    text = text.replace('\xa0', ' ')
    return re.sub(r'\s+', ' ', text).strip()

def fix_asset_path(path):
    if not path:
        return ""
    # Replace ../../fileadmin with /assets/fileadmin
    # Also handle ../../../fileadmin for deeper pages
    if 'fileadmin' in path:
        # Normalize to /assets/fileadmin/...
        # Find where fileadmin starts
        idx = path.find('fileadmin')
        if idx != -1:
            return '/assets/' + path[idx:]
    return path

def extract_field(text, pattern):
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return clean_text(match.group(1))
    return None

def parse_members():
    print("Migrating Members...")
    members_file = os.path.join(TYPO_MIRROR_DIR, 'members.html')
    if not os.path.exists(members_file):
        print(f"Error: {members_file} not found")
        return

    with open(members_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    content_div = soup.find('div', id='c1265')
    if not content_div:
        print("Error: Content div c1265 not found in members.html")
        return

    sections_data = []
    current_section = None
    former_members_section = None
    
    # Iterate through elements in content_div
    for element in content_div.children:
        if element.name == 'h4':
            # Check if this h4 is actually a member (contains a link)
            link = element.find('a')
            if link:
                # It's a member (e.g. Secretary Astrid Cederbaum)
                if current_section:
                    name = clean_text(link.get_text())
                    url = link.get('href')
                    # Role might be the section title if it's a single person section like Secretary
                    # Or we can just use "Member" or "Secretary"
                    role = "Member"
                    if current_section['title'] == 'Secretary':
                        role = "Secretary"
                    
                    member_data = process_member_subpage(name, url, role)
                    current_section['members'].append(member_data)
            else:
                # It's a section title
                section_title = clean_text(element.get_text())
                if section_title:
                    # If previous section exists, add it
                    if current_section:
                        sections_data.append(current_section)
                    
                    # Set layout based on section title
                    layout = 'big' if section_title in ['Head', 'Secretary'] else 'medium'
                    current_section = {
                        'title': section_title,
                        'layout': layout,
                        'members': []
                    }
        
        elif element.name == 'h3':
            # Head of group usually
            if current_section:
                link = element.find('a')
                if link:
                    name = clean_text(link.get_text())
                    url = link.get('href')
                    member_data = process_member_subpage(name, url, "Group Leader")
                    current_section['members'].append(member_data)

        elif element.name == 'ul':
            # List of members
            if current_section:
                for li in element.find_all('li'):
                    link = li.find('a')
                    if link:
                        name = clean_text(link.get_text())
                        url = link.get('href')
                        # Guess role based on name
                        role = "Researcher" if "Dr." in name else "PhD Student"
                        member_data = process_member_subpage(name, url, role)
                        current_section['members'].append(member_data)
        
        elif element.name == 'p':
            # Check for "Former members" link
            link = element.find('a')
            if link and 'Former members' in link.get_text():
                url = link.get('href')
                former_members = parse_former_members(url)
                if former_members:
                    former_members_section = {
                        'title': 'Former Members',
                        'layout': 'small',
                        'members': former_members
                    }

    if current_section:
        sections_data.append(current_section)
    
    # Add Former Members LAST
    if former_members_section:
        sections_data.append(former_members_section)

    # Save to members.yml
    output_file = os.path.join(DATA_DIR, 'members.yml')
    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump({'sections': sections_data}, f, sort_keys=False, allow_unicode=True)
    print(f"Saved to {output_file}")

def parse_former_members(url):
    print(f"Parsing Former Members from {url}...")
    members = []
    if not url:
        return members
        
    path = os.path.join(TYPO_MIRROR_DIR, url)
    if not os.path.exists(path):
        print(f"Warning: Former members page {path} not found")
        return members

    try:
        with open(path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return members

    # Find content
    content_div = soup.find('div', class_='frame-type-text')
    if not content_div:
        content_div = soup.find('div', id='content')

    if not content_div:
        return members

    # Former members are usually in a list or paragraphs
    # Let's look for ul/li or p tags
    
    # Check for lists first
    for ul in content_div.find_all('ul'):
        for li in ul.find_all('li'):
            name = clean_text(li.get_text())
            link = li.find('a')
            url = link.get('href') if link else None
            
            members.append({
                'name': name,
                'role': 'Former Member',
                'group': 'Former Members',
            })

    # Check for paragraphs (as seen in former-members.html)
    for p in content_div.find_all('p'):
        # Skip "back to current members" or empty paragraphs
        text = clean_text(p.get_text())
        if not text or "back to" in text.lower():
            continue
            
        link = p.find('a')
        url = link.get('href') if link else None
        name = clean_text(p.get_text())
        
        # Avoid duplicates if p contains ul (unlikely but possible)
        if p.find('ul'):
            continue
            
        members.append({
            'name': name,
            'role': 'Former Member',
            'group': 'Former Members',
        })
            
    return members

def process_member_subpage(name, url, default_role):
    member_data = {
        'name': name,
        'role': default_role,
        'group': 'Members' # Default
    }
    
    if not url:
        return member_data

    # Resolve subpage path
    # url might be relative like "members/gebhard-boeckle.html"
    subpage_path = os.path.join(TYPO_MIRROR_DIR, url)
    if not os.path.exists(subpage_path):
        print(f"Warning: Subpage {subpage_path} not found")
        return member_data

    try:
        with open(subpage_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
    except Exception as e:
        print(f"Error reading {subpage_path}: {e}")
        return member_data

    # Photo - search ENTIRE content for any image  
    content_container = soup.find('div', id='content')
    if not content_container:
        content_container = soup
    
    # Try multiple ways to find photo
    img = content_container.find('img', class_='image-embed-item')
    if not img:
        # Look for any img in a figure
        figure = content_container.find('figure', class_='image')
        if figure:
            img = figure.find('img')
    if img and img.get('src'):
        member_data['photo'] = fix_asset_path(img.get('src'))

    # Try to find content div
    body_text = soup.find('div', class_='ce-bodytext')
    if not body_text:
        # Try textpic which some pages use
        body_text = soup.find('div', class_='ce-textpic')
        if body_text:
            body_text = body_text.find('div', class_='ce-bodytext')
    if not body_text:
        # Fallback to #content
        body_text = soup.find('div', id='content')
    
    if not body_text:
        return member_data

    # Text content
    text = body_text.get_text(separator='\n')
    
    # Email
    email = extract_field(text, r'Email:\s*([^\n]+)')
    if email:
        member_data['email'] = email.replace('<at>', '@').strip()
    
    # Phone
    phone = extract_field(text, r'Tel\.:\s*([^\n]+)')
    if phone:
        member_data['phone'] = phone
        
    # Fax
    fax = extract_field(text, r'Fax:\s*([^\n]+)')
    if fax:
        member_data['fax'] = fax
        
    # Room
    room = extract_field(text, r'Room:\s*([^\n]+)')
    if room:
        member_data['room'] = room
        
    # Office Hours
    office_hours = extract_field(text, r'Office Hours:\s*([^\n]+)')
    if office_hours:
        member_data['office_hours'] = office_hours

    # CV
    cv_link = body_text.find('a', href=re.compile(r'\.pdf$'))
    if cv_link:
        member_data['cv'] = fix_asset_path(cv_link.get('href'))

    # Research Interests
    # Look for "Research Interests" heading or text
    # This is heuristic
    
    return member_data

def parse_publications():
    print("Migrating Publications...")
    pub_file = os.path.join(TYPO_MIRROR_DIR, 'publications.html')
    if not os.path.exists(pub_file):
        print(f"Error: {pub_file} not found")
        return

    with open(pub_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    content_div = soup.find('div', id='c1579')
    if not content_div:
        print("Error: Content div c1579 not found in publications.html")
        return

    publications_data = []
    software_data = []

    # Parse Software Packages
    # Look for "Software packages:" h2
    software_header = content_div.find('h2', string=re.compile('Software packages', re.I))
    if software_header:
        software_list = software_header.find_next('ul')
        if software_list:
            for li in software_list.find_all('li'):
                title = ""
                link = ""
                description = clean_text(li.get_text())
                
                a_tag = li.find('a')
                if a_tag:
                    title = clean_text(a_tag.get_text())
                    link = fix_asset_path(a_tag.get('href'))
                    # Remove title from description to avoid duplication if it's at the start
                    description = description.replace(title, '').strip()
                    if description.startswith(','):
                        description = description[1:].strip()

                software_data.append({
                    'title': title,
                    'description': description,
                    'link': link,
                    'link_text': 'View Package'
                })

    # Parse Publications from linked pages
    # Look for "Publications and preprints" h2
    pub_header = content_div.find('h2', string=re.compile('Publications and preprints', re.I))
    if pub_header:
        pub_list = pub_header.find_next('ul')
        if pub_list:
            for li in pub_list.find_all('li'):
                a_tag = li.find('a')
                if a_tag:
                    url = a_tag.get('href')
                    # Parse this member's publication page
                    pubs = parse_member_publications(url)
                    publications_data.extend(pubs)

    # Save to publications.yml
    output_file = os.path.join(DATA_DIR, 'publications.yml')
    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump({
            'publications': publications_data,
            'software': software_data
        }, f, sort_keys=False, allow_unicode=True)
    print(f"Saved to {output_file}")

def parse_member_publications(url):
    pubs = []
    if not url:
        return pubs
    
    pub_path = os.path.join(TYPO_MIRROR_DIR, url)
    if not os.path.exists(pub_path):
        print(f"Warning: Publication page {pub_path} not found")
        return pubs

    try:
        with open(pub_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
    except Exception as e:
        print(f"Error reading {pub_path}: {e}")
        return pubs

    # Find content div, usually c2539 or similar
    # We can search for h3 "Research articles" or similar
    content_div = soup.find('div', class_='frame-type-text')
    if not content_div:
        content_div = soup.find('div', id='content')

    if not content_div:
        return pubs

    current_type = "Article"
    current_status = "Journal Article"

    for element in content_div.children:
        if element.name == 'h3':
            header = clean_text(element.get_text()).lower()
            if 'research' in header:
                current_type = "Article"
                current_status = "Journal Article"
            elif 'book' in header:
                current_type = "Book"
                current_status = "Book"
            elif 'preprint' in header:
                current_type = "Article"
                current_status = "Preprint"
            elif 'preparation' in header:
                current_type = "Article"
                current_status = "Submitted" # or Other

        elif element.name == 'ul':
            for li in element.find_all('li'):
                pub_data = {
                    'type': current_type,
                    'status': current_status,
                    'links': [],
                    'pdfs': []
                }
                
                # Extract text and links
                # Format: (joint with X) <a href>Title</a> (<a href>pdf</a>) <br> Journal...
                
                # Title is usually the first link that is not a PDF and not an author link (MathSciNet)
                def is_title_link(href):
                    if not href:
                        return False
                    if href.endswith('.pdf'):
                        return False
                    if 'ams.org' in href or 'mathscinet' in href:
                        return False
                    return True

                title_link = li.find('a', href=is_title_link)
                if title_link:
                    pub_data['title'] = clean_text(title_link.get_text())
                    link_url = title_link.get('href')
                    if link_url:
                        pub_data['links'].append({'label': 'Link', 'url': link_url})
                else:
                    # Maybe title is just text?
                    # Try to extract text before <br> or first text node that is not author info
                    # This is hard without specific structure.
                    # Fallback: use the whole text minus author info
                    clean_li_text = clean_text(li.get_text())
                    # Remove "joint with ..."
                    clean_li_text = re.sub(r'\(joint with [^\)]+\)', '', clean_li_text).strip()
                    # Remove trailing journal info if possible (heuristic)
                    # For now, just take the first sentence or up to a newline/br
                    pub_data['title'] = clean_li_text.split('\n')[0]

                # PDF link
                pdf_link = li.find('a', href=re.compile(r'\.pdf$'))
                if pdf_link:
                    pub_data['pdfs'].append({'label': 'PDF', 'file': fix_asset_path(pdf_link.get('href'))})

                # Authors
                text = li.get_text()
                authors_match = re.search(r'\(joint with ([^\)]+)\)', text)
                if authors_match:
                    pub_data['authors'] = "Joint with " + authors_match.group(1)
                else:
                    pub_data['authors'] = "Gebhard Böckle" # Default/Fallback

                # Journal details
                # Usually after <br>
                if li.find('br'):
                    details = li.find('br').next_sibling
                    if details and isinstance(details, str):
                        pub_data['journal_details'] = clean_text(details)
                    elif details and details.name == 'em':
                        pub_data['journal_details'] = clean_text(details.get_text())

                if 'title' in pub_data and pub_data['title']:
                    pubs.append(pub_data)

    return pubs

def parse_teaching():
    print("Migrating Teaching...")
    teaching_file = os.path.join(TYPO_MIRROR_DIR, 'teaching.html')
    past_teaching_file = os.path.join(TYPO_MIRROR_DIR, 'teaching', 'past-teaching.html')
    
    if not os.path.exists(teaching_file):
        print(f"Error: {teaching_file} not found")
        return

    courses_by_year = {} # year -> list of semester objects

    # Parse current teaching
    with open(teaching_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    content_div = soup.find('div', id='c1360')
    if content_div:
        parse_teaching_content(content_div, courses_by_year)
    
    # Parse past teaching from Duisburg-Essen
    if os.path.exists(past_teaching_file):
        print("  Parsing past teaching from Duisburg-Essen...")
        with open(past_teaching_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
        
        content_div = soup.find('div', id='c2554')
        if content_div:
            parse_teaching_content(content_div, courses_by_year)

    # Convert dict to list
    teaching_data = {'courses': []}
    for year in sorted(courses_by_year.keys(), reverse=True):
        teaching_data['courses'].append({
            'year': year,
            'semesters': courses_by_year[year]
        })

    # Save to teaching.yml
    output_file = os.path.join(DATA_DIR, 'teaching.yml')
    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump(teaching_data, f, sort_keys=False, allow_unicode=True)
    print(f"Saved to {output_file}")

def parse_teaching_content(content_div, courses_by_year):
    """Helper to parse teaching content from a div"""
    current_semester = None
    
    for element in content_div.children:
        if element.name == 'h4':
            semester_name = clean_text(element.get_text())
            if semester_name and ('term' in semester_name.lower() or 'semester' in semester_name.lower()):
                current_semester = semester_name
                # Extract year - handle formats like "Winter term 2009/2010"
                year_match = re.search(r'(19|20)\d\d', semester_name)
                if year_match:
                    year = int(year_match.group(0))
                else:
                    year = 2025
                
                if year not in courses_by_year:
                    courses_by_year[year] = []
                
        elif element.name == 'ul':
            if current_semester:
                # Find the year object
                year_match = re.search(r'(19|20)\d\d', current_semester)
                if year_match:
                    year = int(year_match.group(0))
                else:
                    year = 2025
                
                # Check if semester exists in year list
                sem_obj = next((s for s in courses_by_year[year] if s['semester'] == current_semester), None)
                if not sem_obj:
                    sem_obj = {'semester': current_semester, 'courses': []}
                    courses_by_year[year].append(sem_obj)

                for li in element.find_all('li', recursive=False):
                    course_data = {
                        'title': "",
                        'instructor': "",
                        'description': "",
                        'links': [],
                        'pdfs': []
                    }
                    
                    link = li.find('a')
                    if link:
                        course_data['title'] = clean_text(link.get_text())
                        href = link.get('href')
                        if href:
                            if href.endswith('.pdf'):
                                course_data['pdfs'].append({'label': 'Info', 'file': fix_asset_path(href)})
                            else:
                                course_data['links'].append({'label': 'Course Page', 'url': fix_asset_path(href)})
                    
                    # Get full text
                    full_text = clean_text(li.get_text())
                    if not course_data['title']:
                        course_data['title'] = full_text

                    # Instructor usually in parens
                    text = li.get_text()
                    instr_match = re.search(r'\(([^)]+)\)', text)
                    if instr_match:
                        course_data['instructor'] = instr_match.group(1)
                        # Remove instructor from title if present
                        course_data['title'] = course_data['title'].replace(f"({course_data['instructor']})", "").strip()

                    sem_obj['courses'].append(course_data)

def parse_research():
    print("Migrating Research...")
    research_file = os.path.join(TYPO_MIRROR_DIR, 'research.html')
    if not os.path.exists(research_file):
        print(f"Error: {research_file} not found")
        return

    with open(research_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    content_div = soup.find('div', id='c2580')
    if not content_div:
        print("Error: Content div c2580 not found in research.html")
        return

    research_areas = []
    
    # The content is in a single p tag with b tags for titles
    # <p><b>Title1:</b><br>Content1...<br><br><br><b>Title2:</b><br>Content2...</p>
    
    p_tag = content_div.find('p')
    if p_tag:
        # Get all child elements
        # We can iterate and build the structure
        current_title = ""
        current_content = []
        
        for child in p_tag.children:
            if child.name == 'b':
                # New title
                if current_title:
                    # Save previous
                    research_areas.append({
                        'title': current_title,
                        'icon': 'fas fa-book',
                        'content': clean_text(" ".join(current_content))
                    })
                
                current_title = clean_text(child.get_text()).rstrip(':')
                current_content = []
            elif child.name == 'br':
                continue
            elif isinstance(child, str):
                text = clean_text(child)
                if text:
                    current_content.append(text)
        
        # Add last one
        if current_title:
            research_areas.append({
                'title': current_title,
                'icon': 'fas fa-book',
                'content': clean_text(" ".join(current_content))
            })

    # Save to research.yml
    output_file = os.path.join(DATA_DIR, 'research.yml')
    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump({'research_areas': research_areas}, f, sort_keys=False, allow_unicode=True)
    print(f"Saved to {output_file}")

def parse_links():
    print("Migrating Links...")
    links_file = os.path.join(TYPO_MIRROR_DIR, 'links.html')
    if not os.path.exists(links_file):
        print(f"Error: {links_file} not found")
        return

    with open(links_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    content_div = soup.find('div', id='c1581')
    if not content_div:
        print("Error: Content div c1581 not found in links.html")
        return

    groups = []
    current_group = {'title': 'General Links', 'icon': 'fas fa-link', 'links': []}
    
    for element in content_div.children:
        if element.name == 'p':
            link = element.find('a')
            if link:
                current_group['links'].append({
                    'title': clean_text(link.get_text()),
                    'url': link.get('href')
                })

    if current_group['links']:
        groups.append(current_group)

    # Save to links.yml
    output_file = os.path.join(DATA_DIR, 'links.yml')
    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump({'groups': groups}, f, sort_keys=False, allow_unicode=True)
    print(f"Saved to {output_file}")

if __name__ == "__main__":
    parse_members()
    parse_publications()
    parse_teaching()
    parse_research()
    parse_links()

