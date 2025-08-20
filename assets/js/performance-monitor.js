/**
 * Performance Monitor for AG Computational Arithmetic Geometry
 * Monitors loading performance and reports issues under high load
 */

(function() {
  'use strict';

  // Configuration
  const CONFIG = {
    slowLoadThreshold: 2000, // 2 seconds
    verySlowLoadThreshold: 5000, // 5 seconds
    sampleSize: 10, // Number of page loads to track
    reportInterval: 300000 // Report every 5 minutes
  };

  // State management
  const state = {
    loadTimes: [],
    resourceTimes: new Map(),
    lastReport: Date.now(),
    isHighLoad: false
  };

  // Initialize performance monitoring
  function initPerformanceMonitoring() {
    // Monitor page load performance
    window.addEventListener('load', function() {
      const loadTime = performance.now();
      state.loadTimes.push(loadTime);

      // Keep only recent samples
      if (state.loadTimes.length > CONFIG.sampleSize) {
        state.loadTimes.shift();
      }

      // Check for slow loading
      if (loadTime > CONFIG.slowLoadThreshold) {
        console.warn('⚠️ Slow page load detected:', Math.round(loadTime) + 'ms');
      }

      if (loadTime > CONFIG.verySlowLoadThreshold) {
        console.error('🚨 Very slow page load detected:', Math.round(loadTime) + 'ms');
        reportSlowLoad(loadTime);
      }
    });

    // Monitor resource loading performance
    if (performance.getEntriesByType) {
      // Wait for resources to load
      setTimeout(analyzeResourcePerformance, 1000);
    }

    // Periodic reporting
    setInterval(generatePerformanceReport, CONFIG.reportInterval);
  }

  // Analyze resource loading performance
  function analyzeResourcePerformance() {
    const resources = performance.getEntriesByType('resource');
    const unpkgResources = resources.filter(r => r.name.includes('unpkg.com'));

    unpkgResources.forEach(resource => {
      const url = resource.name;
      const loadTime = resource.duration;

      if (!state.resourceTimes.has(url)) {
        state.resourceTimes.set(url, []);
      }

      const times = state.resourceTimes.get(url);
      times.push(loadTime);

      // Keep only recent samples
      if (times.length > CONFIG.sampleSize) {
        times.shift();
      }

      // Check for slow external resources
      if (loadTime > CONFIG.slowLoadThreshold) {
        console.warn('⚠️ Slow external resource:', url, Math.round(loadTime) + 'ms');
      }
    });

    // Check for high load conditions
    checkHighLoadConditions();
  }

  // Check for high load conditions
  function checkHighLoadConditions() {
    const recentLoads = state.loadTimes.slice(-5); // Last 5 loads
    const avgLoadTime = recentLoads.reduce((a, b) => a + b, 0) / recentLoads.length;

    const slowResources = Array.from(state.resourceTimes.values())
      .flat()
      .filter(time => time > CONFIG.slowLoadThreshold);

    const slowResourceRatio = slowResources.length / Math.max(1, Array.from(state.resourceTimes.values()).flat().length);

    // Detect high load condition
    if (avgLoadTime > CONFIG.slowLoadThreshold && slowResourceRatio > 0.3) {
      if (!state.isHighLoad) {
        state.isHighLoad = true;
        console.warn('🚨 High load condition detected! Consider switching to self-hosted resources.');
        suggestOptimizations(avgLoadTime, slowResourceRatio);
      }
    } else {
      state.isHighLoad = false;
    }
  }

  // Report slow load issues
  function reportSlowLoad(loadTime) {
    const report = {
      timestamp: new Date().toISOString(),
      loadTime: Math.round(loadTime),
      url: window.location.href,
      userAgent: navigator.userAgent,
      connection: navigator.connection ? {
        effectiveType: navigator.connection.effectiveType,
        downlink: navigator.connection.downlink
      } : null
    };

    // In production, you might want to send this to your analytics service
    console.log('Performance Report:', report);

    // Store in localStorage for debugging
    const reports = JSON.parse(localStorage.getItem('performanceReports') || '[]');
    reports.push(report);
    localStorage.setItem('performanceReports', JSON.stringify(reports.slice(-50))); // Keep last 50 reports
  }

  // Generate performance report
  function generatePerformanceReport() {
    const avgLoadTime = state.loadTimes.reduce((a, b) => a + b, 0) / Math.max(1, state.loadTimes.length);

    const resourceStats = {};
    state.resourceTimes.forEach((times, url) => {
      const avgTime = times.reduce((a, b) => a + b, 0) / times.length;
      resourceStats[url] = {
        avgTime: Math.round(avgTime),
        samples: times.length,
        maxTime: Math.max(...times),
        minTime: Math.min(...times)
      };
    });

    const report = {
      timestamp: new Date().toISOString(),
      averageLoadTime: Math.round(avgLoadTime),
      sampleCount: state.loadTimes.length,
      isHighLoad: state.isHighLoad,
      resourceStats: resourceStats
    };

    console.log('Performance Summary:', report);
    return report;
  }

  // Suggest optimizations based on current performance
  function suggestOptimizations(avgLoadTime, slowResourceRatio) {
    const suggestions = [];

    if (avgLoadTime > CONFIG.verySlowLoadThreshold) {
      suggestions.push('🚨 CRITICAL: Page loads are very slow. Consider immediate action!');
    }

    if (slowResourceRatio > 0.5) {
      suggestions.push('📦 HIGH PRIORITY: Switch to self-hosted Lunr.js to reduce external dependencies');
    }

    if (slowResourceRatio > 0.3) {
      suggestions.push('🔄 MEDIUM PRIORITY: Consider using a different CDN or self-hosting critical resources');
    }

    if (navigator.connection && navigator.connection.effectiveType === 'slow-2g') {
      suggestions.push('📶 Consider optimizing for slow connections - reduce external resources');
    }

    suggestions.push('📊 Check browser developer tools Network tab for detailed resource timing');
    suggestions.push('🌐 Consider implementing resource hints (preload, preconnect) for critical resources');

    console.group('🚀 Performance Optimization Suggestions:');
    suggestions.forEach(suggestion => console.log('  • ' + suggestion));
    console.groupEnd();
  }

  // Expose monitoring API
  window.PerformanceMonitor = {
    getReport: generatePerformanceReport,
    isHighLoad: () => state.isHighLoad,
    getReports: () => JSON.parse(localStorage.getItem('performanceReports') || '[]'),
    clearReports: () => localStorage.removeItem('performanceReports')
  };

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initPerformanceMonitoring);
  } else {
    initPerformanceMonitoring();
  }

})();
