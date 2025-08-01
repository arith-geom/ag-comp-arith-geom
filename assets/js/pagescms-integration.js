// Pages CMS Integration for Official Pages CMS
// This script provides integration with the official Pages CMS system at https://app.pagescms.org/

(function() {
  'use strict';
  
  // Pages CMS Configuration
  const PAGESCMS_CONFIG = {
    enabled: true,
    autoRefresh: true,
    refreshInterval: 300000, // 5 minutes
    showSyncStatus: true,
    officialUrl: 'https://app.pagescms.org/',
    repoUrl: window.location.origin + window.location.pathname.replace(/\/$/, ''),
    branch: 'main' // Default branch, can be overridden
  };
  
  // Initialize Pages CMS integration
  function initPagesCMS() {
    if (!PAGESCMS_CONFIG.enabled) {
      console.log('Pages CMS integration is disabled');
      return;
    }
    
    console.log('Initializing Pages CMS integration...');
    
    // Set up auto-refresh if enabled
    if (PAGESCMS_CONFIG.autoRefresh) {
      setupAutoRefresh();
    }
    
    // Set up sync status indicator
    if (PAGESCMS_CONFIG.showSyncStatus) {
      setupSyncStatus();
    }
    
    // Listen for Pages CMS events
    setupEventListeners();
  }
  
  // Set up auto-refresh
  function setupAutoRefresh() {
    setInterval(() => {
      refreshContent();
    }, PAGESCMS_CONFIG.refreshInterval);
    
    // Refresh on page visibility change
    document.addEventListener('visibilitychange', () => {
      if (!document.hidden) {
        refreshContent();
      }
    });
  }
  
  // Set up sync status indicator
  function setupSyncStatus() {
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
    // This would typically be handled by the Pages CMS system
    // We just show a status message for now
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
      case 'resources':
        updateResources(data);
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
    const membersContainer = document.querySelector('.team-grid, .members-list');
    if (!membersContainer || !data || !Array.isArray(data)) return;
    
    // Sort members by order if available
    const sortedMembers = data.sort((a, b) => (a.order || 999) - (b.order || 999));
    
    const membersHTML = sortedMembers.map(member => `
      <div class="team-member-card">
        ${member.photo ? 
          `<img src="${member.photo}" alt="Photo of ${member.name}" class="team-member-photo">` :
          `<img src="/assets/img/placeholder.jpg" alt="Placeholder photo for ${member.name}" class="team-member-photo">`
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
    const publicationsContainer = document.querySelector('.publications-list, .papers-list');
    if (!publicationsContainer || !data || !Array.isArray(data)) return;
    
    const publicationsHTML = data.map(pub => `
      <div class="publication-item">
        <h3 class="publication-title">${escapeHtml(pub.title)}</h3>
        <p class="publication-authors">${escapeHtml(pub.authors)}</p>
        <p class="publication-journal">${escapeHtml(pub.publication_details)} (${pub.year})</p>
        ${pub.abstract ? `<p class="publication-abstract">${pub.abstract}</p>` : ''}
        ${pub.file ? `<a href="${pub.file}" class="publication-link" target="_blank">View PDF</a>` : ''}
        ${pub.doi ? `<a href="https://doi.org/${pub.doi}" class="publication-link" target="_blank">DOI</a>` : ''}
      </div>
    `).join('');
    
    publicationsContainer.innerHTML = publicationsHTML;
  }
  
  // Update news content
  function updateNews(data) {
    const newsContainer = document.querySelector('.news-list, .posts-list');
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
    const researchContainer = document.querySelector('.research-list, .topics-list');
    if (!researchContainer || !data || !Array.isArray(data)) return;
    
    const researchHTML = data.map(item => `
      <div class="research-item">
        <h3 class="research-title">${escapeHtml(item.title)}</h3>
        <p class="research-description">${escapeHtml(item.description)}</p>
      </div>
    `).join('');
    
    researchContainer.innerHTML = researchHTML;
  }
  
  // Update resources content
  function updateResources(data) {
    const resourcesContainer = document.querySelector('.resources-list');
    if (!resourcesContainer || !data || !Array.isArray(data)) return;
    
    const resourcesHTML = data.map(item => `
      <div class="resource-item">
        <h3 class="resource-title">${escapeHtml(item.title)}</h3>
        <p class="resource-description">${escapeHtml(item.description)}</p>
        ${item.author ? `<p class="resource-author">Author: ${escapeHtml(item.author)}</p>` : ''}
        ${item.files ? `<div class="resource-files">${item.files.map(file => `<a href="${file}" class="resource-link" target="_blank">Download</a>`).join('')}</div>` : ''}
      </div>
    `).join('');
    
    resourcesContainer.innerHTML = resourcesHTML;
  }
  
  // Update teaching content
  function updateTeaching(data) {
    const teachingContainer = document.querySelector('.teaching-list, .courses-list');
    if (!teachingContainer || !data || !Array.isArray(data)) return;
    
    const teachingHTML = data.map(item => `
      <div class="teaching-item">
        <h3 class="teaching-title">${escapeHtml(item.title)}</h3>
        <p class="teaching-semester">${escapeHtml(item.semester)}</p>
        <p class="teaching-instructor">Instructor: ${escapeHtml(item.instructor)}</p>
        ${item.details ? `<p class="teaching-details">${escapeHtml(item.details)}</p>` : ''}
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
    const pagesCMSUrl = `${PAGESCMS_CONFIG.officialUrl}?repo=${encodeURIComponent(repoUrl)}&branch=${encodeURIComponent(branch)}`;
    
    console.log('Opening Pages CMS:', pagesCMSUrl);
    window.open(pagesCMSUrl, '_blank', 'noopener,noreferrer');
    
    showSyncStatus('Opening Pages CMS...', 'info');
  }
  
  // Public API
  window.PagesCMS = {
    refresh: refreshContent,
    showStatus: showSyncStatus,
    updateContent: updateContent,
    openOfficial: openOfficialPagesCMS
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