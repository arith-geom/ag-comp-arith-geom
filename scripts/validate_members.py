import os
import yaml
import glob

def validate_member_file(filepath):
    """Validate a single member file for PagesCMS compatibility."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split front matter and content
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                front_matter = parts[1]
                try:
                    data = yaml.safe_load(front_matter)
                    
                    # Check required fields
                    required_fields = ['name', 'role', 'status', 'layout']
                    missing_fields = []
                    
                    for field in required_fields:
                        if field not in data:
                            missing_fields.append(field)
                    
                    if missing_fields:
                        print(f"❌ {os.path.basename(filepath)}: Missing required fields: {missing_fields}")
                        return False
                    else:
                        print(f"✅ {os.path.basename(filepath)}: Valid")
                        return True
                        
                except yaml.YAMLError as e:
                    print(f"❌ {os.path.basename(filepath)}: YAML parsing error: {e}")
                    return False
            else:
                print(f"❌ {os.path.basename(filepath)}: Invalid front matter structure")
                return False
        else:
            print(f"❌ {os.path.basename(filepath)}: No front matter found")
            return False
            
    except Exception as e:
        print(f"❌ {os.path.basename(filepath)}: Error reading file: {e}")
        return False

def main():
    """Validate all member files."""
    members_dir = "../_members"
    member_files = glob.glob(os.path.join(members_dir, "*.md"))
    
    print(f"Validating {len(member_files)} member files...")
    print("=" * 50)
    
    valid_count = 0
    total_count = len(member_files)
    
    for filepath in sorted(member_files):
        if validate_member_file(filepath):
            valid_count += 1
    
    print("=" * 50)
    print(f"Validation complete: {valid_count}/{total_count} files are valid")
    
    if valid_count == total_count:
        print("🎉 All member files are PagesCMS compatible!")
    else:
        print("⚠️  Some files need attention.")

if __name__ == "__main__":
    main()
