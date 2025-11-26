import os
import yaml

members_dir = "_members"

for filename in os.listdir(members_dir):
    if not filename.endswith(".md"):
        continue

    filepath = os.path.join(members_dir, filename)
    
    with open(filepath, "r") as f:
        content = f.read()

    # Split front matter
    parts = content.split("---", 2)
    if len(parts) < 3:
        print(f"Skipping {filename}: Invalid front matter format")
        continue

    front_matter_raw = parts[1]
    body = parts[2]

    try:
        data = yaml.safe_load(front_matter_raw)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML in {filename}: {e}")
        continue

    if "links" in data and data["links"]:
        new_links = []
        for link in data["links"]:
            # Check if it's a legacy profile link
            # Criteria: text is "Profile" OR url contains "typo.iwr" and text is "Profile"
            is_legacy = False
            if link.get("text") == "Profile":
                is_legacy = True
            
            if not is_legacy:
                new_links.append(link)
        
        if len(new_links) != len(data["links"]):
            print(f"Modifying {filename}: Removing {len(data['links']) - len(new_links)} legacy links")
            if new_links:
                data["links"] = new_links
            else:
                del data["links"]
            
            # Reconstruct file
            new_front_matter = yaml.dump(data, sort_keys=False, allow_unicode=True)
            new_content = f"---\n{new_front_matter}---\n{body}"
            
            with open(filepath, "w") as f:
                f.write(new_content)

print("Done removing legacy profile links.")
