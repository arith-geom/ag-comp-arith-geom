#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

console.log('🔍 PROCESSING SCRAPED CONTENT');
console.log('==============================\n');

// Read scraped data
const pdfLinks = JSON.parse(fs.readFileSync('backup_old_content/pdf_links.json', 'utf8'));
const publications = JSON.parse(fs.readFileSync('backup_old_content/publications.json', 'utf8'));
const summary = JSON.parse(fs.readFileSync('backup_old_content/scraping_summary.json', 'utf8'));

console.log(`📊 Loaded data:`);
console.log(`   PDF links: ${pdfLinks.length}`);
console.log(`   Publications: ${publications.length}`);

// Parse the scraped HTML files to extract detailed publication information
function parsePublicationsFromHTML() {
    const allPublications = [];
    
    // Read the scraped HTML files
    const htmlFiles = [
        'backup_old_content_publications.html',
        'backup_old_content_members_peter-graef.html',
        'backup_old_content_members_gebhard-boeckle_publications.html'
    ];
    
    htmlFiles.forEach(file => {
        if (fs.existsSync(file)) {
            const html = fs.readFileSync(file, 'utf8');
            
            // Extract publication information based on the structure
            if (file.includes('gebhard-boeckle')) {
                // Parse Prof. Böckle's publications
                const pubMatches = html.match(/<li[^>]*>([^<]+)<\/li>/g);
                if (pubMatches) {
                    pubMatches.forEach(match => {
                        const text = match.replace(/<[^>]*>/g, '').trim();
                        if (text && text.length > 20 && text.includes('(')) {
                            allPublications.push({
                                author: 'Gebhard Böckle',
                                title: text,
                                source: 'gebhard-boeckle'
                            });
                        }
                    });
                }
            } else if (file.includes('peter-graef')) {
                // Parse Peter Gräf's publications
                const pubMatches = html.match(/<li[^>]*>([^<]+)<\/li>/g);
                if (pubMatches) {
                    pubMatches.forEach(match => {
                        const text = match.replace(/<[^>]*>/g, '').trim();
                        if (text && text.length > 20 && text.includes('(')) {
                            allPublications.push({
                                author: 'Peter Gräf',
                                title: text,
                                source: 'peter-graef'
                            });
                        }
                    });
                }
            }
        }
    });
    
    return allPublications;
}

// Create publication markdown files
function createPublicationFiles(publications) {
    console.log('\n📝 Creating publication files...');
    
    publications.forEach((pub, index) => {
        const filename = `_publications/${index + 1}-${pub.author.toLowerCase().replace(/\s+/g, '-')}-publication.md`;
        
        // Create the content
        const content = `---
layout: publication
title: "${pub.title}"
author: "${pub.author}"
date: ${new Date().toISOString().split('T')[0]}
source: "${pub.source}"
---

${pub.title}

## Author
${pub.author}

## Source
Extracted from ${pub.source} page on the old Heidelberg website.

## Notes
This publication was automatically extracted from the old website. Please verify and update the information as needed.
`;
        
        // Ensure directory exists
        if (!fs.existsSync('_publications')) {
            fs.mkdirSync('_publications', { recursive: true });
        }
        
        // Write file
        fs.writeFileSync(filename, content);
        console.log(`   Created: ${filename}`);
    });
}

// Create a comprehensive publications list
function createPublicationsList(pdfLinks) {
    console.log('\n📋 Creating publications list...');
    
    const publicationsList = [];
    
    // Map PDF filenames to potential publications
    pdfLinks.forEach(pdfUrl => {
        const filename = path.basename(pdfUrl);
        const nameWithoutExt = path.basename(filename, '.pdf');
        
        // Try to extract meaningful information from filename
        let title = nameWithoutExt;
        let author = 'Unknown';
        let year = null;
        
        // Extract year if present
        const yearMatch = nameWithoutExt.match(/(\d{4})/);
        if (yearMatch) {
            year = yearMatch[1];
        }
        
        // Try to identify author from filename patterns
        if (nameWithoutExt.includes('Boeckle')) {
            author = 'Gebhard Böckle';
        } else if (nameWithoutExt.includes('Graef') || nameWithoutExt.includes('Peter')) {
            author = 'Peter Gräf';
        } else if (nameWithoutExt.includes('Cakir')) {
            author = 'Burak Cakir';
        } else if (nameWithoutExt.includes('Banwait')) {
            author = 'Barinder Banwait';
        }
        
        publicationsList.push({
            filename,
            title,
            author,
            year,
            url: pdfUrl,
            localPath: `assets/uploads/${filename}`
        });
    });
    
    // Save the list
    fs.writeFileSync('backup_old_content/publications_list.json', JSON.stringify(publicationsList, null, 2));
    console.log(`   Saved: backup_old_content/publications_list.json`);
    
    return publicationsList;
}

// Create a summary report
function createSummaryReport(pdfLinks, publications, publicationsList) {
    console.log('\n📊 Creating summary report...');
    
    const report = {
        timestamp: new Date().toISOString(),
        summary: {
            totalPdfs: pdfLinks.length,
            totalPublications: publications.length,
            processedPublications: publicationsList.length
        },
        authors: {},
        years: {},
        fileTypes: {}
    };
    
    // Analyze by author
    publicationsList.forEach(pub => {
        if (!report.authors[pub.author]) {
            report.authors[pub.author] = 0;
        }
        report.authors[pub.author]++;
        
        if (pub.year) {
            if (!report.years[pub.year]) {
                report.years[pub.year] = 0;
            }
            report.years[pub.year]++;
        }
    });
    
    // Analyze file types
    pdfLinks.forEach(url => {
        const ext = path.extname(url).toLowerCase();
        if (!report.fileTypes[ext]) {
            report.fileTypes[ext] = 0;
        }
        report.fileTypes[ext]++;
    });
    
    // Save report
    fs.writeFileSync('backup_old_content/analysis_report.json', JSON.stringify(report, null, 2));
    console.log(`   Saved: backup_old_content/analysis_report.json`);
    
    // Print summary
    console.log('\n📈 ANALYSIS SUMMARY:');
    console.log(`   Total PDFs: ${pdfLinks.length}`);
    console.log(`   Publications found: ${publications.length}`);
    console.log(`   Processed publications: ${publicationsList.length}`);
    
    console.log('\n👥 By Author:');
    Object.entries(report.authors).forEach(([author, count]) => {
        console.log(`   ${author}: ${count} publications`);
    });
    
    console.log('\n📅 By Year:');
    Object.entries(report.years).sort(([a], [b]) => b - a).forEach(([year, count]) => {
        console.log(`   ${year}: ${count} publications`);
    });
    
    console.log('\n📁 File Types:');
    Object.entries(report.fileTypes).forEach(([ext, count]) => {
        console.log(`   ${ext}: ${count} files`);
    });
}

// Main processing function
async function processContent() {
    console.log('🔄 Processing scraped content...\n');
    
    // Parse publications from HTML
    const parsedPublications = parsePublicationsFromHTML();
    console.log(`   Parsed ${parsedPublications.length} publications from HTML`);
    
    // Create publication files
    createPublicationFiles(parsedPublications);
    
    // Create publications list
    const publicationsList = createPublicationsList(pdfLinks);
    
    // Create summary report
    createSummaryReport(pdfLinks, publications, publicationsList);
    
    console.log('\n🎉 Content processing completed!');
    console.log('\n📁 Generated files:');
    console.log('   - _publications/ (publication markdown files)');
    console.log('   - backup_old_content/publications_list.json');
    console.log('   - backup_old_content/analysis_report.json');
    console.log('   - assets/uploads/ (all downloaded PDFs)');
}

// Run the processor
processContent().catch(console.error); 