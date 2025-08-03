---
layout: page
title: Publications
permalink: /publications/
nav: true
nav_order: 5
---

<div class="publications-page">
  <!-- Filter Controls -->
  <div class="filter-section">
    <div class="container">
      <!-- Publications Search Bar -->
      <div class="search-container">
        <div class="search-wrapper">
          <input type="text" id="publications-search-input" class="search-input" placeholder="Search titles, authors, keywords...">
          <i class="fas fa-search search-icon"></i>
          <button type="button" id="publications-clear-search" class="clear-search-btn" style="display: none;">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div id="publications-search-results-info" class="search-results-info" style="display: none;">
          <span id="publications-search-results-count"></span> publications found
        </div>
        <div class="search-test-buttons" style="margin-top: 0.5rem;">
          <button type="button" class="btn btn-sm btn-outline-secondary" onclick="testPublicationsSearch('Böckle')">Test: Böckle</button>
          <button type="button" class="btn btn-sm btn-outline-secondary" onclick="testPublicationsSearch('modular')">Test: modular</button>
          <button type="button" class="btn btn-sm btn-outline-secondary" onclick="testPublicationsSearch('2023')">Test: 2023</button>
          <button type="button" class="btn btn-sm btn-outline-secondary" onclick="testPublicationsSearch('2020')">Test: 2020</button>
          <button type="button" class="btn btn-sm btn-outline-secondary" onclick="clearPublicationsSearch()">Clear</button>
        </div>
      </div>

      <!-- Quick Filter Buttons -->
      <div class="quick-filters">
        <button class="quick-filter-btn active" data-filter="all">All Publications</button>
        <button class="quick-filter-btn" data-filter="journal">Journal Articles</button>
        <button class="quick-filter-btn" data-filter="preprint">Preprints</button>
        <button class="quick-filter-btn" data-filter="software">Software</button>
        <button class="quick-filter-btn" data-filter="book">Books</button>
        <button class="quick-filter-btn" data-filter="thesis">Theses</button>
      </div>
    </div>
  </div>

  <!-- Publications Grid -->
  <div class="publications-content">
    <div class="container">
      <!-- Loading State -->
      <div id="loading-state" class="loading-state" style="display: none;">
        <div class="spinner"></div>
        <p>Loading publications...</p>
      </div>

      <!-- Empty State -->
      <div id="empty-state" class="empty-state" style="display: none;">
        <i class="fas fa-search"></i>
        <h3>No publications found</h3>
        <p>Try adjusting your filters or search terms.</p>
      </div>

      <!-- Publications Grid -->
      <div id="publications-grid" class="publications-grid" style="display: grid;">
        <!-- Publications will be dynamically loaded here -->
      </div>

      <!-- Load More Button -->
      <div id="load-more-container" class="load-more-container" style="display: none;">
        <button id="load-more-btn" class="btn btn-outline-primary">
          <i class="fas fa-plus"></i> Load More Publications
        </button>
      </div>
    </div>
  </div>
</div>

<!-- Publication Card Template -->
<template id="publication-card-template">
  <div class="publication-card">
    <div class="publication-header">
      <div class="publication-meta">
        <span class="publication-type"></span>
        <span class="publication-status"></span>
        <span class="publication-year"></span>
      </div>
      <h3 class="publication-title">
        <a href="javascript:void(0)" class="publication-link"></a>
      </h3>
      <div class="publication-authors"></div>
      <div class="publication-venue"></div>
    </div>
    
    <div class="publication-body">
      <div class="publication-abstract"></div>
      <div class="publication-keywords"></div>
    </div>
    
    <div class="publication-footer">
      <div class="publication-links">
        <!-- Links will be dynamically added -->
      </div>
      <div class="publication-metrics">
        <!-- Metrics will be dynamically added -->
      </div>
    </div>
  </div>
</template>

<style>
.publications-page {
  background: white;
  min-height: 100vh;
  padding-top: 1rem;
}

.filter-section {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-bottom: 3px solid #c22032;
  padding: 1rem 0;
  margin-bottom: 0.5rem;
  border-radius: 0 0 12px 12px;
}

.publications-content {
  margin-top: 0;
  padding-top: 0;
}

.search-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 1rem;
  padding: 0 1rem;
}

.search-results-info {
  margin-top: 0.5rem;
  padding: 0.5rem 1.5rem;
  background: #e8f4fd;
  color: #0c5460;
  border-radius: 2rem;
  font-size: 0.9rem;
  font-weight: 500;
  border: 1px solid #bee5eb;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

.search-wrapper {
  position: relative;
  max-width: 600px;
  width: 100%;
}

.search-input {
  width: 100%;
  padding: 1.25rem 4rem 1.25rem 2rem;
  border: 3px solid #e9ecef;
  border-radius: 3rem;
  background: white;
  color: #495057;
  font-size: 1.1rem;
  font-weight: 500;
  transition: all 0.3s ease;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  letter-spacing: 0.5px;
}

.search-input::placeholder {
  color: #adb5bd;
  font-weight: 400;
}

.search-input:focus {
  outline: none;
  border-color: #c22032;
  box-shadow: 0 0 0 4px rgba(194, 32, 50, 0.15), 0 8px 25px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.search-input:hover {
  border-color: #c22032;
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.12);
}

.search-icon {
  position: absolute;
  right: 2rem;
  top: 50%;
  transform: translateY(-50%);
  color: #c22032;
  font-size: 1.3rem;
  pointer-events: none;
  transition: all 0.3s ease;
}

.search-input:focus + .search-icon {
  color: #a01828;
  transform: translateY(-50%) scale(1.1);
}

.clear-search-btn {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  background: #c22032;
  color: white;
  border: none;
  border-radius: 50%;
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
  z-index: 10;
}

.clear-search-btn:hover {
  background: #a01828;
  transform: translateY(-50%) scale(1.1);
}

.clear-search-btn:active {
  transform: translateY(-50%) scale(0.95);
}

@media (max-width: 768px) {
  .search-input {
    padding: 1rem 3.5rem 1rem 1.5rem;
    font-size: 1rem;
  }
  
  .search-icon {
    right: 1.5rem;
    font-size: 1.2rem;
  }
  
  .clear-search-btn {
    width: 1.8rem;
    height: 1.8rem;
    font-size: 0.8rem;
  }
}

.quick-filters {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  justify-content: center;
  margin-top: 0.5rem;
}

.quick-filter-btn {
  padding: 0.5rem 1.5rem;
  border: 2px solid #c22032;
  border-radius: 2rem;
  background: #c22032;
  color: white;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(194, 32, 50, 0.2);
}

.quick-filter-btn:hover,
.quick-filter-btn.active {
  background: #a01828;
  color: white;
  border-color: #a01828;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(194, 32, 50, 0.3);
}

.quick-filter-btn:not(.active) {
  background: white;
  color: #c22032;
  border-color: #c22032;
}

.quick-filter-btn:not(.active):hover {
  background: #f8f9fa;
  color: #a01828;
  border-color: #a01828;
}

.loading-state {
  text-align: center;
  padding: 3rem;
  color: #6c757d;
}

.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #c22032;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: #6c757d;
}

.empty-state i {
  font-size: 3rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.empty-state h3 {
  color: #212529;
  margin-bottom: 0.5rem;
}

.publications-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

@media (max-width: 768px) {
  .publications-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
}

.publication-card {
  background: white;
  border-radius: 0.375rem;
  border: 1px solid #dee2e6;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
  transition: all 0.2s ease;
  overflow: hidden;
  height: fit-content;
}

.publication-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
  border-color: #c22032;
}

.publication-header {
  padding: 1.25rem;
  border-bottom: 1px solid #dee2e6;
}

.publication-meta {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.publication-type,
.publication-status,
.publication-year {
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.8rem;
  font-weight: 600;
}

.publication-type {
  background: linear-gradient(135deg, #c22032 0%, #a01828 100%);
  color: white;
}

.publication-status {
  background: #f8f9fa;
  color: #6c757d;
  border: 1px solid #dee2e6;
}

.publication-year {
  background: #f8f9fa;
  color: #6c757d;
  border: 1px solid #dee2e6;
}

.publication-title {
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
  line-height: 1.3;
}

.publication-title a {
  color: #212529;
  text-decoration: none;
  transition: color 0.2s ease;
  cursor: pointer;
}

.publication-title a:hover {
  color: #c22032;
  text-decoration: underline;
}

.publication-title a[href="javascript:void(0)"] {
  cursor: default;
  color: #212529;
}

.publication-title a[href="javascript:void(0)"]:hover {
  color: #212529;
  text-decoration: none;
}

.publication-authors {
  color: #6c757d;
  font-style: italic;
  margin-bottom: 0.5rem;
  font-size: 0.95rem;
}

.publication-venue {
  color: #adb5bd;
  font-size: 0.9rem;
}

.publication-body {
  padding: 1.25rem;
}

.publication-abstract {
  color: #495057;
  line-height: 1.6;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}

.publication-keywords {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.keyword-tag {
  background: #e9ecef;
  color: #495057;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.8rem;
}

.publication-footer {
  padding: 1.25rem;
  border-top: 1px solid #dee2e6;
  background: #f8f9fa;
}

.publication-links {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin-bottom: 1rem;
}

.publication-link-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  background: #c22032;
  color: white !important;
  text-decoration: none;
  border-radius: 0.5rem;
  font-size: 0.9rem;
  font-weight: 600;
  transition: all 0.2s ease;
  border: 2px solid #c22032;
  box-shadow: 0 2px 4px rgba(194, 32, 50, 0.3);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.publication-link-btn:hover {
  background: #a01828;
  color: white !important;
  border-color: #a01828;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(194, 32, 50, 0.4);
  text-decoration: none;
}

.publication-link-btn:active {
  transform: translateY(0);
  box-shadow: 0 2px 4px rgba(194, 32, 50, 0.3);
}

.publication-link-btn i {
  font-size: 1rem;
  color: white !important;
}

.publication-metrics {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.metric-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #6c757d;
  font-size: 0.85rem;
}

.load-more-container {
  text-align: center;
  margin-top: 2rem;
}

.btn-outline-primary {
  border-color: #c22032;
  color: #c22032;
}

.btn-outline-primary:hover {
  background: #c22032;
  border-color: #c22032;
  color: white;
}
</style>

<script>
class PublicationsManager {
  constructor() {
    this.publications = [];
    this.filteredPublications = [];
    this.currentPage = 1;
    this.itemsPerPage = 12;
    this.filters = {
      type: '',
      status: '',
      year: '',
      search: ''
    };
    
    this.init();
  }
  
  async init() {
    console.log('Initializing PublicationsManager...');
    this.bindEvents();
    await this.loadPublications();
    this.filteredPublications = this.publications;
    this.renderPublications();
    console.log('PublicationsManager initialized successfully');
  }
  
  bindEvents() {
    // Publications search input with debouncing
    let searchTimeout;
    const searchInput = document.getElementById('publications-search-input');
    const clearSearchBtn = document.getElementById('publications-clear-search');
    
    if (searchInput) {
      console.log('✅ Publications search input found and bound');
      searchInput.addEventListener('input', (e) => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
          this.filters.search = e.target.value.toLowerCase().trim();
          console.log('🔍 Publications search term:', this.filters.search);
          
          // Show/hide clear button
          if (clearSearchBtn) {
            if (this.filters.search.length > 0) {
              clearSearchBtn.style.display = 'flex';
            } else {
              clearSearchBtn.style.display = 'none';
            }
          }
          
          this.applyFilters();
        }, 300);
      });
      
      // Also listen for Enter key
      searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
          this.filters.search = e.target.value.toLowerCase().trim();
          console.log('🔍 Publications search term (Enter):', this.filters.search);
          this.applyFilters();
        }
      });
    } else {
      console.error('❌ Publications search input not found');
    }
    
    // Clear search button
    if (clearSearchBtn) {
      clearSearchBtn.addEventListener('click', () => {
        if (searchInput) {
          searchInput.value = '';
          this.filters.search = '';
          clearSearchBtn.style.display = 'none';
          this.applyFilters();
          searchInput.focus();
        }
      });
    }
    
    // Quick filter buttons
    const quickFilterButtons = document.querySelectorAll('.quick-filter-btn');
    
    quickFilterButtons.forEach((btn, index) => {
      btn.addEventListener('click', (e) => {
        // Remove active class from all buttons
        document.querySelectorAll('.quick-filter-btn').forEach(b => b.classList.remove('active'));
        
        // Add active class to clicked button
        e.target.classList.add('active');
        
        const filter = e.target.dataset.filter;
        this.applyQuickFilter(filter);
      });
    });
    
    // Load more button
    const loadMoreBtn = document.getElementById('load-more-btn');
    if (loadMoreBtn) {
      loadMoreBtn.addEventListener('click', () => {
        this.loadMore();
      });
    }
  }
  
  async loadPublications() {
    try {
      // Show loading state
      document.getElementById('loading-state').style.display = 'block';
      document.getElementById('publications-grid').style.display = 'none';
      document.getElementById('empty-state').style.display = 'none';
      
      // Load real publications data
      this.publications = await this.getPublicationsData();
      console.log('Loaded publications:', this.publications.length, this.publications);
      
      // Hide loading state
      document.getElementById('loading-state').style.display = 'none';
      
    } catch (error) {
      console.error('Error loading publications:', error);
      document.getElementById('loading-state').style.display = 'none';
      document.getElementById('empty-state').style.display = 'block';
    }
  }
  
  async getPublicationsData() {
    try {
      const response = await fetch('/assets/json/publications-data.json');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      console.log('Loaded publications data:', data.length, 'publications');
      return data;
    } catch (error) {
      console.error('Error loading publications data:', error);
      // Fallback to sample data if loading fails
      return this.getSamplePublications();
    }
  }
  
  getSamplePublications() {
    return [
      {
        id: 1,
        title: "Irreducibility of versal deformation rings in the (p,p)-case for 2-dimensional representations",
        authors: "Gebhard Böckle, A.-K. Juschka",
        year: 2015,
        journal: "J. Algebra",
        volume: "444",
        pages: "81–123",
        abstract: "This paper studies the irreducibility of versal deformation rings in the (p,p)-case for 2-dimensional representations.",
        keywords: "deformation theory, Galois representations, irreducibility",
        type: "Journal Article",
        status: "Published",
        featured: true,
        url: "http://www.sciencedirect.com/science/article/pii/S002186931500352X"
      }
    ];
  }
  
  applyFilters() {
    console.log('Applying filters:', this.filters);
    
    this.filteredPublications = this.publications.filter(pub => {
      // Type filter
      if (this.filters.type && pub.type !== this.filters.type) return false;
      
      // Status filter
      if (this.filters.status && pub.status !== this.filters.status) return false;
      
      // Year filter
      if (this.filters.year && pub.year.toString() !== this.filters.year) return false;
      
      // Search filter
      if (this.filters.search && this.filters.search.length > 0) {
        const searchTerm = this.filters.search;
        const searchableText = [
          pub.title || '',
          pub.authors || '',
          pub.journal || '',
          pub.abstract || '',
          pub.keywords || '',
          pub.year ? pub.year.toString() : '',
          pub.volume || '',
          pub.pages || '',
          pub.doi || '',
          pub.arxiv || ''
        ].join(' ').toLowerCase();
        
        console.log('🔍 Searching in:', searchableText);
        console.log('🔍 Looking for:', searchTerm);
        console.log('🔍 Publication:', pub.title, 'Year:', pub.year);
        
        if (!searchableText.includes(searchTerm)) {
          console.log('❌ No match found for:', pub.title);
          return false;
        } else {
          console.log('✅ Match found for:', pub.title);
        }
      }
      
      return true;
    });
    
    console.log('Filtered publications count:', this.filteredPublications.length);
    this.currentPage = 1;
    this.renderPublications();
  }
  
  applyQuickFilter(filter) {
    // Reset all filters
    this.filters = { type: '', status: '', year: '', search: '' };
    
    // Apply quick filter
    switch (filter) {
      case 'journal':
        this.filters.type = 'Journal Article';
        break;
      case 'preprint':
        this.filters.type = 'Preprint';
        break;
      case 'software':
        this.filters.type = 'Software Package';
        break;
      case 'book':
        this.filters.type = 'Book';
        break;
      case 'thesis':
        this.filters.type = 'Thesis';
        break;
      case 'all':
        this.filteredPublications = this.publications;
        this.renderPublications();
        return;
      default:
        this.filteredPublications = this.publications;
        this.renderPublications();
        return;
    }
    
    this.applyFilters();
  }
  
  renderPublications() {
    console.log('Rendering publications...', this.filteredPublications.length);
    const grid = document.getElementById('publications-grid');
    const emptyState = document.getElementById('empty-state');
    const loadMoreContainer = document.getElementById('load-more-container');
    const searchResultsInfo = document.getElementById('publications-search-results-info');
    const searchResultsCount = document.getElementById('publications-search-results-count');
    
    console.log('DOM elements found:', { grid: !!grid, emptyState: !!emptyState, loadMoreContainer: !!loadMoreContainer });
    
    // Update search results info
    if (searchResultsInfo && searchResultsCount) {
      if (this.filters.search && this.filters.search.length > 0) {
        searchResultsCount.textContent = this.filteredPublications.length;
        searchResultsInfo.style.display = 'block';
        console.log('📊 Publications search results:', this.filteredPublications.length);
      } else {
        searchResultsInfo.style.display = 'none';
      }
    }
    
    if (this.filteredPublications.length === 0) {
      console.log('No publications to display, showing empty state');
      if (grid) grid.style.display = 'none';
      if (emptyState) emptyState.style.display = 'block';
      if (loadMoreContainer) loadMoreContainer.style.display = 'none';
      return;
    }
    
    if (grid) grid.style.display = 'grid';
    if (emptyState) emptyState.style.display = 'none';
    
    // Calculate pagination
    const startIndex = 0;
    const endIndex = this.currentPage * this.itemsPerPage;
    const publicationsToShow = this.filteredPublications.slice(startIndex, endIndex);
    
    // Clear existing content
    grid.innerHTML = '';
    
    // Render publications
    publicationsToShow.forEach(pub => {
      const card = this.createPublicationCard(pub);
      grid.appendChild(card);
    });
    
    // Show/hide load more button
    if (loadMoreContainer) {
      if (endIndex < this.filteredPublications.length) {
        loadMoreContainer.style.display = 'block';
      } else {
        loadMoreContainer.style.display = 'none';
      }
    }
  }
  
  createPublicationCard(pub) {
    console.log('Creating card for publication:', pub.title);
    const template = document.getElementById('publication-card-template');
    if (!template) {
      console.error('Publication card template not found!');
      return document.createElement('div');
    }
    const card = template.content.cloneNode(true);
    
    // Set basic information
    const typeEl = card.querySelector('.publication-type');
    const statusEl = card.querySelector('.publication-status');
    const yearEl = card.querySelector('.publication-year');
    
    if (typeEl) typeEl.textContent = pub.type;
    if (statusEl) statusEl.textContent = pub.status;
    if (yearEl) yearEl.textContent = pub.year;
    const titleEl = card.querySelector('.publication-title a');
    if (titleEl) titleEl.textContent = pub.title;
    
    // Set the link to the actual URL if available, otherwise make it non-clickable
    const titleLink = card.querySelector('.publication-title a');
    if (titleLink) {
      if (pub.url) {
        titleLink.href = pub.url;
        titleLink.target = '_blank';
        titleLink.style.cursor = 'pointer';
        titleLink.style.color = '#c22032';
      } else if (pub.pdf) {
        titleLink.href = pub.pdf;
        titleLink.target = '_blank';
        titleLink.style.cursor = 'pointer';
        titleLink.style.color = '#c22032';
      } else if (pub.software_info && pub.software_info.repository_url) {
        // For software packages, use the repository URL
        titleLink.href = pub.software_info.repository_url;
        titleLink.target = '_blank';
        titleLink.style.cursor = 'pointer';
        titleLink.style.color = '#c22032';
      } else {
        // Make it clear this is not clickable
        titleLink.href = 'javascript:void(0)';
        titleLink.style.cursor = 'default';
        titleLink.style.color = '#212529';
        titleLink.style.textDecoration = 'none';
        titleLink.title = 'No link available';
      }
    }
    
    card.querySelector('.publication-authors').textContent = pub.authors;
    card.querySelector('.publication-venue').textContent = pub.journal;
    card.querySelector('.publication-abstract').textContent = pub.abstract;
    
    // Add keywords
    if (pub.keywords) {
      const keywordsContainer = card.querySelector('.publication-keywords');
      const keywords = pub.keywords.split(',').map(k => k.trim());
      keywords.forEach(keyword => {
        const tag = document.createElement('span');
        tag.className = 'keyword-tag';
        tag.textContent = keyword;
        keywordsContainer.appendChild(tag);
      });
    }
    
    // Add links
    const linksContainer = card.querySelector('.publication-links');
    if (pub.doi) {
      const doiLink = document.createElement('a');
      doiLink.href = `https://doi.org/${pub.doi}`;
      doiLink.className = 'publication-link-btn';
      doiLink.innerHTML = '<i class="fas fa-external-link-alt"></i> DOI';
      doiLink.target = '_blank';
      linksContainer.appendChild(doiLink);
    }
    
    if (pub.arxiv) {
      const arxivLink = document.createElement('a');
      arxivLink.href = `https://arxiv.org/abs/${pub.arxiv}`;
      arxivLink.className = 'publication-link-btn';
      arxivLink.innerHTML = '<i class="fas fa-file-alt"></i> arXiv';
      arxivLink.target = '_blank';
      linksContainer.appendChild(arxivLink);
    }
    
    if (pub.url) {
      const urlLink = document.createElement('a');
      urlLink.href = pub.url;
      urlLink.className = 'publication-link-btn';
      urlLink.innerHTML = '<i class="fas fa-external-link-alt"></i> View';
      urlLink.target = '_blank';
      linksContainer.appendChild(urlLink);
    }
    
    if (pub.pdf) {
      const pdfLink = document.createElement('a');
      pdfLink.href = pub.pdf;
      pdfLink.className = 'publication-link-btn';
      pdfLink.innerHTML = '<i class="fas fa-file-pdf"></i> PDF';
      pdfLink.target = '_blank';
      linksContainer.appendChild(pdfLink);
    }
    
    if (pub.software_info && pub.software_info.repository_url && pub.software_info.repository_url !== 'https://github.com/rbutenuth/qaquotgraphs') {
      const repoLink = document.createElement('a');
      repoLink.href = pub.software_info.repository_url;
      repoLink.className = 'publication-link-btn';
      repoLink.innerHTML = '<i class="fab fa-github"></i> Repository';
      repoLink.target = '_blank';
      linksContainer.appendChild(repoLink);
    }
    
    return card;
  }
  
  loadMore() {
    this.currentPage++;
    this.renderPublications();
  }
}

// Initialize the publications manager when the page loads
document.addEventListener('DOMContentLoaded', () => {
  console.log('🚀 Initializing Publications Manager...');
  const manager = new PublicationsManager();
  
  // Make manager globally accessible for debugging
  window.publicationsManager = manager;
  
  // Link validation and error detection script
  setTimeout(() => {
    validatePublicationLinks();
  }, 2000); // Wait for publications to load
  
  // Test publications search functionality
  setTimeout(() => {
    console.log('🧪 Testing publications search functionality...');
    const searchInput = document.getElementById('publications-search-input');
    if (searchInput) {
      console.log('✅ Publications search input found');
      // Test with a sample search
      searchInput.value = 'Böckle';
      searchInput.dispatchEvent(new Event('input'));
    } else {
      console.error('❌ Publications search input not found');
    }
  }, 3000);
});

// Publications search test functions
function testPublicationsSearch(term) {
  console.log('🧪 Testing publications search with term:', term);
  const searchInput = document.getElementById('publications-search-input');
  if (searchInput && window.publicationsManager) {
    searchInput.value = term;
    searchInput.dispatchEvent(new Event('input'));
    console.log('✅ Publications search test executed');
  } else {
    console.error('❌ Publications search test failed - elements not found');
  }
}

function clearPublicationsSearch() {
  console.log('🧪 Clearing publications search test');
  const searchInput = document.getElementById('publications-search-input');
  if (searchInput && window.publicationsManager) {
    searchInput.value = '';
    searchInput.dispatchEvent(new Event('input'));
    console.log('✅ Publications search cleared');
  }
}

// Link validation and error detection function
async function validatePublicationLinks() {
  console.log('🔍 Starting publication link validation...');
  
  const links = document.querySelectorAll('a[href]');
  const brokenLinks = [];
  const workingLinks = [];
  
  for (let link of links) {
    const href = link.href;
    
    // Skip internal links and anchors
    if (href.startsWith(window.location.origin) || href.startsWith('#') || href.startsWith('mailto:')) {
      continue;
    }
    
    try {
      // Check if link is accessible
      const response = await fetch(href, { 
        method: 'HEAD', 
        mode: 'no-cors',
        cache: 'no-cache'
      });
      
      // If we can't check due to CORS, assume it's working
      workingLinks.push({
        url: href,
        element: link,
        text: link.textContent.trim()
      });
      
    } catch (error) {
      // Try alternative validation for known domains
      if (isLikelyWorking(href)) {
        workingLinks.push({
          url: href,
          element: link,
          text: link.textContent.trim()
        });
      } else {
        brokenLinks.push({
          url: href,
          element: link,
          text: link.textContent.trim(),
          error: error.message
        });
        
        // Add visual indicator for broken links
        link.style.opacity = '0.6';
        link.style.textDecoration = 'line-through';
        link.title = 'Link may be broken - ' + error.message;
      }
    }
  }
  
  // Log results
  console.log(`✅ Working links: ${workingLinks.length}`);
  console.log(`❌ Broken links: ${brokenLinks.length}`);
  
  if (brokenLinks.length > 0) {
    console.warn('🚨 Broken links detected:', brokenLinks);
    
    // Create a summary in the console
    console.group('📋 Link Validation Summary');
    console.log('Working links:', workingLinks.map(l => l.url));
    console.log('Broken links:', brokenLinks.map(l => l.url));
    console.groupEnd();
  }
  
  // Check for clickable content issues
  checkClickableContent();
}

// Helper function to check if a link is likely working based on domain
function isLikelyWorking(url) {
  const knownWorkingDomains = [
    'doi.org',
    'arxiv.org',
    'springer.com',
    'link.springer.com',
    'ams.org',
    'mathscinet.ams.org',
    'jtnb.cedram.org',
    'github.com',
    'dx.doi.org'
  ];
  
  return knownWorkingDomains.some(domain => url.includes(domain));
}

// Check for clickable content issues
function checkClickableContent() {
  console.log('🔍 Checking clickable content...');
  
  const issues = [];
  
  // Check publication titles
  const titles = document.querySelectorAll('.publication-title a');
  titles.forEach((title, index) => {
    if (!title.href || title.href === '#' || title.href === window.location.href) {
      issues.push({
        type: 'Non-clickable title',
        element: title,
        text: title.textContent.trim(),
        index: index
      });
    }
  });
  
  // Check publication link buttons
  const linkButtons = document.querySelectorAll('.publication-link-btn');
  linkButtons.forEach((btn, index) => {
    if (!btn.href || btn.href === '#' || btn.href === window.location.href) {
      issues.push({
        type: 'Non-clickable button',
        element: btn,
        text: btn.textContent.trim(),
        index: index
      });
    }
  });
  
  // Check filter buttons
  const filterButtons = document.querySelectorAll('.quick-filter-btn');
  filterButtons.forEach((btn, index) => {
    if (!btn.onclick && !btn.dataset.filter) {
      issues.push({
        type: 'Non-functional filter button',
        element: btn,
        text: btn.textContent.trim(),
        index: index
      });
    }
  });
  
  if (issues.length > 0) {
    console.warn('⚠️ Clickable content issues detected:', issues);
    
    // Add visual indicators for issues
    issues.forEach(issue => {
      if (issue.element) {
        issue.element.style.border = '2px solid #ffc107';
        issue.element.style.backgroundColor = '#fff3cd';
        issue.element.title = `Issue: ${issue.type}`;
      }
    });
  } else {
    console.log('✅ All clickable content appears to be working correctly');
  }
  
  // Check for missing content
  checkMissingContent();
}

// Check for missing content
function checkMissingContent() {
  console.log('🔍 Checking for missing content...');
  
  const issues = [];
  
  // Check for empty abstracts
  const abstracts = document.querySelectorAll('.publication-abstract');
  abstracts.forEach((abstract, index) => {
    if (!abstract.textContent.trim()) {
      issues.push({
        type: 'Empty abstract',
        element: abstract,
        index: index
      });
    }
  });
  
  // Check for missing authors
  const authors = document.querySelectorAll('.publication-authors');
  authors.forEach((author, index) => {
    if (!author.textContent.trim()) {
      issues.push({
        type: 'Missing authors',
        element: author,
        index: index
      });
    }
  });
  
  // Check for missing links
  const cards = document.querySelectorAll('.publication-card');
  cards.forEach((card, index) => {
    const links = card.querySelectorAll('.publication-link-btn');
    if (links.length === 0) {
      issues.push({
        type: 'No links available',
        element: card,
        index: index
      });
    }
  });
  
  if (issues.length > 0) {
    console.warn('⚠️ Missing content issues detected:', issues);
  } else {
    console.log('✅ All content appears to be complete');
  }
  
  // Final summary
  console.log('🎯 Publication page validation complete!');
}
</script>

 