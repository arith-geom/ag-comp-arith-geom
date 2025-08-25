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
    <div class="container-fluid px-3 px-md-4 publications-filter-container">
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
    <div class="container-fluid px-3 px-md-4 publications-content-container">
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
      <!-- All 0 publications from Heidelberg website are included and up to date -->
      <!-- Last updated: 2025-08-24T21:38:29.541488 -->

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
          {% assign pub_key = publication.title | slugify | append: '-' | append: publication.year | replace: '?', 'unknown' | replace: '2024', 'unknown' %}
          <div class="publication-card" data-type="{{ publication.type }}" {% if publication.year != "?" and publication.year != "2024" %}data-year="{{ publication.year }}"{% endif %} data-pub-key="{{ pub_key }}">
            <div class="publication-header">
              <div class="publication-main-content">
                <div class="publication-meta">
                  <span class="publication-type">{{ publication.type }}</span>
                  {% if publication.year != "?" and publication.year != "2024" %}
                    <span class="publication-year">{{ publication.year }}</span>
                  {% endif %}
                </div>
                <h3 class="publication-title">
                  {{ publication.title }}
                </h3>
                <div class="publication-authors">{{ publication.authors }}</div>

                {% if publication.abstract %}
                  <div class="publication-abstract">{{ publication.abstract }}</div>
                {% endif %}

                {% if publication.content %}
                  <div class="publication-content">
                    {{ publication.content | remove: "## Publication Details" | markdownify }}
                  </div>
                {% endif %}

                {% if publication.keywords %}
                  <div class="publication-keywords">
                    <strong>Keywords:</strong> {{ publication.keywords }}
                  </div>
                {% endif %}

                {% if publication.links or publication.pdfs %}
                  <div class="publication-actions">
                    {% if publication.links %}
                      {% for link in publication.links %}<a href="{{ link.url }}" target="_blank" class="publication-link-item">{{ link.label }}</a>{% endfor %}
                    {% endif %}
                    {% if publication.pdfs %}
                      {% for pdf in publication.pdfs %}<a href="{{ pdf.url }}" target="_blank" class="publication-pdf-item">{{ pdf.label }}</a>{% endfor %}
                    {% endif %}
                  </div>
                {% endif %}

                {% assign has_external_url = false %}
                {% assign has_links = false %}
                {% if publication.links and publication.links.size > 0 %}
                  {% assign has_links = true %}
                {% endif %}





              </div>


            </div>



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
  background: transparent;
  border: none;
  box-shadow: none;
  padding: 1rem 0 0.25rem 0;
  margin-bottom: 0.25rem;
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
  background: transparent;
  color: var(--text-secondary);
  border-radius: 2rem;
  font-size: 0.9rem;
  font-weight: 500;
  border: none;
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
  border: none;
  border-radius: 3rem;
  background: transparent;
  color: var(--text-primary);
  font-size: 1.1rem;
  font-weight: 500;
  transition: all 0.3s ease;
  box-shadow: none;
  letter-spacing: 0.5px;
}

.pub-search-input::placeholder {
  color: var(--text-muted);
  font-weight: 400;
}

.pub-search-input:focus {
  outline: none;
  border: none;
  background: transparent;
  box-shadow: none;
  transform: translateY(-2px);
}

.pub-search-input:hover {
  border: none;
  background: transparent;
  box-shadow: none;
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
  background: transparent;
  color: var(--text-primary);
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
  background: transparent;
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
  box-shadow: none;
}

.quick-filter-btn:hover,
.quick-filter-btn.active {
  background: var(--primary-hover);
  color: white;
  border-color: var(--primary-hover);
  transform: translateY(-2px);
  box-shadow: none;
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
  background: transparent;
  border: none;
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
  grid-template-columns: 1fr;
  gap: 0.25rem;
  margin-bottom: 1.5rem;
}

.publications-page.detail-view-active #publications-grid {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  width: 100%;
}

.publications-page.detail-view-active .filter-section {
  display: none;
}

.publications-page.detail-view-active .publications-content-container {
  padding-left: 0 !important;
  padding-right: 0 !important;
}

.publications-page.detail-view-active .publications-filter-container {
  padding-left: 0 !important;
  padding-right: 0 !important;
}

/* Full-screen width for detail view */
.publication-card.detail-view {
  width: 100% !important;
  max-width: 100% !important;
  min-width: 100% !important;
  transform: translateY(0) scale(1.01);
  box-shadow: 0 1rem 2rem rgba(0,0,0,0.15);
  position: relative;
  z-index: 2;
  margin: 0 !important;
}

/* Ensure expanded content uses full width */
.publication-card.detail-view .publication-expanded-content {
  width: 100% !important;
  max-width: 100% !important;
  min-width: 100% !important;
}

/* Responsive adjustments for full-screen detail view */
@media (max-width: 768px) {
  .publication-card.detail-view {
    width: 100vw !important;
    max-width: 100vw !important;
    min-width: 100vw !important;
    margin: 0 !important;
  }

  .publication-card.detail-view .publication-expanded-content {
    width: 100vw !important;
    max-width: 100vw !important;
    min-width: 100vw !important;
  }
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

/* Publication content styling */
.publication-content {
  padding: 0.125rem 0;
  margin: 0.125rem 0;
}





.publication-keywords {
  margin-bottom: 0.25rem;
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.publication-actions {
  margin-bottom: 0.5rem;
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  align-items: center;
  justify-content: flex-start;
}

.publication-link-item, .publication-pdf-item {
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.5rem;
  background-color: var(--bg-secondary);
  border-radius: 0.25rem;
  text-decoration: none;
  font-size: 0.9rem;
  white-space: nowrap;
  transition: all 0.2s ease;
}

.publication-link-item:hover, .publication-pdf-item:hover {
  background-color: #c22032;
  color: white;
}

.publication-header {
  padding: 0.5rem;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
}

.publication-main-content {
  flex: 1;
  min-width: 0; /* Allow flex item to shrink below its content size */
}

.publication-expand-section {
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.publication-meta {
  display: flex;
  gap: 0.4rem;
  margin-bottom: 0.5rem;
  flex-wrap: wrap;
}

.publication-type,
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



.publication-year {
  background: var(--bg-secondary);
  color: var(--text-muted);
  border: 1px solid var(--border-color);
}



.publication-title {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
  line-height: 1.3;
}

.publication-actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin: 0.2rem 0 0.1rem 0;
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

.publication-pdfs {
  display: flex;
  gap: 0.4rem;
  flex-wrap: wrap;
}

.publication-title a {
  color: var(--text-primary);
  text-decoration: none;
  transition: color 0.2s ease;
  cursor: pointer;
}

.publication-title a:hover {
  color: var(--primary);
  text-decoration: underline;
}

.publication-title a[href="javascript:void(0)"] {
  cursor: default;
  color: var(--text-primary);
}

.publication-title a[href="javascript:void(0)"]:hover {
  color: var(--text-primary);
  text-decoration: none;
}

.publication-authors {
  color: var(--text-muted);
  font-style: italic;
  margin-bottom: 0.2rem;
  font-size: 0.9rem;
}

.publication-venue {
  color: var(--text-muted);
  font-size: 0.9rem;
}

.publication-abstract {
  color: var(--text-secondary);
  line-height: 1.4;
  margin-bottom: 0.5rem;
  font-size: 0.85rem;
  max-height: 3.2rem;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.publication-keywords {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.keyword-tag {
  background: var(--bg-tertiary);
  color: var(--text-secondary);
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.8rem;
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
  color: var(--text-muted);
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

.publication-expand-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.25rem;
  width: fit-content;
  padding: 0.4rem 1rem;
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-hover) 100%);
  color: var(--primary-text);
  border: none;
  border-radius: 0.25rem;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 1px 4px rgba(194, 32, 50, 0.3);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
  position: relative;
  overflow: hidden;
  white-space: nowrap;
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
  background: linear-gradient(135deg, var(--primary-hover) 0%, var(--primary-dark) 100%);
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(194, 32, 50, 0.4);
}

.publication-expand-btn:active {
  transform: translateY(0);
  box-shadow: 0 1px 4px rgba(194, 32, 50, 0.3);
}

.publication-expand-btn.expanded {
  background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary-darker) 100%);
  border-radius: 0.25rem 0.25rem 0 0;
}

.publication-expand-btn .btn-text {
  font-weight: 600;
  letter-spacing: 0.5px;
}

.publication-expand-btn .btn-icon {
  font-size: 0.7rem;
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
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-top: none;
  border-radius: 0 0 0.375rem 0.375rem;
  padding: 1rem;
  margin-top: 0.25rem;
  animation: slideDown 0.3s ease-out;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
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



</style>

<script>
// Toggle publication details (detail view aware)
function togglePublicationDetails(button) {
  const manager = window.publicationsManager;
  const card = button.closest('.publication-card');
  const key = card?.dataset.pubKey;
  const btnText = button.querySelector('.btn-text');
  const btnIcon = button.querySelector('.btn-icon');
  const page = document.querySelector('.publications-page');
  const isDetailViewActive = page?.classList.contains('detail-view-active');
  const isCurrentDetailCard = isDetailViewActive && manager?.filters?.pubKey === key;

  // If we have the manager and a card key, use the single-card detail view as the toggle target
  if (manager && key) {
    // If we are already showing this card in detail view, hide it (return to list)
    if (isCurrentDetailCard) {
      manager.filters.pubKey = '';
      const url = new URL(window.location);
      url.searchParams.delete('pub');
      window.history.replaceState({}, '', url);
      manager.applyFilters();
      return;
    }

    // Otherwise, show this card in detail view
    manager.filters.pubKey = key;
    const url = new URL(window.location);
    url.searchParams.set('pub', key);
    window.history.replaceState({}, '', url);
    manager.applyFilters();
    return;
  }

  // Fallback: if manager not present, just toggle inline content
  const expandable = button.closest('.publication-expandable');
  const content = expandable?.querySelector('.publication-expanded-content');
  if (!content) return;
  if (content.style.display === 'block' || content.style.display === '') {
    content.style.display = 'block';
    content.style.animation = 'slideUp 0.3s ease-out forwards';
    setTimeout(() => {
      content.style.display = 'none';
      content.style.animation = '';
    }, 300);
    if (btnText) btnText.textContent = 'Show full details';
    if (btnIcon) btnIcon.style.transform = 'rotate(0deg)';
    button.classList.remove('expanded');
  } else {
    content.style.display = 'block';
    content.style.animation = 'slideDown 0.3s ease-out';
    if (btnText) btnText.textContent = 'Hide details';
    if (btnIcon) btnIcon.style.transform = 'rotate(180deg)';
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
    // DISABLED: Filtering system - using simple expand/collapse instead
    console.log('Filters disabled - using simple expand/collapse mode');

    // Just show all publications without filtering
    this.filteredPublications = this.publications;

    // Update the display to show all cards
    this.renderPublications();

    /*
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
    */
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
  
  // DISABLED: Complex click-to-focus behavior - using simple expand/collapse instead
  // Click-to-focus behavior: clicking title or card toggles single-card detail view
  /*
  const publicationsGrid = document.getElementById('publications-grid');
  if (publicationsGrid) {
    publicationsGrid.addEventListener('click', (e) => {
      const titleLink = e.target.closest('.publication-title-link');
      const card = e.target.closest('.publication-card');
      // Allow action links/buttons inside the card to work normally
      const actionOrExpand = e.target.closest(
        '.publication-actions a, .publication-links-badges a, .publication-pdfs a, .publication-links a, .publication-details a, .publication-expanded-content a, .publication-expand-btn'
      );
      if (actionOrExpand) return;
      if (!titleLink && !card) return;

      const key = (titleLink?.dataset.pubKey) || card?.dataset.pubKey;
      if (!key) return;

      e.preventDefault();
      // Toggle: if already focused on this card, clear; otherwise focus this card
      if (manager.filters.pubKey === key) {
        manager.filters.pubKey = '';
        const url = new URL(window.location);
        url.searchParams.delete('pub');
        window.history.replaceState({}, '', url);
        manager.applyFilters();
      } else {
        manager.filters.pubKey = key;
        const url = new URL(window.location);
        url.searchParams.set('pub', key);
        window.history.replaceState({}, '', url);
        manager.applyFilters();
        document.querySelector('.publications-page')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  }
  */

  // DISABLED: Back button functionality - using simple expand/collapse instead
  /*
  document.getElementById('pub-detail-back-btn')?.addEventListener('click', () => {
    manager.filters.pubKey = '';
    const url = new URL(window.location);
    url.searchParams.delete('pub');
    window.history.replaceState({}, '', url);
    manager.applyFilters();
    // Scroll to top of grid
    document.getElementById('publications-grid')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
  */

  // Expand/collapse functionality removed - all content is now always visible
</script>

 