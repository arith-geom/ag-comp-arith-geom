import yaml
import os
from collections import defaultdict

def audit_cms_fields():
    print("Auditing CMS Fields...")

    # Load Pages Config
    if not os.path.exists('.pages.yml'):
        print("Error: .pages.yml not found")
        return

    with open('.pages.yml', 'r') as f:
        pages_config = yaml.safe_load(f)

    # Helper to flatten fields from config
    def get_config_fields(fields_list):
        config_fields = set()
        for field in fields_list:
            config_fields.add(field['name'])
            # We don't recurse deeply for now, just top level of the object/list
            # But for lists, the fields are inside 'fields' or 'field'
            # This is complex because Pages CMS nests things.
            # Let's just track top-level fields for each content type for now,
            # and maybe one level deep if it's a list/object.
        return config_fields

    # Analyze each content type
    for content in pages_config.get('content', []):
        name = content.get('name')
        path = content.get('path')
        print(f"\n--- Analyzing {name} ({path}) ---")

        if not os.path.exists(path):
            print(f"  [WARN] Data file {path} not found")
            continue

        with open(path, 'r') as f:
            data = yaml.safe_load(f)

        # Get configured fields
        config_fields = []
        if 'fields' in content:
            config_fields = content['fields']

        # Flatten config fields to a list of "paths" or names
        # e.g. "publications", "publications.title", "publications.year"
        # Since our data is often nested (e.g. members -> sections -> members -> name),
        # we need to map the config structure to the data structure.

        # MEMBERS
        if name == 'members':
            # Config: sections -> members -> [fields]
            # Data: sections -> members -> [fields]

            # Find the 'members' field definition inside 'sections'
            member_fields_config = []
            for f in config_fields:
                if f['name'] == 'sections':
                    for sub_f in f.get('fields', []):
                        if sub_f['name'] == 'members':
                            member_fields_config = sub_f.get('fields', [])
                            break

            defined_fields = {f['name'] for f in member_fields_config}
            used_fields = defaultdict(int)
            total_items = 0

            if data and 'sections' in data:
                for section in data['sections']:
                    if 'members' in section:
                        for member in section['members']:
                            total_items += 1
                            for key in member.keys():
                                used_fields[key] += 1

            print(f"  Total Members: {total_items}")
            print("  Field Usage:")
            for field in defined_fields:
                count = used_fields.get(field, 0)
                pct = (count / total_items * 100) if total_items else 0
                print(f"    - {field}: {count} ({pct:.1f}%)")

            # Check for extra fields
            extra = set(used_fields.keys()) - defined_fields
            if extra:
                print(f"  [EXTRA] Found fields in data not in config: {extra}")

        # PUBLICATIONS
        elif name == 'publications':
            # Config: publications -> [fields]
            pub_fields_config = []
            for f in config_fields:
                if f['name'] == 'publications':
                    pub_fields_config = f.get('fields', [])
                    break

            defined_fields = {f['name'] for f in pub_fields_config}
            used_fields = defaultdict(int)
            total_items = 0

            if data and 'publications' in data:
                for pub in data['publications']:
                    total_items += 1
                    for key in pub.keys():
                        used_fields[key] += 1

            print(f"  Total Publications: {total_items}")
            print("  Field Usage:")
            for field in defined_fields:
                count = used_fields.get(field, 0)
                pct = (count / total_items * 100) if total_items else 0
                print(f"    - {field}: {count} ({pct:.1f}%)")

            extra = set(used_fields.keys()) - defined_fields
            if extra:
                print(f"  [EXTRA] Found fields in data not in config: {extra}")

        # TEACHING
        elif name == 'teaching':
            # Config: courses -> semesters -> courses -> [fields]
            course_fields_config = []
            # Traverse config to find course fields
            # courses -> semesters -> courses
            # This is hardcoded for this schema structure
            try:
                c_fields = config_fields[0]['fields'] # fields of 'courses' (year, semesters)
                s_fields = c_fields[1]['fields'] # fields of 'semesters' (semester, courses)
                course_fields_config = s_fields[1]['fields'] # fields of 'courses' list
            except:
                print("  [WARN] Could not parse teaching config structure")
                continue

            defined_fields = {f['name'] for f in course_fields_config}
            used_fields = defaultdict(int)
            total_items = 0

            if data and 'courses' in data:
                for year_group in data['courses']:
                    if 'semesters' in year_group:
                        for semester in year_group['semesters']:
                            if 'courses' in semester:
                                for course in semester['courses']:
                                    total_items += 1
                                    for key in course.keys():
                                        used_fields[key] += 1

            print(f"  Total Courses: {total_items}")
            print("  Field Usage:")
            for field in defined_fields:
                count = used_fields.get(field, 0)
                pct = (count / total_items * 100) if total_items else 0
                print(f"    - {field}: {count} ({pct:.1f}%)")

            extra = set(used_fields.keys()) - defined_fields
            if extra:
                print(f"  [EXTRA] Found fields in data not in config: {extra}")

if __name__ == "__main__":
    audit_cms_fields()
