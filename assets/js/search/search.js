// Search functionality
// Handle search interface and interactions

(function() {
  'use strict';

  const SearchHandler = {
    init: function() {
      this.searchInput = document.getElementById('search-input');
      this.searchResults = document.getElementById('search-results');

      if (this.searchInput) {
        this.bindEvents();
        console.log('Search handler initialized');
      }
    },

    bindEvents: function() {
      this.searchInput.addEventListener('input', this.debounce(this.handleSearch.bind(this), 300));
      this.searchInput.addEventListener('focus', this.showResults.bind(this));
      this.searchInput.addEventListener('blur', this.hideResults.bind(this));
    },

    handleSearch: function(event) {
      const query = event.target.value.trim();

      if (query.length < 2) {
        this.clearResults();
        return;
      }

      // Implement search logic here
      console.log('Searching for:', query);
      // This would typically make an AJAX request to search endpoint
    },

    showResults: function() {
      if (this.searchResults) {
        this.searchResults.style.display = 'block';
      }
    },

    hideResults: function() {
      // Delay hiding to allow clicking on results
      setTimeout(() => {
        if (this.searchResults) {
          this.searchResults.style.display = 'none';
        }
      }, 200);
    },

    clearResults: function() {
      if (this.searchResults) {
        this.searchResults.innerHTML = '';
      }
    },

    debounce: function(func, wait) {
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
  };

  // Initialize when DOM is ready
  document.addEventListener('DOMContentLoaded', function() {
    SearchHandler.init();
  });

})();