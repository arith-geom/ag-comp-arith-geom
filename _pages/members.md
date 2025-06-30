---
layout: page
title: Team
permalink: /members/
nav: true
---

<div class="team-grid">
  {% for member in site.members %}
    <div class="team-member-card">
      {% if member.photo %}
        <img src="{{ member.photo | relative_url }}" alt="Photo of {{ member.name }}" class="team-member-photo">
      {% else %}
        <img src="/assets/img/team_placeholder.svg" alt="Placeholder photo for {{ member.name }}" class="team-member-photo">
      {% endif %}
      <div class="team-member-info">
        <h3 class="team-member-name">{{ member.name }}</h3>
        {% if member.role %}
          <p class="team-member-role">{{ member.role }}</p>
        {% endif %}
        {% if member.email %}
          <p class="team-member-email"><a href="mailto:{{ member.email }}">{{ member.email }}</a></p>
        {% endif %}
        {% if member.bio %}
          <div class="team-member-bio">
            {{ member.bio | markdownify }}
          </div>
        {% endif %}
      </div>
    </div>
  {% endfor %}
</div>

<style>
.team-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 2rem;
  padding-top: 2rem;
}
.team-member-card {
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 1.5rem;
  text-align: center;
  background-color: var(--card-bg-color);
  box-shadow: var(--shadow-sm);
  transition: all 0.3s ease;
}
.team-member-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-md);
}
.team-member-photo {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 1rem;
  border: 3px solid var(--border-color);
}
.team-member-name {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}
.team-member-role {
  font-style: italic;
  color: var(--text-color-secondary);
  margin-bottom: 1rem;
}
.team-member-bio {
  text-align: left;
  font-size: 0.95rem;
  color: var(--text-color-secondary);
}
</style> 