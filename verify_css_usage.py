#!/usr/bin/env python3
"""
CSS Usage Verification Script

This script checks if all CSS rules in the header file are actually used.
It analyzes:
1. CSS selectors defined in the <style> block
2. Usage of these selectors in HTML structure
3. Usage of these selectors in JavaScript code
4. Identifies unused CSS rules
"""

import re
from pathlib import Path

def read_file(file_path):
    """Read file and return content as string"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_css_selectors(css_content):
    """Extract all CSS selectors from the style block"""
    # Find all CSS rules
    rules = re.findall(r'([^{]+){([^}]*)}', css_content)

    selectors = set()
    for selector, properties in rules:
        selector = selector.strip()
        # Handle multiple selectors separated by commas
        individual_selectors = [s.strip() for s in selector.split(',')]
        for sel in individual_selectors:
            # Handle pseudo-selectors and media queries
            base_selector = sel.split(':')[0].split('::')[0].split('@')[0].strip()
            if base_selector.startswith('.'):
                selectors.add(base_selector)

    return selectors

def check_html_usage(content, selectors):
    """Check which selectors are used in HTML"""
    html_selectors = set()

    # Find all class attributes in HTML
    class_matches = re.findall(r'class="([^"]*)"', content)
    for classes in class_matches:
        for class_name in classes.split():
            if class_name.startswith('.'):
                class_name = class_name[1:]  # Remove leading dot
            html_selectors.add(f'.{class_name}')

    # Find all id attributes
    id_matches = re.findall(r'id="([^"]*)"', content)
    for id_name in id_matches:
        html_selectors.add(f'#{id_name}')

    # Find usage in HTML (not just class/id attributes but also in content)
    used_selectors = set()
    for selector in selectors:
        if selector in content:
            used_selectors.add(selector)

    return used_selectors, html_selectors

def check_js_usage(content, selectors):
    """Check which selectors are used in JavaScript"""
    js_selectors = set()

    # Extract JavaScript content
    script_match = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
    if script_match:
        js_content = script_match.group(1)

        # Look for className, classList, querySelector, getElementById usage
        class_usage = re.findall(r'\.(\w+)', js_content)
        id_usage = re.findall(r'getElementById\(["\']([^"\']+)["\']\)', js_content)
        query_usage = re.findall(r'querySelector\(["\']([^"\']+)["\']\)', js_content)
        query_all_usage = re.findall(r'querySelectorAll\(["\']([^"\']+)["\']\)', js_content)

        for class_name in class_usage:
            js_selectors.add(f'.{class_name}')

        for id_name in id_usage:
            js_selectors.add(f'#{id_name}')

        for query in query_usage + query_all_usage:
            # Handle complex selectors in querySelector
            if query.startswith('.'):
                js_selectors.add(query)
            elif query.startswith('#'):
                js_selectors.add(query)

    return js_selectors

def analyze_css_usage():
    """Main analysis function"""
    print("🔍 CSS Usage Verification")
    print("=" * 50)

    header_file = Path("/home/victor/Downloads/HiwiAgWebsite/ag-comp-arith-geom/_includes/layout/header.liquid")

    if not header_file.exists():
        print("❌ Header file not found!")
        return

    content = read_file(header_file)

    # Extract CSS content
    css_match = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
    if not css_match:
        print("❌ No CSS found in file!")
        return

    css_content = css_match.group(1)

    # Extract all CSS selectors
    all_selectors = extract_css_selectors(css_content)
    print(f"📊 Total CSS selectors found: {len(all_selectors)}")

    # Check HTML usage
    html_used, html_selectors = check_html_usage(content, all_selectors)
    print(f"✅ Selectors used in HTML: {len(html_used)}")

    # Check JavaScript usage
    js_used = check_js_usage(content, all_selectors)
    print(f"✅ Selectors used in JavaScript: {len(js_used)}")

    # Find unused selectors
    all_used = html_used | js_used
    unused_selectors = all_selectors - all_used

    print(f"\n📋 USAGE SUMMARY:")
    print(f"  • Total selectors: {len(all_selectors)}")
    print(f"  • Used in HTML: {len(html_used)}")
    print(f"  • Used in JavaScript: {len(js_used)}")
    print(f"  • Total used: {len(all_used)}")
    print(f"  • Unused selectors: {len(unused_selectors)}")

    if unused_selectors:
        print(f"\n⚠️  UNUSED SELECTORS ({len(unused_selectors)}):")
        for selector in sorted(unused_selectors):
            print(f"    {selector}")

        # Check if these are used in CSS but not directly in HTML/JS
        print("\n🔍 Checking if unused selectors are used in CSS...")
        css_used_in_css = set()
        for selector in unused_selectors:
            # Remove the dot for class matching
            class_name = selector[1:] if selector.startswith('.') else selector
            if f'.{class_name}' in css_content or f'#{class_name}' in css_content:
                css_used_in_css.add(selector)

        print(f"  • Selectors used within CSS: {len(css_used_in_css)}")
        if css_used_in_css:
            for selector in sorted(css_used_in_css):
                print(f"    {selector} (used in CSS)")

        truly_unused = unused_selectors - css_used_in_css
        print(f"  • Truly unused selectors: {len(truly_unused)}")
        if truly_unused:
            print("  🎯 These can be safely removed:")
            for selector in sorted(truly_unused):
                print(f"    {selector}")
    else:
        print("\n🎉 All CSS selectors are used!")

    # Calculate usage percentage
    usage_percentage = (len(all_used) / len(all_selectors)) * 100 if all_selectors else 0
    print(f"\n📈 Usage Rate: {usage_percentage:.1f}% ({len(all_used)}/{len(all_selectors)})")

    if usage_percentage >= 90:
        print("✅ Excellent usage rate!")
    elif usage_percentage >= 75:
        print("⚠️  Good usage rate, but some optimization possible")
    else:
        print("❌ Poor usage rate - significant optimization needed")

if __name__ == "__main__":
    analyze_css_usage()
