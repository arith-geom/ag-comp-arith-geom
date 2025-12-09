import yaml
import os
import sys
import re

def check_filenames(directory):
    """
    Checks that all files in the given directory (recursive) have safe filenames.
    Safe: a-z, 0-9, -, _, . (no spaces, no special chars)
    """
    print(f"Checking filenames in {directory}...")
    unsafe_pattern = re.compile(r'[^a-zA-Z0-9\-\_\.\/]')
    issues_found = False

    if not os.path.exists(directory):
        print(f"[WARNING] Directory not found: {directory}")
        return False

    for root, dirs, files in os.walk(directory):
        for filename in files:
            # Check for non-ascii or special chars
            if unsafe_pattern.search(filename):
                print(f"[ERROR] Unsafe filename found: {os.path.join(root, filename)}")
                issues_found = True
            # specific check for spaces
            if ' ' in filename:
                print(f"[ERROR] Filename contains spaces: {os.path.join(root, filename)}")
                issues_found = True

    return issues_found

def validate_members(file_path):
    print(f"Validating {file_path}...")
    if not os.path.exists(file_path):
        print(f"  [ERROR] File not found: {file_path}")
        return False

    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)

    errors = []
    if not data or 'sections' not in data:
        errors.append("Missing 'sections' in members.yml")
    else:
        for s_idx, section in enumerate(data['sections']):
            if 'members' in section:
                for m_idx, member in enumerate(section['members']):
                    if 'name' not in member:
                        # Try to find some content to identify the member
                        context = str(member)[:50] # First 50 chars of content
                        errors.append(f"Section '{section.get('title', 'Unknown')}' -> Member #{m_idx+1}: Missing 'name' field. (Context: {context}...)")

    if errors:
        for e in errors:
            print(f"  [ERROR] {e}")
        return False
    print("  [OK] Members valid.")
    return True

def validate_publications(file_path):
    print(f"Validating {file_path}...")
    if not os.path.exists(file_path):
        print(f"  [ERROR] File not found: {file_path}")
        return False

    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)

    errors = []
    if not data or 'publications' not in data:
        errors.append("Missing 'publications' in publications.yml")
    else:
        for idx, pub in enumerate(data['publications']):
            if 'title' not in pub:
                context = str(pub)[:50]
                errors.append(f"Publication #{idx+1}: Missing 'title'. (Context: {context}...)")
            if 'year' not in pub:
                title = pub.get('title', 'Unknown Title')
                errors.append(f"Publication #{idx+1} ('{title}'): Missing 'year'.")

    if errors:
        for e in errors:
            print(f"  [ERROR] {e}")
        return False
    print("  [OK] Publications valid.")
    return True

def validate_teaching(file_path):
    print(f"Validating {file_path}...")
    if not os.path.exists(file_path):
        print(f"  [ERROR] File not found: {file_path}")
        return False

    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)

    errors = []
    if not data or 'courses' not in data:
        errors.append("Missing 'courses' in teaching.yml")
    else:
        if not isinstance(data['courses'], list):
             errors.append("'courses' must be a list")
        else:
            for y_idx, year_group in enumerate(data['courses']):
                if 'year' not in year_group:
                    errors.append(f"Year Group #{y_idx+1}: Missing 'year'.")
                if 'semesters' in year_group:
                    for s_idx, semester in enumerate(year_group['semesters']):
                        if 'courses' in semester:
                            for c_idx, course in enumerate(semester['courses']):
                                if 'title' not in course:
                                    year = year_group.get('year', 'Unknown Year')
                                    sem = semester.get('semester', 'Unknown Semester')
                                    errors.append(f"Teaching {year} {sem} -> Course #{c_idx+1}: Missing 'title'.")

    if errors:
        for e in errors:
            print(f"  [ERROR] {e}")
        return False
    print("  [OK] Teaching valid.")
    return True

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
    assets_dir = os.path.join(base_dir, 'assets', 'uploads')
    data_dir = os.path.join(base_dir, '_data')

    print("=== Starting Site Validation ===")

    failure = False

    # Check uploads for weird filenames and large files
    # We walk the directory once for efficiency
    if os.path.exists(assets_dir):
        print(f"Checking assets in {assets_dir}...")
        unsafe_pattern = re.compile(r'[^a-zA-Z0-9\-\_\.\/]')

        for root, dirs, files in os.walk(assets_dir):
            for filename in files:
                fpath = os.path.join(root, filename)

                # Check 1: Filename safety (Error)
                if unsafe_pattern.search(filename) or ' ' in filename:
                    print(f"[ERROR] Unsafe filename found: {fpath}")
                    failure = True

                # Check 2: File size (Warning)
                try:
                    size_mb = os.path.getsize(fpath) / (1024 * 1024)
                    if size_mb > 2:
                        print(f"[WARNING] Large file ({size_mb:.2f} MB): {fpath}")
                except OSError:
                    pass
    else:
        print(f"[WARNING] Assets directory not found: {assets_dir}")

    # Validate key data files
    if not validate_members(os.path.join(data_dir, 'members.yml')):
        failure = True
    if not validate_publications(os.path.join(data_dir, 'publications.yml')):
        failure = True
    if not validate_teaching(os.path.join(data_dir, 'teaching.yml')):
        failure = True

    if failure:
        print("\n=== Validation FAILED ===")
        sys.exit(1)
    else:
        print("\n=== Validation PASSED ===")

if __name__ == "__main__":
    main()
