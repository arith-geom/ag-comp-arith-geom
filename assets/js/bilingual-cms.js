// Bilingual CMS System
// This script provides a complete bilingual content management system

class BilingualCMS {
  constructor() {
    this.currentLang = this.getCurrentLanguage();
    this.supportedLanguages = ['en', 'de'];
    this.languageNames = {
      'en': 'English',
      'de': 'Deutsch'
    };
    this.contentCache = {};
    this.init();
  }

  async init() {
    console.log('Initializing Bilingual CMS...');
    this.setupCMSInterface();
    this.setupEventListeners();
    this.loadContentForCurrentLanguage();
  }

  getCurrentLanguage() {
    return localStorage.getItem('preferred-language') || 'en';
  }

  setCurrentLanguage(lang) {
    this.currentLang = lang;
    localStorage.setItem('preferred-language', lang);
    this.updateCMSInterface();
    this.loadContentForCurrentLanguage();
  }

  setupCMSInterface() {
    // Create CMS admin panel
    const cmsPanel = document.createElement('div');
    cmsPanel.id = 'bilingual-cms-panel';
    cmsPanel.className = 'cms-panel';
    cmsPanel.style.cssText = `
      position: fixed;
      bottom: 20px;
      right: 20px;
      background: white;
      border: 1px solid #ddd;
      border-radius: 8px;
      padding: 15px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
      z-index: 10000;
      min-width: 300px;
      display: none;
    `;

    cmsPanel.innerHTML = `
      <div class="cms-header">
        <h4 style="margin: 0 0 10px 0; color: #333;">Bilingual CMS</h4>
        <div class="language-selector" style="margin-bottom: 15px;">
          <label style="display: block; margin-bottom: 5px; font-weight: bold;">Language:</label>
          <select id="cms-language-selector" style="width: 100%; padding: 5px; border: 1px solid #ccc; border-radius: 4px;">
            <option value="en">English</option>
            <option value="de">Deutsch</option>
          </select>
        </div>
      </div>
      
      <div class="cms-content">
        <div class="content-section">
          <label style="display: block; margin-bottom: 5px; font-weight: bold;">Page Title:</label>
          <input type="text" id="cms-page-title" style="width: 100%; padding: 5px; border: 1px solid #ccc; border-radius: 4px; margin-bottom: 10px;">
        </div>
        
        <div class="content-section">
          <label style="display: block; margin-bottom: 5px; font-weight: bold;">Content:</label>
          <textarea id="cms-page-content" rows="8" style="width: 100%; padding: 5px; border: 1px solid #ccc; border-radius: 4px; margin-bottom: 10px; resize: vertical;"></textarea>
        </div>
        
        <div class="cms-actions" style="display: flex; gap: 10px;">
          <button id="cms-save-btn" style="flex: 1; padding: 8px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer;">Save</button>
          <button id="cms-preview-btn" style="flex: 1; padding: 8px; background: #28a745; color: white; border: none; border-radius: 4px; cursor: pointer;">Preview</button>
          <button id="cms-close-btn" style="flex: 1; padding: 8px; background: #6c757d; color: white; border: none; border-radius: 4px; cursor: pointer;">Close</button>
        </div>
      </div>
    `;

    document.body.appendChild(cmsPanel);

    // Create CMS toggle button
    const cmsToggle = document.createElement('button');
    cmsToggle.id = 'bilingual-cms-toggle';
    cmsToggle.innerHTML = '<i class="fas fa-edit"></i> CMS';
    cmsToggle.style.cssText = `
      position: fixed;
      bottom: 20px;
      right: 20px;
      background: #007bff;
      color: white;
      border: none;
      border-radius: 50px;
      padding: 12px 20px;
      cursor: pointer;
      box-shadow: 0 2px 8px rgba(0,0,0,0.2);
      z-index: 9999;
      font-size: 14px;
      font-weight: 500;
    `;

    document.body.appendChild(cmsToggle);
  }

  setupEventListeners() {
    // CMS toggle
    document.getElementById('bilingual-cms-toggle').addEventListener('click', () => {
      this.toggleCMSPanel();
    });

    // Language selector
    document.getElementById('cms-language-selector').addEventListener('change', (e) => {
      this.setCurrentLanguage(e.target.value);
    });

    // Save button
    document.getElementById('cms-save-btn').addEventListener('click', () => {
      this.saveContent();
    });

    // Preview button
    document.getElementById('cms-preview-btn').addEventListener('click', () => {
      this.previewContent();
    });

    // Close button
    document.getElementById('cms-close-btn').addEventListener('click', () => {
      this.toggleCMSPanel();
    });

    // Listen for language changes from the main language switcher
    document.addEventListener('languageChanged', (e) => {
      this.setCurrentLanguage(e.detail.language);
    });
  }

  toggleCMSPanel() {
    const panel = document.getElementById('bilingual-cms-panel');
    const isVisible = panel.style.display !== 'none';
    panel.style.display = isVisible ? 'none' : 'block';
    
    if (!isVisible) {
      this.loadCurrentPageContent();
    }
  }

  updateCMSInterface() {
    const languageSelector = document.getElementById('cms-language-selector');
    if (languageSelector) {
      languageSelector.value = this.currentLang;
    }
  }

  loadContentForCurrentLanguage() {
    // Update all translatable content on the page
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

    // Update page title and meta tags
    this.updatePageMetadata();
  }

  getTranslation(key) {
    // Get translation from the main translations file
    if (window.languageSwitcher && window.languageSwitcher.getTranslation) {
      return window.languageSwitcher.getTranslation(key);
    }
    
    // Fallback to localStorage cache
    const cachedTranslations = localStorage.getItem('cms-translations');
    if (cachedTranslations) {
      try {
        const translations = JSON.parse(cachedTranslations);
        const keys = key.split('.');
        let value = translations[this.currentLang];
        
        for (const k of keys) {
          if (value && value[k]) {
            value = value[k];
          } else {
            return key;
          }
        }
        
        return value;
      } catch (e) {
        console.error('Error parsing cached translations:', e);
      }
    }
    
    return key;
  }

  loadCurrentPageContent() {
    const currentPage = this.getCurrentPage();
    const pageTitle = document.querySelector('h1, .page-title')?.textContent || '';
    const pageContent = this.extractPageContent();

    document.getElementById('cms-page-title').value = pageTitle;
    document.getElementById('cms-page-content').value = pageContent;
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

  extractPageContent() {
    // Extract content from translatable elements
    const translatableElements = document.querySelectorAll('.translatable-content');
    let content = '';
    
    translatableElements.forEach(element => {
      const translationKey = element.getAttribute('data-translation-key');
      if (translationKey) {
        content += `[${translationKey}]\n${element.textContent}\n\n`;
      }
    });
    
    return content.trim();
  }

  saveContent() {
    const pageTitle = document.getElementById('cms-page-title').value;
    const pageContent = document.getElementById('cms-page-content').value;
    const currentPage = this.getCurrentPage();

    // Parse content and update translations
    const translations = this.parseContentToTranslations(pageContent);
    
    // Save to localStorage for now (in a real implementation, this would save to a database)
    this.saveTranslationsToCache(translations);
    
    // Update the page immediately
    this.applyTranslations(translations);
    
    // Show success message
    this.showMessage('Content saved successfully!', 'success');
  }

  parseContentToTranslations(content) {
    const translations = {};
    const lines = content.split('\n');
    let currentKey = null;
    let currentContent = '';

    for (const line of lines) {
      if (line.startsWith('[') && line.endsWith(']')) {
        // Save previous content
        if (currentKey && currentContent.trim()) {
          if (!translations[this.currentLang]) {
            translations[this.currentLang] = {};
          }
          this.setNestedValue(translations[this.currentLang], currentKey, currentContent.trim());
        }
        
        // Start new key
        currentKey = line.slice(1, -1);
        currentContent = '';
      } else if (currentKey) {
        currentContent += line + '\n';
      }
    }

    // Save last content
    if (currentKey && currentContent.trim()) {
      if (!translations[this.currentLang]) {
        translations[this.currentLang] = {};
      }
      this.setNestedValue(translations[this.currentLang], currentKey, currentContent.trim());
    }

    return translations;
  }

  setNestedValue(obj, path, value) {
    const keys = path.split('.');
    let current = obj;
    
    for (let i = 0; i < keys.length - 1; i++) {
      if (!current[keys[i]]) {
        current[keys[i]] = {};
      }
      current = current[keys[i]];
    }
    
    current[keys[keys.length - 1]] = value;
  }

  saveTranslationsToCache(translations) {
    const existingTranslations = localStorage.getItem('cms-translations');
    let allTranslations = {};
    
    if (existingTranslations) {
      try {
        allTranslations = JSON.parse(existingTranslations);
      } catch (e) {
        console.error('Error parsing existing translations:', e);
      }
    }
    
    // Merge new translations
    Object.assign(allTranslations, translations);
    
    localStorage.setItem('cms-translations', JSON.stringify(allTranslations));
  }

  applyTranslations(translations) {
    const translatableElements = document.querySelectorAll('.translatable-content');
    
    translatableElements.forEach(element => {
      const translationKey = element.getAttribute('data-translation-key');
      if (translationKey && translations[this.currentLang]) {
        const translation = this.getNestedValue(translations[this.currentLang], translationKey);
        if (translation) {
          element.textContent = translation;
        }
      }
    });
  }

  getNestedValue(obj, path) {
    const keys = path.split('.');
    let current = obj;
    
    for (const key of keys) {
      if (current && current[key] !== undefined) {
        current = current[key];
      } else {
        return null;
      }
    }
    
    return current;
  }

  previewContent() {
    const pageContent = document.getElementById('cms-page-content').value;
    const translations = this.parseContentToTranslations(pageContent);
    
    // Apply translations temporarily
    this.applyTranslations(translations);
    
    this.showMessage('Preview applied! Refresh to revert.', 'info');
  }

  updatePageMetadata() {
    // Update page title if it has a translation key
    const pageTitle = document.querySelector('h1, .page-title');
    if (pageTitle && pageTitle.getAttribute('data-translation-key')) {
      const translation = this.getTranslation(pageTitle.getAttribute('data-translation-key'));
      if (translation) {
        pageTitle.textContent = translation;
      }
    }

    // Update meta description if available
    const metaDescription = document.querySelector('meta[name="description"]');
    if (metaDescription && metaDescription.getAttribute('data-translation-key')) {
      const translation = this.getTranslation(metaDescription.getAttribute('data-translation-key'));
      if (translation) {
        metaDescription.setAttribute('content', translation);
      }
    }
  }

  showMessage(message, type = 'info') {
    const messageDiv = document.createElement('div');
    messageDiv.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      padding: 12px 20px;
      border-radius: 4px;
      color: white;
      z-index: 10001;
      font-weight: 500;
    `;

    switch (type) {
      case 'success':
        messageDiv.style.background = '#28a745';
        break;
      case 'error':
        messageDiv.style.background = '#dc3545';
        break;
      case 'warning':
        messageDiv.style.background = '#ffc107';
        messageDiv.style.color = '#212529';
        break;
      default:
        messageDiv.style.background = '#17a2b8';
    }

    messageDiv.textContent = message;
    document.body.appendChild(messageDiv);

    setTimeout(() => {
      if (document.body.contains(messageDiv)) {
        document.body.removeChild(messageDiv);
      }
    }, 3000);
  }
}

// Initialize bilingual CMS when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  // Wait for language switcher to be ready
  setTimeout(() => {
    window.bilingualCMS = new BilingualCMS();
  }, 1000);
});

// Export for use in other scripts
window.BilingualCMS = BilingualCMS; 