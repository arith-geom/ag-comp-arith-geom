#!/usr/bin/env python3
"""
Pages CMS Integration Test Script
Tests the Pages CMS integration functionality
"""

import os
import json
import yaml
import sys
from pathlib import Path

def test_configuration_files():
    """Test that all configuration files are properly set up"""
    print("Testing configuration files...")
    
    # Test _config.yml
    try:
        with open('_config.yml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        pagescms_config = config.get('pagescms', {})
        if not pagescms_config:
            print("❌ Pages CMS configuration missing in _config.yml")
            return False
        
        if not pagescms_config.get('enabled'):
            print("❌ Pages CMS is disabled in _config.yml")
            return False
        
        print("✅ _config.yml Pages CMS configuration is valid")
        return True
    except Exception as e:
        print(f"❌ Error reading _config.yml: {e}")
        return False

def test_pages_yml():
    """Test .pages.yml configuration"""
    print("Testing .pages.yml configuration...")
    
    try:
        with open('.pages.yml', 'r', encoding='utf-8') as f:
            pages_config = yaml.safe_load(f)
        
        # Check for required sections
        required_sections = ['media', 'content']
        for section in required_sections:
            if section not in pages_config:
                print(f"❌ Missing required section '{section}' in .pages.yml")
                return False
        
        print("✅ .pages.yml configuration is valid")
        return True
    except Exception as e:
        print(f"❌ Error reading .pages.yml: {e}")
        return False

def test_pagescms_config_json():
    """Test pagescms.config.json"""
    print("Testing pagescms.config.json...")
    
    try:
        with open('pagescms.config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Check for required fields
        required_fields = ['name', 'description', 'version', 'contentTypes']
        for field in required_fields:
            if field not in config:
                print(f"❌ Missing required field '{field}' in pagescms.config.json")
                return False
        
        print("✅ pagescms.config.json is valid")
        return True
    except Exception as e:
        print(f"❌ Error reading pagescms.config.json: {e}")
        return False

def test_integration_plugin():
    """Test that the integration plugin exists and is valid"""
    print("Testing integration plugin...")
    
    plugin_path = '_plugins/pagescms_integration.rb'
    if not os.path.exists(plugin_path):
        print("❌ Pages CMS integration plugin not found")
        return False
    
    try:
        with open(plugin_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for key components
        required_components = [
            'class PagesCMSIntegration',
            'Jekyll::Generator',
            'setup_pagescms_integration',
            'process_pagescms_content'
        ]
        
        for component in required_components:
            if component not in content:
                print(f"❌ Missing required component '{component}' in integration plugin")
                return False
        
        print("✅ Integration plugin is valid")
        return True
    except Exception as e:
        print(f"❌ Error reading integration plugin: {e}")
        return False

def test_content_structure():
    """Test that content directories are properly structured"""
    print("Testing content structure...")
    
    content_dirs = ['_members', '_publications', '_research', '_teaching']
    all_valid = True
    
    for dir_name in content_dirs:
        if not os.path.exists(dir_name):
            print(f"❌ Content directory '{dir_name}' not found")
            all_valid = False
            continue
        
        # Check for markdown files
        md_files = [f for f in os.listdir(dir_name) if f.endswith('.md')]
        if not md_files:
            print(f"⚠️  No markdown files found in '{dir_name}'")
        else:
            print(f"✅ {dir_name}: {len(md_files)} markdown files")
    
    return all_valid

def test_assets_structure():
    """Test assets directory structure"""
    print("Testing assets structure...")
    
    assets_dirs = ['assets/img', 'assets/uploads', 'assets/media']
    all_exist = True
    
    for dir_path in assets_dirs:
        if os.path.exists(dir_path):
            files = len([f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))])
            print(f"✅ {dir_path}: {files} files")
        else:
            print(f"⚠️  {dir_path}: Directory not found")
            all_exist = False
    
    return all_exist

def test_jekyll_build():
    """Test that Jekyll can build with Pages CMS integration"""
    print("Testing Jekyll build...")
    
    try:
        import subprocess
        result = subprocess.run(['bundle', 'exec', 'jekyll', 'build', '--safe'], 
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ Jekyll build successful")
            return True
        else:
            print(f"❌ Jekyll build failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error running Jekyll build: {e}")
        return False

def run_integration_tests():
    """Run all integration tests"""
    print("=" * 60)
    print("PAGES CMS INTEGRATION TEST SUITE")
    print("=" * 60)
    
    tests = [
        ("Configuration Files", test_configuration_files),
        ("Pages YAML", test_pages_yml),
        ("Pages CMS Config JSON", test_pagescms_config_json),
        ("Integration Plugin", test_integration_plugin),
        ("Content Structure", test_content_structure),
        ("Assets Structure", test_assets_structure),
        ("Jekyll Build", test_jekyll_build)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("INTEGRATION TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All integration tests passed!")
        print("✅ Pages CMS integration is working correctly")
        return True
    else:
        print("\n⚠️  Some integration tests failed")
        print("❌ Please review the failed tests above")
        return False

def main():
    """Main test function"""
    # Change to the project directory
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_dir)
    
    print(f"Running Pages CMS integration tests in: {project_dir}")
    
    success = run_integration_tests()
    
    if success:
        print("\n✅ Integration test completed successfully!")
        print("\nYour Pages CMS integration is fully functional.")
        print("You can now:")
        print("1. Visit https://app.pagescms.org")
        print("2. Connect your repository")
        print("3. Start managing content through the web interface")
    else:
        print("\n❌ Integration test failed")
        print("Please fix the issues above before using Pages CMS")
        sys.exit(1)

if __name__ == "__main__":
    main() 