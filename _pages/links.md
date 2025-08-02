---
layout: page
title: Links
permalink: /links/
nav: true
nav_order: 4
---

<p class="translatable-content" data-translation-key="links.intro">Here are some links that may be of interest to students and researchers, managed from the CMS.</p>

<!-- Heidelberg University Links -->
<h2>Heidelberg University</h2>
<div class="list-group mb-4">
  <a href="https://www.iwr.uni-heidelberg.de/" target="_blank" rel="noopener" class="list-group-item list-group-item-action">
    <div class="d-flex w-100 justify-content-between">
      <h5 class="mb-1">Interdisciplinary Center for Scientific Computing (IWR)</h5>
    </div>
    <small class="text-muted">https://www.iwr.uni-heidelberg.de/</small>
  </a>
  
  <a href="https://www.mathi.uni-heidelberg.de/" target="_blank" rel="noopener" class="list-group-item list-group-item-action">
    <div class="d-flex w-100 justify-content-between">
      <h5 class="mb-1">Mathematisches Institut</h5>
    </div>
    <small class="text-muted">https://www.mathi.uni-heidelberg.de/</small>
  </a>
  
  <a href="https://www.mathinf.uni-heidelberg.de/" target="_blank" rel="noopener" class="list-group-item list-group-item-action">
    <div class="d-flex w-100 justify-content-between">
      <h5 class="mb-1">Faculty of Mathematics and Computer Sciences</h5>
    </div>
    <small class="text-muted">https://www.mathinf.uni-heidelberg.de/</small>
  </a>
  
  <a href="http://www.match.uni-heidelberg.de/" target="_blank" rel="noopener" class="list-group-item list-group-item-action">
    <div class="d-flex w-100 justify-content-between">
      <h5 class="mb-1">The MAThematics Center Heidelberg (MATCH)</h5>
    </div>
    <small class="text-muted">http://www.match.uni-heidelberg.de/</small>
  </a>
</div>

<!-- DFG Research Projects -->
<h2>DFG Research Projects</h2>
<div class="list-group mb-4">
  <a href="https://crc326gaus.de/" target="_blank" rel="noopener" class="list-group-item list-group-item-action">
    <div class="d-flex w-100 justify-content-between">
      <h5 class="mb-1">DFG CRC 326 GAUS "Geometry and Arithmetic of Uniformized Structures"</h5>
    </div>
    <small class="text-muted">https://crc326gaus.de/</small>
  </a>
  
  <a href="https://www.mathi.uni-heidelberg.de/fg-sga/index-en.html" target="_blank" rel="noopener" class="list-group-item list-group-item-action">
    <div class="d-flex w-100 justify-content-between">
      <h5 class="mb-1">DFG Research Group 1920 "Symmetry, Geometry and Arithmetic" Heidelberg/Darmstadt</h5>
    </div>
    <small class="text-muted">https://www.mathi.uni-heidelberg.de/fg-sga/index-en.html</small>
  </a>
  
  <a href="http://www.computeralgebra.de/" target="_blank" rel="noopener" class="list-group-item list-group-item-action">
    <div class="d-flex w-100 justify-content-between">
      <h5 class="mb-1">DFG Priority Project SSP 1489 "Algorithmic and Experimental Methods in Algebra, Geometry, and Number Theory"</h5>
    </div>
    <small class="text-muted">http://www.computeralgebra.de/</small>
  </a>
</div>

<!-- Academic Resources -->
<h2>Academic Resources</h2>
<div class="list-group mb-4">
  <a href="https://www.mathinf.uni-heidelberg.de/pruefausschuss.html" target="_blank" rel="noopener" class="list-group-item list-group-item-action">
    <div class="d-flex w-100 justify-content-between">
      <h5 class="mb-1">Prüfungsausschuss und Prüfungssekretariat</h5>
    </div>
    <small class="text-muted">https://www.mathinf.uni-heidelberg.de/pruefausschuss.html</small>
  </a>
  
  <a href="http://www.journals.elsevier.com/journal-of-number-theory/" target="_blank" rel="noopener" class="list-group-item list-group-item-action">
    <div class="d-flex w-100 justify-content-between">
      <h5 class="mb-1">Journal of Number Theory</h5>
    </div>
    <small class="text-muted">http://www.journals.elsevier.com/journal-of-number-theory/</small>
  </a>
  
  <a href="https://www.iwr.uni-heidelberg.de/groupswikiarithgeo/" target="_blank" rel="noopener" class="list-group-item list-group-item-action">
    <div class="d-flex w-100 justify-content-between">
      <h5 class="mb-1">Internal Matters</h5>
    </div>
    <small class="text-muted">https://www.iwr.uni-heidelberg.de/groupswikiarithgeo/</small>
  </a>
</div>

<div class="links-list mt-5">
  {% if site.links %}
    {% assign links_by_category = site.links | group_by: "category" | sort: "name" %}
    
    {% for category_group in links_by_category %}
      <h2 class="category-heading">{{ category_group.name }}</h2>
      <div class="list-group">
        {% for link in category_group.items %}
          <a href="{{ link.url }}" target="_blank" rel="noopener" class="list-group-item list-group-item-action">
            <div class="d-flex w-100 justify-content-between">
              <h5 class="mb-1">{{ link.title }}</h5>
            </div>
            {% if link.description %}
              <p class="mb-1">{{ link.description }}</p>
            {% endif %}
            <small class="text-muted">{{ link.url }}</small>
          </a>
        {% endfor %}
      </div>
    {% endfor %}
  {% else %}
    <p class="text-muted">No links available at this time.</p>
  {% endif %}
</div>

<style>
.category-heading {
  font-size: 2rem;
  margin-top: 3rem;
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid var(--primary);
}
</style> 