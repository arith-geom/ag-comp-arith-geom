#!/usr/bin/env python3
"""
Pages CMS Configuration Validation Script
Validates the Pages CMS setup for the AG Computational Arithmetic Geometry website
"""

import os
import json
import yaml
import sys
from pathlib import Path

def check_file_exists(file_path, description):
    """Check if a file exists and return status"""
    exists = os.path.exists(file_path)
    print(f"✓ {description}: {'Found' if exists else 'Missing'}")
    return exists

def validate_yaml_file(file_path, description):
    """Validate YAML file syntax"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            yaml.safe_load(f)
        print(f"✓ {description}: Valid YAML")
        return True
    except yaml.YAMLError as e:
        print(f"✗ {description}: Invalid YAML - {e}")
        return False
    except FileNotFoundError:
        print(f"✗ {description}: File not found")
        return False

def validate_json_file(file_path, description):
    """Validate JSON file syntax"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json.load(f)
        print(f"✓ {description}: Valid JSON")
        return True
    except json.JSONDecodeError as e:
        print(f"✗ {description}: Invalid JSON - {e}")
        return False
    except FileNotFoundError:
        print(f"✗ {description}: File not found")
        return False

def check_content_structure():
    """Check content directory structure"""
    print("\n=== Content Structure Validation ===")
    
    required_dirs = [
        ('_members', 'Team members directory'),
        ('_publications', 'Publications directory'),
        ('_research', 'Research areas directory'),
        ('_teaching', 'Teaching materials directory'),
        ('_pages', 'Static pages directory'),
        ('assets/img', 'Images directory'),
        ('assets/uploads', 'Document uploads directory')
    ]
    
    all_exist = True
    for dir_path, description in required_dirs:
        exists = os.path.exists(dir_path)
        print(f"{'✓' if exists else '✗'} {description}: {'Found' if exists else 'Missing'}")
        if not exists:
            all_exist = False
    
    return all_exist

def validate_config_files():
    """Validate configuration files"""
    print("\n=== Configuration Files Validation ===")
    
    config_files = [
        ('_config.yml', 'Jekyll configuration'),
        ('.pages.yml', 'Pages CMS configuration'),
        ('pagescms.config.json', 'Pages CMS JSON config')
    ]
    
    all_valid = True
    for file_path, description in config_files:
        if file_path.endswith('.yml'):
            valid = validate_yaml_file(file_path, description)
        elif file_path.endswith('.json'):
            valid = validate_json_file(file_path, description)
        else:
            valid = check_file_exists(file_path, description)
        
        if not valid:
            all_valid = False
    
    return all_valid

def check_pagescms_config():
    """Check Pages CMS specific configuration"""
    print("\n=== Pages CMS Configuration Validation ===")
    
    # Check _config.yml for Pages CMS settings
    try:
        with open('_config.yml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        pagescms_config = config.get('pagescms', {})
        
        if not pagescms_config:
            print("✗ Pages CMS configuration missing in _config.yml")
            return False
        
        print("✓ Pages CMS configuration found in _config.yml")
        
        # Check required settings
        required_settings = ['enabled', 'api_url', 'content_types']
        for setting in required_settings:
            if setting in pagescms_config:
                print(f"✓ {setting}: {pagescms_config[setting]}")
            else:
                print(f"✗ Missing required setting: {setting}")
                return False
        
        # Check if enabled
        if pagescms_config.get('enabled'):
            print("✓ Pages CMS is enabled")
        else:
            print("⚠ Pages CMS is disabled")
        
        return True
        
    except Exception as e:
        print(f"✗ Error reading _config.yml: {e}")
        return False

def check_content_files():
    """Check content files for proper structure"""
    print("\n=== Content Files Validation ===")
    
    content_dirs = ['_members', '_publications', '_research', '_teaching']
    all_valid = True
    
    for dir_name in content_dirs:
        if not os.path.exists(dir_name):
            print(f"✗ Directory {dir_name} not found")
            all_valid = False
            continue
        
        files = [f for f in os.listdir(dir_name) if f.endswith('.md')]
        print(f"✓ {dir_name}: {len(files)} markdown files found")
        
        # Check a sample file for proper front matter
        if files:
            sample_file = os.path.join(dir_name, files[0])
            try:
                with open(sample_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if content.startswith('---'):
                    print(f"✓ {dir_name}: Proper front matter structure")
                else:
                    print(f"⚠ {dir_name}: Missing front matter in sample file")
                    all_valid = False
            except Exception as e:
                print(f"✗ {dir_name}: Error reading sample file - {e}")
                all_valid = False
    
    return all_valid

def check_plugins():
    """Check for required plugins"""
    print("\n=== Plugins Validation ===")
    
    plugins_dir = '_plugins'
    if os.path.exists(plugins_dir):
        plugins = [f for f in os.listdir(plugins_dir) if f.endswith('.rb')]
        print(f"✓ Found {len(plugins)} plugin(s) in _plugins directory")
        
        # Check for Pages CMS integration plugin
        pagescms_plugin = 'pagescms_integration.rb'
        if pagescms_plugin in plugins:
            print("✓ Pages CMS integration plugin found")
        else:
            print("⚠ Pages CMS integration plugin not found")
    else:
        print("⚠ _plugins directory not found")
    
    return True

def check_assets():
    """Check assets directory structure"""
    print("\n=== Assets Validation ===")
    
    assets_dirs = ['assets/img', 'assets/uploads', 'assets/media']
    all_exist = True
    
    for dir_path in assets_dirs:
        if os.path.exists(dir_path):
            files = len([f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))])
            print(f"✓ {dir_path}: {files} files")
        else:
            print(f"⚠ {dir_path}: Directory not found")
            all_exist = False
    
    return all_exist

def generate_report():
    """Generate a comprehensive validation report"""
    print("=" * 60)
    print("PAGES CMS CONFIGURATION VALIDATION REPORT")
    print("=" * 60)
    
    results = []
    
    # Run all validation checks
    results.append(("Configuration Files", validate_config_files()))
    results.append(("Pages CMS Config", check_pagescms_config()))
    results.append(("Content Structure", check_content_structure()))
    results.append(("Content Files", check_content_files()))
    results.append(("Plugins", check_plugins()))
    results.append(("Assets", check_assets()))
    
    # Summary
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{status}: {check_name}")
    
    print(f"\nOverall: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 All validations passed! Pages CMS is properly configured.")
        return True
    else:
        print("⚠ Some issues found. Please review the validation results above.")
        return False

def main():
    """Main validation function"""
    # Change to the project directory
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_dir)
    
    print(f"Validating Pages CMS configuration in: {project_dir}")
    
    success = generate_report()
    
    if success:
        print("\n✅ Pages CMS is ready to use!")
        print("\nNext steps:")
        print("1. Visit https://app.pagescms.org to access the CMS")
        print("2. Connect your repository to Pages CMS")
        print("3. Start managing your content through the web interface")
    else:
        print("\n❌ Please fix the issues above before using Pages CMS")
        sys.exit(1)

if __name__ == "__main__":
    main() 