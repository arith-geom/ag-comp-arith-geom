---
layout: page
title: Contact
description: "Contact information for the Computational Arithmetic Geometry group at Heidelberg University, including address, email, and phone."
permalink: /contact/
nav: true
excerpt_separator: ""
---
<div class="contact-grid">
  {% for location in site.data.contact.address %}
  <div class="feature-card location-card">
    <div class="card-header">
      <div class="card-icon">
        <i class="fas fa-map-marker-alt" aria-hidden="true"></i>
      </div>
      <h3>{{ location.title }}</h3>
    </div>
    <div class="card-body">
      <div class="address-block">
        <p><strong>{{ location.institution }}</strong></p>
        <p>{{ location.university }}</p>
        <p>{{ location.street }}</p>
        <p>{{ location.city }}, {{ location.country }}</p>
      </div>
      <div class="location-description">
        <div>{{ location.description | markdownify }}</div>
      </div>
      <div class="map-wrapper">
        <iframe
          width="100%"
          height="300"
          class="contact-map"
          loading="lazy"
          allowfullscreen
          title="Map showing location"
          src="{{ location.map_url }}">
        </iframe>
      </div>
    </div>
  </div>
  {% endfor %}

  {% for detail in site.data.contact.contact_details %}
  <div class="feature-card">
    <div class="card-header">
      <div class="card-icon">
        <i class="fas fa-address-book" aria-hidden="true"></i>
      </div>
      <h3>Contact Details</h3>
    </div>
    <div class="card-body">
      <div class="contact-info">
        <div class="info-item">
          <div class="info-icon">
            <i class="fas fa-phone" aria-hidden="true"></i>
          </div>
          <div class="info-content">
            <strong class="info-label">Phone</strong>
            <span class="info-value">{{ detail.phone }}</span>
            <small class="info-description">{{ detail.phone_hours }}</small>
          </div>
        </div>
        <div class="info-item">
          <div class="info-icon">
            <i class="fas fa-fax" aria-hidden="true"></i>
          </div>
          <div class="info-content">
            <strong class="info-label">Fax</strong>
            <span class="info-value">{{ detail.fax }}</span>
            <small class="info-description">{{ detail.fax_note }}</small>
          </div>
        </div>
      </div>
      <div class="contact-description">
        <div>{{ detail.general_info | markdownify }}</div>
      </div>
    </div>
  </div>
  {% endfor %}

  {% for email in site.data.contact.email %}
  <div class="feature-card">
    <div class="card-header">
      <div class="card-icon">
        <i class="fas fa-envelope" aria-hidden="true"></i>
      </div>
      <h3>Get in Touch</h3>
    </div>
    <div class="card-body">
      <div class="email-info">
        <div>{{ email.intro | markdownify }}</div>
        <div class="email-address">
          <strong>{{ email.address }}</strong>
        </div>
      </div>
      <div class="contact-description">
        <div>{{ email.outro | markdownify }}</div>
      </div>
    </div>
  </div>
  {% endfor %}
</div>
