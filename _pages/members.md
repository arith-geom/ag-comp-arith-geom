---
layout: page
permalink: "/members/"
nav: true
nav_order: 3
show_title: false
title: Group Members
description: "Meet the team of the Computational Arithmetic Geometry research group at Heidelberg University, including professors, researchers, and students."
excerpt_separator: ""
---

<div class="members-page">
  {% for section in site.data.members.sections %}
    {% assign section_slug = section.title | slugify %}
    {% assign layout_class = section.layout | default: "medium" | prepend: "section-layout-" %}
    <div class="member-section member-section-{{ section_slug }} {{ layout_class }}">
      <h2 class="section-title">{{ section.title | escape }}</h2>
      <div class="content-grid {{ section_slug }}-grid">


        {% for member in section.members %}

          <div class="feature-card member-card" style="position: relative;">
            <div class="card-header {% if member.description %}bordered{% endif %}">
              {% if section.title != "Former Members" %}
              <div class="member-photo-container">
                {% if member.photo %}
                  <img src="{{ member.photo | relative_url }}" alt="Photo of {{ member.name | escape }}" class="member-photo">
                {% else %}
                  <div class="member-photo-placeholder"><i class="fas fa-user"></i></div>
                {% endif %}
              </div>
              {% endif %}
              <div class="member-header-info">
                <h3 class="member-name {% if member.name.size > 25 %}long-name{% endif %}">
                  {% assign member_slug = member.name | slugify %}
                  <a href="{{ '/members/' | append: member_slug | append: '/' | relative_url }}" class="text-reset text-decoration-none stretched-link">{{ member.name | escape }}</a>
                </h3>
                <p class="member-role">{{ member.role | escape }}</p>
              </div>
            </div>
            {% if member.description %}
            <div class="card-body">
              <div class="member-description">{{ member.description | strip_html | markdownify }}</div>
            </div>
            {% endif %}


          </div>
        {% endfor %}
      </div>
    </div>
  {% endfor %}
</div>

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {% for section in site.data.members.sections %}
      {% if section.title != "Former Members" %}
        {% for member in section.members %}
          {
            "@type": "Person",
            "name": {{ member.name | jsonify }},
            "jobTitle": {{ member.role | jsonify }},
            "worksFor": {
              "@type": "EducationalOrganization",
              "name": {{ site.title | jsonify }}
            },
            {% assign member_slug = member.name | slugify %}
            "url": {{ '/members/' | append: member_slug | append: '/' | absolute_url | jsonify }}
            {% if member.links %}
              ,"sameAs": [
                {% for link in member.links %}
                  {% if link.url contains "mailto:" %}{% continue %}{% endif %}
                  {{ link.url | jsonify }}{% unless forloop.last %},{% endunless %}
                {% endfor %}
              ]
            {% endif %}
          }{% unless forloop.last and section.title == "Research Members" %},{% endunless %}
        {% endfor %}
      {% endif %}
    {% endfor %}
  ]
}
</script>

<script>
document.addEventListener('DOMContentLoaded', function() {
  function equalizeCardHeights() {
    const sections = document.querySelectorAll('.member-section');

    sections.forEach(section => {
      const cards = section.querySelectorAll('.member-card');
      if (cards.length === 0) return;

      // Reset heights to auto to get natural height
      cards.forEach(card => card.style.height = 'auto');

      // Find max height
      let maxHeight = 0;
      cards.forEach(card => {
        const height = card.offsetHeight;
        if (height > maxHeight) {
          maxHeight = height;
        }
      });

      // Apply max height to all cards in this section
      cards.forEach(card => card.style.height = maxHeight + 'px');
    });
  }

  // Run on load
  equalizeCardHeights();

  // Run on resize with debounce
  let timeout;
  window.addEventListener('resize', function() {
    clearTimeout(timeout);
    timeout = setTimeout(equalizeCardHeights, 100);
  });
});
</script>
