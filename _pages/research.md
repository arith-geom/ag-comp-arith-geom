---
layout: page
title: Research
permalink: /research/
nav: true
nav_order: 2
---

<div class="research-intro">
  <p class="lead translatable-content" data-translation-key="research.intro_lead">Our research focuses on <strong>arithmetic geometry</strong> and <strong>number theory</strong>, with particular emphasis on computational methods and their applications.</p>
  <p class="translatable-content" data-translation-key="research.intro_description">We investigate Galois representations, modular forms, elliptic curves, and their connections to modern number theory. Our work combines theoretical insights with computational experiments to advance understanding in these areas.</p>
</div>

<div class="research-areas mt-5">
  <h2 class="research-section-title translatable-content" data-translation-key="research.areas_title">Research Areas</h2>
  <div class="research-grid">
    {% for item in site.research %}
      <div class="research-card">
        <div class="research-card-header">
          <h3 class="research-card-title">{{ item.title }}</h3>
          {% if item.keywords %}
            <div class="research-card-keywords">
              {% for keyword in item.keywords %}
                <span class="keyword-tag">{{ keyword }}</span>
              {% endfor %}
            </div>
          {% endif %}
        </div>
        <div class="research-card-body">
          {% if item.description %}
            <p class="research-card-description">{{ item.description | markdownify | strip_html | truncatewords: 30 }}</p>
          {% endif %}
          <div class="research-card-content">
            {{ item.content | markdownify | truncatewords: 50 }}
          </div>
        </div>
                 <div class="research-card-footer">
           <a href="{{ item.url | relative_url }}" class="btn btn-outline-primary">
             <i class="fas fa-arrow-right me-2" aria-hidden="true"></i><span class="translatable-content" data-translation-key="research.learn_more">Learn More</span>
           </a>
           {% if item.papers %}
             <span class="research-paper-count">
               <i class="fas fa-file-alt me-1" aria-hidden="true"></i>{{ item.papers | size }} <span class="translatable-content" data-translation-key="research.papers_count">papers</span>
             </span>
           {% endif %}
         </div>
      </div>
    {% endfor %}
  </div>
</div>

<div class="research-methods mt-5">
  <h2 class="research-section-title translatable-content" data-translation-key="research.methodology_title">Methodology</h2>
  <div class="methods-grid">
    <div class="method-card">
      <div class="method-icon">
        <i class="fas fa-calculator" aria-hidden="true"></i>
      </div>
      <h3 class="translatable-content" data-translation-key="research.method_computational.title">Computational Methods</h3>
      <p class="translatable-content" data-translation-key="research.method_computational.description">We develop and use advanced computational techniques to explore arithmetic objects and verify theoretical predictions.</p>
    </div>
    <div class="method-card">
      <div class="method-icon">
        <i class="fas fa-brain" aria-hidden="true"></i>
      </div>
      <h3 class="translatable-content" data-translation-key="research.method_theoretical.title">Theoretical Analysis</h3>
      <p class="translatable-content" data-translation-key="research.method_theoretical.description">Deep theoretical understanding guides our computational experiments and helps interpret their results.</p>
    </div>
    <div class="method-card">
      <div class="method-icon">
        <i class="fas fa-flask" aria-hidden="true"></i>
      </div>
      <h3 class="translatable-content" data-translation-key="research.method_experimental.title">Experimental Mathematics</h3>
      <p class="translatable-content" data-translation-key="research.method_experimental.description">We use computational experiments to discover patterns and formulate new conjectures in arithmetic geometry.</p>
    </div>
  </div>
</div>

<div class="research-collaborations mt-5">
  <h2 class="research-section-title translatable-content" data-translation-key="research.collaborations_title">Collaborations</h2>
  <p class="translatable-content" data-translation-key="research.collaborations_description">We collaborate with researchers worldwide on various aspects of arithmetic geometry and computational number theory. Our group maintains active connections with:</p>
  <ul class="collaboration-list">
    <li class="translatable-content" data-translation-key="research.collaboration_1">International research institutions</li>
    <li class="translatable-content" data-translation-key="research.collaboration_2">Mathematical software development teams</li>
    <li class="translatable-content" data-translation-key="research.collaboration_3">Number theory conferences and workshops</li>
    <li class="translatable-content" data-translation-key="research.collaboration_4">Graduate and undergraduate research programs</li>
  </ul>
</div>

<style>
.research-intro {
  text-align: center;
  max-width: 900px;
  margin: 0 auto 3rem;
}

.research-intro .lead {
  font-size: 1.25rem;
  color: var(--text-primary);
  margin-bottom: 1.5rem;
}

.research-section-title {
  font-size: 2.5rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 2rem;
  text-align: center;
  position: relative;
}

.research-section-title::after {
  content: '';
  position: absolute;
  bottom: -0.5rem;
  left: 50%;
  transform: translateX(-50%);
  width: 60px;
  height: 3px;
  background: var(--primary);
  border-radius: 2px;
}

.research-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.research-card {
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  overflow: hidden;
  transition: all var(--transition-base);
  height: 100%;
  display: flex;
  flex-direction: column;
}

.research-card:hover {
  transform: translateY(-6px);
  box-shadow: var(--shadow-lg);
  border-color: var(--primary);
}

.research-card-header {
  padding: 1.5rem 1.5rem 1rem;
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-color);
}

.research-card-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--primary);
  margin-bottom: 1rem;
  line-height: 1.3;
}

.research-card-keywords {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.keyword-tag {
  background: var(--primary);
  color: var(--white);
  padding: 0.25rem 0.75rem;
  border-radius: var(--radius-full);
  font-size: 0.8rem;
  font-weight: 500;
}

.research-card-body {
  padding: 1.5rem;
  flex-grow: 1;
}

.research-card-description {
  color: var(--text-secondary);
  font-size: 1rem;
  line-height: 1.6;
  margin-bottom: 1rem;
  font-weight: 500;
}

.research-card-content {
  color: var(--text-secondary);
  font-size: 0.95rem;
  line-height: 1.6;
}

.research-card-footer {
  padding: 1rem 1.5rem 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--bg-secondary);
  border-top: 1px solid var(--border-color);
}

.research-paper-count {
  color: var(--text-muted);
  font-size: 0.9rem;
  font-weight: 500;
}

.methods-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.method-card {
  text-align: center;
  padding: 2rem 1.5rem;
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  transition: all var(--transition-base);
}

.method-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-md);
  border-color: var(--primary);
}

.method-icon {
  width: 80px;
  height: 80px;
  background: var(--primary);
  color: var(--white);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem;
  font-size: 2rem;
  transition: all var(--transition-base);
}

.method-card:hover .method-icon {
  transform: scale(1.1);
  background: var(--primary-dark);
}

.method-card h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 1rem;
}

.method-card p {
  color: var(--text-secondary);
  line-height: 1.6;
  margin: 0;
}

.research-collaborations {
  background: var(--bg-secondary);
  padding: 2rem;
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-color);
}

.collaboration-list {
  list-style: none;
  padding: 0;
  margin: 1.5rem 0 0;
}

.collaboration-list li {
  padding: 0.75rem 0;
  color: var(--text-secondary);
  position: relative;
  padding-left: 2rem;
}

.collaboration-list li::before {
  content: '•';
  color: var(--primary);
  font-weight: bold;
  position: absolute;
  left: 0;
  font-size: 1.5rem;
  line-height: 1;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .research-section-title {
    font-size: 2rem;
  }
  
  .research-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .methods-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .research-card-header,
  .research-card-body,
  .research-card-footer {
    padding: 1rem;
  }
  
  .method-card {
    padding: 1.5rem 1rem;
  }
  
  .method-icon {
    width: 60px;
    height: 60px;
    font-size: 1.5rem;
  }
}

@media (max-width: 480px) {
  .research-intro .lead {
    font-size: 1.1rem;
  }
  
  .research-card-title {
    font-size: 1.25rem;
  }
  
  .method-card h3 {
    font-size: 1.25rem;
  }
  
  .research-collaborations {
    padding: 1.5rem;
  }
}
</style> 