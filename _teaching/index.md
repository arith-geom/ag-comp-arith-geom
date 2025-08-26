---
layout: page
permalink: "/teaching/"
scripts:
- "/assets/js/components/teaching-page.js"
show_title: false
description: Teaching overview with filters and recent courses
---
<div class="teaching-page">
  <!-- All 131 teaching entries from Heidelberg website are included and up to date as of 2025-08-26T23:39:39 -->
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
                <div class="course-info-section">
                  <span class="course-badge {{ type_lower }}">
                    {% if type_lower == 'vorlesung' %}<i class="fas fa-chalkboard-teacher"></i> Lecture{% elsif type_lower == 'hauptseminar' %}<i class="fas fa-graduation-cap"></i> Advanced Seminar{% elsif type_lower == 'proseminar' %}<i class="fas fa-book-open"></i> Proseminar{% else %}<i class="fas fa-users"></i> {{ course.course_type }}{% endif %}
                  </span>
                  <span class="course-title">{{ course.title }}</span>
                  {% if course.instructor %}<span class="instructors">({{ course.instructor }})</span>{% endif %}
                </div>
                {% assign has_links = course.links.size %}
                {% assign has_pdfs = course.pdfs.size %}

                {% comment %}Check if course has additional content beyond the title{% endcomment %}
                {% assign has_expandable_content = false %}
                {% if course.content %}
                  {% assign content_length = course.content | size %}
                  {% assign title_length = course.title | size %}
                  {% comment %}If content is significantly longer than title, or contains subdomain content markers{% endcomment %}
                  {% assign min_length = title_length | plus: 20 %}
                  {% if content_length > min_length or course.content contains '--- Content from' %}
                    {% assign has_expandable_content = true %}
                  {% endif %}
                {% endif %}

                {% if has_links or has_pdfs or has_expandable_content %}
                <div class="course-resources-preview">
                  {% for link in course.links %}
                    {% if link.url %}
                    <a href="{{ link.url }}" target="_blank" rel="noopener" class="resource-link" title="{{ link.label | default: link.url }}">
                      <i class="fas fa-external-link-alt"></i>
                      <span class="resource-text">{{ link.label | default: 'Link' }}</span>
                    </a>
                    {% endif %}
                  {% endfor %}
                  {% for pdf in course.pdfs %}
                    {% if pdf.file %}
                    <a href="{{ pdf.file | relative_url }}" target="_blank" rel="noopener" class="resource-link" title="{{ pdf.label | default: 'PDF' }}">
                      <i class="fas fa-file-pdf"></i>
                      <span class="resource-text">{{ pdf.label | default: 'PDF' }}</span>
                    </a>
                    {% endif %}
                  {% endfor %}
                </div>
                {% endif %}

                {% comment %}Only show expand button if there's expandable content{% endcomment %}
                {% if has_expandable_content %}
                <button class="course-expand-btn" aria-expanded="false" title="Show additional content">
                  <i class="fas fa-chevron-down"></i>
                </button>
                {% endif %}
              </div>
              {% comment %}Only show course details if there's expandable content{% endcomment %}
              {% if has_expandable_content %}
              <div class="course-details" style="display: none;">
                <div class="course-details-inner">
                  {% if course.content contains '--- Content from' %}
                    {% comment %}Show only the subdomain content, not the original title{% endcomment %}
                    {% assign subdomain_start = course.content | split: '--- Content from' | last %}
                    {% if subdomain_start != course.content %}
                  <div class="course-full-content">{{ subdomain_start }}</div>
                    {% endif %}
                  {% else %}
                    {% comment %}Show the full content minus the title part{% endcomment %}
                    {% assign content_without_title = course.content | remove: course.title | strip %}
                    {% if content_without_title != "" and content_without_title != course.title %}
                  <div class="course-full-content">{{ content_without_title }}</div>
                    {% endif %}
                  {% endif %}
                </div>
              </div>
              {% endif %}
            </li>
          {% endfor %}
        </ul>
      </div>
    {% endfor %}
  </div>
</div>
