// Language Switcher Functionality
class LanguageSwitcher {
  constructor() {
    this.currentLang = this.getCurrentLanguage();
    this.translations = null;
    this.init();
  }

  async init() {
    try {
      // Load translations
      console.log('Loading translations...');
      const response = await fetch('/assets/js/translations.json');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      this.translations = await response.json();
      console.log('Translations loaded successfully:', this.translations);
      
      // Initialize language switcher
      this.setupLanguageSwitcher();
      this.updatePageContent();
      this.updateHTMLAttributes();
      
      // Listen for language changes
      this.setupEventListeners();
    } catch (error) {
      console.error('Failed to load translations:', error);
      // Create a basic translations object as fallback
      this.translations = {
        en: { nav: {}, common: {}, about: {} },
        de: { nav: {}, common: {}, about: {} }
      };
    }
  }

  getCurrentLanguage() {
    // Check localStorage first, then fallback to default
    return localStorage.getItem('preferred-language') || 'en';
  }

  setCurrentLanguage(lang) {
    this.currentLang = lang;
    localStorage.setItem('preferred-language', lang);
    this.updatePageContent();
    this.updateHTMLAttributes();
    this.updateLanguageSwitcherButton();
    
    // Notify other components about language change
    document.dispatchEvent(new CustomEvent('languageChanged', {
      detail: { language: lang }
    }));
    
    // Update bilingual CMS if available
    if (window.bilingualCMS) {
      window.bilingualCMS.setCurrentLanguage(lang);
    }
  }

  setupLanguageSwitcher() {
    console.log('Setting up language switcher...');
    // The language switcher is now already in the header HTML
    const existingSwitcher = document.getElementById('language-switcher');
    if (existingSwitcher) {
      console.log('Language switcher button found in header');
      this.updateLanguageSwitcherButton();
    } else {
      console.error('Language switcher button not found in header');
    }
  }

  setupEventListeners() {
    console.log('Setting up event listeners...');
    // Listen for language option clicks
    document.addEventListener('click', (e) => {
      if (e.target.classList.contains('language-option') || e.target.closest('.language-option')) {
        const option = e.target.classList.contains('language-option') ? e.target : e.target.closest('.language-option');
        console.log('Language option clicked:', option.dataset.lang);
        const newLang = option.dataset.lang;
        this.setCurrentLanguage(newLang);
        this.updateLanguageSwitcherButton();
        
        // Close the dropdown
        const dropdown = option.closest('.dropdown');
        if (dropdown) {
          const dropdownToggle = dropdown.querySelector('[data-bs-toggle="dropdown"]');
          if (dropdownToggle) {
            // Trigger Bootstrap dropdown close
            const bsDropdown = bootstrap.Dropdown.getInstance(dropdownToggle);
            if (bsDropdown) {
              bsDropdown.hide();
            } else {
              // Fallback: manually close dropdown
              dropdown.classList.remove('show');
              dropdownToggle.setAttribute('aria-expanded', 'false');
            }
          }
        }
      }
    });
  }

  getFlagIcon(lang) {
    const flagMap = {
      'en': 'us',
      'de': 'de'
    };
    return flagMap[lang] || 'us';
  }

  updateLanguageSwitcherButton() {
    const switcherBtn = document.getElementById('language-switcher');
    if (switcherBtn) {
      const flagIcon = switcherBtn.querySelector('.flag-icon');
      const languageCode = switcherBtn.querySelector('.language-code');
      
      if (flagIcon) {
        flagIcon.className = `flag-icon flag-icon-${this.getFlagIcon(this.currentLang)}`;
      }
      
      if (languageCode) {
        languageCode.textContent = this.currentLang.toUpperCase();
      }
      
      switcherBtn.title = this.getTranslation('common.language_switch');
    }
  }

  getTranslation(key) {
    if (!this.translations || !this.translations[this.currentLang]) {
      return key; // Fallback to key if translation not found
    }
    
    const keys = key.split('.');
    let value = this.translations[this.currentLang];
    
    for (const k of keys) {
      if (value && value[k]) {
        value = value[k];
      } else {
        return key; // Fallback to key if translation not found
      }
    }
    
    return value;
  }

  updatePageContent() {
    // Update navigation links
    this.updateNavigation();
    
    // Update search placeholder
    this.updateSearchPlaceholder();
    
    // Update page-specific content
    this.updatePageSpecificContent();
  }

  updateNavigation() {
    // Update navigation links based on page titles
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    navLinks.forEach(link => {
      const text = link.textContent.trim();
      const icon = link.querySelector('i');
      
      // Map common navigation items
      if (text === 'About' || text === 'Über uns') {
        link.textContent = '';
        if (icon) link.appendChild(icon);
        link.appendChild(document.createTextNode(this.getTranslation('nav.about')));
      } else if (text === 'Research' || text === 'Forschung') {
        link.textContent = '';
        if (icon) link.appendChild(icon);
        link.appendChild(document.createTextNode(this.getTranslation('nav.research')));
      } else if (text === 'Publications' || text === 'Publikationen') {
        link.textContent = '';
        if (icon) link.appendChild(icon);
        link.appendChild(document.createTextNode(this.getTranslation('nav.publications')));
      } else if (text === 'Teaching' || text === 'Lehre') {
        link.textContent = '';
        if (icon) link.appendChild(icon);
        link.appendChild(document.createTextNode(this.getTranslation('nav.teaching')));
      } else if (text === 'Members' || text === 'Mitglieder') {
        link.textContent = '';
        if (icon) link.appendChild(icon);
        link.appendChild(document.createTextNode(this.getTranslation('nav.members')));
      } else if (text === 'Links' || text === 'Links') {
        link.textContent = '';
        if (icon) link.appendChild(icon);
        link.appendChild(document.createTextNode(this.getTranslation('nav.links')));
      } else if (text === 'Contact' || text === 'Kontakt') {
        link.textContent = '';
        if (icon) link.appendChild(icon);
        link.appendChild(document.createTextNode(this.getTranslation('nav.contact')));
      } else if (text === 'Resources' || text === 'Ressourcen') {
        link.textContent = '';
        if (icon) link.appendChild(icon);
        link.appendChild(document.createTextNode(this.getTranslation('nav.resources')));
      } else if (text === 'News' || text === 'Neuigkeiten') {
        link.textContent = '';
        if (icon) link.appendChild(icon);
        link.appendChild(document.createTextNode(this.getTranslation('nav.news')));
      }
    });
  }

  updateSearchPlaceholder() {
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
      const placeholderKey = `data-placeholder-${this.currentLang}`;
      const newPlaceholder = searchInput.getAttribute(placeholderKey) || this.getTranslation('common.search_placeholder');
      searchInput.placeholder = newPlaceholder;
      searchInput.setAttribute('aria-label', this.getTranslation('common.search'));
    }
  }

  updatePageSpecificContent() {
    // Update translatable content elements
    this.updateTranslatableContent();
    
    // Update page titles and content based on current page
    const currentPage = this.getCurrentPage();
    
    if (currentPage === 'about' || window.location.pathname === '/' || window.location.pathname === '/index.html') {
      this.updateAboutPage();
    } else if (currentPage === 'research') {
      this.updateResearchPage();
    } else if (currentPage === 'publications') {
      this.updatePublicationsPage();
    } else if (currentPage === 'teaching') {
      this.updateTeachingPage();
    } else if (currentPage === 'members') {
      this.updateMembersPage();
    } else if (currentPage === 'links') {
      this.updateLinksPage();
    } else if (currentPage === 'contact') {
      this.updateContactPage();
    } else if (currentPage === 'resources') {
      this.updateResourcesPage();
    } else if (currentPage === 'news') {
      this.updateNewsPage();
    }
  }

  updateTranslatableContent() {
    // Update all elements with translatable-content class
    const translatableElements = document.querySelectorAll('.translatable-content');
    translatableElements.forEach(element => {
      const translationKey = element.getAttribute('data-translation-key');
      if (translationKey) {
        const translation = this.getTranslation(translationKey);
        if (translation && translation !== translationKey) {
          element.textContent = translation;
        }
      }
    });
  }

  getCurrentPage() {
    const path = window.location.pathname;
    if (path === '/' || path === '/index.html') return 'about';
    
    const segments = path.split('/').filter(s => s);
    if (segments.length > 0) {
      return segments[segments.length - 1].replace('.html', '');
    }
    return 'about';
  }

  updateAboutPage() {
    // Update page title
    const pageTitle = document.querySelector('h1, .page-title');
    if (pageTitle) {
      pageTitle.textContent = this.getTranslation('about.title');
    }

    // Update content paragraphs
    const paragraphs = document.querySelectorAll('p');
    paragraphs.forEach((p, index) => {
      const text = p.textContent.trim();
      
      if (text.includes('research group "computational arithmetic geometry"') || 
          text.includes('Forschungsgruppe "Computational Arithmetic Geometry"')) {
        p.textContent = this.getTranslation('about.description');
      } else if (text.includes('Within algebraic number theory') || 
                 text.includes('Innerhalb der algebraischen Zahlentheorie')) {
        p.textContent = this.getTranslation('about.content');
      } else if (text.includes('To tackle problems') || 
                 text.includes('Um Probleme in den oben beschriebenen')) {
        p.textContent = this.getTranslation('about.methods');
      } else if (text.includes('A more detailed survey') || 
                 text.includes('Eine detailliertere Übersicht')) {
        p.textContent = this.getTranslation('about.more_info');
      }
    });

    // Update "Latest News" section
    const latestNewsHeading = document.querySelector('h2');
    if (latestNewsHeading && latestNewsHeading.textContent.includes('Latest News')) {
      latestNewsHeading.textContent = this.getTranslation('about.latest_news');
    }

    // Update "View all news" button
    const viewAllNewsBtn = document.querySelector('a[href*="/news/"]');
    if (viewAllNewsBtn && viewAllNewsBtn.textContent.includes('View all news')) {
      viewAllNewsBtn.textContent = this.getTranslation('about.view_all_news');
    }
  }

  updateResearchPage() {
    const pageTitle = document.querySelector('h1, .page-title');
    if (pageTitle) {
      pageTitle.textContent = this.getTranslation('research.title');
    }
  }

  updatePublicationsPage() {
    const pageTitle = document.querySelector('h1, .page-title');
    if (pageTitle) {
      pageTitle.textContent = this.getTranslation('publications.title');
    }
  }

  updateTeachingPage() {
    const pageTitle = document.querySelector('h1, .page-title');
    if (pageTitle) {
      pageTitle.textContent = this.getTranslation('teaching.title');
    }
  }

  updateMembersPage() {
    const pageTitle = document.querySelector('h1, .page-title');
    if (pageTitle) {
      pageTitle.textContent = this.getTranslation('members.title');
    }
  }

  updateLinksPage() {
    const pageTitle = document.querySelector('h1, .page-title');
    if (pageTitle) {
      pageTitle.textContent = this.getTranslation('links.title');
    }
  }

  updateContactPage() {
    const pageTitle = document.querySelector('h1, .page-title');
    if (pageTitle) {
      pageTitle.textContent = this.getTranslation('contact.title');
    }
  }

  updateResourcesPage() {
    const pageTitle = document.querySelector('h1, .page-title');
    if (pageTitle) {
      pageTitle.textContent = this.getTranslation('resources.title');
    }
  }

  updateNewsPage() {
    const pageTitle = document.querySelector('h1, .page-title');
    if (pageTitle) {
      pageTitle.textContent = this.getTranslation('news.title');
    }
  }

  updateHTMLAttributes() {
    // Update html lang attribute
    document.documentElement.lang = this.currentLang;
    
    // Update meta tags
    const metaLang = document.querySelector('meta[name="language"]');
    if (metaLang) {
      metaLang.setAttribute('content', this.currentLang);
    }
  }
}

// Initialize language switcher when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  console.log('DOM loaded, initializing Language Switcher...');
  setTimeout(() => {
    new LanguageSwitcher();
  }, 100);
});

// Also try to initialize if DOM is already loaded
if (document.readyState === 'loading') {
  // DOM is still loading
} else {
  // DOM is already loaded
  console.log('DOM already loaded, initializing Language Switcher immediately...');
  setTimeout(() => {
    new LanguageSwitcher();
  }, 100);
}

// Additional initialization after window load
window.addEventListener('load', () => {
  console.log('Window loaded, checking Language Switcher...');
  setTimeout(() => {
    if (!document.getElementById('language-switcher')) {
      console.log('Language switcher not found, reinitializing...');
      new LanguageSwitcher();
    }
  }, 500);
}); 