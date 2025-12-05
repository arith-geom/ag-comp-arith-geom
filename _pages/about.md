---
layout: page
permalink: "/about/"
nav: true
nav_order: 1
order: 100
show_title: false
title: About
excerpt_separator: ""
---
<h1 class="home-page-title">AG Computational Arithmetic Geometry</h1>

<div class="home-card">
  <h2>About Our Research Group</h2>
  <p>This is the website of the research group "computational arithmetic geometry" at the Interdisciplinary Center for Scientific Computing (IWR) in Heidelberg.</p>
</div>

<div class="home-card">
  <h2>Research Focus</h2>
  <p>Within algebraic number theory and arithmetic geometry, the focus of the research group is on Galois representations, their relations to modular forms and elliptic curves, their deformation theory etc., as well as on some aspects of function field arithmetic such as L-functions and Drinfeld modular forms.</p>
</div>

<div class="home-card">
  <h2>Our Methods</h2>
  <p>To tackle problems in the themes described above, we apply a broad range of methods. On one hand we pursue these questions by purely theoretical methods. On the other, we use computer algebra to carry out experiments that help us gather examples for the theory or to solve particular questions that arise from the theory. Some members of our group have also developed routines on top of existing computer algebra packages.</p>
</div>

<div class="home-card">
  <h2>Learn More</h2>
  <p>A more detailed survey of our activities can be found in the research section and in the publications of our members.</p>
</div>

<div class="home-card">
  <h2>Contact Us</h2>
  <p><strong>Email:</strong> arithgeo@iwr.uni-heidelberg.de</p>
  <p><strong>Location:</strong> Interdisciplinary Center for Scientific Computing (IWR), Heidelberg University</p>
</div>

<div class="home-card">
  <h2>Current Members</h2>

  <div class="member-info">
    <h3>Prof. Dr. Gebhard Böckle</h3>
    <p><strong>Role:</strong> Group Leader</p>
    <p><strong>Email:</strong> arithgeo@iwr.uni-heidelberg.de</p>
  </div>

  <div class="member-info">
    <h3>Dr. Barinder Banwait</h3>
    <p><strong>Role:</strong> Researcher</p>
    <p><strong>Email:</strong> arithgeo@iwr.uni-heidelberg.de</p>
  </div>

  <div class="member-info">
    <h3>Dr. Peter Gräf</h3>
    <p><strong>Role:</strong> Former PhD Student (2015-2020)</p>
    <p><strong>Email:</strong> arithgeo@iwr.uni-heidelberg.de</p>
  </div>
</div>

<div class="home-card">
  <h2>Software Development</h2>

  <p>Our group has developed several software packages:</p>

  <div class="software-package">
    <h3>QaQuotGraphs</h3>
    <p><strong>Author:</strong> Dr. Ralf Butenuth</p>
    <p><strong>Description:</strong> Magma package to compute the action by unit groups of maximal orders in quaternion algebras over $F_q(T)$</p>
    <p><strong>Category:</strong> Quaternion Algebras</p>
  </div>

  <div class="software-package">
    <h3>Bruhat-Tits Buildings Package</h3>
    <p><strong>Author:</strong> Lutz Hofmann (Former Master's student)</p>
    <p><strong>Description:</strong> Magma package to compute quotients of Bruhat-Tits buildings over function fields modulo congruence subgroups and the action of Hecke operators on harmonic cocycles with coefficients in char. 0</p>
    <p><strong>Category:</strong> Bruhat-Tits Buildings</p>
  </div>

  <div class="software-package">
    <h3>Hecke Eigensystems Package</h3>
    <p><strong>Author:</strong> Burak Cakir (Master's student)</p>
    <p><strong>Description:</strong> Magma package to compute Hecke eigensystems for harmonic cocycles on the Bruhat-Tits tree for $GL_2(F_q(T))$</p>
    <p><strong>Category:</strong> Hecke Operators</p>
  </div>
</div>

<div class="home-card">
  <h2>Contact Information</h2>
  <ul>
    <li><strong>Email:</strong> arithgeo@iwr.uni-heidelberg.de</li>
    <li><strong>Institution:</strong> Ruprecht-Karls-Universität Heidelberg</li>
    <li><strong>Department:</strong> Interdisciplinary Center for Scientific Computing (IWR)</li>
    <li><strong>Group:</strong> AG Computational Arithmetic Geometry</li>
  </ul>
</div>

<div class="home-card">
  <h2>Location</h2>
  <p>Interdisciplinary Center for Scientific Computing (IWR)</p>
  <p>Heidelberg University</p>
  <p>Germany</p>
</div>

---

*Last updated: 2024-06-04*

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

/* Style software packages */
[data-theme="dark"] .software-package,
body.dark-mode .software-package {
  background: var(--bg-secondary) !important;
  padding: 1rem !important;
  border-radius: var(--radius-md) !important;
  margin-bottom: 1rem !important;
  border-left: 3px solid var(--border-color) !important;
}

[data-theme="dark"] .software-package h3,
body.dark-mode .software-package h3 {
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
