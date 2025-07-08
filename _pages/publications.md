---
layout: page
title: Publications
permalink: /publications/
nav: true
---

<div class="publications-intro">
  <p>Publications and preprints of our research group:</p>
  <ul>
    <li>Prof. Dr. Gebhard Böckle</li>
    <li>Dr. Barinder Banwait</li>
    <li>Dr. Peter Gräf</li>
  </ul>
  <hr>
  <p class="text-muted">
    The following is a dynamic list of publications from our group, organized by year. New papers can be added through the CMS and will appear here automatically.
  </p>
</div>

<div class="publications-list mt-5">
  {% assign pubs_by_year = site.publications | group_by: "year" | sort: "name" | reverse %}
  
  {% for year_group in pubs_by_year %}
    <h2 class="year-heading">{{ year_group.name }}</h2>
    <div class="publication-year-group">
      {% for pub in year_group.items %}
        <div class="publication-entry">
          <h4 class="publication-title">{{ pub.title }}</h4>
          <p class="publication-authors"><em>{{ pub.authors }}</em></p>
          <p class="publication-meta">
            <span class="publication-type">{{ pub.publication_type }}</span>
            {% if pub.publication_details %}
              | <span class="publication-details">{{ pub.publication_details }}</span>
            {% endif %}
          </p>
          <div class="publication-links">
            {% if pub.doi %}
              <a href="https://doi.org/{{ pub.doi }}" target="_blank" rel="noopener" class="btn btn-sm btn-outline-primary">DOI</a>
            {% endif %}
            {% if pub.file %}
              <a href="{{ pub.file | relative_url }}" class="btn btn-sm btn-primary" target="_blank" rel="noopener">
                <i class="fas fa-file-pdf me-1"></i> PDF
              </a>
            {% endif %}
          </div>
          {% if pub.abstract %}
            <div class="publication-abstract mt-3">
              <p>
                <a class="btn btn-sm btn-outline-secondary" data-bs-toggle="collapse" href="#abstract-{{ forloop.index0 }}-{{ year_group.name }}" role="button" aria-expanded="false" aria-controls="abstract-{{ forloop.index0 }}-{{ year_group.name }}">
                  Show Abstract
                </a>
              </p>
              <div class="collapse" id="abstract-{{ forloop.index0 }}-{{ year_group.name }}">
                <div class="card card-body">
                  {{ pub.abstract | markdownify }}
                </div>
              </div>
            </div>
          {% endif %}
        </div>
      {% endfor %}
    </div>
  {% endfor %}
</div>

<style>
.publications-intro {
  margin-bottom: 2rem;
}
.year-heading {
  font-size: 2rem;
  margin-top: 3rem;
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid var(--primary);
}
.publication-entry {
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  border-radius: var(--radius-md);
  background-color: var(--bg-secondary);
  border: 1px solid var(--border-color);
}
.publication-title {
  font-size: 1.4rem;
  font-weight: 600;
}
.publication-authors {
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}
.publication-meta {
  color: var(--text-color-secondary);
  margin-bottom: 1rem;
}
.publication-links a {
  margin-right: 0.5rem;
}
</style> 