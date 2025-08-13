---
layout: page
permalink: "/members/"
nav: true
nav_order: 3
show_title: false
order: 100
title: Members
---
<!-- Simple Navigation -->
<div class="members-nav-simple">
  <div class="container-fluid px-3 px-md-4">
    <button id="btn-current" class="nav-btn active" onclick="showSection('current')">Current Members</button>
    <button id="btn-alumni" class="nav-btn" onclick="showSection('alumni')">Former Members</button>
  </div>
</div>

<div class="team-sections">
  {% assign sorted_members = site.members | sort: 'role' | sort: 'order' %}
  
  <!-- Current Members Section -->
  <div id="current-section" class="members-content-section active">
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
          {% assign group_leader_slug = group_leader.name | slugify %}
          <h4><a href="{{ '/members/' | append: group_leader_slug | append: '/' | relative_url }}">{{ group_leader.name }}</a></h4>
          <p class="member-role">{{ group_leader.role }}</p>
          {% if group_leader.research_interests %}
            <p class="member-description">{{ group_leader.research_interests }}</p>
          {% endif %}
          <div class="member-links">
            <a href="{{ '/members/' | append: group_leader_slug | append: '/' | relative_url }}" class="btn btn-outline-primary btn-sm">
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
              {% assign member_slug = member.name | slugify %}
              <h4><a href="{{ '/members/' | append: member_slug | append: '/' | relative_url }}">{{ member.name }}</a></h4>
              <p class="member-role">{{ member.role }}</p>
              {% if member.research_interests %}
                <p class="member-description">{{ member.research_interests }}</p>
              {% endif %}
              <div class="member-links">
                <a href="{{ '/members/' | append: member_slug | append: '/' | relative_url }}" class="btn btn-outline-primary btn-sm">
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
              {% assign member_slug = member.name | slugify %}
              <h4><a href="{{ '/members/' | append: member_slug | append: '/' | relative_url }}">{{ member.name }}</a></h4>
              <p class="member-role">{{ member.role }}</p>
              {% if member.research_interests %}
                <p class="member-description">{{ member.research_interests }}</p>
              {% endif %}
              <div class="member-links">
                <a href="{{ '/members/' | append: member_slug | append: '/' | relative_url }}" class="btn btn-outline-primary btn-sm">
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

  <!-- Alumni Section -->
  <div id="alumni-section" class="members-content-section">
    {% assign alumni_members = sorted_members | where: "status", "alumni" %}
    {% if alumni_members.size > 0 %}
    <div class="team-section">
      <div class="section-header">
        <div class="section-icon">
          <i class="fas fa-history" aria-hidden="true"></i>
        </div>
        <h3>Former Members (Alumni)</h3>
      </div>
      <div class="members-grid">
        {% for member in alumni_members %}
          <div class="member-card former">
            <div class="member-info">
              <h4>{{ member.name }}</h4>
              <p class="member-role">{{ member.role }}</p>
              {% if member.graduation_year %}
                <p class="member-graduation">Graduated: {{ member.graduation_year }}</p>
              {% endif %}
              {% if member.current_position %}
                <p class="member-current">{{ member.current_position }}</p>
              {% endif %}
              {% if member.research_interests %}
                <p class="member-description">{{ member.research_interests }}</p>
              {% endif %}
            </div>
          </div>
        {% endfor %}
      </div>
    </div>
    {% endif %}
  </div>
</div>

<style>
/* Simple Navigation - Heidelberg Theme */
.members-nav-simple {
  background: var(--bg-primary);
  border-bottom: 2px solid var(--border-color);
  padding: 1.5rem 0;
  margin-bottom: 2rem;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
  text-align: center;
}

.nav-btn {
  background: var(--bg-primary);
  border: 2px solid var(--primary);
  color: var(--primary);
  padding: 0.75rem 2rem;
  margin: 0 0.5rem;
  border-radius: var(--radius-md);
  font-weight: 600;
  cursor: pointer;
  transition: var(--transition-base);
  font-family: inherit;
}

.nav-btn:hover {
  background: var(--primary);
  color: var(--primary-text);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.nav-btn.active {
  background: var(--primary);
  color: var(--primary-text);
  box-shadow: var(--shadow-sm);
}

/* Content Sections */
.members-content-section {
  display: none;
}

.members-content-section.active {
  display: block;
}

/* Team Sections - Heidelberg Theme */
.team-sections {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 3rem;
}

.team-section {
  background: var(--bg-primary);
  border: 2px solid var(--border-color);
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
  border-bottom: 3px solid var(--primary);
}

.section-icon {
  width: 50px;
  height: 50px;
  background: var(--primary);
  color: var(--primary-text);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  box-shadow: var(--shadow-sm);
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
  background: var(--bg-primary);
  border: 2px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: 1.5rem;
  transition: var(--transition-base);
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
  opacity: 0.8;
  background: var(--bg-secondary);
  flex-direction: column;
  text-align: center;
}

.member-card.former:hover {
  opacity: 1;
  background: var(--bg-primary);
}

.member-card.former .member-info {
  width: 100%;
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
  box-shadow: var(--shadow-sm);
}

.member-photo-placeholder {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: var(--primary);
  border: 3px solid var(--primary);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary-text);
  font-size: 2rem;
  box-shadow: var(--shadow-sm);
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
  transition: var(--transition-base);
}

.member-info h4 a:hover {
  color: var(--primary);
}

.member-role {
  color: var(--primary);
  font-weight: 600;
  margin: 0 0 0.75rem 0;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.member-graduation {
  font-size: 0.9rem;
  color: var(--text-secondary);
  margin: 0 0 0.5rem 0;
  font-style: italic;
}

.member-current {
  font-size: 0.9rem;
  color: var(--text-secondary);
  margin: 0 0 0.75rem 0;
  font-weight: 500;
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
  border-radius: var(--radius-sm);
  transition: var(--transition-base);
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
}

.btn-outline-primary {
  background: transparent;
  color: var(--primary);
  border: 1px solid var(--primary);
}

.btn-outline-primary:hover {
  background: var(--primary);
  color: var(--primary-text);
  transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
}

.btn-outline-secondary {
  background: transparent;
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
}

.btn-outline-secondary:hover {
  background: var(--bg-secondary);
  color: var(--text-primary);
  border-color: var(--border-dark);
  transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
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
  
  .section-header {
    flex-direction: column;
    text-align: center;
  }
}
</style>

<script>
function showSection(sectionName) {
  // Hide all sections
  document.querySelectorAll('.members-content-section').forEach(section => {
    section.classList.remove('active');
  });
  
  // Remove active class from all buttons
  document.querySelectorAll('.nav-btn').forEach(btn => {
    btn.classList.remove('active');
  });
  
  // Show selected section
  document.getElementById(sectionName + '-section').classList.add('active');
  
  // Update button active states without relying on global event
  const btnCurrent = document.getElementById('btn-current');
  const btnAlumni = document.getElementById('btn-alumni');
  if (btnCurrent && btnAlumni) {
    btnCurrent.classList.toggle('active', sectionName === 'current');
    btnAlumni.classList.toggle('active', sectionName === 'alumni');
  }
}
</script> 