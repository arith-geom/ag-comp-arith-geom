import os
import sys

def remove_trailing_spaces(directory):
    print(f"Cleaning trailing spaces and ensuring EOF newlines in {directory}...")
    extensions = ['.yml', '.yaml', '.md', '.html', '.css', '.scss', '.js', '.json', '.txt', '.py']

    for root, dirs, files in os.walk(directory):
        if '.git' in root or '_site' in root or 'vendor' in root or 'node_modules' in root:
            continue

        for filename in files:
            if not any(filename.endswith(ext) for ext in extensions):
                continue

            fpath = os.path.join(root, filename)
            try:
                with open(fpath, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                new_lines = [line.rstrip() + '\n' for line in lines]

                # Check if content changed
                # .rstrip() removes all trailing whitespace including newline, so we add \n back.
                # But we valid empty lines to just be \n

                if not new_lines: continue

                # Determine if write is needed
                original_content = ''.join(lines)
                new_content = ''.join(new_lines)

                if original_content != new_content:
                    print(f"Fixed: {filename}")
                    with open(fpath, 'w', encoding='utf-8') as f:
                        f.write(new_content)

            except Exception as e:
                print(f"Skipping {filename}: {e}")

if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    remove_trailing_spaces(base_dir)
