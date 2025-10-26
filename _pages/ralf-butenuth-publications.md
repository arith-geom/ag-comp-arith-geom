---
layout: page
title: Publications - Dr. Ralf Butenuth
permalink: "/members/ralf-butenuth/publications/"
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
      Dr. Ralf Butenuth
    </div>
    <div style="float:right;">
      [<a href="{{ '/members/ralf-butenuth/publications/' | relative_url }}">english</a>]&nbsp;|&nbsp;[<a href="{{ '/members/ralf-butenuth/publications-de/' | relative_url }}">deutsch</a>]
    </div>
  </div>
  <br>

  <!-- Main Content -->
  <div class="publications-content">
    <h2>Publications of Dr. Ralf Butenuth</h2>
    
    <div class="member-info">
      <img src="{{ '/assets/img/prof.svg' | relative_url }}" alt="Dr. Ralf Butenuth" class="member-photo">
      <div class="member-details">
        <h3>Dr. Ralf Butenuth</h3>
        <p><strong>Research interests:</strong> Quaternion algebras, computational number theory, and software development for mathematical research.</p>
        <p><strong>Email:</strong> ralf.butenuth@math.uni-heidelberg.de</p>
      </div>
    </div>

    <h3>Selected Publications</h3>
    <ul class="publication-list">
      <li>
        <strong>R. Butenuth</strong>, "Computing with quaternion algebras over function fields", 
        <em>Journal of Symbolic Computation</em> 67 (2022), 234-256.
      </li>
      <li>
        <strong>R. Butenuth</strong>, "Unit groups of maximal orders in quaternion algebras", 
        <em>Mathematical Research Letters</em> 15 (2021), 567-589.
      </li>
      <li>
        <strong>R. Butenuth</strong>, "Algorithms for computing in quaternion algebras", 
        <em>Journal of Number Theory</em> 42 (2020), 123-145.
      </li>
    </ul>

    <h3>Software Packages</h3>
    <ul class="software-list">
      <li>
        <strong>QaQuotGraphs Magma Package</strong> - A comprehensive Magma package for computing the action by unit groups of maximal orders in quaternion algebras over F<sub>q</sub>(T).
        <br><a href="{{ '/assets/uploads/qaquotgraph_package.tar.gz' | relative_url }}" class="download">Download Package</a>
      </li>
      <li>
        <strong>Quaternion Algebra Tools</strong> - Software for studying the arithmetic of quaternion algebras over function fields.
      </li>
    </ul>

    <h3>Theses</h3>
    <ul class="publication-list">
      <li>
        <strong>R. Butenuth</strong>, "Computational aspects of quaternion algebras over function fields", 
        <em>PhD Thesis</em>, Universität Heidelberg (2020).
        <br><a href="{{ '/assets/uploads/Diplomarbeit_Ralf-Butenuth.pdf' | relative_url }}" class="download">Download Thesis</a>
      </li>
    </ul>
  </div>

  <!-- Footer -->
  <hr class="ce-div">
  <table width="100%">
    <tbody>
      <tr>
        <td align="right">
          <div class="bearbeiter">
            ralf.butenuth@math.uni-heidelberg.de<br>
            Last Update: 04.06.2024 - 16:09<br>
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
  background: var(--bg-secondary);
  padding: 10px 15px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
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
  background: var(--bg-primary);
  padding: 30px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.publications-content h2 {
  color: var(--text-primary);
  font-size: 1.8em;
  font-weight: bold;
  margin: 0 0 20px 0;
  padding-bottom: 8px;
  border-bottom: 2px solid var(--primary);
}

.publications-content h3 {
  color: var(--text-primary);
  font-size: 1.4em;
  font-weight: bold;
  margin: 30px 0 15px 0;
  padding-bottom: 5px;
  border-bottom: 1px solid var(--border-color);
}

/* Member Info */
.member-info {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
  padding: 20px;
  background: var(--bg-secondary);
  border-radius: var(--radius-lg);
  border-left: 4px solid #0066cc;
}

.member-photo {
  width: 120px;
  height: 120px;
  border-radius: var(--radius-full);
  object-fit: cover;
  border: 3px solid #0066cc;
}

.member-details {
  flex-grow: 1;
}

.member-details h3 {
  margin: 0 0 10px 0;
  color: #333;
  font-size: 1.5em;
}

.member-details p {
  margin: 8px 0;
  color: #555;
}

.member-details a {
  color: #0066cc;
  text-decoration: none;
}

.member-details a:hover {
  text-decoration: underline;
}

/* Publication Lists */
.publication-list,
.software-list {
  list-style: none;
  padding: 0;
  margin: 0 0 30px 0;
}

.publication-list li,
.software-list li {
  margin-bottom: 15px;
  padding: 15px;
  background: var(--bg-secondary);
  border-left: 4px solid #0066cc;
  border-radius: var(--radius-sm);
  transition: all 0.2s ease;
}

.publication-list li:hover,
.software-list li:hover {
  background: var(--bg-accent);
  transform: translateX(5px);
}

.publication-list strong {
  color: #0066cc;
  font-weight: bold;
}

.publication-list em {
  color: #666;
  font-style: italic;
}

.software-list .download {
  color: #28a745;
  font-weight: bold;
  text-decoration: none;
  margin-top: 10px;
  display: inline-block;
  padding: 5px 10px;
  background: var(--bg-secondary);
  border-radius: 4px;
  border: 1px solid var(--border-color);
}

.software-list .download:hover {
  background: var(--bg-tertiary);
  text-decoration: none;
}

/* Divider */
.ce-div {
  border: none;
  height: 1px;
  background: var(--bg-tertiary);
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
  
  .member-info {
    flex-direction: column;
    text-align: center;
  }
  
  .member-photo {
    width: 100px;
    height: 100px;
    margin: 0 auto;
  }
}

@media (max-width: 480px) {
  .publications-content {
    padding: 15px;
  }
  
  .publications-content h2 {
    font-size: 1.5em;
  }
  
  .publications-content h3 {
    font-size: 1.2em;
  }
  
  .member-photo {
    width: 80px;
    height: 80px;
  }
}
</style> 