---
layout: page
permalink: "/teaching/"
scripts:
- "/assets/js/components/teaching-page.js"
show_title: false
description: Teaching overview with filters and recent courses
---
<div class="teaching-page">
  <div id="courseFocusBar" class="course-focus-bar" style="display: none;">
    <button id="backToAllCourses" class="back-to-all-btn" aria-label="Back to all courses">
      <span>
        <i class="fas fa-circle-arrow-left"></i>
        Back to All Courses
      </span>
    </button>
  </div>
  
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
      <label for="yearFilter">Filter by Year:</label>
      <select id="yearFilter" class="filter-select">
        <option value="all">All Years</option>
        {% assign teaching_all = site.teaching | where: 'layout', 'teaching' %}
        {% assign years = teaching_all | map: 'semester_year' | compact | uniq | sort | reverse %}
        {% for y in years %}
        {% if y %}<option value="{{ y }}">{{ y }}</option>{% endif %}
        {% endfor %}
      </select>
    </div>
    <div class="filter-group">
      <label for="searchFilter">Search Courses:</label>
      <input type="text" id="searchFilter" class="filter-input" placeholder="Search course titles...">
    </div>
  </div>

  {% assign teaching_all = site.teaching | where: 'layout', 'teaching' %}
  {% assign teaching_sorted = teaching_all | sort: 'semester_sort' | reverse %}

  <!-- Recent Teaching (auto) -->
  <div class="teaching-section recent-section">
    <h3 class="section-title recent-title">
      <i class="fas fa-clock"></i> Recent Teaching
    </h3>
    {% assign recent_courses = teaching_sorted | where_exp: "c", "c.semester_key and c.semester_key != ''" %}
    {% assign recent_by_semester = recent_courses | group_by: 'semester_key' %}
    {% for sem in recent_by_semester %}
      {% assign sample = sem.items | first %}
      <div class="semester-group" data-period="recent" data-semester="{{ sample.semester_key }}">
        <h4 class="semester-title recent-semester">
          <i class="fas fa-calendar-alt"></i> {{ sample.semester_key }}
        </h4>
        <ul class="course-list">
          {% for course in sem.items %}
            {% assign type_lower = course.course_type | downcase %}
            <li class="course-item" data-type="{{ type_lower }}" data-year="{{ course.semester_year }}" data-period="recent" {% if course.external_url %}data-course-url="{{ course.external_url }}" data-external="true"{% endif %}>
              <div class="course-item-header">
                <span class="course-badge {{ type_lower }}">
                  {% if type_lower == 'vorlesung' %}<i class="fas fa-chalkboard-teacher"></i> Lecture{% elsif type_lower == 'hauptseminar' %}<i class="fas fa-graduation-cap"></i> Advanced Seminar{% elsif type_lower == 'proseminar' %}<i class="fas fa-book-open"></i> Proseminar{% else %}<i class="fas fa-users"></i> {{ course.course_type }}{% endif %}
                </span>
                <span class="course-title">{{ course.title }}</span>
                {% if course.instructor %}<span class="instructors">({{ course.instructor }})</span>{% endif %}
                <button class="course-expand-btn" aria-expanded="false" title="Show details">
                  <i class="fas fa-chevron-down"></i>
                </button>
              </div>
              <div class="course-details" style="display: none;">
                <div class="course-details-inner">
                  <div class="course-meta">
                    <span class="meta-item"><i class="fas fa-tag"></i> {{ course.course_type }}</span>
                    {% if course.semester_key %}<span class="meta-item"><i class="fas fa-calendar"></i> {{ course.semester_key }}</span>{% endif %}
                    {% if course.language %}<span class="meta-item"><i class="fas fa-language"></i> {{ course.language }}</span>{% endif %}
                    {% if course.level %}<span class="meta-item"><i class="fas fa-signal"></i> {{ course.level }}</span>{% endif %}
                  </div>
                  {% if course.description %}
                  <div class="course-description">{{ course.description }}</div>
                  {% endif %}
                  {% if course.content %}
                  <div class="course-full-content">{{ course.content }}</div>
                  {% endif %}
                  {% assign has_links = course.links.size %}
                  {% assign has_pdfs  = course.pdfs.size %}
                  {% if has_links or has_pdfs %}
                  <div class="course-links">
                    <div class="links-title"><i class="fas fa-paperclip"></i> Resources</div>
                    <ul>
                      {% if has_links %}
                        {% for link in course.links %}
                          {% if link.url %}
                          <li>
                            <a href="{{ link.url }}" target="_blank" rel="noopener">
                              {% if link.label %}{{ link.label }}{% else %}{{ link.url }}{% endif %}
                            </a>
                          </li>
                          {% endif %}
                        {% endfor %}
                      {% endif %}
                      {% if has_pdfs %}
                        {% for pdf in course.pdfs %}
                          {% if pdf.file %}
                          <li>
                            <a href="{{ pdf.file | relative_url }}" target="_blank" rel="noopener">
                              {% if pdf.label %}{{ pdf.label }}{% else %}PDF{% endif %}
                            </a>
                          </li>
                          {% endif %}
                        {% endfor %}
                      {% endif %}
                    </ul>
                  </div>
                  {% endif %}
                </div>
              </div>
            </li>
          {% endfor %}
        </ul>
      </div>
    {% endfor %}
  </div>
</div>
