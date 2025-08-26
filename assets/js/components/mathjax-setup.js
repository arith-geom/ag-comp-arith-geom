// MathJax Setup
// Configure MathJax for LaTeX rendering

if (typeof MathJax !== 'undefined') {
  MathJax.config = {
    tex: {
      inlineMath: [['$', '$'], ['\\(', '\\)']],
      displayMath: [['$$', '$$'], ['\\[', '\\]']],
      processEscapes: true,
      processEnvironments: true
    },
    options: {
      ignoreHtmlClass: 'tex2jax_ignore',
      processHtmlClass: 'tex2jax_process'
    }
  };

  MathJax.startup = {
    ready: function() {
      MathJax.startup.defaultReady();
      console.log('MathJax configured successfully');
    }
  };
} else {
  console.log('MathJax not loaded');
}