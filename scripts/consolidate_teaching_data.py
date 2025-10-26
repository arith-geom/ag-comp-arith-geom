import os
import yaml
from collections import defaultdict

def consolidate_teaching_data():
    """
    Parses all markdown files in the _teaching directory, extracts their
    front matter and content, and consolidates the data into a single
    _data/teaching.yml file, structured by year and semester.
    """
    teaching_dir = "_teaching"
    output_file = "_data/teaching.yml"

    if not os.path.exists(teaching_dir):
        print(f"Error: Directory '{teaching_dir}' not found.")
        return

    all_courses = defaultdict(lambda: defaultdict(list))

    for filename in os.listdir(teaching_dir):
        if filename.endswith(".md"):
            filepath = os.path.join(teaching_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            try:
                # Split front matter and main content
                parts = content.split('---')
                if len(parts) < 3:
                    continue

                front_matter = yaml.safe_load(parts[1])

                # The main content is after the second '---'
                body = parts[2].strip()

                # Skip index file
                if front_matter.get('layout') == 'page':
                    continue

                # Extract relevant data
                year = front_matter.get("semester_year")
                term = front_matter.get("semester_term")

                if not year or not term:
                    continue

                # Clean up the body content by removing redundant titles and breadcrumbs
                body_lines = body.split('\n')
                if len(body_lines) > 2 and "Uni Heidelberg" in body_lines[2]:
                    body = "" # Set to empty if it only contains breadcrumbs
                else:
                    body = body_lines[0] if body_lines else ""


                course_data = {
                    "title": (front_matter.get("title") or "").strip(),
                    "instructor": (front_matter.get("instructor") or "").strip(),
                    "course_type": (front_matter.get("course_type") or "").strip(),
                    "description": body,
                    "links": front_matter.get("links") or [],
                    "pdfs": front_matter.get("pdfs") or [],
                }

                # Ensure year is an integer for correct sorting later
                year = int(year)

                all_courses[year][term].append(course_data)

            except (yaml.YAMLError, IndexError, ValueError) as e:
                print(f"Warning: Could not parse {filename}. Error: {e}")
                continue

    # Sort the data by year (descending) and term (descending, e.g., WS before SS)
    sorted_years = sorted(all_courses.keys(), reverse=True)

    # Create a structured dictionary for YAML output
    final_data = {
        "courses": []
    }

    for year in sorted_years:
        year_data = {
            "year": year,
            "semesters": []
        }

        # Sort terms so "WS" (Winter) comes before "SS" (Summer)
        sorted_terms = sorted(all_courses[year].keys(), key=lambda t: (t != 'WS', t != 'SS'))

        for term in sorted_terms:
            semester_name = f"Winter Term {year}/{int(str(year)[-2:])+1}" if term == "WS" else f"Summer Term {year}"

            semester_data = {
                "semester": semester_name,
                "courses": sorted(all_courses[year][term], key=lambda x: x['title'])
            }
            year_data["semesters"].append(semester_data)

        final_data["courses"].append(year_data)

    # Create the _data directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Write the consolidated data to the YAML file
    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump(final_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    print(f"Successfully consolidated teaching data into {output_file}")


if __name__ == "__main__":
    consolidate_teaching_data()