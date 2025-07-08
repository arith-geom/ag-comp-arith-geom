---
layout: page
title: Publications
permalink: /publications/
nav: true
---

<div class="publications-list">
  {% for pub in site.publications reversed %}
    <div class="publication-entry">
      <h3 class="publication-title">{{ pub.title }}</h3>
      <p class="publication-authors"><strong>Authors:</strong> {{ pub.authors }}</p>
      <p class="publication-meta">
        <span class="publication-type">{{ pub.publication_type }}</span> | 
        <span class="publication-details">{{ pub.publication_details }}</span> ({{ pub.year }})
      </p>
      {% if pub.doi %}
        <p class="publication-doi">
          <strong>DOI:</strong> <a href="https://doi.org/{{ pub.doi }}" target="_blank" rel="noopener">{{ pub.doi }}</a>
        </p>
      {% endif %}
      {% if pub.abstract %}
        <div class="publication-abstract">
          <p><strong>Abstract:</strong></p>
          {{ pub.abstract | markdownify }}
        </div>
      {% endif %}
      {% if pub.file %}
        <a href="{{ pub.file | relative_url }}" class="btn btn-primary btn-sm mt-2" target="_blank" rel="noopener">
          <i class="fas fa-file-pdf me-1"></i> View PDF
        </a>
      {% endif %}
    </div>
  {% endfor %}
</div>

<style>
.publications-list {
  padding-top: 2rem;
}
.publication-entry {
  margin-bottom: 2.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid var(--border-color);
}
.publication-title {
  font-size: 1.75rem;
  margin-bottom: 0.5rem;
}
.publication-authors {
  font-size: 1.1rem;
  color: var(--text-color-secondary);
}
.publication-meta {
  font-size: 1rem;
  color: var(--text-color-secondary);
  font-style: italic;
}
.publication-type {
  font-weight: 500;
}
.publication-doi {
  font-size: 1rem;
}
.publication-abstract {
  margin-top: 1rem;
  padding-left: 1rem;
  border-left: 3px solid var(--primary);
  background-color: var(--bg-secondary);
  padding: 1rem;
  border-radius: var(--radius-md);
}
</style> 