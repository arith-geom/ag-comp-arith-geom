import os
import yaml
import re
import shutil
from bs4 import BeautifulSoup
from urllib.parse import unquote

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OLD_SITE_DIR = os.path.join(BASE_DIR, 'typo_mirror')
DATA_DIR = os.path.join(BASE_DIR, '_data')
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
MIGRATED_ASSETS_DIR = os.path.join(ASSETS_DIR, 'migrated')

# Ensure migrated assets directory exists
os.makedirs(MIGRATED_ASSETS_DIR, exist_ok=True)

def load_yaml(filepath):
    if not os.path.exists(filepath):
        return {}
    with open(filepath, 'r') as f:
        return yaml.safe_load(f) or {}

def save_yaml(filepath, data):
    with open(filepath, 'w') as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True)

def clean_text(text):
    if not text:
        return ""
    return text.strip()

def copy_asset(old_path, source_file_path=None):
    """Copies an asset from the old site to the new site."""
    # Remove 'file://' prefix if present
    if old_path.startswith('file://'):
        old_path = old_path[7:]
    
    found_path = None

    # Handle relative paths like ../../../fileadmin...
    if source_file_path and old_path.startswith('../'):
        # Resolve relative to the source file
        source_dir = os.path.dirname(source_file_path)
        resolved_path = os.path.normpath(os.path.join(source_dir, old_path))
        if os.path.exists(resolved_path):
            found_path = resolved_path
    
    if not found_path:
        # Try direct path inside typo_mirror (assuming path starts from root if not relative)
        candidate = os.path.join(OLD_SITE_DIR, old_path.lstrip('/'))
        if os.path.exists(candidate):
            found_path = candidate
    
    if not found_path:
        # Try searching
        filename = os.path.basename(old_path)
        # Remove query parameters from filename search
        if '?' in filename:
            filename = filename.split('?')[0]
            
        for root, dirs, files in os.walk(OLD_SITE_DIR):
            if filename in files:
                found_path = os.path.join(root, filename)
                break
    
    if found_path:
        filename = os.path.basename(found_path)
        # Clean filename
        filename = unquote(filename)
        if '?' in filename:
            filename = filename.split('?')[0]
            
        new_path = os.path.join(MIGRATED_ASSETS_DIR, filename)
        if not os.path.exists(new_path):
            shutil.copy2(found_path, new_path)
        return f"/assets/migrated/{filename}"
    
    return None

def migrate_members():
    print("Migrating Members...")
    members_data = load_yaml(os.path.join(DATA_DIR, 'members.yml'))
    
    # Map existing members for easy lookup
    member_map = {}
    for section in members_data.get('sections', []):
        for member in section.get('members', []):
            name = member.get('name')
            if name:
                member_map[name] = member

    # Iterate through old member pages
    members_dir = os.path.join(OLD_SITE_DIR, 'groups/arith-geom/members')
    if not os.path.exists(members_dir):
        print(f"Warning: Members directory not found at {members_dir}")
        return

    for filename in os.listdir(members_dir):
        if not filename.endswith('.html') or filename == 'index.html':
            continue
            
        filepath = os.path.join(members_dir, filename)
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            soup = BeautifulSoup(f, 'html.parser')
            
        # Extract Name (usually in h1 or title or h2 in content)
        name_tag = soup.find('h1')
        if not name_tag:
             # Try h2 inside header (common in typo3)
             name_tag = soup.find('header')
             if name_tag:
                 name_tag = name_tag.find('h2')
        
        if not name_tag:
             # Try h2 anywhere in content
             content_div = soup.find('div', {'id': 'content'})
             if content_div:
                 # Find the FIRST heading tag, regardless of level
                 name_tag = content_div.find(['h1', 'h2', 'h3', 'h4'])

        if not name_tag:
            continue
            
        name = clean_text(name_tag.text)
        
        # Find matching member in existing data
        matched_member = None
        for existing_name, member in member_map.items():
            # Normalize names for comparison
            n1 = existing_name.lower().replace('prof.', '').replace('dr.', '').strip()
            n2 = name.lower().replace('prof.', '').replace('dr.', '').strip()
            
            if n1 in n2 or n2 in n1:
                matched_member = member
                break
        
        if matched_member:
            print(f"  Updating member: {matched_member['name']}")
            
            # Extract Bio/Body
            # Prefer .ce-bodytext
            content_div = soup.find('div', {'class': 'ce-bodytext'})
            if not content_div:
                content_div = soup.find('div', {'id': 'content'})
            
            if content_div:
                # Clean up
                for tag in content_div.find_all(['nav', 'header', 'footer', 'script', 'style', 'h2']): # Remove h2 name
                    tag.decompose()
                
                # Also remove the image container if it's inside the text
                for img_div in content_div.find_all('div', {'class': 'ce-textpic'}):
                     # The image is often inside ce-textpic which also contains the body text.
                     # We want to keep the text but maybe remove the figure?
                     # In the example, ce-bodytext is INSIDE ce-textpic?
                     # Wait, looking at HTML:
                     # <div class="ce-textpic ...">
                     #   <div class="ce-gallery">...image...</div>
                     #   <div class="ce-bodytext">...content...</div>
                     # </div>
                     # So if we selected ce-bodytext, we are already outside the image gallery.
                     pass

                body_html = str(content_div).strip()
                # Only update if body is empty or very short
                if not matched_member.get('body') or len(matched_member.get('body', '')) < 50:
                     matched_member['body'] = body_html
            
            # Extract Photo
            # Look for image-embed-item inside content area to avoid sidebar images
            photo_container = soup.find('div', {'class': 'ce-textpic'})
            if not photo_container:
                photo_container = soup.find('div', {'id': 'content'})
            
            if photo_container:
                img = photo_container.find('img', {'class': 'image-embed-item'})
                if img and img.get('src'):
                    new_src = copy_asset(img['src'], source_file_path=filepath)
                    if new_src:
                        print(f"    Found photo: {new_src}")
                        matched_member['photo'] = new_src

    save_yaml(os.path.join(DATA_DIR, 'members.yml'), members_data)

def migrate_publications():
    print("Migrating Publications...")
    pubs_data = load_yaml(os.path.join(DATA_DIR, 'publications.yml'))
    existing_titles = {p.get('title', '').strip(): p for p in pubs_data.get('publications', [])}
    
    # Parse old publications page
    pubs_html = os.path.join(OLD_SITE_DIR, 'groups/arith-geom/publications.html') # Guessing path
    if not os.path.exists(pubs_html):
        # Try finding it
        for root, dirs, files in os.walk(OLD_SITE_DIR):
            if 'publications.html' in files:
                pubs_html = os.path.join(root, 'publications.html')
                break
    
    if not os.path.exists(pubs_html):
        print("Warning: Old publications page not found.")
        return

    with open(pubs_html, 'r', encoding='utf-8', errors='ignore') as f:
        soup = BeautifulSoup(f, 'html.parser')
    
    # Iterate over publication entries
    # This heavily depends on the old HTML structure.
    # Assuming standard list or divs.
    # We'll look for list items or paragraphs that look like citations.
    
    # Placeholder logic: Find all 'li' elements in a 'ul' with class 'publications'
    # This needs to be adjusted after inspecting the actual HTML
    
    # For now, let's just look for links to PDFs which are strong indicators of publications
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.endswith('.pdf'):
            # This might be a publication
            text = clean_text(a.text)
            parent = a.find_parent(['li', 'p', 'div'])
            if parent:
                full_text = clean_text(parent.text)
                # Heuristic: if text is long enough, it's a citation
                if len(full_text) > 20:
                    # Check if already exists
                    # We use a fuzzy check on the title/text
                    exists = False
                    for title in existing_titles:
                        if title in full_text or full_text in title:
                            exists = True
                            break
                    
                    if not exists:
                        print(f"  Adding new publication found via PDF: {text[:30]}...")
                        new_pub = {
                            'title': full_text, # We might need to parse this better to separate authors/title
                            'type': 'Article', # Default
                            'status': 'Other',
                            'pdfs': [{'label': 'PDF', 'file': copy_asset(href)}]
                        }
                        pubs_data['publications'].append(new_pub)

    save_yaml(os.path.join(DATA_DIR, 'publications.yml'), pubs_data)

    save_yaml(os.path.join(DATA_DIR, 'publications.yml'), pubs_data)

def build_file_map(root_dir):
    """Builds a map of filename -> list of full paths."""
    file_map = {}
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.html') or file.endswith('.pdf'):
                if file not in file_map:
                    file_map[file] = []
                file_map[file].append(os.path.join(root, file))
    return file_map

def find_best_match(url, file_map):
    """Finds the best matching file for a given URL."""
    # Extract filename from URL
    if url.endswith('/'):
        url = url[:-1]
    
    basename = os.path.basename(url)
    if '?' in basename:
        basename = basename.split('?')[0]
    if '#' in basename:
        basename = basename.split('#')[0]
        
    # Common variations
    candidates = [basename]
    if not basename.endswith('.html') and not basename.endswith('.pdf'):
        candidates.append(basename + '.html')
    
    # Try exact filename match first
    for candidate in candidates:
        if candidate in file_map:
            # If multiple, try to match parent directory
            paths = file_map[candidate]
            if len(paths) == 1:
                # If it's index.html, we need to be careful
                if candidate in ['index.html', 'index.php', 'home.html']:
                     # Check if the parent dir matches the URL
                     path_parts = paths[0].split(os.sep)
                     url_parts = url.split('/')
                     # We expect at least one significant part to match (not just 'fileadmin' or 'groups')
                     significant_matches = 0
                     for part in url_parts:
                         if part in path_parts and part not in ['http:', 'https:', '', 'www1', 'typo', 'iwr', 'uni-heidelberg', 'de', 'fileadmin', 'groups', 'arith-geom', 'templates', 'data', 'index.html', 'index.php', 'home.html']:
                             significant_matches += 1
                     
                     if significant_matches > 0:
                         return paths[0]
                     else:
                         continue # Skip this candidate
                return paths[0]
            
            # Disambiguate by checking path components
            url_parts = url.split('/')
            best_score = -1
            best_path = None
            
            for path in paths:
                score = 0
                path_parts = path.split(os.sep)
                for part in url_parts:
                    if part in path_parts:
                        score += 1
                
                # Penalize index.html if score is low
                if candidate in ['index.html', 'index.php', 'home.html']:
                    # We need a high threshold for index.html
                    # Count significant matches
                    significant_matches = 0
                    for part in url_parts:
                         if part in path_parts and part not in ['http:', 'https:', '', 'www1', 'typo', 'iwr', 'uni-heidelberg', 'de', 'fileadmin', 'groups', 'arith-geom', 'templates', 'data', 'index.html', 'index.php', 'home.html']:
                             significant_matches += 1
                    
                    if significant_matches == 0:
                        score = -1 # Discard
                
                if score > best_score:
                    best_score = score
                    best_path = path
            
            if best_score > 0:
                return best_path

    return None

def migrate_teaching():
    print("Migrating Teaching...")
    teaching_data = load_yaml(os.path.join(DATA_DIR, 'teaching.yml'))
    
    # Build file map for fast lookup
    print("  Building file map...")
    file_map = build_file_map(OLD_SITE_DIR)
    
    for course_group in teaching_data.get('courses', []):
        for semester in course_group.get('semesters', []):
            for course in semester.get('courses', []):
                links = course.get('links', [])
                # We iterate over a copy to modify the original list safely
                links_to_process = list(links)
                
                # Special handling for the broken Algebra 1 URL
                if 'testingnggg' in course.get('description', ''):
                     course['description'] = "" 

                for link in links_to_process:
                    url = link.get('url', '')
                    
                    # Check if this is a link we want to migrate
                    is_target = False
                    if 'typo.iwr.uni-heidelberg.de' in url or 'www1.iwr.uni-heidelberg.de' in url:
                        is_target = True
                    elif 'fileadmin' in url or 'groups/arith-geom' in url:
                        is_target = True
                    elif not url.startswith('http') and not url.startswith('/') and ('members/' in url or 'home/' in url or 'teaching/' in url):
                        is_target = True
                    
                    if not is_target:
                        continue

                    print(f"  Processing link for course '{course.get('title')}': {url}")
                    
                    local_path = None
                    
                    # 1. Try direct path mapping if it's a full URL
                    if url.startswith('http'):
                        # Strip domain
                        local_path_suffix = url.replace('https://typo.iwr.uni-heidelberg.de/', '')
                        local_path_suffix = local_path_suffix.replace('http://www1.iwr.uni-heidelberg.de/', '')
                        local_path_suffix = local_path_suffix.replace('https://typo.iwr.uni-heidelberg.de/', '') # typo in replace above?
                        
                        # Handle relative paths
                        while local_path_suffix.startswith('../'):
                            local_path_suffix = local_path_suffix[3:]
                        
                        if '?' in local_path_suffix:
                            local_path_suffix = local_path_suffix.split('?')[0]
                            
                        candidate = os.path.join(OLD_SITE_DIR, local_path_suffix)
                        if os.path.exists(candidate):
                            local_path = candidate
                    
                    # 2. If not found, use fuzzy matching
                    if not local_path:
                        local_path = find_best_match(url, file_map)
                    
                    if local_path and os.path.exists(local_path):
                        print(f"    -> Found local file: {local_path}")
                        
                        # Check if it is a PDF
                        if local_path.lower().endswith('.pdf'):
                            new_pdf_path = copy_asset(local_path, source_file_path=local_path)
                            if new_pdf_path:
                                if 'pdfs' not in course:
                                    course['pdfs'] = []
                                course['pdfs'].append({'label': link.get('label', 'PDF'), 'file': new_pdf_path})
                                
                                # Remove the old link
                                if link in course['links']:
                                    course['links'].remove(link)
                        else:
                            # Assume HTML
                            try:
                                with open(local_path, 'r', encoding='utf-8', errors='ignore') as f:
                                    soup = BeautifulSoup(f, 'html.parser')
                                
                                # Extract content
                                content_div = soup.find('div', {'id': 'content'})
                                if not content_div:
                                    content_div = soup.find('body')
                                    
                                if content_div:
                                    # Extract PDFs and rewrite links
                                    pdfs = []
                                    current_filename = os.path.basename(local_path)
                                    
                                    for a in content_div.find_all('a', href=True):
                                        href = a['href']
                                        
                                        # Fix internal anchor links (e.g. seminar-ws2013.html#c3051 -> #c3051)
                                        if '#' in href:
                                            url_part, anchor_part = href.split('#', 1)
                                            if url_part == current_filename or url_part == '':
                                                a['href'] = '#' + anchor_part
                                                continue
                                        
                                        if href.endswith('.pdf'):
                                            new_pdf_path = copy_asset(href, source_file_path=local_path)
                                            if new_pdf_path:
                                                pdfs.append({'label': clean_text(a.text) or "PDF", 'file': new_pdf_path})
                                                # Update the link in the body to point to the new asset
                                                print(f"      Rewriting PDF link: {href} -> {new_pdf_path}")
                                                a['href'] = new_pdf_path
                                        elif 'fileadmin' in href or 'typo.iwr' in href:
                                            # Try to migrate other assets or fix links
                                            # For now, just try to copy if it looks like a file
                                            if '.' in os.path.basename(href):
                                                 new_asset_path = copy_asset(href, source_file_path=local_path)
                                                 if new_asset_path:
                                                     print(f"      Rewriting asset link: {href} -> {new_asset_path}")
                                                     a['href'] = new_asset_path
                                    
                                    if pdfs:
                                        if 'pdfs' not in course:
                                            course['pdfs'] = []
                                        
                                        existing_files = {p.get('file') for p in course['pdfs']}
                                        for pdf in pdfs:
                                            if pdf['file'] not in existing_files:
                                                course['pdfs'].append(pdf)
                                                existing_files.add(pdf['file'])
                                    
                                    # Update Body
                                    # Always update to ensure it's clean and has rewritten links
                                    cleaned_body = clean_html_content(content_div)
                                    # Verify if link is present in cleaned body
                                    if 'AnkuendigungDeterminants.pdf' in cleaned_body and '/assets/migrated/' not in cleaned_body.split('AnkuendigungDeterminants.pdf')[0][-20:]:
                                         print("      WARNING: Link not rewritten in cleaned body!")
                                    course['body'] = cleaned_body
                                    
                                    # Remove the old link as we have migrated content
                                    if link in course['links']:
                                        course['links'].remove(link)
                            except Exception as e:
                                print(f"    Error processing HTML {local_path}: {e}")
                    else:
                        # Link matched old site patterns but file was not found or didn't exist
                        print(f"    -> Could not find local file for: {url}. Removing broken link.")
                        if link in course['links']:
                            course['links'].remove(link)

                # Cleanup invalid PDFs (e.g. "ssss")
                if 'pdfs' in course:
                    course['pdfs'] = [p for p in course['pdfs'] if p.get('label') != 'ssss']

    # New pass: Fix existing body content for all courses
    print("Fixing existing body content...")
    for course_group in teaching_data.get('courses', []):
        for semester in course_group.get('semesters', []):
            for course in semester.get('courses', []):
                if 'body' in course and course['body']:
                    soup = BeautifulSoup(course['body'], 'html.parser')
                    modified = False
                    
                    # We don't have the local_path easily here, but we can try to find it or just fix what we can
                    # For internal links, we don't need local_path if we assume self-reference
                    # For assets, we need to know where they might be.
                    # However, if the asset link is absolute or relative, we might struggle without context.
                    # But wait, the broken links are like ../../../../fileadmin...
                    # We can try to resolve them relative to the root of typo_mirror if we assume they are relative to some deep path.
                    # Or better: search for the filename in file_map!
                    
                    pdfs = []
                    for a in soup.find_all('a', href=True):
                        href = a['href']
                        
                        # Fix internal anchor links (e.g. seminar-ws2013.html#c3051 -> #c3051)
                        if '#' in href:
                            url_part, anchor_part = href.split('#', 1)
                            # Heuristic: if url_part ends with .html and is not a full URL
                            if url_part.endswith('.html') and 'http' not in url_part:
                                # We assume it's a self-reference if it's just a filename or relative path
                                # that matches the likely original filename.
                                # Since we don't know the original filename easily, let's just strip it if it looks like a local file link
                                # and we are in a context where we expect self-references (like TOCs).
                                a['href'] = '#' + anchor_part
                                modified = True
                                continue
                        
                        # Fix asset links using file_map
                        if 'fileadmin' in href or 'typo.iwr' in href or href.endswith('.pdf'):
                            filename = os.path.basename(href)
                            # Remove query params
                            if '?' in filename:
                                filename = filename.split('?')[0]
                            
                            if filename in file_map:
                                candidates = file_map[filename]
                                if candidates:
                                    # Just pick the first one for now
                                    local_path = candidates[0]
                                    if os.path.exists(local_path):
                                        new_asset_path = copy_asset(local_path, source_file_path=local_path) # source_file_path doesn't matter much if absolute
                                        if new_asset_path:
                                            a['href'] = new_asset_path
                                            modified = True
                                            
                                            if local_path.lower().endswith('.pdf'):
                                                pdfs.append({'label': clean_text(a.text) or "PDF", 'file': new_asset_path})

                    if pdfs:
                        if 'pdfs' not in course:
                            course['pdfs'] = []
                        existing_files = {p.get('file') for p in course['pdfs']}
                        for pdf in pdfs:
                            if pdf['file'] not in existing_files:
                                course['pdfs'].append(pdf)
                                existing_files.add(pdf['file'])
                                modified = True

                    if modified:
                        course['body'] = str(soup)

    save_yaml(os.path.join(DATA_DIR, 'teaching.yml'), teaching_data)

def enrich_past_teaching():
    print("Enriching Past Teaching (Duisburg)...")
    teaching_data = load_yaml(os.path.join(DATA_DIR, 'teaching.yml'))
    past_teaching_file = os.path.join(OLD_SITE_DIR, 'groups', 'arith-geom', 'teaching', 'past-teaching.html')
    
    if not os.path.exists(past_teaching_file):
        print(f"  Error: {past_teaching_file} not found.")
        return

    with open(past_teaching_file, 'r', encoding='utf-8', errors='ignore') as f:
        soup = BeautifulSoup(f, 'html.parser')

    content_div = soup.find('div', {'id': 'content'})
    if not content_div:
        return

    # The structure is h4 (Term) -> ul (Courses) -> li (Course)
    # We need to map "Winter term 2009/2010" to "Winter term 2009/2010 (Duisburg-Essen)" 
    # or just match by title within the year.
    
    current_term = None
    
    # Iterate through siblings
    for element in content_div.find_all(['h4', 'ul']):
        if element.name == 'h4':
            current_term = clean_text(element.text)
            # print(f"  Found term: {current_term}")
        elif element.name == 'ul' and current_term:
            for li in element.find_all('li'):
                # Extract course title. It's usually the text before the first parenthesis or just the text.
                # Example: "Arbeitsgemeinschaft: The Eigencurve (mit U. Goertz und G. Wiese)"
                # Example: "Mathematik Vorkurs (Dr. Cerviño)"
                
                full_text = clean_text(li.text)
                title_part = full_text.split('(')[0].strip()
                
                # Find matching course in teaching_data
                matched_course = None
                
                # We search through all courses to find a match. 
                # Since we know the approximate year from the term, we could optimize, but global search is safer.
                for course_group in teaching_data.get('courses', []):
                    for semester in course_group.get('semesters', []):
                        # Check if semester matches roughly? 
                        # The semester names in teaching.yml are like "Winter term 2009/2010 (Duisburg-Essen)"
                        # The h4 is "Winter term 2009/2010"
                        # So we can check if h4 text is IN semester name.
                        
                        if current_term in semester.get('semester', ''):
                             for course in semester.get('courses', []):
                                 # Fuzzy match title
                                 c_title = course.get('title', '').lower()
                                 t_part = title_part.lower()
                                 
                                 # Check for containment or high similarity
                                 if t_part in c_title or c_title in t_part:
                                     matched_course = course
                                     break
                        if matched_course: break
                    if matched_course: break
                
                if matched_course:
                    # print(f"    Matched: {title_part} -> {matched_course.get('title')}")
                    
                    # Extract PDFs
                    pdfs = []
                    for a in li.find_all('a', href=True):
                        if a['href'].endswith('.pdf'):
                            # Resolve relative path. 
                            # past-teaching.html is in groups/arith-geom/teaching/
                            # links are like ../../../fileadmin/...
                            # copy_asset handles this if we pass source_file_path
                            
                            new_pdf_path = copy_asset(a['href'], source_file_path=past_teaching_file)
                            if new_pdf_path:
                                pdfs.append({'label': clean_text(a.text) or "PDF", 'file': new_pdf_path})
                    
                    if pdfs:
                        if 'pdfs' not in matched_course:
                            matched_course['pdfs'] = []
                        
                        existing_files = {p.get('file') for p in matched_course['pdfs']}
                        added_count = 0
                        for pdf in pdfs:
                            if pdf['file'] not in existing_files:
                                matched_course['pdfs'].append(pdf)
                                existing_files.add(pdf['file'])
                                added_count += 1
                        
                        if added_count > 0:
                            print(f"    Added {added_count} PDFs to: {matched_course.get('title')}")

    save_yaml(os.path.join(DATA_DIR, 'teaching.yml'), teaching_data)

def migrate_recent_teaching():
    print("Migrating Recent Teaching (2020-2025)...")
    teaching_data = load_yaml(os.path.join(DATA_DIR, 'teaching.yml'))
    teaching_file = os.path.join(OLD_SITE_DIR, 'groups', 'arith-geom', 'teaching.html')
    
    if not os.path.exists(teaching_file):
        print(f"  Error: {teaching_file} not found.")
        return

    with open(teaching_file, 'r', encoding='utf-8', errors='ignore') as f:
        soup = BeautifulSoup(f, 'html.parser')

    content_div = soup.find('div', {'id': 'content'})
    if not content_div:
        return

    current_term = None
    
    # Iterate through siblings
    for element in content_div.find_all(['h4', 'ul']):
        if element.name == 'h4':
            current_term = clean_text(element.text)
            # print(f"  Found term: {current_term}")
        elif element.name == 'ul' and current_term:
            # Parse Year from Term
            # "Summer term 2025" -> 2025
            # "Winter term 2024/25" -> 2024
            year = None
            try:
                if 'Winter term' in current_term:
                    year = int(current_term.split(' ')[2].split('/')[0])
                elif 'Summer term' in current_term:
                    year = int(current_term.split(' ')[2])
            except:
                print(f"  Warning: Could not parse year from {current_term}")
                continue
            
            if year and year >= 2020:
                # print(f"  Processing {current_term} ({year})")
                
                # Ensure Year exists
                year_entry = next((y for y in teaching_data.get('courses', []) if y.get('year') == year), None)
                if not year_entry:
                    year_entry = {'year': year, 'semesters': []}
                    # Insert at beginning to keep sorted descending
                    teaching_data['courses'].insert(0, year_entry)
                    # Resort just in case
                    teaching_data['courses'].sort(key=lambda x: x.get('year', 0), reverse=True)
                
                # Ensure Semester exists
                semester_entry = next((s for s in year_entry['semesters'] if s.get('semester') == current_term), None)
                if not semester_entry:
                    semester_entry = {'semester': current_term, 'courses': []}
                    year_entry['semesters'].append(semester_entry)
                
                for li in element.find_all('li'):
                    full_text = clean_text(li.text)
                    # Split title and instructor
                    # Format: "Title" (Instructor)
                    # Sometimes Title is a link
                    
                    title = full_text
                    instructor = ""
                    
                    if '(' in full_text and full_text.endswith(')'):
                        parts = full_text.rsplit('(', 1)
                        title = parts[0].strip()
                        instructor = parts[1][:-1].strip()
                    
                    # Clean title (remove quotes if present)
                    title = title.replace('"', '').strip()
                    
                    # Check if course exists
                    course_entry = next((c for c in semester_entry['courses'] if c.get('title') == title), None)
                    if not course_entry:
                        course_entry = {
                            'title': title,
                            'instructor': instructor,
                            'course_type': 'Lecture' if 'Vorlesung' in full_text or 'Lecture' in full_text else 'Seminar'
                        }
                        semester_entry['courses'].append(course_entry)
                        print(f"    Added course: {title}")
                    
                    # Extract Links and PDFs
                    links = []
                    pdfs = []
                    
                    for a in li.find_all('a', href=True):
                        href = a['href']
                        label = clean_text(a.text) or "Link"
                        
                        if href.endswith('.pdf'):
                            new_pdf_path = copy_asset(href, source_file_path=teaching_file)
                            if new_pdf_path:
                                pdfs.append({'label': label, 'file': new_pdf_path})
                        else:
                            # External or internal link
                            if 'typo.iwr.uni-heidelberg.de' in href or href.startswith('http'):
                                links.append({'label': label, 'url': href})
                            else:
                                # Relative link, maybe to a member page or subpage
                                # We can keep it as is or try to resolve it.
                                # For now, let's just keep the raw href if it looks like a page
                                links.append({'label': label, 'url': href})

                    if links:
                        if 'links' not in course_entry:
                            course_entry['links'] = []
                        # Add unique links
                        existing_urls = {l.get('url') for l in course_entry['links']}
                        for link in links:
                            if link['url'] not in existing_urls:
                                course_entry['links'].append(link)
                                existing_urls.add(link['url'])

                    if pdfs:
                        if 'pdfs' not in course_entry:
                            course_entry['pdfs'] = []
                        # Add unique pdfs
                        existing_files = {p.get('file') for p in course_entry['pdfs']}
                        for pdf in pdfs:
                            if pdf['file'] not in existing_files:
                                course_entry['pdfs'].append(pdf)
                                existing_files.add(pdf['file'])

    save_yaml(os.path.join(DATA_DIR, 'teaching.yml'), teaching_data)

def clean_html_content(soup):
    """Cleans the HTML content from TYPO3 wrappers."""
    if not soup:
        return ""
    
    # Remove breadcrumbs
    for div in soup.find_all('div', {'class': 'pathway'}):
        div.decompose()
        
    # Remove footer/bearbeiter
    for div in soup.find_all('div', {'class': 'bearbeiter'}):
        # Safer removal: just remove the table if it is a table
        p = div.parent
        while p and p.name != 'table' and p.name != 'div':
            p = p.parent
        
        if p and p.name == 'table':
            p.decompose()
        else:
            div.decompose()
        
    # Remove TYPO3 frames/wrappers but keep content
    # We want to keep the semantic content.
    # Often content is in <div class="frame ...">
    
    # Let's just return the inner HTML of the content div, but cleaned.
    # Remove empty paragraphs
    for p in soup.find_all('p'):
        if not p.text.strip() and not p.find('img'):
            p.decompose()
            
    # Resolve relative links
    for a in soup.find_all('a', href=True):
        href = a['href']
        if 'fileadmin' in href:
            # It's an asset. We should copy it?
            # copy_asset handles this.
            # But we need to update the link in the HTML to point to the new asset.
            # This is tricky because copy_asset needs the source path.
            # We'll assume we can pass the source path if we have it.
            pass

    return str(soup).strip()

if __name__ == "__main__":
    migrate_members()
    migrate_publications()
    migrate_recent_teaching()
    migrate_teaching()
    enrich_past_teaching()
