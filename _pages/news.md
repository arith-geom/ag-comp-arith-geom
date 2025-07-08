---
layout: page
title: News
permalink: /news/
nav: true
---

<div class="news-list mt-5">
  {% for post in site.news reversed %}
    <div class="news-item">
      <h3 class="news-title"><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
      <p class="news-meta text-muted">{{ post.date | date: "%B %d, %Y" }}</p>
      <div class="news-excerpt">
        {{ post.content | strip_html | truncatewords: 50 }}
      </div>
      <a href="{{ post.url | relative_url }}" class="btn btn-sm btn-outline-primary mt-2">Read More</a>
    </div>
  {% endfor %}
</div>

<style>
.news-item {
  margin-bottom: 2.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid var(--border-color);
}
.news-title a {
  text-decoration: none;
}
</style> 