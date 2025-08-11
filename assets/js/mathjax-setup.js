// MathJax Configuration and Setup
(function() {
  'use strict';

  // Wait for MathJax to be available
  function waitForMathJax() {
    if (typeof MathJax !== 'undefined') {
      // Configure MathJax
      MathJax = {
        tex: {
          inlineMath: [['$', '$'], ['\\(', '\\)']],
          displayMath: [['$$', '$$'], ['\\[', '\\]']],
          processEscapes: true,
          processEnvironments: true,
          packages: ['base', 'ams', 'noerrors', 'noundefined']
        },
        options: {
          ignoreHtmlClass: 'tex2jax_ignore',
          processHtmlClass: 'tex2jax_process',
          skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre']
        },
        startup: {
          pageReady: function() {
            // Reprocess math when content is dynamically loaded
            if (typeof MathJax !== 'undefined' && MathJax.typesetPromise) {
              MathJax.typesetPromise();
            }
          }
        }
      };

      // Function to reprocess math in specific elements
      window.reprocessMath = function(element) {
        if (typeof MathJax !== 'undefined' && MathJax.typesetPromise) {
          return MathJax.typesetPromise([element]);
        }
      };

      console.log('✅ MathJax configured successfully');
    } else {
      // Retry after a short delay
      setTimeout(waitForMathJax, 100);
    }
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', waitForMathJax);
  } else {
    waitForMathJax();
  }

  // Also try to reprocess math when content is dynamically loaded
  document.addEventListener('DOMContentLoaded', function() {
    // Reprocess math after a short delay to ensure all content is loaded
    setTimeout(function() {
      if (typeof MathJax !== 'undefined' && MathJax.typesetPromise) {
        MathJax.typesetPromise();
      }
    }, 500);
  });

  // Observer for dynamically loaded content
  if (typeof MutationObserver !== 'undefined') {
    const observer = new MutationObserver(function(mutations) {
      let shouldReprocess = false;
      mutations.forEach(function(mutation) {
        if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
          // Check if any added nodes contain math content
          mutation.addedNodes.forEach(function(node) {
            if (node.nodeType === Node.ELEMENT_NODE) {
              const text = node.textContent || '';
              if (text.includes('$') || text.includes('\\(') || text.includes('\\[')) {
                shouldReprocess = true;
              }
            }
          });
        }
      });
      
      if (shouldReprocess && typeof MathJax !== 'undefined' && MathJax.typesetPromise) {
        setTimeout(function() {
          MathJax.typesetPromise();
        }, 100);
      }
    });

    // Start observing when DOM is ready
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', function() {
        observer.observe(document.body, {
          childList: true,
          subtree: true
        });
      });
    } else {
      observer.observe(document.body, {
        childList: true,
        subtree: true
      });
    }
  }
})(); 