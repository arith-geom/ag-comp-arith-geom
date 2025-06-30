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
      {% if resource.author %}
        <p class="post-meta text-muted">By: {{ resource.author }}</p>
      {% endif %}
      {% if resource.description %}
        <p class="post-meta">{{ resource.description | strip_html | truncatewords: 40 }}</p>
      {% endif %}
    </div>
  {% endfor %}
</div> 