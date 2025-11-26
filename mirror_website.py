import os
import sys
import time
import urllib.request
import urllib.parse
import urllib.error
from html.parser import HTMLParser
from collections import deque

# Configuration
START_URL = "https://typo.iwr.uni-heidelberg.de/groups/arith-geom/"
OUTPUT_DIR = "typo_mirror"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

# Extensions to treat as assets (don't parse for links, just download)
ASSET_EXTENSIONS = {
    '.jpg', '.jpeg', '.png', '.gif', '.svg', '.pdf', '.css', '.js', 
    '.zip', '.tar', '.gz', '.ico', '.woff', '.woff2', '.ttf', '.eot'
}

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        for attr, value in attrs:
            if attr in ('href', 'src'):
                self.links.append(value)

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def get_save_path(url, base_url):
    parsed = urllib.parse.urlparse(url)
    path = parsed.path
    
    if path.endswith('/') or not path:
        path += 'index.html'
    
    # Remove leading slash to make it relative
    if path.startswith('/'):
        path = path[1:]
        
    # Combine with output dir
    full_path = os.path.join(OUTPUT_DIR, path)
    
    # If the path ends with a directory but no extension (and not index.html added above),
    # it might be a clean URL. Heuristic: if no extension, add .html
    if not os.path.splitext(full_path)[1]:
        full_path += '.html'
        
    return full_path

def download_url(url):
    req = urllib.request.Request(
        url, 
        data=None, 
        headers={'User-Agent': USER_AGENT}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.read(), response.geturl()
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None, None

def mirror():
    queue = deque([START_URL])
    visited = set()
    
    ensure_dir(OUTPUT_DIR)
    
    print(f"Starting mirror of {START_URL}")
    print(f"Saving to local directory: {os.path.abspath(OUTPUT_DIR)}")
    print("Press Ctrl+C to stop.")

    while queue:
        url = queue.popleft()
        
        # Normalize URL (remove fragment)
        url = urllib.parse.urldefrag(url)[0]
        
        if url in visited:
            continue
            
        # Only crawl links within the same domain and path prefix
        if not url.startswith(START_URL):
            # Allow downloading assets from the same domain even if outside prefix?
            # For strict mirroring of a sub-site, usually we stick to prefix, 
            # but assets might be in /assets/ or /images/.
            # Let's be permissive for assets on the same domain.
            parsed_start = urllib.parse.urlparse(START_URL)
            parsed_url = urllib.parse.urlparse(url)
            
            if parsed_url.netloc != parsed_start.netloc:
                continue
                
            # If it's not in the prefix, only download if it looks like an asset
            is_asset = any(parsed_url.path.lower().endswith(ext) for ext in ASSET_EXTENSIONS)
            if not url.startswith(START_URL) and not is_asset:
                continue

        visited.add(url)
        print(f"Downloading: {url}")
        
        content, final_url = download_url(url)
        if content is None:
            continue
            
        save_path = get_save_path(url, START_URL)
        ensure_dir(os.path.dirname(save_path))
        
        with open(save_path, 'wb') as f:
            f.write(content)
            
        # Parse for more links if it's HTML
        if save_path.endswith('.html') or save_path.endswith('.htm'):
            try:
                html_content = content.decode('utf-8', errors='ignore')
                parser = LinkParser()
                parser.feed(html_content)
                
                for link in parser.links:
                    absolute_link = urllib.parse.urljoin(url, link)
                    # Filter out mailto, javascript, etc.
                    scheme = urllib.parse.urlparse(absolute_link).scheme
                    if scheme in ('http', 'https'):
                        if absolute_link not in visited:
                            queue.append(absolute_link)
            except Exception as e:
                print(f"Error parsing HTML from {url}: {e}")

        # Be polite
        time.sleep(0.1)

if __name__ == "__main__":
    try:
        mirror()
    except KeyboardInterrupt:
        print("\nStopped by user.")
