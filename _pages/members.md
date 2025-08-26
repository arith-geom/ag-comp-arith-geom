---
layout: page
permalink: "/members/"
nav: true
nav_order: 3
show_title: false
order: 100
title: Members
---

<div class="members-page">
  <!-- Simple Navigation -->
  <div class="members-nav-simple">
    <div class="nav-buttons-container">
      <button id="btn-current" class="nav-btn active" onclick="showSection('current')">Current Members</button>
      <button id="btn-alumni" class="nav-btn" onclick="showSection('alumni')">Former Members</button>
    </div>
  </div>

  <!-- Current Members Section -->
  <div id="current-section" class="members-content-section active">
    {% assign sorted_members = site.members | sort: 'role' | sort: 'order' %}

    <!-- Head of Group -->
    {% assign group_leader = sorted_members | where: "role", "Professor & Group Leader" | first %}
    {% if group_leader %}
    <div class="member-section">
      <h2>Head of Research Group</h2>
      <div class="member-card-simple featured" data-member-id="{{ group_leader.name | slugify }}">
        <div class="member-header" onclick="toggleMemberCard(this)">
          {% if group_leader.photo %}
            <img src="{{ group_leader.photo }}" alt="{{ group_leader.name }}" class="member-photo">
          {% else %}
            <div class="member-photo-placeholder">
              <i class="fas fa-user"></i>
            </div>
          {% endif %}
          <div class="member-info">
            <h3>{{ group_leader.name }}</h3>
            <p class="member-role">{{ group_leader.role }}</p>
          </div>
          <div class="member-expand-icon">
            <i class="fas fa-chevron-down"></i>
          </div>
        </div>

        <div class="member-expanded-content">
          <div class="member-expanded-header">
            <button type="button" class="btn btn-outline-primary btn-sm member-close-btn" onclick="toggleMemberCard(this.closest('.member-card-simple').querySelector('.member-header'))">
              <i class="fas fa-times"></i> Close & Show All
            </button>
          </div>

          {% if group_leader.research_interests %}
          <div class="member-research-interests">
            <h4>Research Interests</h4>
            <div>{{ group_leader.research_interests | markdownify }}</div>
          </div>
          {% endif %}

          {% if group_leader.content %}
          <div class="member-about">
            <h4>About</h4>
            <div>{{ group_leader.content | markdownify }}</div>
          </div>
          {% endif %}

          {% if group_leader.email %}
          <div class="member-contact">
            <a href="mailto:{{ group_leader.email }}" class="btn btn-outline-primary">
              <i class="fas fa-envelope"></i> Email
            </a>
          </div>
          {% endif %}
        </div>
      </div>
    </div>
    {% endif %}

    <!-- Research Members -->
    {% assign research_members = sorted_members | where: "status", "active" | where_exp: "member", "member.role != 'Professor & Group Leader'" %}
    {% if research_members.size > 0 %}
    <div class="member-section">
      <h2>Research Members</h2>
      <div class="members-grid-simple">
        {% for member in research_members %}
        <div class="member-card-simple" data-member-id="{{ member.name | slugify }}">
          <div class="member-header" onclick="toggleMemberCard(this)">
            {% if member.photo %}
              <img src="{{ member.photo }}" alt="{{ member.name }}" class="member-photo">
            {% else %}
              <div class="member-photo-placeholder">
                <i class="fas fa-user"></i>
              </div>
            {% endif %}
            <div class="member-info">
              <h3>{{ member.name }}</h3>
              <p class="member-role">{{ member.role }}</p>
            </div>
            <div class="member-expand-icon">
              <i class="fas fa-chevron-down"></i>
            </div>
          </div>

          <div class="member-expanded-content">
            <div class="member-expanded-header">
              <button type="button" class="btn btn-outline-primary btn-sm member-close-btn" onclick="toggleMemberCard(this.closest('.member-card-simple').querySelector('.member-header'))">
                <i class="fas fa-times"></i> Close & Show All
              </button>
            </div>

            {% if member.research_interests %}
            <div class="member-research-interests">
              <h4>Research Interests</h4>
              <div>{{ member.research_interests | markdownify }}</div>
            </div>
            {% endif %}

            {% if member.content %}
            <div class="member-about">
              <h4>About</h4>
              <div>{{ member.content | markdownify }}</div>
            </div>
            {% endif %}

            {% if member.email %}
            <div class="member-contact">
              <a href="mailto:{{ member.email }}" class="btn btn-outline-primary btn-sm">
                <i class="fas fa-envelope"></i> Email
              </a>
            </div>
            {% endif %}
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
    <div class="member-section">
      <h2>Former Members</h2>
      <div class="members-grid-simple">
        {% for member in alumni_members %}
        <div class="member-card-simple former">
          <div class="member-header">
            {% if member.photo %}
              <img src="{{ member.photo }}" alt="{{ member.name }}" class="member-photo">
            {% else %}
              <div class="member-photo-placeholder">
                <i class="fas fa-user"></i>
              </div>
            {% endif %}
            <div class="member-info">
              <h3>{{ member.name }}</h3>
              <p class="member-role">{{ member.role }}</p>
              {% if member.graduation %}
                <p class="member-graduation">{{ member.graduation }}</p>
              {% endif %}
            </div>
          </div>

          <div class="member-contact">
            {% if member.email %}
              <a href="mailto:{{ member.email }}" class="btn btn-outline-primary btn-sm">
                <i class="fas fa-envelope"></i> Email
              </a>
            {% endif %}
          </div>
        </div>
        {% endfor %}
      </div>
    </div>
    {% endif %}
  </div>
</div>

<script>
// Simple section switching
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

  // Update button active states
  const btnCurrent = document.getElementById('btn-current');
  const btnAlumni = document.getElementById('btn-alumni');
  if (btnCurrent && btnAlumni) {
    btnCurrent.classList.toggle('active', sectionName === 'current');
    btnAlumni.classList.toggle('active', sectionName === 'alumni');
  }
}

// Simple card expand/collapse functionality - only one expanded at a time, hides all others
function toggleMemberCard(headerElement) {
  const card = headerElement.closest('.member-card-simple');
  const expandedContent = card.querySelector('.member-expanded-content');
  const expandIcon = card.querySelector('.member-expand-icon i');

  // If this card is already expanded, collapse it
  if (expandedContent.style.display === 'block') {
    expandedContent.style.display = 'none';
    expandIcon.classList.remove('fa-chevron-up');
    expandIcon.classList.add('fa-chevron-down');
    card.classList.remove('expanded');
    return;
  }

  // Collapse all other expanded cards first
  document.querySelectorAll('.member-card-simple.expanded').forEach(expandedCard => {
    if (expandedCard !== card) {
      const otherContent = expandedCard.querySelector('.member-expanded-content');
      const otherIcon = expandedCard.querySelector('.member-expand-icon i');

      if (otherContent) {
        otherContent.style.display = 'none';
      }
      if (otherIcon) {
        otherIcon.classList.remove('fa-chevron-up');
        otherIcon.classList.add('fa-chevron-down');
      }
      expandedCard.classList.remove('expanded');
    }
  });

  // Expand the clicked card
  expandedContent.style.display = 'block';
  expandIcon.classList.remove('fa-chevron-down');
  expandIcon.classList.add('fa-chevron-up');
  card.classList.add('expanded');
}

// Apply initial section from URL (?section=alumni|current)
document.addEventListener('DOMContentLoaded', function() {
  try {
    const params = new URLSearchParams(window.location.search);
    const section = (params.get('section') || '').toLowerCase();
    if (section === 'alumni' || section === 'former') {
      showSection('alumni');
    } else if (section === 'current') {
      showSection('current');
    }
  } catch (_) {}
});
</script>

<style>
/* Simple, clean styles - much less code than the complex version */

.members-nav-simple {
  padding: 2rem 0;
  margin-bottom: 2rem;
  text-align: center;
}

.nav-buttons-container {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.nav-btn {
  background: transparent;
  border: 2px solid var(--primary);
  color: var(--primary);
  padding: 0.75rem 2rem;
  border-radius: 20px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.nav-btn:hover {
  background: var(--primary);
  color: var(--primary-text);
}

.nav-btn.active {
  background: var(--primary);
  color: var(--primary-text);
}

.members-content-section {
  display: none;
}

.members-content-section.active {
  display: block;
}

.member-section {
  margin-bottom: 3rem;
}

.member-section h2 {
  color: var(--text-primary);
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid var(--primary);
}

.members-grid-simple {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.member-card-simple {
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 1.5rem;
  transition: transform 0.3s ease;
}

.member-card-simple:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.member-card-simple.featured {
  border-color: var(--primary);
  background: linear-gradient(145deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
}

.member-card-simple.former {
  opacity: 0.9;
}

.member-header {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
  margin-bottom: 1rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 8px;
  transition: background-color 0.3s ease;
}

.member-header:hover {
  background-color: var(--bg-secondary);
}

.member-photo {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid var(--primary);
}

.member-photo-placeholder {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: var(--primary);
  color: var(--primary-text);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.member-info h3 {
  margin: 0 0 0.5rem 0;
  color: var(--text-primary);
  font-size: 1.2rem;
}

.member-expand-icon {
  margin-left: auto;
  display: flex;
  align-items: center;
  color: var(--primary);
  transition: transform 0.3s ease;
}

.member-expand-icon i {
  font-size: 1.2rem;
}

.member-role {
  margin: 0;
  color: var(--primary);
  font-weight: 600;
  font-size: 0.9rem;
}

.member-graduation {
  margin: 0.5rem 0 0 0;
  color: var(--text-secondary);
  font-size: 0.8rem;
  font-style: italic;
}

.member-research-interests {
  margin-bottom: 1rem;
}

.member-research-interests h4 {
  margin: 0 0 0.5rem 0;
  color: var(--text-primary);
  font-size: 1rem;
}

.member-about {
  margin-bottom: 1rem;
}

.member-about h4 {
  margin: 0 0 0.5rem 0;
  color: var(--text-primary);
  font-size: 1rem;
}

.member-contact {
  margin-top: 1rem;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-outline-primary {
  background: transparent;
  color: var(--primary);
  border: 2px solid var(--primary);
}

.btn-outline-primary:hover {
  background: var(--primary);
  color: var(--primary-text);
}

.btn-sm {
  padding: 0.4rem 0.8rem;
  font-size: 0.9rem;
}

/* Expand/Collapse functionality */
.member-expanded-content {
  display: none;
  padding: 1rem;
  border-top: 1px solid var(--border-color);
  margin-top: 1rem;
  animation: fadeIn 0.3s ease;
}

.member-card-simple.expanded {
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
  border-color: var(--primary);
}

/* Hide collapsed cards and headers when any card is expanded */
.members-content-section:has(.member-card-simple.expanded) .member-card-simple:not(.expanded) {
  display: none;
}

.members-content-section:has(.member-card-simple.expanded) .member-section h2 {
  display: none;
}

/* Hide navigation buttons when any card is expanded */
div:has(.member-card-simple.expanded) .members-nav-simple {
  display: none;
}

.member-expanded-header {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--border-color);
}

.member-close-btn {
  background: var(--bg-primary) !important;
  border-color: var(--primary) !important;
  color: var(--primary) !important;
  transition: all 0.3s ease;
}

.member-close-btn:hover {
  background: var(--primary) !important;
  color: var(--primary-text) !important;
  transform: scale(1.05);
}

.member-expanded-content h4 {
  margin: 0 0 0.5rem 0;
  color: var(--text-primary);
  font-size: 1rem;
  font-weight: 600;
}

.member-research-interests,
.member-about {
  margin-bottom: 1rem;
}

.member-research-interests div,
.member-about div {
  color: var(--text-secondary);
  line-height: 1.6;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Mobile responsive */
@media (max-width: 768px) {
  .members-grid-simple {
    grid-template-columns: 1fr;
  }

  .nav-buttons-container {
    flex-direction: column;
    align-items: center;
  }

  .member-header {
    flex-direction: column;
    text-align: center;
  }
}
</style>
