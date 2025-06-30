---
layout: page
title: Team Members
permalink: /members/
---
<div class="row">
  {% for member in site.members %}
    <div class="col-md-6">
      <div class="card mb-4">
        {% if member.photo %}
          <img src="{{ member.photo | relative_url }}" class="card-img-top" alt="{{ member.name }}">
        {% endif %}
        <div class="card-body">
          <h5 class="card-title">{{ member.name }}</h5>
          <h6 class="card-subtitle mb-2 text-muted">{{ member.role }}</h6>
          <p class="card-text">{{ member.bio | markdownify }}</p>
          {% if member.email %}
            <a href="mailto:{{ member.email }}" class="card-link">{{ member.email }}</a>
          {% endif %}
        </div>
      </div>
    </div>
  {% endfor %}
</div> 