---
layout: page
title: Research
permalink: /research/
nav: true
nav_order: 2
---

<div class="research-areas">
  {% assign sorted_research = site.research | sort: 'order' %}
  {% for research_area in sorted_research %}
    <div class="research-area-card">
      <div class="research-icon">
        <i class="fas fa-microscope" aria-hidden="true"></i>
      </div>
      <div class="research-content">
        <h3>{{ research_area.title }}</h3>
        <div class="research-text">
          {{ research_area.content }}
        </div>
        {% if research_area.keywords %}
          <div class="research-keywords">
            <strong>Keywords:</strong> 
            {% for keyword in research_area.keywords %}
              <span class="keyword-tag">{{ keyword }}</span>
            {% endfor %}
          </div>
        {% endif %}
        {% if research_area.related_publications %}
          <div class="related-publications">
            <strong>Related Publications:</strong>
            <ul>
              {% for pub_id in research_area.related_publications %}
                {% assign pub = site.publications | where: "id", pub_id | first %}
                {% if pub %}
                  <li><a href="{{ pub.url | default: pub.pdf | default: '#' }}">{{ pub.title }}</a></li>
                {% endif %}
              {% endfor %}
            </ul>
          </div>
        {% endif %}
      </div>
    </div>
  {% endfor %}
</div>

<style>
/* Clean and modern research page styling */
.research-areas {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 3rem;
}

.research-area-card {
  display: flex;
  gap: 2rem;
  padding: 2.5rem;
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-base);
}

.research-area-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-md);
  border-color: var(--primary);
}

.research-icon {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, var(--primary) 0%, var(--heidelberg-red) 100%);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  flex-shrink: 0;
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-base);
}

.research-area-card:hover .research-icon {
  transform: scale(1.1);
  box-shadow: var(--shadow-md);
}

.research-area-card .research-content h3 {
  color: var(--text-primary);
  font-size: 1.8rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid var(--primary);
  display: inline-block;
}

.research-text {
  color: var(--text-secondary);
  line-height: 1.7;
  font-size: 1.1rem;
}

.research-text p {
  margin-bottom: 1rem;
}

.research-text h2, .research-text h3, .research-text h4 {
  color: var(--text-primary);
  margin-top: 1.5rem;
  margin-bottom: 0.75rem;
}

.research-keywords {
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border-color);
}

.keyword-tag {
  display: inline-block;
  background: var(--primary);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
  margin: 0.25rem;
}

.related-publications {
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border-color);
}

.related-publications ul {
  list-style: none;
  padding: 0;
  margin: 0.5rem 0 0 0;
}

.related-publications li {
  margin-bottom: 0.5rem;
}

.related-publications a {
  color: var(--primary);
  text-decoration: none;
  transition: color var(--transition-base);
}

.related-publications a:hover {
  color: var(--heidelberg-red);
  text-decoration: underline;
}

/* Responsive design */
@media (max-width: 768px) {
  .research-area-card {
    flex-direction: column;
    text-align: center;
  }
  
  .research-icon {
    align-self: center;
  }
  
  .research-area-card .research-content h3 {
    text-align: center;
    display: block;
  }
}

@media (max-width: 480px) {
  .research-areas {
    gap: 2rem;
  }
  
  .research-area-card {
    padding: 1.5rem;
  }
  
  .research-area-card .research-content h3 {
    font-size: 1.5rem;
  }
  
  .research-text {
    font-size: 1rem;
  }
}
</style> 