---
layout: default
title: Debug Members
permalink: /debug-members/
---

<h1>Debug Members</h1>

<h2>Data Members</h2>
<ul>
{% for member in site.data.members.sections[0].members %}
  <li>
    Name: "{{ member.name }}" <br>
    Length: {{ member.name.size }} <br>
    Bytes: {{ member.name | split: '' | join: ',' }}
  </li>
{% endfor %}
{% for member in site.data.members.sections[1].members %}
  <li>
    Name: "{{ member.name }}" <br>
    Length: {{ member.name.size }} <br>
    Bytes: {{ member.name | split: '' | join: ',' }}
  </li>
{% endfor %}
</ul>

<h2>Site Members</h2>
<ul>
{% for member in site.members %}
  <li>
    Name: "{{ member.name }}" <br>
    Length: {{ member.name.size }} <br>
    Bytes: {{ member.name | split: '' | join: ',' }} <br>
    URL: {{ member.url }}
  </li>
{% endfor %}
</ul>

<h2>Matching Test</h2>
<ul>
{% for member in site.data.members.sections[0].members %}
  {% assign member_page = site.members | where: "name", member.name | first %}
  <li>
    Searching for: "{{ member.name }}" <br>
    Found: {% if member_page %}{{ member_page.name }} ({{ member_page.url }}){% else %}NOT FOUND{% endif %}
  </li>
{% endfor %}
{% for member in site.data.members.sections[1].members %}
  {% assign member_page = site.members | where: "name", member.name | first %}
  <li>
    Searching for: "{{ member.name }}" <br>
    Found: {% if member_page %}{{ member_page.name }} ({{ member_page.url }}){% else %}NOT FOUND{% endif %}
  </li>
{% endfor %}
</ul>
