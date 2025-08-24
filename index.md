---
layout: page
title: "Computational Arithmetic Geometry"
permalink: /
nav_order: 1
---

<div class="hero-header mb-5">
  <img src="{{ '/assets/img/Design ohne Titel.png' | relative_url }}" alt="Heidelberg Castle with IWR/University logos" class="hero-image">
  <div class="hero-overlay">
    <div class="hero-content">
      <h1 class="hero-title">AG Computational Arithmetic Geometry</h1>
      <p class="hero-subtitle">Prof. Dr. Gebhard Böckle</p>
    </div>
  </div>
</div>

<style>
.hero-header {
  position: relative;
  width: 100%;
  height: 500px; /* smaller height */
  overflow: hidden;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.15);
  margin-bottom: 3rem;
}

.hero-image {
  width: 100%;
  height: 100%;
  object-fit: cover; /* fill width, crop bottom */
  object-position: 50% 0%; /* focus the top area (show logos) */
  background: transparent;
}

.hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(0,0,0,0.7) 0%, rgba(0,0,0,0.4) 50%, rgba(0,0,0,0.2) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero-content {
  text-align: center;
  color: white;
  padding: 2rem;
}

/* Ensure hero text stays white even with global heading overrides */
.hero-title,
.hero-subtitle {
  color: var(--white) !important;
}

.hero-title {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
}

.hero-subtitle {
  font-size: 1.5rem;
  font-weight: 400;
  margin: 0;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.8);
}

@media (max-width: 768px) {
  .hero-header {
    height: 360px; /* smaller on mobile too */
  }
  
  .hero-title {
    font-size: 2rem;
  }
  
  .hero-subtitle {
    font-size: 1.2rem;
  }
}

/* Content Sections Styles */
.content-sections {
  width: 100%;
  margin: 0;
  padding-left: 1rem;
  padding-right: 1rem;
}

.content-section {
  margin-bottom: 0.25rem;
  padding: 2rem;
  background: var(--bg-primary);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-base);
}

.content-section:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.section-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.125rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid var(--primary);
}

.section-icon {
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, var(--primary) 0%, var(--heidelberg-red) 100%);
  color: var(--primary-text);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  box-shadow: var(--shadow-sm);
}

.section-header h3 {
  color: var(--text-primary);
  font-size: 1.8rem;
  font-weight: 600;
  margin: 0;
}

.content-section p {
  color: var(--text-secondary);
  font-size: 1.1rem;
  line-height: 1.7;
  margin-bottom: 1rem;
}

.cta-buttons {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  margin-top: 1.5rem;
}

.cta-buttons .btn {
  padding: 0.75rem 1.5rem;
  font-weight: 500;
  border-radius: var(--radius-md);
  transition: all var(--transition-base);
}

.cta-buttons .btn:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.contact-section {
  background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
  border: 2px solid var(--primary);
}

.contact-info {
  background: var(--bg-secondary);
  padding: 1.5rem;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-color);
}

.contact-info p {
  margin-bottom: 0.5rem;
  font-size: 1rem;
}

.contact-info a {
  color: var(--primary);
  text-decoration: none;
  font-weight: 500;
}

.contact-info a:hover {
  text-decoration: underline;
}

/* Responsive adjustments for content sections */
@media (max-width: 768px) {
  .content-section {
    padding: 1.5rem;
  }
  
  .section-header {
    flex-direction: column;
    text-align: center;
    gap: 0.5rem;
  }
  
  .section-icon {
    width: 40px;
    height: 40px;
    font-size: 1rem;
  }
  
  .section-header h3 {
    font-size: 1.5rem;
  }
  
  .cta-buttons {
    flex-direction: column;
  }
  
  .cta-buttons .btn {
    width: 100%;
    text-align: center;
  }
}

@media (max-width: 480px) {
  .content-section {
    padding: 1rem;
  }
  
  .contact-info {
    padding: 1rem;
  }
}
</style>



<div class="content-sections">
  <div class="content-section">
    <div class="section-header">
      <div class="section-icon">
        <i class="fas fa-university" aria-hidden="true"></i>
      </div>
      <h3>About Our Research Group</h3>
    </div>
    <p>This is the website of the research group "computational arithmetic geometry" at the Interdisciplinary Center for Scientific Computing (IWR) in Heidelberg.</p>
  </div>

  <div class="content-section">
    <div class="section-header">
      <div class="section-icon">
        <i class="fas fa-microscope" aria-hidden="true"></i>
      </div>
      <h3>Research Focus</h3>
    </div>
    <p>Within algebraic number theory and arithmetic geometry, the focus of the research group is on Galois representations, their relations to modular forms and elliptic curves, their deformation theory etc., as well as on some aspects of function field arithmetic such as L-functions and Drinfeld modular forms.</p>
  </div>

  <div class="content-section">
    <div class="section-header">
      <div class="section-icon">
        <i class="fas fa-cogs" aria-hidden="true"></i>
      </div>
      <h3>Our Methods</h3>
    </div>
    <p>To tackle problems in the themes described above, we apply a broad range of methods. On one hand we pursue these questions by purely theoretical methods. On the other, we use computer algebra to carry out experiments that help us gather examples for the theory or to solve particular questions that arise from the theory. Some members of our group have also developed routines on top of existing computer algebra packages.</p>
  </div>

  <div class="content-section">
    <div class="section-header">
      <div class="section-icon">
        <i class="fas fa-book" aria-hidden="true"></i>
      </div>
      <h3>Learn More</h3>
    </div>
    <p>A more detailed survey of our activities can be found in the research section and in the publications of our members.</p>
    <div class="cta-buttons">
      <a href="{{ '/research/' | relative_url }}" class="btn btn-outline-primary">
        <i class="fas fa-search me-2" aria-hidden="true"></i>Research Areas
      </a>
      <a href="{{ '/publications/' | relative_url }}" class="btn btn-outline-primary">
        <i class="fas fa-file-alt me-2" aria-hidden="true"></i>Publications
      </a>
      <a href="{{ '/members/' | relative_url }}" class="btn btn-outline-primary">
        <i class="fas fa-users me-2" aria-hidden="true"></i>Our Team
      </a>
    </div>
  </div>

  <div class="content-section contact-section">
    <div class="section-header">
      <div class="section-icon">
        <i class="fas fa-envelope" aria-hidden="true"></i>
      </div>
      <h3>Contact Us</h3>
    </div>
    <div class="contact-info">
      <p><strong>Email:</strong> <a href="mailto:arithgeo@iwr.uni-heidelberg.de">arithgeo@iwr.uni-heidelberg.de</a></p>
      <p><strong>Location:</strong> Interdisciplinary Center for Scientific Computing (IWR), Heidelberg University</p>
    </div>
  </div>
</div>
