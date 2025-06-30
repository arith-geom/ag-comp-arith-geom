---
layout: page
title: Resources
permalink: /resources/
nav: true
---

<div class="post-list">
  {% for resource in site.resources %}
    <div class="post-item">
      <h3 class="post-title">
        <a href="{{ resource.url | relative_url }}">{{ resource.title }}</a>
      </h3>
      {% if resource.description %}
        <p class="post-meta">{{ resource.description }}</p>
      {% endif %}
    </div>
  {% endfor %}
</div> 