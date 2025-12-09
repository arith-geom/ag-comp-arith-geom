---
layout: page
permalink: /links/
nav: true
nav_order: 4
title: Links
description: "Useful links to external resources, number theory tools, and related research groups."
excerpt_separator: ""
---

<div class="content-grid">
  {% for group in site.data.links.groups %}
  <div class="feature-card">
    <div class="card-header">
      <div class="card-icon">
        <i class="{{ group.icon }}" aria-hidden="true"></i>
      </div>
      <h3>{{ group.title }}</h3>
    </div>
    <div class="card-body">
      <div class="links-container">
        {% for link in group.links %}
        <a href="{{ link.url | sanitize_url | escape }}" target="_blank" rel="noopener" class="link-item">
          <div class="link-title">{{ link.title | escape | markdownify }}</div>
          <span class="link-url">{{ link.url | escape }}</span>
        </a>
        {% endfor %}
      </div>
    </div>
  </div>
  {% endfor %}
</div>
