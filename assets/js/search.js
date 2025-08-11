// Optimized Search System for AG Computational Arithmetic Geometry
// High-performance, modern search with minimal lag

(function(){
  'use strict';
  
  // Configuration - Optimized for performance
  const SEARCH_CONFIG = {
    minQueryLength: 2,
    maxResults: 10, // Reduced for better performance
    debounceDelay: 200, // Increased for better performance
    highlightClass: 'search-highlight',
    categories: {
      'member': { icon: 'ti ti-user', color: '#3B82F6', label: 'Member' },
      'teaching': { icon: 'ti ti-book', color: '#10B981', label: 'Teaching' },
      'research': { icon: 'ti ti-microscope', color: '#8B5CF6', label: 'Research' },
      'publication': { icon: 'ti ti-file-text', color: '#F59E0B', label: 'Publication' },
      'news': { icon: 'ti ti-news', color: '#EF4444', label: 'News' },
      'page': { icon: 'ti ti-file', color: '#6B7280', label: 'Page' },
      'link': { icon: 'ti ti-link', color: '#06B6D4', label: 'Link' }
    }
  };
  
  // State management - Optimized
  let searchState = {
    data: [],
    index: null,
    currentQuery: '',
    selectedIndex: -1,
    isOpen: false,
    isLoading: false,
    lastResults: [],
    searchCache: new Map() // Cache for search results
  };
  
  // DOM elements cache
  let elements = {
    desktop: {
      input: null,
      results: null,
      container: null
    },
    mobile: {
      input: null,
      results: null,
      container: null
    },
    overlay: null
  };
  
  // Performance optimization: Use requestAnimationFrame for smooth animations
  let animationFrameId = null;
  
  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initialize);
  } else {
    initialize();
  }
  
  function initialize() {
    // Get DOM elements
    elements.desktop.input = document.getElementById('search-input');
    elements.desktop.results = document.getElementById('search-results');
    elements.desktop.container = elements.desktop.input?.closest('.search-container');
    
    elements.mobile.input = document.getElementById('search-input-mobile');
    elements.mobile.results = document.getElementById('search-results-mobile');
    elements.mobile.container = elements.mobile.input?.closest('.search-container');
    
    if (!elements.desktop.input && !elements.mobile.input) {
      return;
    }
    
    // Create overlay for mobile
    createOverlay();
    
    // Load search data asynchronously
    loadSearchDataAsync();
    
    // Setup event listeners
    setupEventListeners();
    
    // Add keyboard shortcuts
    setupKeyboardShortcuts();
  }
  
  function createOverlay() {
    elements.overlay = document.createElement('div');
    elements.overlay.className = 'search-overlay';
    elements.overlay.innerHTML = `
      <div class="search-overlay-content">
        <div class="search-overlay-header">
          <h3>Search</h3>
          <button class="search-overlay-close" aria-label="Close search">
            <i class="ti ti-x"></i>
          </button>
        </div>
        <div class="search-overlay-input-container">
          <i class="ti ti-search"></i>
          <input type="text" class="search-overlay-input" placeholder="Search everything..." />
        </div>
        <div class="search-overlay-results"></div>
      </div>
    `;
    document.body.appendChild(elements.overlay);
    
    // Setup overlay event listeners
    const overlayInput = elements.overlay.querySelector('.search-overlay-input');
    const overlayResults = elements.overlay.querySelector('.search-overlay-results');
    const closeBtn = elements.overlay.querySelector('.search-overlay-close');
    
    setupSearchInput(overlayInput, overlayResults, 'overlay');
    
    closeBtn.addEventListener('click', () => {
      hideOverlay();
    });
    
    elements.overlay.addEventListener('click', (e) => {
      if (e.target === elements.overlay) {
        hideOverlay();
      }
    });
  }
  
  // Optimized async data loading
  async function loadSearchDataAsync() {
    try {
      searchState.isLoading = true;
      showLoadingState();
      
      const response = await fetch('/assets/search-data.json');
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      searchState.data = await response.json();
      
      // Build search index in background
      setTimeout(() => {
        buildSearchIndex();
        searchState.isLoading = false;
        hideLoadingState();
      }, 100);
      
    } catch (error) {
      searchState.isLoading = false;
      hideLoadingState();
      showErrorMessage('Failed to load search data. Please refresh the page.');
    }
  }
  
  // Optimized search index building
  function buildSearchIndex() {
    if (typeof lunr === 'undefined') {
      return;
    }
    
    try {
      searchState.index = lunr(function() {
        // Define searchable fields with boost values
        this.field('title', { boost: 10 });
        this.field('content', { boost: 3 });
        this.field('description', { boost: 5 });
        this.field('tags', { boost: 4 });
        this.field('category', { boost: 2 });
        this.field('authors', { boost: 3 });
        this.field('instructor', { boost: 3 });
        this.field('position', { boost: 3 });
        this.field('research_interests', { boost: 4 });
        this.field('area', { boost: 3 });
        this.field('journal', { boost: 2 });
        this.field('semester', { boost: 2 });
        this.field('course_type', { boost: 2 });
        this.field('collaborators', { boost: 2 });
        this.ref('id');
        
        // Add documents to index in chunks for better performance
        const chunkSize = 50;
        for (let i = 0; i < searchState.data.length; i += chunkSize) {
          const chunk = searchState.data.slice(i, i + chunkSize);
          chunk.forEach((item, index) => {
            this.add({
              id: i + index,
              title: item.title || '',
              content: item.content || '',
              description: item.description || '',
              tags: item.tags || '',
              category: item.category || '',
              authors: item.authors || '',
              instructor: item.instructor || '',
              position: item.position || '',
              research_interests: item.research_interests || '',
              area: item.area || '',
              journal: item.journal || '',
              semester: item.semester || '',
              course_type: item.course_type || '',
              collaborators: item.collaborators || ''
            });
          });
        }
      });
    } catch (error) {
      searchState.index = null;
    }
  }
  
  function setupEventListeners() {
    // Desktop search
    if (elements.desktop.input) {
      setupSearchInput(elements.desktop.input, elements.desktop.results, 'desktop');
    }
    
    // Mobile search
    if (elements.mobile.input) {
      setupSearchInput(elements.mobile.input, elements.mobile.results, 'mobile');
    }
  }
  
  // Optimized search input setup with better debouncing
  function setupSearchInput(input, results, type) {
    let debounceTimer;
    let lastQuery = '';
    
    // Optimized input event with better debouncing
    input.addEventListener('input', (e) => {
      const query = e.target.value.trim();
      
      // Clear previous timer
      clearTimeout(debounceTimer);
      
      // Don't search if query is too short or same as last query
      if (query.length < SEARCH_CONFIG.minQueryLength) {
        hideResults(results, type);
        return;
      }
      
      if (query === lastQuery) {
        return;
      }
      
      lastQuery = query;
      
      // Use longer debounce for better performance
      debounceTimer = setTimeout(() => {
        performSearch(query, results, type);
      }, SEARCH_CONFIG.debounceDelay);
    });
    
    // Focus events
    input.addEventListener('focus', () => {
      if (searchState.currentQuery.length >= SEARCH_CONFIG.minQueryLength) {
        showResults(results, type);
      }
      addFocusStyles(input);
    });
    
    input.addEventListener('blur', () => {
      setTimeout(() => {
        removeFocusStyles(input);
      }, 200);
    });
    
    // Keyboard navigation
    input.addEventListener('keydown', (e) => {
      handleKeyboardNavigation(e, results, type);
    });
    
    // Click outside to close
    document.addEventListener('click', (e) => {
      const isClickInsideInput = input.contains(e.target);
      const isClickInsideResults = results && results.contains(e.target);
      const isClickOnSearchButton = e.target.closest('#search-shortcut');
      
      if (!isClickInsideInput && !isClickInsideResults && !isClickOnSearchButton) {
        hideResults(results, type);
      }
    });
    
    // Prevent form submission
    input.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
      }
    });
  }
  
  function setupKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
      // Ctrl/Cmd + K to open search
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        openSearch();
      }
      
      // Escape to close search
      if (e.key === 'Escape') {
        closeSearch();
      }
    });
  }
  
  // Optimized search performance with caching
  function performSearch(query, results, type) {
    searchState.currentQuery = query;
    
    if (!query || query.length < SEARCH_CONFIG.minQueryLength) {
      hideResults(results, type);
      return;
    }
    
    // Check cache first
    const cacheKey = query.toLowerCase();
    if (searchState.searchCache.has(cacheKey)) {
      const cachedResults = searchState.searchCache.get(cacheKey);
      displayResults(cachedResults, query, results, type);
      return;
    }
    
    let searchResults;
    
    if (searchState.index) {
      try {
        searchResults = searchState.index.search(query);
      } catch (error) {
        searchResults = simpleSearch(query);
      }
    } else {
      searchResults = simpleSearch(query);
    }
    
    // Cache results
    searchState.searchCache.set(cacheKey, searchResults);
    
    // Limit cache size
    if (searchState.searchCache.size > 100) {
      const firstKey = searchState.searchCache.keys().next().value;
      searchState.searchCache.delete(firstKey);
    }
    
    searchState.lastResults = searchResults;
    displayResults(searchResults, query, results, type);
  }
  
  // Optimized simple search
  function simpleSearch(query) {
    const lowerQuery = query.toLowerCase();
    const results = [];
    
    // Use for loop instead of forEach for better performance
    for (let i = 0; i < searchState.data.length; i++) {
      const item = searchState.data[i];
      let score = 0;
      
      // Title matches (highest priority)
      if (item.title && item.title.toLowerCase().includes(lowerQuery)) {
        score += 10;
      }
      
      // Description matches
      if (item.description && item.description.toLowerCase().includes(lowerQuery)) {
        score += 5;
      }
      
      // Content matches (limit content search for performance)
      if (item.content && item.content.toLowerCase().includes(lowerQuery)) {
        score += 3;
      }
      
      // Tag matches
      if (item.tags && item.tags.toLowerCase().includes(lowerQuery)) {
        score += 4;
      }
      
      // Category matches
      if (item.category && item.category.toLowerCase().includes(lowerQuery)) {
        score += 2;
      }
      
      // Other field matches
      const otherFields = ['authors', 'instructor', 'position', 'research_interests', 'area', 'journal', 'semester'];
      for (let j = 0; j < otherFields.length; j++) {
        const field = otherFields[j];
        if (item[field] && item[field].toLowerCase().includes(lowerQuery)) {
          score += 2;
          break; // Only count first match for performance
        }
      }
      
      if (score > 0) {
        results.push({
          ref: i,
          score: score
        });
      }
    }
    
    return results.sort((a, b) => b.score - a.score);
  }
  
  // Optimized results display
  function displayResults(results, query, resultsContainer, type) {
    if (!resultsContainer) return;
    
    if (results.length === 0) {
      resultsContainer.innerHTML = `
        <div class="search-empty-state">
          <div class="search-empty-icon">
            <i class="ti ti-search-off"></i>
          </div>
          <div class="search-empty-content">
            <h4>No results found</h4>
            <p>No results found for "${escapeHtml(query)}"</p>
            <small>Try different keywords or check your spelling</small>
          </div>
        </div>
      `;
      showResults(resultsContainer, type);
      return;
    }
    
    // Use DocumentFragment for better performance
    const fragment = document.createDocumentFragment();
    
    const limitedResults = results.slice(0, SEARCH_CONFIG.maxResults);
    
    limitedResults.forEach((result, index) => {
      const item = searchState.data[result.ref];
      const category = SEARCH_CONFIG.categories[item.category] || SEARCH_CONFIG.categories.page;
      
      const resultElement = document.createElement('div');
      resultElement.className = 'search-result-item';
      resultElement.dataset.url = item.url;
      resultElement.dataset.index = index;
      
      resultElement.innerHTML = `
        <div class="search-result-icon" style="background-color: ${category.color}20; color: ${category.color}">
          <i class="${category.icon}"></i>
        </div>
        <div class="search-result-content">
          <div class="search-result-header">
            <h4 class="search-result-title">${highlightText(item.title, query)}</h4>
            <span class="search-result-category" style="color: ${category.color}">
              ${category.label}
            </span>
          </div>
          <div class="search-result-description">
            ${highlightText(item.description || truncateText(item.content, 120), query)}
          </div>
          <div class="search-result-meta">
            <span class="search-result-url">${escapeHtml(item.url)}</span>
            ${item.date ? `<span class="search-result-date">${formatDate(item.date)}</span>` : ''}
          </div>
        </div>
      `;
      
      fragment.appendChild(resultElement);
    });
    
    resultsContainer.innerHTML = '';
    resultsContainer.appendChild(fragment);
    showResults(resultsContainer, type);
    
    // Add click handlers
    addResultClickHandlers(resultsContainer, type);
  }
  
  function addResultClickHandlers(resultsContainer, type) {
    const items = resultsContainer.querySelectorAll('.search-result-item');
    
    items.forEach((item, index) => {
      item.addEventListener('click', () => {
        const url = item.dataset.url;
        if (url) {
          navigateToResult(url, type);
        }
      });
      
      item.addEventListener('mouseenter', () => {
        searchState.selectedIndex = index;
        updateSelection(resultsContainer, type);
      });
    });
  }
  
  function handleKeyboardNavigation(e, results, type) {
    const items = results.querySelectorAll('.search-result-item');
    
    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        searchState.selectedIndex = Math.min(searchState.selectedIndex + 1, items.length - 1);
        updateSelection(results, type);
        break;
        
      case 'ArrowUp':
        e.preventDefault();
        searchState.selectedIndex = Math.max(searchState.selectedIndex - 1, -1);
        updateSelection(results, type);
        break;
        
      case 'Enter':
        e.preventDefault();
        if (searchState.selectedIndex >= 0 && items[searchState.selectedIndex]) {
          const url = items[searchState.selectedIndex].dataset.url;
          if (url) {
            navigateToResult(url, type);
          }
        }
        break;
        
      case 'Escape':
        hideResults(results, type);
        break;
    }
  }
  
  function updateSelection(results, type) {
    const items = results.querySelectorAll('.search-result-item');
    
    items.forEach((item, index) => {
      if (index === searchState.selectedIndex) {
        item.classList.add('search-result-selected');
        item.scrollIntoView({ block: 'nearest' });
      } else {
        item.classList.remove('search-result-selected');
      }
    });
  }
  
  function navigateToResult(url, type) {
    closeSearch();
    
    if (url.startsWith('http')) {
      window.open(url, '_blank');
    } else {
      window.location.href = url;
    }
  }
  
  function openSearch() {
    if (window.innerWidth < 992) {
      showOverlay();
    } else {
      elements.desktop.input?.focus();
    }
  }
  
  function closeSearch() {
    hideResults(elements.desktop.results, 'desktop');
    hideResults(elements.mobile.results, 'mobile');
    hideOverlay();
    searchState.selectedIndex = -1;
  }
  
  function showOverlay() {
    elements.overlay.classList.add('search-overlay-active');
    const input = elements.overlay.querySelector('.search-overlay-input');
    input.focus();
    document.body.style.overflow = 'hidden';
  }
  
  function hideOverlay() {
    elements.overlay.classList.remove('search-overlay-active');
    document.body.style.overflow = '';
  }
  
  // Optimized show/hide results with requestAnimationFrame
  function showResults(results, type) {
    if (!results) return;
    
    if (animationFrameId) {
      cancelAnimationFrame(animationFrameId);
    }
    
    animationFrameId = requestAnimationFrame(() => {
      results.style.display = 'block';
      searchState.isOpen = true;
      
      if (type === 'mobile') {
        results.closest('.search-container')?.classList.add('search-active');
      }
      
      // Add show class after display is set
      setTimeout(() => {
        results.classList.add('show');
      }, 10);
    });
  }
  
  function hideResults(results, type) {
    if (!results) return;
    
    if (animationFrameId) {
      cancelAnimationFrame(animationFrameId);
    }
    
    animationFrameId = requestAnimationFrame(() => {
      results.classList.remove('show');
      searchState.isOpen = false;
      
      if (type === 'mobile') {
        results.closest('.search-container')?.classList.remove('search-active');
      }
      
      // Hide after animation
      setTimeout(() => {
        results.style.display = 'none';
      }, 300);
    });
  }
  
  function showLoadingState() {
    [elements.desktop.input, elements.mobile.input].forEach(input => {
      if (input) {
        input.classList.add('search-loading');
      }
    });
  }
  
  function hideLoadingState() {
    [elements.desktop.input, elements.mobile.input].forEach(input => {
      if (input) {
        input.classList.remove('search-loading');
      }
    });
  }
  
  function showErrorMessage(message) {
    [elements.desktop.results, elements.mobile.results].forEach(results => {
      if (results) {
        results.innerHTML = `
          <div class="search-error-state">
            <i class="ti ti-alert-circle"></i>
            <p>${escapeHtml(message)}</p>
          </div>
        `;
        showResults(results, 'desktop');
      }
    });
  }
  
  function addFocusStyles(input) {
    input?.closest('.search-container')?.classList.add('search-focused');
  }
  
  function removeFocusStyles(input) {
    input?.closest('.search-container')?.classList.remove('search-focused');
  }
  
  // Optimized utility functions
  function highlightText(text, query) {
    if (!text || !query) return escapeHtml(text);
    
    const regex = new RegExp(`(${escapeRegex(query)})`, 'gi');
    return escapeHtml(text).replace(regex, `<mark class="${SEARCH_CONFIG.highlightClass}">$1</mark>`);
  }
  
  function truncateText(text, maxLength) {
    if (!text || text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
  }
  
  function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString();
  }
  
  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
  
  function escapeRegex(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }
  
  // Expose public API
  window.SearchSystem = {
    open: openSearch,
    close: closeSearch,
    search: (query) => {
      if (elements.desktop.input) {
        elements.desktop.input.value = query;
        performSearch(query, elements.desktop.results, 'desktop');
      }
    }
  };
  
})(); 