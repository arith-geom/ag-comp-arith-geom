---
layout: page
permalink: "/teaching/"
scripts:
- "/assets/js/teaching-page.js"
active: false
show_title: false
content: "<div class=\"teaching-page\">\n  <div id=\"courseFocusBar\" class=\"course-focus-bar\"
  style=\"display: none;\">\n    <button id=\"backToAllCourses\" class=\"back-to-all-btn\">\n
  \     <i class=\"fas fa-arrow-left\"></i> Back to all courses\n    </button>\n  </div>\n
  \ \n  <!-- Filter Controls -->\n  <div class=\"filter-controls\">\n    <div class=\"filter-group\">\n
  \     <label for=\"courseTypeFilter\">Filter by Type:</label>\n      <select id=\"courseTypeFilter\"
  class=\"filter-select\">\n        <option value=\"all\">All Courses</option>\n        <option
  value=\"vorlesung\">Lectures</option>\n        <option value=\"seminar\">Seminars</option>\n
  \       <option value=\"proseminar\">Proseminars</option>\n        <option value=\"hauptseminar\">Hauptseminars</option>\n
  \     </select>\n    </div>\n    <div class=\"filter-group\">\n      <label for=\"yearFilter\">Filter
  by Year:</label>\n      <select id=\"yearFilter\" class=\"filter-select\">\n        <option
  value=\"all\">All Years</option>\n        {% assign teaching_all = site.teaching
  | where: 'layout', 'teaching' %}\n        {% assign years = teaching_all | map:
  'semester_year' | compact | uniq | sort | reverse %}\n        {% for y in years
  %}\n        {% if y %}<option value=\"{{ y }}\">{{ y }}</option>{% endif %}\n        {%
  endfor %}\n      </select>\n    </div>\n    <div class=\"filter-group\">\n      <label
  for=\"searchFilter\">Search Courses:</label>\n      <input type=\"text\" id=\"searchFilter\"
  class=\"filter-input\" placeholder=\"Search course titles...\">\n    </div>\n  </div>\n\n
  \ {% assign teaching_all = site.teaching | where: 'layout', 'teaching' %}\n  {%
  assign teaching_sorted = teaching_all | sort: 'semester_sort' | reverse %}\n  {%
  assign current_courses = teaching_sorted | where_exp: \"c\", \"c.active == true
  or c.active == 'true'\" %}\n\n  <!-- Recent Teaching (auto) -->\n  <div class=\"teaching-section
  recent-section\">\n    <h3 class=\"section-title recent-title\">\n      <i class=\"fas
  fa-clock\"></i> Recent Teaching\n    </h3>\n    {% assign recent_courses = teaching_sorted
  | where_exp: \"c\", \"c.semester_key and c.semester_key != ''\" %}\n    {% assign
  recent_by_semester = recent_courses | group_by: 'semester_key' %}\n    {% for sem
  in recent_by_semester %}\n      {% assign sample = sem.items | first %}\n      <div
  class=\"semester-group\" data-period=\"recent\" data-semester=\"{{ sample.semester_key
  }}\">\n        <h4 class=\"semester-title recent-semester\">\n          <i class=\"fas
  fa-calendar-alt\"></i> {{ sample.semester_key }}\n        </h4>\n        <ul class=\"course-list\">\n
  \         {% for course in sem.items %}\n            {% assign type_lower = course.course_type
  | downcase %}\n            <li class=\"course-item\" data-type=\"{{ type_lower }}\"
  data-year=\"{{ course.semester_year }}\" {% if course.external_url %}data-course-url=\"{{
  course.external_url }}\" data-external=\"true\"{% endif %}>\n              <span
  class=\"course-badge {{ type_lower }}\">\n                {% if type_lower == 'vorlesung'
  %}<i class=\"fas fa-chalkboard-teacher\"></i> Lecture{% elsif type_lower == 'hauptseminar'
  %}<i class=\"fas fa-graduation-cap\"></i> Advanced Seminar{% elsif type_lower ==
  'proseminar' %}<i class=\"fas fa-book-open\"></i> Proseminar{% else %}<i class=\"fas
  fa-users\"></i> {{ course.course_type }}{% endif %}\n              </span>\n              <span
  class=\"course-title\">{{ course.title }}</span>\n              {% if course.instructor
  %}<span class=\"instructors\">({{ course.instructor }})</span>{% endif %}\n              <button
  class=\"course-expand-btn\" aria-expanded=\"false\" title=\"Show details\" tabindex=\"-1\"
  disabled aria-disabled=\"true\">\n                <i class=\"fas fa-chevron-down\"></i>\n
  \             </button>\n              <div class=\"course-details\" style=\"display:
  none;\">\n                <div class=\"course-details-inner\">\n                  <div
  class=\"course-meta\">\n                    <span class=\"meta-item\"><i class=\"fas
  fa-tag\"></i> {{ course.course_type }}</span>\n                    {% if course.semester_key
  %}<span class=\"meta-item\"><i class=\"fas fa-calendar\"></i> {{ course.semester_key
  }}</span>{% endif %}\n                    {% if course.language %}<span class=\"meta-item\"><i
  class=\"fas fa-language\"></i> {{ course.language }}</span>{% endif %}\n                    {%
  if course.level %}<span class=\"meta-item\"><i class=\"fas fa-signal\"></i> {{ course.level
  }}</span>{% endif %}\n                  </div>\n                  {% if course.description
  %}\n                  <div class=\"course-description\">{{ course.description }}</div>\n
  \                 {% endif %}\n                  {% if course.content %}\n                  <div
  class=\"course-full-content\">{{ course.content }}</div>\n                  {% endif
  %}\n                  {% assign has_links = course.links and course.links.size >
  0 %}\n                  {% assign has_pdfs  = course.pdfs and course.pdfs.size >
  0 %}\n                  {% if has_links or has_pdfs %}\n                  <div class=\"course-links\">\n
  \                   <div class=\"links-title\"><i class=\"fas fa-paperclip\"></i>
  Resources</div>\n                    <ul>\n                      {% if has_links
  %}\n                        {% for link in course.links %}\n                          {%
  if link.url %}\n                          <li>\n                            <a href=\"{{
  link.url }}\" target=\"_blank\" rel=\"noopener\">\n                              {%
  if link.label %}{{ link.label }}{% else %}{{ link.url }}{% endif %}\n                            </a>\n
  \                         </li>\n                          {% endif %}\n                        {%
  endfor %}\n                      {% endif %}\n                      {% if has_pdfs
  %}\n                        {% for pdf in course.pdfs %}\n                          {%
  if pdf.file %}\n                          <li>\n                            <a href=\"{{
  pdf.file | relative_url }}\" target=\"_blank\" rel=\"noopener\">\n                              {%
  if pdf.label %}{{ pdf.label }}{% else %}PDF{% endif %}\n                            </a>\n
  \                         </li>\n                          {% endif %}\n                        {%
  endfor %}\n                      {% endif %}\n                    </ul>\n                  </div>\n
  \                 {% endif %}\n                </div>\n              </div>\n            </li>\n
  \         {% endfor %}\n        </ul>\n      </div>\n    {% endfor %}\n  </div>\n\n\n
  \ \n</div>\n\n<!-- Enhanced CSS and JavaScript -->\n<style>\n.teaching-page {\n
  \ width: 100%;\n  margin: 0;\n  padding: 0 1rem;\n}\n\n  .semester-filter-bar {\n
  \   margin: 0 0 1rem 0;\n  }\n\n  .back-to-all-btn {\n    display: inline-flex;\n
  \   align-items: center;\n    gap: 0.5rem;\n    padding: 0.5rem 0.9rem;\n    background:
  var(--bg-primary);\n    border: 1px solid var(--border-color);\n    border-radius:
  6px;\n    cursor: pointer;\n  }\n\n/* Filter Controls */\n.filter-controls {\n  background:
  var(--bg-primary) !important;\n  border: 1px solid var(--border-color) !important;\n
  \ box-shadow: var(--shadow-sm) !important;\n  border-radius: 12px !important;\n
  \ border-bottom: 0 !important;\n  padding: 1.5rem;\n  margin-bottom: 2rem;\n  display:
  grid;\n  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));\n  gap: 1rem;\n}\n\n.filter-group
  {\n  display: flex;\n  flex-direction: column;\n  gap: 0.5rem;\n}\n\n.filter-group
  label {\n  font-weight: 600;\n  color: #495057;\n  font-size: 0.9rem;\n}\n\n.filter-select,
  .filter-input {\n  padding: 0.75rem;\n  border: 1px solid #ced4da;\n  border-radius:
  6px;\n  font-size: 0.9rem;\n  background: var(--bg-primary);\n  transition: all
  0.2s ease;\n}\n\n.filter-select:focus, .filter-input:focus {\n  outline: none;\n
  \ border-color: #667eea;\n  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);\n}\n\n/*
  Section Styles */\n.teaching-section {\n  margin-bottom: 3rem;\n}\n\n.section-title
  {\n  font-size: 1.8rem;\n  font-weight: 600;\n  margin-bottom: 1.5rem;\n  padding:
  1rem 0;\n  border-bottom: 3px solid var(--primary);\n  display: flex;\n  align-items:
  center;\n  gap: 0.75rem;\n  transition: all 0.3s ease;\n}\n\n.section-title i {\n
  \ font-size: 1.2rem;\n}\n\n.current-title {\n  color: #28a745;\n  border-bottom-color:
  #28a745;\n}\n\n.recent-title {\n  color: #17a2b8;\n  border-bottom-color: #17a2b8;\n}\n\n.historical-title
  {\n  color: #6c757d;\n  border-bottom-color: #6c757d;\n}\n\n/* Semester Groups */\n.semester-group
  {\n  margin-bottom: 2rem;\n  padding: 1.5rem;\n  background: var(--bg-primary);\n
  \ border-radius: 12px;\n  border: 1px solid var(--border-color);\n  box-shadow:
  0 2px 8px rgba(0,0,0,0.05);\n  transition: all 0.3s ease;\n}\n\n.semester-group:hover
  {\n  box-shadow: 0 4px 16px rgba(0,0,0,0.1);\n  transform: translateY(-2px);\n}\n\n.semester-title
  {\n  font-size: 1.3rem;\n  font-weight: 600;\n  margin-bottom: 1rem;\n  padding:
  0.75rem 0;\n  border-bottom: 2px solid;\n  display: flex;\n  align-items: center;\n
  \ gap: 0.5rem;\n  cursor: pointer;\n}\n\n.current-semester {\n  color: #28a745;\n
  \ border-bottom-color: #28a745;\n}\n\n.recent-semester {\n  color: #17a2b8;\n  border-bottom-color:
  #17a2b8;\n}\n\n.historical-semester {\n  color: #6c757d;\n  border-bottom-color:
  #6c757d;\n}\n\n/* Course Lists */\n.course-list {\n  list-style: none;\n  padding:
  0;\n  margin: 0;\n}\n\n.course-item {\n  background: #f8f9fa;\n  margin: 0.75rem
  0;\n  padding: 1rem 1.5rem;\n  border-radius: 8px;\n  border-left: 4px solid #667eea;\n
  \ transition: all 0.3s ease;\n  display: flex;\n  align-items: center;\n  gap: 1rem;\n
  \ flex-wrap: wrap;\n  animation: fadeInUp 0.6s ease forwards;\n  opacity: 0;\n  transform:
  translateY(20px);\n  cursor: pointer;\n}\n\n.course-item:hover {\n  background:
  #e3f2fd;\n  transform: translateX(5px);\n  box-shadow: 0 4px 12px rgba(102, 126,
  234, 0.15);\n}\n\n.course-item:nth-child(1) { animation-delay: 0.1s; }\n.course-item:nth-child(2)
  { animation-delay: 0.2s; }\n.course-item:nth-child(3) { animation-delay: 0.3s; }\n.course-item:nth-child(4)
  { animation-delay: 0.4s; }\n\n.course-item.hidden {\n  display: none;\n}\n\n/* Focus-mode
  visibility control (kept separate from filter .hidden) */\n.course-item.focus-hidden,\n.semester-group.focus-hidden
  {\n  display: none;\n}\n\n/* Course Badges */\n.course-badge {\n  display: inline-flex;\n
  \ align-items: center;\n  gap: 0.5rem;\n  padding: 0.4rem 0.8rem;\n  border-radius:
  20px;\n  font-size: 0.8rem;\n  font-weight: 600;\n  white-space: nowrap;\n  box-shadow:
  0 2px 4px rgba(0,0,0,0.1);\n  cursor: pointer;\n  transition: transform 0.2s ease;\n}\n\n.course-badge:hover
  {\n  transform: scale(1.05);\n}\n\n.course-badge.seminar { background: #e8f5e8;
  color: #1b5e20; border: 1px solid #a5d6a7; }\n.course-badge.vorlesung { background:
  #eaeef7; color: #0d47a1; border: 1px solid #93b3e3; }\n.course-badge.proseminar
  { background: #fff3e0; color: #e65100; border: 1px solid #ffb74d; }\n.course-badge.hauptseminar
  { background: #fce4ec; color: #880e4f; border: 1px solid #f48fb1; }\n\n/* Course
  Links */\n.course-link {\n  color: #111;\n  text-decoration: none;\n  font-weight:
  500;\n  flex: 1;\n  min-width: 200px;\n  transition: color 0.2s ease;\n}\n\n.course-link:hover
  {\n  color: #000;\n  text-decoration: underline;\n}\n\n/* Non-clickable course title
  */\n.course-title {\n  color: #111;\n  font-weight: 500;\n  flex: 1;\n  min-width:
  200px;\n}\n\n  .course-expand-btn {\n    margin-left: auto;\n    background: transparent;\n
  \   border: 1px dashed var(--border-color);\n    border-radius: 6px;\n    padding:
  0.3rem 0.55rem;\n    cursor: default;\n    pointer-events: none;\n  }\n\n  .course-details
  {\n    flex-basis: 100%;\n    background: var(--bg-primary);\n    border: 1px solid
  var(--border-color);\n    border-radius: 8px;\n    margin-top: 0.75rem;\n    padding:
  0.9rem 1rem;\n  }\n\n  .course-meta {\n    display: flex;\n    gap: 0.75rem;\n    flex-wrap:
  wrap;\n    color: #6c757d;\n    font-size: 0.9rem;\n    margin-bottom: 0.4rem;\n
  \ }\n\n  .course-actions {\n    margin-top: 0.5rem;\n  }\n\n  .open-course-page
  {\n    display: inline-flex;\n    align-items: center;\n    gap: 0.4rem;\n    text-decoration:
  none;\n    color: #2980b9;\n    font-weight: 500;\n  }\n\n.instructors {\n  color:
  #6c757d;\n  font-size: 0.9rem;\n  font-style: italic;\n  white-space: nowrap;\n}\n\n/*
  Historical Content - Always Visible */\n.historical-content {\n  /* Remove max-height
  and overflow restrictions */\n}\n\n.historical-note {\n  background: #fff3cd;\n
  \ border: 1px solid #ffeaa7;\n  border-radius: 8px;\n  padding: 1rem;\n  margin-top:
  1rem;\n  color: #856404;\n}\n\n.historical-note p {\n  margin: 0;\n  display: flex;\n
  \ align-items: center;\n  gap: 0.5rem;\n}\n\n/* Footer */\n.teaching-footer {\n
  \ background: #f8f9fa;\n  border-top: 3px solid #667eea;\n  margin: 3rem -2rem -2rem
  -2rem;\n  padding: 2rem;\n  border-radius: 15px 15px 0 0;\n}\n\n/* Dark mode cleanup
  for neutral surfaces */\n[data-theme=\"dark\"] .semester-group,\nbody.dark-mode
  .semester-group {\n  background: #0f1115;\n  border-color: #1f232b;\n}\n\n[data-theme=\"dark\"]
  .course-item,\nbody.dark-mode .course-item {\n  background: #0b0d11;\n}\n\n.footer-content
  {\n  max-width: 800px;\n  margin: 0 auto;\n  display: grid;\n  grid-template-columns:
  2fr 1fr;\n  gap: 2rem;\n  align-items: start;\n}\n\n.contact-info h3 {\n  color:
  #2c3e50;\n  margin-bottom: 1rem;\n  font-size: 1.2rem;\n  display: flex;\n  align-items:
  center;\n  gap: 0.5rem;\n}\n\n.contact-info p {\n  margin: 0.5rem 0;\n  color: #555;\n}\n\n.contact-info
  a {\n  color: #3498db;\n  text-decoration: none;\n}\n\n.contact-info a:hover {\n
  \ text-decoration: underline;\n}\n\n.last-update {\n  text-align: right;\n  color:
  #7f8c8d;\n  font-size: 0.9rem;\n}\n\n.last-update p {\n  display: flex;\n  align-items:
  center;\n  gap: 0.5rem;\n  justify-content: flex-end;\n}\n\n/* Responsive Design
  */\n@media (max-width: 768px) {\n  .teaching-intro h2 {\n    font-size: 2rem;\n
  \ }\n  \n  .filter-controls {\n    grid-template-columns: 1fr;\n  }\n  \n  .course-item
  {\n    flex-direction: column;\n    align-items: flex-start;\n    gap: 0.5rem;\n
  \ }\n  \n  .course-badge {\n    align-self: flex-start;\n  }\n  \n  .footer-content
  {\n    grid-template-columns: 1fr;\n    text-align: center;\n  }\n  \n  .last-update
  {\n    text-align: center;\n  }\n  \n  .last-update p {\n    justify-content: center;\n
  \ }\n}\n\n@media (max-width: 480px) {\n  .course-badge {\n    font-size: 0.7rem;\n
  \   padding: 0.3rem 0.6rem;\n  }\n  \n  .course-link, .course-title {\n    min-width:
  auto;\n  }\n    .course-expand-btn {\n      align-self: flex-start;\n      margin-left:
  0;\n    }\n}\n\n/* Animation for course items */\n@keyframes fadeInUp {\n  to {\n
  \   opacity: 1;\n    transform: translateY(0);\n  }\n}\n\n/* Hidden class for filtering
  */\n.semester-group.hidden {\n  display: none;\n}\n\n.course-focus-bar {\n  margin:
  0 0 1rem 0;\n}\n\n[data-theme=\"dark\"] .filter-controls,\nbody.dark-mode .filter-controls
  {\n  border-bottom: 0 !important;\n}\n\n[data-theme=\"dark\"] .section-title,\nbody.dark-mode
  .section-title {\n  border-bottom: 3px solid #111 !important;\n}\n</style>\n\n<!--
  page-level inline script removed to avoid conflicts; global assets/js/teaching-page.js
  handles behavior -->"
description: '<div class="teaching-page"> <div id="courseFocusBar" class="course-focus-bar"
  style="display: none;"> <button id="backToAllCourses" class="back-to-all-btn"> <i
  class="fas fa-arrow-left"></i> Back to all courses </button> </div> <!-- Filter
  Controls --> <div class="filter-controls'
---
<div class="teaching-page">
  <div id="courseFocusBar" class="course-focus-bar" style="display: none;">
    <button id="backToAllCourses" class="back-to-all-btn">
      <i class="fas fa-arrow-left"></i> Back to all courses
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
  {% assign current_courses = teaching_sorted | where_exp: "c", "c.active == true or c.active == 'true'" %}

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
            <li class="course-item" data-type="{{ type_lower }}" data-year="{{ course.semester_year }}" {% if course.external_url %}data-course-url="{{ course.external_url }}" data-external="true"{% endif %}>
              <span class="course-badge {{ type_lower }}">
                {% if type_lower == 'vorlesung' %}<i class="fas fa-chalkboard-teacher"></i> Lecture{% elsif type_lower == 'hauptseminar' %}<i class="fas fa-graduation-cap"></i> Advanced Seminar{% elsif type_lower == 'proseminar' %}<i class="fas fa-book-open"></i> Proseminar{% else %}<i class="fas fa-users"></i> {{ course.course_type }}{% endif %}
              </span>
              <span class="course-title">{{ course.title }}</span>
              {% if course.instructor %}<span class="instructors">({{ course.instructor }})</span>{% endif %}
              <button class="course-expand-btn" aria-expanded="false" title="Show details" tabindex="-1" disabled aria-disabled="true">
                <i class="fas fa-chevron-down"></i>
              </button>
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
                  {% assign has_links = course.links and course.links.size > 0 %}
                  {% assign has_pdfs  = course.pdfs and course.pdfs.size > 0 %}
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

<!-- Enhanced CSS and JavaScript -->
<style>
.teaching-page {
  width: 100%;
  margin: 0;
  padding: 0 1rem;
}

  .semester-filter-bar {
    margin: 0 0 1rem 0;
  }

  .back-to-all-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 0.9rem;
    background: var(--bg-primary);
    border: 1px solid var(--border-color);
    border-radius: 6px;
    cursor: pointer;
  }

/* Filter Controls */
.filter-controls {
  background: var(--bg-primary) !important;
  border: 1px solid var(--border-color) !important;
  box-shadow: var(--shadow-sm) !important;
  border-radius: 12px !important;
  border-bottom: 0 !important;
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
  cursor: pointer;
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
  cursor: pointer;
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

/* Focus-mode visibility control (kept separate from filter .hidden) */
.course-item.focus-hidden,
.semester-group.focus-hidden {
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

.course-badge.seminar { background: #e8f5e8; color: #1b5e20; border: 1px solid #a5d6a7; }
.course-badge.vorlesung { background: #eaeef7; color: #0d47a1; border: 1px solid #93b3e3; }
.course-badge.proseminar { background: #fff3e0; color: #e65100; border: 1px solid #ffb74d; }
.course-badge.hauptseminar { background: #fce4ec; color: #880e4f; border: 1px solid #f48fb1; }

/* Course Links */
.course-link {
  color: #111;
  text-decoration: none;
  font-weight: 500;
  flex: 1;
  min-width: 200px;
  transition: color 0.2s ease;
}

.course-link:hover {
  color: #000;
  text-decoration: underline;
}

/* Non-clickable course title */
.course-title {
  color: #111;
  font-weight: 500;
  flex: 1;
  min-width: 200px;
}

  .course-expand-btn {
    margin-left: auto;
    background: transparent;
    border: 1px dashed var(--border-color);
    border-radius: 6px;
    padding: 0.3rem 0.55rem;
    cursor: default;
    pointer-events: none;
  }

  .course-details {
    flex-basis: 100%;
    background: var(--bg-primary);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    margin-top: 0.75rem;
    padding: 0.9rem 1rem;
  }

  .course-meta {
    display: flex;
    gap: 0.75rem;
    flex-wrap: wrap;
    color: #6c757d;
    font-size: 0.9rem;
    margin-bottom: 0.4rem;
  }

  .course-actions {
    margin-top: 0.5rem;
  }

  .open-course-page {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    text-decoration: none;
    color: #2980b9;
    font-weight: 500;
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

/* Dark mode cleanup for neutral surfaces */
[data-theme="dark"] .semester-group,
body.dark-mode .semester-group {
  background: #0f1115;
  border-color: #1f232b;
}

[data-theme="dark"] .course-item,
body.dark-mode .course-item {
  background: #0b0d11;
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
  
  .course-link, .course-title {
    min-width: auto;
  }
    .course-expand-btn {
      align-self: flex-start;
      margin-left: 0;
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

.course-focus-bar {
  margin: 0 0 1rem 0;
}

[data-theme="dark"] .filter-controls,
body.dark-mode .filter-controls {
  border-bottom: 0 !important;
}

[data-theme="dark"] .section-title,
body.dark-mode .section-title {
  border-bottom: 3px solid #111 !important;
}
</style>

<!-- page-level inline script removed to avoid conflicts; global assets/js/teaching-page.js handles behavior -->
