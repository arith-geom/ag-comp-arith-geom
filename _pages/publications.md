---
layout: page
permalink: "/publications/"
nav: true
nav_order: 5
show_title: false
order: 100
title: Publications
description: "Browse the comprehensive list of publications from the Computational Arithmetic Geometry research group, including journal articles, preprints, and books."
excerpt_separator: ""
---

<div class="publications-container">
  <div class="search-results-header">
    <span class="results-count">{{ site.data.publications.publications.size }} results</span>
  </div>
  <div class="publication-grid">
    {% assign all_pubs = site.data.publications.publications %}
    {% assign pubs_with_year = all_pubs | where_exp: "item", "item.year != nil and item.year != ''" %}
    {% assign pubs_without_year = all_pubs | where_exp: "item", "item.year == nil or item.year == ''" %}
    
    {% assign sorted_pubs = pubs_with_year | sort: "year" | reverse %}
    
    {% for pub in sorted_pubs %}
      <div class="publication-card">
        <div class="publication-main">
          <div class="publication-title">
            <a href="/publications/{{ pub.title | slugify }}/" class="text-decoration-none text-dark">{{ pub.title | escape }}</a>
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
            <span class="publication-status text-decoration-none badge-custom badge-custom-{{ pub.status | slugify }}">
              <i class="fas {% case pub.status %}{% when 'Journal Article' %}fa-newspaper{% when 'Book' %}fa-book{% when 'Submitted' %}fa-file-import{% when 'Preprint' %}fa-file-alt{% else %}fa-file{% endcase %}"></i> {{ pub.status | escape }}
            </span>
          {% endif %}
          {% if pub.mr_number and pub.mr_number != "" %}
          <a href="https://mathscinet.ams.org/mathscinet/article?mr={{ pub.mr_number | remove: 'MR' | escape }}" target="_blank" class="btn-custom btn-custom-outline btn-custom-sm">
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
            <a href="/publications/{{ pub.title | slugify }}/" class="text-decoration-none text-dark">{{ pub.title | escape }}</a>
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
            <span class="publication-status text-decoration-none badge-custom badge-custom-{{ pub.status | slugify }}">
              <i class="fas {% case pub.status %}{% when 'Journal Article' %}fa-newspaper{% when 'Book' %}fa-book{% when 'Submitted' %}fa-file-import{% when 'Preprint' %}fa-file-alt{% else %}fa-file{% endcase %}"></i> {{ pub.status | escape }}
            </span>
          {% endif %}
          {% if pub.mr_number and pub.mr_number != "" %}
          <a href="https://mathscinet.ams.org/mathscinet/article?mr={{ pub.mr_number | remove: 'MR' | escape }}" target="_blank" class="btn-custom btn-custom-outline btn-custom-sm">
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

  {% if site.data.publications.software %}
  <div class="software-section mt-5">
    <h2>Software Packages</h2>
    <div class="publication-grid">
      {% for software in site.data.publications.software %}
        <div class="publication-card">
          <div class="publication-main">
            <div class="publication-title">
              <a href="{{ software.link | escape }}" target="_blank" class="text-decoration-none text-dark">{{ software.title | escape }}</a>
            </div>
            <div class="publication-details">
              {{ software.description | markdownify }}
            </div>
            <div class="publication-authors">
              By {{ software.author | escape }}
            </div>
            {% if software.thesis %}
            <div class="publication-links mt-2">
               <a href="{{ software.thesis | escape }}" target="_blank">Thesis</a>
            </div>
            {% endif %}
          </div>
          <div class="publication-sidebar">
             <a href="{{ software.link | escape }}" target="_blank" class="btn-custom btn-custom-outline btn-custom-sm">
                <i class="fas fa-code"></i> {{ software.link_text | escape }}
             </a>
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