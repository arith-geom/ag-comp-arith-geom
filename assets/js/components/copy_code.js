// Copy code functionality
// Add copy to clipboard functionality for code blocks

(function() {
  'use strict';

  const CopyCodeHandler = {
    init: function() {
      // Find all code blocks and add copy buttons
      document.querySelectorAll('pre code').forEach(function(codeBlock) {
        const pre = codeBlock.parentNode;
        const copyButton = document.createElement('button');
        copyButton.className = 'copy-code-btn';
        copyButton.textContent = 'Copy';
        copyButton.title = 'Copy to clipboard';

        copyButton.addEventListener('click', function() {
          navigator.clipboard.writeText(codeBlock.textContent).then(function() {
            copyButton.textContent = 'Copied!';
            setTimeout(function() {
              copyButton.textContent = 'Copy';
            }, 2000);
          });
        });

        pre.style.position = 'relative';
        pre.appendChild(copyButton);
      });

      console.log('Copy code functionality initialized');
    }
  };

  document.addEventListener('DOMContentLoaded', function() {
    CopyCodeHandler.init();
  });

})();
