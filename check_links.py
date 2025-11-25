import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, unquote
import concurrent.futures

SITE_DIR = '_site'
TIMEOUT = 5

def get_all_html_files(root_dir):
    html_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    return html_files

def check_external_link(url):
    try:
        response = requests.head(url, timeout=TIMEOUT, allow_redirects=True)
        if response.status_code >= 400:
            # Try GET if HEAD fails (some servers block HEAD)
            response = requests.get(url, timeout=TIMEOUT, stream=True)
            if response.status_code >= 400:
                return False, f"Status code: {response.status_code}"
        return True, "OK"
    except requests.RequestException as e:
        return False, str(e)

def check_internal_link(source_file, href):
    # Strip anchor
    url_part = href.split('#')[0]
    anchor_part = href.split('#')[1] if '#' in href else None

    if not url_part:
        # Self-reference with anchor
        if anchor_part:
            # Check if anchor exists in source_file
            # We need to re-parse source file or cache it. 
            # For simplicity, we might skip anchor check or do it if we pass soup.
            return True, "Anchor check skipped for self-ref" 
        return True, "Self-ref"

    # Resolve path
    if url_part.startswith('/'):
        # Handle baseurl
        baseurl = "/ag-comp-arith-geom"
        if url_part.startswith(baseurl):
            url_part = url_part[len(baseurl):]
        
        target_path = os.path.join(SITE_DIR, url_part.lstrip('/'))
    else:
        target_path = os.path.normpath(os.path.join(os.path.dirname(source_file), url_part))

    # Handle directory links (index.html)
    if os.path.isdir(target_path):
        target_path = os.path.join(target_path, 'index.html')
    
    # Check existence
    if not os.path.exists(target_path):
        # Decode URL just in case
        decoded_path = unquote(target_path)
        if not os.path.exists(decoded_path):
            return False, f"File not found: {target_path}"
    
    return True, "OK"

def process_file(file_path):
    broken_links = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
        
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.startswith('mailto:') or href.startswith('tel:'):
                continue
            
            is_broken = False
            reason = ""
            
            if href.startswith('http'):
                # External link
                # Skip localhost
                if 'localhost' in href or '127.0.0.1' in href:
                    continue
                # We can skip checking external links if user wants only internal, but they asked for "all"
                # To be faster, we can skip known good domains or just check them.
                # For now, let's check them but maybe limit concurrency or just report.
                # Actually, checking ALL external links might take forever. 
                # Let's just check internal for now and maybe a few external if requested?
                # The user said "check for all the links". I will check external too.
                pass 
            else:
                # Internal link
                valid, msg = check_internal_link(file_path, href)
                if not valid:
                    is_broken = True
                    reason = msg
            
            if is_broken:
                broken_links.append({'file': file_path, 'href': href, 'reason': reason})
                
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        
    return broken_links

def main():
    print("Scanning for HTML files...")
    html_files = get_all_html_files(SITE_DIR)
    print(f"Found {len(html_files)} HTML files.")
    
    all_broken_links = []
    
    # Check internal links first (fast)
    print("Checking internal links...")
    for file in html_files:
        links = process_file(file)
        all_broken_links.extend(links)
        
    # Check external links? 
    # To avoid blocking, let's collect all unique external links first.
    print("Collecting external links...")
    external_links = set()
    for file in html_files:
        with open(file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.startswith('http') and not 'localhost' in href and not '127.0.0.1' in href:
                external_links.add(href)
    
    print(f"Found {len(external_links)} unique external links. Checking them now (this may take a while)...")
    
    broken_external = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(check_external_link, url): url for url in external_links}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                valid, msg = future.result()
                if not valid:
                    broken_external.append({'href': url, 'reason': msg})
                    print(f"  Broken external: {url} ({msg})")
            except Exception as e:
                broken_external.append({'href': url, 'reason': str(e)})
                print(f"  Error checking {url}: {e}")

    # Combine results
    # We need to map broken external links back to files?
    # Or just list them. The user asked for a list.
    # Ideally we show where they are used.
    
    print("\n" + "="*50)
    print("BROKEN INTERNAL LINKS")
    print("="*50)
    for item in all_broken_links:
        print(f"File: {item['file']}\n  Link: {item['href']}\n  Reason: {item['reason']}\n")
        
    print("\n" + "="*50)
    print("BROKEN EXTERNAL LINKS")
    print("="*50)
    # To show where they are used, we'd need to re-scan or store usage.
    # Let's just list them for now, or do a quick scan to find usage.
    for item in broken_external:
        print(f"Link: {item['href']}\n  Reason: {item['reason']}")
        # Find usage
        used_in = []
        for file in html_files:
            with open(file, 'r', encoding='utf-8') as f:
                if item['href'] in f.read():
                    used_in.append(file)
                    if len(used_in) > 3: break
        print(f"  Used in: {', '.join(used_in[:3])}...")
        print("")

if __name__ == "__main__":
    main()
