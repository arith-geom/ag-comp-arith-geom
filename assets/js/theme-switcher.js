/**
 * Enhanced High-Contrast Theme Switcher & Navigation Manager
 * Handles dark/light mode switching with maximum readability and accessibility
 */

(function() {
  'use strict';

  // Enhanced Theme Manager with High Contrast Support
  const ThemeManager = {
    init() {
      this.body = document.body;
      this.html = document.documentElement;
      this.themeToggle = document.querySelector('#theme-toggle');
      this.darkModeToggle = document.querySelector('#dark-mode-toggle');
      this.floatingToggle = document.querySelector('#floating-theme-toggle');
      
      // Load saved theme or detect system preference
      this.currentTheme = this.getSavedTheme();
      console.log('Initial theme detected:', this.currentTheme);
      
      this.applyTheme(this.currentTheme);
      
      // Bind events
      this.bindEvents();
      
      console.log('Enhanced High-Contrast Theme Manager initialized with theme:', this.currentTheme);
      console.log('Body classes:', this.body.className);
      console.log('HTML data-theme:', this.html.getAttribute('data-theme'));
    },

    getSavedTheme() {
      const saved = localStorage.getItem('theme');
      if (saved && (saved === 'light' || saved === 'dark')) {
        return saved;
      }
      
      // Detect system preference
      if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        return 'dark';
      }
      
      return 'light';
    },

    bindEvents() {
      // Main theme toggle (in navbar)
      if (this.themeToggle) {
        this.themeToggle.addEventListener('click', (e) => {
          e.preventDefault();
          this.toggleTheme();
        });
      }
      
      // Dark mode toggle (floating)
      if (this.darkModeToggle) {
        this.darkModeToggle.addEventListener('click', (e) => {
          e.preventDefault();
          this.toggleTheme();
        });
      }
      
      // Listen for system theme changes
      if (window.matchMedia) {
        const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
        mediaQuery.addEventListener('change', (e) => {
          // Only auto-switch if user hasn't manually set a theme
          if (!localStorage.getItem('theme')) {
            this.currentTheme = e.matches ? 'dark' : 'light';
            this.applyTheme(this.currentTheme);
          }
        });
      }
      
      // Listen for custom theme change events
      document.addEventListener('themeChanged', (e) => {
        if (e.detail && e.detail.theme !== this.currentTheme) {
          this.currentTheme = e.detail.theme;
          this.applyTheme(this.currentTheme);
        }
      });
    },

    toggleTheme() {
      this.currentTheme = this.currentTheme === 'light' ? 'dark' : 'light';
      this.applyTheme(this.currentTheme);
      localStorage.setItem('theme', this.currentTheme);
      
      // Dispatch custom event for other components
      document.dispatchEvent(new CustomEvent('themeChanged', {
        detail: { theme: this.currentTheme }
      }));
      
      // Announce theme change for accessibility
      this.announceThemeChange();
    },

    applyTheme(theme) {
      console.log('Applying theme:', theme);
      
      // Remove existing theme classes and attributes
      this.body.classList.remove('dark-mode', 'light-mode');
      this.body.removeAttribute('data-theme');
      this.html.removeAttribute('data-theme');
      
      if (theme === 'dark') {
        // Apply dark mode with maximum contrast
        this.body.classList.add('dark-mode');
        this.body.setAttribute('data-theme', 'dark');
        this.html.setAttribute('data-theme', 'dark');
        
        // Force high contrast dark theme styles
        this.applyDarkModeStyles();
        console.log('Dark mode applied');
      } else {
        // Apply light mode with maximum contrast
        this.body.classList.add('light-mode');
        this.body.setAttribute('data-theme', 'light');
        this.html.setAttribute('data-theme', 'light');
        
        // Force high contrast light theme styles
        this.applyLightModeStyles();
        console.log('Light mode applied');
      }
      
      // Update all theme toggle icons and labels
      this.updateAllToggleElements(theme);
      
      console.log('Final body classes:', this.body.className);
      console.log('Final HTML data-theme:', this.html.getAttribute('data-theme'));
    },

    applyDarkModeStyles() {
      // Set CSS custom properties for maximum dark mode contrast
      const root = document.documentElement;
      
      // High contrast dark mode colors
      root.style.setProperty('--bg-primary', '#000000');
      root.style.setProperty('--bg-secondary', '#0A0A0A');
      root.style.setProperty('--bg-tertiary', '#111827');
      root.style.setProperty('--bg-muted', '#111827');
      root.style.setProperty('--bg-accent', '#450A0A');
      
      root.style.setProperty('--text-primary', '#FFFFFF');
      root.style.setProperty('--text-secondary', '#F3F4F6');
      root.style.setProperty('--text-tertiary', '#E5E7EB');
      root.style.setProperty('--text-muted', '#9CA3AF');
      root.style.setProperty('--text-inverse', '#000000');
      
      root.style.setProperty('--border-color', '#374151');
      root.style.setProperty('--border-dark', '#4B5563');
      root.style.setProperty('--border-light', '#1F2937');
      
      root.style.setProperty('--link-color', '#FF6B6B');
      root.style.setProperty('--link-hover', '#FF5252');
      
      root.style.setProperty('--primary', '#DC2626');
      root.style.setProperty('--primary-hover', '#B91C1C');
      root.style.setProperty('--primary-text', '#000000');
    },

    applyLightModeStyles() {
      // Set CSS custom properties for maximum light mode contrast
      const root = document.documentElement;
      
      // High contrast light mode colors
      root.style.setProperty('--bg-primary', '#FFFFFF');
      root.style.setProperty('--bg-secondary', '#F9FAFB');
      root.style.setProperty('--bg-tertiary', '#F3F4F6');
      root.style.setProperty('--bg-muted', '#F3F4F6');
      root.style.setProperty('--bg-accent', '#FEF2F2');
      
      root.style.setProperty('--text-primary', '#000000');
      root.style.setProperty('--text-secondary', '#111827');
      root.style.setProperty('--text-tertiary', '#1F2937');
      root.style.setProperty('--text-muted', '#4B5563');
      root.style.setProperty('--text-inverse', '#FFFFFF');
      
      root.style.setProperty('--border-color', '#E5E7EB');
      root.style.setProperty('--border-dark', '#D1D5DB');
      root.style.setProperty('--border-light', '#F3F4F6');
      
      root.style.setProperty('--link-color', '#C22032');
      root.style.setProperty('--link-hover', '#991B1B');
      
      root.style.setProperty('--primary', '#C22032');
      root.style.setProperty('--primary-hover', '#991B1B');
      root.style.setProperty('--primary-text', '#FFFFFF');
    },

    updateAllToggleElements(theme) {
      // Update main theme toggle icon (navbar)
      const themeIcon = document.querySelector('#theme-icon');
      if (themeIcon) {
        themeIcon.className = theme === 'dark' ? 'fas fa-sun theme-icon' : 'fas fa-moon theme-icon';
      }
      
      // Update floating dark mode toggle icon
      const darkModeIcon = document.querySelector('#dark-mode-icon');
      if (darkModeIcon) {
        darkModeIcon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
      }
      
      // Update any other theme icons
      const allThemeIcons = document.querySelectorAll('.theme-icon');
      allThemeIcons.forEach(icon => {
        if (icon.id !== 'theme-icon') { // Avoid double-updating the main icon
          icon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
        }
      });
      
      // Update aria labels and titles
      this.updateAriaLabels(theme);
      
      // Update meta theme color for mobile browsers
      this.updateMetaThemeColor(theme);
    },

    updateAriaLabels(theme) {
      const label = theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode';
      
      // Update all theme toggle buttons
      const toggleButtons = document.querySelectorAll('#theme-toggle, #dark-mode-toggle');
      toggleButtons.forEach(button => {
        button.setAttribute('aria-label', label);
        button.setAttribute('title', label);
      });
    },

    announceThemeChange() {
      // Create screen reader announcement
      const announcement = document.createElement('div');
      announcement.setAttribute('aria-live', 'polite');
      announcement.className = 'sr-only';
      announcement.textContent = `Switched to ${this.currentTheme} mode`;
      document.body.appendChild(announcement);
      
      // Remove announcement after screen readers have processed it
      setTimeout(() => {
        if (document.body.contains(announcement)) {
        document.body.removeChild(announcement);
        }
      }, 1000);
    },

    updateMetaThemeColor(theme) {
      const metaThemeColor = document.querySelector('meta[name="theme-color"]');
      if (metaThemeColor) {
        metaThemeColor.setAttribute('content', theme === 'dark' ? '#000000' : '#C22032');
      }
    }
  };

  // Enhanced Mobile Menu Manager
  const MobileMenuManager = {
    init() {
      this.navbarToggler = document.querySelector('.navbar-toggler');
      this.navbarCollapse = document.querySelector('.navbar-collapse');
      this.navLinks = document.querySelectorAll('.navbar-nav .nav-link');
      
      this.bindEvents();
    },

    bindEvents() {
      if (this.navbarToggler && this.navbarCollapse) {
        this.navbarToggler.addEventListener('click', () => {
          this.toggleMenu();
        });
        
        // Close menu when clicking nav links (mobile only)
        this.navLinks.forEach(link => {
          link.addEventListener('click', () => {
            if (window.innerWidth < 992) {
          this.closeMenu();
        }
          });
      });
      
      // Close menu on escape key
      document.addEventListener('keydown', (e) => {
          if (e.key === 'Escape' && this.navbarCollapse.classList.contains('show')) {
          this.closeMenu();
        }
      });
      }
    },

    toggleMenu() {
      // This will be handled by Bootstrap's collapse component
    },

    openMenu() {
      const isExpanded = this.navbarToggler.getAttribute('aria-expanded') === 'true';
      if (!isExpanded) {
        this.navbarToggler.setAttribute('aria-expanded', 'true');
        this.announceMenuState('Menu expanded');
      }
    },

    closeMenu() {
      const bsCollapse = bootstrap?.Collapse?.getInstance(this.navbarCollapse);
      if (bsCollapse) {
        bsCollapse.hide();
      }
      this.navbarToggler.setAttribute('aria-expanded', 'false');
      this.announceMenuState('Menu collapsed');
    },

    announceMenuState(message) {
      // Create screen reader announcement
      const announcement = document.createElement('div');
      announcement.setAttribute('aria-live', 'polite');
      announcement.className = 'sr-only';
      announcement.textContent = message;
      document.body.appendChild(announcement);
      
      setTimeout(() => {
        if (document.body.contains(announcement)) {
          document.body.removeChild(announcement);
        }
      }, 1000);
    }
  };

  // Enhanced Accessibility Manager
  const AccessibilityManager = {
    init() {
      this.addSkipLink();
      this.enhanceKeyboardNavigation();
      this.addKeyboardSupportToCustomElements();
      this.improveColorContrast();
    },

    addSkipLink() {
      // Skip link is already in the header template
      const skipLink = document.querySelector('.skip-link');
      if (skipLink) {
        skipLink.addEventListener('click', (e) => {
          e.preventDefault();
          const target = document.querySelector('#main-content');
          if (target) {
            target.focus();
            target.scrollIntoView();
          }
        });
      }
    },

    enhanceKeyboardNavigation() {
      // Add keyboard support for custom elements
      document.addEventListener('keydown', (e) => {
        // Handle theme switching with keyboard shortcuts
        if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'T') {
          e.preventDefault();
          ThemeManager.toggleTheme();
        }
        
        // Alternative shortcut: Ctrl/Cmd + D
        if ((e.ctrlKey || e.metaKey) && e.key === 'd') {
          e.preventDefault();
          ThemeManager.toggleTheme();
        }
      });
    },

    addKeyboardSupportToCustomElements() {
      // Ensure all interactive elements have proper keyboard support
      const interactiveElements = document.querySelectorAll('[role="button"]:not(button):not(input)');
      interactiveElements.forEach(element => {
        if (!element.getAttribute('tabindex')) {
          element.setAttribute('tabindex', '0');
        }
        
        element.addEventListener('keydown', (e) => {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            element.click();
          }
        });
      });
    },

    improveColorContrast() {
      // This is handled by CSS variables and forced contrast in theme files
      // Additional contrast improvements could be added here if needed
      console.log('Color contrast improvements applied');
    }
  };

  // Performance Manager for optimizations
  const PerformanceManager = {
    init() {
      this.optimizeImages();
      this.addLoadingStates();
    },

    optimizeImages() {
      // Add loading="lazy" to images that don't have it
      const images = document.querySelectorAll('img:not([loading])');
      images.forEach(img => {
          img.setAttribute('loading', 'lazy');
      });
    },

    addLoadingStates() {
      // Add loading states for theme switches
      document.addEventListener('themeChanged', () => {
        document.body.classList.add('theme-transitioning');
        setTimeout(() => {
          document.body.classList.remove('theme-transitioning');
        }, 300);
      });
    }
  };

  // Initialize all managers when DOM is ready
  function initializeApp() {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', initializeApp);
      return;
    }

    // Initialize all components
    ThemeManager.init();
    MobileMenuManager.init();
    AccessibilityManager.init();
    PerformanceManager.init();
    
    console.log('Theme Switcher: All components initialized successfully');
  }

  // Start initialization
    initializeApp();

  // Expose ThemeManager globally for external access
  window.ThemeManager = ThemeManager;

})(); 