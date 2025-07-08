---
layout: page
title: Resources
permalink: /resources/
nav: true
---

<div class="resource-list mt-5">
  {% for resource in site.resources %}
    <div class="resource-entry card mb-4">
      <div class="card-body">
        <h3 class="card-title">{{ resource.title }}</h3>
        {% if resource.description %}
          <p class="card-text">{{ resource.description | markdownify }}</p>
        {% endif %}
        {% if resource.url %}
          <a href="{{ resource.url }}" class="btn btn-primary" target="_blank" rel="noopener">
            <i class="fas fa-external-link-alt me-1"></i> Visit Resource
          </a>
        {% endif %}
      </div>
    </div>
  {% else %}
    <p>There are no resources available at this time.</p>
  {% endfor %}
</div> 