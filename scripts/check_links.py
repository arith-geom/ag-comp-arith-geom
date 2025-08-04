import os
import re
import requests
import glob
from urllib.parse import urlparse

def check_links_in_file(filepath):
    """Check all links in a member file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all URLs in the content
        urls = re.findall(r'https?://[^\s<>"{}|\\^`\[\]]+', content)
        
        if urls:
            print(f"\n📄 {os.path.basename(filepath)}:")
            for url in urls:
                try:
                    response = requests.head(url, timeout=10, allow_redirects=True)
                    if response.status_code == 200:
                        print(f"  ✅ {url}")
                    else:
                        print(f"  ❌ {url} (Status: {response.status_code})")
                except Exception as e:
                    print(f"  ❌ {url} (Error: {e})")
        else:
            print(f"📄 {os.path.basename(filepath)}: No external links found")
            
    except Exception as e:
        print(f"❌ Error reading {filepath}: {e}")

def main():
    """Check all links in member files."""
    members_dir = "../_members"
    member_files = glob.glob(os.path.join(members_dir, "*.md"))
    
    print("🔍 Checking links in member files...")
    print("=" * 60)
    
    for filepath in sorted(member_files):
        check_links_in_file(filepath)
    
    print("\n" + "=" * 60)
    print("✅ Link checking complete!")

if __name__ == "__main__":
    main()
