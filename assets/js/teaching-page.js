/**
 * Simple Teaching Page Interactive Functionality
 * Handles filtering, statistics, and user interactions
 */

document.addEventListener('DOMContentLoaded', function() {
  // Initialize all interactive features
  initStatistics();
  initFilters();
  initQuickFilters();
  initKeyboardNavigation();
});

/**
 * Initialize and update statistics
 */
function initStatistics() {
  const courseItems = document.querySelectorAll('.course-item');
  const currentCourses = document.querySelectorAll('.course-item[data-period="current"]');
  
  // Update statistics
  document.getElementById('totalCourses').textContent = courseItems.length;
  document.getElementById('currentCourses').textContent = currentCourses.length;
  
  // Animate statistics on load
  animateStatistics();
}

function animateStatistics() {
  const statNumbers = document.querySelectorAll('.stat-number');
  
  statNumbers.forEach(stat => {
    const finalValue = stat.textContent;
    const isNumber = !isNaN(parseInt(finalValue));
    
    if (isNumber) {
      const target = parseInt(finalValue);
      let current = 0;
      const increment = target / 20;
      
      const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
          current = target;
          clearInterval(timer);
        }
        stat.textContent = Math.floor(current);
      }, 50);
    }
  });
}

/**
 * Initialize enhanced filtering functionality
 */
function initFilters() {
  const courseTypeFilter = document.getElementById('courseTypeFilter');
  const timeFilter = document.getElementById('timeFilter');
  const yearFilter = document.getElementById('yearFilter');
  const searchFilter = document.getElementById('searchFilter');
  const courseItems = document.querySelectorAll('.course-item');
  const semesterGroups = document.querySelectorAll('.semester-group');

  if (!courseTypeFilter || (!timeFilter && !yearFilter) || !searchFilter) return;

  function applyFilters() {
    const selectedType = courseTypeFilter.value;
    const selectedPeriod = timeFilter ? timeFilter.value : 'all';
    const selectedYear = yearFilter ? yearFilter.value : 'all';
    const searchTerm = searchFilter.value.toLowerCase();

    let visibleCount = 0;
    let currentCount = 0;

    courseItems.forEach(item => {
      const type = item.dataset.type;
      const period = item.dataset.period;
      const year = item.dataset.year;
      const title = item.querySelector('.course-link')?.textContent.toLowerCase() || '';
      const instructors = item.querySelector('.instructors')?.textContent.toLowerCase() || '';
      
      const typeMatch = selectedType === 'all' || type === selectedType;
      const periodMatch = selectedPeriod === 'all' || period === selectedPeriod;
      const yearMatch = selectedYear === 'all' || (year && year === selectedYear);
      const searchMatch = searchTerm === '' || 
                         title.includes(searchTerm) || 
                         instructors.includes(searchTerm);
      
      if (typeMatch && periodMatch && yearMatch && searchMatch) {
        item.classList.remove('hidden');
        visibleCount++;
        if (period === 'current') currentCount++;
      } else {
        item.classList.add('hidden');
      }
    });

    // Hide empty semester groups
    semesterGroups.forEach(group => {
      const visibleItems = group.querySelectorAll('.course-item:not(.hidden)');
      if (visibleItems.length === 0) {
        group.classList.add('hidden');
      } else {
        group.classList.remove('hidden');
      }
    });

    // Update statistics
    updateStatistics(visibleCount, currentCount);
    
    // Update filter status
    updateFilterStatus(visibleCount, courseItems.length);
  }

  // Event listeners for filters
  courseTypeFilter.addEventListener('change', applyFilters);
  if (timeFilter) timeFilter.addEventListener('change', applyFilters);
  if (yearFilter) yearFilter.addEventListener('change', applyFilters);
  searchFilter.addEventListener('input', debounce(applyFilters, 300));

  // Initialize filters
  applyFilters();
}

/**
 * Initialize quick filter buttons
 */
function initQuickFilters() {
  const quickFilterBtns = document.querySelectorAll('.quick-filter-btn');
  const courseTypeFilter = document.getElementById('courseTypeFilter');
  const timeFilter = document.getElementById('timeFilter');

  quickFilterBtns.forEach(btn => {
    btn.addEventListener('click', function() {
      const filter = this.dataset.filter;
      
      // Update active state
      quickFilterBtns.forEach(b => b.classList.remove('active'));
      this.classList.add('active');
      
      // Apply filter
      if (filter === 'all') {
        courseTypeFilter.value = 'all';
        timeFilter.value = 'all';
      } else if (filter === 'current') {
        courseTypeFilter.value = 'all';
        timeFilter.value = 'current';
      } else {
        courseTypeFilter.value = filter;
        timeFilter.value = 'all';
      }
      
      // Trigger filter change
      courseTypeFilter.dispatchEvent(new Event('change'));
    });
  });
}

/**
 * Update statistics display
 */
function updateStatistics(visibleCount, currentCount) {
  const totalCoursesEl = document.getElementById('totalCourses');
  const currentCoursesEl = document.getElementById('currentCourses');
  
  if (totalCoursesEl) totalCoursesEl.textContent = visibleCount;
  if (currentCoursesEl) currentCoursesEl.textContent = currentCount;
}

/**
 * Update filter status display
 */
function updateFilterStatus(visibleCount, totalCount) {
  let statusElement = document.getElementById('filterStatus');
  
  if (!statusElement) {
    statusElement = document.createElement('div');
    statusElement.id = 'filterStatus';
    statusElement.className = 'filter-status';
    const filterControls = document.querySelector('.filter-controls');
    if (filterControls) {
      filterControls.appendChild(statusElement);
    }
  }

  if (visibleCount === totalCount) {
    statusElement.style.display = 'none';
  } else {
    statusElement.style.display = 'block';
    statusElement.innerHTML = `
      <div class="status-message">
        Showing ${visibleCount} of ${totalCount} courses
        <button class="clear-filters" onclick="clearAllFilters()">
          Clear filters
        </button>
      </div>
    `;
  }
}

/**
 * Clear all filters
 */
function clearAllFilters() {
  const courseTypeFilter = document.getElementById('courseTypeFilter');
  const timeFilter = document.getElementById('timeFilter');
  const searchFilter = document.getElementById('searchFilter');
  const quickFilterBtns = document.querySelectorAll('.quick-filter-btn');

  // Reset filters
  courseTypeFilter.value = 'all';
  timeFilter.value = 'all';
  searchFilter.value = '';

  // Reset quick filter buttons
  quickFilterBtns.forEach(btn => btn.classList.remove('active'));
  quickFilterBtns[0].classList.add('active'); // "All" button

  // Trigger filter update
  courseTypeFilter.dispatchEvent(new Event('change'));
}

/**
 * Initialize keyboard navigation
 */
function initKeyboardNavigation() {
  document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + F to focus search
    if ((e.ctrlKey || e.metaKey) && e.key === 'f') {
      e.preventDefault();
      const searchFilter = document.getElementById('searchFilter');
      if (searchFilter) {
        searchFilter.focus();
        searchFilter.select();
      }
    }
    
    // Escape to clear filters
    if (e.key === 'Escape') {
      clearAllFilters();
    }
  });
}

/**
 * Debounce function for search input
 */
function debounce(func, wait) {
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

// Global functions for HTML onclick handlers
window.clearAllFilters = clearAllFilters; 