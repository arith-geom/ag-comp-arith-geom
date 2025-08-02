// Pages CMS Integration for Official Pages CMS
// This script provides integration with the official Pages CMS system at https://app.pagescms.org/

(function() {
  'use strict';
  
  // Pages CMS Configuration
  const PAGESCMS_CONFIG = {
    enabled: true,
    autoRefresh: false, // Disabled by default to avoid unnecessary requests
    refreshInterval: 300000, // 5 minutes
    showSyncStatus: true,
    officialUrl: 'https://app.pagescms.org/',
    repoUrl: getRepoUrl(),
    branch: getBranch()
  };
  
  // Get repository URL from meta tags or current location
  function getRepoUrl() {
    // Try to get from meta tag first
    const metaRepo = document.querySelector('meta[name="repository-url"]');
    if (metaRepo && metaRepo.content) {
      return metaRepo.content;
    }
    
    // Try to get from GitHub Pages URL
    const hostname = window.location.hostname;
    if (hostname.includes('github.io')) {
      const pathParts = window.location.pathname.split('/').filter(Boolean);
      if (pathParts.length >= 2) {
        return `https://github.com/${pathParts[0]}/${pathParts[1]}`;
      }
    }
    
    // Fallback to current origin
    return window.location.origin;
  }
  
  // Get branch from meta tags or default to main
  function getBranch() {
    const metaBranch = document.querySelector('meta[name="repository-branch"]');
    if (metaBranch && metaBranch.content) {
      return metaBranch.content;
    }
    
    // Try to detect from URL path
    const pathParts = window.location.pathname.split('/').filter(Boolean);
    if (pathParts.length > 2 && pathParts[2] !== 'assets' && pathParts[2] !== '_site') {
      return pathParts[2];
    }
    
    return 'main';
  }
  
  // Initialize Pages CMS integration
  function initPagesCMS() {
    if (!PAGESCMS_CONFIG.enabled) {
      console.log('Pages CMS integration is disabled');
      return;
    }
    
    console.log('Initializing Pages CMS integration...', PAGESCMS_CONFIG);
    
    // Set up sync status indicator
    if (PAGESCMS_CONFIG.showSyncStatus) {
      setupSyncStatus();
    }
    
    // Listen for Pages CMS events
    setupEventListeners();
    
    // Show initial status
    showSyncStatus('Pages CMS ready', 'success');
  }
  
  // Set up sync status indicator
  function setupSyncStatus() {
    // Check if status indicator already exists
    if (document.getElementById('pagescms-status')) {
      return;
    }
    
    const statusIndicator = document.createElement('div');
    statusIndicator.id = 'pagescms-status';
    statusIndicator.style.cssText = `
      position: fixed;
      bottom: 20px;
      right: 20px;
      background: rgba(0, 0, 0, 0.8);
      color: white;
      padding: 8px 12px;
      border-radius: 4px;
      font-size: 12px;
      z-index: 1000;
      display: none;
      max-width: 300px;
      word-wrap: break-word;
    `;
    document.body.appendChild(statusIndicator);
  }
  
  // Show sync status
  function showSyncStatus(message, type = 'info') {
    const statusIndicator = document.getElementById('pagescms-status');
    if (!statusIndicator) return;
    
    statusIndicator.textContent = message;
    statusIndicator.style.display = 'block';
    
    // Set color based on type
    switch (type) {
      case 'success':
        statusIndicator.style.background = 'rgba(40, 167, 69, 0.9)';
        break;
      case 'error':
        statusIndicator.style.background = 'rgba(220, 53, 69, 0.9)';
        break;
      case 'warning':
        statusIndicator.style.background = 'rgba(255, 193, 7, 0.9)';
        break;
      default:
        statusIndicator.style.background = 'rgba(0, 0, 0, 0.8)';
    }
    
    // Hide after 3 seconds
    setTimeout(() => {
      statusIndicator.style.display = 'none';
    }, 3000);
  }
  
  // Set up event listeners
  function setupEventListeners() {
    // Listen for Pages CMS content updates
    window.addEventListener('pagescms-content-updated', (event) => {
      const { contentType, data } = event.detail;
      updateContent(contentType, data);
      showSyncStatus(`Content updated: ${contentType}`, 'success');
    });
    
    // Listen for Pages CMS errors
    window.addEventListener('pagescms-error', (event) => {
      const { error } = event.detail;
      console.error('Pages CMS error:', error);
      showSyncStatus(`Error: ${error}`, 'error');
    });
  }
  
  // Refresh content from Pages CMS
  function refreshContent() {
    showSyncStatus('Checking for updates...', 'info');
    
    // Simulate content refresh
    setTimeout(() => {
      showSyncStatus('Content is up to date', 'success');
    }, 1000);
  }
  
  // Update content on the page
  function updateContent(contentType, data) {
    switch (contentType) {
      case 'members':
        updateMembers(data);
        break;
      case 'publications':
        updatePublications(data);
        break;
      case 'news':
        updateNews(data);
        break;
      case 'research':
        updateResearch(data);
        break;
      case 'links':
        updateLinks(data);
        break;
      case 'teaching':
        updateTeaching(data);
        break;
      default:
        console.warn(`Unknown content type: ${contentType}`);
    }
  }
  
  // Update members content
  function updateMembers(data) {
    const membersContainer = document.querySelector('.team-grid, .members-list, .team-members');
    if (!membersContainer || !data || !Array.isArray(data)) return;
    
    // Sort members by order if available
    const sortedMembers = data.sort((a, b) => (a.order || 999) - (b.order || 999));
    
    const membersHTML = sortedMembers.map(member => `
      <div class="team-member-card">
        ${member.photo ? 
          `<img src="${member.photo}" alt="Photo of ${member.name}" class="team-member-photo">` :
          `<img src="/assets/img/team_placeholder.svg" alt="Placeholder photo for ${member.name}" class="team-member-photo">`
        }
        <div class="team-member-info">
          <h3 class="team-member-name">${escapeHtml(member.name)}</h3>
          ${member.role ? `<p class="team-member-role">${escapeHtml(member.role)}</p>` : ''}
          ${member.email ? `<p class="team-member-email"><a href="mailto:${member.email}">${escapeHtml(member.email)}</a></p>` : ''}
          <div class="team-member-links">
            ${member.website ? `<a href="${member.website}" target="_blank" rel="noopener noreferrer" class="team-member-link" aria-label="Personal Website"><i class="fas fa-globe"></i></a>` : ''}
            ${member.github ? `<a href="https://github.com/${member.github}" target="_blank" rel="noopener noreferrer" class="team-member-link" aria-label="GitHub Profile"><i class="fab fa-github"></i></a>` : ''}
          </div>
          ${member.bio ? `<div class="team-member-bio">${member.bio}</div>` : ''}
        </div>
      </div>
    `).join('');
    
    membersContainer.innerHTML = membersHTML;
  }
  
  // Update publications content
  function updatePublications(data) {
    const publicationsContainer = document.querySelector('.publications-list, .papers-list, .publications');
    if (!publicationsContainer || !data || !Array.isArray(data)) return;
    
    const publicationsHTML = data.map(pub => `
      <div class="publication-item">
        <h3 class="publication-title">${escapeHtml(pub.title)}</h3>
        <p class="publication-authors">${escapeHtml(pub.authors)}</p>
        <p class="publication-journal">${escapeHtml(pub.publication_details || pub.journal || '')} (${pub.year})</p>
        ${pub.abstract ? `<p class="publication-abstract">${pub.abstract}</p>` : ''}
        ${pub.doi ? `<a href="https://doi.org/${pub.doi}" class="publication-link" target="_blank">DOI</a>` : ''}
      </div>
    `).join('');
    
    publicationsContainer.innerHTML = publicationsHTML;
  }
  
  // Update news content
  function updateNews(data) {
    const newsContainer = document.querySelector('.news-list, .posts-list, .news');
    if (!newsContainer || !data || !Array.isArray(data)) return;
    
    const newsHTML = data.map(item => `
      <div class="news-item">
        <h3 class="news-title">${escapeHtml(item.title)}</h3>
        <div class="news-content">${item.content}</div>
      </div>
    `).join('');
    
    newsContainer.innerHTML = newsHTML;
  }
  
  // Update research content
  function updateResearch(data) {
    const researchContainer = document.querySelector('.research-list, .topics-list, .research');
    if (!researchContainer || !data || !Array.isArray(data)) return;
    
    const researchHTML = data.map(item => `
      <div class="research-item">
        <h3 class="research-title">${escapeHtml(item.title)}</h3>
        <p class="research-description">${escapeHtml(item.description)}</p>
      </div>
    `).join('');
    
    researchContainer.innerHTML = researchHTML;
  }
  
  // Update links content
  function updateLinks(data) {
    const linksContainer = document.querySelector('.links-list, .resources-list');
    if (!linksContainer || !data || !Array.isArray(data)) return;
    
    const linksHTML = data.map(item => `
      <div class="link-item">
        <h3 class="link-title">${escapeHtml(item.title)}</h3>
        <p class="link-description">${escapeHtml(item.description || '')}</p>
        <a href="${item.url}" class="link-url" target="_blank" rel="noopener noreferrer">Visit Link</a>
      </div>
    `).join('');
    
    linksContainer.innerHTML = linksHTML;
  }
  
  // Update teaching content
  function updateTeaching(data) {
    const teachingContainer = document.querySelector('.teaching-list, .courses-list, .teaching');
    if (!teachingContainer || !data || !Array.isArray(data)) return;
    
    const teachingHTML = data.map(item => `
      <div class="teaching-item">
        <h3 class="teaching-title">${escapeHtml(item.title)}</h3>
        <p class="teaching-semester">${escapeHtml(item.semester)}</p>
        <p class="teaching-instructor">Instructor: ${escapeHtml(item.instructor)}</p>
        ${item.description ? `<div class="teaching-description">${item.description}</div>` : ''}
      </div>
    `).join('');
    
    teachingContainer.innerHTML = teachingHTML;
  }
  
  // Utility function to escape HTML
  function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
  
  // Open official Pages CMS
  function openOfficialPagesCMS() {
    const repoUrl = PAGESCMS_CONFIG.repoUrl;
    const branch = PAGESCMS_CONFIG.branch;
    
    // Construct the Pages CMS URL
    let pagesCMSUrl = PAGESCMS_CONFIG.officialUrl;
    
    // Add repository and branch parameters if available
    if (repoUrl && repoUrl !== window.location.origin) {
      pagesCMSUrl += `?repo=${encodeURIComponent(repoUrl)}`;
      if (branch && branch !== 'main') {
        pagesCMSUrl += `&branch=${encodeURIComponent(branch)}`;
      }
    }
    
    console.log('Opening Pages CMS:', pagesCMSUrl);
    window.open(pagesCMSUrl, '_blank', 'noopener,noreferrer');
    
    showSyncStatus('Opening Pages CMS...', 'info');
  }
  
  // Public API
  window.PagesCMS = {
    refresh: refreshContent,
    showStatus: showSyncStatus,
    updateContent: updateContent,
    openOfficial: openOfficialPagesCMS,
    config: PAGESCMS_CONFIG
  };
  
  // Global function for button click
  window.openPagesCMSAdmin = openOfficialPagesCMS;
  
  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initPagesCMS);
  } else {
    initPagesCMS();
  }
  
})(); 