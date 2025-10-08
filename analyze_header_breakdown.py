#!/usr/bin/env python3
"""
Header File Deep Dive Analysis Script

This script provides a detailed breakdown of what's using the 1179 lines in the header file.
It analyzes:
1. HTML structure breakdown
2. CSS sections breakdown
3. JavaScript breakdown
4. Media queries breakdown
5. Line-by-line analysis
"""

import re
from pathlib import Path

def read_file(file_path):
    """Read file and return content as string"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def count_section_lines(content, start_pattern, end_pattern=None):
    """Count lines in a specific section"""
    lines = content.split('\n')
    in_section = False
    section_lines = []

    for line in lines:
        if start_pattern in line:
            in_section = True

        if in_section:
            section_lines.append(line)

        if end_pattern and end_pattern in line:
            in_section = False

    return len(section_lines)

def analyze_html_sections(content):
    """Analyze HTML sections"""
    print("📄 HTML Structure Breakdown:")

    # Count different HTML sections
    html_sections = {
        "Header opening": '<header>',
        "Skip link": 'skip-link',
        "Main navbar": 'heidelberg-navbar',
        "Brand section": 'brand-text',
        "Desktop navigation": 'navbar-collapse',
        "Sidebar navigation": 'sidebar-nav',
        "Header closing": '</header>',
        "Style section": '<style>',
        "Script section": '<script>',
    }

    total_html = 0
    for name, pattern in html_sections.items():
        count = content.count(pattern)
        lines = count_section_lines(content, pattern) if pattern in ['<header>', '<style>', '<script>'] else count
        print(f"  {name}: {lines} lines/elements")
        total_html += lines if pattern in ['<header>', '<style>', '<script>'] else count

    return total_html

def analyze_css_sections(content):
    """Analyze CSS sections in detail"""
    print("\n🎨 CSS Sections Breakdown:")

    # Extract CSS content
    css_match = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
    if not css_match:
        print("❌ No CSS found in file")
        return 0

    css_content = css_match.group(1)
    css_lines = len(css_content.split('\n'))

    print(f"  Total CSS: {css_lines} lines")

    # Break down by media queries and sections
    media_queries = re.findall(r'@media[^}]+{([^}]*)}', css_content, re.DOTALL)
    print(f"  Media queries: {len(media_queries)}")

    # Count different CSS sections
    css_sections = {
        "Navbar base styles": '.heidelberg-navbar',
        "Brand styles": '.brand-text',
        "Navigation link styles": '.nav-link',
        "Sidebar styles": '.sidebar-nav',
        "Theme toggle styles": '.theme-toggle-btn',
        "Responsive breakpoints": '@media',
        "Dark mode styles": '[data-theme="dark"]',
        "Accessibility styles": '.skip-link',
    }

    section_breakdown = {}
    for name, pattern in css_sections.items():
        count = css_content.count(pattern)
        section_breakdown[name] = count

    # Sort by count
    sorted_sections = sorted(section_breakdown.items(), key=lambda x: x[1], reverse=True)

    for name, count in sorted_sections:
        print(f"  {name}: {count} occurrences")

    return css_lines

def analyze_javascript_sections(content):
    """Analyze JavaScript sections"""
    print("\n⚡ JavaScript Breakdown:")

    # Extract JavaScript content
    script_match = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
    if not script_match:
        print("❌ No JavaScript found in file")
        return 0

    js_content = script_match.group(1)
    js_lines = len(js_content.split('\n'))

    print(f"  Total JavaScript: {js_lines} lines")

    # Break down JavaScript functions
    functions = re.findall(r'function (\w+)', js_content)
    print(f"  Functions defined: {len(functions)}")
    for func in functions:
        print(f"    - {func}")

    # Count event listeners and other JS constructs
    event_listeners = len(re.findall(r'addEventListener', js_content))
    query_selectors = len(re.findall(r'getElementById|querySelector', js_content))

    print(f"  Event listeners: {event_listeners}")
    print(f"  DOM queries: {query_selectors}")

    return js_lines

def analyze_responsive_breakpoints(content):
    """Analyze responsive breakpoints"""
    print("\n📱 Responsive Breakpoints Analysis:")

    # Extract CSS content
    css_match = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
    if not css_match:
        return

    css_content = css_match.group(1)

    breakpoints = {
        "Large screens (1300px+)": '@media (min-width: 1300px)',
        "Medium screens (800-1299px)": '@media (min-width: 800px) and (max-width: 1299.98px)',
        "Small screens (under 800px)": '@media (max-width: 799.98px)',
        "Mobile adjustments": '@media (max-width: 799.98px)',
        "High contrast mode": '@media (prefers-contrast: high)',
        "Reduced motion": '@media (prefers-reduced-motion: reduce)',
    }

    for name, pattern in breakpoints.items():
        count = css_content.count(pattern)
        if count > 0:
            print(f"  {name}: {count} occurrences")

def analyze_line_by_line(content):
    """Analyze content line by line"""
    print("\n🔍 Line-by-Line Analysis:")

    lines = content.split('\n')
    empty_lines = sum(1 for line in lines if not line.strip())
    comment_lines = sum(1 for line in lines if line.strip().startswith('//') or '/*' in line and '*/' in line)

    print(f"  Total lines: {len(lines)}")
    print(f"  Empty lines: {empty_lines}")
    print(f"  Comment lines: {comment_lines}")
    print(f"  Actual content lines: {len(lines) - empty_lines - comment_lines}")

    # Analyze content distribution
    html_lines = sum(1 for line in lines if any(tag in line for tag in ['<header', '<nav', '<div', '<a ', '<button', '</']))
    css_lines = sum(1 for line in lines if any(selector in line for selector in ['.heidelberg-navbar', '.nav-link', '.sidebar-nav', '@media']))
    js_lines = sum(1 for line in lines if any(js_keyword in line for js_keyword in ['function', 'addEventListener', 'querySelector']))

    print(f"  HTML markup lines: {html_lines}")
    print(f"  CSS styling lines: {css_lines}")
    print(f"  JavaScript lines: {js_lines}")

def main():
    """Main analysis function"""
    print("🔍 Header File Deep Dive Analysis")
    print("=" * 60)

    header_file = Path("/home/victor/Downloads/HiwiAgWebsite/ag-comp-arith-geom/_includes/layout/header.liquid")

    if not header_file.exists():
        print("❌ Header file not found!")
        return

    content = read_file(header_file)

    # Run all analyses
    html_lines = analyze_html_sections(content)
    css_lines = analyze_css_sections(content)
    js_lines = analyze_javascript_sections(content)
    analyze_responsive_breakpoints(content)
    analyze_line_by_line(content)

    # Summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY BREAKDOWN:")

    total_lines = len(content.split('\n'))
    print(f"📄 Total file size: {total_lines} lines")

    if css_lines > 0:
        css_percentage = (css_lines / total_lines) * 100
        print(f"🎨 CSS content: {css_lines} lines ({css_percentage:.1f}%)")

    if js_lines > 0:
        js_percentage = (js_lines / total_lines) * 100
        print(f"⚡ JavaScript content: {js_lines} lines ({js_percentage:.1f}%)")

    html_percentage = ((total_lines - css_lines - js_lines) / total_lines) * 100
    print(f"📄 HTML markup: {total_lines - css_lines - js_lines} lines ({html_percentage:.1f}%)")

    print("\n💡 ANALYSIS INSIGHTS:")
    print("  • CSS is the largest section - contains responsive styles, theme styles, etc.")
    print("  • JavaScript handles interactivity (theme toggle, sidebar, responsive behavior)")
    print("  • HTML provides the structure with accessibility features")
    print("  • File is comprehensive but could potentially be split into separate files")

if __name__ == "__main__":
    main()
