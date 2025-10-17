---
layout: page
permalink: "/links/"
nav: true
nav_order: 4
show_title: false
order: 100
title: Links
---

<style>
/* Links Cards Layout */
.main-container {
  width: 100%;
  margin: 0;
  padding: 0 0.75rem;
}

.content-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.link-category-card {
  background: var(--bg-primary);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-base);
  overflow: hidden;
  position: relative;
}

.link-category-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-4px);
  border-color: var(--primary);
}

.card-header {
  background: linear-gradient(135deg, var(--primary) 0%, var(--heidelberg-red) 100%);
  padding: 1rem;
  color: white;
  position: relative;
}

.card-header h3 {
  margin: 0;
  font-size: 1.3rem;
  font-weight: 600;
  line-height: 1.2;
}

.card-body {
  padding: 1.25rem;
}

.link-item {
  display: block;
  padding: 0.75rem;
  margin-bottom: 0.5rem;
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
  text-decoration: none;
  transition: all var(--transition-base);
  border: 1px solid var(--border-color);
}

.link-item:hover {
  background: var(--primary-light);
  transform: translateY(-2px);
  box-shadow: var(--shadow-sm);
  border-color: var(--primary);
}

.link-title {
  font-weight: 600;
  color: var(--text-primary);
  font-size: 1rem;
  margin-bottom: 0.25rem;
  display: block;
}

.link-url {
  color: var(--text-muted);
  font-size: 0.85rem;
  display: block;
  word-break: break-all;
}

.link-item:hover .link-title {
  color: var(--primary);
}

.link-item:hover .link-url {
  color: var(--text-secondary);
}

/* Responsive Design */
@media (max-width: 768px) {
  .content-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .main-container {
    padding: 0 0.5rem;
  }

  .card-header {
    padding: 0.75rem;
  }

  .card-body {
    padding: 1rem;
  }

  .link-item {
    padding: 0.6rem;
  }
}

@media (max-width: 480px) {
  .main-container {
    padding: 0 0.25rem;
  }

  .card-header h3 {
    font-size: 1.1rem;
  }

  .card-body {
    padding: 0.75rem;
  }
}
</style>

<div class="main-container">
  <div class="content-grid">
    <!-- Heidelberg University Links -->
    <div class="link-category-card">
      <div class="card-header">
        <h3><i class="fas fa-university" aria-hidden="true"></i> Heidelberg University</h3>
      </div>
      <div class="card-body">
        <a href="https://www.iwr.uni-heidelberg.de/" target="_blank" rel="noopener" class="link-item">
          <span class="link-title">Interdisciplinary Center for Scientific Computing (IWR)</span>
          <span class="link-url">https://www.iwr.uni-heidelberg.de/</span>
        </a>

        <a href="https://www.math.uni-heidelberg.de/en" target="_blank" rel="noopener" class="link-item">
          <span class="link-title">Institute of Mathematics Heidelberg</span>
          <span class="link-url">https://www.math.uni-heidelberg.de/en</span>
        </a>

        <a href="https://www.mathinf.uni-heidelberg.de/" target="_blank" rel="noopener" class="link-item">
          <span class="link-title">Faculty of Mathematics and Computer Sciences</span>
          <span class="link-url">https://www.mathinf.uni-heidelberg.de/</span>
        </a>

        <a href="https://www.uni-heidelberg.de/excellenceinitiative/institutionalstrategy/match.html" target="_blank" rel="noopener" class="link-item">
          <span class="link-title">The MAThematics Center Heidelberg (MATCH)</span>
          <span class="link-url">https://www.uni-heidelberg.de/excellenceinitiative/institutionalstrategy/match.html</span>
        </a>
      </div>
    </div>

    <!-- DFG Research Projects -->
    <div class="link-category-card">
      <div class="card-header">
        <h3><i class="fas fa-flask" aria-hidden="true"></i> DFG Research Projects</h3>
      </div>
      <div class="card-body">
        <a href="https://crc326gaus.de/" target="_blank" rel="noopener" class="link-item">
          <span class="link-title">DFG CRC 326 GAUS "Geometry and Arithmetic of Uniformized Structures"</span>
          <span class="link-url">https://crc326gaus.de/</span>
        </a>

        <a href="http://www.computeralgebra.de/" target="_blank" rel="noopener" class="link-item">
          <span class="link-title">DFG Priority Project SSP 1489 "Algorithmic and Experimental Methods in Algebra, Geometry, and Number Theory"</span>
          <span class="link-url">http://www.computeralgebra.de/</span>
        </a>
      </div>
    </div>

    <!-- Academic Resources -->
    <div class="link-category-card">
      <div class="card-header">
        <h3><i class="fas fa-book" aria-hidden="true"></i> Academic Resources</h3>
      </div>
      <div class="card-body">
        <a href="https://math.osu.edu/research/journals" target="_blank" rel="noopener" class="link-item">
          <span class="link-title">Journal of Number Theory</span>
          <span class="link-url">https://math.osu.edu/research/journals</span>
        </a>
      </div>
    </div>
  </div>
</div>
