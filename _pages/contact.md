---
layout: page
title: Contact
permalink: /contact/
nav: true
---
<div class="contact-grid">
  <div class="feature-card location-card">
    <div class="card-header">
      <div class="card-icon">
        <i class="fas fa-map-marker-alt" aria-hidden="true"></i>
      </div>
      <h3>Our Location</h3>
    </div>
    <div class="card-body">
      <div class="address-block">
        <p><strong>{{ site.data.contact.address[0].title }}</strong></p>
        <p>{{ site.data.contact.address[0].institution }}</p>
        <p>{{ site.data.contact.address[0].university }}</p>
        <p>{{ site.data.contact.address[0].street }}</p>
        <p>{{ site.data.contact.address[0].city }}, {{ site.data.contact.address[0].country }}</p>
      </div>
      <div class="location-description">
        <p>{{ site.data.contact.address[0].description }}</p>
      </div>
      <div class="map-wrapper">
        <iframe
          width="100%"
          height="300"
          class="contact-map"
          loading="lazy"
          allowfullscreen
          title="Map showing the location of AG Computational Arithmetic Geometry at Heidelberg University"
          src="{{ site.data.contact.address[0].map_url }}">
        </iframe>
      </div>
    </div>
  </div>

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
            <span class="info-value">{{ site.data.contact.contact_details[0].phone }}</span>
            <small class="info-description">{{ site.data.contact.contact_details[0].phone_hours }}</small>
          </div>
        </div>
        <div class="info-item">
          <div class="info-icon">
            <i class="fas fa-fax" aria-hidden="true"></i>
          </div>
          <div class="info-content">
            <strong class="info-label">Fax</strong>
            <span class="info-value">{{ site.data.contact.contact_details[0].fax }}</span>
            <small class="info-description">{{ site.data.contact.contact_details[0].fax_note }}</small>
          </div>
        </div>
      </div>
      <div class="contact-description">
        <p>{{ site.data.contact.contact_details[0].general_info }}</p>
      </div>
    </div>
  </div>

  <div class="feature-card">
    <div class="card-header">
      <div class="card-icon">
        <i class="fas fa-envelope" aria-hidden="true"></i>
      </div>
      <h3>Get in Touch</h3>
    </div>
    <div class="card-body">
      <div class="email-info">
        <p>{{ site.data.contact.email[0].intro }}</p>
        <div class="email-address">
          <strong>{{ site.data.contact.email[0].address }}</strong>
        </div>
      </div>
      <div class="contact-description">
        <p>{{ site.data.contact.email[0].outro }}</p>
      </div>
    </div>
  </div>
</div>
