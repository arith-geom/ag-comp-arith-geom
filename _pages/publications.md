---
layout: page
title: Publications
permalink: /publications/
nav: true
nav_order: 5
---

<div class="publications-page">
  <!-- Header Section -->
  <div class="publications-header">
    <div class="container">
      <div class="publications-intro">
        <h1>Publications & Research Output</h1>
        <p class="lead">Discover the latest research papers, software packages, and academic contributions from our research group in computational arithmetic geometry.</p>
      </div>


    </div>
  </div>

  <!-- Filter Controls -->
  <div class="filter-section">
    <div class="container">
      <div class="filter-controls">
        <div class="filter-group">
          <label for="type-filter">Publication Type</label>
          <select id="type-filter" class="filter-select">
            <option value="">All Types</option>
            <option value="Journal Article">Journal Articles</option>
            <option value="Conference Paper">Conference Papers</option>
            <option value="Preprint">Preprints</option>
            <option value="Software Package">Software Packages</option>
            <option value="Book Chapter">Book Chapters</option>
            <option value="Technical Report">Technical Reports</option>
            <option value="Thesis">Theses</option>
          </select>
      </div>
        
        <div class="filter-group">
          <label for="status-filter">Status</label>
          <select id="status-filter" class="filter-select">
            <option value="">All Status</option>
            <option value="Published">Published</option>
            <option value="Submitted">Submitted</option>
            <option value="Under Review">Under Review</option>
            <option value="In Preparation">In Preparation</option>
            <option value="Accepted">Accepted</option>
          </select>
    </div>
    
        <div class="filter-group">
          <label for="year-filter">Year</label>
          <select id="year-filter" class="filter-select">
            <option value="">All Years</option>
            <option value="2025">2025</option>
            <option value="2024">2024</option>
            <option value="2023">2023</option>
            <option value="2022">2022</option>
            <option value="2021">2021</option>
            <option value="2020">2020</option>
            <option value="2019">2019</option>
            <option value="2018">2018</option>
            <option value="2017">2017</option>
            <option value="2016">2016</option>
            <option value="2015">2015</option>
          </select>
        </div>
        
        <div class="filter-group">
          <label for="search-input">Search</label>
          <div class="search-wrapper">
            <input type="text" id="search-input" class="filter-input" placeholder="Search titles, authors, keywords...">
            <i class="fas fa-search search-icon"></i>
          </div>
        </div>
      </div>

      <!-- Quick Filter Buttons -->
      <div class="quick-filters">
        <button class="quick-filter-btn active" data-filter="all">All</button>
        <button class="quick-filter-btn" data-filter="recent">Recent</button>
        <button class="quick-filter-btn" data-filter="featured">Featured</button>
        <button class="quick-filter-btn" data-filter="software">Software</button>
        <button class="quick-filter-btn" data-filter="papers">Papers</button>
          </div>
        </div>
      </div>

  <!-- Publications Grid -->
  <div class="publications-content">
    <div class="container">
      <!-- Loading State -->
      <div id="loading-state" class="loading-state">
        <div class="spinner"></div>
        <p>Loading publications...</p>
        </div>

      <!-- Empty State -->
      <div id="empty-state" class="empty-state" style="display: none;">
        <i class="fas fa-search"></i>
        <h3>No publications found</h3>
        <p>Try adjusting your filters or search terms.</p>
          </div>

      <!-- Publications Grid -->
      <div id="publications-grid" class="publications-grid" style="display: none;">
        <!-- Publications will be dynamically loaded here -->
        </div>

      <!-- Load More Button -->
      <div id="load-more-container" class="load-more-container" style="display: none;">
        <button id="load-more-btn" class="btn btn-outline-primary">
          <i class="fas fa-plus"></i> Load More Publications
        </button>
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
        <a href="#" class="publication-link"></a>
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
}

.publications-header {
  background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-primary) 100%);
  border-bottom: 3px solid var(--primary);
  padding: 3rem 0;
  margin-bottom: 2rem;
}

.publications-intro {
  text-align: center;
  max-width: 800px;
  margin: 0 auto 3rem;
}

.publications-intro h1 {
  font-size: 3rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 1rem;
  background: linear-gradient(135deg, var(--primary) 0%, var(--heidelberg-red) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.publications-intro .lead {
  font-size: 1.25rem;
  color: var(--text-secondary);
  line-height: 1.6;
}



.filter-section {
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-color);
  padding: 2rem 0;
  margin-bottom: 2rem;
}

.filter-controls {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-group label {
  font-weight: 600;
  color: var(--text-primary);
  font-size: 0.9rem;
}

.filter-select,
.filter-input {
  padding: 0.75rem 1rem;
  border: 2px solid var(--border-color);
  border-radius: var(--radius-md);
  background: var(--bg-primary);
  color: var(--text-primary);
  font-size: 0.95rem;
  transition: all var(--transition-base);
}

.filter-select:focus,
.filter-input:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(194, 32, 50, 0.1);
}

.search-wrapper {
  position: relative;
}

.search-icon {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-muted);
  pointer-events: none;
}

.quick-filters {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  justify-content: center;
}

.quick-filter-btn {
  padding: 0.5rem 1.5rem;
  border: 2px solid var(--border-color);
  border-radius: 2rem;
  background: var(--bg-primary);
  color: var(--text-secondary);
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-base);
}

.quick-filter-btn:hover,
.quick-filter-btn.active {
  background: var(--primary);
  color: white;
  border-color: var(--primary);
  transform: translateY(-2px);
}

.publications-content {
  padding: 0 0 3rem 0;
}

.loading-state,
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: var(--text-muted);
}

.spinner {
  width: 3rem;
  height: 3rem;
  border: 3px solid var(--border-color);
  border-top: 3px solid var(--primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-state i {
  font-size: 4rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.empty-state h3 {
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}

.publications-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.publication-card {
  background: var(--bg-secondary);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-base);
  overflow: hidden;
}

.publication-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-md);
  border-color: var(--primary);
}

.publication-header {
  padding: 1.5rem;
  border-bottom: 1px solid var(--border-color);
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
  background: linear-gradient(135deg, var(--primary) 0%, var(--heidelberg-red) 100%);
  color: white;
}

.publication-status {
  background: var(--bg-muted);
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
}

.publication-year {
  background: var(--bg-muted);
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
}

.publication-title {
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
  line-height: 1.3;
}

.publication-title a {
  color: var(--text-primary);
  text-decoration: none;
  transition: color var(--transition-base);
}

.publication-title a:hover {
  color: var(--primary);
}

.publication-authors {
  color: var(--text-secondary);
  font-style: italic;
  margin-bottom: 0.5rem;
  font-size: 0.95rem;
}

.publication-venue {
  color: var(--text-muted);
  font-size: 0.9rem;
}

.publication-body {
  padding: 1.5rem;
}

.publication-abstract {
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 1rem;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.publication-keywords {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.keyword-tag {
  background: var(--bg-muted);
  color: var(--text-secondary);
  padding: 0.25rem 0.5rem;
  border-radius: 0.5rem;
  font-size: 0.8rem;
  border: 1px solid var(--border-color);
}

.publication-footer {
  padding: 1.5rem;
  border-top: 1px solid var(--border-color);
  background: var(--bg-primary);
}

.publication-links {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.publication-link-btn {
  padding: 0.4rem 0.8rem;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  background: var(--bg-secondary);
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 0.8rem;
  transition: all var(--transition-base);
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.publication-link-btn:hover {
  background: var(--primary);
  color: white;
  border-color: var(--primary);
  text-decoration: none;
}

.publication-metrics {
  display: flex;
  gap: 1rem;
  font-size: 0.85rem;
  color: var(--text-muted);
}

.metric-item {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.load-more-container {
  text-align: center;
  margin-top: 2rem;
}

.load-more-btn {
  padding: 1rem 2rem;
  font-size: 1rem;
  font-weight: 500;
}

/* Responsive Design */
@media (max-width: 991.98px) {
  .publications-intro h1 {
    font-size: 2.5rem;
  }
  

  
  .filter-controls {
    grid-template-columns: 1fr;
  }
  
  .publications-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .publications-header {
    padding: 2rem 0;
  }
  
  .publications-intro h1 {
    font-size: 2rem;
  }
  
  .publications-intro .lead {
    font-size: 1.1rem;
  }
  

  
  .quick-filters {
    gap: 0.5rem;
  }
  
  .quick-filter-btn {
    padding: 0.4rem 1rem;
    font-size: 0.9rem;
  }
}

@media (max-width: 576px) {
  .publication-card {
    margin: 0 1rem;
  }
  
  .publication-header,
  .publication-body,
  .publication-footer {
    padding: 1rem;
  }
  
  .publication-title {
    font-size: 1.1rem;
  }
}
</style>

<script>
// Publications Management System
class PublicationsManager {
  constructor() {
    this.publications = [];
    this.filteredPublications = [];
    this.currentPage = 1;
    this.itemsPerPage = 12;
    this.filters = {
      type: '',
      status: '',
      year: '',
      search: ''
    };
    
    this.init();
  }
  
  async init() {
    this.bindEvents();
    await this.loadPublications();
    this.renderPublications();
  }
  
  bindEvents() {
    // Filter controls
    document.getElementById('type-filter').addEventListener('change', (e) => {
      this.filters.type = e.target.value;
      this.applyFilters();
    });
    
    document.getElementById('status-filter').addEventListener('change', (e) => {
      this.filters.status = e.target.value;
      this.applyFilters();
    });
    
    document.getElementById('year-filter').addEventListener('change', (e) => {
      this.filters.year = e.target.value;
      this.applyFilters();
    });
    
    // Search input with debouncing
    let searchTimeout;
    document.getElementById('search-input').addEventListener('input', (e) => {
      clearTimeout(searchTimeout);
      searchTimeout = setTimeout(() => {
        this.filters.search = e.target.value.toLowerCase();
        this.applyFilters();
      }, 300);
    });
    
    // Quick filter buttons
    document.querySelectorAll('.quick-filter-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        document.querySelectorAll('.quick-filter-btn').forEach(b => b.classList.remove('active'));
        e.target.classList.add('active');
        
        const filter = e.target.dataset.filter;
        this.applyQuickFilter(filter);
      });
    });
    
    // Load more button
    document.getElementById('load-more-btn').addEventListener('click', () => {
      this.loadMore();
    });
  }
  
  async loadPublications() {
    try {
      // Show loading state
      document.getElementById('loading-state').style.display = 'block';
      document.getElementById('publications-grid').style.display = 'none';
      document.getElementById('empty-state').style.display = 'none';
      
      // In a real implementation, this would fetch from the CMS API
      // For now, we'll use sample data
      this.publications = await this.getSamplePublications();
      
      // Hide loading state
      document.getElementById('loading-state').style.display = 'none';
      
    } catch (error) {
      console.error('Error loading publications:', error);
      document.getElementById('loading-state').style.display = 'none';
      document.getElementById('empty-state').style.display = 'block';
    }
  }
  
  async getSamplePublications() {
    // Sample publications data - in real implementation, this would come from CMS
    return [
      // Prof. Dr. Gebhard Böckle Publications
      {
        id: 1,
        title: "Irreducibility of versal deformation rings in the (p,p)-case for 2-dimensional representations",
        authors: "Gebhard Böckle, A.-K. Juschka",
        year: 2015,
        journal: "J. Algebra",
        volume: "444",
        pages: "81–123",
        doi: "10.1016/j.jalgebra.2015.07.001",
        abstract: "This paper studies the irreducibility of versal deformation rings in the (p,p)-case for 2-dimensional representations, providing important insights into deformation theory.",
        keywords: "deformation theory, Galois representations, irreducibility",
        type: "Journal Article",
        status: "Published",
        featured: true,
        url: "http://www.sciencedirect.com/science/article/pii/S002186931500352X",
        pdf: "/assets/uploads/BoeckleJuschka-Irreducibility.pdf"
      },
      {
        id: 2,
        title: "Independence of l-adic representations of geometric Galois groups",
        authors: "Gebhard Böckle, W. Gajda, S. Petersen",
        year: 2015,
        journal: "J. Reine Angew. Math.",
        doi: "10.1515/crelle-2015-0024",
        abstract: "This work establishes independence results for l-adic representations of geometric Galois groups, extending our understanding of Galois representations.",
        keywords: "l-adic representations, Galois groups, independence",
        type: "Journal Article",
        status: "Published",
        featured: true,
        url: "http://dx.doi.org/10.1515/crelle-2015-0024",
        pdf: "/assets/uploads/Boeckle-Gajda-Petersen-crelle-2015-0024.pdf"
      },
      {
        id: 3,
        title: "Hecke characters associated to Drinfeld modular forms",
        authors: "Gebhard Böckle, T. Centeleghe",
        year: 2015,
        journal: "Compos. Math.",
        abstract: "This paper explores the relationship between Hecke characters and Drinfeld modular forms, providing new insights into function field arithmetic.",
        keywords: "Hecke characters, Drinfeld modular forms, function fields",
        type: "Journal Article",
        status: "Published",
        featured: true,
        url: "http://dx.doi.org/10.1112/S0010437X15007290",
        pdf: "/assets/uploads/Boeckle-Centeleghe-HeckeCharactersAssociatedToDrinfeldModularForms.pdf"
      },
      {
        id: 4,
        title: "The distribution of the zeros of the Goss zeta-function for A=F₂[x,y]/(y²+y+x³+x+1)",
        authors: "Gebhard Böckle",
        year: 2013,
        journal: "Math. Z.",
        volume: "275",
        pages: "835–861",
        doi: "10.1007/s00209-013-1162-9",
        abstract: "This work studies the distribution of zeros of the Goss zeta-function for a specific function field, contributing to our understanding of L-functions over function fields.",
        keywords: "Goss zeta-function, function fields, zero distribution",
        type: "Journal Article",
        status: "Published",
        url: "http://dx.doi.org/10.1007/s00209-013-1162-9",
        pdf: "/assets/uploads/ZeroDistribForOneA.pdf"
      },
      {
        id: 5,
        title: "Algebraic Hecke characters and compatible systems of abelian mod p Galois representations over global fields",
        authors: "Gebhard Böckle",
        year: 2013,
        journal: "Manuscripta Math.",
        volume: "140",
        pages: "303-331",
        doi: "10.1007/s00222-012-0418-z",
        abstract: "This paper establishes connections between algebraic Hecke characters and compatible systems of abelian mod p Galois representations.",
        keywords: "Hecke characters, Galois representations, global fields",
        type: "Journal Article",
        status: "Published",
        url: "http://www.springerlink.com/content/ll5v246782212835/",
        pdf: "/assets/uploads/Boeckle-AlgHeckeCharsAndStrictlyCompSys.pdf"
      },
      {
        id: 6,
        title: "On computing quaternion quotient graphs for function fields",
        authors: "Gebhard Böckle, Ralf Butenuth",
        year: 2012,
        journal: "J. Théor. Nombres Bordeaux",
        volume: "24",
        pages: "73-99",
        doi: "10.5802/jtnb.789",
        abstract: "This work presents computational methods for computing quaternion quotient graphs over function fields.",
        keywords: "quaternion algebras, function fields, computational methods",
        type: "Journal Article",
        status: "Published",
        url: "http://jtnb.cedram.org/jtnb-bin/item?id=JTNB_2012__24_1_73_0",
        pdf: "/assets/uploads/Proofs-Boeckle-Butenuth.pdf"
      },
      {
        id: 7,
        title: "Cartier Modules: finiteness results",
        authors: "M. Blickle, Gebhard Böckle",
        year: 2011,
        journal: "J. Reine Angew. Math.",
        volume: "661",
        pages: "85-123",
        doi: "10.1515/CRELLE.2011.085",
        abstract: "This paper establishes finiteness results for Cartier modules, contributing to the theory of D-modules in positive characteristic.",
        keywords: "Cartier modules, D-modules, finiteness results",
        type: "Journal Article",
        status: "Published",
        url: "http://www.ams.org/mathscinet-getitem?mr=2863904",
        pdf: "/assets/uploads/BlickleBoeckle-CartierModulesFinitenessResults.pdf"
      },
      {
        id: 8,
        title: "Computations with Modular Forms",
        authors: "Gebhard Böckle, G. Wiese",
        year: 2014,
        journal: "Springer",
        abstract: "A comprehensive textbook on computational aspects of modular forms, covering both theoretical foundations and practical implementation.",
        keywords: "modular forms, computational methods, textbook",
        type: "Book",
        status: "Published",
        featured: true,
        url: "http://link.springer.com/book/10.1007/978-3-319-03847-6"
      },
      {
        id: 9,
        title: "Cohomological Theory of Crystals over Function Fields",
        authors: "Gebhard Böckle, R. Pink",
        year: 2009,
        journal: "European Mathematical Society",
        abstract: "A comprehensive treatment of the cohomological theory of crystals over function fields, including applications to arithmetic geometry.",
        keywords: "crystals, function fields, cohomology, arithmetic geometry",
        type: "Book",
        status: "Published",
        featured: true,
        url: "http://www.ams.org/mathscinet-getitem?mr=2561048"
      },
      // Dr. Barinder Banwait Publications
      {
        id: 10,
        title: "Explicit Chabauty-Kim for the thrice-punctured line in depth two",
        authors: "Barinder S. Banwait, Ishai Dan-Cohen",
        year: 2019,
        journal: "Preprint",
        doi: "10.48550/arXiv.1905.08902",
        arxiv: "1905.08902",
        abstract: "This paper presents explicit computations for the Chabauty-Kim method applied to the thrice-punctured line. The work extends previous results in computational arithmetic geometry and provides new insights into the structure of fundamental groups in relative pro-unipotent completions.",
        keywords: "Chabauty-Kim method, arithmetic geometry, fundamental groups",
        type: "Preprint",
        status: "Published",
        featured: true,
        url: "https://arxiv.org/abs/1905.08902"
      },
      // Dr. Peter Gräf Publications
      {
        id: 11,
        title: "A Hecke-equivariant decomposition of spaces of Drinfeld cusp forms via representation theory, and an investigation of its subfactors",
        authors: "Peter Gräf, G. Böckle, R. Perkins",
        year: 2021,
        journal: "Research in Number Theory",
        volume: "7",
        pages: "Article number: 44",
        doi: "10.1007/s40993-021-00254-0",
        abstract: "This paper develops Hecke-equivariant decomposition methods for spaces of Drinfeld cusp forms using representation theory, providing new insights into the structure of these spaces.",
        keywords: "Drinfeld modular forms, representation theory, Hecke operators, cusp forms",
        type: "Journal Article",
        status: "Published",
        featured: true,
        url: "https://link.springer.com/article/10.1007%2Fs40993-021-00254-0"
      },
      {
        id: 12,
        title: "Computing L-invariants via the Greenberg-Stevens formula",
        authors: "S. Anni, G. Böckle, Peter Gräf, A. Troya",
        year: 2019,
        journal: "Journal de Théorie des Nombres de Bordeaux",
        volume: "31",
        pages: "727–746",
        doi: "10.5802/jtnb.789",
        abstract: "This work advances computational methods for computing L-invariants via the Greenberg-Stevens formula, contributing to our understanding of p-adic L-functions.",
        keywords: "L-invariants, Greenberg-Stevens formula, p-adic L-functions, computational methods",
        type: "Journal Article",
        status: "Published",
        url: "https://jtnb.centre-mersenne.org/article/JTNB_2019__31_3_727_0.pdf"
      },
      {
        id: 13,
        title: "A control theorem for p-adic automorphic forms and Teitelbaum's L-invariant",
        authors: "Peter Gräf",
        year: 2019,
        journal: "The Ramanujan Journal",
        volume: "50",
        pages: "13-43",
        doi: "10.1007/s11139-019-00160-1",
        abstract: "This paper establishes control theorems for p-adic automorphic forms and Teitelbaum's L-invariant, advancing our understanding of p-adic automorphic representations.",
        keywords: "p-adic automorphic forms, L-invariants, control theorems, Teitelbaum",
        type: "Journal Article",
        status: "Published",
        url: "http://dx.doi.org/10.1007/s11139-019-00160-1"
      },
      {
        id: 14,
        title: "Boundary Distributions for GL3 over a Local Field and Symmetric Power Coefficients",
        authors: "Peter Gräf",
        year: 2020,
        journal: "Ph.D. Thesis",
        abstract: "This thesis studies boundary distributions for GL3 over local fields and their relationship to symmetric power coefficients, providing new insights into the structure of automorphic representations.",
        keywords: "boundary distributions, GL3, local fields, symmetric power coefficients, automorphic representations",
        type: "Thesis",
        status: "Published",
        pdf: "/assets/uploads/boundary_peter_graef.pdf"
      },
      // Software Packages
      {
        id: 15,
        title: "QaQuotGraphs Magma Package",
        authors: "Dr. Ralf Butenuth",
        year: 2020,
        journal: "Software Package",
        abstract: "A comprehensive Magma package for computing the action by unit groups of maximal orders in quaternion algebras over F_q(T). This package provides efficient algorithms for working with quaternion algebras and their unit groups in the function field setting.",
        keywords: "Magma, quaternion algebras, computational algebra, function fields",
        type: "Software Package",
        status: "Published",
        featured: true,
        software_info: {
          repository_url: "https://github.com/example/qaquotgraphs",
          download_url: "/assets/uploads/qaquotgraph_package.tar.gz",
          version: "1.0.0",
          license: "GPL-3.0",
          documentation: "https://github.com/example/qaquotgraphs/wiki"
        }
      },
      {
        id: 16,
        title: "Bruhat-Tits Buildings Package",
        authors: "Lutz Hofmann",
        year: 2021,
        journal: "Software Package",
        abstract: "Magma package to compute quotients of Bruhat-Tits buildings over function fields modulo congruence subgroups and the action of Hecke operators on harmonic cocycles with coefficients in char. 0.",
        keywords: "Bruhat-Tits buildings, Hecke operators, harmonic cocycles, function fields",
        type: "Software Package",
        status: "Published",
        software_info: {
          repository_url: "https://github.com/lhofmann/buildings",
          version: "2.1.0",
          license: "MIT",
          documentation: "https://github.com/lhofmann/buildings/blob/main/README.md"
        }
      },
      {
        id: 17,
        title: "Hecke Operator Package",
        authors: "Burak Cakir",
        year: 2022,
        journal: "Software Package",
        abstract: "Magma package to compute Hecke eigensystems for harmonic cocycles on the Bruhat-Tits tree for GL_2(F_q(T)). This package implements efficient algorithms for computing with Hecke operators in the function field setting.",
        keywords: "Hecke operators, harmonic cocycles, GL_2, Bruhat-Tits tree",
        type: "Software Package",
        status: "Published",
        software_info: {
          repository_url: "https://github.com/b-cakir/hecke-operator",
          version: "1.5.0",
          license: "GPL-2.0",
          documentation: "https://github.com/b-cakir/hecke-operator/blob/main/README.md"
        }
      },
      // Preprints and In Preparation
      {
        id: 18,
        title: "Equidimensionality of universal pseudodeformation rings in characteristic p for absolute Galois groups of p-adic fields",
        authors: "Gebhard Böckle, A.-K. Juschka",
        year: 2023,
        journal: "Preprint",
        abstract: "This preprint establishes equidimensionality results for universal pseudodeformation rings in characteristic p for absolute Galois groups of p-adic fields.",
        keywords: "pseudodeformation rings, Galois groups, p-adic fields",
        type: "Preprint",
        status: "In Preparation",
        pdf: "/assets/uploads/Boeckle-Juschka-Pseudo-20230701.pdf"
      },
      {
        id: 19,
        title: "An Eichler-Shimura isomorphism over function fields between Drinfeld modular forms and cohomology classes of crystals",
        authors: "Gebhard Böckle",
        year: 2023,
        journal: "Preprint",
        abstract: "This work establishes an Eichler-Shimura isomorphism over function fields, connecting Drinfeld modular forms to cohomology classes of crystals.",
        keywords: "Eichler-Shimura isomorphism, Drinfeld modular forms, crystals, function fields",
        type: "Preprint",
        status: "In Preparation",
        pdf: "/assets/uploads/EiShNew.pdf"
      }
    ];
  }
  
  applyFilters() {
    this.filteredPublications = this.publications.filter(pub => {
      // Type filter
      if (this.filters.type && pub.type !== this.filters.type) return false;
      
      // Status filter
      if (this.filters.status && pub.status !== this.filters.status) return false;
      
      // Year filter
      if (this.filters.year && pub.year.toString() !== this.filters.year) return false;
      
      // Search filter
      if (this.filters.search) {
        const searchTerm = this.filters.search;
        const searchableText = `${pub.title} ${pub.authors} ${pub.abstract} ${pub.keywords}`.toLowerCase();
        if (!searchableText.includes(searchTerm)) return false;
      }
      
      return true;
    });
    
    this.currentPage = 1;
    this.renderPublications();
  }
  
  applyQuickFilter(filter) {
    // Reset all filters
    this.filters = { type: '', status: '', year: '', search: '' };
    
    // Apply quick filter
    switch (filter) {
      case 'recent':
        this.filters.year = '2020';
        break;
      case 'featured':
        this.filteredPublications = this.publications.filter(pub => pub.featured);
        this.renderPublications();
        return;
      case 'software':
        this.filters.type = 'Software Package';
        break;
      case 'papers':
        this.filters.type = 'Journal Article';
        break;
      default:
        this.filteredPublications = this.publications;
        this.renderPublications();
        return;
    }
    
    this.applyFilters();
  }
  
  renderPublications() {
    const grid = document.getElementById('publications-grid');
    const emptyState = document.getElementById('empty-state');
    const loadMoreContainer = document.getElementById('load-more-container');
    
    if (this.filteredPublications.length === 0) {
      grid.style.display = 'none';
      emptyState.style.display = 'block';
      loadMoreContainer.style.display = 'none';
      return;
    }
    
    grid.style.display = 'grid';
    emptyState.style.display = 'none';
    
    // Calculate pagination
    const startIndex = 0;
    const endIndex = this.currentPage * this.itemsPerPage;
    const publicationsToShow = this.filteredPublications.slice(startIndex, endIndex);
    
    // Clear existing content
    grid.innerHTML = '';
    
    // Render publications
    publicationsToShow.forEach(pub => {
      const card = this.createPublicationCard(pub);
      grid.appendChild(card);
    });
    
    // Show/hide load more button
    if (endIndex < this.filteredPublications.length) {
      loadMoreContainer.style.display = 'block';
    } else {
      loadMoreContainer.style.display = 'none';
    }
  }
  
  createPublicationCard(pub) {
    const template = document.getElementById('publication-card-template');
    const card = template.content.cloneNode(true);
    
    // Set basic information
    card.querySelector('.publication-type').textContent = pub.type;
    card.querySelector('.publication-status').textContent = pub.status;
    card.querySelector('.publication-year').textContent = pub.year;
    card.querySelector('.publication-title a').textContent = pub.title;
    card.querySelector('.publication-title a').href = `/publications/${pub.id}/`;
    card.querySelector('.publication-authors').textContent = pub.authors;
    card.querySelector('.publication-venue').textContent = pub.journal;
    card.querySelector('.publication-abstract').textContent = pub.abstract;
    
    // Add keywords
    if (pub.keywords) {
      const keywordsContainer = card.querySelector('.publication-keywords');
      const keywords = pub.keywords.split(',').map(k => k.trim());
      keywords.forEach(keyword => {
        const tag = document.createElement('span');
        tag.className = 'keyword-tag';
        tag.textContent = keyword;
        keywordsContainer.appendChild(tag);
      });
    }
    
    // Add links
    const linksContainer = card.querySelector('.publication-links');
    if (pub.doi) {
      const doiLink = document.createElement('a');
      doiLink.href = `https://doi.org/${pub.doi}`;
      doiLink.className = 'publication-link-btn';
      doiLink.innerHTML = '<i class="fas fa-external-link-alt"></i> DOI';
      doiLink.target = '_blank';
      linksContainer.appendChild(doiLink);
    }
    
    if (pub.arxiv) {
      const arxivLink = document.createElement('a');
      arxivLink.href = `https://arxiv.org/abs/${pub.arxiv}`;
      arxivLink.className = 'publication-link-btn';
      arxivLink.innerHTML = '<i class="fas fa-file-alt"></i> arXiv';
      arxivLink.target = '_blank';
      linksContainer.appendChild(arxivLink);
    }
    
    if (pub.url) {
      const urlLink = document.createElement('a');
      urlLink.href = pub.url;
      urlLink.className = 'publication-link-btn';
      urlLink.innerHTML = '<i class="fas fa-external-link-alt"></i> View';
      urlLink.target = '_blank';
      linksContainer.appendChild(urlLink);
    }
    
    if (pub.software_info && pub.software_info.repository_url) {
      const repoLink = document.createElement('a');
      repoLink.href = pub.software_info.repository_url;
      repoLink.className = 'publication-link-btn';
      repoLink.innerHTML = '<i class="fab fa-github"></i> Repository';
      repoLink.target = '_blank';
      linksContainer.appendChild(repoLink);
    }
    
    // Add metrics
    const metricsContainer = card.querySelector('.publication-metrics');
    if (pub.impact_factor) {
      const impactMetric = document.createElement('div');
      impactMetric.className = 'metric-item';
      impactMetric.innerHTML = `<i class="fas fa-star"></i> IF: ${pub.impact_factor}`;
      metricsContainer.appendChild(impactMetric);
    }
    
    if (pub.citations) {
      const citationMetric = document.createElement('div');
      citationMetric.className = 'metric-item';
      citationMetric.innerHTML = `<i class="fas fa-quote-left"></i> ${pub.citations} citations`;
      metricsContainer.appendChild(citationMetric);
    }
    
    return card;
  }
  
  loadMore() {
    this.currentPage++;
    this.renderPublications();
  }
  

}

// Initialize the publications manager when the page loads
document.addEventListener('DOMContentLoaded', () => {
  new PublicationsManager();
});
</script>

 