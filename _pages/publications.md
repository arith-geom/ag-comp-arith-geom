---
layout: page
permalink: "/publications/"
nav: true
nav_order: 5
show_title: false
order: 100
title: Publications
---
<div class="publications-page">
  <!-- Filter Controls -->
  <div class="filter-section">
    <div class="container-fluid px-3 px-md-4">
      <!-- Publications Search Bar -->
      <div class="pub-search-container">
        <div class="pub-search-wrapper">
          <input type="text" id="publications-search-input" class="pub-search-input" placeholder="Search titles, authors, keywords...">
          <i class="fas fa-search search-icon"></i>
          <button type="button" id="publications-clear-search" class="clear-search-btn" style="display: none;">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div id="publications-search-results-info" class="search-results-info" style="display: none;">
          <span id="publications-search-results-count"></span> publications found
        </div>
      </div>

      <!-- Quick Filter Buttons -->
      <div class="quick-filters">
        <button class="quick-filter-btn active" data-filter="all">All Publications</button>
        <button class="quick-filter-btn" data-filter="Journal Article">Journal Articles</button>
        <button class="quick-filter-btn" data-filter="Preprint">Preprints</button>
        <button class="quick-filter-btn" data-filter="Software">Software</button>
        <button class="quick-filter-btn" data-filter="Book">Books</button>
        <button class="quick-filter-btn" data-filter="Thesis">Theses</button>
      </div>

      <!-- Author Filter Display -->
      <div id="author-filter-display" class="author-filter-display" style="display: none;">
        <div class="author-filter-info">
          <i class="fas fa-user" aria-hidden="true"></i>
          <span>Filtering by author: <strong id="author-filter-name"></strong></span>
          <button type="button" id="clear-author-filter" class="clear-author-filter-btn">
            <i class="fas fa-times"></i>
            Clear Filter
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Publications Grid -->
  <div class="publications-content">
    <div class="container-fluid px-3 px-md-4">
      <!-- Loading State -->
      <div id="loading-state" class="loading-state" style="display: none;">
        <div class="spinner"></div>
        <p>Loading publications...</p>
      </div>

      <!-- Empty State -->
      <div id="empty-state" class="empty-state" style="display: none;">
        <i class="fas fa-search"></i>
        <h3>No publications found</h3>
        <p>Try adjusting your filters or search terms.</p>
      </div>

      <!-- Software Packages Status -->
      <!-- All software packages from Heidelberg website are included and up to date -->
      <!-- Last updated: 2025-08-04T10:26:31.561Z -->

      <!-- Back from detail view -->
      <div id="pub-detail-back" class="pub-detail-back" style="display: none;">
        <button type="button" id="pub-detail-back-btn" class="btn btn-outline-primary">
          <i class="fas fa-arrow-left"></i> Back to all publications
        </button>
      </div>

      <!-- Publications Grid -->
      <div id="publications-grid" class="publications-grid">
        {% assign sorted_publications = site.publications | sort: 'year' | reverse %}
        {% for publication in sorted_publications %}
          {% assign pub_key = publication.title | slugify | append: '-' | append: publication.year %}
          <div class="publication-card" data-type="{{ publication.type }}" data-year="{{ publication.year }}" data-pub-key="{{ pub_key }}">
            <div class="publication-header">
              <div class="publication-meta">
                <span class="publication-type">{{ publication.type }}</span>
                <span class="publication-status">{{ publication.status }}</span>
                <span class="publication-year">{{ publication.year }}</span>
      </div>
              <h3 class="publication-title">
                <a href="javascript:void(0)" class="publication-title-link" data-pub-key="{{ pub_key }}">{{ publication.title }}</a>
              </h3>
              <div class="publication-authors">{{ publication.authors }}</div>
              {% assign has_external_url = false %}

              {% assign has_links = false %}
              {% if publication.links and publication.links.size > 0 %}
                {% assign has_links = true %}
              {% endif %}
              {% if publication.pdf or publication.pdf_file or has_links %}
              <div class="publication-actions">


                {% if has_links %}
                  <div class="publication-links-badges">
                    {% for link in publication.links %}
                      {% assign label = link.label | default: 'Link' %}
                      {% assign href = link.url %}
                      {% if href %}
                        <a href="{{ href }}" class="link-badge" target="_blank" rel="noopener noreferrer">
                          <i class="fas fa-link"></i> {{ label }}
                        </a>
                      {% endif %}
                    {% endfor %}
                  </div>
                {% endif %}

                {% assign pdf_href = publication.pdf_file | default: publication.pdf %}
                {% if pdf_href %}
                  <a href="{% if pdf_href contains '://' %}{{ pdf_href }}{% else %}{{ pdf_href | relative_url }}{% endif %}" class="btn btn-sm btn-outline-secondary" target="_blank" rel="noopener noreferrer">
                    <i class="fas fa-file-pdf"></i> PDF
                  </a>
                {% endif %}
              </div>
              {% endif %}
              {% if publication.journal %}
                <div class="publication-venue">
                  {% if publication.journal_full %}{{ publication.journal_full }}{% else %}{{ publication.journal }}{% endif %}
                  {% if publication.volume %}, Volume {{ publication.volume }}{% endif %}
                  {% if publication.pages %}, {{ publication.pages }}{% endif %}
                  {% if publication.year %}, {{ publication.year }}{% endif %}
                </div>
              {% endif %}
              
              {% if publication.volume or publication.pages or publication.url %}
                <div class="publication-details">
                  {% if publication.volume %}<span class="detail-item">Volume: {{ publication.volume }}</span>{% endif %}
                  {% if publication.pages %}<span class="detail-item">Pages: {{ publication.pages }}</span>{% endif %}
                  {% if publication.url and publication.url != publication.pdf %}
                    {% assign url_str = publication.url %}
                    {% unless url_str contains site.url or url_str contains site.baseurl or url_str contains '/publications/' %}
                      {% unless url_str contains 'arxiv.org' %}
                        <span class="detail-item">URL: <a href="{{ url_str }}" target="_blank" rel="noopener noreferrer">View</a></span>
                      {% endunless %}
                    {% endunless %}
                  {% endif %}
      </div>
              {% endif %}
    </div>
            
            {% if publication.abstract or publication.content %}
              <div class="publication-body">
                {% if publication.abstract %}
                  <div class="publication-abstract">{{ publication.abstract }}</div>
                {% endif %}
                                {% if publication.content and publication.content != publication.abstract %}
                  <div class="publication-content">
                    <div class="publication-expandable">
                      <button class="publication-expand-btn" onclick="togglePublicationDetails(this)">
                        <span class="btn-text">Show full details</span>
                        <i class="fas fa-chevron-down btn-icon"></i>
                      </button>
                      <div class="publication-expanded-content" style="display: none;">
                        {{ publication.content | markdownify }}
                      </div>
                    </div>
                  </div>
                {% endif %}
              </div>
            {% endif %}
            
              
            
            <div class="publication-footer"></div>
          </div>
        {% endfor %}
      </div>
    </div>
  </div>
</div>

<!-- Publication Card Template -->
<template id="publication-card-template">
  <div class="publication-card">
    <div class="publication-header">
      <div class="publication-meta">
        <span class="publication-type"></span>
        <span class="publication-status"></span>
        <span class="publication-year"></span>
      </div>
      <h3 class="publication-title">
        <a href="javascript:void(0)" class="publication-link"></a>
      </h3>
      <div class="publication-authors"></div>
      <div class="publication-venue"></div>
    </div>
    
    <div class="publication-body">
      <div class="publication-abstract"></div>
      <div class="publication-keywords"></div>
    </div>
    
    <div class="publication-footer">
      <div class="publication-links">
        <!-- Links will be dynamically added -->
      </div>
      <div class="publication-metrics">
        <!-- Metrics will be dynamically added -->
      </div>
    </div>
  </div>
</template>

<style>
.publications-page {
  background: var(--bg-primary);
  min-height: 100vh;
  padding-top: 1rem;
}

.pub-detail-back {
  display: flex;
  justify-content: center;
  margin: 0.25rem 0 0.75rem 0;
}

.pub-detail-back .btn {
  min-width: 260px;
}

.filter-section {
  background: var(--bg-primary);
  border-bottom: 0;
  padding: 1rem 0 0.25rem 0;
  margin-bottom: 0.25rem;
}

.section-title {
  border-bottom: 3px solid var(--primary);
}

[data-theme="dark"] .filter-section,
body.dark-mode .filter-section {
  border-bottom: 0 !important;
}

[data-theme="dark"] .section-title,
body.dark-mode .section-title {
  border-bottom: 3px solid #111 !important;
}

.publications-content {
  margin-top: 0;
  padding-top: 0;
}

.pub-search-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 1rem;
  padding: 0 1rem;
}

.search-results-info {
  margin-top: 0.5rem;
  padding: 0.5rem 1.5rem;
  background: var(--bg-secondary);
  color: var(--text-secondary);
  border-radius: 2rem;
  font-size: 0.9rem;
  font-weight: 500;
  border: 1px solid var(--border-color);
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

.pub-search-wrapper {
  position: relative;
  max-width: 600px;
  width: 100%;
}

.pub-search-input {
  width: 100%;
  padding: 1.25rem 4rem 1.25rem 2rem;
  border: 3px solid var(--border-color);
  border-radius: 3rem;
  background: var(--bg-primary);
  color: var(--text-primary);
  font-size: 1.1rem;
  font-weight: 500;
  transition: all 0.3s ease;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  letter-spacing: 0.5px;
}

.pub-search-input::placeholder {
  color: var(--text-muted);
  font-weight: 400;
}

.pub-search-input:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 4px rgba(194, 32, 50, 0.15), 0 8px 25px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.pub-search-input:hover {
  border-color: var(--primary);
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.12);
}

.search-icon {
  position: absolute;
  right: 2rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--primary);
  font-size: 1.3rem;
  pointer-events: none;
  transition: all 0.3s ease;
}

.pub-search-input:focus + .search-icon {
  color: var(--primary-hover);
  transform: translateY(-50%) scale(1.1);
}

.clear-search-btn {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  background: var(--primary);
  color: white;
  border: none;
  border-radius: 50%;
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
  z-index: 10;
}

.clear-search-btn:hover {
  background: var(--primary-hover);
  transform: translateY(-50%) scale(1.1);
}

.clear-search-btn:active {
  transform: translateY(-50%) scale(0.95);
}

@media (max-width: 768px) {
  .search-input {
    padding: 1rem 3.5rem 1rem 1.5rem;
    font-size: 1rem;
  }
  
  .search-icon {
    right: 1.5rem;
    font-size: 1.2rem;
  }
  
  .clear-search-btn {
    width: 1.8rem;
    height: 1.8rem;
    font-size: 0.8rem;
  }
}

.quick-filters {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  justify-content: center;
  margin-top: 0.5rem;
}

.quick-filter-btn {
  padding: 0.5rem 1.5rem;
  border: 2px solid var(--primary);
  border-radius: 2rem;
  background: var(--primary);
  color: white;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(194, 32, 50, 0.2);
}

.quick-filter-btn:hover,
.quick-filter-btn.active {
  background: var(--primary-hover);
  color: white;
  border-color: var(--primary-hover);
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(194, 32, 50, 0.3);
}

.quick-filter-btn:not(.active) {
  background: var(--bg-primary);
  color: var(--primary);
  border-color: var(--primary);
}

.quick-filter-btn:not(.active):hover {
  background: var(--bg-secondary);
  color: var(--primary-hover);
  border-color: var(--primary-hover);
}

/* Author Filter Display */
.author-filter-display {
  margin-top: 1rem;
  padding: 1rem;
  background: var(--bg-secondary);
  border: 1px solid var(--primary);
  border-radius: var(--radius-md);
}

.author-filter-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: var(--text-primary);
}

.author-filter-info i {
  color: var(--primary);
  font-size: 1.1rem;
}

.clear-author-filter-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: var(--primary);
  color: var(--primary-text);
  border: none;
  padding: 0.5rem 1rem;
  border-radius: var(--radius-sm);
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: var(--transition-base);
  margin-left: auto;
}

.clear-author-filter-btn:hover {
  background: var(--primary-dark);
  transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
}

.loading-state {
  text-align: center;
  padding: 3rem;
  color: var(--text-muted);
}

.spinner {
  border: 4px solid var(--border-color);
  border-top: 4px solid var(--primary);
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: var(--text-muted);
}

.empty-state i {
  font-size: 3rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.empty-state h3 {
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}

.publications-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

@media (max-width: 768px) {
  .publications-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
}

.publications-page.detail-view-active #publications-grid {
  display: flex;
  justify-content: center;
  align-items: flex-start;
}

.publications-page.detail-view-active .filter-section {
  display: none;
}

.publication-card.detail-view {
  width: min(1000px, 92vw);
  max-width: 1000px;
  transform: translateY(0) scale(1.01);
  box-shadow: 0 1rem 2rem rgba(0,0,0,0.15);
  position: relative;
  z-index: 2;
}

.publication-card.detail-view .publication-body,
.publication-card.detail-view .publication-footer {
  background: var(--bg-primary);
}

.publication-card {
  background: var(--bg-primary);
  border-radius: 0.375rem;
  border: 1px solid var(--border-color);
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
  transition: all 0.2s ease;
  overflow: hidden;
  height: fit-content;
}

.publication-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
  border-color: #c22032;
}

.publication-header {
  padding: 1.25rem;
  border-bottom: 1px solid #dee2e6;
}

.publication-meta {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.publication-type,
.publication-status,
.publication-year {
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.8rem;
  font-weight: 600;
}

.publication-type {
  background: linear-gradient(135deg, #c22032 0%, #a01828 100%);
  color: white;
}

.publication-status {
  background: #f8f9fa;
  color: #6c757d;
  border: 1px solid #dee2e6;
}

.publication-year {
  background: #f8f9fa;
  color: #6c757d;
  border: 1px solid #dee2e6;
}



.publication-title {
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
  line-height: 1.3;
}

.publication-actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin: 0.5rem 0 0.25rem 0;
}

.publication-links-badges {
  display: flex;
  gap: 0.4rem;
  flex-wrap: wrap;
}

.link-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.25rem 0.6rem;
  border: 1px solid var(--border-color);
  border-radius: 9999px;
  background: var(--bg-secondary);
  color: var(--text-primary);
  text-decoration: none;
  font-size: 0.8rem;
}

.link-badge:hover {
  background: var(--bg-tertiary);
  border-color: var(--border-dark);
}

.publication-title a {
  color: #212529;
  text-decoration: none;
  transition: color 0.2s ease;
  cursor: pointer;
}

.publication-title a:hover {
  color: #c22032;
  text-decoration: underline;
}

.publication-title a[href="javascript:void(0)"] {
  cursor: default;
  color: #212529;
}

.publication-title a[href="javascript:void(0)"]:hover {
  color: #212529;
  text-decoration: none;
}

.publication-authors {
  color: #6c757d;
  font-style: italic;
  margin-bottom: 0.5rem;
  font-size: 0.95rem;
}

.publication-venue {
  color: #adb5bd;
  font-size: 0.9rem;
}

.publication-body {
  padding: 1.25rem;
}

.publication-abstract {
  color: #495057;
  line-height: 1.6;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}

.publication-keywords {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.keyword-tag {
  background: #e9ecef;
  color: #495057;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.8rem;
}

.publication-footer {
  padding: 1.25rem;
  border-top: 1px solid #dee2e6;
  background: #f8f9fa;
}

.publication-links {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin-bottom: 1rem;
}

.publication-link-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  background: #c22032;
  color: white !important;
  text-decoration: none;
  border-radius: 0.5rem;
  font-size: 0.9rem;
  font-weight: 600;
  transition: all 0.2s ease;
  border: 2px solid #c22032;
  box-shadow: 0 2px 4px rgba(194, 32, 50, 0.3);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.publication-link-btn:hover {
  background: #a01828;
  color: white !important;
  border-color: #a01828;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(194, 32, 50, 0.4);
  text-decoration: none;
}

.publication-link-btn:active {
  transform: translateY(0);
  box-shadow: 0 2px 4px rgba(194, 32, 50, 0.3);
}

.publication-link-btn i {
  font-size: 1rem;
  color: white !important;
}

.publication-metrics {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.metric-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #6c757d;
  font-size: 0.85rem;
}

.load-more-container {
  text-align: center;
  margin-top: 2rem;
}

.btn-outline-primary {
  border-color: #c22032;
  color: #c22032;
}

.btn-outline-primary:hover {
  background: #c22032;
  border-color: #c22032;
  color: white;
}

/* Expandable Content Styles */
.publication-expandable {
  margin-top: 1rem;
  border-top: 1px solid var(--border-color);
  padding-top: 1rem;
}

.publication-expand-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  width: 100%;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #c22032 0%, #a01828 100%);
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(194, 32, 50, 0.3);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
  position: relative;
  overflow: hidden;
}

.publication-expand-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s ease;
}

.publication-expand-btn:hover::before {
  left: 100%;
}

.publication-expand-btn:hover {
  background: linear-gradient(135deg, #a01828 0%, #8a1422 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(194, 32, 50, 0.4);
}

.publication-expand-btn:active {
  transform: translateY(0);
  box-shadow: 0 2px 8px rgba(194, 32, 50, 0.3);
}

.publication-expand-btn.expanded {
  background: linear-gradient(135deg, #8a1422 0%, #6f101b 100%);
  border-radius: 0.5rem 0.5rem 0 0;
}

.publication-expand-btn .btn-text {
  font-weight: 600;
  letter-spacing: 0.5px;
}

.publication-expand-btn .btn-icon {
  font-size: 0.8rem;
  transition: transform 0.3s ease;
  color: white;
}

/* Ensure expand button text is white in light mode (override global span color) */
.publication-expand-btn,
.publication-expand-btn .btn-text,
.publication-expand-btn .btn-icon {
  color: #ffffff !important;
}

.publication-expanded-content {
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-top: none;
  border-radius: 0 0 0.5rem 0.5rem;
  padding: 1.5rem;
  margin-top: -1px;
  animation: slideDown 0.3s ease-out;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
    max-height: 0;
  }
  to {
    opacity: 1;
    transform: translateY(0);
    max-height: 1000px;
  }
}

@keyframes slideUp {
  from {
    opacity: 1;
    transform: translateY(0);
    max-height: 1000px;
  }
  to {
    opacity: 0;
    transform: translateY(-10px);
    max-height: 0;
  }
}

.publication-expanded-content h1,
.publication-expanded-content h2,
.publication-expanded-content h3,
.publication-expanded-content h4,
.publication-expanded-content h5,
.publication-expanded-content h6 {
  color: var(--text-primary);
  margin-top: 1.5rem;
  margin-bottom: 0.75rem;
  font-weight: 600;
}

.publication-expanded-content h1:first-child,
.publication-expanded-content h2:first-child,
.publication-expanded-content h3:first-child,
.publication-expanded-content h4:first-child,
.publication-expanded-content h5:first-child,
.publication-expanded-content h6:first-child {
  margin-top: 0;
}

.publication-expanded-content p {
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 1rem;
}

.publication-expanded-content ul,
.publication-expanded-content ol {
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 1rem;
  padding-left: 1.5rem;
}

.publication-expanded-content li {
  margin-bottom: 0.5rem;
}

.publication-expanded-content strong,
.publication-expanded-content b {
  color: var(--text-primary);
  font-weight: 600;
}

.publication-expanded-content em,
.publication-expanded-content i {
  color: var(--text-secondary);
  font-style: italic;
}

.publication-expanded-content code {
  background: var(--bg-tertiary);
  color: var(--text-primary);
  padding: 0.2rem 0.4rem;
  border-radius: 0.25rem;
  font-size: 0.85rem;
  font-family: 'Courier New', monospace;
}

.publication-expanded-content pre {
  background: var(--bg-tertiary);
  border: 1px solid var(--border-color);
  border-radius: 0.5rem;
  padding: 1rem;
  overflow-x: auto;
  margin: 1rem 0;
}

.publication-expanded-content pre code {
  background: none;
  padding: 0;
  border-radius: 0;
}

.publication-expanded-content blockquote {
  border-left: 4px solid #c22032;
  padding-left: 1rem;
  margin: 1rem 0;
  color: var(--text-secondary);
  font-style: italic;
}

.publication-expanded-content a {
  color: #c22032;
  text-decoration: none;
  transition: color 0.2s ease;
}

.publication-expanded-content a:hover {
  color: #a01828;
  text-decoration: underline;
}

/* Dark mode support */
[data-theme="dark"] .publication-expanded-content,
body.dark-mode .publication-expanded-content {
  background: var(--bg-secondary);
  border-color: var(--border-color);
}

[data-theme="dark"] .publication-expand-btn,
body.dark-mode .publication-expand-btn {
  background: linear-gradient(135deg, #c22032 0%, #a01828 100%);
}

[data-theme="dark"] .publication-expand-btn:hover,
body.dark-mode .publication-expand-btn:hover {
  background: linear-gradient(135deg, #a01828 0%, #8a1422 100%);
}

[data-theme="dark"] .publication-expand-btn.expanded,
body.dark-mode .publication-expand-btn.expanded {
  background: linear-gradient(135deg, #8a1422 0%, #6f101b 100%);
}


</style>

<script>
// Toggle publication details
function togglePublicationDetails(button) {
  const expandable = button.closest('.publication-expandable');
  const content = expandable.querySelector('.publication-expanded-content');
  const btnText = button.querySelector('.btn-text');
  const btnIcon = button.querySelector('.btn-icon');
  
  // Add smooth animation
  if (content.style.display === 'block' || content.style.display === '') {
    // Hide content
    content.style.display = 'block'; // Ensure it's visible for animation
    content.style.animation = 'slideUp 0.3s ease-out forwards';
    
    setTimeout(() => {
      content.style.display = 'none';
      content.style.animation = '';
    }, 300);
    
    btnText.textContent = 'Show full details';
    btnIcon.style.transform = 'rotate(0deg)';
    button.classList.remove('expanded');
  } else {
    // Show content
    content.style.display = 'block';
    content.style.animation = 'slideDown 0.3s ease-out';
    
    btnText.textContent = 'Hide details';
    btnIcon.style.transform = 'rotate(180deg)';
    button.classList.add('expanded');
  }
}

// Initialize expandable content on page load
document.addEventListener('DOMContentLoaded', function() {
  // Ensure all expanded content is hidden by default
  const expandedContents = document.querySelectorAll('.publication-expanded-content');
  expandedContents.forEach(content => {
    content.style.display = 'none';
  });
});

// Publications Manager for CMS-managed publications
class PublicationsManager {
  constructor() {
    this.publications = [];
    this.filteredPublications = [];
    this.filters = {
      search: '',
      type: 'all',
      author: '',
      pubKey: ''
    };
  }
  
  init() {
    console.log('Initializing PublicationsManager for CMS publications...');
    this.loadPublicationsFromDOM();
    this.bindEvents();
    this.checkAuthorFilter();
    this.checkPublicationParam();
    this.applyFilters();
    console.log('PublicationsManager initialized successfully');
  }
  
  loadPublicationsFromDOM() {
    // Get all publication cards from the DOM
    const publicationCards = document.querySelectorAll('.publication-card');
    this.publications = Array.from(publicationCards).map(card => {
      return {
        element: card,
        type: card.dataset.type,
        year: parseInt(card.dataset.year),
        title: card.querySelector('.publication-title').textContent,
        authors: card.querySelector('.publication-authors').textContent,
        abstract: card.querySelector('.publication-abstract')?.textContent || '',
        key: card.dataset.pubKey
      };
    });
    
    console.log(`📖 Loaded ${this.publications.length} publications from DOM`);
  }
  
  bindEvents() {
    // Publications search input with debouncing
    let searchTimeout;
    const searchInput = document.getElementById('publications-search-input');
    const clearSearchBtn = document.getElementById('publications-clear-search');
    
    if (searchInput) {
      console.log('✅ Publications search input found and bound');
      searchInput.addEventListener('input', (e) => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
          this.filters.search = e.target.value.toLowerCase().trim();
          console.log('🔍 Publications search term:', this.filters.search);
          
          // Show/hide clear button
          if (clearSearchBtn) {
            if (this.filters.search.length > 0) {
              clearSearchBtn.style.display = 'flex';
            } else {
              clearSearchBtn.style.display = 'none';
            }
          }
          
          this.applyFilters();
        }, 300);
      });
      
      // Also listen for Enter key
      searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
          this.filters.search = e.target.value.toLowerCase().trim();
          console.log('🔍 Publications search term (Enter):', this.filters.search);
          this.applyFilters();
        }
      });
    } else {
      console.error('❌ Publications search input not found');
    }
    
    // Clear search button
    if (clearSearchBtn) {
      clearSearchBtn.addEventListener('click', () => {
        if (searchInput) {
          searchInput.value = '';
          this.filters.search = '';
          clearSearchBtn.style.display = 'none';
          this.applyFilters();
          searchInput.focus();
        }
      });
    }
    
    // Quick filter buttons
    const quickFilterButtons = document.querySelectorAll('.quick-filter-btn');
    
    quickFilterButtons.forEach((btn, index) => {
      btn.addEventListener('click', (e) => {
        // Remove active class from all buttons
        document.querySelectorAll('.quick-filter-btn').forEach(b => b.classList.remove('active'));
        
        // Add active class to clicked button
        e.target.classList.add('active');
        
        const filter = e.target.dataset.filter;
        this.applyQuickFilter(filter);
      });
    });
    
    // Clear author filter button
    const clearAuthorFilterBtn = document.getElementById('clear-author-filter');
    if (clearAuthorFilterBtn) {
      clearAuthorFilterBtn.addEventListener('click', () => {
        this.clearAuthorFilter();
        this.applyFilters();
      });
    }
  }
  
  checkAuthorFilter() {
    // Check for author parameter in URL
    const urlParams = new URLSearchParams(window.location.search);
    const authorParam = urlParams.get('author');
    
    if (authorParam) {
      this.filters.author = decodeURIComponent(authorParam);
      this.showAuthorFilter();
      console.log('🔍 Author filter applied:', this.filters.author);
    }
  }

  checkPublicationParam() {
    const urlParams = new URLSearchParams(window.location.search);
    const pubParam = urlParams.get('pub');
    if (pubParam) {
      this.filters.pubKey = decodeURIComponent(pubParam);
    }
  }
  
  showAuthorFilter() {
    const authorFilterDisplay = document.getElementById('author-filter-display');
    const authorFilterName = document.getElementById('author-filter-name');
    
    if (authorFilterDisplay && authorFilterName) {
      authorFilterName.textContent = this.filters.author;
      authorFilterDisplay.style.display = 'block';
    }
  }
  
  clearAuthorFilter() {
    this.filters.author = '';
    const authorFilterDisplay = document.getElementById('author-filter-display');
    if (authorFilterDisplay) {
      authorFilterDisplay.style.display = 'none';
    }
    
    // Remove author parameter from URL
    const url = new URL(window.location);
    url.searchParams.delete('author');
    window.history.replaceState({}, '', url);
  }
  
  applyFilters() {
    console.log('Applying filters:', this.filters);
    
    this.filteredPublications = this.publications.filter(pub => {
      // Type filter
      if (this.filters.type && this.filters.type !== 'all' && pub.type !== this.filters.type) {
        return false;
      }
      
      // Author filter
      if (this.filters.author && this.filters.author.length > 0) {
        const authorName = this.filters.author.toLowerCase();
        const publicationAuthors = pub.authors.toLowerCase();
        
        if (!publicationAuthors.includes(authorName)) {
          return false;
        }
      }
      
      // Publication key filter (single publication detail view)
      if (this.filters.pubKey && this.filters.pubKey.length > 0) {
        if (pub.key !== this.filters.pubKey) {
          return false;
        }
      }

      // Search filter
      if (this.filters.search && this.filters.search.length > 0) {
        const searchTerm = this.filters.search;
        const searchableText = [
          pub.title || '',
          pub.authors || '',
          pub.abstract || ''
        ].join(' ').toLowerCase();
        
        if (!searchableText.includes(searchTerm)) {
          return false;
        }
      }
      
      return true;
    });
    
    console.log('Filtered publications count:', this.filteredPublications.length);
    this.renderPublications();
    this.updateDetailState();
  }
  
  applyQuickFilter(filter) {
    this.filters.type = filter;
    this.applyFilters();
  }
  
  renderPublications() {
    console.log('Rendering publications...', this.filteredPublications.length);
    const grid = document.getElementById('publications-grid');
    const emptyState = document.getElementById('empty-state');
    const searchResultsInfo = document.getElementById('publications-search-results-info');
    const searchResultsCount = document.getElementById('publications-search-results-count');
    
    // Update search results info
    if (searchResultsInfo && searchResultsCount) {
      if (this.filters.search && this.filters.search.length > 0) {
        searchResultsCount.textContent = this.filteredPublications.length;
        searchResultsInfo.style.display = 'block';
        console.log('📊 Publications search results:', this.filteredPublications.length);
      } else {
        searchResultsInfo.style.display = 'none';
      }
    }
    
    // Show/hide publications based on filters
    this.publications.forEach(pub => {
      const isVisible = this.filteredPublications.includes(pub);
      pub.element.style.display = isVisible ? 'block' : 'none';
      pub.element.classList.toggle('detail-view', this.filteredPublications.length === 1 && isVisible);
    });
    
    // Show/hide empty state
    if (emptyState) {
      if (this.filteredPublications.length === 0) {
        emptyState.style.display = 'block';
      } else {
        emptyState.style.display = 'none';
      }
    }
  }

  updateDetailState() {
    const page = document.querySelector('.publications-page');
    const back = document.getElementById('pub-detail-back');
    if (!page || !back) return;
    if (this.filteredPublications.length === 1) {
      page.classList.add('detail-view-active');
      back.style.display = 'flex';
      // Ensure expanded details and scroll to top
      this.ensureExpandedDetail();
      page.scrollIntoView({ behavior: 'smooth', block: 'start' });
    } else {
      page.classList.remove('detail-view-active');
      back.style.display = 'none';
      this.collapseAllDetails();
    }
  }

  ensureExpandedDetail() {
    if (this.filteredPublications.length !== 1) return;
    const card = this.filteredPublications[0].element;
    if (!card) return;
    const btn = card.querySelector('.publication-expand-btn');
    const content = card.querySelector('.publication-expanded-content');
    if (content) {
      content.style.display = 'block';
      content.style.animation = '';
    }
    if (btn) {
      btn.classList.add('expanded');
      const btnText = btn.querySelector('.btn-text');
      if (btnText) btnText.textContent = 'Hide details';
      const btnIcon = btn.querySelector('.btn-icon');
      if (btnIcon) btnIcon.style.transform = 'rotate(180deg)';
    }
  }

  collapseAllDetails() {
    this.publications.forEach(p => {
      const btn = p.element.querySelector('.publication-expand-btn');
      const content = p.element.querySelector('.publication-expanded-content');
      if (content) {
        content.style.display = 'none';
        content.style.animation = '';
      }
      if (btn) {
        btn.classList.remove('expanded');
        const btnText = btn.querySelector('.btn-text');
        if (btnText) btnText.textContent = 'Show full details';
        const btnIcon = btn.querySelector('.btn-icon');
        if (btnIcon) btnIcon.style.transform = 'rotate(0deg)';
      }
    });
  }
}

// Initialize the publications manager when the page loads
document.addEventListener('DOMContentLoaded', () => {
  console.log('🚀 Initializing Publications Manager for CMS publications...');
  const manager = new PublicationsManager();
  manager.init();
  
  // Make manager globally accessible for debugging
  window.publicationsManager = manager;
  
  // Click-to-focus behavior: clicking title or card enters detail view
  document.getElementById('publications-grid')?.addEventListener('click', (e) => {
    const titleLink = e.target.closest('.publication-title-link');
    const card = e.target.closest('.publication-card');
    // Allow action links inside the card to work normally
    const actionLink = e.target.closest('.publication-links a, .publication-expand-btn, .publication-details a, .publication-expanded-content a');
    if (actionLink) return;
    if (titleLink || card) {
      const key = (titleLink?.dataset.pubKey) || card?.dataset.pubKey;
      if (key) {
        e.preventDefault();
        manager.filters.pubKey = key;
        // Reflect in URL without reload
        const url = new URL(window.location);
        url.searchParams.set('pub', key);
        window.history.replaceState({}, '', url);
        manager.applyFilters();
        // Ensure we are at the top where the detail view renders nicely
        document.querySelector('.publications-page')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }
  });

  // Back button
  document.getElementById('pub-detail-back-btn')?.addEventListener('click', () => {
    manager.filters.pubKey = '';
    const url = new URL(window.location);
    url.searchParams.delete('pub');
    window.history.replaceState({}, '', url);
    manager.applyFilters();
    // Scroll to top of grid
    document.getElementById('publications-grid')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
});
</script>

 