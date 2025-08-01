---
layout: page
title: Publications
permalink: /publications/
nav: true
nav_order: 4
---

<div class="publications-intro">
  <p class="lead translatable-content" data-translation-key="publications.intro">Publications and preprints of our research group:</p>
  <div class="publications-authors">
    <h4 class="translatable-content" data-translation-key="publications.group_members">Group Members</h4>
    <ul class="list-unstyled">
      <li><strong>Prof. Dr. Gebhard Böckle</strong> - <span class="translatable-content" data-translation-key="publications.group_leader">Group Leader</span></li>
      <li><strong>Dr. Barinder Banwait</strong> - <span class="translatable-content" data-translation-key="publications.postdoc">Postdoctoral Researcher</span></li>
      <li><strong>Dr. Peter Gräf</strong> - <span class="translatable-content" data-translation-key="publications.postdoc">Postdoctoral Researcher</span></li>
    </ul>
  </div>
  <hr>
  <p class="text-muted translatable-content" data-translation-key="publications.description">
    The following is a dynamic list of publications from our group, organized by year. New papers can be added through the CMS and will appear here automatically.
  </p>
</div>

<div class="publications-controls mb-4">
  <div class="row">
    <div class="col-md-6">
      <label for="publication-filter" class="form-label translatable-content" data-translation-key="publications.filter_by_year">Filter by year:</label>
      <select id="publication-filter" class="form-select">
        <option value="all" class="translatable-content" data-translation-key="publications.all_years">All Years</option>
        {% assign years = site.publications | map: "year" | uniq | sort | reverse %}
        {% for year in years %}
          <option value="{{ year }}">{{ year }}</option>
        {% endfor %}
      </select>
    </div>
    <div class="col-md-6">
      <label for="publication-search" class="form-label translatable-content" data-translation-key="publications.search_publications">Search publications:</label>
      <input type="text" id="publication-search" class="form-control" placeholder="Search by title, author, or keyword..." data-placeholder-en="Search by title, author, or keyword..." data-placeholder-de="Suche nach Titel, Autor oder Schlüsselwort...">
    </div>
  </div>
</div>

<div class="publications-list">
  {% assign pubs_by_year = site.publications | group_by: "year" | sort: "name" | reverse %}
  
  {% for year_group in pubs_by_year %}
    <div class="publication-year-group" data-year="{{ year_group.name }}">
      <h2 class="year-heading">{{ year_group.name }}</h2>
      <div class="publication-year-content">
        {% for pub in year_group.items %}
          <div class="publication-entry" data-title="{{ pub.title | downcase }}" data-authors="{{ pub.authors | downcase }}" data-keywords="{{ pub.tags | join: ' ' | downcase }}">
            <div class="publication-header">
              <h4 class="publication-title">{{ pub.title }}</h4>
              <div class="publication-meta">
                <span class="publication-authors"><em>{{ pub.authors }}</em></span>
                {% if pub.publication_type %}
                  <span class="publication-type">{{ pub.publication_type }}</span>
                {% endif %}
                {% if pub.publication_details %}
                  <span class="publication-details">{{ pub.publication_details }}</span>
                {% endif %}
                {% if pub.year %}
                  <span class="publication-year">{{ pub.year }}</span>
                {% endif %}
              </div>
            </div>
            
            <div class="publication-links">
              {% if pub.doi %}
                <a href="https://doi.org/{{ pub.doi }}" target="_blank" rel="noopener" class="btn btn-sm btn-outline-primary" aria-label="View DOI for {{ pub.title }}">
                  <i class="fas fa-external-link-alt me-1" aria-hidden="true"></i> DOI
                </a>
              {% endif %}
              {% if pub.file %}
                <a href="{{ pub.file | relative_url }}" class="btn btn-sm btn-primary" target="_blank" rel="noopener" aria-label="Download PDF for {{ pub.title }}">
                  <i class="fas fa-file-pdf me-1" aria-hidden="true"></i> PDF
                </a>
              {% endif %}
              {% if pub.abstract %}
                <button class="btn btn-sm btn-outline-secondary" data-bs-toggle="collapse" data-bs-target="#abstract-{{ forloop.index0 }}-{{ year_group.name }}" aria-expanded="false" aria-controls="abstract-{{ forloop.index0 }}-{{ year_group.name }}">
                  <i class="fas fa-eye me-1" aria-hidden="true"></i> <span class="translatable-content" data-translation-key="publications.show_abstract">Show Abstract</span>
                </button>
              {% endif %}
            </div>
            
            {% if pub.abstract %}
              <div class="publication-abstract mt-3">
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
    </div>
  {% endfor %}
</div>

<div class="publications-empty-state" style="display: none;">
  <div class="text-center py-5">
    <i class="fas fa-search fa-3x text-muted mb-3"></i>
    <h4>No publications found</h4>
    <p class="text-muted">Try adjusting your search criteria or year filter.</p>
  </div>
</div>

<style>
.publications-intro {
  margin-bottom: 2rem;
}

.publications-authors {
  margin: 1.5rem 0;
}

.publications-authors h4 {
  margin-bottom: 1rem;
  color: var(--text-primary);
}

.publications-authors ul {
  margin-left: 1rem;
}

.publications-authors li {
  margin-bottom: 0.5rem;
  color: var(--text-secondary);
}

.publications-controls {
  background: var(--bg-secondary);
  padding: 1.5rem;
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-color);
}

.year-heading {
  font-size: 2rem;
  margin-top: 3rem;
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid var(--primary);
  color: var(--text-primary);
}

.publication-entry {
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  border-radius: var(--radius-lg);
  background-color: var(--bg-primary);
  border: 1px solid var(--border-color);
  transition: all var(--transition-base);
}

.publication-entry:hover {
  box-shadow: var(--shadow-md);
  border-color: var(--primary);
  transform: translateY(-2px);
}

.publication-header {
  margin-bottom: 1rem;
}

.publication-title {
  font-size: 1.4rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
  line-height: 1.3;
}

.publication-meta {
  color: var(--text-secondary);
  font-size: 0.95rem;
  line-height: 1.5;
}

.publication-authors {
  display: block;
  margin-bottom: 0.5rem;
}

.publication-type,
.publication-details,
.publication-year {
  display: inline-block;
  margin-right: 1rem;
  font-weight: 500;
}

.publication-type {
  color: var(--primary);
  background-color: var(--bg-accent);
  padding: 0.25rem 0.5rem;
  border-radius: var(--radius-sm);
  font-size: 0.8rem;
}

.publication-links {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.publication-links a,
.publication-links button {
  min-height: 36px;
  display: inline-flex;
  align-items: center;
}

.publication-abstract .card {
  background-color: var(--bg-secondary);
  border-color: var(--border-color);
}

.publication-abstract .card-body {
  color: var(--text-secondary);
  font-size: 0.95rem;
  line-height: 1.6;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .publications-controls .row {
    gap: 1rem;
  }
  
  .publication-entry {
    padding: 1rem;
  }
  
  .publication-title {
    font-size: 1.2rem;
  }
  
  .publication-links {
    flex-direction: column;
  }
  
  .publication-links a,
  .publication-links button {
    width: 100%;
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .year-heading {
    font-size: 1.5rem;
  }
  
  .publication-meta {
    font-size: 0.9rem;
  }
  
  .publication-type,
  .publication-details,
  .publication-year {
    display: block;
    margin-right: 0;
    margin-bottom: 0.25rem;
  }
}
</style>

<script>
document.addEventListener('DOMContentLoaded', function() {
  const yearFilter = document.getElementById('publication-filter');
  const searchInput = document.getElementById('publication-search');
  const publicationEntries = document.querySelectorAll('.publication-entry');
  const yearGroups = document.querySelectorAll('.publication-year-group');
  const emptyState = document.querySelector('.publications-empty-state');
  
  function filterPublications() {
    const selectedYear = yearFilter.value;
    const searchTerm = searchInput.value.toLowerCase();
    let visibleCount = 0;
    
    publicationEntries.forEach(entry => {
      const year = entry.closest('.publication-year-group').dataset.year;
      const title = entry.dataset.title || '';
      const authors = entry.dataset.authors || '';
      const keywords = entry.dataset.keywords || '';
      
      const yearMatch = selectedYear === 'all' || year === selectedYear;
      const searchMatch = !searchTerm || 
        title.includes(searchTerm) || 
        authors.includes(searchTerm) || 
        keywords.includes(searchTerm);
      
      if (yearMatch && searchMatch) {
        entry.style.display = 'block';
        visibleCount++;
      } else {
        entry.style.display = 'none';
      }
    });
    
    // Show/hide year groups based on visibility
    yearGroups.forEach(group => {
      const hasVisibleEntries = group.querySelectorAll('.publication-entry[style*="display: block"]').length > 0;
      group.style.display = hasVisibleEntries ? 'block' : 'none';
    });
    
    // Show/hide empty state
    if (visibleCount === 0) {
      emptyState.style.display = 'block';
    } else {
      emptyState.style.display = 'none';
    }
  }
  
  // Event listeners
  yearFilter.addEventListener('change', filterPublications);
  searchInput.addEventListener('input', filterPublications);
  
  // Initialize
  filterPublications();
});
</script> 