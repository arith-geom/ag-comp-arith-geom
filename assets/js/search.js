// Enhanced Search Functionality with Modern UX
// Improved search implementation with better animations and user feedback

(function(){
  'use strict';
  
  // DOM elements - support both desktop and mobile
  var searchInput = document.getElementById('search-input');
  var searchInputMobile = document.getElementById('search-input-mobile');
  var searchResults = document.getElementById('search-results');
  var searchResultsMobile = document.getElementById('search-results-mobile');
  var searchData = [];
  var searchIndex = null;
  var currentQuery = '';
  var searchTimeout = null;
  var isInitialized = false;
  var isLoading = false;
  
  // Initialize search when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeSearch);
  } else {
    initializeSearch();
  }
  
  function initializeSearch() {
    if (!searchInput && !searchInputMobile) {
      console.warn('No search inputs found');
      return;
    }
    
    console.log('Initializing enhanced search functionality...');
    
    // Load search data and build index
    loadSearchData();
    
    // Add event listeners for both desktop and mobile
    setupEventListeners();
    
    // Add search toggle functionality
    addSearchToggle();
    
    // Add loading states
    addLoadingStates();
    
    isInitialized = true;
    console.log('Enhanced search functionality initialized');
  }
  
  function loadSearchData() {
    console.log('Loading search data...');
    showLoadingState();
    
    // Try multiple paths to load search data
    const searchPaths = [
      '/assets/json/search.json',
      './assets/json/search.json',
      '../assets/json/search.json',
      '../../assets/json/search.json'
    ];
    
    function tryLoadSearchData(index) {
      if (index >= searchPaths.length) {
        console.warn('All search data loading attempts failed, using fallback');
        hideLoadingState();
        extractPageContent();
        return;
      }
      
      const path = searchPaths[index];
      console.log('Trying to load search data from:', path);
      
      fetch(path)
        .then(function(response) {
          if (!response.ok) {
            throw new Error('Failed to load search data from ' + path + ': ' + response.status);
          }
          return response.json();
        })
        .then(function(data) {
          console.log('Search data loaded successfully from', path + ':', data.length, 'items');
          searchData = data;
          buildSearchIndex();
          hideLoadingState();
        })
        .catch(function(error) {
          console.warn('Failed to load from', path + ':', error);
          // Try next path
          tryLoadSearchData(index + 1);
        });
    }
    
    // Start with the first path
    tryLoadSearchData(0);
  }
  
  function buildSearchIndex() {
    if (typeof lunr === 'undefined') {
      console.warn('Lunr.js not loaded, using simple search');
      return;
    }
    
    try {
      searchIndex = lunr(function() {
        this.field('title', { boost: 10 });
        this.field('content', { boost: 5 });
        this.field('tags', { boost: 3 });
        this.field('category', { boost: 2 });
        this.field('description', { boost: 4 });
        this.ref('id');
        
        searchData.forEach(function(item, index) {
          this.add({
            id: index,
            title: item.title || '',
            content: item.content || '',
            tags: item.tags || '',
            category: item.category || '',
            description: item.description || '',
            url: item.url || ''
          });
        }, this);
      });
      console.log('Search index built successfully with', searchData.length, 'items');
    } catch (error) {
      console.error('Error building search index:', error);
      searchIndex = null;
    }
  }
  
  function extractPageContent() {
    console.log('Extracting content from current page as fallback...');
    // Fallback: extract content from current page
    const pages = [];
    const currentUrl = window.location.pathname;
    
    // Extract headings and content
    document.querySelectorAll('h1, h2, h3, h4, h5, h6, p, article, section').forEach(function(element) {
      const text = element.textContent.trim();
      if (text.length > 10) {
        pages.push({
          title: element.tagName.startsWith('H') ? text : '',
          content: text,
          url: currentUrl + '#' + (element.id || ''),
          category: 'page'
        });
      }
    });
    
    searchData = pages;
    buildSearchIndex();
  }
  
  function setupEventListeners() {
    // Setup event listeners for desktop search
    if (searchInput) {
      setupSearchInput(searchInput, searchResults);
    }
    
    // Setup event listeners for mobile search
    if (searchInputMobile) {
      setupSearchInput(searchInputMobile, searchResultsMobile);
    }
  }
  
  function setupSearchInput(input, results) {
    // Input event for real-time search with enhanced feedback
    input.addEventListener('input', function(e) {
      e.preventDefault();
      const query = e.target.value.trim();
      
      // Clear previous timeout
      if (searchTimeout) {
        clearTimeout(searchTimeout);
      }
      
      // Show typing indicator for longer queries
      if (query.length > 2) {
        showTypingIndicator(results);
      }
      
      // Debounce search with progressive delay
      const delay = query.length > 3 ? 100 : 200;
      searchTimeout = setTimeout(function() {
        performSearch(query, results);
      }, delay);
    });
    
    // Enhanced keydown events for navigation
    input.addEventListener('keydown', function(e) {
      handleSearchKeydown(e, results);
    });
    
    // Focus events with enhanced feedback
    input.addEventListener('focus', function() {
      if (currentQuery.length > 0) {
        showSearchResults(results);
      }
      // Add focus animation
      this.parentElement.parentElement.classList.add('search-focused');
    });
    
    input.addEventListener('blur', function() {
      // Remove focus animation after a delay
      setTimeout(() => {
        this.parentElement.parentElement.classList.remove('search-focused');
      }, 200);
    });
    
    // Click outside to close results
    document.addEventListener('click', function(e) {
      if (!input.contains(e.target) && !results.contains(e.target)) {
        hideSearchResults(results);
      }
    });
    
    // Prevent form submission and enhance enter key behavior
    input.addEventListener('keypress', function(e) {
      if (e.key === 'Enter') {
        e.preventDefault();
        const activeResult = results.querySelector('.search-result-item.active');
        if (activeResult) {
          activeResult.click();
        } else {
          const firstResult = results.querySelector('.search-result-item');
          if (firstResult) {
            firstResult.click();
          }
        }
      }
    });
  }
  
  function handleSearchKeydown(e, results) {
    const resultItems = results.querySelectorAll('.search-result-item');
    const currentActive = results.querySelector('.search-result-item.active');
    let nextActive = null;
    
    switch(e.key) {
      case 'ArrowDown':
        e.preventDefault();
        if (currentActive) {
          nextActive = currentActive.nextElementSibling;
        } else if (resultItems.length > 0) {
          nextActive = resultItems[0];
        }
        break;
        
      case 'ArrowUp':
        e.preventDefault();
        if (currentActive) {
          nextActive = currentActive.previousElementSibling;
        } else if (resultItems.length > 0) {
          nextActive = resultItems[resultItems.length - 1];
        }
        break;
        
      case 'Escape':
        e.preventDefault();
        hideSearchResults(results);
        e.target.blur();
        break;
        
      case 'Enter':
        e.preventDefault();
        if (currentActive) {
          currentActive.click();
        }
        break;
    }
    
    // Update active state with smooth transitions
    if (currentActive) {
      currentActive.classList.remove('active');
    }
    if (nextActive) {
      nextActive.classList.add('active');
      // Ensure the active item is visible
      nextActive.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  }
  
  function performSearch(query, results) {
    currentQuery = query;
    
    if (!query || query.length < 2) {
      hideSearchResults(results);
      return;
    }
    
    console.log('Performing enhanced search for:', query);
    
    if (!searchIndex) {
      // Fallback to simple search
      const searchResults = simpleSearch(query);
      displayResults(searchResults, query, results);
      return;
    }
    
    try {
      const searchResults = searchIndex.search(query);
      console.log('Search results:', searchResults.length);
      displayResults(searchResults, query, results);
    } catch (error) {
      console.warn('Search error:', error);
      const searchResults = simpleSearch(query);
      displayResults(searchResults, query, results);
    }
  }
  
  function simpleSearch(query) {
    const lowerQuery = query.toLowerCase();
    const results = [];
    
    searchData.forEach(function(item, index) {
      const title = (item.title || '').toLowerCase();
      const content = (item.content || '').toLowerCase();
      const tags = (item.tags || '').toLowerCase();
      const category = (item.category || '').toLowerCase();
      const description = (item.description || '').toLowerCase();
      
      let score = 0;
      
      // Title matches get highest score
      if (title.includes(lowerQuery)) {
        score += 10;
      }
      
      // Content matches
      if (content.includes(lowerQuery)) {
        score += 5;
      }
      
      // Description matches
      if (description.includes(lowerQuery)) {
        score += 4;
      }
      
      // Tag matches
      if (tags.includes(lowerQuery)) {
        score += 3;
      }
      
      // Category matches
      if (category.includes(lowerQuery)) {
        score += 2;
      }
      
      if (score > 0) {
        results.push({
          ref: index,
          score: score
        });
      }
    });
    
    // Sort by score
    return results.sort(function(a, b) {
      return b.score - a.score;
    });
  }
  
  function displayResults(results, query, resultsContainer) {
    if (!resultsContainer) return;
    
    if (results.length === 0) {
      resultsContainer.innerHTML = `
        <div class="search-empty-state">
          <i class="ti ti-search-off"></i>
          <p>No results found for "${escapeHtml(query)}"</p>
          <small>Try different keywords or check spelling</small>
        </div>
      `;
      showSearchResults(resultsContainer);
      return;
    }
    
    const resultsHTML = results.slice(0, 8).map(function(result, index) {
      const item = searchData[result.ref];
      const title = item.title || 'Untitled';
      const content = item.content || '';
      const url = item.url || '#';
      const category = item.category || '';
      const description = item.description || '';
      
      // Use description if available, otherwise truncate content
      const displayContent = description || content.substring(0, 120) + (content.length > 120 ? '...' : '');
      
      return `
        <div class="search-result-item" data-url="${escapeHtml(url)}" style="animation-delay: ${index * 0.05}s">
          <div class="search-result-header">
            <div class="search-result-title">${highlightText(title, query)}</div>
            ${category ? `<div class="search-result-category">${escapeHtml(category)}</div>` : ''}
          </div>
          <div class="search-result-content">${highlightText(displayContent, query)}</div>
          <div class="search-result-url">${escapeHtml(url)}</div>
        </div>
      `;
    }).join('');
    
    resultsContainer.innerHTML = resultsHTML;
    showSearchResults(resultsContainer);
    
    // Add enhanced click handlers with feedback
    resultsContainer.querySelectorAll('.search-result-item').forEach(function(item) {
      item.addEventListener('click', function() {
        const url = this.getAttribute('data-url');
        if (url && url !== '#') {
          // Add click feedback
          this.style.transform = 'scale(0.98)';
          setTimeout(() => {
            window.location.href = url;
          }, 150);
        }
      });
      
      // Add hover effects
      item.addEventListener('mouseenter', function() {
        this.style.transform = 'translateX(4px) scale(1.01)';
      });
      
      item.addEventListener('mouseleave', function() {
        this.style.transform = 'translateX(0) scale(1)';
      });
    });
  }
  
  function highlightText(text, query) {
    if (!query) return escapeHtml(text);
    
    const regex = new RegExp(`(${escapeRegExp(query)})`, 'gi');
    return escapeHtml(text).replace(regex, '<mark>$1</mark>');
  }
  
  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
  
  function escapeRegExp(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }
  
  function showSearchResults(resultsContainer) {
    if (resultsContainer) {
      resultsContainer.style.display = 'block';
      // Add a small delay for smooth animation
      setTimeout(() => {
        resultsContainer.classList.add('show');
      }, 10);
    }
  }
  
  function hideSearchResults(resultsContainer) {
    if (resultsContainer) {
      resultsContainer.classList.remove('show');
      // Wait for animation to complete before hiding
      setTimeout(() => {
        resultsContainer.style.display = 'none';
      }, 200);
    }
  }
  
  function showLoadingState() {
    isLoading = true;
    const containers = [searchResults, searchResultsMobile];
    containers.forEach(container => {
      if (container) {
        container.innerHTML = `
          <div class="search-loading-state">
            <div class="search-spinner"></div>
            <p>Loading search data...</p>
          </div>
        `;
        showSearchResults(container);
      }
    });
  }
  
  function hideLoadingState() {
    isLoading = false;
    const containers = [searchResults, searchResultsMobile];
    containers.forEach(container => {
      if (container) {
        hideSearchResults(container);
      }
    });
  }
  
  function showTypingIndicator(resultsContainer) {
    if (isLoading) return;
    
    if (resultsContainer && !resultsContainer.querySelector('.search-typing-indicator')) {
      const typingIndicator = document.createElement('div');
      typingIndicator.className = 'search-typing-indicator';
      typingIndicator.innerHTML = `
        <div class="typing-dots">
          <span></span>
          <span></span>
          <span></span>
        </div>
        <p>Searching...</p>
      `;
      resultsContainer.appendChild(typingIndicator);
      showSearchResults(resultsContainer);
    }
  }
  
  function addLoadingStates() {
    // Add CSS for loading states
    const loadingCSS = `
      <style>
        .search-loading-state {
          padding: 2rem;
          text-align: center;
          color: var(--text-muted);
        }
        
        .search-spinner {
          width: 2rem;
          height: 2rem;
          border: 2px solid var(--border-color);
          border-top: 2px solid var(--primary);
          border-radius: 50%;
          animation: spin 1s linear infinite;
          margin: 0 auto 1rem;
        }
        
        .search-typing-indicator {
          padding: 1rem;
          text-align: center;
          color: var(--text-muted);
        }
        
        .typing-dots {
          display: flex;
          justify-content: center;
          gap: 0.25rem;
          margin-bottom: 0.5rem;
        }
        
        .typing-dots span {
          width: 0.5rem;
          height: 0.5rem;
          background: var(--text-muted);
          border-radius: 50%;
          animation: typing 1.4s infinite ease-in-out;
        }
        
        .typing-dots span:nth-child(1) { animation-delay: -0.32s; }
        .typing-dots span:nth-child(2) { animation-delay: -0.16s; }
        
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
        
        @keyframes typing {
          0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
          40% { transform: scale(1); opacity: 1; }
        }
        
        .search-focused {
          transform: translateY(-2px) scale(1.02);
        }
        
        .search-result-item {
          animation: searchResultSlideIn 0.3s ease forwards;
          opacity: 0;
          transform: translateX(-10px);
        }
        
        @keyframes searchResultSlideIn {
          to {
            opacity: 1;
            transform: translateX(0);
          }
        }
      </style>
    `;
    
    document.head.insertAdjacentHTML('beforeend', loadingCSS);
  }
  
  function addSearchToggle() {
    // Add keyboard shortcut (Ctrl/Cmd + K) with enhanced feedback
    document.addEventListener('keydown', function(e) {
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        // Focus desktop search if available, otherwise mobile
        if (searchInput) {
          searchInput.focus();
          // Add visual feedback
          searchInput.parentElement.parentElement.classList.add('search-shortcut-triggered');
          setTimeout(() => {
            searchInput.parentElement.parentElement.classList.remove('search-shortcut-triggered');
          }, 300);
        } else if (searchInputMobile) {
          searchInputMobile.focus();
          // Add visual feedback
          searchInputMobile.parentElement.parentElement.classList.add('search-shortcut-triggered');
          setTimeout(() => {
            searchInputMobile.parentElement.parentElement.classList.remove('search-shortcut-triggered');
          }, 300);
        }
      }
    });
    
    // Listen for theme changes to update search styling
    document.addEventListener('themeChanged', function(e) {
      updateSearchTheme(e.detail.theme);
    });
  }
  
  function updateSearchTheme(theme) {
    const allResults = [searchResults, searchResultsMobile];
    
    allResults.forEach(function(resultsContainer) {
      if (resultsContainer) {
        if (theme === 'dark') {
          resultsContainer.classList.add('dark-theme');
        } else {
          resultsContainer.classList.remove('dark-theme');
        }
      }
    });
  }
  
})(); 