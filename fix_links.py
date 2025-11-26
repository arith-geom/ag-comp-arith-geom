import yaml
import re
import os
from bs4 import BeautifulSoup

MEMBERS_FILE = '_data/members.yml'
TEACHING_FILE = '_data/teaching.yml'

broken_domains = [
    'lsf.uni-heidelberg.de',
    'www.iwr.uni-heidelberg.de',
    'www1.iwr.uni-heidelberg.de',
    'typo.iwr.uni-heidelberg.de',
    'elearning2.uni-heidelberg.de',
    'www.rzuser.uni-heidelberg.de',
    'www.mathi.uni-heidelberg.de',
    'sage.mathi.uni-heidelberg.de',
    'www.ub.uni-heidelberg.de',
    'www.math.uni-bonn.de',
    'magma.maths.usyd.edu.au',
    'www.uni-oldenburg.de',
    'www.pki.dfn.de',
    'members.vistaserv.net',
    'www.math.harvard.edu',
    'www.sciencedirect.com',
    'citeseerx.ist.psu.edu',
    'webusers.imj-prg.fr',
    'wwwmath.uni-muenster.de',
    'jtnb.cedram.org',
    'mathserver.neu.edu',
    'www.springerlink.com',
    'people.math.ethz.ch',
    'www.cems.uvm.edu',
    'web.maths.unsw.edu.au',
    'www.jmilne.org',
    'www.mathematik.uni-heidelberg.de',
    'www.cambridge.org',
    'dx.doi.org'
]

# Map old filenames (without .html) to new slugs
member_map = {
    'gebhard-boeckle': 'prof-dr-gebhard-böckle',
    'alireza-shavali': 'alireza-shavali',
    'judith-ludwig': 'prof-dr-judith-ludwig',
    'peter-graef': 'dr-peter-gräf',
    'yujia-qiu': 'dr-yujia-qiu',
    'ann-kristin-juschka': 'dr-ann-kristin-juschka',
    'barinder-banwait': 'dr-barinder-banwait',
    'sriramcv': 'sriram-chinthalagiri-venkata',
    'julian-quast': 'dr-julian-quast',
    'andreas-maurischat': 'dr-andreas-maurischat',
    'ralf-butenuth': 'dr-ralf-butenuth',
    'konrad-fischer': 'konrad-fischer'
}

# Helper to check if local asset exists
def asset_exists(path):
    # Remove query params or anchors
    clean_path = path.split('?')[0].split('#')[0]
    # Remove leading slash
    if clean_path.startswith('/'):
        clean_path = clean_path[1:]
    # Check if file exists relative to project root
    return os.path.exists(clean_path)

def fix_html_content(content):
    soup = BeautifulSoup(content, 'html.parser')
    changed = False
    
    # 1. Handle <img> tags
    for img in soup.find_all('img', src=True):
        src = img['src']
        
        # Fix fileadmin paths
        if 'fileadmin/' in src:
             if '/assets/fileadmin/' in src:
                 if '/assets//assets/' in src:
                     new_src = src.replace('/assets//assets/', '/assets/')
                     img['src'] = new_src
                     changed = True
                     src = new_src
             else:
                new_src = re.sub(r'(\.\./)*fileadmin/', '/assets/fileadmin/', src)
                if new_src != src:
                    img['src'] = new_src
                    changed = True
                    src = new_src
        
        # Check existence if it's a local asset
        if src.startswith('/assets/'):
            if not asset_exists(src):
                print(f"Removing broken image: {src}")
                img.decompose() # Remove the image tag entirely
                changed = True

    # 2. Handle <a> tags
    for a in soup.find_all('a', href=True):
        href = a['href']
        
        # Unlink broken external domains
        is_broken = False
        for domain in broken_domains:
            if domain in href:
                a.unwrap() # Remove the <a> tag but keep the text
                changed = True
                is_broken = True
                break
        if is_broken:
            continue
        
        # Fix fileadmin links
        if 'fileadmin/' in href:
            if '/assets/fileadmin/' in href:
                 if '/assets//assets/' in href:
                     new_href = href.replace('/assets//assets/', '/assets/')
                     a['href'] = new_href
                     changed = True
                     href = new_href
            else:
                new_href = re.sub(r'(\.\./)*fileadmin/', '/assets/fileadmin/', href)
                if new_href != href:
                    a['href'] = new_href
                    changed = True
                    href = new_href
        
        # Check existence if it's a local asset (specifically fileadmin or migrated)
        if href.startswith('/assets/'):
            if not asset_exists(href):
                print(f"Unlinking broken asset link: {href}")
                a.unwrap()
                changed = True
                continue

        # Fix member links
        for old_name, new_slug in member_map.items():
            if f'{old_name}.html' in href or f'/members/{old_name}/' in href or f'/members/{old_name}.html' in href:
                if new_slug not in href:
                    a['href'] = f'/members/{new_slug}/'
                    changed = True
                    break
        
        # 4. Fix specific page links
        if 'research.html' in href:
            a['href'] = '/research/'
            changed = True
        elif 'publications.html' in href:
            a['href'] = '/publications/'
            changed = True
        elif 'p-adic-numbers.html' in href:
            print(f"Unlinking broken p-adic-numbers link: {href}")
            a.unwrap()
            changed = True

    if changed:
        return str(soup)
    return content

def fix_members_links():
    print(f"Fixing links in {MEMBERS_FILE}...")
    with open(MEMBERS_FILE, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    count = 0
    
    def process_member(member):
        nonlocal count
        if 'body' in member and member['body']:
            original_body = member['body']
            new_body = fix_html_content(original_body)
            
            # Also fix relative links like ../contact.html which might not be caught by fix_html_content
            new_body = new_body.replace('href="../contact.html"', 'href="/contact/"')
            new_body = new_body.replace('href="/members/../contact/"', 'href="/contact/"')
            new_body = new_body.replace('href="../members.html"', 'href="/members/"')
            new_body = new_body.replace('href="/members/../members/"', 'href="/members/"')
            
            if new_body != original_body:
                member['body'] = new_body
                count += 1
        
        # Check metadata fields
        for field in ['website', 'cv', 'cv_link', 'url']:
            if field in member and member[field]:
                val = member[field]
                # Check broken domains
                for domain in broken_domains:
                    if domain in val:
                        print(f"Removing broken {field} link: {val}")
                        member[field] = ''
                        count += 1
                        break
                # Check local asset existence
                if val.startswith('/assets/') and not asset_exists(val):
                     print(f"Removing missing asset in {field}: {val}")
                     member[field] = ''
                     count += 1
        
        # Check links list
        if 'links' in member and isinstance(member['links'], list):
            new_links = []
            for link in member['links']:
                url = link.get('url', '')
                is_broken = False
                # Check broken domains
                for domain in broken_domains:
                    if domain in url:
                        print(f"Removing broken member link: {url}")
                        is_broken = True
                        break
                
                # Check local asset existence
                if not is_broken and url.startswith('/assets/') and not asset_exists(url):
                     print(f"Removing missing asset in member link: {url}")
                     is_broken = True
                
                if not is_broken:
                    new_links.append(link)
                else:
                    count += 1
            member['links'] = new_links

    # members.yml structure: sections -> list of section -> members -> list of member
    if isinstance(data, dict) and 'sections' in data:
        for section in data['sections']:
            if 'members' in section:
                for member in section['members']:
                    process_member(member)
    elif isinstance(data, list):
        # Fallback if it's a list
        for member in data:
            process_member(member)
                    
    with open(MEMBERS_FILE, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
    print(f"Fixed links in {count} member profiles.")

def fix_teaching_links():
    print(f"Removing broken links and fixing internal paths in {TEACHING_FILE}...")
    with open(TEACHING_FILE, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    count = 0
    body_count = 0
    
    # Helper to process a single course object
    def process_course(course):
        nonlocal count, body_count
        # Fix links list
        if 'links' in course:
            new_links = []
            for link in course['links']:
                is_broken = False
                url = link.get('url', '')
                for domain in broken_domains:
                    if domain in url:
                        is_broken = True
                        break
                if not is_broken:
                    new_links.append(link)
                else:
                    count += 1
            course['links'] = new_links
        
        # Fix body content
        if 'body' in course and course['body']:
            original_body = course['body']
            new_body = fix_html_content(original_body)
            if new_body != original_body:
                course['body'] = new_body
                body_count += 1

    # Traverse the nested structure
    if isinstance(data, dict) and 'courses' in data:
        # Root is a dict with 'courses' key
        for item in data['courses']:
            if 'semesters' in item:
                for semester in item['semesters']:
                    if 'courses' in semester:
                        for course in semester['courses']:
                            process_course(course)
            elif 'title' in item: 
                 process_course(item)
    elif isinstance(data, list):
        for course in data:
            process_course(course)
            
    with open(TEACHING_FILE, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
    print(f"Removed {count} broken links from teaching data.")
    print(f"Fixed/Unlinked links in {body_count} course bodies.")

def fix_publications_links():
    PUBLICATIONS_FILE = '_data/publications.yml'
    print(f"Fixing links in {PUBLICATIONS_FILE}...")
    
    if not os.path.exists(PUBLICATIONS_FILE):
        print(f"{PUBLICATIONS_FILE} not found.")
        return

    with open(PUBLICATIONS_FILE, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    count = 0
    
    # Helper to check if local asset exists
    def asset_exists(path):
        clean_path = path.split('?')[0].split('#')[0]
        if clean_path.startswith('/'):
            clean_path = clean_path[1:]
        return os.path.exists(clean_path)

    if isinstance(data, dict):
        # Fix publications list
        if 'publications' in data and isinstance(data['publications'], list):
            for pub in data['publications']:
                # Fix links list
                if 'links' in pub and isinstance(pub['links'], list):
                    new_links = []
                    for link in pub['links']:
                        is_broken = False
                        url = link.get('url', '')
                        for domain in broken_domains:
                            if domain in url:
                                is_broken = True
                                break
                        if not is_broken:
                            new_links.append(link)
                        else:
                            count += 1
                    pub['links'] = new_links
                
                # Fix pdfs list (check existence)
                if 'pdfs' in pub and isinstance(pub['pdfs'], list):
                    new_pdfs = []
                    for pdf in pub['pdfs']:
                        file_path = pdf.get('file', '')
                        if file_path.startswith('/assets/'):
                            if asset_exists(file_path):
                                new_pdfs.append(pdf)
                            else:
                                print(f"Removing missing PDF from publication: {file_path}")
                                count += 1
                        else:
                            # External PDF link? Check broken domains
                            is_broken = False
                            for domain in broken_domains:
                                if domain in file_path:
                                    is_broken = True
                                    break
                            if not is_broken:
                                new_pdfs.append(pdf)
                            else:
                                count += 1
                    pub['pdfs'] = new_pdfs

        # Fix software list
        if 'software' in data and isinstance(data['software'], list):
            for soft in data['software']:
                link = soft.get('link', '')
                if link:
                    # Check broken domains
                    for domain in broken_domains:
                        if domain in link:
                            print(f"Removing broken software link: {link}")
                            soft['link'] = '' # Clear the link
                            count += 1
                            break
                    
                    # Check local existence (e.g. members/ralf-butenuth/...)
                    # The report showed: members/ralf-butenuth/publications.html (relative?)
                    # If it's relative and broken, we might want to clear it.
                    # But checking relative paths is tricky without context.
                    # The report says: File not found: _site/publications/members/ralf-butenuth/publications.html
                    # So it's treated as relative to /publications/.
                    # If we want to fix it, we should probably check if it exists or clear it.
                    # For now, let's just clear it if it looks like the specific broken one.
                    if 'members/ralf-butenuth/publications.html' in link:
                         soft['link'] = ''
                         count += 1

    with open(PUBLICATIONS_FILE, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
    print(f"Fixed/Removed {count} links in publications.")

if __name__ == "__main__":
    fix_members_links()
    fix_teaching_links()
    fix_publications_links()
