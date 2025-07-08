---
layout: page
title: Links
permalink: /links/
nav: true
---

Here are some links that may be of interest to students and researchers, managed from the CMS.

<div class="links-list mt-5">
  {% assign links_by_category = site.links | group_by: "category" | sort: "name" %}
  
  {% for category_group in links_by_category %}
    <h2 class="category-heading">{{ category_group.name }}</h2>
    <div class="list-group">
      {% for link in category_group.items %}
        <a href="{{ link.url }}" target="_blank" rel="noopener" class="list-group-item list-group-item-action">
          <div class="d-flex w-100 justify-content-between">
            <h5 class="mb-1">{{ link.title }}</h5>
          </div>
          {% if link.description %}
            <p class="mb-1">{{ link.description }}</p>
          {% endif %}
          <small class="text-muted">{{ link.url }}</small>
        </a>
      {% endfor %}
    </div>
  {% endfor %}
</div>

<style>
.category-heading {
  font-size: 2rem;
  margin-top: 3rem;
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid var(--primary);
}
</style> 