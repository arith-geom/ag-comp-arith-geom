---
layout: page
permalink: "/teaching/"
title: "Teaching"
show_title: false
description: "An overview of our courses, seminars, and lectures, organized by semester."
---

{% assign current_year = site.time | date: "%Y" | plus: 0 %}
{% assign current_month = site.time | date: "%m" | plus: 0 %}

{% if current_month >= 4 and current_month <= 9 %}
  {% assign current_semester_string = "Summer Term " | append: current_year %}
{% else %}
  {% if current_month >= 10 %}
    {% assign next_year = current_year | plus: 1 %}
    {% assign next_year_short = next_year | modulo: 100 %}
    {% assign current_semester_string = "Winter Term " | append: current_year | append: "/" | append: next_year_short %}
  {% else %}
    {% assign prev_year = current_year | minus: 1 %}
    {% assign current_year_short = current_year | modulo: 100 %}
    {% assign current_semester_string = "Winter Term " | append: prev_year | append: "/" | append: current_year_short %}
  {% endif %}
{% endif %}

<div class="teaching-by-semester-container">
    {% assign previous_university = "" %}
    {% for year_data in site.data.teaching.courses %}
      {% if year_data.university and year_data.university != previous_university %}
        {% if previous_university != "" %}
          <div class="university-separator my-5">
            <hr class="my-4">
            <h3 class="text-center text-muted mb-4">
              <i class="fas fa-university me-2"></i>{{ year_data.university }}
            </h3>
            <hr class="my-4">
          </div>
        {% endif %}
        {% assign previous_university = year_data.university %}
      {% endif %}
      
      {% for semester in year_data.semesters %}
        {% assign highlight_class = "" %}
        {% if semester.semester == current_semester_string %}
          {% assign highlight_class = "highlight-current" %}
        {% endif %}
        <div class="semester-section {{ highlight_class | strip }}">
          <h4 class="semester-title">{{ semester.semester }}</h4>
          {% for course in semester.courses %}
            <div class="course-card position-relative">
              <h5 class="course-title">
                {% assign course_slug = course.title | slugify %}
                {% assign semester_slug = semester.semester | slugify %}
                <a href="{{ '/teaching/' | append: year_data.year | append: '/' | append: semester_slug | append: '/' | append: course_slug | append: '/' | relative_url }}" class="text-decoration-none text-dark stretched-link">{{ course.title }}</a>
              </h5>
              {% if course.instructor %}
                <p class="course-instructor"><i class="fas fa-user-tie"></i> {{ course.instructor }}</p>
              {% endif %}
              <div class="course-body">
                {% if course.description and course.description != "" %}
                  <p>{{ course.description }}</p>
                {% endif %}
                
                {% if course.links or course.pdfs %}
                <div class="course-resources mt-2 position-relative" style="z-index: 2;">
                  {% for link in course.links %}
                    <a href="{{ link.url }}" class="btn btn-sm btn-outline-primary me-1 mb-1" target="_blank" rel="noopener">
                      <i class="fas fa-external-link-alt"></i> {{ link.label | default: "More Info" }}
                    </a>
                  {% endfor %}
                  {% for pdf in course.pdfs %}
                    <a href="{{ pdf.file | relative_url }}" class="btn btn-sm btn-outline-danger me-1 mb-1" target="_blank" rel="noopener">
                      <i class="fas fa-file-pdf"></i> {{ pdf.label | default: "PDF" }}
                    </a>
                  {% endfor %}
                </div>
                {% endif %}
              </div>
            </div>
          {% endfor %}
        </div>
      {% endfor %}
    {% endfor %}
</div>
