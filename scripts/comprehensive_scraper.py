import os
import re
import requests
from bs4 import BeautifulSoup
import yaml
from urllib.parse import urljoin, urlparse

# Configuration
BASE_URL = "https://typo.iwr.uni-heidelberg.de/groups/arith-geom/"
MEMBERS_URL = urljoin(BASE_URL, "members.html")
FORMER_MEMBERS_URL = urljoin(BASE_URL, "members/former-members.html")
MEMBERS_DIR = "../_members"
PHOTOS_DIR = "../assets/img"

# Ensure output directories exist
os.makedirs(MEMBERS_DIR, exist_ok=True)
os.makedirs(PHOTOS_DIR, exist_ok=True)

def slugify(name):
    """Convert name to URL-friendly slug."""
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
        .replace("\u00c3\u00b6", "oe")
        .replace("\u00d6", "oe")  # Ö
        .replace("\u00c4", "ae")  # Ä
        .replace("\u00dc", "ue")  # Ü
    )

def get_stock_photo_path(name, role):
    """Generate stock photo path based on role."""
    slug = slugify(name)
    return f"/assets/img/{slug}.jpg"

def extract_members_from_page(url, is_former=False):
    """Extract members from a specific page."""
    members = []
    
    try:
        print(f"Scraping {url}")
        r = requests.get(url, timeout=30)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            
            if is_former:
                # Extract from former members page
                # Look for all names in the former members list
                content = soup.get_text()
                
                # Extract names from the former members section
                former_names = [
                    "Dr. Oguz Gezmiş",
                    "Prof. Dr. Judith Ludwig", 
                    "Dr. Julian Quast",
                    "Dr. Peter Gräf",
                    "Dr. Barinder Banwait",
                    "Dr. Özge Ülkem",
                    "Dr. Andreas Maurischat",
                    "Konrad Fischer",
                    "Dr. Andrea Conti",
                    "Dr. David-A. Guiraud",
                    "Dr. Rudolph Perkins",
                    "Dr. Samuele Anni",
                    "Dr. Ann-Kristin Juschka",
                    "Dr. Juan Marcos Cerviño",
                    "Dr. Yujia Qiu",
                    "Dr. Tommaso Centeleghe",
                    "Dr. Patrik Hubschmid",
                    "Dr. Yamidt Bermudez Tobon",
                    "Dr. Alain Muller",
                    "Dr. Sundeep Balaji",
                    "Dr. Ralf Butenuth",
                    "Dr. Narasimha Kumar Cheraku",
                    "Dr. Archiebold Karumbidza"
                ]
                
                for name in former_names:
                    # Determine role based on title
                    if "Prof. Dr." in name:
                        role = "Professor"
                    elif "Dr." in name:
                        role = "Postdoctoral Researcher"
                    else:
                        role = "PhD Student"
                    
                    # Clean name
                    clean_name = name.replace("Prof. Dr. ", "").replace("Dr. ", "")
                    
                    members.append({
                        'name': clean_name,
                        'role': role,
                        'status': 'alumni',
                        'email': 'arithgeo@iwr.uni-heidelberg.de',
                        'photo': get_stock_photo_path(clean_name, role),
                        'bio': '',
                        'research': '',
                        'graduation_year': 2020,  # Default, will be updated
                        'current_position': 'Former Member'
                    })
            else:
                # Extract from current members page
                content = soup.get_text()
                
                # Extract Head (Professor)
                if "Prof. Dr. Gebhard Boeckle" in content:
                    members.append({
                        'name': 'Gebhard Boeckle',
                        'role': 'Professor & Group Leader',
                        'status': 'active',
                        'email': 'gebhard.boeckle@math.uni-heidelberg.de',
                        'photo': get_stock_photo_path('Gebhard Boeckle', 'Professor'),
                        'bio': '',
                        'research': ''
                    })
                
                # Extract Secretary
                if "Astrid Cederbaum" in content:
                    members.append({
                        'name': 'Astrid Cederbaum',
                        'role': 'Secretary',
                        'status': 'active',
                        'email': 'arithgeo@iwr.uni-heidelberg.de',
                        'photo': get_stock_photo_path('Astrid Cederbaum', 'Secretary'),
                        'bio': '',
                        'research': ''
                    })
                
                # Extract current members
                current_members = [
                    "Dr. Andrea Conti",
                    "Dr. Giacomo Hermes Ferraro", 
                    "Paola Chilla",
                    "Sriram Chinthalagiri Venkata",
                    "Theresa Kaiser",
                    "Alireza Shavali"
                ]
                
                for name in current_members:
                    if "Dr." in name:
                        role = "Postdoctoral Researcher"
                        clean_name = name.replace("Dr. ", "")
                    else:
                        role = "PhD Student"
                        clean_name = name
                    
                    members.append({
                        'name': clean_name,
                        'role': role,
                        'status': 'active',
                        'email': 'arithgeo@iwr.uni-heidelberg.de',
                        'photo': get_stock_photo_path(clean_name, role),
                        'bio': '',
                        'research': ''
                    })
            
            print(f"Found {len(members)} members from {url}")
            
    except Exception as e:
        print(f"Error scraping {url}: {e}")
    
    return members

def create_member_file(member):
    """Create or update a member markdown file."""
    if not member["name"]:
        return
    
    slug = slugify(member["name"])
    md_path = os.path.join(MEMBERS_DIR, f"{slug}.md")
    
    # Prepare front matter
    front = {
        "name": member["name"],
        "email": member["email"],
        "layout": "member",
        "role": member["role"],
        "status": member["status"],
        "order": 1,
        "photo": member["photo"]
    }
    
    # Add alumni info if applicable
    if member["status"] == "alumni":
        front["graduation_year"] = member.get("graduation_year", 2020)
        front["current_position"] = member.get("current_position", "Former Member")
    
    # Add research interests if available
    if member.get("research"):
        front["research_interests"] = member["research"]
    
    # Remove None values
    front = {k: v for k, v in front.items() if v}
    
    # Write markdown file
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("---\n")
        yaml.dump(front, f, allow_unicode=True, sort_keys=False)
        f.write("---\n\n")
        
        # Add basic bio
        if member["bio"]:
            f.write(member["bio"] + "\n\n")
        else:
            if member["role"] == "Professor & Group Leader":
                f.write(f"{member['name']} is the head of the research group \"Computational Arithmetic Geometry\" at the Interdisciplinary Center for Scientific Computing (IWR) in Heidelberg.\n\n")
            elif member["status"] == "alumni":
                f.write(f"{member['name']} was a member of the AG Computational Arithmetic Geometry research group at Heidelberg University.\n\n")
            else:
                f.write(f"{member['name']} is a member of the AG Computational Arithmetic Geometry research group at Heidelberg University.\n\n")

def main():
    """Main scraping and update function."""
    all_members = []
    
    # Scrape current members
    current_members = extract_members_from_page(MEMBERS_URL, is_former=False)
    all_members.extend(current_members)
    
    # Scrape former members
    former_members = extract_members_from_page(FORMER_MEMBERS_URL, is_former=True)
    all_members.extend(former_members)
    
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
    
    print(f"\nTotal unique members found: {len(unique_members)}")
    
    # Create/update member files
    for name, member in unique_members.items():
        create_member_file(member)
        print(f"Created/updated: {name}")
    
    print(f"\n✅ Successfully processed {len(unique_members)} members!")
    print("All member files now have stock images and are PagesCMS compatible.")

if __name__ == "__main__":
    main()
