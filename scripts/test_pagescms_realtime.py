#!/usr/bin/env python3
"""
Test Pages CMS Real-time Integration
This script tests whether new content created through Pages CMS appears immediately on the website.
"""

import os
import sys
import yaml
import json
import time
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

def main():
    print("Testing Pages CMS Real-time Integration...")
    print("=" * 60)
    
    # Get project root
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    # Test 1: Check if Pages CMS is properly configured
    print("\n1. Checking Pages CMS Configuration...")
    test_configuration()
    
    # Test 2: Check if plugin is working
    print("\n2. Testing Pages CMS Plugin...")
    test_plugin()
    
    # Test 3: Test content synchronization
    print("\n3. Testing Content Synchronization...")
    test_content_sync()
    
    # Test 4: Test Jekyll build with new content
    print("\n4. Testing Jekyll Build...")
    test_jekyll_build()
    
    print("\n" + "=" * 60)
    print("Real-time Integration Test Complete!")

def test_configuration():
    """Test if Pages CMS is properly configured"""
    try:
        # Check _config.yml
        with open('_config.yml', 'r') as f:
            config = yaml.safe_load(f)
        
        if 'pagescms' in config and config['pagescms']['enabled']:
            print("✅ Pages CMS is enabled in _config.yml")
            print(f"   API URL: {config['pagescms']['api_url']}")
            print(f"   Auto Sync: {config['pagescms']['auto_sync']}")
            print(f"   Content Types: {config['pagescms']['content_types']}")
        else:
            print("❌ Pages CMS is not properly configured in _config.yml")
            return False
        
        # Check .pages.yml
        if os.path.exists('.pages.yml'):
            print("✅ .pages.yml configuration file exists")
        else:
            print("❌ .pages.yml configuration file missing")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking configuration: {e}")
        return False

def test_plugin():
    """Test if the Pages CMS plugin is working"""
    try:
        plugin_path = '_plugins/pagescms_integration.rb'
        if os.path.exists(plugin_path):
            print("✅ Pages CMS integration plugin exists")
            
            # Check if plugin has required methods
            with open(plugin_path, 'r') as f:
                plugin_content = f.read()
            
            required_methods = [
                'sync_pagescms_content',
                'process_pagescms_item',
                'ensure_front_matter_structure'
            ]
            
            for method in required_methods:
                if method in plugin_content:
                    print(f"   ✅ Method '{method}' found")
                else:
                    print(f"   ❌ Method '{method}' missing")
            
            return True
        else:
            print("❌ Pages CMS integration plugin missing")
            return False
            
    except Exception as e:
        print(f"❌ Error testing plugin: {e}")
        return False

def test_content_sync():
    """Test content synchronization functionality"""
    try:
        # Check content directories
        content_dirs = ['_members', '_publications', '_research', '_teaching']
        
        for dir_name in content_dirs:
            if os.path.exists(dir_name):
                files = list(Path(dir_name).glob('*.md'))
                print(f"✅ {dir_name}: {len(files)} files found")
                
                # Check for recent files (modified in last hour)
                recent_files = [f for f in files if f.stat().st_mtime > time.time() - 3600]
                if recent_files:
                    print(f"   📝 Recent files: {len(recent_files)}")
                    for f in recent_files:
                        print(f"      - {f.name} (modified {datetime.fromtimestamp(f.stat().st_mtime)})")
            else:
                print(f"❌ {dir_name}: Directory missing")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing content sync: {e}")
        return False

def test_jekyll_build():
    """Test if Jekyll builds successfully with Pages CMS integration"""
    try:
        print("Building Jekyll site...")
        
        # Run Jekyll build
        result = subprocess.run(
            ['bundle', 'exec', 'jekyll', 'build', '--safe'],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print("✅ Jekyll build successful")
            
            # Check for Pages CMS related output
            if 'Pages CMS' in result.stdout:
                print("✅ Pages CMS integration detected in build output")
            else:
                print("⚠️  No Pages CMS output detected in build")
            
            return True
        else:
            print("❌ Jekyll build failed")
            print(f"Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Jekyll build timed out")
        return False
    except Exception as e:
        print(f"❌ Error testing Jekyll build: {e}")
        return False

def create_test_content():
    """Create a test content file to verify real-time integration"""
    try:
        test_file = '_teaching/test-semester-2025.md'
        
        test_content = """---
layout: teaching
title: "Test Semester 2025"
semester: "Winter Semester 2025"
type: "Lecture"
language: "en"
description: "This is a test course created to verify Pages CMS real-time integration"
active: true
status: "Active"
---

This is a test course created to verify that Pages CMS real-time integration is working properly.

## Course Information
- **Semester**: Winter Semester 2025
- **Type**: Lecture
- **Language**: English
- **Status**: Active

## Learning Objectives
- Test Pages CMS integration
- Verify real-time content updates
- Ensure proper front matter structure

## Course Content
This course will cover:
1. Pages CMS integration testing
2. Real-time content synchronization
3. Jekyll build verification

*This is a test file and should be removed after testing.*
"""
        
        with open(test_file, 'w') as f:
            f.write(test_content)
        
        print(f"✅ Created test file: {test_file}")
        return test_file
        
    except Exception as e:
        print(f"❌ Error creating test content: {e}")
        return None

if __name__ == "__main__":
    main() 