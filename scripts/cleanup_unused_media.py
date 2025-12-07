import os
import argparse
import sys

# Configuration
MEDIA_DIR = "assets/uploads"
CONTENT_DIRS = ["_data", "_pages", "_posts", "_projects", "_research", "_teaching"]
CONTENT_EXTENSIONS = [".yml", ".yaml", ".md", ".html", ".json"]

def get_all_media_files(media_dir):
    """
    Recursively gets all files in the media directory.
    Returns a set of filenames (assuming usage relies on filenames).
    """
    media_files = set()
    full_paths = {} # Map filename to full relative path for deletion

    if not os.path.exists(media_dir):
        print(f"Error: Media directory '{media_dir}' does not exist.")
        return set(), {}

    for root, _, files in os.walk(media_dir):
        for file in files:
             # We assume filenames are unique enough or that if 'file.pdf' is used,
             # we want to keep all 'file.pdf' instances to be safe,
             # OR we track full relative paths if usage is strictly by path.
             # Pages CMS often stores just the path.
             # Let's check matching by filename to be robust against path variations.
             full_path = os.path.join(root, file)
             media_files.add(file)
             if file not in full_paths:
                 full_paths[file] = []
             full_paths[file].append(full_path)

    return media_files, full_paths

def scan_content_for_references(content_dirs, content_extensions):
    """
    Recursively scans content directories and reads files to find references to media.
    Returns a set of referenced strings (which we will check against filenames).
    """
    referenced_content = set()

    # Also check root directory for single files like index.md
    root_files = [f for f in os.listdir(".") if os.path.isfile(f) and any(f.endswith(ext) for ext in content_extensions)]

    for file in root_files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                referenced_content.add(content)
        except Exception as e:
            print(f"Warning: Could not read {file}: {e}")

    for search_dir in content_dirs:
        if not os.path.exists(search_dir):
            continue

        for root, _, files in os.walk(search_dir):
            for file in files:
                if any(file.endswith(ext) for ext in content_extensions):
                    path = os.path.join(root, file)
                    try:
                        with open(path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            # Store the whole content blob to search in later?
                            # Or just search line by line?
                            # For simple string matching, reading whole file is okay for small sites.
                            referenced_content.add(content)
                    except Exception as e:
                        print(f"Warning: Could not read {path}: {e}")

    return referenced_content

def main():
    parser = argparse.ArgumentParser(description="Find and delete unused media files.")
    parser.add_argument("--delete", action="store_true", help="Permanently delete unused files.")
    parser.add_argument("--verbose", action="store_true", help="Show more details.")
    args = parser.parse_args()

    print(f"Scanning media directory: {MEDIA_DIR} ...")
    media_files, full_paths_map = get_all_media_files(MEDIA_DIR)

    if not media_files:
        print("No media files found.")
        return

    print(f"Found {len(media_files)} media files.")
    print("Scanning content files for references...")

    # Optimize: concatenate all content into one huge string for faster "in" checks
    # if memory allows (likely yes for a static site).
    content_blobs = scan_content_for_references(CONTENT_DIRS, CONTENT_EXTENSIONS)
    combined_content = "\n".join(content_blobs)

    unused_files = []

    for filename in media_files:
        # Check if filename exists in the content
        # Note: This is a loose check. It finds "file.pdf" anywhere in the text.
        # This is safe (ignores false negatives) but might have false positives
        # (e.g. if a text just happens to say "file.pdf" without linking it).
        # Better safe than sorry for a deletion script.
        if filename not in combined_content:
            unused_files.append(filename)

    print(f"Analysis complete. Found {len(unused_files)} unused files out of {len(media_files)} total.")

    if unused_files:
        print("\nUnused Files:")
        for f in sorted(unused_files):
            paths = full_paths_map[f]
            for p in paths:
                print(f"  - {p}")

        if args.delete:
            confirm = input(f"\nAre you SURE you want to delete these {len(unused_files)} files? (yes/no): ")
            if confirm.lower() == 'yes':
                print("Deleting...")
                deleted_count = 0
                for f in unused_files:
                    paths = full_paths_map[f]
                    for p in paths:
                        try:
                            os.remove(p)
                            print(f"Deleted: {p}")
                            deleted_count += 1
                        except OSError as e:
                            print(f"Error deleting {p}: {e}")
                print(f"Done. Deleted {deleted_count} files.")
            else:
                print("Deletion cancelled.")
        else:
            print("\nRun with --delete to permanently remove these files.")
    else:
        print("No unused files found. Good job!")

if __name__ == "__main__":
    main()
