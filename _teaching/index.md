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

<div class="timeline-section">
  <h2 class="timeline-title">Courses Timeline</h2>
  <div class="teaching-by-semester-container">
    {% assign all_semesters = "" | split: "," %}
    {% for year_data in site.data.teaching.courses %}
      {% for semester in year_data.semesters %}
        {% assign all_semesters = all_semesters | push: semester %}
      {% endfor %}
    {% endfor %}

    {% for semester in all_semesters %}
      {% assign highlight_class = "" %}
      {% if semester.semester == current_semester_string %}
        {% assign highlight_class = "highlight-current" %}
      {% endif %}
      <div class="semester-section {{ highlight_class | strip }}">
        <h4 class="semester-title">{{ semester.semester }}</h4>
        {% for course in semester.courses %}
          <div class="course-card">
            <h5 class="course-title">{{ course.title }}</h5>
            {% if course.instructor %}
              <p class="course-instructor"><i class="fas fa-user-tie"></i> {{ course.instructor }}</p>
            {% endif %}
            <div class="course-body">
              {% if course.description and course.description != "" %}
                <p>{{ course.description }}</p>
              {% endif %}
              {% if course.links or course.pdfs %}
                <div class="course-resources">
                  {% for link in course.links %}
                    <a href="{{ link.url }}" class="resource-link" target="_blank" rel="noopener">
                      <i class="fas fa-external-link-alt"></i> {{ link.label | default: "More Info" }}
                    </a>
                  {% endfor %}
                  {% for pdf in course.pdfs %}
                    <a href="{{ pdf.file | relative_url }}" class="resource-link" target="_blank" rel="noopener">
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
  </div>
</div>
