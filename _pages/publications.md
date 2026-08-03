---
layout: page
permalink: "/publications/"
nav: true
nav_order: 5
show_title: false
mathjax: true
order: 100
title: Publications
description: "Browse the comprehensive list of publications from the Computational Arithmetic Geometry research group, including journal articles, preprints, and books."
excerpt_separator: ""
scripts:
  - /assets/js/publication-search.js
---

<div class="publications-container">
  <section class="publication-search-panel" aria-labelledby="publications-heading">
    <div class="publication-search-heading">
      <div class="publication-search-heading-icon" aria-hidden="true">
        <i class="fas fa-book-open"></i>
      </div>
      <div>
        <span class="publication-search-eyebrow">Research output</span>
        <h1 id="publications-heading">Publications</h1>
        <p>Browse articles, preprints, books, and software from the research group.</p>
      </div>
    </div>
    <form class="publication-search" role="search" aria-label="Search publications" novalidate>
      <label for="publication-search-input">Search the publication archive</label>
      <div class="publication-search-control">
        <i class="fas fa-search" aria-hidden="true"></i>
        <input
          id="publication-search-input"
          type="search"
          inputmode="search"
          autocomplete="off"
          placeholder="Title, author, journal, year, status, or MR number"
          aria-controls="publication-grid"
          aria-describedby="publication-result-count"
        >
        <button type="button" class="publication-search-clear" aria-label="Clear publication search" hidden>Clear</button>
      </div>
    </form>
    <div class="search-results-header" aria-live="polite" aria-atomic="true">
      <i class="fas fa-list" aria-hidden="true"></i>
      <span class="results-count" id="publication-result-count">{{ site.data.publications.publications.size }} publications</span>
    </div>
  </section>
  <div class="publication-grid" id="publication-grid">
    {% assign all_pubs = site.data.publications.publications %}
    {% assign pubs_with_year = all_pubs | where_exp: "item", "item.year != nil and item.year != ''" %}
    {% assign pubs_without_year = all_pubs | where_exp: "item", "item.year == nil or item.year == ''" %}

    {% assign sorted_pubs = pubs_with_year | sort: "year" | reverse %}

    {% for pub in sorted_pubs %}
      <div class="publication-card">
        <div class="publication-main">
          <div class="publication-title">
            <a href="/publications/{{ pub.title | slugify: 'latin' }}/" class="text-decoration-none text-dark">{{ pub.title | escape }}</a>
            {% if pub.year %}
              <span class="text-muted ms-2 small">({{ pub.year | escape }})</span>
            {% endif %}
          </div>
          <div class="publication-details">
            {{ pub.journal_details | escape }}
          </div>
          <div class="publication-authors">
            {{ pub.authors | escape }}
          </div>

        </div>
        <div class="publication-sidebar">
          {% if pub.status %}
            <span class="publication-status text-decoration-none badge-custom badge-custom-{{ pub.status | slugify: 'latin' }}">
              <i class="fas {% case pub.status %}{% when 'Journal Article' %}fa-newspaper{% when 'Book' %}fa-book{% when 'Submitted' %}fa-file-import{% when 'Preprint' %}fa-file-alt{% else %}fa-file{% endcase %}"></i> {{ pub.status | escape }}
            </span>
          {% endif %}
          {% if pub.mr_number and pub.mr_number != "" %}
          <a href="https://mathscinet.ams.org/mathscinet/article?mr={{ pub.mr_number | remove: 'MR' | escape }}" target="_blank" rel="noopener noreferrer" class="btn-custom btn-custom-outline btn-custom-sm">
            {{ pub.mr_number | escape }}
          </a>
          {% endif %}
          {% if pub.type == "Article" %}
            <span class="badge-custom badge-custom-danger">
              <i class="fas fa-file-pdf"></i> Article
            </span>
          {% endif %}
        </div>
      </div>
    {% endfor %}

    {% for pub in pubs_without_year %}
      <div class="publication-card">
        <div class="publication-main">
          <div class="publication-title">
            <a href="/publications/{{ pub.title | slugify: 'latin' }}/" class="text-decoration-none text-dark">{{ pub.title | escape }}</a>
            {% if pub.year %}
              <span class="text-muted ms-2 small">({{ pub.year | escape }})</span>
            {% endif %}
          </div>
          <div class="publication-details">
            {{ pub.journal_details | escape }}
          </div>
          <div class="publication-authors">
            {{ pub.authors | escape }}
          </div>

        </div>
        <div class="publication-sidebar">
          {% if pub.status %}
            <span class="publication-status text-decoration-none badge-custom badge-custom-{{ pub.status | slugify: 'latin' }}">
              <i class="fas {% case pub.status %}{% when 'Journal Article' %}fa-newspaper{% when 'Book' %}fa-book{% when 'Submitted' %}fa-file-import{% when 'Preprint' %}fa-file-alt{% else %}fa-file{% endcase %}"></i> {{ pub.status | escape }}
            </span>
          {% endif %}
          {% if pub.mr_number and pub.mr_number != "" %}
          <a href="https://mathscinet.ams.org/mathscinet/article?mr={{ pub.mr_number | remove: 'MR' | escape }}" target="_blank" rel="noopener noreferrer" class="btn-custom btn-custom-outline btn-custom-sm">
            {{ pub.mr_number | escape }}
          </a>
          {% endif %}
          {% if pub.type == "Article" %}
            <span class="badge-custom badge-custom-danger">
              <i class="fas fa-file-pdf"></i> Article
            </span>
          {% endif %}
        </div>
      </div>
    {% endfor %}
  </div>
  <p class="publication-search-empty" hidden>No publications match your search.</p>

  {% if site.data.publications.software %}
  <div class="software-section mt-5">
    <h2>Software Packages</h2>
    <div class="publication-grid">
      {% for software in site.data.publications.software %}
        {% assign safe_software_link = software.link | sanitize_url %}
        {% assign safe_thesis_link = software.thesis | sanitize_url %}
        <div class="publication-card">
          <div class="publication-main">
            <div class="publication-title">
              {% if software.link and safe_software_link != "#" %}
                <a href="{{ safe_software_link | escape }}" target="_blank" rel="noopener noreferrer" class="text-decoration-none text-dark">{{ software.title | escape }}</a>
              {% else %}
                {{ software.title | escape }}
              {% endif %}
            </div>
            <div class="publication-details">
              {{ software.description | markdownify }}
            </div>
            <div class="publication-authors">
              By {{ software.author | escape }}
            </div>
            {% if software.thesis and safe_thesis_link != "#" %}
            <div class="publication-links mt-2">
               <a href="{{ safe_thesis_link | escape }}" target="_blank" rel="noopener noreferrer">Thesis</a>
            </div>
            {% endif %}
          </div>
          <div class="publication-sidebar">
             {% if software.link and safe_software_link != "#" %}
             <a href="{{ safe_software_link | escape }}" target="_blank" rel="noopener noreferrer" class="btn-custom btn-custom-outline btn-custom-sm">
                <i class="fas fa-code"></i> {{ software.link_text | escape }}
             </a>
             {% endif %}
          </div>
        </div>
      {% endfor %}
    </div>
  </div>
  {% endif %}
</div>

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "CollectionPage",
  "url": {{ page.url | absolute_url | jsonify }},
  "mainEntity": {
    "@type": "ItemList",
    "numberOfItems": {{ site.data.publications.publications.size }},
    "itemListElement": [
    {% for pub in site.data.publications.publications %}
    {% assign pub_slug = pub.title | slugify: 'latin' %}
    {
      "@type": "ListItem",
      "position": {{ forloop.index }},
      "name": {{ pub.title | jsonify }},
      "url": {{ '/publications/' | append: pub_slug | append: '/' | absolute_url | jsonify }}
    }{% unless forloop.last %},{% endunless %}
    {% endfor %}
    ]
  }
}
</script>
