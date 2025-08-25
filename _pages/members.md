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
  <div class="nav-buttons-container">
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
      {% assign group_leader_slug = group_leader.slug | default: group_leader.name | slugify %}
      {% assign group_leader_key = group_leader.name | slugify | append: '-' | append: group_leader.role | slugify %}
      <div class="member-card featured" data-member-key="{{ group_leader_key }}" data-member-slug="{{ group_leader_slug }}">
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
          <h4 class="member-name-link" data-member-key="{{ group_leader_key }}">{{ group_leader.name }}</h4>
          <p class="member-role">{{ group_leader.role }}</p>
          {% if group_leader.research_interests %}
            <p class="member-description">{{ group_leader.research_interests }}</p>
          {% endif %}
          <div class="member-links">
            <button class="btn btn-outline-primary btn-sm member-profile-btn" data-member-key="{{ group_leader_key }}">
              <i class="fas fa-user me-2" aria-hidden="true"></i>View Profile
            </button>
            {% if group_leader.email %}
              <a href="mailto:{{ group_leader.email }}" class="btn btn-outline-secondary btn-sm">
                <i class="fas fa-envelope me-2" aria-hidden="true"></i>Email
              </a>
            {% endif %}
          </div>
        </div>

        <!-- Expanded Member Detail Content -->
        <div class="member-detail-content" style="display: none;">
          <div class="member-detail-header">
            <button type="button" class="btn btn-outline-primary member-detail-back-btn">
              <i class="fas fa-arrow-left"></i> Back to all members
            </button>
          </div>

          <div class="member-detail-body">
            {% if group_leader.research_interests %}
            <div class="member-detail-section">
              <h3>Research Interests</h3>
              <div class="member-detail-content-text">{{ group_leader.research_interests | markdownify }}</div>
            </div>
            {% endif %}

            {% if group_leader.content or group_leader.description %}
            <div class="member-detail-section">
              <h3>About</h3>
              <div class="member-detail-content-text">{{ group_leader.content | default: group_leader.description | markdownify }}</div>
            </div>
            {% endif %}

            <!-- Publications Section -->
            {% assign member_publications = site.publications | where_exp: "pub", "pub.authors contains group_leader.name" | sort: 'year' | reverse %}
            {% if member_publications.size > 0 %}
            <div class="member-detail-section">
              <h3>
                <i class="fas fa-book" aria-hidden="true"></i>
                Publications ({{ member_publications.size }})
              </h3>
              <div class="member-detail-publications">
                {% for publication in member_publications limit: 5 %}
                <div class="publication-item">
                  <div class="publication-header">
                    <div class="publication-meta">
                      <span class="publication-type">{{ publication.type }}</span>
                      <span class="publication-year">{{ publication.year }}</span>
                    </div>
                    <h4 class="publication-title">
                      {% if publication.pdf %}
                        <a href="{% if publication.pdf contains '://' %}{{ publication.pdf }}{% else %}{{ publication.pdf | relative_url }}{% endif %}" target="_blank" rel="noopener noreferrer">{{ publication.title }}</a>
                      {% elsif publication.url %}
                        <a href="{{ publication.url }}" target="_blank" rel="noopener noreferrer">{{ publication.title }}</a>
                      {% elsif publication.doi %}
                        <a href="https://doi.org/{{ publication.doi }}" target="_blank" rel="noopener noreferrer">{{ publication.title }}</a>
                      {% else %}
                        {{ publication.title }}
                      {% endif %}
                    </h4>
                  </div>
                  <div class="publication-authors">{{ publication.authors }}</div>
                  {% if publication.journal %}
                    <div class="publication-venue">
                      {% if publication.journal_full %}{{ publication.journal_full }}{% else %}{{ publication.journal }}{% endif %}
                      {% if publication.volume %}, Volume {{ publication.volume }}{% endif %}
                      {% if publication.pages %}, {{ publication.pages }}{% endif %}
                      {% if publication.year %}, {{ publication.year }}{% endif %}
                    </div>
                  {% endif %}
                </div>
                {% endfor %}
                {% if member_publications.size > 5 %}
                <div class="view-all-link">
                  <a href="{{ '/publications/' | relative_url }}?author={{ group_leader.name | url_encode }}" class="btn btn-outline-primary btn-sm">
                    View all {{ member_publications.size }} publications
                  </a>
                </div>
                {% endif %}
              </div>
            </div>
            {% endif %}

            <!-- Teaching Section -->
            {% assign member_teaching = site.teaching | where_exp: "course", "course.instructor contains group_leader.name" | sort: 'semester' | reverse %}
            {% if member_teaching.size > 0 %}
            <div class="member-detail-section">
              <h3>
                <i class="fas fa-chalkboard-teacher" aria-hidden="true"></i>
                Teaching ({{ member_teaching.size }} courses)
              </h3>
              <div class="member-detail-teaching">
                {% for course in member_teaching limit: 3 %}
                <div class="teaching-item">
                  <div class="teaching-header">
                    <h4 class="teaching-title">{{ course.title }}</h4>
                    <div class="teaching-meta">
                      <span class="teaching-type">{{ course.course_type }}</span>
                      <span class="teaching-semester">{{ course.semester_key }}</span>
                    </div>
                  </div>
                  <div class="teaching-description">{{ course.description | truncate: 150 }}</div>
                </div>
                {% endfor %}
                {% if member_teaching.size > 3 %}
                <div class="view-all-link">
                  <a href="{{ '/teaching/' | relative_url }}#{{ group_leader_slug }}" class="btn btn-outline-primary btn-sm">
                    View all {{ member_teaching.size }} courses
                  </a>
                </div>
                {% endif %}
              </div>
            </div>
            {% endif %}

            <!-- Research Projects Section -->
            {% assign member_research = site.research | where_exp: "project", "project.members contains group_leader.name" %}
            {% if member_research.size > 0 %}
            <div class="member-detail-section">
              <h3>
                <i class="fas fa-microscope" aria-hidden="true"></i>
                Research Projects ({{ member_research.size }})
              </h3>
              <div class="member-detail-research">
                {% for project in member_research %}
                <div class="research-item">
                  <div class="research-header">
                    <h4 class="research-title">{{ project.title }}</h4>
                    {% if project.status %}
                      <span class="research-status">{{ project.status }}</span>
                    {% endif %}
                  </div>
                  <div class="research-description">{{ project.description | truncate: 200 }}</div>
                </div>
                {% endfor %}
              </div>
            </div>
            {% endif %}

            <!-- Contact Information -->
            <div class="member-detail-section">
              <h3>Contact Information</h3>
              <div class="member-detail-contact">
                {% if group_leader.email %}
                <div class="contact-item">
                  <i class="fas fa-envelope"></i>
                  <a href="mailto:{{ group_leader.email }}">{{ group_leader.email }}</a>
                </div>
                {% endif %}

                {% if group_leader.website %}
                <div class="contact-item">
                  <i class="fas fa-globe"></i>
                  <a href="{{ group_leader.website }}" target="_blank" rel="noopener noreferrer">Personal Website</a>
                </div>
                {% endif %}

                {% if group_leader.github %}
                <div class="contact-item">
                  <i class="fab fa-github"></i>
                  <a href="https://github.com/{{ group_leader.github }}" target="_blank" rel="noopener noreferrer">GitHub Profile</a>
                </div>
                {% endif %}

                {% if group_leader.orcid %}
                <div class="contact-item">
                  <i class="ai ai-orcid"></i>
                  <a href="https://orcid.org/{{ group_leader.orcid }}" target="_blank" rel="noopener noreferrer">ORCID Profile</a>
                </div>
                {% endif %}
              </div>
            </div>
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
          {% assign member_slug = member.slug | default: member.name | slugify %}
          {% assign member_key = member.name | slugify | append: '-' | append: member.role | slugify %}
          <div class="member-card" data-member-key="{{ member_key }}" data-member-slug="{{ member_slug }}">
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
              <h4 class="member-name-link" data-member-key="{{ member_key }}">{{ member.name }}</h4>
              <p class="member-role">{{ member.role }}</p>
              {% if member.research_interests %}
                <p class="member-description">{{ member.research_interests }}</p>
              {% endif %}
              <div class="member-links">
                <button class="btn btn-outline-primary btn-sm member-profile-btn" data-member-key="{{ member_key }}">
                  <i class="fas fa-user me-2" aria-hidden="true"></i>View Profile
                </button>
                {% if member.email %}
                  <a href="mailto:{{ member.email }}" class="btn btn-outline-secondary btn-sm">
                    <i class="fas fa-envelope me-2" aria-hidden="true"></i>Email
                  </a>
                {% endif %}
              </div>
            </div>

            <!-- Expanded Member Detail Content -->
            <div class="member-detail-content" style="display: none;">
              <div class="member-detail-header">
                <button type="button" class="btn btn-outline-primary member-detail-back-btn">
                  <i class="fas fa-arrow-left"></i> Back to all members
                </button>
              </div>

              <div class="member-detail-body">
                {% if member.research_interests %}
                <div class="member-detail-section">
                  <h3>Research Interests</h3>
                  <div class="member-detail-content-text">{{ member.research_interests | markdownify }}</div>
                </div>
                {% endif %}

                {% if member.content or member.description %}
                <div class="member-detail-section">
                  <h3>About</h3>
                  <div class="member-detail-content-text">{{ member.content | default: member.description | markdownify }}</div>
                </div>
                {% endif %}

                <!-- Publications Section -->
                {% assign member_publications = site.publications | where_exp: "pub", "pub.authors contains member.name" | sort: 'year' | reverse %}
                {% if member_publications.size > 0 %}
                <div class="member-detail-section">
                  <h3>
                    <i class="fas fa-book" aria-hidden="true"></i>
                    Publications ({{ member_publications.size }})
                  </h3>
                  <div class="member-detail-publications">
                    {% for publication in member_publications limit: 5 %}
                    <div class="publication-item">
                      <div class="publication-header">
                        <div class="publication-meta">
                          <span class="publication-type">{{ publication.type }}</span>
                          <span class="publication-year">{{ publication.year }}</span>
                        </div>
                        <h4 class="publication-title">
                          {% if publication.pdf %}
                            <a href="{% if publication.pdf contains '://' %}{{ publication.pdf }}{% else %}{{ publication.pdf | relative_url }}{% endif %}" target="_blank" rel="noopener noreferrer">{{ publication.title }}</a>
                          {% elsif publication.url %}
                            <a href="{{ publication.url }}" target="_blank" rel="noopener noreferrer">{{ publication.title }}</a>
                          {% elsif publication.doi %}
                            <a href="https://doi.org/{{ publication.doi }}" target="_blank" rel="noopener noreferrer">{{ publication.title }}</a>
                          {% else %}
                            {{ publication.title }}
                          {% endif %}
                        </h4>
                      </div>
                      <div class="publication-authors">{{ publication.authors }}</div>
                      {% if publication.journal %}
                        <div class="publication-venue">
                          {% if publication.journal_full %}{{ publication.journal_full }}{% else %}{{ publication.journal }}{% endif %}
                          {% if publication.volume %}, Volume {{ publication.volume }}{% endif %}
                          {% if publication.pages %}, {{ publication.pages }}{% endif %}
                          {% if publication.year %}, {{ publication.year }}{% endif %}
                        </div>
                      {% endif %}
                    </div>
                    {% endfor %}
                    {% if member_publications.size > 5 %}
                    <div class="view-all-link">
                      <a href="{{ '/publications/' | relative_url }}?author={{ member.name | url_encode }}" class="btn btn-outline-primary btn-sm">
                        View all {{ member_publications.size }} publications
                      </a>
                    </div>
                    {% endif %}
                  </div>
                </div>
                {% endif %}

                <!-- Teaching Section -->
                {% assign member_teaching = site.teaching | where_exp: "course", "course.instructor contains member.name" | sort: 'semester' | reverse %}
                {% if member_teaching.size > 0 %}
                <div class="member-detail-section">
                  <h3>
                    <i class="fas fa-chalkboard-teacher" aria-hidden="true"></i>
                    Teaching ({{ member_teaching.size }} courses)
                  </h3>
                  <div class="member-detail-teaching">
                    {% for course in member_teaching limit: 3 %}
                    <div class="teaching-item">
                      <div class="teaching-header">
                        <h4 class="teaching-title">{{ course.title }}</h4>
                        <div class="teaching-meta">
                          <span class="teaching-type">{{ course.course_type }}</span>
                          <span class="teaching-semester">{{ course.semester_key }}</span>
                        </div>
                      </div>
                      <div class="teaching-description">{{ course.description | truncate: 150 }}</div>
                    </div>
                    {% endfor %}
                    {% if member_teaching.size > 3 %}
                    <div class="view-all-link">
                      <a href="{{ '/teaching/' | relative_url }}#{{ member_slug }}" class="btn btn-outline-primary btn-sm">
                        View all {{ member_teaching.size }} courses
                      </a>
                    </div>
                    {% endif %}
                  </div>
                </div>
                {% endif %}

                <!-- Research Projects Section -->
                {% assign member_research = site.research | where_exp: "project", "project.members contains member.name" %}
                {% if member_research.size > 0 %}
                <div class="member-detail-section">
                  <h3>
                    <i class="fas fa-microscope" aria-hidden="true"></i>
                    Research Projects ({{ member_research.size }})
                  </h3>
                  <div class="member-detail-research">
                    {% for project in member_research %}
                    <div class="research-item">
                      <div class="research-header">
                        <h4 class="research-title">{{ project.title }}</h4>
                        {% if project.status %}
                          <span class="research-status">{{ project.status }}</span>
                        {% endif %}
                      </div>
                      <div class="research-description">{{ project.description | truncate: 200 }}</div>
                    </div>
                    {% endfor %}
                  </div>
                </div>
                {% endif %}

                <!-- Contact Information -->
                <div class="member-detail-section">
                  <h3>Contact Information</h3>
                  <div class="member-detail-contact">
                    {% if member.email %}
                    <div class="contact-item">
                      <i class="fas fa-envelope"></i>
                      <a href="mailto:{{ member.email }}">{{ member.email }}</a>
                    </div>
                    {% endif %}

                    {% if member.website %}
                    <div class="contact-item">
                      <i class="fas fa-globe"></i>
                      <a href="{{ member.website }}" target="_blank" rel="noopener noreferrer">Personal Website</a>
                    </div>
                    {% endif %}

                    {% if member.github %}
                    <div class="contact-item">
                      <i class="fab fa-github"></i>
                      <a href="https://github.com/{{ member.github }}" target="_blank" rel="noopener noreferrer">GitHub Profile</a>
                    </div>
                    {% endif %}

                    {% if member.orcid %}
                    <div class="contact-item">
                      <i class="ai ai-orcid"></i>
                      <a href="https://orcid.org/{{ member.orcid }}" target="_blank" rel="noopener noreferrer">ORCID Profile</a>
                    </div>
                    {% endif %}
                  </div>
                </div>
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
          {% assign member_slug = member.slug | default: member.name | slugify %}
          {% assign member_key = member.name | slugify | append: '-' | append: member.role | slugify %}
          <div class="member-card" data-member-key="{{ member_key }}" data-member-slug="{{ member_slug }}">
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
              <h4 class="member-name-link" data-member-key="{{ member_key }}">{{ member.name }}</h4>
              <p class="member-role">{{ member.role }}</p>
              {% if member.research_interests %}
                <p class="member-description">{{ member.research_interests }}</p>
              {% endif %}
              <div class="member-links">
                <button class="btn btn-outline-primary btn-sm member-profile-btn" data-member-key="{{ member_key }}">
                  <i class="fas fa-user me-2" aria-hidden="true"></i>View Profile
                </button>
                {% if member.email %}
                  <a href="mailto:{{ member.email }}" class="btn btn-outline-secondary btn-sm">
                    <i class="fas fa-envelope me-2" aria-hidden="true"></i>Email
                  </a>
                {% endif %}
              </div>
            </div>

            <!-- Expanded Member Detail Content -->
            <div class="member-detail-content" style="display: none;">
              <div class="member-detail-header">
                <button type="button" class="btn btn-outline-primary member-detail-back-btn">
                  <i class="fas fa-arrow-left"></i> Back to all members
                </button>
              </div>

              <div class="member-detail-body">
                {% if member.research_interests %}
                <div class="member-detail-section">
                  <h3>Research Interests</h3>
                  <div class="member-detail-content-text">{{ member.research_interests | markdownify }}</div>
                </div>
                {% endif %}

                {% if member.content or member.description %}
                <div class="member-detail-section">
                  <h3>About</h3>
                  <div class="member-detail-content-text">{{ member.content | default: member.description | markdownify }}</div>
                </div>
                {% endif %}

                <!-- Publications Section -->
                {% assign member_publications = site.publications | where_exp: "pub", "pub.authors contains member.name" | sort: 'year' | reverse %}
                {% if member_publications.size > 0 %}
                <div class="member-detail-section">
                  <h3>
                    <i class="fas fa-book" aria-hidden="true"></i>
                    Publications ({{ member_publications.size }})
                  </h3>
                  <div class="member-detail-publications">
                    {% for publication in member_publications limit: 5 %}
                    <div class="publication-item">
                      <div class="publication-header">
                        <div class="publication-meta">
                          <span class="publication-type">{{ publication.type }}</span>
                          <span class="publication-year">{{ publication.year }}</span>
                        </div>
                        <h4 class="publication-title">
                          {% if publication.pdf %}
                            <a href="{% if publication.pdf contains '://' %}{{ publication.pdf }}{% else %}{{ publication.pdf | relative_url }}{% endif %}" target="_blank" rel="noopener noreferrer">{{ publication.title }}</a>
                          {% elsif publication.url %}
                            <a href="{{ publication.url }}" target="_blank" rel="noopener noreferrer">{{ publication.title }}</a>
                          {% elsif publication.doi %}
                            <a href="https://doi.org/{{ publication.doi }}" target="_blank" rel="noopener noreferrer">{{ publication.title }}</a>
                          {% else %}
                            {{ publication.title }}
                          {% endif %}
                        </h4>
                      </div>
                      <div class="publication-authors">{{ publication.authors }}</div>
                      {% if publication.journal %}
                        <div class="publication-venue">
                          {% if publication.journal_full %}{{ publication.journal_full }}{% else %}{{ publication.journal }}{% endif %}
                          {% if publication.volume %}, Volume {{ publication.volume }}{% endif %}
                          {% if publication.pages %}, {{ publication.pages }}{% endif %}
                          {% if publication.year %}, {{ publication.year }}{% endif %}
                        </div>
                      {% endif %}
                    </div>
                    {% endfor %}
                    {% if member_publications.size > 5 %}
                    <div class="view-all-link">
                      <a href="{{ '/publications/' | relative_url }}?author={{ member.name | url_encode }}" class="btn btn-outline-primary btn-sm">
                        View all {{ member_publications.size }} publications
                      </a>
                    </div>
                    {% endif %}
                  </div>
                </div>
                {% endif %}

                <!-- Teaching Section -->
                {% assign member_teaching = site.teaching | where_exp: "course", "course.instructor contains member.name" | sort: 'semester' | reverse %}
                {% if member_teaching.size > 0 %}
                <div class="member-detail-section">
                  <h3>
                    <i class="fas fa-chalkboard-teacher" aria-hidden="true"></i>
                    Teaching ({{ member_teaching.size }} courses)
                  </h3>
                  <div class="member-detail-teaching">
                    {% for course in member_teaching limit: 3 %}
                    <div class="teaching-item">
                      <div class="teaching-header">
                        <h4 class="teaching-title">{{ course.title }}</h4>
                        <div class="teaching-meta">
                          <span class="teaching-type">{{ course.course_type }}</span>
                          <span class="teaching-semester">{{ course.semester_key }}</span>
                        </div>
                      </div>
                      <div class="teaching-description">{{ course.description | truncate: 150 }}</div>
                    </div>
                    {% endfor %}
                    {% if member_teaching.size > 3 %}
                    <div class="view-all-link">
                      <a href="{{ '/teaching/' | relative_url }}#{{ member_slug }}" class="btn btn-outline-primary btn-sm">
                        View all {{ member_teaching.size }} courses
                      </a>
                    </div>
                    {% endif %}
                  </div>
                </div>
                {% endif %}

                <!-- Research Projects Section -->
                {% assign member_research = site.research | where_exp: "project", "project.members contains member.name" %}
                {% if member_research.size > 0 %}
                <div class="member-detail-section">
                  <h3>
                    <i class="fas fa-microscope" aria-hidden="true"></i>
                    Research Projects ({{ member_research.size }})
                  </h3>
                  <div class="member-detail-research">
                    {% for project in member_research %}
                    <div class="research-item">
                      <div class="research-header">
                        <h4 class="research-title">{{ project.title }}</h4>
                        {% if project.status %}
                          <span class="research-status">{{ project.status }}</span>
                        {% endif %}
                      </div>
                      <div class="research-description">{{ project.description | truncate: 200 }}</div>
                    </div>
                    {% endfor %}
                  </div>
                </div>
                {% endif %}

                <!-- Contact Information -->
                <div class="member-detail-section">
                  <h3>Contact Information</h3>
                  <div class="member-detail-contact">
                    {% if member.email %}
                    <div class="contact-item">
                      <i class="fas fa-envelope"></i>
                      <a href="mailto:{{ member.email }}">{{ member.email }}</a>
                    </div>
                    {% endif %}

                    {% if member.website %}
                    <div class="contact-item">
                      <i class="fas fa-globe"></i>
                      <a href="{{ member.website }}" target="_blank" rel="noopener noreferrer">Personal Website</a>
                    </div>
                    {% endif %}

                    {% if member.github %}
                    <div class="contact-item">
                      <i class="fab fa-github"></i>
                      <a href="https://github.com/{{ member.github }}" target="_blank" rel="noopener noreferrer">GitHub Profile</a>
                    </div>
                    {% endif %}

                    {% if member.orcid %}
                    <div class="contact-item">
                      <i class="ai ai-orcid"></i>
                      <a href="https://orcid.org/{{ member.orcid }}" target="_blank" rel="noopener noreferrer">ORCID Profile</a>
                    </div>
                    {% endif %}
                  </div>
                </div>
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
  padding: 2rem 0;
  margin-bottom: 2rem;
  position: relative;
  overflow: hidden;
}

.members-nav-simple::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, transparent 50%, rgba(255, 255, 255, 0.02) 100%);
  pointer-events: none;
  z-index: 1;
}

.nav-buttons-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
  text-align: center;
  position: relative;
  z-index: 2;
}

.nav-btn {
  background: transparent;
  border: 2px solid var(--primary);
  color: var(--primary);
  padding: 0.75rem 2rem;
  margin: 0 0.5rem;
  border-radius: 20px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-family: inherit;
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  letter-spacing: 0.5px;
  text-transform: uppercase;
  font-size: 0.85rem;
  position: relative;
  z-index: 2;
}

.nav-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.6s ease;
}

.nav-btn:hover::before {
  left: 100%;
}

.nav-btn:hover {
  background: var(--primary);
  color: var(--primary-text);
  border-color: var(--primary);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

.nav-btn.active {
  background: var(--primary);
  color: var(--primary-text);
  border-color: var(--primary);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.12);
  transform: translateY(-1px);
}

.nav-btn:active {
  transform: translateY(-1px) scale(1.02);
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

/* Expanded team sections for centered detail display */
.team-sections.expanded {
  max-width: 100% !important;
  width: 100% !important;
  padding: 0 !important;
  margin: 0 !important;
}

/* Additional rules to ensure proper expansion */
.members-content-section:has(.member-card.expanded) {
  width: 100% !important;
  max-width: 100% !important;
  margin: 0 !important;
  padding: 0 !important;
}





/* Debug styles to verify expansion is working */
.member-card.expanded {
  border: 3px solid red !important;
  background: rgba(255, 0, 0, 0.1) !important;
}

.team-sections.expanded {
  border: 2px solid blue !important;
  background: rgba(0, 0, 255, 0.05) !important;
}

.team-section {
  background: transparent;
  border: none;
  border-radius: var(--radius-lg);
  padding: 0;
  box-shadow: none;
}

/* Enhanced dark mode styling for members cards */

[data-theme="dark"] .member-card,
body.dark-mode .member-card {
  background: var(--bg-tertiary) !important;
  border-color: var(--border-dark) !important;
  box-shadow: var(--shadow-md) !important;
}

[data-theme="dark"] .member-card:hover,
body.dark-mode .member-card:hover {
  background: var(--bg-secondary) !important;
  border-color: var(--primary) !important;
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

[data-theme="dark"] .member-card.former,
body.dark-mode .member-card.former {
  background: var(--bg-secondary) !important;
  opacity: 0.9;
}

[data-theme="dark"] .member-card.former:hover,
body.dark-mode .member-card.former:hover {
  background: var(--bg-tertiary) !important;
  opacity: 1;
  border-color: var(--primary) !important;
}

/* Dark mode styling for section headers */
[data-theme="dark"] .section-header,
body.dark-mode .section-header {
  background: transparent !important;
  border-radius: 8px !important;
  padding: 0 !important;
  margin-bottom: 2rem !important;
  border-left: none !important;
}

[data-theme="dark"] .section-icon,
body.dark-mode .section-icon {
  background: var(--primary) !important;
  box-shadow: var(--shadow-md) !important;
}

/* Enhanced member info styling for dark mode */
[data-theme="dark"] .member-info h4,
body.dark-mode .member-info h4 {
  color: var(--text-primary) !important;
  border-bottom: 2px solid var(--primary) !important;
  padding-bottom: 0.5rem !important;
}

[data-theme="dark"] .member-description,
[data-theme="dark"] .member-graduation,
[data-theme="dark"] .member-current,
body.dark-mode .member-description,
body.dark-mode .member-graduation,
body.dark-mode .member-current {
  background: transparent !important;
  padding: 0 !important;
  border-radius: 0 !important;
  margin: 0.5rem 0 !important;
}

/* Dark mode navigation styling */
[data-theme="dark"] .members-nav-simple,
body.dark-mode .members-nav-simple {
  background: transparent !important;
}

[data-theme="dark"] .nav-btn,
body.dark-mode .nav-btn {
  background: rgba(255, 255, 255, 0.05) !important;
  border-color: var(--primary) !important;
  color: var(--primary) !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3) !important;
  backdrop-filter: blur(15px) !important;
}

[data-theme="dark"] .nav-btn:hover,
body.dark-mode .nav-btn:hover {
  background: var(--primary) !important;
  color: var(--primary-text) !important;
  border-color: var(--primary) !important;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4) !important;
}

[data-theme="dark"] .nav-btn.active,
body.dark-mode .nav-btn.active {
  background: var(--primary) !important;
  color: var(--primary-text) !important;
  border-color: var(--primary) !important;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.35) !important;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
  padding: 1.5rem 0;
  position: relative;
}

.section-header::before {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 80px;
  height: 4px;
  background: linear-gradient(90deg, var(--primary), var(--heidelberg-red));
  border-radius: 2px;
}

.section-icon {
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, var(--primary), var(--heidelberg-red));
  color: var(--primary-text);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
  position: relative;
  transition: all 0.3s ease;
}

.section-icon:hover {
  transform: scale(1.1);
  box-shadow: 0 12px 35px rgba(0, 0, 0, 0.2);
}

.section-header h3 {
  margin: 0;
  color: var(--text-primary);
  font-size: 1.4rem;
  font-weight: 700;
  background: linear-gradient(135deg, var(--text-primary), var(--primary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.5px;
}

.members-grid {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1rem 0;
}

.team-sections {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 4rem;
}

.team-section {
  background: transparent;
  border: none;
  border-radius: 0;
  padding: 0;
  box-shadow: none;
}

/* Ensure grid container allows full width for expanded cards */
.members-grid:has(.member-card.expanded) {
  width: 100% !important;
  max-width: 100% !important;
  display: block !important;
  gap: 0 !important;
}

.member-card {
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 0.75rem;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  gap: 0.75rem;
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(10px);
  box-shadow:
    0 2px 12px rgba(0, 0, 0, 0.08),
    0 1px 2px rgba(0, 0, 0, 0.06);
  width: 100%;
}

.member-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--primary), var(--heidelberg-red));
  opacity: 0;
  transition: opacity 0.3s ease;
}

.member-card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow:
    0 20px 60px rgba(0, 0, 0, 0.15),
    0 8px 20px rgba(0, 0, 0, 0.1);
  border-color: var(--primary);
  background: var(--bg-secondary);
}

.member-card:hover::before {
  opacity: 1;
}

.member-card.featured {
  border-color: var(--primary);
  box-shadow: var(--shadow-sm);
}

.member-card.former {
  opacity: 0.9;
  background: var(--bg-secondary);
  flex-direction: column;
  text-align: center;
  border: 2px solid var(--border-color);
  position: relative;
  overflow: hidden;
  width: 100%;
}

.member-card.former::before {
  content: 'FORMER';
  position: absolute;
  top: 15px;
  right: 15px;
  background: var(--text-secondary);
  color: var(--bg-primary);
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.5px;
}

.member-card.former:hover {
  opacity: 1;
  background: var(--bg-primary);
  border-color: var(--primary);
  transform: translateY(-6px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
}

.member-card.former:hover::before {
  background: var(--primary);
  color: var(--primary-text);
}

.member-card.former .member-info {
  width: 100%;
}

/* Unified expanded member card styles */
.member-card.expanded {
  width: 100% !important;
  max-width: 100% !important;
  min-width: 100% !important;
  margin: 0 !important;
  padding: 0 !important;
  display: block !important;
  gap: 0 !important;
  flex-direction: column !important;
  background: rgba(255, 255, 255, 0.02) !important;
  border: 1px solid rgba(255, 255, 255, 0.05) !important;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05) !important;
  box-sizing: border-box !important;
  position: relative;
  overflow: visible !important;
  backdrop-filter: blur(5px) !important;
}

/* Dark mode expanded card background - MINIMAL */
[data-theme="dark"] .member-card.expanded,
body.dark-mode .member-card.expanded {
  background: rgba(0, 0, 0, 0.02) !important;
  border-color: rgba(255, 255, 255, 0.05) !important;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05) !important;
}

/* Transform the member detail content into a unified card */
.member-card.expanded .member-detail-content {
  border-radius: var(--radius-lg) !important;
  margin: 0 !important;
  width: 100% !important;
  max-width: 1200px !important;
  min-width: auto !important;
  margin: 0 auto !important;
}

.member-avatar {
  flex-shrink: 0;
}

.member-avatar {
  position: relative;
}

.member-photo {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  object-fit: contain;
  object-position: center;
  border: 2px solid var(--primary);
  box-shadow:
    0 4px 15px rgba(0, 0, 0, 0.12),
    0 2px 6px rgba(0, 0, 0, 0.08);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  z-index: 2;
  background-color: var(--bg-secondary);
}

.member-card:hover .member-photo {
  transform: scale(1.1);
  border-color: var(--heidelberg-red);
  box-shadow:
    0 15px 40px rgba(0, 0, 0, 0.2),
    0 8px 20px rgba(0, 0, 0, 0.15);
}

.member-photo-placeholder {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary), var(--heidelberg-red));
  border: 2px solid var(--primary);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary-text);
  font-size: 1.5rem;
  font-weight: 600;
  box-shadow:
    0 4px 15px rgba(0, 0, 0, 0.12),
    0 2px 6px rgba(0, 0, 0, 0.08);
  transition: all 0.3s cubic-bezier(0.4, 0, 0, 0.2, 1);
  position: relative;
  z-index: 2;
  overflow: hidden;
}

.member-photo-placeholder i {
  font-size: 1.5rem;
  line-height: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.member-card:hover .member-photo-placeholder {
  transform: scale(1.1);
  box-shadow:
    0 15px 40px rgba(0, 0, 0, 0.2),
    0 8px 20px rgba(0, 0, 0, 0.15);
}

.member-info {
  flex: 1;
}

.member-info h4 {
  margin: 0 0 0.4rem 0;
  color: var(--text-primary);
  font-size: 1rem;
  font-weight: 700;
  line-height: 1.3;
  letter-spacing: -0.01em;
  position: relative;
}

.member-info h4 a {
  color: inherit;
  text-decoration: none;
  transition: all 0.3s ease;
  position: relative;
}

.member-info h4 a::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 0;
  height: 2px;
  background: linear-gradient(90deg, var(--primary), var(--heidelberg-red));
  transition: width 0.3s ease;
}

.member-info h4 a:hover::after {
  width: 100%;
}

.member-role {
  color: var(--primary);
  font-weight: 700;
  margin: 0 0 0.75rem 0;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 1px;
  position: relative;
  display: inline-block;
}

.member-role::before {
  content: '';
  position: absolute;
  bottom: -4px;
  left: 0;
  width: 30%;
  height: 2px;
  background: var(--primary);
  border-radius: 1px;
}

.member-graduation {
  font-size: 0.9rem;
  color: var(--text-secondary);
  margin: 0 0 0.75rem 0;
  font-style: italic;
  background: var(--bg-tertiary);
  padding: 0.5rem 1rem;
  border-radius: 15px;
  display: inline-block;
  border-left: 3px solid var(--primary);
}

.member-current {
  font-size: 0.9rem;
  color: var(--text-secondary);
  margin: 0 0 1rem 0;
  font-weight: 500;
  background: var(--bg-secondary);
  padding: 0.5rem 1rem;
  border-radius: 15px;
  border: 1px solid var(--border-color);
}

.member-description {
  color: var(--text-primary);
  font-size: 0.85rem;
  line-height: 1.4;
  margin: 0 0 1rem 0;
  font-weight: 400;
}

.member-links {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.member-links .btn {
  font-size: 0.8rem;
  padding: 0.4rem 0.8rem;
  border-radius: 12px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  font-weight: 600;
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(10px);
}

.member-links .btn i {
  font-size: 0.75rem;
}

.btn-outline-primary {
  background: var(--bg-primary);
  color: var(--primary);
  border: 2px solid var(--primary);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.btn-outline-primary:hover {
  background: var(--primary);
  color: var(--primary-text);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
  border-color: var(--primary);
}

.btn-outline-secondary {
  background: var(--bg-primary);
  color: var(--text-secondary);
  border: 2px solid var(--border-color);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.btn-outline-secondary:hover {
  background: var(--bg-secondary);
  color: var(--text-primary);
  border-color: var(--primary);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

@media (max-width: 768px) {
  .members-grid {
    gap: 0.75rem;
  }

  .member-card {
    flex-direction: column;
    text-align: center;
    padding: 0.75rem;
    gap: 0.5rem;
  }

  .member-avatar {
    align-self: center;
  }

  .member-info h4 {
    font-size: 0.95rem;
  }

  .member-role {
    font-size: 0.75rem;
  }

  .member-description {
    font-size: 0.8rem;
  }

  .member-links {
    justify-content: center;
  }

  .section-header {
    flex-direction: column;
    text-align: center;
    gap: 0.75rem;
    margin-bottom: 1.5rem;
    padding: 1rem 0;
  }

  .section-icon {
    width: 45px;
    height: 45px;
    font-size: 1rem;
  }

  .section-header h3 {
    font-size: 1.2rem;
  }

  /* Responsive navigation */
  .nav-buttons-container {
    padding: 0 0.5rem;
  }

  .nav-btn {
    padding: 0.6rem 1.5rem;
    margin: 0 0.25rem;
    font-size: 0.8rem;
  }
}

/* Member Detail Content Styles */
.member-detail-content {
  width: 100% !important;
  max-width: min(1200px, 95vw) !important;
  min-width: min(400px, 90vw) !important;
  margin: 2rem auto !important;
  padding: 0;
  background: var(--bg-primary);
  border: 3px solid var(--primary);
  border-radius: var(--radius-xl);
  box-shadow: 0 15px 50px rgba(0, 0, 0, 0.2);
  overflow: hidden;
  box-sizing: border-box !important;
  position: relative;
  z-index: 10;
}

/* Dark mode styles for member detail content - SOLID BACKGROUND */
[data-theme="dark"] .member-detail-content,
body.dark-mode .member-detail-content {
  background: var(--bg-primary) !important;
  border-color: var(--primary) !important;
  box-shadow: 0 15px 50px rgba(0, 0, 0, 0.4) !important;
}

/* Specific styles for expanded member cards */
.member-card.expanded .member-detail-content {
  width: 100% !important;
  max-width: min(1200px, 95vw) !important;
  min-width: min(400px, 90vw) !important;
  margin: 0 !important;
  background: var(--bg-primary) !important;
  border: 3px solid var(--primary) !important;
  border-radius: var(--radius-xl) !important;
  box-shadow: 0 15px 50px rgba(0, 0, 0, 0.2) !important;
}

/* Dark mode expanded card background */
[data-theme="dark"] .member-card.expanded .member-detail-content,
body.dark-mode .member-card.expanded .member-detail-content {
  background: var(--bg-primary) !important;
  border-color: var(--primary) !important;
  box-shadow: 0 15px 50px rgba(0, 0, 0, 0.4) !important;
}

.member-detail-content::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: transparent;
  pointer-events: none;
  z-index: 1;
}

/* Dark mode overlay gradients - REMOVED for readability */
[data-theme="dark"] .member-detail-content::before,
body.dark-mode .member-detail-content::before {
  display: none !important;
}

/* Ensure member detail content is properly displayed */
.members-page .member-detail-content,
.member-detail-content[style*="display: block"] {
  display: block !important;
  width: 100% !important;
  max-width: min(1200px, 95vw) !important;
  min-width: min(400px, 90vw) !important;
  box-sizing: border-box !important;
}

/* Ensure profile images maintain proper aspect ratio and don't stretch */
.member-photo,
.member-photo-placeholder {
  max-width: 100%;
  max-height: 100%;
  aspect-ratio: 1 / 1;
}

.member-card.expanded .member-photo,
.member-card.expanded .member-photo-placeholder {
  max-width: 90px;
  max-height: 90px;
  aspect-ratio: 1 / 1;
}

/* Force full width for all member detail elements */
.member-detail-content,
.member-detail-content * {
  box-sizing: border-box !important;
}

/* MAXIMUM PRIORITY: Ensure ALL text in expanded member cards is readable */
.member-card.expanded,
.member-card.expanded *,
.member-card.expanded .member-detail-content,
.member-card.expanded .member-detail-content *,
.member-card.expanded .member-detail-section,
.member-card.expanded .member-detail-section *,
.member-card.expanded .member-detail-body,
.member-card.expanded .member-detail-body *,
.member-card.expanded h1,
.member-card.expanded h2,
.member-card.expanded h3,
.member-card.expanded h4,
.member-card.expanded h5,
.member-card.expanded h6,
.member-card.expanded p,
.member-card.expanded span,
.member-card.expanded div,
.member-card.expanded strong,
.member-card.expanded b,
.member-card.expanded em,
.member-card.expanded i,
.member-card.expanded a,
.member-card.expanded ul,
.member-card.expanded ol,
.member-card.expanded li {
  color: var(--text-primary) !important;
  border-color: var(--text-primary) !important;
}

/* Specific text color overrides for different elements */
.member-card.expanded h3 {
  color: var(--text-primary) !important;
  border-bottom-color: var(--primary) !important;
}

.member-card.expanded a {
  color: var(--link-color) !important;
}

.member-card.expanded a:hover {
  color: var(--link-hover) !important;
}

/* Ensure all elements inside expanded member card use full width and have proper colors */
.member-card.expanded .member-detail-content,
.member-card.expanded .member-detail-content *,
.member-card.expanded .member-detail-body,
.member-card.expanded .member-detail-section {
  width: 100% !important;
  max-width: min(1200px, 95vw) !important;
  min-width: min(400px, 90vw) !important;
  box-sizing: border-box !important;
  color: var(--text-primary) !important;
}

/* Specific styling for member-detail-section within expanded cards */
.member-card.expanded .member-detail-section {
  background: var(--bg-primary) !important;
  backdrop-filter: blur(10px) !important;
  border: 1px solid var(--border-color) !important;
  border-radius: var(--radius-lg) !important;
  padding: 2rem !important;
  margin-bottom: 2.5rem !important;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08) !important;
  text-align: left !important;
}

/* Ensure all content within expanded member sections is left-aligned */
.member-card.expanded .member-detail-section *,
.member-card.expanded .member-detail-section h3,
.member-card.expanded .member-detail-section p,
.member-card.expanded .member-detail-section div,
.member-card.expanded .member-detail-section span {
  text-align: left !important;
}

/* Dark mode for expanded card sections */
[data-theme="dark"] .member-card.expanded .member-detail-section,
body.dark-mode .member-card.expanded .member-detail-section {
  background: rgba(255, 255, 255, 0.08) !important;
  border-color: rgba(255, 255, 255, 0.2) !important;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.25) !important;
}

/* Ensure member detail sections and their content are always readable */
.member-detail-section,
.member-detail-section * {
  color: var(--text-primary);
}

.member-detail-section p,
.member-detail-section div,
.member-detail-section span {
  color: var(--text-primary);
}

.member-detail-section ul,
.member-detail-section ol,
.member-detail-section li {
  color: var(--text-primary);
}

/* Ensure expanded member card is properly visible and positioned */
.member-card.expanded {
  position: relative !important;
  z-index: 100 !important;
  visibility: visible !important;
  opacity: 1 !important;
  margin: 0 0 2rem 0 !important;
}

/* Hide the view profile button when member detail is expanded */
.member-card.expanded .member-profile-btn,
.member-card.expanded .btn {
  display: none !important;
}

/* Debug styles removed - expansion is working correctly */

.member-detail-content.show {
  display: block !important;
  width: 100% !important;
  max-width: none !important;
  min-width: 100% !important;
  visibility: visible !important;
  opacity: 1 !important;
}

.member-detail-header {
  background: linear-gradient(135deg, var(--primary) 0%, var(--heidelberg-red) 100%);
  color: var(--primary-text);
  padding: 2rem 4rem;
  text-align: center;
  margin-bottom: 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  position: relative;
  z-index: 4;
  width: 100%;
}

.member-detail-back-btn {
  background: var(--primary);
  color: var(--primary-text);
  border: 2px solid var(--primary-text);
  padding: 0.75rem 2rem;
  border-radius: var(--radius-md);
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: var(--transition-base);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1000;
}

.member-detail-back-btn:hover {
  background: var(--primary-hover);
  border-color: var(--primary-hover);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

/* Enhanced member detail header with integrated member info */
.member-detail-header {
  background: linear-gradient(135deg, var(--primary) 0%, var(--heidelberg-red) 100%);
  color: var(--primary-text);
  padding: 2rem 3rem !important;
  margin-bottom: 1rem;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
  position: relative;
  z-index: 4;
  width: 100%;
  border-radius: var(--radius-lg) var(--radius-lg) 0 0 !important;
  flex-wrap: wrap;
}

/* Member info section within expanded header */
.member-card.expanded .member-detail-header {
  flex-direction: row;
  text-align: left;
  justify-content: space-between;
  align-items: center;
  padding: 2rem 3rem !important;
  gap: 1.5rem;
  position: relative;
  z-index: 5;
  flex-wrap: wrap;
}

/* Member avatar styling in expanded header */
.member-card.expanded .member-detail-header .member-avatar {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: auto;
  height: auto;
}

.member-card.expanded .member-detail-header .member-avatar .member-photo {
  width: 80px !important;
  height: 80px !important;
  border: 3px solid var(--primary-text) !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
}

/* Member info styling in expanded header */
.member-card.expanded .member-detail-header .member-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  text-align: left;
  min-width: 0;
  max-width: calc(100% - 200px);
}

/* Back button styling in expanded header */
.member-card.expanded .member-detail-header .member-detail-back-btn {
  flex-shrink: 0;
  white-space: nowrap;
  margin-left: auto;
}

/* Member info text styling in expanded header */
.member-card.expanded .member-detail-header .member-info h4 {
  font-size: 1.5rem !important;
  font-weight: 700 !important;
  margin-bottom: 0.5rem !important;
  color: var(--primary-text) !important;
}

.member-card.expanded .member-detail-header .member-info .member-role {
  font-size: 1.1rem !important;
  font-weight: 500 !important;
  margin-bottom: 0.75rem !important;
  color: var(--primary-text) !important;
  opacity: 0.95 !important;
}

.member-card.expanded .member-detail-header .member-info .member-description {
  font-size: 1rem !important;
  line-height: 1.5 !important;
  margin-bottom: 1rem !important;
  color: var(--primary-text) !important;
  opacity: 0.9 !important;
}

/* Member links styling in expanded header */
.member-card.expanded .member-detail-header .member-info .member-links {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.member-card.expanded .member-detail-header .member-info .member-links .btn {
  font-size: 0.85rem !important;
  padding: 0.4rem 0.8rem !important;
}

.member-card.expanded .member-detail-header .member-photo {
  width: 90px;
  height: 90px;
  border: 3px solid var(--primary-text);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
  display: block !important;
  visibility: visible !important;
  object-fit: contain !important;
  object-position: center !important;
  background-color: var(--bg-secondary) !important;
}

.member-card.expanded .member-detail-header .member-photo-placeholder {
  width: 70px !important;
  height: 70px !important;
  font-size: 2rem !important;
}

.member-card.expanded .member-detail-header .member-photo-placeholder i {
  font-size: 2rem !important;
  line-height: 1 !important;
}

.member-card.expanded .member-detail-header .member-info {
  flex: 1;
  display: flex !important;
  flex-direction: column;
  justify-content: center;
  visibility: visible !important;
}

.member-card.expanded .member-detail-header .member-name-link {
  font-size: 1.8rem;
  font-weight: 800;
  margin-bottom: 0.75rem;
  color: var(--primary-text) !important;
  text-decoration: none;
  line-height: 1.1;
  display: block !important;
  visibility: visible !important;
}

.member-card.expanded .member-detail-header .member-role {
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--primary-text) !important;
  opacity: 0.95;
  margin-bottom: 0.5rem;
  display: block !important;
  visibility: visible !important;
}

.member-card.expanded .member-detail-header .member-description {
  font-size: 1.1rem;
  color: var(--primary-text) !important;
  opacity: 0.9;
  line-height: 1.5;
  margin-bottom: 0;
  display: block !important;
  visibility: visible !important;
}

/* Center member name and role in header for non-expanded view */
.member-detail-header .member-name-link,
.member-detail-header .member-role {
  text-align: center;
  display: block;
  width: 100%;
  margin: 0 auto;
}

.member-detail-header .member-name-link {
  font-size: 1.8rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  color: var(--primary-text);
  text-decoration: none;
}

.member-detail-header .member-role {
  font-size: 1.2rem;
  font-weight: 500;
  color: var(--primary-text);
  opacity: 0.9;
}

.member-detail-body {
  padding: 3rem 4rem;
  max-width: 100% !important;
  width: 100% !important;
  min-width: 100% !important;
  box-sizing: border-box !important;
  text-align: left;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.member-detail-section {
  margin-bottom: 2.5rem;
  background: var(--bg-primary);
  backdrop-filter: blur(10px);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 2rem;
  width: 100% !important;
  max-width: min(1200px, 95vw) !important;
  min-width: min(400px, 90vw) !important;
  box-sizing: border-box !important;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  transition: var(--transition-base);
  text-align: left;
  position: relative;
  z-index: 3;
}

/* Dark mode styles for member detail sections - IMPROVED READABILITY */
[data-theme="dark"] .member-detail-section,
body.dark-mode .member-detail-section {
  background: rgba(255, 255, 255, 0.08) !important;
  border-color: rgba(255, 255, 255, 0.2) !important;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.25) !important;
  backdrop-filter: blur(15px) !important;
}

[data-theme="dark"] .member-detail-section h3,
body.dark-mode .member-detail-section h3 {
  color: var(--text-primary) !important;
}

[data-theme="dark"] .member-detail-content-text,
body.dark-mode .member-detail-content-text {
  color: var(--text-primary) !important;
}

[data-theme="dark"] .member-detail-contact .contact-item,
body.dark-mode .member-detail-contact .contact-item {
  color: var(--text-primary) !important;
}

[data-theme="dark"] .member-detail-contact .contact-item a,
body.dark-mode .member-detail-contact .contact-item a {
  color: var(--primary) !important;
}

/* Light mode member detail sections for better visibility */
.member-detail-section {
  background: var(--bg-primary) !important;
  backdrop-filter: blur(10px) !important;
}

/* Dark mode styles for modern member cards */
[data-theme="dark"] .member-card,
body.dark-mode .member-card {
  background: rgba(20, 20, 30, 0.95) !important;
  border-color: rgba(255, 255, 255, 0.1) !important;
  box-shadow:
    0 4px 20px rgba(0, 0, 0, 0.5),
    0 1px 3px rgba(0, 0, 0, 0.6) !important;
  backdrop-filter: blur(20px) !important;
}

[data-theme="dark"] .member-card:hover,
body.dark-mode .member-card:hover {
  background: rgba(30, 30, 40, 0.98) !important;
  border-color: var(--primary) !important;
  box-shadow:
    0 20px 60px rgba(0, 0, 0, 0.6),
    0 8px 20px rgba(0, 0, 0, 0.4) !important;
  backdrop-filter: blur(25px) !important;
}

[data-theme="dark"] .member-card::before,
body.dark-mode .member-card::before {
  background: linear-gradient(90deg, var(--primary), var(--heidelberg-red)) !important;
}

/* Dark mode styles for member info and typography */
[data-theme="dark"] .member-info h4,
body.dark-mode .member-info h4 {
  color: rgba(255, 255, 255, 0.95) !important;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5) !important;
}

[data-theme="dark"] .member-role,
body.dark-mode .member-role {
  color: var(--primary) !important;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5) !important;
}

[data-theme="dark"] .member-description,
body.dark-mode .member-description {
  color: rgba(255, 255, 255, 0.8) !important;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5) !important;
}

[data-theme="dark"] .member-graduation,
body.dark-mode .member-graduation {
  background: rgba(10, 10, 20, 0.8) !important;
  color: rgba(255, 255, 255, 0.9) !important;
  border-left-color: var(--primary) !important;
  backdrop-filter: blur(10px) !important;
}

[data-theme="dark"] .member-current,
body.dark-mode .member-current {
  background: rgba(15, 15, 25, 0.8) !important;
  color: rgba(255, 255, 255, 0.9) !important;
  border-color: rgba(255, 255, 255, 0.1) !important;
  backdrop-filter: blur(10px) !important;
}

/* Dark mode styles for buttons */
[data-theme="dark"] .btn-outline-primary,
body.dark-mode .btn-outline-primary {
  background: var(--bg-tertiary) !important;
  color: var(--primary) !important;
  border-color: var(--primary) !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3) !important;
}

[data-theme="dark"] .btn-outline-primary:hover,
body.dark-mode .btn-outline-primary:hover {
  background: var(--primary) !important;
  color: var(--primary-text) !important;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4) !important;
}

[data-theme="dark"] .btn-outline-secondary,
body.dark-mode .btn-outline-secondary {
  background: var(--bg-tertiary) !important;
  color: var(--text-secondary) !important;
  border-color: var(--border-color) !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3) !important;
}

[data-theme="dark"] .btn-outline-secondary:hover,
body.dark-mode .btn-outline-secondary:hover {
  background: var(--bg-secondary) !important;
  color: var(--text-primary) !important;
  border-color: var(--primary) !important;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4) !important;
}

/* Improved email button contrast for member cards */
.member-links .btn-outline-secondary {
  font-weight: 700 !important;
  text-shadow: none !important;
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(10px);
}

.member-links .btn-outline-secondary::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
  transition: left 0.5s ease;
}

.member-links .btn-outline-secondary:hover::before {
  left: 100%;
}

/* Light mode email button improvements */
[data-theme="light"] .member-links .btn-outline-secondary,
:root .member-links .btn-outline-secondary {
  background: #F8F9FA !important;
  color: #6B7280 !important;
  border: 2px solid #D1D5DB !important;
  box-shadow: 0 2px 8px rgba(107, 114, 128, 0.15) !important;
}

[data-theme="light"] .member-links .btn-outline-secondary:hover,
:root .member-links .btn-outline-secondary:hover {
  background: #6B7280 !important;
  color: #FFFFFF !important;
  border-color: #6B7280 !important;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(107, 114, 128, 0.3) !important;
}

/* Dark mode email button improvements */
[data-theme="dark"] .member-links .btn-outline-secondary,
body.dark-mode .member-links .btn-outline-secondary {
  background: rgba(30, 30, 40, 0.9) !important;
  color: #9CA3AF !important;
  border: 2px solid #9CA3AF !important;
  box-shadow: 0 2px 8px rgba(156, 163, 175, 0.2) !important;
}

[data-theme="dark"] .member-links .btn-outline-secondary:hover,
body.dark-mode .member-links .btn-outline-secondary:hover {
  background: #9CA3AF !important;
  color: #000000 !important;
  border-color: #9CA3AF !important;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(156, 163, 175, 0.4) !important;
}

/* Improved button contrast for member profile buttons */
.member-links .btn-outline-primary {
  font-weight: 700 !important;
  text-shadow: none !important;
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(10px);
}

.member-links .btn-outline-primary::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
  transition: left 0.5s ease;
}

.member-links .btn-outline-primary:hover::before {
  left: 100%;
}

/* Light mode member profile button improvements */
[data-theme="light"] .member-links .btn-outline-primary,
:root .member-links .btn-outline-primary {
  background: #FFFFFF !important;
  color: #C22032 !important;
  border: 2px solid #C22032 !important;
  box-shadow: 0 2px 8px rgba(194, 32, 50, 0.15) !important;
}

[data-theme="light"] .member-links .btn-outline-primary:hover,
:root .member-links .btn-outline-primary:hover {
  background: #C22032 !important;
  color: #FFFFFF !important;
  border-color: #C22032 !important;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(194, 32, 50, 0.3) !important;
}

/* Dark mode member profile button improvements */
[data-theme="dark"] .member-links .btn-outline-primary,
body.dark-mode .member-links .btn-outline-primary {
  background: rgba(30, 30, 40, 0.9) !important;
  color: #FF6B6B !important;
  border: 2px solid #FF6B6B !important;
  box-shadow: 0 2px 8px rgba(255, 107, 107, 0.2) !important;
}

[data-theme="dark"] .member-links .btn-outline-primary:hover,
body.dark-mode .member-links .btn-outline-primary:hover {
  background: #FF6B6B !important;
  color: #000000 !important;
  border-color: #FF6B6B !important;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4) !important;
}

/* Dark mode styles for navigation */
[data-theme="dark"] .members-nav-simple,
body.dark-mode .members-nav-simple {
  background: rgba(15, 15, 25, 0.9) !important;
  border-color: rgba(255, 255, 255, 0.1) !important;
  backdrop-filter: blur(20px) !important;
}

[data-theme="dark"] .nav-btn,
body.dark-mode .nav-btn {
  background: rgba(20, 20, 30, 0.8) !important;
  color: rgba(255, 255, 255, 0.9) !important;
  border-color: rgba(255, 255, 255, 0.2) !important;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4) !important;
  backdrop-filter: blur(15px) !important;
}

[data-theme="dark"] .nav-btn:hover,
body.dark-mode .nav-btn:hover {
  background: var(--primary) !important;
  color: var(--primary-text) !important;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.6) !important;
}

[data-theme="dark"] .nav-btn.active,
body.dark-mode .nav-btn.active {
  background: var(--primary) !important;
  color: var(--primary-text) !important;
  border-color: var(--primary) !important;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.6) !important;
}

/* Dark mode styles for section headers */
[data-theme="dark"] .section-header h3,
body.dark-mode .section-header h3 {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.9), var(--primary)) !important;
  -webkit-background-clip: text !important;
  -webkit-text-fill-color: transparent !important;
  background-clip: text !important;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5) !important;
}

/* Dark mode styles for former member cards */
[data-theme="dark"] .member-card.former,
body.dark-mode .member-card.former {
  background: rgba(25, 25, 35, 0.9) !important;
  border-color: rgba(255, 255, 255, 0.15) !important;
  backdrop-filter: blur(20px) !important;
}

[data-theme="dark"] .member-card.former:hover,
body.dark-mode .member-card.former:hover {
  background: rgba(35, 35, 45, 0.95) !important;
  border-color: var(--primary) !important;
}

[data-theme="dark"] .member-card.former::before,
body.dark-mode .member-card.former::before {
  background: rgba(255, 255, 255, 0.1) !important;
  color: rgba(255, 255, 255, 0.9) !important;
  border: 1px solid rgba(255, 255, 255, 0.2) !important;
}

[data-theme="dark"] .member-card.former:hover::before,
body.dark-mode .member-card.former:hover::before {
  background: var(--primary) !important;
  color: var(--primary-text) !important;
  border-color: var(--primary) !important;
}

.member-detail-section:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
  border-color: var(--primary-hover);
}

.member-detail-section:last-child {
  margin-bottom: 0;
}

.member-detail-section h3 {
  color: var(--text-primary);
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  padding-bottom: 0.75rem;
  border-bottom: 3px solid var(--primary);
  display: flex;
  align-items: center;
  gap: 0.75rem;
  position: relative;
}

.member-detail-section h3::before {
  content: '';
  position: absolute;
  bottom: -3px;
  left: 0;
  width: 100%;
  height: 3px;
  background: linear-gradient(90deg, var(--primary), var(--primary-hover));
  border-radius: 2px;
}

.member-detail-section h3 i {
  color: var(--primary);
  font-size: 1.1rem;
}

.member-detail-content-text {
  color: var(--text-primary);
  line-height: 1.6;
  font-size: 1rem;
  text-align: left;
}

.member-detail-content-text p {
  margin-bottom: 1rem;
}

.member-detail-content-text h4,
.member-detail-content-text h5 {
  color: var(--text-primary);
  margin-top: 1.5rem;
  margin-bottom: 0.5rem;
}

.member-detail-content-text ul,
.member-detail-content-text ol {
  margin-left: 1.5rem;
  margin-bottom: 1rem;
}

.member-detail-content-text li {
  margin-bottom: 0.5rem;
}

/* Member Detail Publications */
.member-detail-publications {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  width: 100%;
  align-items: stretch;
  justify-content: flex-start;
}

.member-detail-publications .publication-item {
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: 1.25rem;
  transition: var(--transition-base);
  width: 100%;
  box-sizing: border-box;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
}

.member-detail-publications .publication-item:hover {
  border-color: var(--primary);
  box-shadow: var(--shadow-sm);
}

.member-detail-publications .publication-header {
  margin-bottom: 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.member-detail-publications .publication-meta {
  display: flex;
  gap: 0.75rem;
  align-items: center;
  font-size: 0.85rem;
  flex-wrap: wrap;
}

.member-detail-publications .publication-type {
  background: var(--primary);
  color: var(--primary-text);
  padding: 0.25rem 0.75rem;
  border-radius: var(--radius-sm);
  font-weight: 500;
  font-size: 0.8rem;
  white-space: nowrap;
}

.member-detail-publications .publication-year {
  color: var(--text-secondary);
  font-weight: 500;
  font-size: 0.8rem;
}

/* Ensure all publication elements have proper text colors */
.member-detail-publications .publication-item {
  color: var(--text-primary);
}

.member-detail-publications .publication-item * {
  color: inherit;
}

.member-detail-publications .publication-meta span {
  color: var(--text-secondary);
}

.member-detail-publications .publication-authors {
  color: var(--text-primary) !important;
}

.member-detail-publications .publication-venue {
  color: var(--text-secondary) !important;
}

.member-detail-publications .publication-title {
  font-size: 1rem;
  font-weight: 600;
  margin: 0 0 0.5rem 0;
  line-height: 1.4;
  color: var(--text-primary);
}

.member-detail-publications .publication-title a {
  color: var(--link-color);
  text-decoration: none;
  transition: var(--transition-base);
}

.member-detail-publications .publication-title a:hover {
  color: var(--primary);
}

.member-detail-publications .publication-authors {
  color: var(--text-secondary);
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
  font-style: italic;
}

/* Dark mode styling for publications */
[data-theme="dark"] .member-detail-publications .publication-item,
body.dark-mode .member-detail-publications .publication-item {
  background: rgba(255, 255, 255, 0.05) !important;
  border-color: rgba(255, 255, 255, 0.15) !important;
}

[data-theme="dark"] .member-detail-publications .publication-title,
body.dark-mode .member-detail-publications .publication-title {
  color: var(--text-primary) !important;
}

[data-theme="dark"] .member-detail-publications .publication-authors,
body.dark-mode .member-detail-publications .publication-authors {
  color: var(--text-primary) !important;
}

[data-theme="dark"] .member-detail-publications .publication-venue,
body.dark-mode .member-detail-publications .publication-venue {
  color: var(--text-secondary) !important;
}

/* Force publications to stay within bounds */
.member-detail-publications {
  max-width: 100%;
  overflow: hidden;
  contain: layout style paint;
}

.member-detail-publications .publication-item {
  max-width: 100%;
  overflow: hidden;
  word-wrap: break-word;
  overflow-wrap: break-word;
}

/* Ensure publication content doesn't overflow horizontally */
.member-detail-publications .publication-title,
.member-detail-publications .publication-authors,
.member-detail-publications .publication-venue {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 100%;
}

/* Allow wrapping for long titles */
.member-detail-publications .publication-title {
  white-space: normal;
  line-height: 1.3;
}

/* Ensure publications in expanded cards have proper styling and left alignment */
.member-card.expanded .member-detail-publications .publication-item {
  background: var(--bg-secondary) !important;
  border: 1px solid var(--border-color) !important;
  border-radius: var(--radius-md) !important;
  padding: 1.25rem !important;
  width: 100% !important;
  box-sizing: border-box !important;
  flex-shrink: 0 !important;
  display: flex !important;
  flex-direction: column !important;
  align-items: flex-start !important;
  justify-content: flex-start !important;
  text-align: left !important;
  color: var(--text-primary) !important;
}

.member-card.expanded .member-detail-publications .publication-header {
  display: flex !important;
  flex-direction: column !important;
  align-items: flex-start !important;
  justify-content: flex-start !important;
  text-align: left !important;
  width: 100% !important;
}

.member-card.expanded .member-detail-publications .publication-meta {
  display: flex !important;
  flex-direction: row !important;
  align-items: center !important;
  justify-content: flex-start !important;
  text-align: left !important;
  width: 100% !important;
  flex-wrap: wrap !important;
}

.member-card.expanded .member-detail-publications .publication-title {
  text-align: left !important;
  width: 100% !important;
}

.member-card.expanded .member-detail-publications .publication-authors {
  text-align: left !important;
  width: 100% !important;
}

.member-card.expanded .member-detail-publications .publication-venue {
  text-align: left !important;
  width: 100% !important;
}

/* Dark mode for expanded card publications */
[data-theme="dark"] .member-card.expanded .member-detail-publications .publication-item,
body.dark-mode .member-card.expanded .member-detail-publications .publication-item {
  background: rgba(255, 255, 255, 0.05) !important;
  border-color: rgba(255, 255, 255, 0.15) !important;
}

/* Ensure all publication text in expanded cards is readable */
.member-card.expanded .member-detail-publications .publication-item * {
  color: var(--text-primary) !important;
}

.member-card.expanded .member-detail-publications .publication-title {
  color: var(--text-primary) !important;
}

.member-card.expanded .member-detail-publications .publication-authors {
  color: var(--text-primary) !important;
}

.member-card.expanded .member-detail-publications .publication-venue {
  color: var(--text-secondary) !important;
}

.member-card.expanded .member-detail-publications .publication-meta span {
  color: var(--text-secondary) !important;
}

/* Dark mode text colors for expanded card publications */
[data-theme="dark"] .member-card.expanded .member-detail-publications .publication-title,
body.dark-mode .member-card.expanded .member-detail-publications .publication-title {
  color: var(--text-primary) !important;
}

[data-theme="dark"] .member-card.expanded .member-detail-publications .publication-authors,
body.dark-mode .member-card.expanded .member-detail-publications .publication-authors {
  color: var(--text-primary) !important;
}

[data-theme="dark"] .member-card.expanded .member-detail-publications .publication-venue,
body.dark-mode .member-card.expanded .member-detail-publications .publication-venue {
  color: var(--text-secondary) !important;
}

[data-theme="dark"] .member-card.expanded .member-detail-publications .publication-meta span,
body.dark-mode .member-card.expanded .member-detail-publications .publication-meta span {
  color: var(--text-secondary) !important;
}

/* Mobile responsive styling for publications */
@media (max-width: 768px) {
  .member-detail-publications .publication-item {
    padding: 1rem;
    text-align: left !important;
  }

  .member-detail-publications .publication-meta {
    flex-direction: column;
    gap: 0.5rem;
    align-items: flex-start;
    text-align: left !important;
  }

  .member-detail-publications .publication-authors,
  .member-detail-publications .publication-venue {
    white-space: normal;
    overflow: visible;
    text-overflow: clip;
    text-align: left !important;
  }

  .member-card.expanded .member-detail-publications .publication-meta {
    flex-direction: column !important;
    gap: 0.5rem !important;
    align-items: flex-start !important;
    text-align: left !important;
  }
}

@media (max-width: 480px) {
  .member-detail-publications .publication-item {
    padding: 0.75rem;
  }

  .member-detail-publications .publication-title {
    font-size: 0.9rem;
  }

  /* Mobile responsive styling for member detail header */
  .member-detail-header,
  .member-card.expanded .member-detail-header {
    flex-direction: column !important;
    text-align: center !important;
    padding: 1.5rem 2rem !important;
    gap: 1rem !important;
  }

  .member-card.expanded .member-detail-header .member-avatar {
    margin: 0 auto !important;
  }

  .member-card.expanded .member-detail-header .member-info {
    text-align: center !important;
    max-width: 100% !important;
    margin: 0 auto !important;
  }

  .member-card.expanded .member-detail-header .member-detail-back-btn {
    margin: 1rem auto 0 !important;
    width: 100% !important;
    max-width: 200px !important;
  }

  .member-card.expanded .member-detail-header .member-avatar .member-photo {
    width: 70px !important;
    height: 70px !important;
  }
}

.member-detail-publications .publication-venue {
  color: var(--text-secondary);
  font-size: 0.85rem;
  margin-bottom: 0.5rem;
}

/* Member Detail Teaching */
.member-detail-teaching {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.member-detail-teaching .teaching-item {
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: 1rem;
  transition: var(--transition-base);
}

.member-detail-teaching .teaching-item:hover {
  border-color: var(--primary);
  box-shadow: var(--shadow-sm);
}

.member-detail-teaching .teaching-header {
  margin-bottom: 0.75rem;
}

.member-detail-teaching .teaching-title {
  font-size: 1rem;
  font-weight: 600;
  margin: 0 0 0.5rem 0;
  color: var(--text-primary);
}

.member-detail-teaching .teaching-meta {
  display: flex;
  gap: 0.75rem;
  font-size: 0.8rem;
}

.member-detail-teaching .teaching-type {
  background: var(--primary);
  color: var(--primary-text);
  padding: 0.2rem 0.5rem;
  border-radius: var(--radius-sm);
  font-weight: 500;
}

.member-detail-teaching .teaching-semester {
  color: var(--text-secondary);
  font-weight: 500;
}

.member-detail-teaching .teaching-description {
  color: var(--text-secondary);
  font-size: 0.85rem;
  line-height: 1.5;
  margin-bottom: 0.5rem;
}

/* Member Detail Research */
.member-detail-research {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.member-detail-research .research-item {
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: 1rem;
  transition: var(--transition-base);
}

.member-detail-research .research-item:hover {
  border-color: var(--primary);
  box-shadow: var(--shadow-sm);
}

.member-detail-research .research-header {
  margin-bottom: 0.75rem;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
}

.member-detail-research .research-title {
  font-size: 1rem;
  font-weight: 600;
  margin: 0;
  color: var(--text-primary);
}

.member-detail-research .research-status {
  background: var(--primary);
  color: var(--primary-text);
  padding: 0.2rem 0.5rem;
  border-radius: var(--radius-sm);
  font-size: 0.75rem;
  font-weight: 500;
  white-space: nowrap;
  flex-shrink: 0;
}

.member-detail-research .research-description {
  color: var(--text-secondary);
  font-size: 0.85rem;
  line-height: 1.5;
  margin-bottom: 0.5rem;
}

/* Member Detail Contact */
.member-detail-contact {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.member-detail-contact .contact-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: var(--text-secondary);
  font-size: 0.95rem;
}

.member-detail-contact .contact-item i {
  color: var(--primary);
  font-size: 1.1rem;
  width: 20px;
}

.member-detail-contact .contact-item a {
  color: var(--link-color);
  text-decoration: none;
  transition: var(--transition-base);
}

.member-detail-contact .contact-item a:hover {
  color: var(--primary);
}

/* Ensure contact information is readable */
.member-detail-contact .contact-item {
  color: var(--text-primary);
}

.member-detail-contact .contact-item a {
  color: var(--link-color);
  text-decoration: none;
}

.member-detail-contact .contact-item a:hover {
  color: var(--link-hover);
}

/* Ensure all text in member detail sections is readable */
.member-detail-section h4,
.member-detail-section h5,
.member-detail-section h6 {
  color: var(--text-primary);
}

.member-detail-section strong,
.member-detail-section b {
  color: var(--text-primary);
  font-weight: 600;
}

.member-detail-section em,
.member-detail-section i {
  color: var(--text-primary);
}

/* View All Links */
.view-all-link {
  text-align: center;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border-color);
}

.view-all-link .btn {
  font-size: 0.9rem;
}

/* Responsive design for member detail */
@media (max-width: 768px) {
  .member-detail-content {
    width: min(100%, calc(100vw - 2rem)) !important;
    max-width: min(100%, calc(100vw - 2rem)) !important;
    min-width: min(300px, calc(100vw - 2rem)) !important;
    margin: 1rem auto !important;
    border-radius: var(--radius-md);
  }

  .member-detail-header {
    padding: 1.5rem 2rem;
    gap: 1rem;
  }

  .member-detail-header .member-name-link {
    font-size: 1.5rem;
  }

  .member-detail-header .member-role {
    font-size: 1.1rem;
  }

  .member-detail-body {
    padding: 2rem 2.5rem;
    align-items: stretch;
  }

  .member-detail-section {
    padding: 1.5rem;
    margin-bottom: 2rem;
    border-radius: var(--radius-md);
  }

  .member-detail-section h3 {
    font-size: 1.2rem;
  }
}

@media (max-width: 480px) {
  .member-detail-content {
    width: min(100%, calc(100vw - 1rem)) !important;
    max-width: min(100%, calc(100vw - 1rem)) !important;
    min-width: min(280px, calc(100vw - 1rem)) !important;
    margin: 0.5rem auto !important;
    border-radius: var(--radius-sm);
  }

  .member-detail-header {
    padding: 1rem 1.5rem;
    gap: 0.75rem;
  }

  .member-detail-header .member-name-link {
    font-size: 1.3rem;
  }

  .member-detail-header .member-role {
    font-size: 1rem;
  }

  .member-detail-body {
    padding: 1.5rem 2rem;
    align-items: stretch;
  }

  .member-detail-section {
    padding: 1rem;
    margin-bottom: 1.5rem;
  }

  .member-detail-section h3 {
    font-size: 1.1rem;
  }
}

  .member-detail-contact .contact-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
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

// Members Manager for accordion-style member detail views
class MembersManager {
  constructor() {
    this.members = [];
    this.filteredMembers = [];
    this.filters = {
      memberKey: ''
    };
  }

  init() {
    console.log('Initializing MembersManager for accordion-style member views...');
    this.loadMembersFromDOM();
    this.bindEvents();
    this.checkMemberParam();
    this.applyFilters();
    console.log('MembersManager initialized successfully');
  }

  loadMembersFromDOM() {
    // Get all member cards from the DOM
    const memberCards = document.querySelectorAll('.member-card');
    this.members = Array.from(memberCards).map(card => {
      return {
        element: card,
        key: card.dataset.memberKey,
        slug: card.dataset.memberSlug,
        name: card.querySelector('.member-name-link')?.textContent || '',
        role: card.querySelector('.member-role')?.textContent || ''
      };
    });

    console.log(`👥 Loaded ${this.members.length} members from DOM`);
  }

  bindEvents() {
    // Member profile button clicks
    document.addEventListener('click', (e) => {
      const profileBtn = e.target.closest('.member-profile-btn');
      const nameLink = e.target.closest('.member-name-link');

      if (profileBtn || nameLink) {
        e.preventDefault();
        const key = (profileBtn?.dataset.memberKey) || (nameLink?.dataset.memberKey);
        if (key) {
          this.showMemberDetail(key);
        }
      }
    });

    // Back button clicks
    document.addEventListener('click', (e) => {
      const backBtn = e.target.closest('.member-detail-back-btn');
      if (backBtn) {
        e.preventDefault();
        this.hideAllDetails();
      }
    });
  }

  checkMemberParam() {
    // Check for hash-based member parameter
    const hash = window.location.hash.substring(1); // Remove the # symbol
    if (hash.startsWith('member-')) {
      this.filters.memberKey = hash.substring(7); // Remove 'member-' prefix
    }

    // Also check for query parameter as fallback
    const urlParams = new URLSearchParams(window.location.search);
    const memberParam = urlParams.get('member');
    if (memberParam && !this.filters.memberKey) {
      this.filters.memberKey = decodeURIComponent(memberParam);
    }
  }

  applyFilters() {
    console.log('Applying member filters:', this.filters);

    // Hide all detail views first
    this.members.forEach(member => {
      const detailContent = member.element.querySelector('.member-detail-content');
      if (detailContent) {
        detailContent.style.display = 'none';
        detailContent.classList.remove('show');
      }
      // Remove expanded class from all member cards
      member.element.classList.remove('expanded');
    });

    // Remove expanded class from team sections
    const teamSections = document.querySelector('.team-sections');
    if (teamSections) {
      teamSections.classList.remove('expanded');
    }

            // Show detail view for filtered member
        if (this.filters.memberKey) {
          const targetMember = this.members.find(m => m.key === this.filters.memberKey);
          if (targetMember) {
            // First, make sure the target member card is visible and properly positioned
            targetMember.element.style.display = 'block';
            targetMember.element.style.visibility = 'visible';
            targetMember.element.style.zIndex = '100';

            const detailContent = targetMember.element.querySelector('.member-detail-content');
            if (detailContent) {
              // Use both style and class for maximum compatibility
              detailContent.style.display = 'block';
              detailContent.style.visibility = 'visible';
              detailContent.classList.add('show');

              // Add expanded class to the member card for full width styling
              targetMember.element.classList.add('expanded');

              // Add expanded class to team sections for full width container
              const teamSections = document.querySelector('.team-sections');
              if (teamSections) {
                teamSections.classList.add('expanded');
              }

              // Move member info to the expanded header for unified experience
              this.integrateMemberInfo(targetMember.element, detailContent);

              // Hide the "View Profile" button in the expanded card
              const viewProfileBtn = targetMember.element.querySelector('.member-profile-btn');
              if (viewProfileBtn) {
                viewProfileBtn.style.display = 'none';
              }

              // Hide other member cards
              this.members.forEach(member => {
                if (member.key !== this.filters.memberKey) {
                  member.element.style.display = 'none';
                  // Also hide any detail content that might be showing
                  const otherDetail = member.element.querySelector('.member-detail-content');
                  if (otherDetail) {
                    otherDetail.style.display = 'none';
                    otherDetail.classList.remove('show');
                  }
                }
              });

              // Hide navigation buttons and section headers
              this.hideNavigationElements();

              // Show global "Show All Members" button
              this.showGlobalBackButton();

              // Scroll to the member detail
              targetMember.element.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
          }
        } else {
      // Show all members
      this.members.forEach(member => {
        member.element.style.display = 'block';
        member.element.style.visibility = 'visible';
        member.element.style.zIndex = 'auto';

        // Hide any detail content that might be showing
        const detailContent = member.element.querySelector('.member-detail-content');
        if (detailContent) {
          detailContent.style.display = 'none';
          detailContent.classList.remove('show');
        }

        // Remove expanded class and show the "View Profile" button again
        member.element.classList.remove('expanded');
        const viewProfileBtn = member.element.querySelector('.member-profile-btn');
        if (viewProfileBtn) {
          viewProfileBtn.style.display = 'inline-flex';
        }

        // Restore member info visibility
        this.restoreMemberInfo(member.element);
      });

      // Remove expanded class from team sections
      const teamSections = document.querySelector('.team-sections');
      if (teamSections) {
        teamSections.classList.remove('expanded');
      }

      // Show navigation buttons and section headers
      this.showNavigationElements();

      // Hide global "Show All Members" button
      this.hideGlobalBackButton();
    }
  }

  showMemberDetail(memberKey) {
    if (this.filters.memberKey === memberKey) {
      // Already showing this member, hide it
      this.filters.memberKey = '';
      const url = new URL(window.location);
      url.hash = '';
      window.history.replaceState({}, '', url);
    } else {
      // Show this member
      this.filters.memberKey = memberKey;
      const url = new URL(window.location);
      url.hash = `member-${memberKey}`;
      window.history.replaceState({}, '', url);
    }
    this.applyFilters();
  }

  restoreMemberInfo(memberCard) {
    // Restore member info visibility when collapsing expanded view
    const memberAvatar = memberCard.querySelector('.member-avatar');
    const memberInfo = memberCard.querySelector('.member-info');

    if (memberAvatar) {
      memberAvatar.style.display = 'flex';
    }
    if (memberInfo) {
      memberInfo.style.display = 'flex';
    }
  }

  hideAllDetails() {
    this.filters.memberKey = '';
    const url = new URL(window.location);
    url.hash = '';
    window.history.replaceState({}, '', url);

    // Reset all member cards
    this.members.forEach(member => {
      member.element.style.display = 'block';
      member.element.style.visibility = 'visible';
      member.element.style.zIndex = 'auto';
      member.element.classList.remove('expanded');

      // Show the "View Profile" button again
      const viewProfileBtn = member.element.querySelector('.member-profile-btn');
      if (viewProfileBtn) {
        viewProfileBtn.style.display = 'inline-flex';
      }

      // Hide any detail content
      const detailContent = member.element.querySelector('.member-detail-content');
      if (detailContent) {
        detailContent.style.display = 'none';
        detailContent.classList.remove('show');
      }

      // Restore member info visibility
      this.restoreMemberInfo(member.element);
    });

    // Remove expanded class from team sections
    const teamSections = document.querySelector('.team-sections');
    if (teamSections) {
      teamSections.classList.remove('expanded');
    }

    this.applyFilters();
  }

  hideNavigationElements() {
    // Hide navigation buttons
    const navButtons = document.querySelector('.members-nav-simple');
    if (navButtons) {
      navButtons.style.display = 'none';
    }

    // Hide section headers
    const sectionHeaders = document.querySelectorAll('.section-header');
    sectionHeaders.forEach(header => {
      header.style.display = 'none';
    });
  }

  showNavigationElements() {
    // Show navigation buttons
    const navButtons = document.querySelector('.members-nav-simple');
    if (navButtons) {
      navButtons.style.display = 'block';
    }

    // Show section headers
    const sectionHeaders = document.querySelectorAll('.section-header');
    sectionHeaders.forEach(header => {
      header.style.display = 'block';
    });
  }

  integrateMemberInfo(memberCard, detailContent) {
    // Create a unified experience by moving member info to the expanded header
    const memberAvatar = memberCard.querySelector('.member-avatar');
    const memberInfo = memberCard.querySelector('.member-info');
    const detailHeader = detailContent.querySelector('.member-detail-header');

    if (memberAvatar && memberInfo && detailHeader) {
      // Clone and move member avatar and info to the detail header
      const avatarClone = memberAvatar.cloneNode(true);
      const infoClone = memberInfo.cloneNode(true);

      // Clear the existing header content and add the member info
      detailHeader.innerHTML = '';

      // Add the cloned elements to the header
      detailHeader.appendChild(avatarClone);
      detailHeader.appendChild(infoClone);

      // Add the back button to the header
      const backButton = document.createElement('button');
      backButton.type = 'button';
      backButton.className = 'btn btn-outline-primary member-detail-back-btn';
      backButton.innerHTML = '<i class="fas fa-arrow-left"></i> Back to all members';
      detailHeader.appendChild(backButton);

      // Hide the original member avatar and info in the card
      memberAvatar.style.display = 'none';
      memberInfo.style.display = 'none';
    }
  }

  showGlobalBackButton() {
    // Remove existing global back button if it exists
    const existingButton = document.getElementById('global-back-btn');
    if (existingButton) {
      existingButton.remove();
    }

    // Find the team sections container
    const teamSections = document.querySelector('.team-sections');
    if (!teamSections) return;

    // Create and add global back button at the top of the content
    const backButton = document.createElement('div');
    backButton.id = 'global-back-btn';
    backButton.innerHTML = `
      <div class="global-back-container" style="
        position: relative;
        width: 100%;
        max-width: 400px;
        margin: 0 auto 2rem auto;
        background: var(--primary);
        color: var(--primary-text);
        padding: 1rem 2rem;
        border-radius: var(--radius-lg);
        cursor: pointer;
        box-shadow: var(--shadow-md);
        font-weight: 600;
        transition: var(--transition-base);
        border: 2px solid var(--primary-text);
        text-align: center;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
      ">
        <i class="fas fa-users"></i>
        Show All Members
      </div>
    `;

    // Add click handler
    backButton.querySelector('.global-back-container').addEventListener('click', () => {
      this.hideAllDetails();
      // Also remove expanded class from team sections
      const teamSections = document.querySelector('.team-sections');
      if (teamSections) {
        teamSections.classList.remove('expanded');
      }
    });

    // Add hover effect
    backButton.querySelector('.global-back-container').addEventListener('mouseenter', function() {
      this.style.background = 'var(--primary-hover)';
      this.style.transform = 'translateY(-2px)';
      this.style.boxShadow = 'var(--shadow-lg)';
    });

    backButton.querySelector('.global-back-container').addEventListener('mouseleave', function() {
      this.style.background = 'var(--primary)';
      this.style.transform = 'translateY(0)';
      this.style.boxShadow = 'var(--shadow-md)';
    });

    // Apply dark mode styles if needed
    const isDarkMode = document.documentElement.getAttribute('data-theme') === 'dark' ||
                      document.body.classList.contains('dark-mode');
    if (isDarkMode) {
      backButton.querySelector('.global-back-container').style.background = 'var(--primary)';
      backButton.querySelector('.global-back-container').style.color = 'var(--primary-text)';
      backButton.querySelector('.global-back-container').style.borderColor = 'var(--primary-text)';
    }

    // Insert the button at the beginning of the team sections
    teamSections.insertBefore(backButton, teamSections.firstChild);
  }

  hideGlobalBackButton() {
    const existingButton = document.getElementById('global-back-btn');
    if (existingButton) {
      existingButton.remove();
    }
  }
}

// Initialize the members manager when the page loads
document.addEventListener('DOMContentLoaded', () => {
  console.log('🚀 Initializing Members Manager...');
  const membersManager = new MembersManager();

  // Add retry mechanism for URL parameter handling
  const initWithRetry = (retries = 10) => {
    try {
      membersManager.init();

      // Check if we need to show a member from URL parameter
      const urlParams = new URLSearchParams(window.location.search);
      const memberParam = urlParams.get('member');
      if (memberParam) {
        // Give a small delay to ensure DOM is fully ready
        setTimeout(() => {
          membersManager.checkMemberParam();
          membersManager.applyFilters();
        }, 100);
      }
    } catch (error) {
      console.warn('MembersManager init failed, retrying...', error);
      if (retries > 0) {
        setTimeout(() => initWithRetry(retries - 1), 100);
      }
    }
  };

  initWithRetry();

  // Make manager globally accessible for debugging
  window.membersManager = membersManager;

  // Listen for hash changes to handle browser back/forward
  window.addEventListener('hashchange', () => {
    if (window.membersManager) {
      window.membersManager.checkMemberParam();
      window.membersManager.applyFilters();
    }
  });

  // Add mutation observer to ensure proper initialization
  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      if (mutation.type === 'childList' && window.membersManager) {
        // Check if we need to show a member from hash
        const hash = window.location.hash.substring(1);
        if (hash.startsWith('member-') && !window.membersManager.filters.memberKey) {
          const memberKey = hash.substring(7);
          if (window.membersManager.members.find(m => m.key === memberKey)) {
            window.membersManager.filters.memberKey = memberKey;
            window.membersManager.applyFilters();
          }
        }
      }
    });
  });

  // Observe the entire document for changes
  observer.observe(document.body, {
    childList: true,
    subtree: true
  });

  // Immediate initialization check
  const hash = window.location.hash.substring(1);
  if (hash.startsWith('member-')) {
    setTimeout(() => {
      if (window.membersManager && window.membersManager.members.length > 0) {
        window.membersManager.checkMemberParam();
        window.membersManager.applyFilters();
      }
    }, 50);
  }
});

// Fallback initialization on window load
window.addEventListener('load', () => {
  // If membersManager is not initialized or not working properly, retry
  if (!window.membersManager || !window.membersManager.members || window.membersManager.members.length === 0) {
    console.log('🔄 Fallback initialization triggered...');
    setTimeout(() => {
      if (window.membersManager) {
        try {
          window.membersManager.init();
          // Check for hash-based member parameter
          const hash = window.location.hash.substring(1);
          if (hash.startsWith('member-')) {
            window.membersManager.filters.memberKey = hash.substring(7);
            window.membersManager.applyFilters();
          }
          // Also check for query parameter as fallback
          const urlParams = new URLSearchParams(window.location.search);
          const memberParam = urlParams.get('member');
          if (memberParam && !window.membersManager.filters.memberKey) {
            window.membersManager.filters.memberKey = memberParam;
            window.membersManager.applyFilters();
          }
        } catch (error) {
          console.warn('Fallback initialization failed:', error);
        }
      }
    }, 200);
  }
});

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