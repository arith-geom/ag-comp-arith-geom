---
layout: page
title: Teaching
permalink: /teaching/
nav: true
---

<p class="translatable-content" data-translation-key="teaching.intro">Our group is actively involved in teaching at Heidelberg University. Below is a list of current and past courses, which you can manage from the CMS. For official details, please refer to the university's course catalog.</p>

<div class="teaching-list mt-5">
  {% if site.teaching %}
    {% assign courses_by_semester = site.teaching | group_by: "semester" | sort: "name" | reverse %}
    
    {% for semester_group in courses_by_semester %}
      <h2 class="semester-heading">{{ semester_group.name }}</h2>
      <div class="course-grid">
        {% for course in semester_group.items %}
          <div class="course-card">
            <div class="card-body">
              <h4 class="card-title">{{ course.title }}</h4>
              <p class="card-subtitle mb-2 text-muted"><strong class="translatable-content" data-translation-key="teaching.instructor">Instructor:</strong> {{ course.instructor }}</p>
              {% if course.details %}
                <p class="card-text"><strong class="translatable-content" data-translation-key="teaching.time_location">Time/Location:</strong> {{ course.details }}</p>
              {% endif %}
              {% if course.description %}
                <div class="course-description mt-3">
                  {{ course.description | markdownify }}
                </div>
              {% endif %}
            </div>
          </div>
        {% endfor %}
      </div>
    {% endfor %}
  {% else %}
    <p class="text-muted">No teaching information available at this time.</p>
  {% endif %}
</div>

<style>
.semester-heading {
  font-size: 2rem;
  margin-top: 3rem;
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid var(--primary);
}
.course-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
}
.course-card {
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  background-color: var(--bg-secondary);
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-base);
}
.course-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-md);
}
.course-card .card-body {
  padding: 1.5rem;
}
</style> 