/**
 * Teaching Page Interactive Functionality
 * Handles filtering and animations
 */

document.addEventListener('DOMContentLoaded', function() {
  // Initialize all interactive features
  initFilters();
  initAnimations();
  initSmoothScrolling();
});

/**
 * Initialize filtering functionality
 */
function initFilters() {
  const courseTypeFilter = document.getElementById('courseTypeFilter');
  const timeFilter = document.getElementById('timeFilter');
  const searchFilter = document.getElementById('searchFilter');
  const courseItems = document.querySelectorAll('.course-item');
  const semesterGroups = document.querySelectorAll('.semester-group');

  if (!courseTypeFilter || !timeFilter || !searchFilter) return;

  function applyFilters() {
    const selectedType = courseTypeFilter.value;
    const selectedPeriod = timeFilter.value;
    const searchTerm = searchFilter.value.toLowerCase();

    let visibleCount = 0;

    courseItems.forEach(item => {
      const type = item.dataset.type;
      const period = item.dataset.period;
      const title = item.querySelector('.course-link')?.textContent.toLowerCase() || '';
      
      const typeMatch = selectedType === 'all' || type === selectedType;
      const periodMatch = selectedPeriod === 'all' || period === selectedPeriod;
      const searchMatch = searchTerm === '' || title.includes(searchTerm);
      
      if (typeMatch && periodMatch && searchMatch) {
        item.classList.remove('hidden');
        visibleCount++;
      } else {
        item.classList.add('hidden');
      }
    });

    // Hide empty semester groups and show/hide section headers
    semesterGroups.forEach(group => {
      const visibleItems = group.querySelectorAll('.course-item:not(.hidden)');
      if (visibleItems.length === 0) {
        group.classList.add('hidden');
      } else {
        group.classList.remove('hidden');
      }
    });

    // Update filter status
    updateFilterStatus(visibleCount, courseItems.length);
  }

  // Event listeners for filters
  courseTypeFilter.addEventListener('change', applyFilters);
  timeFilter.addEventListener('change', applyFilters);
  searchFilter.addEventListener('input', debounce(applyFilters, 300));

  // Initialize filters
  applyFilters();
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
        <i class="fas fa-filter"></i>
        Showing ${visibleCount} of ${totalCount} courses
        <button class="clear-filters" onclick="clearAllFilters()">
          <i class="fas fa-times"></i> Clear filters
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

  if (courseTypeFilter) courseTypeFilter.value = 'all';
  if (timeFilter) timeFilter.value = 'all';
  if (searchFilter) searchFilter.value = '';

  // Trigger filter update
  const event = new Event('change');
  courseTypeFilter?.dispatchEvent(event);
}

/**
 * Initialize animations
 */
function initAnimations() {
  // Intersection Observer for fade-in animations
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
      }
    });
  }, observerOptions);

  // Observe course items for animation
  document.querySelectorAll('.course-item').forEach(item => {
    observer.observe(item);
  });
}

/**
 * Initialize smooth scrolling for anchor links
 */
function initSmoothScrolling() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
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

/**
 * Add keyboard navigation support
 */
function initKeyboardNavigation() {
  document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + F to focus search
    if ((e.ctrlKey || e.metaKey) && e.key === 'f') {
      e.preventDefault();
      const searchInput = document.getElementById('searchFilter');
      if (searchInput) {
        searchInput.focus();
      }
    }

    // Escape to clear search
    if (e.key === 'Escape') {
      const searchInput = document.getElementById('searchFilter');
      if (searchInput && document.activeElement === searchInput) {
        searchInput.value = '';
        searchInput.dispatchEvent(new Event('input'));
      }
    }
  });
}

/**
 * Add tooltips for course badges
 */
function initTooltips() {
  const badges = document.querySelectorAll('.course-badge');
  
  badges.forEach(badge => {
    const type = badge.classList.contains('seminar') ? 'Seminar' :
                 badge.classList.contains('vorlesung') ? 'Lecture' :
                 badge.classList.contains('proseminar') ? 'Proseminar' :
                 badge.classList.contains('hauptseminar') ? 'Hauptseminar' : 'Course';
    
    badge.title = `${type} - Click to filter by this type`;
    
    badge.addEventListener('click', function() {
      const courseTypeFilter = document.getElementById('courseTypeFilter');
      if (courseTypeFilter) {
        courseTypeFilter.value = this.dataset.type || 'all';
        courseTypeFilter.dispatchEvent(new Event('change'));
      }
    });
  });
}

/**
 * Add export functionality
 */
function initExport() {
  const exportButton = document.createElement('button');
  exportButton.className = 'export-button';
  exportButton.innerHTML = '<i class="fas fa-download"></i> Export Course List';
  exportButton.onclick = exportCourseList;
  
  const filterControls = document.querySelector('.filter-controls');
  if (filterControls) {
    filterControls.appendChild(exportButton);
  }
}

/**
 * Export course list to CSV
 */
function exportCourseList() {
  const courseItems = document.querySelectorAll('.course-item:not(.hidden)');
  let csvContent = 'data:text/csv;charset=utf-8,';
  csvContent += 'Semester,Type,Course Title,Instructors\n';
  
  courseItems.forEach(item => {
    const semester = item.closest('.semester-group')?.querySelector('.semester-title')?.textContent.trim() || '';
    const type = item.querySelector('.course-badge')?.textContent.trim() || '';
    const title = item.querySelector('.course-link')?.textContent.trim() || '';
    const instructors = item.querySelector('.instructors')?.textContent.trim() || '';
    
    csvContent += `"${semester}","${type}","${title}","${instructors}"\n`;
  });
  
  const encodedUri = encodeURI(csvContent);
  const link = document.createElement('a');
  link.setAttribute('href', encodedUri);
  link.setAttribute('download', 'teaching_courses.csv');
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

// Initialize additional features
document.addEventListener('DOMContentLoaded', function() {
  initKeyboardNavigation();
  initTooltips();
  initExport();
});

// Note: CSS styles are now handled in the main teaching-page.scss file
// to ensure proper theme integration 