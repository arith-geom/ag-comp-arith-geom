---
layout: page
title: "Computational Arithmetic Geometry"
description: "Official website of the Computational Arithmetic Geometry research group at Heidelberg University, led by Prof. Dr. Gebhard Böckle. Discover our research, publications, and team."
permalink: /
nav_order: 1
---

<div class="hero-header">
  <img src="{{ site.data.home.hero.image | relative_url }}" alt="Panoramic view of Heidelberg, home to the Computational Arithmetic Geometry research group at Heidelberg University." class="hero-image" loading="lazy">
  <div class="hero-overlay">
    <div class="hero-content">
      <h1 class="hero-title">{{ site.data.home.hero.title | escape }}</h1>
      <p class="hero-subtitle">{{ site.data.home.hero.subtitle | escape }}</p>
      <div class="hero-description">{{ site.data.home.hero.description | strip_html | markdownify }}</div>
    </div>
  </div>
</div>




<!-- Main Feature Cards -->
<div class="content-grid">
  {% for card in site.data.home.feature_cards %}
  <div class="feature-card">
    <div class="card-header">
      <div class="card-icon">
        <i class="{{ card.icon }}" aria-hidden="true"></i>
      </div>
      <h3>{{ card.title | escape }}</h3>
    </div>
    <div class="card-body">
      <div>{{ card.content | strip_html | markdownify }}</div>
    </div>
    <div class="card-footer">
      <a href="{{ card.link | relative_url }}" class="card-link">
        <i class="{{ card.link_icon }}" aria-hidden="true"></i>{{ card.link_text | escape }}
      </a>
    </div>
  </div>
  {% endfor %}
</div>
