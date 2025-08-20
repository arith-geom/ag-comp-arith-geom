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
      // Floating toggle removed

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

        initWithoutTheme() {
      this.body = document.body;
      this.html = document.documentElement;

      // Load saved theme but don't apply it (head script already did)
      this.currentTheme = this.getSavedTheme();
      console.log('Theme detected (already applied by head script):', this.currentTheme);

      // Don't bind events yet - wait for DOM to be ready
      console.log('Theme Manager initialized without applying theme');
    },

    getSavedTheme() {
      const saved = localStorage.getItem('theme');
      console.log('Saved theme in localStorage:', saved);

      if (saved && (saved === 'light' || saved === 'dark')) {
        console.log('Using saved theme:', saved);
        return saved;
      }

      // Detect system preference
      if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        console.log('System prefers dark theme');
        return 'dark';
      }

      console.log('Defaulting to light theme');
      return 'light';
    },

    bindEvents() {
      console.log('Binding events. Theme toggle element found:', !!this.themeToggle);

      // Main theme toggle (in navbar)
      if (this.themeToggle) {
        console.log('Adding click event to theme toggle');
        this.themeToggle.addEventListener('click', (e) => {
          console.log('Theme toggle clicked!');
          e.preventDefault();
          this.toggleTheme();
        });
      } else {
        console.error('Theme toggle element not found!');
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
      console.log('=== THEME TOGGLE START ===');
      console.log('Toggle theme called. Current theme:', this.currentTheme);
      console.log('localStorage theme before:', localStorage.getItem('theme'));

      this.currentTheme = this.currentTheme === 'light' ? 'dark' : 'light';
      console.log('New theme will be:', this.currentTheme);

      this.applyTheme(this.currentTheme);
      localStorage.setItem('theme', this.currentTheme);
      console.log('Theme saved to localStorage:', this.currentTheme);
      console.log('localStorage theme after:', localStorage.getItem('theme'));

      // Dispatch custom event for other components
      document.dispatchEvent(new CustomEvent('themeChanged', {
        detail: { theme: this.currentTheme }
      }));

      // Announce theme change for accessibility
      this.announceThemeChange();
      console.log('=== THEME TOGGLE END ===');
    },

    applyTheme(theme) {
      console.log('Applying theme:', theme, '- Current localStorage:', localStorage.getItem('theme'));
      
      console.log('Removing existing theme classes and attributes');
      // Remove existing theme classes and attributes
      this.body.classList.remove('dark-mode', 'light-mode');
      this.body.removeAttribute('data-theme');
      this.html.removeAttribute('data-theme');
      
      if (theme === 'dark') {
        console.log('Setting dark mode classes and attributes');
        // Apply dark mode with maximum contrast
        this.body.classList.add('dark-mode');
        this.body.setAttribute('data-theme', 'dark');
        this.html.setAttribute('data-theme', 'dark');

        // Force high contrast dark theme styles
        this.applyDarkModeStyles();
        console.log('Dark mode applied');
      } else {
        console.log('Setting light mode classes and attributes');
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
      console.log('Applying dark mode CSS variables - matching head script exactly');
      // Set CSS custom properties - must match head script exactly
      const root = document.documentElement;

      // Set the same variables that the head script sets
      root.style.setProperty('--primary', '#DC2626');
      root.style.setProperty('--primary-hover', '#B91C1C');
      root.style.setProperty('--primary-text', '#000000');
      root.style.setProperty('--bg-primary', '#000000');
      root.style.setProperty('--text-primary', '#FFFFFF');
      root.style.setProperty('--bg-secondary', '#0A0A0A');
      root.style.setProperty('--text-secondary', '#F3F4F6');

      console.log('Dark mode CSS variables applied - matches head script');
    },

    applyLightModeStyles() {
      console.log('Applying light mode CSS variables - matching head script exactly');
      // Set CSS custom properties - must match head script exactly
      const root = document.documentElement;

      // Set the same variables that the head script sets
      root.style.setProperty('--primary', '#C22032');
      root.style.setProperty('--primary-hover', '#991B1B');
      root.style.setProperty('--primary-text', '#FFFFFF');
      root.style.setProperty('--bg-primary', '#FFFFFF');
      root.style.setProperty('--text-primary', '#000000');
      root.style.setProperty('--bg-secondary', '#F9FAFB');
      root.style.setProperty('--text-secondary', '#111827');

      console.log('Light mode CSS variables applied - matches head script');
    },

    updateAllToggleElements(theme) {
      // Update main theme toggle icons (navbar)
      const themeIconLight = document.querySelector('#theme-icon-light');
      const themeIconDark = document.querySelector('#theme-icon-dark');
      if (themeIconLight && themeIconDark) {
        if (theme === 'dark') {
          themeIconLight.style.display = 'inline-block';
          themeIconDark.style.display = 'none';
        } else {
          themeIconLight.style.display = 'none';
          themeIconDark.style.display = 'inline-block';
        }
      }
      
      // Update floating dark mode toggle icons
      const darkModeIconLight = document.querySelector('#dark-mode-icon-light');
      const darkModeIconDark = document.querySelector('#dark-mode-icon-dark');
      if (darkModeIconLight && darkModeIconDark) {
        if (theme === 'dark') {
          darkModeIconLight.style.display = 'inline-block';
          darkModeIconDark.style.display = 'none';
        } else {
          darkModeIconLight.style.display = 'none';
          darkModeIconDark.style.display = 'inline-block';
        }
      }
      
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

  // Initialize immediately to prevent flash
  function initializeApp() {
    // Don't apply theme immediately - let the head script handle that
    ThemeManager.initWithoutTheme();

    // Initialize all components and bind events when DOM is ready
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', function() {
        // Find and bind theme toggle elements
        ThemeManager.themeToggle = document.querySelector('#theme-toggle');
        ThemeManager.darkModeToggle = document.querySelector('#dark-mode-toggle');
        ThemeManager.floatingToggle = document.querySelector('#floating-theme-toggle');

        // Now bind events
        ThemeManager.bindEvents();

        MobileMenuManager.init();
        AccessibilityManager.init();
        PerformanceManager.init();
        console.log('Theme Switcher: All components initialized successfully');
      });
    } else {
      // Find and bind theme toggle elements
      ThemeManager.themeToggle = document.querySelector('#theme-toggle');
      ThemeManager.darkModeToggle = document.querySelector('#dark-mode-toggle');
      ThemeManager.floatingToggle = document.querySelector('#floating-theme-toggle');

      // Now bind events
      ThemeManager.bindEvents();

      MobileMenuManager.init();
      AccessibilityManager.init();
      PerformanceManager.init();
      console.log('Theme Switcher: All components initialized successfully');
    }
  }

  // Start initialization immediately
  initializeApp();

  // Expose ThemeManager globally for external access
  window.ThemeManager = ThemeManager;

})(); 