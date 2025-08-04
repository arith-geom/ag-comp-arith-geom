---
layout: page
title: Team
permalink: /members/
nav: true
nav_order: 3
---

<div class="team-sections">
  {% assign sorted_members = site.members | sort: 'order' %}
  
  <!-- Head of Group -->
  {% assign group_leader = sorted_members | where: "role", "Professor & Group Leader" | first %}
  {% if group_leader %}
  <div class="team-section">
    <div class="section-header">
      <div class="section-icon">
        <i class="fas fa-crown" aria-hidden="true"></i>
      </div>
      <h3>Head of Research Group</h3>
    </div>
    <div class="member-card featured">
      <div class="member-avatar">
        {% if group_leader.photo %}
          <img src="{{ group_leader.photo }}" alt="{{ group_leader.name }}" class="member-photo">
        {% else %}
          <div class="member-photo-placeholder">
            <i class="fas fa-user"></i>
          </div>
        {% endif %}
      </div>
      <div class="member-info">
        <h4><a href="/members/{{ group_leader.name | slugify }}/">{{ group_leader.name }}</a></h4>
        <p class="member-role">{{ group_leader.role }}</p>
        {% if group_leader.research_interests %}
          <p class="member-description">{{ group_leader.research_interests }}</p>
        {% endif %}
        <div class="member-links">
          <a href="/members/{{ group_leader.name | slugify }}/" class="btn btn-outline-primary btn-sm">
            <i class="fas fa-user me-2" aria-hidden="true"></i>View Profile
          </a>
          {% if group_leader.email %}
            <a href="mailto:{{ group_leader.email }}" class="btn btn-outline-secondary btn-sm">
              <i class="fas fa-envelope me-2" aria-hidden="true"></i>Email
            </a>
          {% endif %}
        </div>
      </div>
    </div>
  </div>
  {% endif %}

  <!-- Administrative Support -->
  {% assign admin_members = sorted_members | where: "role", "Secretary" %}
  {% if admin_members.size > 0 %}
  <div class="team-section">
    <div class="section-header">
      <div class="section-icon">
        <i class="fas fa-user-cog" aria-hidden="true"></i>
      </div>
      <h3>Administrative Support</h3>
    </div>
    <div class="members-grid">
      {% for member in admin_members %}
        <div class="member-card">
          <div class="member-avatar">
            {% if member.photo %}
              <img src="{{ member.photo }}" alt="{{ member.name }}" class="member-photo">
            {% else %}
              <div class="member-photo-placeholder">
                <i class="fas fa-user"></i>
              </div>
            {% endif %}
          </div>
          <div class="member-info">
            <h4><a href="/members/{{ member.name | slugify }}/">{{ member.name }}</a></h4>
            <p class="member-role">{{ member.role }}</p>
            {% if member.research_interests %}
              <p class="member-description">{{ member.research_interests }}</p>
            {% endif %}
            <div class="member-links">
              <a href="/members/{{ member.name | slugify }}/" class="btn btn-outline-primary btn-sm">
                <i class="fas fa-user me-2" aria-hidden="true"></i>View Profile
              </a>
              {% if member.email %}
                <a href="mailto:{{ member.email }}" class="btn btn-outline-secondary btn-sm">
                  <i class="fas fa-envelope me-2" aria-hidden="true"></i>Email
                </a>
              {% endif %}
            </div>
          </div>
        </div>
      {% endfor %}
    </div>
  </div>
  {% endif %}

  <!-- Research Members -->
  {% assign research_members = sorted_members | where: "status", "active" | where_exp: "member", "member.role != 'Professor & Group Leader' and member.role != 'Secretary'" %}
  {% if research_members.size > 0 %}
  <div class="team-section">
    <div class="section-header">
      <div class="section-icon">
        <i class="fas fa-users" aria-hidden="true"></i>
      </div>
      <h3>Research Members</h3>
    </div>
    <div class="members-grid">
      {% for member in research_members %}
        <div class="member-card">
          <div class="member-avatar">
            {% if member.photo %}
              <img src="{{ member.photo }}" alt="{{ member.name }}" class="member-photo">
            {% else %}
              <div class="member-photo-placeholder">
                <i class="fas fa-user"></i>
              </div>
            {% endif %}
          </div>
          <div class="member-info">
            <h4><a href="/members/{{ member.name | slugify }}/">{{ member.name }}</a></h4>
            <p class="member-role">{{ member.role }}</p>
            {% if member.research_interests %}
              <p class="member-description">{{ member.research_interests }}</p>
            {% endif %}
            <div class="member-links">
              <a href="/members/{{ member.name | slugify }}/" class="btn btn-outline-primary btn-sm">
                <i class="fas fa-user me-2" aria-hidden="true"></i>View Profile
              </a>
              {% if member.email %}
                <a href="mailto:{{ member.email }}" class="btn btn-outline-secondary btn-sm">
                  <i class="fas fa-envelope me-2" aria-hidden="true"></i>Email
                </a>
              {% endif %}
            </div>
          </div>
        </div>
      {% endfor %}
    </div>
  </div>
  {% endif %}

  <!-- Former Members -->
  {% assign former_members = sorted_members | where: "status", "former" %}
  {% if former_members.size > 0 %}
  <div class="team-section">
    <div class="section-header">
      <div class="section-icon">
        <i class="fas fa-history" aria-hidden="true"></i>
      </div>
      <h3>Former Members</h3>
    </div>
    <div class="members-grid">
      {% for member in former_members %}
        <div class="member-card former">
          <div class="member-avatar">
            {% if member.photo %}
              <img src="{{ member.photo }}" alt="{{ member.name }}" class="member-photo">
            {% else %}
              <div class="member-photo-placeholder">
                <i class="fas fa-user"></i>
              </div>
            {% endif %}
          </div>
          <div class="member-info">
            <h4><a href="/members/{{ member.name | slugify }}/">{{ member.name }}</a></h4>
            <p class="member-role">{{ member.role }}</p>
            {% if member.research_interests %}
              <p class="member-description">{{ member.research_interests }}</p>
            {% endif %}
            <div class="member-links">
              <a href="/members/{{ member.name | slugify }}/" class="btn btn-outline-primary btn-sm">
                <i class="fas fa-user me-2" aria-hidden="true"></i>View Profile
              </a>
              {% if member.email %}
                <a href="mailto:{{ member.email }}" class="btn btn-outline-secondary btn-sm">
                  <i class="fas fa-envelope me-2" aria-hidden="true"></i>Email
                </a>
              {% endif %}
            </div>
          </div>
        </div>
      {% endfor %}
    </div>
  </div>
  {% endif %}
</div>

<style>
.team-sections {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 3rem;
}

.team-section {
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 2rem;
  box-shadow: var(--shadow-sm);
}

.section-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid var(--primary);
}

.section-icon {
  width: 50px;
  height: 50px;
  background: var(--primary);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
}

.section-header h3 {
  margin: 0;
  color: var(--text-primary);
  font-size: 1.5rem;
  font-weight: 600;
}

.members-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

.member-card {
  background: white;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: 1.5rem;
  transition: all var(--transition-base);
  display: flex;
  gap: 1rem;
}

.member-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-md);
  border-color: var(--primary);
}

.member-card.featured {
  border-color: var(--primary);
  box-shadow: var(--shadow-sm);
}

.member-card.former {
  opacity: 0.7;
}

.member-avatar {
  flex-shrink: 0;
}

.member-photo {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid var(--primary);
}

.member-photo-placeholder {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: var(--bg-secondary);
  border: 3px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
  font-size: 2rem;
}

.member-info {
  flex: 1;
}

.member-info h4 {
  margin: 0 0 0.5rem 0;
  color: var(--text-primary);
  font-size: 1.2rem;
  font-weight: 600;
}

.member-info h4 a {
  color: inherit;
  text-decoration: none;
  transition: color var(--transition-base);
}

.member-info h4 a:hover {
  color: var(--primary);
}

.member-role {
  color: var(--primary);
  font-weight: 600;
  margin: 0 0 0.75rem 0;
  font-size: 0.9rem;
}

.member-description {
  color: var(--text-secondary);
  font-size: 0.9rem;
  line-height: 1.5;
  margin: 0 0 1rem 0;
}

.member-links {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.member-links .btn {
  font-size: 0.8rem;
  padding: 0.25rem 0.5rem;
}

@media (max-width: 768px) {
  .members-grid {
    grid-template-columns: 1fr;
  }
  
  .member-card {
    flex-direction: column;
    text-align: center;
  }
  
  .member-avatar {
    align-self: center;
  }
  
  .member-links {
    justify-content: center;
  }
}
</style> 