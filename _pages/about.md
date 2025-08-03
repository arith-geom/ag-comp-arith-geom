---
layout: page
title: About
permalink: /about/
nav: true
---

<div class="about-hero mb-5">
  <img src="{{ site.baseurl }}/assets/img/heidelberg_castle.jpg" alt="Heidelberg Castle" class="about-hero-image">
  <div class="about-hero-overlay">
    <div class="about-hero-content">
      <h1 class="about-hero-title">About Our Research Group</h1>
      <p class="about-hero-subtitle">Interdisciplinary Center for Scientific Computing (IWR), Heidelberg</p>
    </div>
  </div>
</div>

<style>
.about-hero {
  position: relative;
  width: 100%;
  height: 350px;
  overflow: hidden;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.15);
  margin-bottom: 3rem;
}

.about-hero-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}

.about-hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(0,0,0,0.6) 0%, rgba(0,0,0,0.3) 50%, rgba(0,0,0,0.1) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.about-hero-content {
  text-align: center;
  color: white;
  padding: 2rem;
}

.about-hero-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
}

.about-hero-subtitle {
  font-size: 1.3rem;
  font-weight: 400;
  margin: 0;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.8);
}

@media (max-width: 768px) {
  .about-hero {
    height: 250px;
  }
  
  .about-hero-title {
    font-size: 2rem;
  }
  
  .about-hero-subtitle {
    font-size: 1.1rem;
  }
}
</style>

<div class="translatable-content" data-translation-key="about.description">
  This is the website of the research group "computational arithmetic geometry" at the Interdisciplinary Center for Scientific Computing (IWR) in Heidelberg.
</div>

<div class="translatable-content" data-translation-key="about.content">
  Within algebraic number theory and arithmetic geometry, the focus of the research group is on Galois representations, their relations to modular forms and elliptic curves, their deformation theory etc., as well as on some aspects of function field arithmetic such as $L$-functions and Drinfeld modular forms.
</div>

<div class="translatable-content" data-translation-key="about.methods">
  To tackle problems in the themes described above, we apply a broad range of methods. On one hand we pursue these questions by purely theoretical methods. On the other, we use computer algebra to carry out experiments that help us gather examples for the theory or to solve particular questions that arise from the theory. Some members of our group have also developed routines on top of existing computer algebra packages.
</div>

<div class="translatable-content" data-translation-key="about.more_info">
  A more detailed survey of our activities can be found in the research section and in the publications of our members.
</div>

<!-- Website Credits Section -->
<div class="website-credits-section mt-5 pt-4 border-top">
  <div class="row">
    <div class="col-md-8 mx-auto">
      <h4 class="text-center mb-3">Website Credits</h4>
      <div class="credits-content text-center">
        <p class="text-muted mb-2">
          This website was designed and developed by 
          <a href="https://github.com/VictorMerk" target="_blank" rel="noopener" class="creator-link">
            Victor Merk
          </a>
          as part of a comprehensive web development project.
        </p>
        <p class="text-muted small">
          Built with modern web technologies including Jekyll, Bootstrap, and custom JavaScript. 
          Features include responsive design, dark mode support, and a content management system.
        </p>
      </div>
    </div>
  </div>
</div>

<style>
.website-credits-section {
  background: var(--bg-secondary, #f8f9fa);
  border-radius: 8px;
  padding: 2rem;
  margin-top: 3rem;
}

.website-credits-section h4 {
  color: var(--text-primary, #212529);
  font-weight: 600;
}

.credits-content .creator-link {
  color: var(--link-color, #C22032);
  text-decoration: none;
  font-weight: 500;
  transition: all 0.2s ease;
}

.credits-content .creator-link:hover {
  color: var(--link-hover, #991B1B);
  text-decoration: underline;
}

/* Dark mode styles */
[data-theme="dark"] .website-credits-section,
body.dark-mode .website-credits-section {
  background: var(--bg-secondary, #1a1a1a);
  border-color: var(--border-color, #374151);
}

[data-theme="dark"] .website-credits-section h4,
body.dark-mode .website-credits-section h4 {
  color: var(--text-primary, #FFFFFF);
}

[data-theme="dark"] .credits-content .creator-link,
body.dark-mode .credits-content .creator-link {
  color: var(--link-color, #FF6B6B);
}

[data-theme="dark"] .credits-content .creator-link:hover,
body.dark-mode .credits-content .creator-link:hover {
  color: var(--link-hover, #FF5252);
}
</style>

 