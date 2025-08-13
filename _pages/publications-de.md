---
layout: page
permalink: "/publications-de/"
nav: true
nav_order: 5
order: 100
show_title: false
title: Publications De
---
<div class="heidelberg-style-publications">
  <!-- Breadcrumb Navigation -->
  <div class="pathway">
    <div style="float:left;">
      <a href="https://www.uni-heidelberg.de">Uni Heidelberg</a> &gt; 
      <a href="{{ '/' | relative_url }}">IWR</a> &gt; 
      <a href="{{ '/' | relative_url }}">ARITHGEO</a> &gt; 
      Publikationen
    </div>
    <div style="float:right;">
      [<a href="{{ '/publications/' | relative_url }}">english</a>]&nbsp;|&nbsp;[<a href="{{ '/publications-de/' | relative_url }}">deutsch</a>]
    </div>
  </div>
  <br>

  <!-- Main Content -->
  <div class="publications-content">
    <h2>Publikationen und Preprints unserer Forschungsgruppe:</h2>
    
    <!-- Publications by Type -->
    <div class="publications-by-type">
      <h3>Journal-Artikel</h3>
      {% assign journal_pubs = site.publications | where: "type", "Journal Article" | sort: 'year' | reverse %}
      {% if journal_pubs.size > 0 %}
        <div class="publications-grid">
          {% for publication in journal_pubs limit: 10 %}
            <div class="publication-item">
              <h4><a href="{{ publication.url }}">{{ publication.title }}</a></h4>
              <div class="publication-authors">{{ publication.authors }}</div>
              <div class="publication-venue">{{ publication.journal }}{% if publication.volume %}, {{ publication.volume }}{% endif %}{% if publication.pages %}, {{ publication.pages }}{% endif %}, {{ publication.year }}</div>
              <div class="publication-links">
                {% if publication.url %}
                  <a href="{{ publication.url }}" target="_blank">View</a>
                {% endif %}
              </div>
            </div>
          {% endfor %}
        </div>
      {% else %}
        <p>Keine Journal-Artikel gefunden.</p>
      {% endif %}

      <h3>Preprints</h3>
      {% assign preprint_pubs = site.publications | where: "type", "Preprint" | sort: 'year' | reverse %}
      {% if preprint_pubs.size > 0 %}
        <div class="publications-grid">
          {% for publication in preprint_pubs %}
            <div class="publication-item">
              <h4><a href="{{ publication.url }}">{{ publication.title }}</a></h4>
              <div class="publication-authors">{{ publication.authors }}</div>
              <div class="publication-venue">{{ publication.year }}</div>
              <div class="publication-links">
                {% if publication.arxiv_id %}
                  <a href="https://arxiv.org/abs/{{ publication.arxiv_id }}" target="_blank">arXiv</a>
                {% endif %}
                {% if publication.url %}
                  <a href="{{ publication.url }}" target="_blank">View</a>
                {% endif %}
              </div>
            </div>
          {% endfor %}
        </div>
      {% else %}
        <p>Keine Preprints gefunden.</p>
      {% endif %}

      <h3>Software-Pakete</h3>
      {% assign software_pubs = site.publications | where: "type", "Software" | sort: 'year' | reverse %}
      {% if software_pubs.size > 0 %}
        <div class="publications-grid">
          {% for publication in software_pubs %}
            <div class="publication-item">
              <h4><a href="{{ publication.url }}">{{ publication.title }}</a></h4>
              <div class="publication-authors">{{ publication.authors }}</div>
              <div class="publication-venue">{{ publication.year }}</div>
              <div class="publication-links">
                {% if publication.url %}
                  <a href="{{ publication.url }}" target="_blank">Repository</a>
                {% endif %}
                {% if publication.pdf %}
                  <a href="{% if publication.pdf contains '://' %}{{ publication.pdf }}{% else %}{{ publication.pdf | relative_url }}{% endif %}" target="_blank">PDF</a>
                {% endif %}
              </div>
            </div>
          {% endfor %}
        </div>
      {% else %}
        <p>Keine Software-Pakete gefunden.</p>
      {% endif %}
    </div>

    <!-- Member Publications Links -->
    <h3>Publikationen nach Mitgliedern:</h3>
    <ul class="member-publications">
      <li><a href="{{ '/members/gebhard-boeckle/publications/' | relative_url }}" class="internal-link">Prof. Dr. Gebhard Böckle</a></li>
      <li><a href="https://members.vistaserv.net/barinder" target="_blank" class="external-link">Dr. Barinder Banwait</a></li>
      <li><a href="{{ '/members/peter-graef/publications/' | relative_url }}" class="internal-link">Dr. Peter Gräf</a></li>
    </ul>
  </div>

  <!-- Footer -->
  <hr class="ce-div">
  <table width="100%">
    <tbody>
      <tr>
        <td align="right">
          <div class="bearbeiter">
            <a href="mailto:arithgeo@iwr.uni-heidelberg.de?subject=Über%20Publikationen">arithgeo@iwr.uni-heidelberg.de</a><br>
            Letzte Aktualisierung: 04.06.2024 - 16:09<br>
          </div>
        </td>
      </tr>
    </tbody>
  </table>
</div>

<style>
/* Heidelberg-style Publications Page */
.heidelberg-style-publications {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
  line-height: 1.6;
}

/* Breadcrumb Navigation */
.pathway {
  background: #f5f5f5;
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-bottom: 20px;
  overflow: hidden;
}

.pathway a {
  color: #0066cc;
  text-decoration: none;
  font-weight: 500;
}

.pathway a:hover {
  text-decoration: underline;
}

.pathway div[style*="float:right"] a {
  color: #333;
  font-weight: normal;
}

/* Main Content */
.publications-content {
  background: white;
  padding: 30px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.publications-content h2 {
  color: #333;
  font-size: 1.5em;
  font-weight: bold;
  margin: 30px 0 15px 0;
  padding-bottom: 8px;
  border-bottom: 2px solid #0066cc;
}

.publications-content h2:first-child {
  margin-top: 0;
}

/* Member Publications List */
.member-publications {
  list-style: none;
  padding: 0;
  margin: 0 0 30px 0;
}

.member-publications li {
  margin-bottom: 12px;
  padding: 8px 0;
}

.member-publications a {
  color: #0066cc;
  text-decoration: none;
  font-weight: 500;
  padding: 8px 12px;
  border-radius: 4px;
  transition: all 0.2s ease;
  display: inline-block;
}

.member-publications a:hover {
  background: #f0f8ff;
  text-decoration: underline;
}

/* Software Packages List */
.software-packages {
  list-style: none;
  padding: 0;
  margin: 0;
}

.software-packages li {
  margin-bottom: 20px;
  padding: 15px;
  background: #f9f9f9;
  border-left: 4px solid #0066cc;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.software-packages li:hover {
  background: #f0f8ff;
  transform: translateX(5px);
}

.software-packages a {
  color: #0066cc;
  text-decoration: none;
  font-weight: 500;
}

.software-packages a:hover {
  text-decoration: underline;
}

.software-packages a.download {
  color: #28a745;
  font-weight: bold;
}

.software-packages a.download:hover {
  color: #218838;
}

/* Link Types */
.internal-link {
  position: relative;
}

.internal-link::after {
  content: " (intern)";
  font-size: 0.8em;
  color: #666;
  font-weight: normal;
}

.external-link {
  position: relative;
}

.external-link::after {
  content: " (extern)";
  font-size: 0.8em;
  color: #666;
  font-weight: normal;
}

/* Divider */
.ce-div {
  border: none;
  height: 1px;
  background: #ddd;
  margin: 30px 0;
}

/* Footer */
.bearbeiter {
  font-size: 0.9em;
  color: #666;
  line-height: 1.4;
}

.bearbeiter a {
  color: #0066cc;
  text-decoration: none;
}

.bearbeiter a:hover {
  text-decoration: underline;
}

/* Responsive Design */
@media (max-width: 768px) {
  .heidelberg-style-publications {
    padding: 10px;
  }
  
  .publications-content {
    padding: 20px;
  }
  
  .pathway {
    font-size: 0.9em;
  }
  
  .pathway div[style*="float:left"] {
    float: none !important;
    margin-bottom: 10px;
  }
  
  .pathway div[style*="float:right"] {
    float: none !important;
    text-align: left;
  }
  
  .software-packages li {
    padding: 12px;
  }
}

@media (max-width: 480px) {
  .publications-content {
    padding: 15px;
  }
  
  .publications-content h2 {
    font-size: 1.3em;
  }
  
  .member-publications a,
  .software-packages a {
    display: block;
    padding: 10px;
    margin: 5px 0;
  }
}
</style> 