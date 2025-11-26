---
layout: page
title: Debug Members
permalink: /debug-members/
---

<ul>
{% for member in site.members %}
  <li>
    Name: {{ member.name }} <br>
    Slug: {{ member.slug }} <br>
    URL: {{ member.url }} <br>
    Relative URL: {{ member.url | relative_url }} <br>
    Absolute URL: {{ member.url | absolute_url }}
  </li>
{% endfor %}
</ul>
