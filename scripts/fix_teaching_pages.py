#!/usr/bin/env python3
"""
Fix malformed front matter in teaching pages.
Removes empty front matter blocks that cause Quirks Mode errors.
"""

import os
import re
import glob

def fix_teaching_pages():
    """Fix all teaching pages with malformed front matter."""
    
    # Get all teaching markdown files
    teaching_dir = "_teaching"
    md_files = glob.glob(os.path.join(teaching_dir, "*.md"))
    
    fixed_count = 0
    
    for file_path in md_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if file has the problematic pattern: ---\n---\n
            if content.startswith('---\n---\n'):
                print(f"Fixing: {file_path}")
                
                # Remove the empty front matter block
                fixed_content = content.replace('---\n---\n', '', 1)
                
                # Write the fixed content back
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                
                fixed_count += 1
                
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    print(f"\n✅ Fixed {fixed_count} teaching pages")
    return fixed_count

if __name__ == "__main__":
    print("🔧 Fixing malformed front matter in teaching pages...")
    fixed = fix_teaching_pages()
    print(f"🎉 Completed! Fixed {fixed} files.") 