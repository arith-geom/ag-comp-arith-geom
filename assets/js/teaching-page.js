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
  // Removed semester-wide collapsing per request; only per-course expansion remains
  initCourseExpanders();
  initCourseFocusMode();
});

/**
 * Initialize and update statistics
 */
function initStatistics() {
  const courseItems = document.querySelectorAll('.course-item');
  const currentCourses = document.querySelectorAll('.course-item[data-period="current"]');
  
  // Update statistics
  const totalEl = document.getElementById('totalCourses');
  const currentEl = document.getElementById('currentCourses');
  if (totalEl) totalEl.textContent = courseItems.length;
  if (currentEl) currentEl.textContent = currentCourses.length;
  
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
  const filterControls = document.querySelector('.filter-controls');
  const semesterFilterBar = document.getElementById('semesterFilterBar');

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
      const titleEl = item.querySelector('.course-link, .course-title-btn, .course-title');
      const title = titleEl ? titleEl.textContent.toLowerCase() : '';
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

    // Reset focus mode when filters change
    document.querySelectorAll('.course-item.focus-hidden, .semester-group.focus-hidden').forEach(el => el.classList.remove('focus-hidden'));
    const focusBar = document.getElementById('courseFocusBar');
    if (focusBar) focusBar.style.display = 'none';
    const fc = document.querySelector('.filter-controls');
    if (fc) fc.style.display = '';

    // Update statistics (filter status UI removed)
    updateStatistics(visibleCount, currentCount);
  }

  // Event listeners for filters
  courseTypeFilter.addEventListener('change', applyFilters);
  if (timeFilter) timeFilter.addEventListener('change', applyFilters);
  if (yearFilter) yearFilter.addEventListener('change', applyFilters);
  searchFilter.addEventListener('input', debounce(applyFilters, 300));

  // Initialize filters
  applyFilters();

  // Apply initial filters from URL query parameters (q, type, year)
  try {
    const params = new URLSearchParams(window.location.search);
    const qParam = params.get('q');
    const typeParam = params.get('type');
    const yearParam = params.get('year');

    let needsApply = false;
    if (qParam) {
      searchFilter.value = qParam;
      needsApply = true;
    }
    if (typeParam && courseTypeFilter.querySelector(`option[value="${typeParam}"]`)) {
      courseTypeFilter.value = typeParam;
      needsApply = true;
    }
    if (yearParam && yearFilter && yearFilter.querySelector(`option[value="${yearParam}"]`)) {
      yearFilter.value = yearParam;
      needsApply = true;
    }
    if (needsApply) {
      applyFilters();
      // Scroll into view for better UX
      document.querySelector('.teaching-page')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  } catch (_) {}

  // Expose helpers for semester filter UI
  window.__teachingFilters = {
    showSemesterBar: function(show) {
      if (semesterFilterBar) semesterFilterBar.style.display = show ? 'block' : 'none';
      if (filterControls) filterControls.style.display = show ? 'none' : '';
    },
    clearAll: function() {
      if (courseTypeFilter) courseTypeFilter.value = 'all';
      if (timeFilter) timeFilter.value = 'all';
      if (yearFilter) yearFilter.value = 'all';
      if (searchFilter) searchFilter.value = '';
      applyFilters();
    }
  };
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
        if (timeFilter) timeFilter.value = 'all';
      } else if (filter === 'current') {
        courseTypeFilter.value = 'all';
        if (timeFilter) timeFilter.value = 'current';
      } else {
        courseTypeFilter.value = filter;
        if (timeFilter) timeFilter.value = 'all';
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
// Removed filter status UI per request

/**
 * Clear all filters
 */
function clearAllFilters() {
  const courseTypeFilter = document.getElementById('courseTypeFilter');
  const timeFilter = document.getElementById('timeFilter');
  const yearFilter = document.getElementById('yearFilter');
  const searchFilter = document.getElementById('searchFilter');
  const quickFilterBtns = document.querySelectorAll('.quick-filter-btn');
  const semesterFilterBar = document.getElementById('semesterFilterBar');
  const filterControls = document.querySelector('.filter-controls');

  // Reset filters
  courseTypeFilter.value = 'all';
  if (timeFilter) timeFilter.value = 'all';
  if (yearFilter) yearFilter.value = 'all';
  searchFilter.value = '';

  // Reset quick filter buttons
  if (quickFilterBtns.length > 0) {
    quickFilterBtns.forEach(btn => btn.classList.remove('active'));
    quickFilterBtns[0].classList.add('active'); // "All" button
  }

  // Trigger filter update
  courseTypeFilter.dispatchEvent(new Event('change'));

  // Restore default UI bars
  if (semesterFilterBar) semesterFilterBar.style.display = 'none';
  if (filterControls) filterControls.style.display = '';
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

/**
 * Semester header click-to-filter (collapse other semesters and show Back to all)
 */
/**
 * Expandable per-course details
 */
function initCourseExpanders() {
  // Chevron is a visual indicator only; no interactive listeners here.
}

/**
 * Make the whole course card clickable to expand and enter focus mode
 */
function initCourseFocusMode() {
  const courseItems = document.querySelectorAll('.course-item');
  const groups = document.querySelectorAll('.semester-group');
  const backBtn = document.getElementById('backToAllCourses');
  const focusBar = document.getElementById('courseFocusBar');
  const filterControls = document.querySelector('.filter-controls');
  let focusedItem = null;
  let previousScrollY = null;

  function enterFocus(li) {
    if (previousScrollY === null) {
      previousScrollY = window.pageYOffset || document.documentElement.scrollTop || 0;
    }
    // Expand selected card
    const toggleBtn = li.querySelector('.course-expand-btn');
    const details = li.querySelector('.course-details');
    if (toggleBtn) {
      toggleBtn.setAttribute('aria-expanded', 'true');
      toggleBtn.innerHTML = '<i class="fas fa-chevron-up"></i>';
    }
    if (details) details.style.display = 'block';
    // Scroll the page to the very top so the user sees the full content area
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        try {
          window.scrollTo({ top: 0, behavior: 'smooth' });
        } catch (_) {}
      });
    });
    // Hide all other cards within each group
    courseItems.forEach(item => {
      if (item !== li) item.classList.add('focus-hidden');
    });
    // Hide empty groups
    groups.forEach(group => {
      const anyVisible = group.querySelector('.course-item:not(.focus-hidden)');
      if (!anyVisible) group.classList.add('focus-hidden');
    });
    if (focusBar) focusBar.style.display = 'block';
    if (filterControls) filterControls.style.display = 'none';
    focusedItem = li;
  }

  function exitFocus() {
    courseItems.forEach(item => item.classList.remove('focus-hidden'));
    groups.forEach(group => group.classList.remove('focus-hidden'));
    if (focusBar) focusBar.style.display = 'none';
    if (filterControls) filterControls.style.display = '';
    // Collapse details of previously focused item
    if (focusedItem) {
      const toggleBtn = focusedItem.querySelector('.course-expand-btn');
      const details = focusedItem.querySelector('.course-details');
      if (toggleBtn && details && details.style.display !== 'none') {
        toggleBtn.setAttribute('aria-expanded', 'false');
        details.style.display = 'none';
        toggleBtn.innerHTML = '<i class="fas fa-chevron-down"></i>';
      }
    }
    focusedItem = null;
    // Restore previous scroll position (to where the user was before focusing)
    if (previousScrollY !== null) {
      try {
        window.scrollTo({ top: previousScrollY, behavior: 'smooth' });
      } catch (_) {}
      previousScrollY = null;
    }
  }

  // Expose for use in other handlers
  window.__teachingExitFocus = exitFocus;

  courseItems.forEach(li => {
    li.addEventListener('click', (e) => {
      // Allow clicks on links to proceed without toggling (e.g. external_url)
      const target = e.target;
      const isLink = target.closest && target.closest('a');
      const isExpandBtn = target.closest && target.closest('.course-expand-btn');
      if (isLink) return;
      // Toggle: if this is already focused, exit focus; otherwise enter focus
      if (focusedItem && focusedItem === li) {
        exitFocus();
      } else {
        enterFocus(li);
      }
      // If chevron specifically was clicked, we already handled inside its listener
    });
  });

  if (backBtn) backBtn.addEventListener('click', exitFocus);
}