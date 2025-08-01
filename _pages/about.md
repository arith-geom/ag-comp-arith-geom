---
layout: page
title: About
permalink: /about/
nav: true
---

<div class="translatable-content" data-translation-key="about.description">
  This is the website of the research group "computational arithmetic geometry" at the Interdisciplinary Center for Scientific Computing (IWR) in Heidelberg.
</div>

<div class="translatable-content" data-translation-key="about.content">
  Within algebraic number theory and arithmetic geometry, the focus of the research group is on Galois representations, their relations to modular forms and elliptic curves, their deformation theory etc., as well as on some aspects of function field arithmetic such as L-functions and Drinfeld modular forms.
</div>

<div class="translatable-content" data-translation-key="about.methods">
  To tackle problems in the themes described above, we apply a broad range of methods. On one hand we pursue these questions by purely theoretical methods. On the other, we use computer algebra to carry out experiments that help us gather examples for the theory or to solve particular questions that arise from the theory. Some members of our group have also developed routines on top of existing computer algebra packages.
</div>

<div class="translatable-content" data-translation-key="about.more_info">
  A more detailed survey of our activities can be found in the research section and in the publications of our members.
</div>

---

<h2 class="mt-5 translatable-content" data-translation-key="about.latest_news">Latest News</h2>
<div class="news-list-home mt-4">
  {% for post in site.news limit:3 %}
    <div class="news-item-home">
      <p class="news-meta-home text-muted">{{ post.date | date: "%B %d, %Y" }}</p>
      <h4 class="news-title-home"><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h4>
      <p>{{ post.content | strip_html | truncatewords: 30 }}</p>
    </div>
  {% endfor %}
  <a href="{{ '/news/' | relative_url }}" class="btn btn-outline-primary mt-3 translatable-content" data-translation-key="about.view_all_news">View all news</a>
</div>

<style>
.news-item-home {
  padding-bottom: 1rem;
  margin-bottom: 1rem;
  border-bottom: 1px solid var(--border-color);
}
.news-title-home a {
  text-decoration: none;
}
</style> 