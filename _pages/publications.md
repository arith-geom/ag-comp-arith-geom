---
layout: page
permalink: "/publications/"
nav: true
nav_order: 5
show_title: false
order: 100
title: Publications
description: "Browse the comprehensive list of publications from the Computational Arithmetic Geometry research group, including journal articles, preprints, and books."
---

<div class="publications-container">
  <div class="search-results-header">
    <span class="results-count">133 results</span>
  </div>
  <div class="publication-grid">
    {% for pub in site.data.publications.publications %}
      <div class="publication-card">
        <div class="publication-main">
          <div class="publication-title">
            {{ pub.title }}
          </div>
          <div class="publication-authors">
            {{ pub.authors }}
          </div>
          {% if pub.appendix %}
            <div class="publication-appendix">
              {{ pub.appendix }}
            </div>
          {% endif %}
          <div class="publication-details">
            {{ pub.journal_details }}
          </div>
          {% if pub.publisher_details %}
            <div class="publication-publisher">
              {{ pub.publisher_details }}
            </div>
          {% endif %}
          {% if pub.isbn %}
            <div class="publication-isbn">
              ISBN: {{ pub.isbn }}
            </div>
          {% endif %}
        </div>
        <div class="publication-sidebar">
          {% if pub.status %}
            <a href="#" class="publication-status publication-status-{{ pub.status | slugify }}">
              <i class="fas {% case pub.status %}{% when 'Journal Article' %}fa-newspaper{% when 'Book' %}fa-book{% when 'Submitted' %}fa-file-import{% when 'Preprint' %}fa-file-alt{% else %}fa-file{% endcase %}"></i> {{ pub.status }}
            </a>
          {% endif %}
          <a href="https://mathscinet.ams.org/mathscinet/article?mr={{ pub.mr_number | remove: 'MR' }}" target="_blank" class="publication-mr">
            {{ pub.mr_number }}
          </a>
          {% if pub.type == "Article" %}
            <a href="#" class="publication-type publication-type-pdf">
              <i class="fas fa-file-pdf"></i> Article
            </a>
          {% endif %}
        </div>
      </div>
    {% endfor %}
  </div>
</div>

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {% for pub in site.data.publications.publications %}
    {
      "@type": "ScholarlyArticle",
      "headline": "{{ pub.title | escape_once }}",
      "author": [
        {% assign authors = pub.authors | split: ', ' %}
        {% for author in authors %}
          {
            "@type": "Person",
            "name": "{{ author | strip }}"
          }{% unless forloop.last %},{% endunless %}
        {% endfor %}
      ],
      {% assign year = pub.journal_details | split: '(' | last | split: ')' | first %}
      "datePublished": "{{ year }}",
      "isPartOf": {
        "@type": "PublicationIssue",
        "name": "{{ pub.journal_details | escape_once }}"
      },
      "identifier": {
        "@type": "PropertyValue",
        "propertyID": "MathSciNet",
        "value": "{{ pub.mr_number }}"
      }
    }{% unless forloop.last %},{% endunless %}
    {% endfor %}
  ]
}
</script>