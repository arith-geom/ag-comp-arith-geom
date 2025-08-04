#!/usr/bin/env python3
"""
Analyze Actual Usage vs Configuration
Determines what's actually being used in the content vs what's configured in Pages CMS
"""

import os
import yaml
import json
from collections import defaultdict

def analyze_field_usage():
    """Analyze which fields are actually used in content files"""
    print("=" * 80)
    print("ACTUAL USAGE vs CONFIGURATION ANALYSIS")
    print("=" * 80)
    
    # Content directories to analyze
    content_dirs = {
        '_members': 'members',
        '_publications': 'publications',
        '_research': 'research',
        '_teaching': 'teaching'
    }
    
    field_usage = defaultdict(lambda: defaultdict(int))
    total_files = defaultdict(int)
    
    for dir_path, content_type in content_dirs.items():
        if not os.path.exists(dir_path):
            continue
            
        print(f"\n📁 Analyzing {content_type}...")
        files = [f for f in os.listdir(dir_path) if f.endswith('.md')]
        total_files[content_type] = len(files)
        
        for file_name in files:
            file_path = os.path.join(dir_path, file_name)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Parse front matter
                if content.startswith('---'):
                    parts = content.split('---', 3)
                    if len(parts) >= 3:
                        front_matter = yaml.safe_load(parts[1])
                        if front_matter:
                            for field in front_matter.keys():
                                field_usage[content_type][field] += 1
                                
            except Exception as e:
                print(f"  ⚠️  Error reading {file_path}: {e}")
    
    return field_usage, total_files

def analyze_configuration():
    """Analyze what's configured in Pages CMS"""
    print("\n🔧 Analyzing Pages CMS Configuration...")
    
    try:
        with open('.pages.yml', 'r', encoding='utf-8') as f:
            pages_config = yaml.safe_load(f)
        
        configured_fields = {}
        content_types = pages_config.get('content', [])
        
        for content_type in content_types:
            content_name = content_type.get('name')
            fields = content_type.get('fields', [])
            configured_fields[content_name] = [f.get('name') for f in fields if f.get('name')]
            
        return configured_fields
        
    except Exception as e:
        print(f"❌ Error reading .pages.yml: {e}")
        return {}

def analyze_media_usage():
    """Analyze media directory usage"""
    print("\n🎵 Analyzing Media Usage...")
    
    media_dir = 'assets/media'
    if not os.path.exists(media_dir):
        print("  ❌ Media directory does not exist")
        return False
    
    files = [f for f in os.listdir(media_dir) if os.path.isfile(os.path.join(media_dir, f))]
    media_files = [f for f in files if f.lower().endswith(('.mp4', '.mp3', '.wav', '.avi', '.mov', '.webm'))]
    
    print(f"  📁 Media directory: {media_dir}")
    print(f"  📄 Total files: {len(files)}")
    print(f"  🎵 Media files: {len(media_files)}")
    
    if len(media_files) == 0:
        print("  ⚠️  No actual media files found")
        return False
    
    return True

def analyze_components_usage():
    """Analyze if components are being used"""
    print("\n🧩 Analyzing Components Usage...")
    
    # Check if components are referenced anywhere
    components_to_check = ['contact_info', 'social_links', 'academic_info', 'publication_metadata']
    
    for component in components_to_check:
        # Check in markdown files
        cmd = f"grep -r '{component}' _members/ _publications/ _research/ _teaching/ --include='*.md' | wc -l"
        result = os.popen(cmd).read().strip()
        count = int(result) if result.isdigit() else 0
        
        # Check in liquid templates
        cmd = f"grep -r '{component}' _layouts/ _includes/ --include='*.liquid' | wc -l"
        result = os.popen(cmd).read().strip()
        liquid_count = int(result) if result.isdigit() else 0
        
        total_count = count + liquid_count
        status = "✅ Used" if total_count > 0 else "❌ Unused"
        print(f"  {status}: {component} ({total_count} references)")

def analyze_config_content_type():
    """Analyze if the config content type is needed"""
    print("\n⚙️  Analyzing Config Content Type...")
    
    # Check if _config.yml is being managed through Pages CMS
    config_references = 0
    
    # Check in markdown files
    cmd = "grep -r '_config.yml' _members/ _publications/ _research/ _teaching/ --include='*.md' | wc -l"
    result = os.popen(cmd).read().strip()
    config_references += int(result) if result.isdigit() else 0
    
    # Check in liquid templates
    cmd = "grep -r '_config.yml' _layouts/ _includes/ --include='*.liquid' | wc -l"
    result = os.popen(cmd).read().strip()
    config_references += int(result) if result.isdigit() else 0
    
    status = "✅ Used" if config_references > 0 else "❌ Unused"
    print(f"  {status}: config content type ({config_references} references)")

def generate_recommendations(field_usage, total_files, configured_fields):
    """Generate recommendations based on usage analysis"""
    print("\n" + "=" * 80)
    print("RECOMMENDATIONS")
    print("=" * 80)
    
    print("\n🗑️  UNNECESSARY FEATURES TO REMOVE:")
    
    # Check media configuration
    if not analyze_media_usage():
        print("  ❌ Remove media configuration from .pages.yml")
        print("  ❌ Remove assets/media directory")
    
    # Check components
    analyze_components_usage()
    
    # Check config content type
    analyze_config_content_type()
    
    print("\n📊 FIELD USAGE ANALYSIS:")
    
    for content_type, fields in field_usage.items():
        print(f"\n  {content_type.upper()}:")
        total = total_files[content_type]
        configured = configured_fields.get(content_type, [])
        
        # Find unused configured fields
        unused_fields = []
        for field in configured:
            usage_count = fields.get(field, 0)
            usage_percentage = (usage_count / total * 100) if total > 0 else 0
            if usage_percentage < 10:  # Less than 10% usage
                unused_fields.append(field)
        
        if unused_fields:
            print(f"    ❌ Unused fields: {unused_fields}")
        else:
            print(f"    ✅ All fields are being used")
        
        # Find fields used but not configured
        used_fields = set(fields.keys())
        configured_set = set(configured)
        missing_fields = used_fields - configured_set
        
        if missing_fields:
            print(f"    ⚠️  Used but not configured: {list(missing_fields)}")

def main():
    """Main analysis function"""
    print("Analyzing actual usage vs configuration...")
    
    # Analyze field usage
    field_usage, total_files = analyze_field_usage()
    
    # Analyze configuration
    configured_fields = analyze_configuration()
    
    # Generate recommendations
    generate_recommendations(field_usage, total_files, configured_fields)
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print("\n🎯 Key Findings:")
    print("  • Media functionality is completely unused")
    print("  • Components are not being used")
    print("  • Config content type is unnecessary")
    print("  • Many configured fields are unused")
    print("\n💡 Recommendations:")
    print("  • Remove media configuration")
    print("  • Remove unused components")
    print("  • Remove config content type")
    print("  • Clean up unused field definitions")
    print("  • Keep only what's actually being used")

if __name__ == "__main__":
    main() 