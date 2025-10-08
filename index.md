---
layout: page
title: "Computational Arithmetic Geometry"
permalink: /
nav_order: 1
---

<div class="hero-header">
  <img src="{{ '/assets/img/Design ohne Titel.png' | relative_url }}" alt="Heidelberg Castle with IWR/University logos" class="hero-image">
  <div class="hero-overlay">
    <div class="hero-content">
      <h1 class="hero-title">AG Computational Arithmetic Geometry</h1>
      <p class="hero-subtitle">Prof. Dr. Gebhard Böckle</p>
      <p class="hero-description">Research Group at the Interdisciplinary Center for Scientific Computing (IWR), Heidelberg University</p>
    </div>
  </div>
</div>

<style>
.hero-header {
  position: relative;
  width: 100%;
  height: 500px;
  overflow: hidden;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.15);
  margin-bottom: 2rem;
}

.hero-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: 50% 0%;
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
  color: #ffffff !important;
  padding: 2rem;
}

/* Ensure all text in hero content is white */
.hero-content * {
  color: #ffffff !important;
}

.hero-title {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
  color: #ffffff !important;
}

/* Override any global heading styles for hero title */
.hero-header .hero-title,
.hero-overlay .hero-title,
.hero-content .hero-title {
  color: #ffffff !important;
}

.hero-subtitle {
  font-size: 1.5rem;
  font-weight: 400;
  margin-bottom: 0.75rem;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.8);
  color: #ffffff !important;
}

/* Override any global styles for hero subtitle */
.hero-header .hero-subtitle,
.hero-overlay .hero-subtitle,
.hero-content .hero-subtitle {
  color: #ffffff !important;
}

.hero-description {
  font-size: 1.1rem;
  font-weight: 300;
  margin: 0;
  opacity: 0.9;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.8);
  color: #ffffff !important;
}

/* Override any global styles for hero description */
.hero-header .hero-description,
.hero-overlay .hero-description,
.hero-content .hero-description,
.hero-description {
  color: #ffffff !important;
}

@media (max-width: 768px) {
  .hero-header {
    height: 360px;
  }

  .hero-title {
    font-size: 2rem;
  }

  .hero-subtitle {
    font-size: 1.2rem;
  }

  .hero-description {
    font-size: 1rem;
  }
}

/* Horizontal Card Layout Styles */
.main-container {
  width: 100%;
  margin: 0;
  padding: 0 0.75rem;
}

.content-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.feature-card {
  background: var(--bg-primary);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-base);
  overflow: hidden;
  position: relative;
}

.feature-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-4px);
  border-color: var(--primary);
}

.card-header {
  background: linear-gradient(135deg, var(--primary) 0%, var(--heidelberg-red) 100%);
  padding: 0.75rem;
  color: white;
  position: relative;
}

.card-icon {
  width: 45px;
  height: 45px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  margin-bottom: 0.5rem;
  backdrop-filter: blur(10px);
}

.card-header h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  line-height: 1.2;
}

.card-body {
  padding: 1rem;
}

.card-body p {
  color: var(--text-secondary);
  font-size: 0.9rem;
  line-height: 1.4;
  margin-bottom: 1rem;
}

.card-footer {
  padding: 0 1rem 1rem 1rem;
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.card-link {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.5rem 1rem;
  background: transparent;
  color: var(--primary);
  border: 2px solid var(--primary);
  border-radius: var(--radius-md);
  text-decoration: none;
  font-weight: 500;
  font-size: 0.8rem;
  transition: all var(--transition-base);
}

.card-link:hover {
  background: var(--primary);
  color: var(--primary-text);
  transform: translateY(-2px);
  box-shadow: var(--shadow-sm);
}



/* Responsive Design */
@media (max-width: 768px) {
  .content-grid {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }

  .card-footer {
    flex-direction: column;
  }

  .card-link {
    width: 100%;
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .main-container {
    padding: 0 0.5rem;
  }

  .card-header {
    padding: 0.5rem;
  }

  .card-body {
    padding: 0.75rem;
  }

  .card-footer {
    padding: 0 0.75rem 0.75rem 0.75rem;
  }
}
</style>



<div class="main-container">
  <!-- Main Feature Cards -->
  <div class="content-grid">
    <div class="feature-card">
      <div class="card-header">
        <div class="card-icon">
          <i class="fas fa-university" aria-hidden="true"></i>
        </div>
        <h3>About Our Research Group</h3>
      </div>
      <div class="card-body">
        <p>Website of the computational arithmetic geometry research group at IWR, Heidelberg University. Conducting cutting-edge research in algebraic number theory and arithmetic geometry.</p>
      </div>
      <div class="card-footer">
        <a href="{{ '/research/' | relative_url }}" class="card-link">
          <i class="fas fa-search" aria-hidden="true"></i>Research Areas
        </a>
        <a href="{{ '/members/' | relative_url }}" class="card-link">
          <i class="fas fa-users" aria-hidden="true"></i>Our Team
        </a>
      </div>
    </div>

    <div class="feature-card">
      <div class="card-header">
        <div class="card-icon">
          <i class="fas fa-microscope" aria-hidden="true"></i>
        </div>
        <h3>Research Focus</h3>
      </div>
      <div class="card-body">
        <p>Focus on Galois representations, modular forms, elliptic curves, deformation theory, and function field arithmetic including L-functions and Drinfeld modular forms.</p>
      </div>
      <div class="card-footer">
        <a href="{{ '/research/' | relative_url }}" class="card-link">
          <i class="fas fa-flask" aria-hidden="true"></i>Explore Research
        </a>
      </div>
    </div>

    <div class="feature-card">
      <div class="card-header">
        <div class="card-icon">
          <i class="fas fa-cogs" aria-hidden="true"></i>
        </div>
        <h3>Our Methods</h3>
      </div>
      <div class="card-body">
        <p>We apply theoretical methods and computer algebra experiments to solve problems in number theory and arithmetic geometry, developing computational tools and gathering examples.</p>
      </div>
      <div class="card-footer">
        <a href="{{ '/publications/' | relative_url }}" class="card-link">
          <i class="fas fa-file-alt" aria-hidden="true"></i>Publications
        </a>
      </div>
    </div>
  </div>



</div>
