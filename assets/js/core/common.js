// Common JavaScript functions
// This file contains shared functionality used across the site

(function() {
  'use strict';

  // Utility function to check if element exists
  function elementExists(selector) {
    return document.querySelector(selector) !== null;
  }

  // Safe event listener attachment
  function addEventListenerIfExists(selector, event, handler) {
    const element = document.querySelector(selector);
    if (element) {
      element.addEventListener(event, handler);
    }
  }

  // Initialize common functionality when DOM is ready
  document.addEventListener('DOMContentLoaded', function() {
    console.log('Common JS loaded');

    // Add any common functionality here
    // For example, smooth scrolling, accessibility improvements, etc.
  });

  // Expose utility functions to global scope
  window.CommonUtils = {
    elementExists: elementExists,
    addEventListenerIfExists: addEventListenerIfExists
  };

})();