import os
import requests
import urllib.parse
from PIL import Image, ImageDraw, ImageFont
import io
import time

# Configuration
MEMBERS_DIR = "../_members"
PHOTOS_DIR = "../assets/img"

# Ensure photos directory exists
os.makedirs(PHOTOS_DIR, exist_ok=True)

def create_placeholder_image(name, role, filename):
    """Create a professional placeholder image with the member's name."""
    # Create a 400x400 image with a professional background
    width, height = 400, 400
    
    # Background colors based on role
    if "Professor" in role or "Group Leader" in role:
        bg_color = (25, 118, 210)  # Blue for professors
    elif "Postdoctoral" in role:
        bg_color = (56, 142, 60)   # Green for postdocs
    elif "PhD" in role:
        bg_color = (123, 31, 162)  # Purple for PhD students
    elif "Secretary" in role:
        bg_color = (255, 87, 34)   # Orange for admin
    else:
        bg_color = (96, 125, 139)  # Gray for others
    
    # Create image
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Try to load a font, fall back to default if not available
    try:
        # Try different font paths
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
        ]
        font = None
        for font_path in font_paths:
            if os.path.exists(font_path):
                font = ImageFont.truetype(font_path, 32)
                break
        if font is None:
            font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()
    
    # Split name into first and last name
    name_parts = name.split()
    if len(name_parts) >= 2:
        first_name = name_parts[0]
        last_name = " ".join(name_parts[1:])
    else:
        first_name = name
        last_name = ""
    
    # Calculate text positions
    bbox = draw.textbbox((0, 0), first_name, font=font)
    first_name_width = bbox[2] - bbox[0]
    first_name_height = bbox[3] - bbox[1]
    
    if last_name:
        bbox = draw.textbbox((0, 0), last_name, font=font)
        last_name_width = bbox[2] - bbox[0]
        last_name_height = bbox[3] - bbox[1]
        total_height = first_name_height + last_name_height + 10
    else:
        total_height = first_name_height
    
    # Calculate center positions
    y_start = (height - total_height) // 2
    
    # Draw first name
    x = (width - first_name_width) // 2
    y = y_start
    draw.text((x, y), first_name, fill=(255, 255, 255), font=font)
    
    # Draw last name
    if last_name:
        x = (width - last_name_width) // 2
        y = y_start + first_name_height + 10
        draw.text((x, y), last_name, fill=(255, 255, 255), font=font)
    
    # Add role at bottom
    try:
        small_font = ImageFont.truetype(font_paths[0], 16) if font_paths and os.path.exists(font_paths[0]) else ImageFont.load_default()
    except:
        small_font = ImageFont.load_default()
    
    bbox = draw.textbbox((0, 0), role, font=small_font)
    role_width = bbox[2] - bbox[0]
    x = (width - role_width) // 2
    y = height - 40
    draw.text((x, y), role, fill=(255, 255, 255, 180), font=small_font)
    
    # Save image
    filepath = os.path.join(PHOTOS_DIR, filename)
    img.save(filepath, 'JPEG', quality=95)
    print(f"Created placeholder image: {filename}")
    return filepath

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
        .replace("\u00d6", "oe")
        .replace("\u00c4", "ae")
        .replace("\u00dc", "ue")
    )

def download_member_images():
    """Download or create images for all members."""
    member_files = [f for f in os.listdir(MEMBERS_DIR) if f.endswith('.md')]
    
    print(f"Processing {len(member_files)} member files...")
    
    for filename in member_files:
        filepath = os.path.join(MEMBERS_DIR, filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract front matter
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    import yaml
                    front_matter = yaml.safe_load(parts[1])
                    
                    name = front_matter.get('name', '')
                    role = front_matter.get('role', '')
                    
                    if name:
                        # Create image filename
                        image_filename = f"{slugify(name)}.jpg"
                        image_path = os.path.join(PHOTOS_DIR, image_filename)
                        
                        # Check if image already exists
                        if not os.path.exists(image_path):
                            # Create placeholder image
                            create_placeholder_image(name, role, image_filename)
                        else:
                            print(f"Image already exists: {image_filename}")
                        
                        # Update the member file with the correct photo path
                        photo_path = f"/assets/img/{image_filename}"
                        
                        # Update front matter if photo path is different
                        if front_matter.get('photo') != photo_path:
                            front_matter['photo'] = photo_path
                            
                            # Rewrite the file
                            with open(filepath, 'w', encoding='utf-8') as f:
                                f.write("---\n")
                                yaml.dump(front_matter, f, allow_unicode=True, sort_keys=False)
                                f.write("---\n\n")
                                f.write(parts[2])
                            
                            print(f"Updated photo path for: {name}")
        
        except Exception as e:
            print(f"Error processing {filename}: {e}")
    
    print("✅ All member images processed!")

if __name__ == "__main__":
    download_member_images()
