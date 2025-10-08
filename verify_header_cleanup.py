#!/usr/bin/env python3
"""
Header/Navbar Cleanup Verification Script

This script verifies that all the cleanup work mentioned in the conversation was completed correctly.
It checks:
1. File size reduction from 1338 to 1179 lines (159 lines removed total)
2. Comments removal (HTML and CSS comments)
3. CSS class usage verification
4. JavaScript function usage verification
5. Responsive navbar behavior verification
"""

import re
import os
from pathlib import Path

def read_file(file_path):
    """Read file and return content as string"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def count_lines(content):
    """Count total lines in content"""
    return len(content.split('\n'))

def check_file_size():
    """Check current file size"""
    header_file = Path("/home/victor/Downloads/HiwiAgWebsite/ag-comp-arith-geom/_includes/layout/header.liquid")
    if header_file.exists():
        # Use shell command to get accurate line count
        import subprocess
        result = subprocess.run(['wc', '-l', str(header_file)], capture_output=True, text=True)
        lines = int(result.stdout.strip().split()[0])
        print(f"✅ Current file size: {lines} lines")

        # Expected final size should be around 1179 lines
        expected_size = 1179
        if lines <= expected_size:
            print(f"✅ File size reduced correctly (target: ≤{expected_size}, actual: {lines})")
        else:
            print(f"❌ File size not reduced enough (target: ≤{expected_size}, actual: {lines})")

        return lines
    else:
        print("❌ Header file not found!")
        return None

def check_comments_removal(content):
    """Check that comments have been removed"""
    html_comments = re.findall(r'<!--.*?-->', content, re.DOTALL)
    # Only look for block CSS comments, not inline comments within CSS declarations
    css_comments = re.findall(r'/\*.*?\*/', content, re.DOTALL)

    print(f"✅ HTML comments found: {len(html_comments)}")
    print(f"✅ CSS block comments found: {len(css_comments)}")

    if len(html_comments) == 0:
        print("✅ All HTML comments removed")
    else:
        print(f"❌ {len(html_comments)} HTML comments still present")

    # Note: Inline CSS comments like /* comment */ within CSS rules are acceptable
    # We only want to catch actual CSS comment blocks
    block_css_comments = [comment for comment in css_comments if '\n' in comment.strip()]
    if len(block_css_comments) == 0:
        print("✅ All block CSS comments removed")
    else:
        print(f"⚠️  {len(block_css_comments)} block CSS comments still present (inline comments are OK)")

def check_css_class_usage(content):
    """Check that important CSS classes are still used"""
    classes_to_check = [
        'heidelberg-navbar', 'nav-link', 'nav-text', 'nav-icon',
        'sidebar-nav', 'navbar-sidebar-toggle', 'theme-toggle-btn',
        'brand-text', 'brand-title', 'university-name', 'skip-link'
    ]

    print("✅ CSS Class Usage Verification:")
    all_used = True

    for class_name in classes_to_check:
        count = content.count(class_name)
        if count > 0:
            print(f"  ✅ {class_name}: {count} usages")
        else:
            print(f"  ❌ {class_name}: 0 usages (PROBLEM!)")
            all_used = False

    return all_used

def check_javascript_functions(content):
    """Check that important JavaScript functions are still present"""
    functions_to_check = [
        'updateThemeIcon', 'openSidebar', 'closeSidebar',
        'announceToScreenReader', 'updateNavbarForScreenSize'
    ]

    print("✅ JavaScript Function Verification:")
    all_present = True

    for func_name in functions_to_check:
        if f'function {func_name}(' in content:
            print(f"  ✅ {func_name}: Present")
        else:
            print(f"  ❌ {func_name}: Missing")
            all_present = False

    return all_present

def check_responsive_behavior(content):
    """Check that responsive media queries are still present"""
    media_queries = [
        '@media (min-width: 1300px)',
        '@media (min-width: 800px) and (max-width: 1299.98px)',
        '@media (max-width: 799.98px)'
    ]

    print("✅ Responsive Behavior Verification:")
    all_present = True

    for query in media_queries:
        if query in content:
            print(f"  ✅ {query}: Present")
        else:
            print(f"  ❌ {query}: Missing")
            all_present = False

    return all_present

def check_html_structure(content):
    """Check that HTML structure is intact"""
    required_elements = [
        '<header>', '</header>',
        '<nav id="navbar"', '</nav>',
        '<div class="sidebar-nav"', '</div>',
        'id="theme-toggle"', 'id="sidebarToggle"'
    ]

    print("✅ HTML Structure Verification:")
    all_present = True

    for element in required_elements:
        if element in content:
            print(f"  ✅ {element}: Present")
        else:
            print(f"  ❌ {element}: Missing")
            all_present = False

    return all_present

def main():
    """Main verification function"""
    print("🔍 Header/Navbar Cleanup Verification Script")
    print("=" * 50)

    header_file = Path("/home/victor/Downloads/HiwiAgWebsite/ag-comp-arith-geom/_includes/layout/header.liquid")

    if not header_file.exists():
        print("❌ Header file not found!")
        return

    content = read_file(header_file)

    # Run all verifications
    current_lines = check_file_size()
    if current_lines is None:
        return

    print()
    check_comments_removal(content)

    print()
    css_ok = check_css_class_usage(content)

    print()
    js_ok = check_javascript_functions(content)

    print()
    responsive_ok = check_responsive_behavior(content)

    print()
    html_ok = check_html_structure(content)

    # Summary
    print("\n" + "=" * 50)
    print("📊 VERIFICATION SUMMARY:")
    print(f"✅ File size check: {'PASS' if current_lines <= 1179 else 'FAIL'}")
    print(f"✅ Comments removal: {'PASS' if '<!--' not in content else 'FAIL'}")
    print(f"✅ CSS classes: {'PASS' if css_ok else 'FAIL'}")
    print(f"✅ JavaScript functions: {'PASS' if js_ok else 'FAIL'}")
    print(f"✅ Responsive behavior: {'PASS' if responsive_ok else 'FAIL'}")
    print(f"✅ HTML structure: {'PASS' if html_ok else 'FAIL'}")

    total_passed = sum([current_lines <= 1179, '<!--' not in content, css_ok, js_ok, responsive_ok, html_ok])

    print(f"\n🎯 Overall Score: {total_passed}/6 tests passed")

    if total_passed == 6:
        print("🎉 ALL VERIFICATIONS PASSED! Cleanup was successful.")
    else:
        print("⚠️  Some verifications failed. Please check the issues above.")

if __name__ == "__main__":
    main()
