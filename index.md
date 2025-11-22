---
layout: page
title: "Computational Arithmetic Geometry"
description: "Official website of the Computational Arithmetic Geometry research group at Heidelberg University, led by Prof. Dr. Gebhard Böckle. Discover our research, publications, and team."
permalink: /
nav_order: 1
---

<div class="hero-header">
  <img src="{{ site.data.home.hero.image | relative_url }}" alt="Panoramic view of Heidelberg, home to the Computational Arithmetic Geometry research group at Heidelberg University." class="hero-image">
  <div class="hero-overlay">
    <div class="hero-content">
      <h1 class="hero-title">{{ site.data.home.hero.title }}</h1>
      <p class="hero-subtitle">{{ site.data.home.hero.subtitle }}</p>
      <p class="hero-description">{{ site.data.home.hero.description }}</p>
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
      <h3>{{ card.title }}</h3>
    </div>
    <div class="card-body">
      <p>{{ card.content }}</p>
    </div>
    <div class="card-footer">
      <a href="{{ card.link | relative_url }}" class="card-link">
        <i class="{{ card.link_icon }}" aria-hidden="true"></i>{{ card.link_text }}
      </a>
    </div>
  </div>
  {% endfor %}
</div>
