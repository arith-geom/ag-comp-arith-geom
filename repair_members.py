import os
import re

members_dir = "_members"

for filename in os.listdir(members_dir):
    if not filename.endswith(".md"):
        continue

    filepath = os.path.join(members_dir, filename)
    with open(filepath, "r") as f:
        content = f.read()

    # Check if the file has the corrupted pattern:
    # photo: ...
    # - url: ...
    
    # We look for a line starting with "- url:" that is NOT preceded by "links:"
    
    lines = content.splitlines()
    new_lines = []
    in_front_matter = False
    
    for i, line in enumerate(lines):
        if line.strip() == "---":
            in_front_matter = not in_front_matter
            new_lines.append(line)
            continue
            
        if in_front_matter:
            # If we see a line starting with "- url:" or "- text:" (list item)
            # And the previous line was NOT "links:"
            if line.startswith("- url:") or line.startswith("- text:"):
                # Check previous line in new_lines (ignoring empty lines if any, though YAML usually doesn't have them in block)
                prev_line = new_lines[-1] if new_lines else ""
                if not prev_line.strip().startswith("links:"):
                    print(f"Fixing {filename}: Inserting 'links:' before '{line}'")
                    new_lines.append("links:")
            
        new_lines.append(line)
    
    new_content = "\n".join(new_lines)
    if content != new_content:
        with open(filepath, "w") as f:
            f.write(new_content)
            # Ensure trailing newline if it was there
            if content.endswith("\n") and not new_content.endswith("\n"):
                f.write("\n")

print("Done repairing files.")
