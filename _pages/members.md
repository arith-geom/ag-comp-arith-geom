---
layout: page
title: Team
permalink: /members/
nav: true
nav_order: 3
---

<div class="team-intro mb-4">
  <p class="lead translatable-content" data-translation-key="members.intro">Our research group consists of faculty, postdoctoral researchers, and students working on computational arithmetic geometry.</p>
</div>

<div class="team-grid">
  {% assign sorted_members = site.members | sort: "order" %}
  {% for member in sorted_members %}
    <div class="team-member-card">
      <div class="team-member-photo-container">
        {% if member.photo %}
          <img src="{{ member.photo | relative_url }}" alt="Photo of {{ member.name }}" class="team-member-photo" loading="lazy">
        {% else %}
          <img src="{{ '/assets/img/team_placeholder.svg' | relative_url }}" alt="Placeholder photo for {{ member.name }}" class="team-member-photo" loading="lazy">
        {% endif %}
      </div>
      <div class="team-member-info">
        <h3 class="team-member-name">{{ member.name }}</h3>
        {% if member.role %}
          <p class="team-member-role">{{ member.role }}</p>
        {% endif %}
        {% if member.email %}
          <p class="team-member-email">
            <a href="mailto:{{ member.email }}" aria-label="Email {{ member.name }}">
              <i class="fas fa-envelope me-2" aria-hidden="true"></i>{{ member.email }}
            </a>
          </p>
        {% endif %}
        <div class="team-member-links">
          {% if member.website %}
            <a href="{{ member.website }}" target="_blank" rel="noopener noreferrer" class="team-member-link" aria-label="Personal Website of {{ member.name }}">
              <i class="fas fa-globe" aria-hidden="true"></i>
            </a>
          {% endif %}
          {% if member.github %}
            <a href="https://github.com/{{ member.github }}" target="_blank" rel="noopener noreferrer" class="team-member-link" aria-label="GitHub Profile of {{ member.name }}">
              <i class="fab fa-github" aria-hidden="true"></i>
            </a>
          {% endif %}
          {% if member.orcid %}
            <a href="https://orcid.org/{{ member.orcid }}" target="_blank" rel="noopener noreferrer" class="team-member-link" aria-label="ORCID Profile of {{ member.name }}">
              <i class="ai ai-orcid" aria-hidden="true"></i>
            </a>
          {% endif %}
        </div>
        {% if member.bio %}
          <div class="team-member-bio">
            {{ member.bio | markdownify }}
          </div>
        {% endif %}
        {% if member.research_interests %}
          <div class="team-member-research">
            <h4 class="team-member-research-title">Research Interests</h4>
            <p class="team-member-research-text">{{ member.research_interests }}</p>
          </div>
        {% endif %}
      </div>
    </div>
  {% endfor %}
</div>

<style>
.team-intro {
  text-align: center;
  max-width: 800px;
  margin: 0 auto 2rem;
}

.team-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 2rem;
  padding-top: 1rem;
}

.team-member-card {
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  text-align: center;
  background-color: var(--bg-primary);
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-base);
  height: 100%;
  display: flex;
  flex-direction: column;
}

.team-member-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-md);
  border-color: var(--primary);
}

.team-member-photo-container {
  margin-bottom: 1.5rem;
}

.team-member-photo {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid var(--border-color);
  transition: all var(--transition-base);
}

.team-member-card:hover .team-member-photo {
  border-color: var(--primary);
  transform: scale(1.05);
}

.team-member-name {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: var(--text-primary);
}

.team-member-role {
  font-style: italic;
  color: var(--text-secondary);
  margin-bottom: 1rem;
  font-weight: 500;
}

.team-member-email {
  margin-bottom: 1rem;
}

.team-member-email a {
  color: var(--link-color);
  text-decoration: none;
  font-size: 0.9rem;
}

.team-member-email a:hover {
  color: var(--link-hover);
  text-decoration: underline;
}

.team-member-links {
  margin-bottom: 1.5rem;
  display: flex;
  justify-content: center;
  gap: 1rem;
}

.team-member-link {
  font-size: 1.25rem;
  color: var(--text-secondary);
  transition: all var(--transition-fast);
  padding: 0.5rem;
  border-radius: var(--radius-md);
  min-width: 44px;
  min-height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.team-member-link:hover {
  color: var(--primary);
  background-color: var(--bg-secondary);
  transform: translateY(-2px);
}

.team-member-bio {
  text-align: left;
  font-size: 0.95rem;
  color: var(--text-secondary);
  margin-bottom: 1rem;
  flex-grow: 1;
}

.team-member-research {
  text-align: left;
  margin-top: auto;
}

.team-member-research-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}

.team-member-research-text {
  font-size: 0.9rem;
  color: var(--text-secondary);
  line-height: 1.5;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .team-grid {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1.5rem;
  }
  
  .team-member-card {
    padding: 1rem;
  }
  
  .team-member-photo {
    width: 120px;
    height: 120px;
  }
  
  .team-member-name {
    font-size: 1.25rem;
  }
}

@media (max-width: 480px) {
  .team-grid {
    grid-template-columns: 1fr;
  }
  
  .team-member-photo {
    width: 100px;
    height: 100px;
  }
}
</style> 