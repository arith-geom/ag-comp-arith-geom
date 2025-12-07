import yaml
import os

def setup_yaml():
    """Configure yaml to handle special characters and block styles better."""
    yaml.SafeDumper.org_represent_str = yaml.SafeDumper.represent_str

    def repr_str(dumper, data):
        if '\n' in data:
            return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
        return dumper.org_represent_str(data)

    yaml.add_representer(str, repr_str, Dumper=yaml.SafeDumper)

def sort_members(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)

    if not data or 'sections' not in data:
        print("Invalid members.yml structure")
        return

    # Sort sections if needed (Head, Secretary, Members, Former Members)
    # The order seems fixed by title, but let's ensure members within sections are sorted by name
    
    for section in data['sections']:
        if 'members' in section and section['members']:
            # Sort members by name
            section['members'].sort(key=lambda x: x.get('name', ''))

    with open(file_path, 'w') as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False, width=1000)
    print(f"Sorted {file_path}")

def sort_publications(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)

    if not data or 'publications' not in data:
        print("Invalid publications.yml structure")
        return

    # Sort by year descending
    # Handle year as string or int
    def get_year(pub):
        y = pub.get('year', '0')
        return str(y)

    data['publications'].sort(key=get_year, reverse=True)

    with open(file_path, 'w') as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False, width=1000)
    print(f"Sorted {file_path}")

def sort_teaching(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)

    if not data or 'courses' not in data:
        print("Invalid teaching.yml structure")
        return

    # Sort by year descending
    data['courses'].sort(key=lambda x: str(x.get('year', '0')), reverse=True)
    
    # Sort semesters within year (Winter then Summer? Or Summer then Winter? Usually Winter starts later in year but spans to next)
    # Let's assume standard academic order or just keep them consistent.
    # Often: Winter, Summer.
    
    semester_order = {'Winter': 0, 'Summer': 1}
    
    for year_group in data['courses']:
        if 'semesters' in year_group:
            year_group['semesters'].sort(key=lambda x: semester_order.get(x.get('semester', ''), 2))
            
            # Sort courses within semester by title
            for semester in year_group['semesters']:
                if 'courses' in semester:
                    semester['courses'].sort(key=lambda x: x.get('title', ''))

    with open(file_path, 'w') as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False, width=1000)
    print(f"Sorted {file_path}")

if __name__ == "__main__":
    setup_yaml()
    sort_members('_data/members.yml')
    sort_publications('_data/publications.yml')
    sort_teaching('_data/teaching.yml')
