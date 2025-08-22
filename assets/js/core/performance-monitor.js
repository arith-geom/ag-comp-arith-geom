// Performance Monitor
// Monitor site performance and report issues under high load

(function() {
  'use strict';

  // Performance monitoring for high-load scenarios
  const PerformanceMonitor = {
    init: function() {
      this.startTime = performance.now();
      this.measurePageLoad();
      this.monitorMemoryUsage();
      console.log('Performance monitor initialized');
    },

    measurePageLoad: function() {
      window.addEventListener('load', () => {
        const loadTime = performance.now() - this.startTime;
        console.log(`Page loaded in ${loadTime.toFixed(2)}ms`);

        // Report slow loads
        if (loadTime > 3000) {
          console.warn('Slow page load detected:', loadTime.toFixed(2) + 'ms');
        }
      });
    },

    monitorMemoryUsage: function() {
      // Check memory usage if available (Chrome/Edge)
      if (performance.memory) {
        setInterval(() => {
          const memory = performance.memory;
          const usedPercent = (memory.usedJSHeapSize / memory.totalJSHeapSize * 100);

          if (usedPercent > 80) {
            console.warn('High memory usage detected:', usedPercent.toFixed(1) + '%');
          }
        }, 10000); // Check every 10 seconds
      }
    }
  };

  // Initialize when DOM is ready
  document.addEventListener('DOMContentLoaded', function() {
    PerformanceMonitor.init();
  });

})();