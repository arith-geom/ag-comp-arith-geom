import os
import re
import requests
from bs4 import BeautifulSoup
import yaml
from urllib.parse import urljoin, urlparse

# Configuration
BASE_URL = "https://typo.iwr.uni-heidelberg.de/groups/arith-geom/"
MEMBERS_URLS = [
    BASE_URL,
    urljoin(BASE_URL, "members.html"),
    urljoin(BASE_URL, "alumni.html"),
]
MEMBERS_DIR = "../_members"
PHOTOS_DIR = "../assets/img"

# Ensure output directories exist
os.makedirs(MEMBERS_DIR, exist_ok=True)
os.makedirs(PHOTOS_DIR, exist_ok=True)

def slugify(name):
    return (
        name.lower()
        .replace(" ", "-")
        .replace(".", "")
        .replace(",", "")
        .replace("'", "")
        .replace("\u00e4", "ae")
        .replace("\u00f6", "oe")
        .replace("\u00fc", "ue")
        .replace("\u00df", "ss")
        .replace("\u00f8", "oe")
        .replace("\u00e5", "aa")
    )

def download_photo(photo_url, name):
    if not photo_url:
        return None
    filename = slugify(name) + os.path.splitext(urlparse(photo_url).path)[-1]
    filepath = os.path.join(PHOTOS_DIR, filename)
    try:
        r = requests.get(photo_url, timeout=10)
        if r.status_code == 200:
            with open(filepath, "wb") as f:
                f.write(r.content)
            return "/assets/img/" + filename
    except Exception:
        pass
    return None

def extract_members_from_text(text):
    """Extract member information from the text content of the members page."""
    members = []
    
    # Split by sections
    sections = text.split('\n')
    current_section = None
    current_members = []
    
    for line in sections:
        line = line.strip()
        if not line:
            continue
            
        # Detect sections
        if 'head' in line.lower():
            current_section = 'head'
            current_members = []
        elif 'secretary' in line.lower():
            current_section = 'secretary'
            current_members = []
        elif 'members' in line.lower() and 'former' not in line.lower():
            current_section = 'members'
            current_members = []
        elif 'former' in line.lower():
            current_section = 'former'
            current_members = []
        elif current_section and line:
            # Extract names from the line
            # Look for patterns like "Prof. Dr. Gebhard Boeckle", "Dr. Andrea Conti", etc.
            names = re.findall(r'(?:Prof\.\s*)?(?:Dr\.\s*)?([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', line)
            for name in names:
                if len(name.split()) >= 2:  # At least first and last name
                    # Determine role based on section
                    if current_section == 'head':
                        role = 'Professor & Group Leader'
                        status = 'active'
                    elif current_section == 'secretary':
                        role = 'Secretary'
                        status = 'active'
                    elif current_section == 'members':
                        role = 'PhD Student'  # Default, will be refined
                        status = 'active'
                    elif current_section == 'former':
                        role = 'Alumni'
                        status = 'alumni'
                    else:
                        role = 'Member'
                        status = 'active'
                    
                    # Refine role based on name patterns
                    if 'Prof.' in line or 'Professor' in line:
                        role = 'Professor'
                    elif 'Dr.' in line and 'Prof.' not in line:
                        role = 'Postdoctoral Researcher'
                    
                    members.append({
                        'name': name,
                        'role': role,
                        'status': status,
                        'email': None,  # Will be filled later
                        'photo_url': None,
                        'bio': '',
                        'research': '',
                        'links': []
                    })
    
    return members

def scrape_and_update():
    all_members = []
    
    for url in MEMBERS_URLS:
        print(f"Scraping {url}")
        try:
            r = requests.get(url, timeout=30)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'html.parser')
                text_content = soup.get_text()
                members = extract_members_from_text(text_content)
                all_members.extend(members)
                print(f"Found {len(members)} members from {url}")
        except Exception as e:
            print(f"Error scraping {url}: {e}")
    
    # Remove duplicates based on name
    unique_members = {}
    for member in all_members:
        name = member['name']
        if name not in unique_members:
            unique_members[name] = member
        else:
            # Merge information if needed
            existing = unique_members[name]
            if member['role'] != 'Member':
                existing['role'] = member['role']
            if member['status'] != 'active':
                existing['status'] = member['status']
    
    print(f"Total unique members found: {len(unique_members)}")
    
    # Write member files
    for name, member in unique_members.items():
        write_member_md(member)
        print(f"Created/updated: {name}")

def write_member_md(member):
    if not member["name"]:
        return
    
    slug = slugify(member["name"])
    md_path = os.path.join(MEMBERS_DIR, f"{slug}.md")
    
    # Download photo if available
    photo_path = download_photo(member["photo_url"], member["name"])
    
    # Prepare front matter
    front = {
        "name": member["name"],
        "email": member["email"] or "arithgeo@iwr.uni-heidelberg.de",
        "layout": "member",
        "role": member["role"],
        "status": member["status"],
        "order": 1,  # Default order
    }
    
    if photo_path:
        front["photo"] = photo_path
    
    if member["research"]:
        front["research_interests"] = member["research"]
    
    # Remove None values
    front = {k: v for k, v in front.items() if v}
    
    # Write markdown file
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("---\n")
        yaml.dump(front, f, allow_unicode=True, sort_keys=False)
        f.write("---\n\n")
        
        # Add basic bio if available
        if member["bio"]:
            f.write(member["bio"] + "\n\n")
        else:
            # Generate basic bio based on role
            if member["role"] == "Professor & Group Leader":
                f.write(f"{member['name']} is the head of the research group \"Computational Arithmetic Geometry\" at the Interdisciplinary Center for Scientific Computing (IWR) in Heidelberg.\n\n")
            elif member["status"] == "alumni":
                f.write(f"{member['name']} was a member of the AG Computational Arithmetic Geometry research group at the University of Heidelberg.\n\n")
            else:
                f.write(f"{member['name']} is a member of the AG Computational Arithmetic Geometry research group at the University of Heidelberg.\n\n")

if __name__ == "__main__":
    scrape_and_update()
    print("Scraping and update complete.")
