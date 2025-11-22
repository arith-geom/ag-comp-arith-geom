import yaml
import os
import re

# Paths
members_dir = '_members'
data_file = '_data/members.yml'

# Read existing data file (which currently only has sections)
with open(data_file, 'r') as f:
    data = yaml.safe_load(f)

# Helper to find section by title
def find_section(title):
    for section in data['sections']:
        if section['title'] == title:
            return section
    return None

# Helper to parse front matter and body
def parse_file(path):
    with open(path, 'r') as f:
        content = f.read()
    
    parts = content.split('---')
    if len(parts) >= 3:
        front_matter = yaml.safe_load(parts[1])
        body = '---'.join(parts[2:]).strip()
        return front_matter, body
    return None, None

# Iterate over member files
member_files = [f for f in os.listdir(members_dir) if f.endswith('.md')]

# We need to sort them by 'order' first to maintain the order in the list
members_to_add = []

for filename in member_files:
    path = os.path.join(members_dir, filename)
    fm, body = parse_file(path)
    
    if fm:
        member = fm.copy()
        member['body'] = body
        # Remove internal fields
        member.pop('layout', None)
        # Keep group and order for sorting/placing
        members_to_add.append(member)

# Sort by order
members_to_add.sort(key=lambda x: x.get('order', 999))

# Add to sections
for member in members_to_add:
    group = member.get('group', 'Members')
    section = find_section(group)
    
    if section:
        if 'members' not in section:
            section['members'] = []
        
        # Clean up member object for data file
        # Remove 'group' and 'order' from the object itself if we are using list position?
        # The user wants drag and drop. Pages CMS list widget uses the array order.
        # So we don't strictly need 'order' field anymore if the array order is correct.
        # But we should keep 'group' if we want to be safe, or maybe not needed if nested.
        # Let's keep 'group' for reference but rely on nesting.
        
        # Remove 'order' as it will be implicit in the list
        member.pop('order', None)
        
        section['members'].append(member)
    else:
        print(f"Warning: Section '{group}' not found for {member.get('name')}")

# Write back to data file
with open(data_file, 'w') as f:
    yaml.dump(data, f, sort_keys=False, allow_unicode=True)

print("Migration complete.")
