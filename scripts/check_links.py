import os
import re
import requests
import glob
from pathlib import Path

def check_links_in_file(filepath):
    """Check all links in a member file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all URLs in the raw text (best-effort)
        urls = re.findall(r'https?://[^\s<>"{}|\\^`\[\]]+', content)
        
        if urls:
            print(f"\n📄 {os.path.basename(filepath)}:")
            ALLOWLIST_HOSTS = {
                'mathscinet.ams.org',
                'www.mathinf.uni-heidelberg.de',
                'www.iwr.uni-heidelberg.de',
            }
            for url in urls:
                # Skip Liquid-interpolated placeholders
                idx = content.find(url)
                if idx != -1:
                    window = content[max(0, idx-64):idx+64]
                    if '{{' in window and '}}' in window:
                        continue
                trimmed = url.rstrip(').,;')
                # Allowlist hosts that typically block HEAD or require auth
                try:
                    host = re.sub(r'^https?://', '', trimmed).split('/')[0]
                except Exception:
                    host = ''
                if host in ALLOWLIST_HOSTS:
                    print(f"  ✅ {trimmed} (skipped: allowlisted)")
                    continue
                try:
                    response = requests.head(trimmed, timeout=10, allow_redirects=True)
                    if response.status_code == 200:
                        print(f"  ✅ {trimmed}")
                    else:
                        # Try GET as some sites block HEAD
                        get_resp = requests.get(trimmed, timeout=15, allow_redirects=True)
                        if get_resp.status_code == 200:
                            print(f"  ✅ {trimmed}")
                        else:
                            print(f"  ❌ {trimmed} (Status: {get_resp.status_code})")
                except Exception as e:
                    print(f"  ❌ {trimmed} (Error: {e})")
        else:
            print(f"📄 {os.path.basename(filepath)}: No external links found")
            
    except Exception as e:
        print(f"❌ Error reading {filepath}: {e}")

def main():
    """Check external links in key content directories."""
    ROOT = Path(__file__).resolve().parents[1]
    roots = [
        ROOT / "_members",
        ROOT / "_pages",
        ROOT / "_publications",
        ROOT / "_research",
        ROOT / "_teaching",
    ]

    print("🔍 Checking external links in content files...")
    print("=" * 60)

    any_found = False
    for root in roots:
        files = glob.glob(str(root / "*.md"))
        for filepath in sorted(files):
            check_links_in_file(filepath)
            any_found = True

    if not any_found:
        print("(No markdown files scanned)")

    print("\n" + "=" * 60)
    print("✅ Link checking complete!")

if __name__ == "__main__":
    main()
