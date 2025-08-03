#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

console.log('🔍 SCRAPING OLD HEIDELBERG WEBSITE');
console.log('===================================\n');

// Base URLs from the old website
const BASE_URL = 'https://typo.iwr.uni-heidelberg.de/groups/arith-geom';
const PAGES = [
    '/publications.html',
    '/members/peter-graef.html',
    '/members/gebhard-boeckle/publications.html'
];

// Create directories
const dirs = ['assets/uploads', 'assets/img', 'backup_old_content'];
dirs.forEach(dir => {
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }
});

// Helper function to make HTTP requests
function makeRequest(url) {
    return new Promise((resolve, reject) => {
        const protocol = url.startsWith('https:') ? https : http;
        
        protocol.get(url, (res) => {
            let data = '';
            
            res.on('data', (chunk) => {
                data += chunk;
            });
            
            res.on('end', () => {
                resolve({ statusCode: res.statusCode, data });
            });
        }).on('error', (err) => {
            reject(err);
        });
    });
}

// Helper function to download files
async function downloadFile(url, localPath) {
    return new Promise((resolve, reject) => {
        const protocol = url.startsWith('https:') ? https : http;
        
        protocol.get(url, (res) => {
            if (res.statusCode !== 200) {
                reject(new Error(`Failed to download ${url}: ${res.statusCode}`));
                return;
            }
            
            const fileStream = fs.createWriteStream(localPath);
            res.pipe(fileStream);
            
            fileStream.on('finish', () => {
                fileStream.close();
                console.log(`✅ Downloaded: ${localPath}`);
                resolve();
            });
            
            fileStream.on('error', (err) => {
                fs.unlink(localPath, () => {}); // Delete file on error
                reject(err);
            });
        }).on('error', (err) => {
            reject(err);
        });
    });
}

// Extract PDF links from HTML content
function extractPdfLinks(html, baseUrl) {
    const pdfLinks = [];
    const pdfRegex = /href\s*=\s*["']([^"']*\.pdf[^"']*)["']/gi;
    let match;
    
    while ((match = pdfRegex.exec(html)) !== null) {
        let url = match[1];
        if (url.startsWith('/')) {
            url = 'https://typo.iwr.uni-heidelberg.de' + url;
        } else if (!url.startsWith('http')) {
            url = baseUrl + '/' + url;
        }
        pdfLinks.push(url);
    }
    
    return [...new Set(pdfLinks)]; // Remove duplicates
}

// Extract publication data from HTML
function extractPublications(html) {
    const publications = [];
    
    // Extract from publications page
    const pubMatches = html.match(/<li[^>]*>([^<]+)<\/li>/g);
    if (pubMatches) {
        pubMatches.forEach(match => {
            const text = match.replace(/<[^>]*>/g, '').trim();
            if (text && text.length > 10) {
                publications.push(text);
            }
        });
    }
    
    return publications;
}

// Main scraping function
async function scrapeWebsite() {
    console.log('🌐 Starting website scraping...\n');
    
    const allPdfLinks = [];
    const allPublications = [];
    const scrapedContent = {};
    
    // Scrape each page
    for (const page of PAGES) {
        const url = BASE_URL + page;
        console.log(`📄 Scraping: ${url}`);
        
        try {
            const response = await makeRequest(url);
            if (response.statusCode === 200) {
                const html = response.data;
                scrapedContent[page] = html;
                
                // Extract PDF links
                const pdfLinks = extractPdfLinks(html, BASE_URL);
                allPdfLinks.push(...pdfLinks);
                
                // Extract publications
                const publications = extractPublications(html);
                allPublications.push(...publications);
                
                console.log(`   Found ${pdfLinks.length} PDF links`);
                console.log(`   Found ${publications.length} publications`);
                
                // Save HTML content
                const filename = page.replace(/\//g, '_').replace('.html', '.html');
                fs.writeFileSync(`backup_old_content${filename}`, html);
                console.log(`   Saved HTML: backup_old_content${filename}`);
                
            } else {
                console.log(`   ❌ Failed to fetch: ${response.statusCode}`);
            }
        } catch (error) {
            console.log(`   ❌ Error scraping ${url}: ${error.message}`);
        }
    }
    
    // Remove duplicate PDF links
    const uniquePdfLinks = [...new Set(allPdfLinks)];
    console.log(`\n📊 Found ${uniquePdfLinks.length} unique PDF links`);
    
    // Download PDFs
    console.log('\n📥 Downloading PDFs...');
    for (let i = 0; i < uniquePdfLinks.length; i++) {
        const pdfUrl = uniquePdfLinks[i];
        const filename = path.basename(pdfUrl);
        const localPath = `assets/uploads/${filename}`;
        
        // Skip if already exists
        if (fs.existsSync(localPath)) {
            console.log(`⏭️  Skipping (exists): ${filename}`);
            continue;
        }
        
        try {
            await downloadFile(pdfUrl, localPath);
        } catch (error) {
            console.log(`❌ Failed to download ${filename}: ${error.message}`);
        }
        
        // Add delay to be respectful to the server
        await new Promise(resolve => setTimeout(resolve, 1000));
    }
    
    // Save extracted data
    console.log('\n💾 Saving extracted data...');
    
    // Save PDF links
    fs.writeFileSync('backup_old_content/pdf_links.json', JSON.stringify(uniquePdfLinks, null, 2));
    console.log('   Saved: backup_old_content/pdf_links.json');
    
    // Save publications
    fs.writeFileSync('backup_old_content/publications.json', JSON.stringify(allPublications, null, 2));
    console.log('   Saved: backup_old_content/publications.json');
    
    // Save scraped content summary
    const summary = {
        scrapedPages: PAGES,
        totalPdfLinks: uniquePdfLinks.length,
        totalPublications: allPublications.length,
        timestamp: new Date().toISOString()
    };
    fs.writeFileSync('backup_old_content/scraping_summary.json', JSON.stringify(summary, null, 2));
    console.log('   Saved: backup_old_content/scraping_summary.json');
    
    console.log('\n🎉 Scraping completed!');
    console.log(`📊 Summary:`);
    console.log(`   Pages scraped: ${PAGES.length}`);
    console.log(`   PDF links found: ${uniquePdfLinks.length}`);
    console.log(`   Publications found: ${allPublications.length}`);
}

// Run the scraper
scrapeWebsite().catch(console.error); 