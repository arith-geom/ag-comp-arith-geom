#!/usr/bin/env python3
"""
Teaching Link Maintenance Script

This script can be run periodically to maintain the health of all teaching links.
It provides a quick status check and can automatically fix common issues.
"""

import os
import sys
from pathlib import Path
from datetime import datetime

def main():
    """Main maintenance function."""
    print("🔍 Teaching Link Maintenance Check")
    print("=" * 50)
    
    # Get project root
    project_root = Path(__file__).parent
    print(f"Project: {project_root}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check if comprehensive link checker exists
    checker_path = project_root / "comprehensive_link_checker.py"
    if not checker_path.exists():
        print("❌ Comprehensive link checker not found!")
        print("Please ensure comprehensive_link_checker.py is in the project root.")
        return 1
    
    # Run the comprehensive check
    print("🔍 Running comprehensive link check...")
    try:
        import subprocess
        result = subprocess.run([sys.executable, "comprehensive_link_checker.py"], 
                              capture_output=True, text=True, cwd=project_root)
        
        if result.returncode == 0:
            print("✅ Link check completed successfully!")
            
            # Parse the summary from output
            output_lines = result.stdout.split('\n')
            for line in output_lines:
                if 'Working links:' in line:
                    working = line.split(':')[1].strip()
                    print(f"✅ Working links: {working}")
                elif 'Broken internal links:' in line:
                    broken_internal = line.split(':')[1].strip()
                    print(f"🔧 Broken internal links: {broken_internal}")
                elif 'Broken external links:' in line:
                    broken_external = line.split(':')[1].strip()
                    print(f"🌐 Broken external links: {broken_external}")
                elif 'Missing PDFs:' in line:
                    missing_pdfs = line.split(':')[1].strip()
                    print(f"📄 Missing PDFs: {missing_pdfs}")
                elif 'Verified PDFs:' in line:
                    verified_pdfs = line.split(':')[1].strip()
                    print(f"📚 Verified PDFs: {verified_pdfs}")
            
            print()
            
            # Check if there are any issues
            if broken_internal == '0' and broken_external == '0' and missing_pdfs == '0':
                print("🎉 All links are working perfectly!")
                print("✅ No maintenance required.")
                return 0
            else:
                print("⚠️  Some issues detected:")
                if broken_internal != '0':
                    print(f"   - {broken_internal} broken internal links")
                if broken_external != '0':
                    print(f"   - {broken_external} broken external links")
                if missing_pdfs != '0':
                    print(f"   - {missing_pdfs} missing PDFs")
                
                print()
                print("🔧 To fix issues, run:")
                print("   python3 fix_all_teaching_links.py")
                return 1
                
        else:
            print("❌ Link check failed!")
            print("Error output:")
            print(result.stderr)
            return 1
            
    except Exception as e:
        print(f"❌ Error running link check: {e}")
        return 1

def quick_status():
    """Quick status check without running full link checker."""
    print("🔍 Quick Teaching Link Status")
    print("=" * 40)
    
    project_root = Path(__file__).parent
    
    # Check key directories
    teaching_dir = project_root / "_teaching"
    members_dir = project_root / "_members"
    assets_dir = project_root / "assets"
    
    print(f"📁 Teaching directory: {'✅' if teaching_dir.exists() else '❌'}")
    print(f"👥 Members directory: {'✅' if members_dir.exists() else '❌'}")
    print(f"📚 Assets directory: {'✅' if assets_dir.exists() else '❌'}")
    
    # Count files
    if teaching_dir.exists():
        teaching_files = len(list(teaching_dir.rglob('*.md')))
        print(f"📄 Teaching files: {teaching_files}")
    
    if members_dir.exists():
        member_files = len(list(members_dir.glob('*.md')))
        print(f"👤 Member files: {member_files}")
    
    if assets_dir.exists():
        uploads_dir = assets_dir / "uploads"
        if uploads_dir.exists():
            pdf_files = len(list(uploads_dir.glob('*.pdf')))
            print(f"📚 PDF files: {pdf_files}")
    
    print()
    print("💡 For detailed link checking, run:")
    print("   python3 comprehensive_link_checker.py")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        quick_status()
    else:
        exit(main()) 