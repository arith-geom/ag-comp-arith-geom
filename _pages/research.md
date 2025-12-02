---
layout: page
permalink: "/research/"
nav: true
nav_order: 2
show_title: false
order: 100
title: Research Areas
description: "Explore the research areas of the Computational Arithmetic Geometry group at Heidelberg University."
---

<div class="research-section">
  <div class="content-grid">
    
    {% for area in site.data.research.research_areas %}
    <div class="feature-card">
      <div class="card-header">
        <div class="card-icon">
          <i class="{{ area.icon }}" aria-hidden="true"></i>
        </div>
        <h3>{{ area.title | escape }}</h3>
      </div>
      <div class="card-body">
        {{ area.content | strip_html | markdownify }}
      </div>
    </div>
    {% endfor %}

  </div>
</div>

<style>
.feature-card .card-body {
  text-align: justify;
}
</style>