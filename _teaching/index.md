---
---
layout: page
title: Teaching
permalink: "/teaching/"
scripts:
- "/assets/js/teaching-page.js"
active: false
---







<div class="teaching-page">
  <!-- Filter Controls -->
  <div class="filter-controls">
    <div class="filter-group">
      <label for="courseTypeFilter">Filter by Type:</label>
      <select id="courseTypeFilter" class="filter-select">
        <option value="all">All Courses</option>
        <option value="vorlesung">Lectures</option>
        <option value="seminar">Seminars</option>
        <option value="proseminar">Proseminars</option>
        <option value="hauptseminar">Hauptseminars</option>
      </select>
    </div>
    <div class="filter-group">
      <label for="timeFilter">Filter by Period:</label>
      <select id="timeFilter" class="filter-select">
        <option value="all">All Time</option>
        <option value="current">Current & Recent (2023-2025)</option>
        <option value="recent">Recent (2020-2022)</option>
        <option value="historical">Historical (2010-2019)</option>
      </select>
    </div>
    <div class="filter-group">
      <label for="searchFilter">Search Courses:</label>
      <input type="text" id="searchFilter" class="filter-input" placeholder="Search course titles...">
    </div>
  </div>

  {% assign teaching_all = site.teaching %}
  {% assign teaching_sorted = teaching_all | sort: 'semester_sort' | reverse %}
  {% assign current_courses = teaching_sorted | where_exp: "c", "c.active == true or c.active == 'true'" %}

  <!-- Current Teaching (auto) -->
  {% if current_courses and current_courses.size > 0 %}
  <div class="teaching-section current-section">
    <h3 class="section-title current-title">
      <i class="fas fa-star"></i> Current Teaching
    </h3>
    {% assign current_by_semester = current_courses | group_by: 'semester_key' %}
    {% for sem in current_by_semester %}
      {% assign sample = sem.items | first %}
      <div class="semester-group" data-period="current">
        <h4 class="semester-title current-semester">
          <i class="fas fa-calendar-alt"></i> {{ sample.semester }}
        </h4>
        <ul class="course-list">
          {% for course in sem.items %}
            {% assign type_lower = course.course_type | downcase %}
            <li class="course-item" data-type="{{ type_lower }}" data-period="current">
              <span class="course-badge {{ type_lower }}">
                {% if type_lower == 'vorlesung' %}<i class="fas fa-chalkboard-teacher"></i> Vorlesung{% elsif type_lower == 'hauptseminar' %}<i class="fas fa-graduation-cap"></i> Hauptseminar{% elsif type_lower == 'proseminar' %}<i class="fas fa-book-open"></i> Proseminar{% else %}<i class="fas fa-users"></i> {{ course.course_type }}{% endif %}
              </span>
              <a href="{{ course.url }}" class="course-link">{{ course.title }}</a>
              {% if course.instructor %}<span class="instructors">({{ course.instructor }})</span>{% endif %}
            </li>
          {% endfor %}
        </ul>
      </div>
    {% endfor %}
  </div>
  {% endif %}

  <!-- Recent Teaching (auto) -->
  <div class="teaching-section recent-section">
    <h3 class="section-title recent-title">
      <i class="fas fa-clock"></i> Recent Teaching
    </h3>
    {% assign recent_courses = teaching_sorted | where_exp: "c", "c.active != true and c.active != 'true' and c.semester_year >= 2020" %}
    {% assign recent_by_semester = recent_courses | group_by: 'semester_key' %}
    {% for sem in recent_by_semester %}
      {% assign sample = sem.items | first %}
      <div class="semester-group" data-period="recent">
        <h4 class="semester-title recent-semester">
          <i class="fas fa-calendar-alt"></i> {{ sample.semester }}
        </h4>
        <ul class="course-list">
          {% for course in sem.items %}
            {% assign type_lower = course.course_type | downcase %}
            <li class="course-item" data-type="{{ type_lower }}" data-period="recent">
              <span class="course-badge {{ type_lower }}">
                {% if type_lower == 'vorlesung' %}<i class="fas fa-chalkboard-teacher"></i> Vorlesung{% elsif type_lower == 'hauptseminar' %}<i class="fas fa-graduation-cap"></i> Hauptseminar{% elsif type_lower == 'proseminar' %}<i class="fas fa-book-open"></i> Proseminar{% else %}<i class="fas fa-users"></i> {{ course.course_type }}{% endif %}
              </span>
              <a href="{{ course.url }}" class="course-link">{{ course.title }}</a>
              {% if course.instructor %}<span class="instructors">({{ course.instructor }})</span>{% endif %}
            </li>
          {% endfor %}
        </ul>
      </div>
    {% endfor %}
  </div>

  <!-- Historical Teaching (auto) -->
  <div class="teaching-section historical-section">
    <h3 class="section-title historical-title">
      <i class="fas fa-history"></i> Historical Teaching
    </h3>
    <div class="historical-content">
      {% assign historical_courses = teaching_sorted | where_exp: "c", "c.active != true and c.active != 'true' and c.semester_year < 2020" %}
      {% assign historical_by_semester = historical_courses | group_by: 'semester_key' %}
      {% for sem in historical_by_semester %}
        {% assign sample = sem.items | first %}
        <div class="semester-group" data-period="historical">
          <h4 class="semester-title historical-semester">
            <i class="fas fa-calendar-alt"></i> {{ sample.semester }}
          </h4>
          <ul class="course-list">
            {% for course in sem.items %}
              {% assign type_lower = course.course_type | downcase %}
              <li class="course-item" data-type="{{ type_lower }}" data-period="historical">
                <span class="course-badge {{ type_lower }}">
                  {% if type_lower == 'vorlesung' %}<i class="fas fa-chalkboard-teacher"></i> Vorlesung{% elsif type_lower == 'hauptseminar' %}<i class="fas fa-graduation-cap"></i> Hauptseminar{% elsif type_lower == 'proseminar' %}<i class="fas fa-book-open"></i> Proseminar{% else %}<i class="fas fa-users"></i> {{ course.course_type }}{% endif %}
                </span>
                <a href="{{ course.url }}" class="course-link">{{ course.title }}</a>
                {% if course.instructor %}<span class="instructors">({{ course.instructor }})</span>{% endif %}
              </li>
            {% endfor %}
          </ul>
        </div>
      {% endfor %}
    </div>
  </div>

  <!-- Contact Section -->
  <div class="teaching-footer">
    <div class="footer-content">
      <div class="contact-info">
        <h3><i class="fas fa-envelope"></i> Contact Information</h3>
        <p><strong>For course inquiries:</strong> <a href="mailto:boeckle@mathi.uni-heidelberg.de">boeckle@mathi.uni-heidelberg.de</a></p>
        <p><strong>Office hours:</strong> By appointment</p>
        <p><strong>Location:</strong> Mathematisches Institut, Heidelberg University</p>
      </div>
      <div class="last-update">
        <p><i class="fas fa-clock"></i> Last updated: January 2025</p>
      </div>
    </div>
  </div>
</div>

<!-- Enhanced CSS and JavaScript -->
<style>
.teaching-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

/* Filter Controls */
.filter-controls {
  background: linear-gradient(135deg, #212529 0%, #343a40 100%) !important;
  border-color: #495057 !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
  border-radius: 12px !important;
  border-bottom: 3px solid var(--primary);
  padding: 1.5rem;
  margin-bottom: 2rem;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-group label {
  font-weight: 600;
  color: #495057;
  font-size: 0.9rem;
}

.filter-select, .filter-input {
  padding: 0.75rem;
  border: 1px solid #ced4da;
  border-radius: 6px;
  font-size: 0.9rem;
  background: var(--bg-primary);
  transition: all 0.2s ease;
}

.filter-select:focus, .filter-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

/* Section Styles */
.teaching-section {
  margin-bottom: 3rem;
}

.section-title {
  font-size: 1.8rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  padding: 1rem 0;
  border-bottom: 3px solid var(--primary);
  display: flex;
  align-items: center;
  gap: 0.75rem;
  transition: all 0.3s ease;
}

.section-title i {
  font-size: 1.2rem;
}

.current-title {
  color: #28a745;
  border-bottom-color: #28a745;
}

.recent-title {
  color: #17a2b8;
  border-bottom-color: #17a2b8;
}

.historical-title {
  color: #6c757d;
  border-bottom-color: #6c757d;
}

/* Semester Groups */
.semester-group {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: var(--bg-primary);
  border-radius: 12px;
  border: 1px solid var(--border-color);
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  transition: all 0.3s ease;
}

.semester-group:hover {
  box-shadow: 0 4px 16px rgba(0,0,0,0.1);
  transform: translateY(-2px);
}

.semester-title {
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 1rem;
  padding: 0.75rem 0;
  border-bottom: 2px solid;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.current-semester {
  color: #28a745;
  border-bottom-color: #28a745;
}

.recent-semester {
  color: #17a2b8;
  border-bottom-color: #17a2b8;
}

.historical-semester {
  color: #6c757d;
  border-bottom-color: #6c757d;
}

/* Course Lists */
.course-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.course-item {
  background: #f8f9fa;
  margin: 0.75rem 0;
  padding: 1rem 1.5rem;
  border-radius: 8px;
  border-left: 4px solid #667eea;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
  animation: fadeInUp 0.6s ease forwards;
  opacity: 0;
  transform: translateY(20px);
}

.course-item:hover {
  background: #e3f2fd;
  transform: translateX(5px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
}

.course-item:nth-child(1) { animation-delay: 0.1s; }
.course-item:nth-child(2) { animation-delay: 0.2s; }
.course-item:nth-child(3) { animation-delay: 0.3s; }
.course-item:nth-child(4) { animation-delay: 0.4s; }

.course-item.hidden {
  display: none;
}

/* Course Badges */
.course-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  white-space: nowrap;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  cursor: pointer;
  transition: transform 0.2s ease;
}

.course-badge:hover {
  transform: scale(1.05);
}

.course-badge.seminar {
  background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%);
  color: #27ae60;
  border: 1px solid #a5d6a7;
}

.course-badge.vorlesung {
  background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
  color: #1976d2;
  border: 1px solid #90caf9;
}

.course-badge.proseminar {
  background: linear-gradient(135deg, #fff3e0 0%, #ffcc02 100%);
  color: #f57c00;
  border: 1px solid #ffb74d;
}

.course-badge.hauptseminar {
  background: linear-gradient(135deg, #fce4ec 0%, #f8bbd9 100%);
  color: #c2185b;
  border: 1px solid #f48fb1;
}

/* Course Links */
.course-link {
  color: #2980b9;
  text-decoration: none;
  font-weight: 500;
  flex: 1;
  min-width: 200px;
  transition: color 0.2s ease;
}

.course-link:hover {
  color: #1f5f8b;
  text-decoration: underline;
}

.instructors {
  color: #6c757d;
  font-size: 0.9rem;
  font-style: italic;
  white-space: nowrap;
}

/* Historical Content - Always Visible */
.historical-content {
  /* Remove max-height and overflow restrictions */
}

.historical-note {
  background: #fff3cd;
  border: 1px solid #ffeaa7;
  border-radius: 8px;
  padding: 1rem;
  margin-top: 1rem;
  color: #856404;
}

.historical-note p {
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* Footer */
.teaching-footer {
  background: #f8f9fa;
  border-top: 3px solid #667eea;
  margin: 3rem -2rem -2rem -2rem;
  padding: 2rem;
  border-radius: 15px 15px 0 0;
}

.footer-content {
  max-width: 800px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
  align-items: start;
}

.contact-info h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.contact-info p {
  margin: 0.5rem 0;
  color: #555;
}

.contact-info a {
  color: #3498db;
  text-decoration: none;
}

.contact-info a:hover {
  text-decoration: underline;
}

.last-update {
  text-align: right;
  color: #7f8c8d;
  font-size: 0.9rem;
}

.last-update p {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  justify-content: flex-end;
}

/* Responsive Design */
@media (max-width: 768px) {
  .teaching-intro h2 {
    font-size: 2rem;
  }
  
  .filter-controls {
    grid-template-columns: 1fr;
  }
  
  .course-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .course-badge {
    align-self: flex-start;
  }
  
  .footer-content {
    grid-template-columns: 1fr;
    text-align: center;
  }
  
  .last-update {
    text-align: center;
  }
  
  .last-update p {
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .course-badge {
    font-size: 0.7rem;
    padding: 0.3rem 0.6rem;
  }
  
  .course-link {
    min-width: auto;
  }
}

/* Animation for course items */
@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Hidden class for filtering */
.semester-group.hidden {
  display: none;
}

[data-theme="dark"] .filter-controls,
body.dark-mode .filter-controls {
  border-bottom: 3px solid #111 !important;
}

[data-theme="dark"] .section-title,
body.dark-mode .section-title {
  border-bottom: 3px solid #111 !important;
}
</style>

<script>
document.addEventListener('DOMContentLoaded', function() {
  // Filtering functionality
  const courseTypeFilter = document.getElementById('courseTypeFilter');
  const timeFilter = document.getElementById('timeFilter');
  const searchFilter = document.getElementById('searchFilter');
  const courseItems = document.querySelectorAll('.course-item');
  const semesterGroups = document.querySelectorAll('.semester-group');

  function applyFilters() {
    const selectedType = courseTypeFilter.value;
    const selectedPeriod = timeFilter.value;
    const searchTerm = searchFilter.value.toLowerCase();

    courseItems.forEach(item => {
      const type = item.dataset.type;
      const period = item.dataset.period;
      const title = item.querySelector('.course-link').textContent.toLowerCase();
      
      const typeMatch = selectedType === 'all' || type === selectedType;
      const periodMatch = selectedPeriod === 'all' || period === selectedPeriod;
      const searchMatch = searchTerm === '' || title.includes(searchTerm);
      
      if (typeMatch && periodMatch && searchMatch) {
        item.classList.remove('hidden');
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
  }

  // Event listeners for filters
  courseTypeFilter.addEventListener('change', applyFilters);
  timeFilter.addEventListener('change', applyFilters);
  searchFilter.addEventListener('input', applyFilters);

  // Add smooth scrolling for anchor links
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
});
</script>
