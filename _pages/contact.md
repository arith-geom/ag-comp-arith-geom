---
layout: page
title: Contact
permalink: /contact/
nav: true
nav_order: 6
---

<div class="contact-intro">
  <p class="lead translatable-content" data-translation-key="contact.intro">Get in touch with our research group. We welcome inquiries from students, researchers, and collaborators interested in arithmetic geometry and computational number theory.</p>
</div>

<div class="row">
  <div class="col-lg-8">
    <div class="contact-info">
      <h3 class="translatable-content" data-translation-key="contact.postal_address">Postal Address</h3>
      <div class="address-card">
        <div class="address-icon">
          <i class="fas fa-map-marker-alt" aria-hidden="true"></i>
        </div>
        <div class="address-content">
          <p class="address-text">
            <strong>AG Computational Arithmetic Geometry</strong><br>
            IWR (Interdisciplinary Center for Scientific Computing)<br>
            University of Heidelberg<br>
            Im Neuenheimer Feld 205<br>
            69120 Heidelberg<br>
            Germany
          </p>
        </div>
      </div>

      <h3 class="mt-4 translatable-content" data-translation-key="contact.contact_details">Contact Details</h3>
      <div class="contact-details">
        <div class="contact-item">
          <div class="contact-icon">
            <i class="fas fa-envelope" aria-hidden="true"></i>
          </div>
          <div class="contact-content">
            <strong>Email:</strong>
            <a href="mailto:sekretariat.boeckle@iwr.uni-heidelberg.de" class="contact-link">
              sekretariat.boeckle@iwr.uni-heidelberg.de
            </a>
          </div>
        </div>
        
        <div class="contact-item">
          <div class="contact-icon">
            <i class="fas fa-phone" aria-hidden="true"></i>
          </div>
          <div class="contact-content">
            <strong>Phone:</strong>
            <a href="tel:+49-6221-54-14734" class="contact-link">
              +49-6221-54-14734
            </a>
          </div>
        </div>
        
        <div class="contact-item">
          <div class="contact-icon">
            <i class="fas fa-fax" aria-hidden="true"></i>
          </div>
          <div class="contact-content">
            <strong>Fax:</strong>
            <span class="contact-text">+49-6221-54-14737</span>
          </div>
        </div>
      </div>

      <h3 class="mt-4 translatable-content" data-translation-key="contact.office_hours">Office Hours</h3>
      <div class="office-hours">
        <p><strong>Monday - Friday:</strong> 9:00 AM - 5:00 PM (CET)</p>
        <p><strong>Weekends:</strong> Closed</p>
        <p class="text-muted small">Please note that we may be unavailable during university holidays and conference periods.</p>
      </div>

      <h3 class="mt-4 translatable-content" data-translation-key="contact.getting_here">Getting Here</h3>
      <div class="directions">
        <h4>By Public Transport</h4>
        <ul>
          <li><strong>Bus:</strong> Lines 32, 33, 35 to "Mathematikon" stop</li>
          <li><strong>Tram:</strong> Line 5 to "Universitätsplatz" then bus connection</li>
          <li><strong>Train:</strong> Heidelberg Hauptbahnhof, then bus connection</li>
        </ul>
        
        <h4>By Car</h4>
        <ul>
          <li>Parking available at Mathematikon building</li>
          <li>Follow signs to "IWR" or "Mathematikon"</li>
          <li>Building is located on the north side of Im Neuenheimer Feld</li>
        </ul>
      </div>
    </div>
  </div>
  
  <div class="col-lg-4">
    <div class="map-container">
      <h3 class="translatable-content" data-translation-key="contact.location">Location</h3>
      <div class="map-wrapper">
        <iframe
          width="100%"
          height="300"
          style="border:0; border-radius: var(--radius-lg);"
          loading="lazy"
          allowfullscreen
          title="Map showing the location of AG Computational Arithmetic Geometry at University of Heidelberg"
          src="https://www.google.com/maps/embed/v1/place?q=place_id:ChIJ70D9Zms_l0cR2z_w-A4-CoY&key={{ site.google_maps_api_key }}">
        </iframe>
      </div>
      <div class="map-actions mt-3">
        <a href="https://maps.google.com/?q=Im+Neuenheimer+Feld+205,+69120+Heidelberg,+Germany" 
           target="_blank" 
           rel="noopener" 
           class="btn btn-outline-primary btn-sm">
          <i class="fas fa-external-link-alt me-2" aria-hidden="true"></i>Open in Google Maps
        </a>
      </div>
    </div>
    
    <div class="quick-links mt-4">
      <h3>Quick Links</h3>
      <div class="quick-links-list">
        <a href="https://www.uni-heidelberg.de/en" target="_blank" rel="noopener" class="quick-link">
          <i class="fas fa-university me-2" aria-hidden="true"></i>University of Heidelberg
        </a>
        <a href="https://www.iwr.uni-heidelberg.de/en" target="_blank" rel="noopener" class="quick-link">
          <i class="fas fa-cogs me-2" aria-hidden="true"></i>IWR Homepage
        </a>
        <a href="https://www.mathi.uni-heidelberg.de/" target="_blank" rel="noopener" class="quick-link">
          <i class="fas fa-square-root-alt me-2" aria-hidden="true"></i>Mathematics Institute
        </a>
        <a href="https://www.uni-heidelberg.de/en/study/degree-programmes" target="_blank" rel="noopener" class="quick-link">
          <i class="fas fa-graduation-cap me-2" aria-hidden="true"></i>Study Programs
        </a>
      </div>
    </div>
  </div>
</div>

<style>
.contact-intro {
  text-align: center;
  max-width: 800px;
  margin: 0 auto 3rem;
}

.contact-intro .lead {
  font-size: 1.25rem;
  color: var(--text-primary);
}

.contact-info h3 {
  color: var(--text-primary);
  font-weight: 600;
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid var(--primary);
  display: inline-block;
}

.address-card {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  background: var(--bg-secondary);
  padding: 1.5rem;
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-color);
  margin-bottom: 1rem;
}

.address-icon {
  width: 40px;
  height: 40px;
  background: var(--primary);
  color: var(--white);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.address-content {
  flex-grow: 1;
}

.address-text {
  margin: 0;
  line-height: 1.6;
  color: var(--text-primary);
}

.contact-details {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: var(--bg-secondary);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-color);
  transition: all var(--transition-base);
}

.contact-item:hover {
  border-color: var(--primary);
  transform: translateX(4px);
}

.contact-icon {
  width: 40px;
  height: 40px;
  background: var(--primary);
  color: var(--white);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.contact-content {
  flex-grow: 1;
}

.contact-link {
  color: var(--link-color);
  text-decoration: none;
  font-weight: 500;
}

.contact-link:hover {
  color: var(--link-hover);
  text-decoration: underline;
}

.contact-text {
  color: var(--text-secondary);
  font-weight: 500;
}

.office-hours {
  background: var(--bg-secondary);
  padding: 1.5rem;
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-color);
}

.office-hours p {
  margin-bottom: 0.5rem;
  color: var(--text-primary);
}

.directions h4 {
  color: var(--primary);
  font-weight: 600;
  margin: 1.5rem 0 1rem;
  font-size: 1.1rem;
}

.directions ul {
  list-style: none;
  padding: 0;
  margin: 0 0 1.5rem;
}

.directions li {
  padding: 0.5rem 0;
  color: var(--text-secondary);
  position: relative;
  padding-left: 1.5rem;
}

.directions li::before {
  content: '→';
  color: var(--primary);
  position: absolute;
  left: 0;
  font-weight: bold;
}

.map-container {
  background: var(--bg-secondary);
  padding: 1.5rem;
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-color);
}

.map-container h3 {
  margin-bottom: 1rem;
  color: var(--text-primary);
  font-weight: 600;
}

.map-wrapper {
  position: relative;
  overflow: hidden;
  border-radius: var(--radius-lg);
}

.map-actions {
  text-align: center;
}

.quick-links {
  background: var(--bg-secondary);
  padding: 1.5rem;
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-color);
}

.quick-links h3 {
  margin-bottom: 1rem;
  color: var(--text-primary);
  font-weight: 600;
}

.quick-links-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.quick-link {
  display: flex;
  align-items: center;
  padding: 0.75rem 1rem;
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  color: var(--text-primary);
  text-decoration: none;
  transition: all var(--transition-base);
  font-weight: 500;
}

.quick-link:hover {
  background: var(--primary);
  color: var(--white);
  border-color: var(--primary);
  transform: translateX(4px);
  text-decoration: none;
}

/* Responsive adjustments */
@media (max-width: 991px) {
  .map-container,
  .quick-links {
    margin-top: 2rem;
  }
}

@media (max-width: 768px) {
  .contact-intro .lead {
    font-size: 1.1rem;
  }
  
  .address-card,
  .contact-item {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }
  
  .contact-item:hover {
    transform: translateY(2px);
  }
  
  .quick-link:hover {
    transform: translateY(2px);
  }
  
  .directions li {
    padding-left: 1rem;
  }
}

@media (max-width: 480px) {
  .contact-info h3 {
    font-size: 1.25rem;
  }
  
  .address-card,
  .contact-item,
  .office-hours,
  .map-container,
  .quick-links {
    padding: 1rem;
  }
  
  .address-icon,
  .contact-icon {
    width: 35px;
    height: 35px;
  }
}
</style> 