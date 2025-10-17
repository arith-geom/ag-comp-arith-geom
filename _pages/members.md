---
layout: page
permalink: "/members/"
nav: true
nav_order: 3
show_title: false
title: Members
---

<div class="main-container members-page">
  {% for section in site.data.members.sections %}
    {% assign section_slug = section.title | slugify %}
    <div class="member-section member-section-{{ section_slug }}">
      <h2 class="section-title">{{ section.title }}</h2>
      <div class="content-grid {{ section_slug }}-grid">
        {% for member in section.members %}
          <div class="feature-card member-card">
            <div class="card-header">
              {% if section.title != "Former Members" %}
              <div class="member-photo-container">
                {% if member.photo %}
                  <img src="{{ member.photo | relative_url }}" alt="Photo of {{ member.name }}" class="member-photo">
                {% else %}
                  <div class="member-photo-placeholder"><i class="fas fa-user"></i></div>
                {% endif %}
              </div>
              {% endif %}
              <div class="member-header-info">
                <h3 class="member-name">{{ member.name }}</h3>
                <p class="member-role">{{ member.role }}</p>
              </div>
            </div>
            <div class="card-body">
              <p class="member-description">{{ member.description }}</p>
            </div>
            {% if member.links %}
            <div class="card-footer">
              <div class="member-links">
                {% for link in member.links %}
                  <a href="{{ link.url }}" class="btn-social" target="_blank" rel="noopener noreferrer" aria-label="{{ link.text }}">
                    <i class="{{ link.icon }}"></i>
                  </a>
                {% endfor %}
              </div>
            </div>
            {% endif %}
          </div>
        {% endfor %}
      </div>
    </div>
  {% endfor %}
</div>