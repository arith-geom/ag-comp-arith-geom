/*******************************************************************************
 * Modern AG Computational Arithmetic Geometry Website
 * Enhanced JavaScript for Theme Switching, Search, and Smooth Interactions
 ******************************************************************************/

$(document).ready(function () {
  // add toggle functionality to abstract, award and bibtex buttons
  $("a.abstract").click(function () {
    $(this).parent().parent().find(".abstract.hidden").toggleClass("open");
    $(this).parent().parent().find(".award.hidden.open").toggleClass("open");
    $(this).parent().parent().find(".bibtex.hidden.open").toggleClass("open");
  });
  $("a.award").click(function () {
    $(this).parent().parent().find(".abstract.hidden.open").toggleClass("open");
    $(this).parent().parent().find(".award.hidden").toggleClass("open");
    $(this).parent().parent().find(".bibtex.hidden.open").toggleClass("open");
  });
  $("a.bibtex").click(function () {
    $(this).parent().parent().find(".abstract.hidden.open").toggleClass("open");
    $(this).parent().parent().find(".award.hidden.open").toggleClass("open");
    $(this).parent().parent().find(".bibtex.hidden").toggleClass("open");
  });
  $("a").removeClass("waves-effect waves-light");

  // bootstrap-toc
  if ($("#toc-sidebar").length) {
    // remove related publications years from the TOC
    $(".publications h2").each(function () {
      $(this).attr("data-toc-skip", "");
    });
    var navSelector = "#toc-sidebar";
    var $myNav = $(navSelector);
    Toc.init($myNav);
    $("body").scrollspy({
      target: navSelector,
    });
  }

  // add css to jupyter notebooks
  const cssLink = document.createElement("link");
  cssLink.href = "../css/jupyter.css";
  cssLink.rel = "stylesheet";
  cssLink.type = "text/css";

  let jupyterTheme = determineComputedTheme();

  $(".jupyter-notebook-iframe-container iframe").each(function () {
    $(this).contents().find("head").append(cssLink);

    if (jupyterTheme == "dark") {
      $(this).bind("load", function () {
        $(this).contents().find("body").attr({
          "data-jp-theme-light": "false",
          "data-jp-theme-name": "JupyterLab Dark",
        });
      });
    }
  });

  // trigger popovers
  $('[data-toggle="popover"]').popover({
    trigger: "hover",
  });

  // Initialize theme system
  initializeTheme();
  
  // Initialize search functionality
  initializeSearch();
  
  // Initialize smooth animations
  initializeAnimations();
  
  // Initialize mobile menu
  initializeMobileMenu();
  
  // Initialize progress bar
  initializeProgressBar();
  
  // Initialize tooltips and popovers
  initializeTooltips();
});

/**
 * Theme Management System
 */
function initializeTheme() {
  const themeToggle = document.getElementById('light-toggle');
  const html = document.documentElement;
  
  // Get stored theme or default to light
  let currentTheme = localStorage.getItem('theme') || 'light';
  
  // Apply stored theme
  setTheme(currentTheme);
  
  // Theme toggle event listener
  if (themeToggle) {
    themeToggle.addEventListener('click', function() {
      currentTheme = currentTheme === 'light' ? 'dark' : 'light';
      setTheme(currentTheme);
      localStorage.setItem('theme', currentTheme);
      
      // Add a smooth transition effect
      document.body.style.transition = 'background-color 0.3s ease, color 0.3s ease';
      setTimeout(() => {
        document.body.style.transition = '';
      }, 300);
    });
  }
  
  function setTheme(theme) {
    html.setAttribute('data-theme', theme);
    updateThemeIcon(theme);
    
    // Update meta theme-color for mobile browsers
    updateMetaThemeColor(theme);
    
    // Trigger custom event for other components
    window.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme } }));
  }
  
  function updateThemeIcon(theme) {
    const sunIcon = document.getElementById('light-toggle-light');
    const moonIcon = document.getElementById('light-toggle-dark');
    const systemIcon = document.getElementById('light-toggle-system');
    
    if (sunIcon && moonIcon) {
      if (theme === 'dark') {
        sunIcon.style.display = 'inline-block';
        moonIcon.style.display = 'none';
        if (systemIcon) systemIcon.style.display = 'none';
      } else {
        sunIcon.style.display = 'none';
        moonIcon.style.display = 'inline-block';
        if (systemIcon) systemIcon.style.display = 'none';
      }
    }
  }
  
  function updateMetaThemeColor(theme) {
    const metaThemeColor = document.querySelector('meta[name="theme-color"]');
    if (metaThemeColor) {
      metaThemeColor.setAttribute('content', theme === 'dark' ? '#0F172A' : '#FFFFFF');
    }
  }
}

/**
 * Enhanced Search Functionality
 */
function initializeSearch() {
  const searchToggle = document.getElementById('search-toggle');
  const searchInput = document.getElementById('search-input');
  let searchResults = [];
  let searchIndex = null;
  
  // Initialize search index
  if (typeof lunr !== 'undefined') {
    buildSearchIndex();
  }
  
  // Search toggle functionality
  if (searchToggle) {
    searchToggle.addEventListener('click', function() {
      openSearchModal();
    });
  }
  
  // Keyboard shortcut for search (Ctrl/Cmd + K)
  document.addEventListener('keydown', function(e) {
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
      e.preventDefault();
      openSearchModal();
    }
    
    // Escape to close search
    if (e.key === 'Escape') {
      closeSearchModal();
    }
  });
  
  function openSearchModal() {
    // Create search modal if it doesn't exist
    let searchModal = document.getElementById('search-modal');
    if (!searchModal) {
      createSearchModal();
      searchModal = document.getElementById('search-modal');
    }
    
    searchModal.style.display = 'flex';
    searchModal.classList.add('fade-in');
    
    const modalSearchInput = document.getElementById('modal-search-input');
    if (modalSearchInput) {
      modalSearchInput.focus();
    }
    
    // Prevent body scrolling
    document.body.style.overflow = 'hidden';
  }
  
  function closeSearchModal() {
    const searchModal = document.getElementById('search-modal');
    if (searchModal) {
      searchModal.style.display = 'none';
      searchModal.classList.remove('fade-in');
    }
    
    // Restore body scrolling
    document.body.style.overflow = '';
  }
  
  function createSearchModal() {
    const modalHTML = `
      <div id="search-modal" class="search-modal" style="display: none;">
        <div class="search-modal-backdrop" onclick="closeSearchModal()"></div>
        <div class="search-modal-content">
          <div class="search-modal-header">
            <div class="search-input-container">
              <i class="ti ti-search search-icon"></i>
              <input 
                type="text" 
                id="modal-search-input" 
                class="search-modal-input" 
                placeholder="Search articles, pages, and content..."
                autocomplete="off"
              >
              <div class="search-shortcut">⌘K</div>
            </div>
          </div>
          <div class="search-modal-body">
            <div id="search-results" class="search-results">
              <div class="search-empty-state">
                <i class="ti ti-search search-empty-icon"></i>
                <p>Start typing to search...</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    
    // Add event listeners
    const modalSearchInput = document.getElementById('modal-search-input');
    if (modalSearchInput) {
      modalSearchInput.addEventListener('input', debounce(performSearch, 300));
    }
    
    // Make closeSearchModal globally available
    window.closeSearchModal = closeSearchModal;
  }
  
  function buildSearchIndex() {
    // Load search data from JSON file
    fetch('/assets/json/search.json')
      .then(response => response.json())
      .then(data => {
        searchResults = data.pages || [];
        
        // Build lunr search index
        searchIndex = lunr(function() {
          this.field('title', { boost: 10 });
          this.field('content', { boost: 5 });
          this.field('tags', { boost: 3 });
          this.ref('id');
          
          searchResults.forEach((page, index) => {
            this.add({
              id: index,
              title: page.title || '',
              content: page.content || '',
              tags: page.tags || '',
              url: page.url || ''
            });
          });
        });
      })
      .catch(error => {
        console.warn('Failed to load search index:', error);
        // Fallback to page content extraction
        const pages = [];
        
        document.querySelectorAll('h1, h2, h3, p').forEach(element => {
          const text = element.textContent.trim();
          if (text.length > 10) {
            pages.push({
              title: element.tagName.startsWith('H') ? text : '',
              content: text,
              url: window.location.pathname
            });
          }
        });
        
        searchIndex = lunr(function() {
          this.field('title', { boost: 10 });
          this.field('content');
          this.ref('id');
          
          pages.forEach((page, index) => {
            this.add({
              id: index,
              title: page.title,
              content: page.content,
              url: page.url
            });
          });
        });
        
        searchResults = pages;
      });
  }
  
  function performSearch(query) {
    const resultsContainer = document.getElementById('search-results');
    if (!resultsContainer || !searchIndex) return;
    
    if (query.length < 2) {
      resultsContainer.innerHTML = `
        <div class="search-empty-state">
          <i class="ti ti-search search-empty-icon"></i>
          <p>Start typing to search...</p>
        </div>
      `;
      return;
    }
    
    try {
      const results = searchIndex.search(query);
      displaySearchResults(results, query);
    } catch (error) {
      console.warn('Search error:', error);
      displaySearchResults([], query);
    }
  }
  
  function displaySearchResults(results, query) {
    const resultsContainer = document.getElementById('search-results');
    if (!resultsContainer) return;
    
    if (results.length === 0) {
      resultsContainer.innerHTML = `
        <div class="search-empty-state">
          <i class="ti ti-search-off search-empty-icon"></i>
          <p>No results found for "${query}"</p>
        </div>
      `;
      return;
    }
    
    const resultsHTML = results.slice(0, 8).map(result => {
      const item = searchResults[result.ref];
      return `
        <div class="search-result-item" onclick="navigateToResult('${item.url}')">
          <div class="search-result-title">${highlightText(item.title || 'Page', query)}</div>
          <div class="search-result-content">${highlightText(item.content.substring(0, 120) + '...', query)}</div>
          <div class="search-result-url">${item.url}</div>
        </div>
      `;
    }).join('');
    
    resultsContainer.innerHTML = resultsHTML;
  }
  
  function highlightText(text, query) {
    const regex = new RegExp(`(${escapeRegExp(query)})`, 'gi');
    return text.replace(regex, '<mark>$1</mark>');
  }
  
  function escapeRegExp(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }
  
  // Make navigateToResult globally available
  window.navigateToResult = function(url) {
    closeSearchModal();
    if (url !== window.location.pathname) {
      window.location.href = url;
    }
  };
}

/**
 * Smooth Animations and Interactions
 */
function initializeAnimations() {
  // Intersection Observer for fade-in animations
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };
  
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('fade-in');
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);
  
  // Observe elements for animation
  document.querySelectorAll('.card, .alert, .member-item').forEach(el => {
    observer.observe(el);
  });
  
  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });
  
  // Add hover effects to cards
  document.querySelectorAll('.card').forEach(card => {
    card.addEventListener('mouseenter', function() {
      this.style.transform = 'translateY(-4px)';
    });
    
    card.addEventListener('mouseleave', function() {
      this.style.transform = 'translateY(0)';
    });
  });
}

/**
 * Mobile Menu Functionality
 */
function initializeMobileMenu() {
  const navbarToggler = document.querySelector('.navbar-toggler');
  const navbarNav = document.querySelector('.navbar-nav');
  
  if (navbarToggler && navbarNav) {
    navbarToggler.addEventListener('click', function() {
      const isExpanded = this.getAttribute('aria-expanded') === 'true';
      this.setAttribute('aria-expanded', !isExpanded);
      navbarNav.classList.toggle('mobile-menu-open');
    });
    
    // Close mobile menu when clicking outside
    document.addEventListener('click', function(e) {
      if (!navbarToggler.contains(e.target) && !navbarNav.contains(e.target)) {
        navbarToggler.setAttribute('aria-expanded', 'false');
        navbarNav.classList.remove('mobile-menu-open');
      }
    });
  }
}

/**
 * Progress Bar for Page Loading
 */
function initializeProgressBar() {
  const progressBar = document.getElementById('progress');
  if (!progressBar) return;
  
  // Show progress on page load
  window.addEventListener('load', function() {
    progressBar.value = 100;
    setTimeout(() => {
      progressBar.style.opacity = '0';
    }, 500);
  });
  
  // Show progress on navigation
  document.addEventListener('beforeunload', function() {
    progressBar.style.opacity = '1';
    progressBar.value = 30;
  });
}

/**
 * Initialize Tooltips and Popovers
 */
function initializeTooltips() {
  // Initialize Bootstrap tooltips
  const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  tooltipTriggerList.map(function(tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });
  
  // Initialize Bootstrap popovers
  const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
  popoverTriggerList.map(function(popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl);
  });
}

/**
 * Utility Functions
 */
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// Theme change event listener for other components
window.addEventListener('themeChanged', function(e) {
  // Update any theme-dependent components
  console.log('Theme changed to:', e.detail.theme);
});

// Add CSS for search modal
const searchModalCSS = `
<style>
.search-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  z-index: 9999;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding-top: 10vh;
}

.search-modal-backdrop {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.search-modal-content {
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-2xl);
  box-shadow: var(--shadow-xl);
  width: 90%;
  max-width: 600px;
  max-height: 70vh;
  overflow: hidden;
  position: relative;
}

.search-modal-header {
  padding: var(--space-6);
  border-bottom: 1px solid var(--border-color);
}

.search-input-container {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: var(--space-4);
  color: var(--text-tertiary);
  font-size: 1.2rem;
}

.search-modal-input {
  width: 100%;
  padding: var(--space-4) var(--space-12);
  border: none;
  background: var(--bg-secondary);
  border-radius: var(--radius-lg);
  font-size: 1.1rem;
  color: var(--text-primary);
}

.search-modal-input:focus {
  outline: none;
  background: var(--bg-tertiary);
}

.search-shortcut {
  position: absolute;
  right: var(--space-4);
  background: var(--bg-tertiary);
  color: var(--text-tertiary);
  padding: var(--space-1) var(--space-2);
  border-radius: var(--radius-md);
  font-size: 0.75rem;
  font-weight: 500;
}

.search-modal-body {
  max-height: 50vh;
  overflow-y: auto;
}

.search-results {
  padding: var(--space-4);
}

.search-empty-state {
  text-align: center;
  padding: var(--space-8);
  color: var(--text-tertiary);
}

.search-empty-icon {
  font-size: 3rem;
  margin-bottom: var(--space-4);
  opacity: 0.5;
}

.search-result-item {
  padding: var(--space-4);
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: all var(--transition-fast);
  margin-bottom: var(--space-2);
}

.search-result-item:hover {
  background: var(--bg-secondary);
}

.search-result-title {
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--space-1);
}

.search-result-content {
  color: var(--text-secondary);
  font-size: 0.9rem;
  margin-bottom: var(--space-1);
}

.search-result-url {
  color: var(--text-tertiary);
  font-size: 0.8rem;
}

.search-result-item mark {
  background: var(--heidelberg-red);
  color: white;
  padding: 0 var(--space-1);
  border-radius: var(--radius-sm);
}
</style>
`;

// Add search modal CSS to head
document.head.insertAdjacentHTML('beforeend', searchModalCSS);
