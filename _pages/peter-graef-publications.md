---
layout: page
title: Publications - Dr. Peter Gräf
permalink: "/members/peter-graef/publications/"
nav: false
order: 100
---
<div class="heidelberg-style-publications">
  <!-- Breadcrumb Navigation -->
  <div class="pathway">
    <div style="float:left;">
      <a href="https://www.uni-heidelberg.de">Uni Heidelberg</a> &gt; 
      <a href="{{ '/' | relative_url }}">IWR</a> &gt; 
      <a href="{{ '/' | relative_url }}">ARITHGEO</a> &gt; 
      <a href="{{ '/publications/' | relative_url }}">Publications</a> &gt; 
      Dr. Peter Gräf
    </div>
    <div style="float:right;">
      [<a href="{{ '/members/peter-graef/publications/' | relative_url }}">english</a>]&nbsp;|&nbsp;[<a href="{{ '/members/peter-graef/publications-de/' | relative_url }}">deutsch</a>]
    </div>
  </div>
  <br>

  <!-- Main Content -->
  <div class="publications-content">
    <h2>Publications of Dr. Peter Gräf</h2>
    
    <div class="member-info">
      <img src="{{ '/assets/img/peter-graef.jpg' | relative_url }}" alt="Dr. Peter Gräf" class="member-photo">
      <div class="member-details">
        <h3>Dr. Peter Gräf</h3>
        <p><strong>Former PhD Student</strong> (2015-2020)</p>
        <p><strong>Research interests:</strong> Drinfeld modular forms, p-adic automorphic forms, L-invariants, representation theory, arithmetic geometry</p>
        <p><strong>Email:</strong> <a href="mailto:peter.graef@iwr.uni-heidelberg.de">peter.graef@iwr.uni-heidelberg.de</a></p>
        <p><strong>Website:</strong> <a href="https://sites.google.com/view/peter-graef" target="_blank">Personal Website</a></p>
      </div>
    </div>

    <h3>Publications</h3>
    <div class="member-publications">
      {% assign peter_publications = site.publications | where_exp: "pub", "pub.authors contains 'P. Gräf' or pub.authors contains 'Peter Gräf'" | sort: 'year' | reverse %}
      {% if peter_publications.size > 0 %}
        {% for publication in peter_publications %}
          <div class="publication-item">
            <div class="publication-header">
              <h4><a href="{{ publication.url }}">{{ publication.title }}</a></h4>
              <div class="publication-meta">
                <span class="publication-type">{{ publication.type }}</span>
                <span class="publication-year">{{ publication.year }}</span>
              </div>
            </div>
            <div class="publication-authors">{{ publication.authors }}</div>
            {% if publication.journal %}
              <div class="publication-venue">{{ publication.journal }}{% if publication.volume %}, {{ publication.volume }}{% endif %}{% if publication.pages %}, {{ publication.pages }}{% endif %}</div>
            {% endif %}
            {% if publication.abstract %}
              <div class="publication-abstract">{{ publication.abstract | truncate: 300 }}</div>
            {% endif %}
            <div class="publication-links">
              {% if publication.doi %}
                <a href="https://doi.org/{{ publication.doi }}" class="btn btn-sm btn-outline-primary" target="_blank">
                  <i class="fas fa-external-link-alt"></i> DOI
                </a>
              {% endif %}
              {% if publication.url %}
                <a href="{{ publication.url }}" class="btn btn-sm btn-outline-primary" target="_blank">
                  <i class="fas fa-external-link-alt"></i> View
                </a>
              {% endif %}
              {% if publication.pdf %}
                <a href="{{ publication.pdf }}" class="btn btn-sm btn-outline-secondary" target="_blank">
                  <i class="fas fa-file-pdf"></i> PDF
                </a>
              {% endif %}
              {% if publication.arxiv_id %}
                <a href="https://arxiv.org/abs/{{ publication.arxiv_id }}" class="btn btn-sm btn-outline-info" target="_blank">
                  <i class="fas fa-external-link-alt"></i> arXiv
                </a>
              {% endif %}
            </div>
          </div>
        {% endfor %}
      {% else %}
        <p>No publications found for Peter Gräf in the CMS system.</p>
      {% endif %}
    </div>

    <h3>Conference Presentations</h3>
    <ul class="presentation-list">
      <li>
        <strong>Journées du GDR TLAG 2021</strong> (Rennes, 24/03/2021 - 26/03/2021)
        <br><a href="{{ '/assets/uploads/slides_rennes.pdf' | relative_url }}" class="download">Slides</a>
      </li>
      <li>
        <strong>AMS Fall Eastern Virtual Sectional Meeting</strong> (03/10/2020 - 04/10/2020)
        <br>Special Session on Drinfeld Modules, Modular Varieties and Arithmetic Applications
        <br><a href="{{ '/assets/uploads/Slides_AMS.pdf' | relative_url }}" class="download">Slides</a>
      </li>
    </ul>

    <h3>Posters</h3>
    <ul class="poster-list">
      <li>
        <strong>Workshop Arithmetic Geometry and Computer Algebra</strong> (Oldenburg, 29/06/2017 - 01/07/2017)
        <br><a href="{{ '/assets/uploads/Poster_Peter_Graef.pdf' | relative_url }}" class="download">Poster</a> | 
        <a href="http://www.uni-oldenburg.de/jan-steffen-mueller/workshop" target="_blank">Workshop Website</a>
      </li>
    </ul>

    <h3>Research Summary</h3>
    <p>Dr. Peter Gräf's research focused on Drinfeld modular forms, p-adic automorphic forms, and L-invariants. His work made significant contributions to:</p>
    <ul>
      <li><strong>Drinfeld Modular Forms:</strong> Developed Hecke-equivariant decomposition methods for spaces of Drinfeld cusp forms using representation theory</li>
      <li><strong>L-invariants:</strong> Advanced computational methods for computing L-invariants via the Greenberg-Stevens formula</li>
      <li><strong>p-adic Automorphic Forms:</strong> Established control theorems for p-adic automorphic forms and Teitelbaum's L-invariant</li>
      <li><strong>Boundary Distributions:</strong> Studied boundary distributions for GL3 over local fields and their relationship to symmetric power coefficients</li>
    </ul>

    <h3>Teaching Experience</h3>
    <p>During his time at Heidelberg University, Peter was involved in various teaching activities:</p>
    <ul>
      <li><strong>Working Group Seminars:</strong> Plectic Stark-Heegner points (WS 2021/22), Higher Hida theory (SS 2021), p-adic Uniformization (SS 2016)</li>
      <li><strong>Lectures:</strong> Linear algebra 1 & 2, Introduction to geometry, Complex analysis 1 & 2</li>
      <li><strong>Proseminars:</strong> p-adic Analysis (SS 2016)</li>
    </ul>

    <div class="contact-info">
      <h3>Contact</h3>
      <p>For questions about Peter's research or publications:</p>
      <p><strong>Email:</strong> <a href="mailto:arithgeo@iwr.uni-heidelberg.de">arithgeo@iwr.uni-heidelberg.de</a></p>
      <p><strong>Personal Website:</strong> <a href="https://sites.google.com/view/peter-graef" target="_blank">https://sites.google.com/view/peter-graef</a></p>
    </div>
  </div>
</div>

<style>
.heidelberg-style-publications {
  font-family: Arial, sans-serif;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.pathway {
  background: #f5f5f5;
  padding: 10px;
  margin-bottom: 20px;
  border-left: 4px solid #c22032;
  font-size: 0.9em;
}

.pathway a {
  color: #c22032;
  text-decoration: none;
}

.pathway a:hover {
  text-decoration: underline;
}

.member-info {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
  padding: 20px;
  background: #f9f9f9;
  border-radius: 5px;
}

.member-photo {
  width: 150px;
  height: 225px;
  object-fit: cover;
  border-radius: 5px;
}

.member-details h3 {
  color: #c22032;
  margin-top: 0;
}

.publication-list, .thesis-list, .presentation-list, .poster-list {
  list-style: none;
  padding: 0;
}

.publication-list li, .thesis-list li, .presentation-list li, .poster-list li {
  margin-bottom: 15px;
  padding: 15px;
  background: #f9f9f9;
  border-left: 4px solid #c22032;
  border-radius: 3px;
}

.publication-list li strong, .thesis-list li strong, .presentation-list li strong, .poster-list li strong {
  color: #c22032;
}

.download {
  color: #c22032;
  text-decoration: none;
  font-weight: bold;
}

.download:hover {
  text-decoration: underline;
}

.contact-info {
  margin-top: 30px;
  padding: 20px;
  background: #f9f9f9;
  border-radius: 5px;
}

.contact-info h3 {
  color: #c22032;
  margin-top: 0;
}

h2, h3 {
  color: #c22032;
  border-bottom: 2px solid #c22032;
  padding-bottom: 5px;
}

@media (max-width: 768px) {
  .member-info {
    flex-direction: column;
  }
  
  .member-photo {
    width: 120px;
    height: 180px;
  }
}
</style> 