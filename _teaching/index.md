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
    {% assign sorted_years = site.data.teaching.courses | sort: "year" | reverse %}
    {% assign previous_university = "" %}
    
    {% for year_data in sorted_years %}
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
      
      {% comment %} Sort semesters: Winter should come before Summer {% endcomment %}
      {% assign winter_semesters = year_data.semesters | where: "semester", "Winter" %}
      {% assign summer_semesters = year_data.semesters | where: "semester", "Summer" %}
      {% assign other_semesters = year_data.semesters | where_exp: "item", "item.semester != 'Winter' and item.semester != 'Summer'" %}
      
      {% assign sorted_semesters = winter_semesters | concat: summer_semesters | concat: other_semesters %}

      {% for semester in sorted_semesters %}
        {% assign semester_title = semester.semester %}
        {% if semester.semester == "Winter" %}
           {% assign next_year_short = year_data.year | plus: 1 | modulo: 100 %}
           {% if next_year_short < 10 %}
             {% assign next_year_short = "0" | append: next_year_short %}
           {% endif %}
           {% assign semester_title = "Winter Semester " | append: year_data.year | append: "/" | append: next_year_short %}
        {% elsif semester.semester == "Summer" %}
           {% assign semester_title = "Summer Semester " | append: year_data.year %}
        {% endif %}

        {% assign highlight_class = "" %}
        {% if semester_title == current_semester_string %}
          {% assign highlight_class = "highlight-current" %}
        {% endif %}
        <div class="semester-section {{ highlight_class | strip }}">
          <h4 class="semester-title">{{ semester_title }}</h4>
          {% for course in semester.courses %}
            <div class="course-card position-relative">
              <h5 class="course-title">
                {% assign course_slug = course.title | slugify %}
                {% assign semester_slug = semester_title | slugify %}
                <a href="{{ '/teaching/' | append: year_data.year | append: '/' | append: semester_slug | append: '/' | append: course_slug | append: '/' | relative_url }}" class="text-decoration-none text-dark stretched-link">{{ course.title }}</a>
              </h5>
              {% if course.instructor %}
                <p class="course-instructor"><i class="fas fa-user-tie"></i> {{ course.instructor }}</p>
              {% endif %}
              <div class="course-body">
                {% if course.description and course.description != "" %}
                  <div>{{ course.description | markdownify }}</div>
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
