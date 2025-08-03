# Publications CMS Guide

## Overview

The Publications CMS system has been completely modernized and enhanced to provide a comprehensive solution for managing academic publications, software packages, and research outputs. This guide explains how to use the new system effectively.

## 🎯 **Key Features**

### **Enhanced Publication Management**
- **Comprehensive Metadata**: Title, authors, year, journal, DOI, arXiv ID, abstract, keywords
- **Publication Types**: Journal articles, conference papers, preprints, software packages, theses, books
- **Status Tracking**: Published, submitted, under review, in preparation, accepted, in press
- **Metrics Integration**: Impact factors, citation counts, publication dates
- **File Management**: PDF uploads, supplementary materials
- **Relationships**: Link publications to team members and research areas

### **Software Package Support**
- **Repository Links**: GitHub, GitLab, or other repository URLs
- **Download Links**: Direct download URLs for software packages
- **Version Tracking**: Software version numbers and release dates
- **License Information**: Open source licenses and terms
- **Documentation Links**: Links to documentation and user guides

### **Advanced Filtering & Search**
- **Type-based Filtering**: Filter by publication type (papers, software, etc.)
- **Status Filtering**: Filter by publication status
- **Year Filtering**: Filter by publication year
- **Full-text Search**: Search across titles, authors, abstracts, and keywords
- **Quick Filters**: One-click filtering for common views

### **Modern Display System**
- **Responsive Design**: Works perfectly on all devices
- **Publication Cards**: Clean, modern card-based layout
- **Statistics Dashboard**: Live publication counts and metrics
- **Interactive Elements**: Hover effects, smooth transitions
- **Accessibility**: WCAG compliant design

## 📝 **Adding Publications via CMS**

### **Step 1: Access the CMS**
1. Navigate to your website's admin panel
2. Click on "Publications" in the content management section
3. Click "Add New Publication"

### **Step 2: Fill in Basic Information**
- **Publication Title**: Enter the full title of the publication
- **Authors**: List all authors separated by commas
- **Publication Year**: Year when published or submitted
- **Publication Month**: Optional month of publication
- **Publication Type**: Select from dropdown (Journal Article, Software Package, etc.)
- **Status**: Current status of the publication

### **Step 3: Add Publication Details**
- **Journal/Conference/Publisher**: Where the publication appears
- **Volume/Issue**: Volume number, issue number, or proceedings details
- **Pages**: Page range or article number
- **DOI**: Digital Object Identifier (if available)
- **arXiv ID**: arXiv identifier (if applicable)
- **Abstract**: Brief description of the publication's content
- **Keywords**: Comma-separated keywords for searchability

### **Step 4: Add Links and Files**
- **Publication URL**: Direct link to the publication
- **PDF File**: Upload the publication PDF (if available)
- **Repository URL**: For software packages, link to source code
- **Download URL**: For software packages, direct download link

### **Step 5: Add Software Information (for Software Packages)**
- **Repository URL**: Link to GitHub, GitLab, etc.
- **Download URL**: Direct download link
- **Version**: Current version number
- **License**: Software license (MIT, GPL, etc.)
- **Documentation URL**: Link to documentation

### **Step 6: Add Relationships**
- **Team Members Involved**: Select team members who are authors/contributors
- **Related Research Areas**: Select research areas this publication relates to
- **Featured Publication**: Mark as featured to highlight on main page

### **Step 7: Add Metrics (Optional)**
- **Journal Impact Factor**: If available
- **Citation Count**: Number of citations (can be updated periodically)

### **Step 8: Save and Publish**
- Click "Save" to store the publication
- The publication will automatically appear on the website

## 🔍 **Managing Publications**

### **Viewing Publications**
- **All Publications**: View all publications in chronological order
- **By Type**: Group publications by type (papers, software, etc.)
- **By Status**: Group by publication status
- **Featured**: View only featured publications
- **Recent**: View publications from 2020 onwards
- **Software**: View only software packages

### **Editing Publications**
1. Find the publication in the CMS
2. Click "Edit" to modify any field
3. Update information as needed
4. Save changes

### **Deleting Publications**
1. Find the publication in the CMS
2. Click "Delete" (use with caution)
3. Confirm deletion

## 🎨 **Display Features**

### **Publication Cards**
Each publication is displayed as a modern card with:
- **Header**: Type badge, status, year, title, authors, venue
- **Body**: Abstract preview, keywords
- **Footer**: Links (DOI, arXiv, PDF, etc.), metrics

### **Statistics Dashboard**
Live statistics showing:
- Total number of publications
- Recent publications (2020+)
- Software packages count
- Featured publications count

### **Filtering System**
- **Type Filter**: Filter by publication type
- **Status Filter**: Filter by publication status
- **Year Filter**: Filter by publication year
- **Search**: Full-text search across all fields
- **Quick Filters**: One-click filtering buttons

## 📱 **Responsive Design**

The publications system is fully responsive:
- **Desktop**: Full grid layout with sidebar
- **Tablet**: Adjusted grid with optimized spacing
- **Mobile**: Single-column layout with touch-friendly controls

## 🔗 **Integration Features**

### **Team Member Integration**
- Link publications to team members
- Publications appear on member profile pages
- Automatic author highlighting

### **Research Area Integration**
- Link publications to research areas
- Publications appear on research area pages
- Cross-referencing between content

### **Search Integration**
- Publications are included in site-wide search
- Full-text search across all publication fields
- Search results show publication type and year

## 📊 **Data Management**

### **Backup System**
- Automatic daily backups of publication data
- 30-day retention period
- Easy restoration if needed

### **Export Options**
- Export publications as JSON
- Export as BibTeX format
- Export as CSV for spreadsheet analysis

### **Import Options**
- Import from BibTeX files
- Import from CSV files
- Bulk import from external sources

## 🛠 **Technical Details**

### **CMS Configuration**
The publications content type is configured in `pagescms.config.json` with:
- **25+ fields** for comprehensive metadata
- **Validation rules** for data quality
- **Multiple views** for different display options
- **Reference fields** for content relationships

### **Frontend Implementation**
- **Modern JavaScript** for interactive features
- **CSS Grid/Flexbox** for responsive layouts
- **Accessibility features** for screen readers
- **Performance optimized** for fast loading

### **File Management**
- **PDF uploads** with size limits (50MB)
- **Image optimization** for thumbnails
- **Secure file storage** with access controls

## 🎯 **Best Practices**

### **Adding Publications**
1. **Complete Information**: Fill in all available fields for better searchability
2. **Consistent Formatting**: Use consistent author name formats
3. **Keywords**: Add relevant keywords for better search results
4. **Links**: Include all relevant links (DOI, arXiv, repository, etc.)
5. **Files**: Upload PDFs when available

### **Managing Software Packages**
1. **Repository Links**: Always include repository URLs
2. **Version Numbers**: Keep version numbers updated
3. **Documentation**: Link to documentation when available
4. **License Information**: Include license details
5. **Download Links**: Provide direct download links

### **Content Organization**
1. **Featured Publications**: Mark important publications as featured
2. **Keywords**: Use consistent keyword terminology
3. **Team Member Links**: Link publications to relevant team members
4. **Research Area Links**: Link publications to research areas
5. **Status Updates**: Keep publication status current

## 🔧 **Troubleshooting**

### **Common Issues**

**Publication not appearing on website:**
- Check if publication is saved and published
- Verify all required fields are filled
- Check for any validation errors

**Search not finding publications:**
- Ensure keywords are properly added
- Check that abstract text is complete
- Verify author names are spelled correctly

**File upload issues:**
- Check file size limits (50MB for PDFs)
- Verify file format is supported
- Ensure sufficient storage space

**Display issues:**
- Clear browser cache
- Check for JavaScript errors
- Verify CSS is loading properly

### **Getting Help**
- Check the CMS documentation
- Review the configuration files
- Contact the system administrator
- Check browser console for errors

## 🚀 **Future Enhancements**

### **Planned Features**
- **Citation Import**: Import citations from external databases
- **Impact Metrics**: Automatic impact factor updates
- **Collaboration Tracking**: Track collaborations with other institutions
- **Analytics Dashboard**: Detailed publication analytics
- **Export Formats**: Additional export formats (EndNote, Mendeley)

### **Integration Opportunities**
- **ORCID Integration**: Link publications to ORCID profiles
- **Google Scholar**: Automatic citation updates
- **Research Gate**: Integration with Research Gate profiles
- **Institutional Repository**: Integration with university repositories

## 📞 **Support**

For technical support or questions about the Publications CMS system:
- **Email**: admin@mathi.uni-heidelberg.de
- **Documentation**: Check this guide and related documentation
- **Training**: Contact for training sessions on CMS usage

---

**Last Updated**: January 2025  
**Version**: 2.0  
**Status**: ✅ Production Ready 