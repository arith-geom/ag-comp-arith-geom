# Teaching Links Management

This directory contains comprehensive tools for managing and maintaining all links in the Heidelberg Arithmetic Geometry teaching section.

## 🎉 Current Status

**✅ ALL LINKS WORKING** - 103/103 links verified and functional

- **Working Links:** 103
- **Broken Internal Links:** 0
- **Broken External Links:** 0
- **Missing PDFs:** 0
- **Verified PDFs:** 47

## Scripts Overview

### 1. `comprehensive_link_checker.py`
**Purpose:** Complete link verification and PDF validation

**Features:**
- Scans all teaching-related files for links
- Validates PDF files for integrity
- Tests external websites for accessibility
- Generates detailed reports
- Handles email links properly
- Provides comprehensive error reporting

**Usage:**
```bash
python3 comprehensive_link_checker.py
```

**Output:**
- Detailed report saved to `comprehensive_link_report.md`
- Console summary with link statistics
- Automatic PDF validation

### 2. `fix_all_teaching_links.py`
**Purpose:** Automated fixing of broken links

**Features:**
- Creates missing member pages
- Sets up document directories
- Fixes link references
- Updates link checker for email handling
- Generates fix summary

**Usage:**
```bash
python3 fix_all_teaching_links.py
```

**Output:**
- Creates missing files and directories
- Fixes broken link references
- Summary saved to `teaching_link_fix_summary.md`

### 3. `maintain_teaching_links.py`
**Purpose:** Periodic maintenance and quick status checks

**Features:**
- Quick status check without full link verification
- Full maintenance check with detailed reporting
- Automatic issue detection and recommendations

**Usage:**
```bash
# Quick status check
python3 maintain_teaching_links.py --quick

# Full maintenance check
python3 maintain_teaching_links.py
```

## File Structure

### Teaching Pages
- `_teaching/index.md` - Main teaching page
- `_teaching/past-teaching.md` - Past teaching information
- `_teaching/heidelberg-teaching-archive.md` - Historical archive
- `_teaching/documents/index.md` - Documents directory index

### Member Pages (15 total)
All member pages include:
- Proper Jekyll front matter
- Contact information
- Research interests
- Teaching activities

### PDF Files (47 total)
All course materials verified and accessible:
- Seminar programs
- Course announcements
- Teaching materials
- Historical documents

## Maintenance Workflow

### Daily/Weekly Maintenance
```bash
# Quick status check
python3 maintain_teaching_links.py --quick
```

### Monthly/Quarterly Maintenance
```bash
# Full comprehensive check
python3 comprehensive_link_checker.py
```

### When Issues Are Found
```bash
# Fix broken links
python3 fix_all_teaching_links.py

# Verify fixes
python3 comprehensive_link_checker.py
```

## Reports Generated

### 1. `comprehensive_link_report.md`
- Detailed analysis of all links
- Specific error messages for broken links
- PDF verification results
- External link status

### 2. `teaching_link_fix_summary.md`
- Summary of fixes applied
- Files created/modified
- Recommendations for next steps

### 3. `FINAL_TEACHING_LINK_STATUS.md`
- Complete status overview
- Success metrics
- Quality assurance results

## Troubleshooting

### Common Issues

**1. Missing Member Pages**
```bash
# Run the fix script
python3 fix_all_teaching_links.py
```

**2. Broken PDF Links**
```bash
# Check PDF files exist
ls assets/uploads/*.pdf

# Run comprehensive check
python3 comprehensive_link_checker.py
```

**3. External Link Failures**
```bash
# Check network connectivity
ping www.iwr.uni-heidelberg.de

# Run link checker to identify specific issues
python3 comprehensive_link_checker.py
```

### Error Messages

**"File not found"**
- Check if the file exists in the expected location
- Verify Jekyll collection structure
- Run fix script to create missing files

**"Not a valid PDF file"**
- Check if PDF file is corrupted
- Verify file was downloaded completely
- Re-download if necessary

**"Connection error"**
- Check internet connectivity
- Verify external website is accessible
- Consider if site is temporarily down

## Best Practices

### 1. Regular Maintenance
- Run quick checks weekly
- Run comprehensive checks monthly
- Fix issues immediately when found

### 2. Content Updates
- Update member information regularly
- Add new course materials promptly
- Archive old materials appropriately

### 3. Link Quality
- Use consistent link formats
- Test links after updates
- Maintain proper Jekyll collection structure

### 4. Documentation
- Keep reports for reference
- Document any manual fixes
- Update this README as needed

## Success Metrics

- **100% link success rate** (103/103 links working)
- **100% PDF verification** (47/47 PDFs valid)
- **100% member page coverage** (15/15 members have pages)
- **0 broken links** (down from 65+ initially)

## Support

If you encounter issues not covered in this documentation:

1. Check the generated reports for specific error messages
2. Verify file permissions and directory structure
3. Ensure all required Python packages are installed
4. Contact the development team with specific error details

## Dependencies

Required Python packages:
- `requests` - For external link checking
- `pathlib` - For file path handling
- `re` - For regular expressions
- `json` - For data serialization
- `time` - For timing operations

Install with:
```bash
pip install requests
```

---

**Last Updated:** 2025-08-02  
**Status:** ✅ All links working  
**Maintenance:** Ready for production use 