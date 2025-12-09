---
layout: page
permalink: "/home/"
nav: true
nav_order: 1
order: 100
show_title: false
title: Home
description: "Official website of the Computational Arithmetic Geometry research group at Heidelberg University."
about_title: "About Our Research Group"
about_content: |
  <p>This is the website of the research group "computational arithmetic geometry" at the <a href="http://www.iwr.uni-heidelberg.de/">Interdisciplinary Center for Scientific Computing (IWR)</a> in <a href="http://www.heidelberg.de/">Heidelberg</a>.</p>
  <p>Within algebraic number theory and arithmetic geometry, the focus of the research group is on Galois representations, their relations to modular forms and elliptic curves, their deformation theory etc., as well as on some aspects of function field arithmetic such as L-functions and Drinfeld modular forms.</p>
methods_title: "Our Methods"
methods_content: |
  <p>To tackle problems in the themes described above, we apply a broad range of methods. On one hand we pursue these questions by purely theoretical methods. On the other, we use computer algebra to carry out experiments that help us gather examples for the theory or to solve particular questions that arise from the theory. Some members of our group have also developed routines on top of existing computer algebra packages.</p>
  <p>A more detailed survey of our activities can be found in the <a href="/research/">research section</a> and in the <a href="/publications/">publications</a> of our members.</p>

contact_title: "Contact Us"
contact_email: "arithgeo@iwr.uni-heidelberg.de"
contact_location: "Interdisciplinary Center for Scientific Computing (IWR), Heidelberg University"
excerpt_separator: ""
---
<h1 class="home-page-title">AG Computational Arithmetic Geometry</h1>

<div class="home-card">
  <h2>{{ page.about_title | escape }}</h2>
  {{ page.about_content | strip_html }}
</div>

<div class="home-card">
  <h2>{{ page.methods_title | escape }}</h2>
  {{ page.methods_content | strip_html }}
</div>



<div class="home-card">
  <h2>{{ page.contact_title }}</h2>
  <p><strong>Email:</strong> {{ page.contact_email | escape }}</p>
  <p><strong>Location:</strong> {{ page.contact_location | escape }}</p>
</div>

<style>
/* Light mode Home page title and leader name colors */
.page-article h1,
.home-page-title {
  color: var(--white) !important;
}

.page-article .leader-name {
  color: var(--heidelberg-red);
}

/* Improve title/subtitle visibility in dark mode on Home and Links */
[data-theme="dark"] .page-article h1,
body.dark-mode .page-article h1,
[data-theme="dark"] .page-article h2,
body.dark-mode .page-article h2 {
  color: var(--text-primary) !important;
}

[data-theme="dark"] .page-article .desc,
body.dark-mode .page-article .desc {
  color: var(--text-muted) !important;
}

/* Ensure profile/image blocks on Home stay visible in dark mode */
[data-theme="dark"] .profile img,
body.dark-mode .profile img,
[data-theme="dark"] .profile .more-info,
body.dark-mode .profile .more-info {
  filter: none !important;
  opacity: 1 !important;
  visibility: visible !important;
}

/* Dark mode styling for the main article container */
[data-theme="dark"] .page-article,
body.dark-mode .page-article {
  background: var(--bg-primary) !important;
  border-color: var(--border-dark) !important;
  box-shadow: var(--shadow-lg) !important;
}

/* Light mode styling for home cards */
.home-card {
  background: var(--bg-primary);
  border: 3px solid red !important;
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  margin-bottom: 0.25rem;
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-base);
}

.home-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
  border-color: var(--primary);
}

.home-card h2 {
  color: var(--text-primary);
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 0;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid var(--primary);
}

/* Dark mode styling for home cards - matching other pages */
[data-theme="dark"] .home-card,
body.dark-mode .home-card {
  background: var(--bg-primary) !important;
  border-color: var(--border-color) !important;
  box-shadow: var(--shadow-sm) !important;
}

[data-theme="dark"] .home-card:hover,
body.dark-mode .home-card:hover {
  transform: translateY(-4px) !important;
  box-shadow: 0 8px 24px rgba(248, 113, 113, 0.2) !important;
  border-color: var(--primary) !important;
}

[data-theme="dark"] .home-card h2,
body.dark-mode .home-card h2 {
  color: var(--text-primary) !important;
  border-bottom-color: var(--primary) !important;
}

[data-theme="dark"] .home-card:hover,
body.dark-mode .home-card:hover {
  border-color: var(--primary) !important;
  box-shadow: 0 8px 24px rgba(248, 113, 113, 0.2) !important;
  transform: translateY(-4px) !important;
}

/* Style section headers in cards consistently */
[data-theme="dark"] .home-card h2,
body.dark-mode .home-card h2 {
  color: var(--text-primary) !important;
  border-bottom-color: var(--primary) !important;
  padding-bottom: 0.5rem !important;
  margin-bottom: 0 !important;
  font-weight: 600 !important;
}



/* Style subsections within cards */
[data-theme="dark"] .home-subsection,
body.dark-mode .home-subsection {
  background: var(--bg-secondary) !important;
  padding: 1rem !important;
  border-radius: var(--radius-md) !important;
  margin-bottom: 1rem !important;
  border-left: 3px solid var(--border-color) !important;
}

[data-theme="dark"] .home-subsection h3,
body.dark-mode .home-subsection h3 {
  background: var(--bg-secondary) !important;
  color: var(--text-primary) !important;
  padding: 0.5rem 0.75rem !important;
  border-radius: var(--radius-sm) !important;
  border-left: 3px solid var(--primary) !important;
  margin: -1rem -1rem 0.5rem -1rem !important;
  font-weight: 600 !important;
}

/* Style member info sections */
[data-theme="dark"] .member-info,
body.dark-mode .member-info {
  background: var(--bg-secondary) !important;
  padding: 1rem !important;
  border-radius: var(--radius-md) !important;
  margin-bottom: 1rem !important;
  border-left: 3px solid var(--border-color) !important;
}

[data-theme="dark"] .member-info h3,
body.dark-mode .member-info h3 {
  color: var(--text-primary) !important;
  margin-top: 0 !important;
  margin-bottom: 0.5rem !important;
  font-weight: 600 !important;
}



/* Ensure links and buttons have proper contrast */
[data-theme="dark"] .page-article a,
body.dark-mode .page-article a {
  color: var(--link-color) !important;
}

[data-theme="dark"] .page-article strong,
body.dark-mode .page-article strong {
  color: var(--primary) !important;
  font-weight: 600 !important;
}
</style>
