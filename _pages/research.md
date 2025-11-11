---
layout: page
permalink: "/research/"
nav: true
nav_order: 2
show_title: false
order: 100
title: Research Areas
description: "Explore the research areas of the Computational Arithmetic Geometry group at Heidelberg University, including Galois representations, modular forms, and function field arithmetic."
---
<div class="research-section research-page-override">
  <div class="content-grid">
    {% assign sorted_research = site.research | sort: 'title' %}
    {% for research_area in sorted_research %}
      <div class="feature-card">
        <div class="card-header">
          <div class="card-icon">
            <i class="fas fa-flask" aria-hidden="true"></i>
          </div>
          <h3>{{ research_area.title }}</h3>
        </div>
        <div class="card-body">
          {{ research_area.content | markdownify }}
          {% if research_area.keywords %}
            <div class="research-keywords mt-3">
              <strong>Keywords:</strong>
              {% for keyword in research_area.keywords %}
                <span class="keyword-pill">{{ keyword }}</span>
              {% endfor %}
            </div>
          {% endif %}
        </div>
        {% if research_area.related_publications %}
          <div class="card-footer">
            {% for pub_id in research_area.related_publications %}
              {% assign pub = site.publications | where: "id", pub_id | first %}
              {% if pub %}
                {% assign pub_key = pub.title | slugify | append: '-' | append: pub.year %}
                <a href="{{ '/publications/' | relative_url }}?pub={{ pub_key }}" class="card-link">
                  <i class="fas fa-file-alt" aria-hidden="true"></i> {{ pub.title | truncate: 30 }}
                </a>
              {% endif %}
            {% endfor %}
          </div>
        {% endif %}
      </div>
    {% endfor %}
  </div>
</div>