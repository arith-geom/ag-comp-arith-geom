---
layout: page
title: Research
permalink: /research/
nav: true
---

The research of our group is in **arithmetic geometry** and **number theory**. Below are some of our key research areas and topics. For more details, click on any of the topics to see a detailed description, related papers, and resources.

You can also browse the [publications](/publications) of our group members.

<div class="research-grid mt-5">
  {% for item in site.research %}
    <a href="{{ item.url | relative_url }}" class="research-card">
      <div class="card-body">
        <h4 class="card-title">{{ item.title }}</h4>
        {% if item.description %}
          <p class="card-text">{{ item.description | markdownify | strip_html | truncatewords: 25 }}</p>
        {% endif %}
        <span class="btn btn-sm btn-outline-primary">Read More</span>
      </div>
    </a>
  {% endfor %}
</div>

<style>
.research-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}
.research-card {
  display: block;
  text-decoration: none;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  background-color: var(--bg-primary);
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-base);
  height: 100%;
}
.research-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-md);
  border-color: var(--primary);
}
.research-card .card-body {
  padding: 1.5rem;
}
.research-card .card-title {
  font-size: 1.5rem;
  color: var(--primary);
  margin-bottom: 1rem;
}
.research-card .card-text {
  color: var(--text-secondary);
  font-size: 1rem;
}
</style> 