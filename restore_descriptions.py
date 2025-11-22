import yaml
import os
import re

# Paths
members_dir = '_members'

# Old data content (from step 12)
old_data_yaml = """
sections:
- title: Head
  layout: big
  members:
  - name: Prof. Dr. Gebhard Böckle
    role: Group Leader
    photo: /assets/img/gebhard-boeckle.jpg
- title: Secretary
  layout: big
  members:
  - name: Astrid Cederbaum
    role: Secretary
    photo: /assets/img/astrid-cederbaum.jpg
- title: Members
  layout: medium
  members:
  - name: Dr. Andrea Conti
    role: Researcher
    photo: /assets/img/andrea-conti.jpg
  - name: Dr. Giacomo Hermes Ferraro
    role: Researcher
    photo: /assets/img/giacomo-hermes-ferraro.jpg
    description: dsadsadasdas
  - name: Paola Chilla
    role: PhD Student
    photo: /assets/img/paola-chilla.jpg
  - name: Sriram Chinthalagiri Venkata
    role: PhD Student
    photo: /assets/img/sriram-chinthalagiri-venkata.jpg
  - name: Theresa Kaiser
    role: PhD Student
    photo: /assets/img/theresa-kaiser.jpg
  - name: Alireza Shavali
    role: PhD Student
    photo: /assets/img/alireza-shavali.jpg
- title: Former Members
  layout: small
  members:
  - name: Dr. Oguz Gezmiş
    role: Former Member
    photo: /assets/img/oguz-gezmis.jpg
  - name: Prof. Dr. Judith Ludwig
    role: Former Member
    photo: /assets/img/judith-ludwig.jpg
  - name: Dr. Julian Quast
    role: Former Member
    photo: /assets/img/julian-quast.jpg
  - name: Dr. Peter Gräf
    role: Former Member
    photo: /assets/img/peter-graef.jpg
  - name: Dr. Barinder Banwait
    role: Former Member
    photo: /assets/img/barinder-banwait.jpg
  - name: Dr. Özge Ülkem
    role: Former Member
    photo: /assets/img/oezge-uelkem.jpg
  - name: Dr. Andreas Maurischat
    role: Former Member
    photo: /assets/img/andreas-maurischat.jpg
  - name: Konrad Fischer
    role: Former Member
    photo: /assets/img/konrad-fischer.jpg
  - name: Dr. David-A. Guiraud
    role: Former Member
    photo: /assets/img/david-a-guiraud.jpg
  - name: Dr. Rudolph Perkins
    role: Former Member
    photo: /assets/img/rudolph-perkins.jpg
  - name: Dr. Samuele Anni
    role: Former Member
    photo: /assets/img/samuele-anni.jpg
  - name: Dr. Ann-Kristin Juschka
    role: Former Member
    photo: /assets/img/ann-kristin-juschka.jpg
  - name: Dr. Juan Marcos Cerviño
    role: Former Member
    photo: /assets/img/juan-marcos-cervino.jpg
  - name: Dr. Yujia Qiu
    role: Former Member
    photo: /assets/img/yujia-qiu.jpg
  - name: Dr. Tommaso Centeleghe
    role: Former Member
    photo: /assets/img/tommaso-centeleghe.jpg
  - name: Dr. Patrik Hubschmid
    role: Former Member
    photo: /assets/img/patrik-hubschmid.jpg
  - name: Dr. Yamidt Bermudez Tobon
    role: Former Member
    photo: /assets/img/yamidt-bermudez-tobon.jpg
  - name: Dr. Alain Muller
    role: Former Member
    photo: /assets/img/alain-muller.jpg
  - name: Dr. Sundeep Balaji
    role: Former Member
    photo: /assets/img/sundeep-balaji.jpg
  - name: Dr. Ralf Butenuth
    role: Former Member
    photo: /assets/img/ralf-butenuth.jpg
  - name: Dr. Narasimha Kumar Cheraku
    role: Former Member
    photo: /assets/img/narasimha-kumar-cheraku.jpg
  - name: Dr. Archiebold Karumbidza
    role: Former Member
    photo: /assets/img/archiebold-karumbidza.jpg
"""

data = yaml.safe_load(old_data_yaml)

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
    if 'members' not in section:
        continue
        
    for member in section['members']:
        if 'description' in member:
            name = member['name']
            description = member['description']
            path = find_member_file(name)
            
            if path:
                print(f"Restoring description for {name} in {path}")
                
                with open(path, 'r') as f:
                    content = f.read()
                
                # Parse front matter
                parts = content.split('---')
                if len(parts) >= 3:
                    front_matter = parts[1]
                    body = '---'.join(parts[2:])
                    
                    try:
                        fm_yaml = yaml.safe_load(front_matter)
                        if fm_yaml is None: fm_yaml = {}
                        
                        # Add description
                        fm_yaml['description'] = description
                        
                        # Reconstruct file
                        new_front_matter = yaml.dump(fm_yaml, sort_keys=False, allow_unicode=True)
                        new_content = f"---\n{new_front_matter}---\n{body}"
                        
                        with open(path, 'w') as f:
                            f.write(new_content)
                            
                    except Exception as e:
                        print(f"    Error parsing YAML for {name}: {e}")
