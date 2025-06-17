/**
 * Heidelberg University Theme Switcher & Mobile Navigation
 * Handles dark/light mode switching and mobile menu functionality
 */

(function() {
  'use strict';

  // Theme Management
  const ThemeManager = {
    init() {
      this.body = document.body;
      this.themeToggle = document.querySelector('.theme-toggle');
      this.sunIcon = document.querySelector('.sun-icon');
      this.moonIcon = document.querySelector('.moon-icon');
      
      // Load saved theme or default to light
      this.currentTheme = localStorage.getItem('heidelberg-theme') || 'light';
      this.applyTheme(this.currentTheme);
      
      // Bind events
      this.bindEvents();
      
      console.log('Theme Manager initialized');
    },

    bindEvents() {
      if (this.themeToggle) {
        this.themeToggle.addEventListener('click', () => this.toggleTheme());
      }
      
      // Listen for system theme changes
      if (window.matchMedia) {
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
          if (!localStorage.getItem('heidelberg-theme')) {
            this.currentTheme = e.matches ? 'dark' : 'light';
            this.applyTheme(this.currentTheme);
          }
        });
      }
    },

    toggleTheme() {
      this.currentTheme = this.currentTheme === 'light' ? 'dark' : 'light';
      this.applyTheme(this.currentTheme);
      localStorage.setItem('heidelberg-theme', this.currentTheme);
      
      // Announce theme change for accessibility
      this.announceThemeChange();
    },

    applyTheme(theme) {
      if (theme === 'dark') {
        this.body.classList.add('dark-mode');
      } else {
        this.body.classList.remove('dark-mode');
      }
      
      // Update icons
      if (this.sunIcon && this.moonIcon) {
        if (theme === 'dark') {
          this.sunIcon.style.display = 'none';
          this.moonIcon.style.display = 'block';
        } else {
          this.sunIcon.style.display = 'block';
          this.moonIcon.style.display = 'none';
        }
      }
      
      // Update theme toggle aria-label
      if (this.themeToggle) {
        this.themeToggle.setAttribute('aria-label', 
          theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'
        );
      }
    },

    announceThemeChange() {
      const announcement = document.createElement('div');
      announcement.setAttribute('aria-live', 'polite');
      announcement.setAttribute('aria-atomic', 'true');
      announcement.className = 'sr-only';
      announcement.textContent = `Switched to ${this.currentTheme} mode`;
      
      document.body.appendChild(announcement);
      
      setTimeout(() => {
        document.body.removeChild(announcement);
      }, 1000);
    }
  };

  // Mobile Menu Management
  const MobileMenu = {
    init() {
      this.menuToggle = document.querySelector('.mobile-menu-toggle');
      this.mobileMenu = document.querySelector('.navbar-nav');
      this.isOpen = false;
      
      this.bindEvents();
      this.createMenuIcon();
      
      console.log('Mobile Menu initialized');
    },

    bindEvents() {
      if (this.menuToggle) {
        this.menuToggle.addEventListener('click', () => this.toggleMenu());
      }
      
      // Close menu when clicking outside
      document.addEventListener('click', (e) => {
        if (this.isOpen && !this.menuToggle.contains(e.target) && !this.mobileMenu.contains(e.target)) {
          this.closeMenu();
        }
      });
      
      // Close menu on escape key
      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && this.isOpen) {
          this.closeMenu();
        }
      });
      
      // Handle window resize
      window.addEventListener('resize', () => {
        if (window.innerWidth > 768 && this.isOpen) {
          this.closeMenu();
        }
      });
    },

    createMenuIcon() {
      if (this.menuToggle && !this.menuToggle.innerHTML.trim()) {
        this.menuToggle.innerHTML = '☰';
      }
    },

    toggleMenu() {
      if (this.isOpen) {
        this.closeMenu();
      } else {
        this.openMenu();
      }
    },

    openMenu() {
      if (this.mobileMenu) {
        this.mobileMenu.classList.add('mobile-menu-open');
        this.isOpen = true;
        this.menuToggle.innerHTML = '✕';
        
        // Focus first menu item for accessibility
        const firstMenuItem = this.mobileMenu.querySelector('.nav-link');
        if (firstMenuItem) {
          firstMenuItem.focus();
        }
      }
    },

    closeMenu() {
      if (this.mobileMenu) {
        this.mobileMenu.classList.remove('mobile-menu-open');
        this.isOpen = false;
        this.menuToggle.innerHTML = '☰';
      }
    }
  };

  // Search Enhancement
  const SearchManager = {
    init() {
      this.searchInput = document.querySelector('.search-input');
      this.searchContainer = document.querySelector('.search-container');
      
      if (this.searchInput) {
        this.bindEvents();
        console.log('Search Manager initialized');
      }
    },

    bindEvents() {
      // Enhanced search functionality
      this.searchInput.addEventListener('input', (e) => {
        this.handleSearchInput(e.target.value);
      });
      
      this.searchInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
          this.performSearch(e.target.value);
        }
      });
    },

    handleSearchInput(query) {
      if (query.length > 2) {
        // Add search suggestions or live search here
        console.log('Searching for:', query);
      }
    },

    performSearch(query) {
      if (query.trim()) {
        // Implement search functionality
        console.log('Performing search for:', query);
        // You can integrate with Jekyll's search or external search service
      }
    }
  };

  // Animation Manager
  const AnimationManager = {
    init() {
      this.observeElements();
      console.log('Animation Manager initialized');
    },

    observeElements() {
      if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
          entries.forEach(entry => {
            if (entry.isIntersecting) {
              entry.target.classList.add('animate-fade-in');
              observer.unobserve(entry.target);
            }
          });
        }, {
          threshold: 0.1,
          rootMargin: '50px'
        });

        // Observe elements with animation classes
        document.querySelectorAll('.animate-slide-up, .animate-slide-in-left, .animate-slide-in-right').forEach(el => {
          observer.observe(el);
        });
      }
    }
  };

  // Accessibility Manager
  const AccessibilityManager = {
    init() {
      this.addSkipLink();
      this.enhanceKeyboardNavigation();
      console.log('Accessibility Manager initialized');
    },

    addSkipLink() {
      const skipLink = document.createElement('a');
      skipLink.href = '#main-content';
      skipLink.textContent = 'Skip to main content';
      skipLink.className = 'skip-link sr-only';
      skipLink.style.cssText = `
        position: absolute;
        top: -40px;
        left: 6px;
        background: #C22032;
        color: white;
        padding: 8px;
        text-decoration: none;
        border-radius: 4px;
        z-index: 10000;
        transition: top 0.3s ease;
      `;
      
      skipLink.addEventListener('focus', () => {
        skipLink.style.top = '6px';
      });
      
      skipLink.addEventListener('blur', () => {
        skipLink.style.top = '-40px';
      });
      
      document.body.insertBefore(skipLink, document.body.firstChild);
    },

    enhanceKeyboardNavigation() {
      // Add focus indicators for better keyboard navigation
      document.addEventListener('keydown', (e) => {
        if (e.key === 'Tab') {
          document.body.classList.add('keyboard-nav');
        }
      });
      
      document.addEventListener('mousedown', () => {
        document.body.classList.remove('keyboard-nav');
      });
    }
  };

  // Performance Manager
  const PerformanceManager = {
    init() {
      this.optimizeImages();
      this.addLoadingStates();
      console.log('Performance Manager initialized');
    },

    optimizeImages() {
      // Add loading="lazy" to images
      document.querySelectorAll('img').forEach(img => {
        if (!img.hasAttribute('loading')) {
          img.setAttribute('loading', 'lazy');
        }
      });
    },

    addLoadingStates() {
      // Add loading states for better perceived performance
      document.addEventListener('DOMContentLoaded', () => {
        document.body.classList.add('loaded');
      });
    }
  };

  // Initialize everything when DOM is ready
  function initializeApp() {
    ThemeManager.init();
    MobileMenu.init();
    SearchManager.init();
    AnimationManager.init();
    AccessibilityManager.init();
    PerformanceManager.init();
    
    console.log('Heidelberg University Theme - All systems initialized');
  }

  // Wait for DOM to be ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeApp);
  } else {
    initializeApp();
  }

  // Add CSS for keyboard navigation
  const style = document.createElement('style');
  style.textContent = `
    .keyboard-nav *:focus {
      outline: 2px solid #C22032 !important;
      outline-offset: 2px !important;
    }
    
    .sr-only {
      position: absolute !important;
      width: 1px !important;
      height: 1px !important;
      padding: 0 !important;
      margin: -1px !important;
      overflow: hidden !important;
      clip: rect(0, 0, 0, 0) !important;
      white-space: nowrap !important;
      border: 0 !important;
    }
    
    .loaded {
      opacity: 1;
      transition: opacity 0.3s ease;
    }
    
    body:not(.loaded) {
      opacity: 0;
    }
  `;
  document.head.appendChild(style);

})(); 