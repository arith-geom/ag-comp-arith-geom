import yaml
import os
import re

# Paths
data_file = '_data/members.yml'
members_dir = '_members'

# Read data file
with open(data_file, 'r') as f:
    data = yaml.safe_load(f)

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def find_member_file(name):
    # Try exact match first (slugified)
    slug = slugify(name)
    filename = f"{slug}.md"
    path = os.path.join(members_dir, filename)
    if os.path.exists(path):
        return path
    
    # Try searching for file containing the name
    for f in os.listdir(members_dir):
        if f.endswith('.md'):
            with open(os.path.join(members_dir, f), 'r') as file:
                content = file.read()
                if f"name: {name}" in content:
                    return os.path.join(members_dir, f)
    return None

# Iterate sections
for section in data['sections']:
    section_title = section['title']
    print(f"Processing section: {section_title}")
    
    if 'members' not in section:
        continue
        
    for index, member in enumerate(section['members']):
        name = member['name']
        path = find_member_file(name)
        
        if path:
            print(f"  Found file for {name}: {path}")
            
            with open(path, 'r') as f:
                content = f.read()
            
            # Parse front matter
            parts = content.split('---')
            if len(parts) >= 3:
                front_matter = parts[1]
                body = '---'.join(parts[2:])
                
                # Update/Add fields
                # We'll use simple string replacement or appending for safety to avoid ruining formatting
                # But yaml parser is safer for structure. Let's try to parse front matter as yaml.
                
                try:
                    fm_yaml = yaml.safe_load(front_matter)
                    if fm_yaml is None: fm_yaml = {}
                    
                    # Update fields
                    fm_yaml['group'] = section_title
                    fm_yaml['order'] = index + 1
                    
                    # Ensure other fields from data are present if missing in file
                    if 'role' not in fm_yaml and 'role' in member:
                        fm_yaml['role'] = member['role']
                    if 'photo' not in fm_yaml and 'photo' in member:
                        fm_yaml['photo'] = member['photo']
                    # Description in data is usually short, body in file is long. 
                    # If file has no body and data has description, maybe move it? 
                    # But user said "combine", usually profile has more info.
                    # Let's just stick to group and order for now to fix the structure.
                    
                    # Reconstruct file
                    new_front_matter = yaml.dump(fm_yaml, sort_keys=False, allow_unicode=True)
                    new_content = f"---\n{new_front_matter}---\n{body}"
                    
                    with open(path, 'w') as f:
                        f.write(new_content)
                        
                except Exception as e:
                    print(f"    Error parsing YAML for {name}: {e}")
        else:
            print(f"  WARNING: No file found for {name}")
            # Create file if missing?
            # For now just warn.
